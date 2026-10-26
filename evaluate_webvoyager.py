#!/usr/bin/env python3
"""Post-hoc screenshot judging for Webwright's WebVoyager artifacts.

Python 3.6+; optional JPEG transport requires Pillow. Original artifacts are read-only.
"""

import argparse
import base64
import csv
import getpass
import hashlib
import io
import json
import math
import mimetypes
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Verbatim prompts from upstream WebVoyager evaluation/auto_eval.py.
PROMPT_SOURCE = "https://github.com/MinorJerry/WebVoyager/blob/main/evaluation/auto_eval.py"
SYSTEM_PROMPT = """As an evaluator, you will be presented with three primary components to assist you in your role:

1. Web Task Instruction: This is a clear and specific directive provided in natural language, detailing the online activity to be carried out. These requirements may include conducting searches, verifying information, comparing prices, checking availability, or any other action relevant to the specified web service (such as Amazon, Apple, ArXiv, BBC News, Booking etc).

2. Result Screenshots: This is a visual representation of the screen showing the result or intermediate state of performing a web task. It serves as visual proof of the actions taken in response to the instruction.

3. Result Response: This is a textual response obtained after the execution of the web task. It serves as textual result in response to the instruction.

-- You DO NOT NEED to interact with web pages or perform actions such as booking flights or conducting searches on websites.
-- You SHOULD NOT make assumptions based on information not presented in the screenshot when comparing it to the instructions.
-- Your primary responsibility is to conduct a thorough assessment of the web task instruction against the outcome depicted in the screenshot and in the response, evaluating whether the actions taken align with the given instructions.
-- NOTE that the instruction may involve more than one task, for example, locating the garage and summarizing the review. Failing to complete either task, such as not providing a summary, should be considered unsuccessful.
-- NOTE that the screenshot is authentic, but the response provided by LLM is generated at the end of web browsing, and there may be discrepancies between the text and the screenshots.
-- Note the difference: 1) Result response may contradict the screenshot, then the content of the screenshot prevails, 2) The content in the Result response is not mentioned on the screenshot, choose to believe the content.

You should elaborate on how you arrived at your final evaluation and then provide a definitive verdict on whether the task has been successfully accomplished, either as 'SUCCESS' or 'NOT SUCCESS'."""

USER_PROMPT = """TASK: <task>
Result Response: <answer>
<num> screenshots at the end: """

VERDICT_PROMPT = "Your verdict:\n"

SCHEMA_VERSION = 1
ANSWER_SOURCE = "final_response.txt (fallback: final_script_log.txt:Final Response)"
ANSWER_POLICY = ("Use the selected run's final_response.txt when it contains a usable answer. If that file is absent, empty, or incomplete, "
                 "extract the last non-empty Final Response block from that same run's "
                 "final_script_log.txt. Never use evidence files or older runs; INCOMPLETE "
                 "placeholders are excluded.")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
TRANSIENT_HTTP_CODES = {408, 409, 425, 429, 500, 502, 503, 504}
TERMINAL_STATUSES = {"success", "failure", "missing_evidence", "parse_error"}
CSV_FIELDS = [
    "task_id", "website", "status", "predicted_label", "task", "answer",
    "answer_input_mode", "answer_source", "answer_file_sha256",
    "task_record", "final_run", "screenshot_count", "response_model",
    "api_attempts", "error", "judge_reasoning",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def natural_key(value: str) -> tuple:
    return tuple((1, int(p)) if p.isdigit() else (0, p.lower())
                 for p in re.split(r"(\d+)", value))


def digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def safe_name(value: str) -> str:
    clean = re.sub(r"[^\w.-]+", "_", value, flags=re.UNICODE).strip("._") or "task"
    return clean[:100] + "_" + hashlib.sha256(value.encode()).hexdigest()[:8]


def record_order(record: dict) -> tuple:
    name = record["directory"].name
    timestamp = re.search(r"_(\d{8}_\d{6})$", name)
    return (timestamp.group(1) if timestamp else "", natural_key(str(record["directory"])))


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def discover_records(input_root: Path) -> Dict[str, List[dict]]:
    grouped = defaultdict(list)
    for directory, children, files in os.walk(input_root, followlinks=False):
        children[:] = sorted(c for c in children if c not in {".git", "__pycache__"})
        if "task.json" not in files:
            continue
        task_path = Path(directory) / "task.json"
        task = read_json(task_path)
        if not isinstance(task, dict) or not isinstance(task.get("task_id"), str):
            raise ValueError(f"Invalid task_id in {task_path}")
        if not isinstance(task.get("task"), str) or not task["task"].strip():
            raise ValueError(f"Missing task instruction in {task_path}")
        task_id = task["task_id"]
        grouped[task_id].append({"directory": Path(directory), "definition": task})
        children[:] = []
    if not grouped:
        raise ValueError(f"No task.json records found under {input_root}")
    return dict(grouped)


def latest_final_run(record_directory: Path) -> Optional[Path]:
    parent = record_directory / "final_runs"
    if not parent.is_dir():
        return None
    runs = [p for p in parent.iterdir() if p.is_dir() and re.fullmatch(r"run_\d+", p.name)]
    return max(runs, key=lambda p: int(p.name.split("_")[-1])) if runs else None


def final_answer(run_directory: Path) -> Tuple[str, str]:
    """Read the selected run's answer, with a narrowly scoped log fallback.

    ``final_response.txt`` is authoritative when it contains a usable answer.
    If it is absent, empty, or marked ``[INCOMPLETE]``, extract a labelled
    ``Final Response`` block from the same run's ``final_script_log.txt``.
    Evidence JSON files and older runs are intentionally never consulted.
    """
    answer_path = run_directory / "final_response.txt"
    if answer_path.is_file():
        answer = answer_path.read_text(encoding="utf-8").strip()
        if answer and not answer.startswith("[INCOMPLETE]"):
            return answer, "final_response.txt"
        # An empty/incomplete artifact is unusable; apply the same scoped
        # fallback as for a missing file rather than consulting another run.

    log_path = run_directory / "final_script_log.txt"
    if log_path.is_file():
        answer = extract_final_response_from_log(log_path)
        if answer:
            return answer, "final_script_log.txt:Final Response"
    return "", "missing"


def extract_final_response_from_log(log_path: Path) -> str:
    """Extract the last complete, labelled Final Response block from a log."""
    text = log_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    marker = re.compile(
        r"^\s*(?:(?:\[[^\]\r\n]+\]|\d{4}-\d{2}-\d{2}T\S+)\s*)?"
        r"Final[ _]Response:[ \t]*(.*?)[ \t]*$", re.IGNORECASE)
    boundary = re.compile(
        r"^\s*(?:\[[^\]\r\n]+\]\s*)?(?:"
        r"TASK(?:_|\s+)(?:SUCCESS|FAILURE|COMPLETE|COMPLETED)\b|"
        r"FINAL_SCRIPT(?:_(?:SUCCESS|FAILURE|COMPLETE|COMPLETED))?\b|"
        r"DONE\b|EXIT(?:_CODE)?\s*[:=]|RC\s*=|BROWSER_ADVISORY\s*:|"
        r"(?:CP\d+|Screenshot saved)\s*:|RUNTIME_VALIDATION\s*:|"
        r"evidence\.(?:finish|written|saved)\b|Evidence\s+(?:finished|written|saved)\b|"
        r"(?:LOG WRITTEN|RUN_DIR|RUN COMPLETE|RUN END|RUN_END)\s*[:=]?)",
        re.IGNORECASE,
    )
    timestamped_event = re.compile(
        r"^\s*(?:\[(?:\d{2}:\d{2}:\d{2}|\d{4}-\d{2}-\d{2}T)[^\]]*\]|"
        r"\d{4}-\d{2}-\d{2}T\S+)"
    )
    starts = [(index, match.group(1)) for index, line in enumerate(lines)
              for match in [marker.match(line)] if match]
    for candidate_index in range(len(starts) - 1, -1, -1):
        start_index, first_line = starts[candidate_index]
        next_marker = starts[candidate_index + 1][0] if candidate_index + 1 < len(starts) else len(lines)
        answer_lines = [first_line]
        for line in lines[start_index + 1:next_marker]:
            if boundary.match(line) or timestamped_event.match(line):
                break
            answer_lines.append(line)
        answer = "\n".join(answer_lines).strip()
        if answer and not answer.startswith("[INCOMPLETE]"):
            return answer
    return ""


def evaluation_answer(run_directory: Path) -> Tuple[str, str]:
    return final_answer(run_directory)


def evaluation_system_prompt() -> str:
    return SYSTEM_PROMPT


def screenshot_files(run_directory: Path) -> Tuple[List[Path], str]:
    screenshots_root = run_directory / "screenshots"
    if not screenshots_root.is_dir():
        return [], "screenshots_directory_missing"
    available = sorted(
        (p for p in screenshots_root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES),
        key=lambda p: natural_key(p.relative_to(screenshots_root).as_posix()),
    )
    manifest_path = run_directory / "run_manifest.json"
    if manifest_path.is_file():
        manifest = read_json(manifest_path)
        listed = manifest.get("screenshots", []) if isinstance(manifest, dict) else []
        if listed:
            ordered = []
            for value in listed:
                if not isinstance(value, str):
                    raise ValueError("run_manifest screenshot entry must be a path string")
                path = Path(value)
                if path.is_absolute():
                    matches = [p for p in available if p.name == path.name]
                    if len(matches) != 1:
                        raise ValueError(f"Cannot map manifest screenshot: {path.name}")
                    path = matches[0]
                else:
                    path = run_directory / path
                if not is_within(path.resolve(), screenshots_root.resolve()):
                    raise ValueError("Screenshot is outside the selected run's screenshots directory")
                if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                    raise ValueError(f"Missing/unsupported manifest screenshot: {path.name}")
                if path not in ordered:
                    ordered.append(path)
            return ordered, "run_manifest_sequence"
    return available, "natural_filename_order"


def prepare_selection(grouped: Dict[str, List[dict]], input_root: Path,
                      websites: List[str], task_ids: List[str], limit: int,
                      max_images: int) -> List[dict]:
    selected = []
    for task_id in sorted(grouped, key=natural_key):
        website = task_id.rsplit("--", 1)[0]
        if websites and website not in websites and website.replace(" ", "_") not in websites:
            continue
        if task_ids and task_id not in task_ids:
            continue
        records = sorted(grouped[task_id], key=record_order)
        record = records[-1]
        directory = record["directory"]
        relative_record = directory.relative_to(input_root).as_posix()
        run = latest_final_run(directory)
        item = {
            "task_id": task_id, "website": website,
            "task": record["definition"]["task"],
            "task_record": relative_record,
            "task_definition_sha256": file_digest(directory / "task.json"),
            "candidate_record_count": len(records),
            "candidate_records": [r["directory"].relative_to(input_root).as_posix() for r in records],
            "final_run": run.name if run else None,
            "answer_input_mode": "final_response.txt with final_script_log.txt fallback",
            "answer": "", "answer_source": "missing", "screenshots": [],
            "screenshot_order": None, "input_error": None,
        }
        if run is None:
            item["input_error"] = "No final_runs/run_NNN execution found."
        else:
            try:
                item["answer"], item["answer_source"] = evaluation_answer(run)
                if item["answer"]:
                    source_path = run / ("final_response.txt" if item["answer_source"] == "final_response.txt"
                                         else "final_script_log.txt")
                    item["answer_file_sha256"] = file_digest(source_path)
                screenshots, order = screenshot_files(run)
                screenshots = screenshots[-max_images:]
                item["screenshot_order"] = order
                item["screenshots"] = [
                    {"path": p.relative_to(input_root).as_posix(), "sha256": file_digest(p)}
                    for p in screenshots
                ]
                missing = []
                if not item["answer"]:
                    missing.append("answer (final_response.txt or final_script_log.txt:Final Response)")
                if not screenshots:
                    missing.append("execution screenshots")
                if missing:
                    item["input_error"] = "Missing " + " and ".join(missing)
            except (OSError, ValueError) as error:
                item["input_error"] = f"Evidence error: {error}"
        item["fingerprint"] = digest(item)
        selected.append(item)
        if limit and len(selected) >= limit:
            break
    if not selected:
        raise ValueError("No tasks matched the requested filters")
    absent = set(task_ids) - {item["task_id"] for item in selected}
    if absent and not limit:
        raise ValueError("Requested task IDs not found: " + ", ".join(sorted(absent)))
    return selected


# def parse_verdict(response: str) -> Optional[int]:
#     """Parse only an unambiguous terminal verdict."""
#     lines = [re.sub(r"[*`_]", "", line).strip().lstrip("# ")
#              for line in response.splitlines() if line.strip()]
#     if not lines:
#         return None
#     match = re.fullmatch(
#         r"(?:(?:final\s+verdict|verdict|status)\s*:\s*)?(NOT\s+SUCCESS|SUCCESS)[.!]?",
#         lines[-1], flags=re.IGNORECASE,
#     )
#     if not match:
#         return None
#     return 0 if re.fullmatch(r"NOT\s+SUCCESS", match.group(1), re.IGNORECASE) else 1
def parse_verdict(response: str) -> Optional[int]:
    """Parse an explicit verdict on the response's final non-empty line.

    Judges commonly wrap the terminal verdict in Markdown (for example,
    ``### **Final Verdict: NOT SUCCESS**``) or put an emoji before it.  Those
    decorations are presentation, not additional evidence, so normalize them
    while retaining the conservative requirement for an explicit
    ``Verdict``/``Final Verdict``/``Status`` label.
    """
    lines = [line for line in response.splitlines() if line.strip()]
    if not lines:
        return None

    # Only inspect the terminal line; do not let a verdict mentioned in the
    # reasoning override an absent or contradictory final verdict.
    last_line = lines[-1]
    # Remove Markdown punctuation and non-text decorations (such as ✅), then
    # normalize whitespace.  Keep ':' so the labelled form remains explicit.
    normalized = re.sub(r"[`*_\[\]#>()]", " ", last_line)
    normalized = re.sub(r"[^\w\s:.-]", " ", normalized, flags=re.UNICODE)
    normalized = re.sub(r"\s+", " ", normalized).strip().upper()

    # The upstream prompt also permits a bare terminal verdict.
    bare = re.fullmatch(r"(NOT\s+SUCCESS|SUCCESS)[.!]?", normalized)
    if bare:
        return 0 if bare.group(1).startswith("NOT") else 1

    match = re.fullmatch(
        r"(?:FINAL\s+VERDICT|VERDICT|STATUS)\s*:?\s*"
        r"(NOT\s+SUCCESS|SUCCESS)[.!]?",
        normalized,
    )
    if not match:
        return None
    return 0 if match.group(1).startswith("NOT") else 1


def image_transport_policy(image_format: str, jpeg_quality: int,
                           image_resize: str = "none", image_tile_height: int = 0,
                           image_tile_overlap: int = 128) -> dict:
    if image_format not in {"original", "jpeg"}:
        raise ValueError("Unknown image format")
    if not 1 <= jpeg_quality <= 100:
        raise ValueError("JPEG quality must be between 1 and 100")
    if image_resize not in {"none", "fit"}:
        raise ValueError("Unknown image resize mode")
    if image_tile_height < 0 or image_tile_overlap < 0:
        raise ValueError("Image tile height and overlap must be nonnegative")
    if image_tile_height and image_tile_overlap >= image_tile_height:
        raise ValueError("Image tile overlap must be smaller than tile height")
    if image_tile_height and image_resize != "none":
        raise ValueError("Image tiling preserves source resolution; do not combine it with resizing")
    if image_format == "original":
        if image_resize != "none" or image_tile_height:
            raise ValueError("Image resizing/tiling requires --image-format jpeg; original preserves exact bytes")
        return {"format": "original", "resize": False, "crop": False}
    try:
        import PIL
    except ImportError as error:
        raise ValueError("JPEG transport requires Pillow. Install it: python3 -m pip install Pillow") from error
    policy = {"format": "jpeg", "quality": jpeg_quality, "subsampling": 0,
              "resize": image_resize == "fit", "crop": bool(image_tile_height),
              "alpha_background": "white", "pillow_version": PIL.__version__}
    if image_resize == "fit":
        policy["max_size"] = "1280x1280"
    if image_tile_height:
        policy["tiling"] = {"height": image_tile_height, "overlap": image_tile_overlap,
                            "order": "top_to_bottom", "full_coverage": True}
    return policy


def jpeg_bytes(image: Any, quality: int) -> bytes:
    with io.BytesIO() as output:
        image.save(output, format="JPEG", quality=quality, subsampling=0)
        return output.getvalue()


def encode_image(contents: bytes, filename: str, image_format: str = "original",
                 jpeg_quality: int = 90, image_resize: str = "none") -> Tuple[bytes, str, dict]:
    policy = image_transport_policy(image_format, jpeg_quality, image_resize)
    mime = mimetypes.guess_type(filename)[0] or "image/png"
    metadata = {"source_sha256": hashlib.sha256(contents).hexdigest(),
                "source_bytes": len(contents), "transport_policy": policy}
    if image_format == "jpeg":
        from PIL import Image
        with Image.open(io.BytesIO(contents)) as image:
            dimensions = list(image.size)
            rgba = image.convert("RGBA")
            rgb = Image.new("RGB", image.size, "white")
            rgb.paste(rgba, mask=rgba.getchannel("A"))
            if image_resize == "fit":
                rgb.thumbnail((1280, 1280), Image.Resampling.LANCZOS)
            new_dimensions = list(rgb.size)
            contents = jpeg_bytes(rgb, jpeg_quality)
        mime = "image/jpeg"
        metadata.update(source_dimensions=dimensions, transmitted_dimensions=new_dimensions)
    metadata.update(transmitted_bytes=len(contents), transmitted_mime=mime,
                    transmitted_sha256=hashlib.sha256(contents).hexdigest())
    return contents, mime, metadata


def encode_image_parts(contents: bytes, filename: str, image_format: str = "original",
                       jpeg_quality: int = 90, image_resize: str = "none",
                       image_tile_height: int = 0,
                       image_tile_overlap: int = 128) -> List[Tuple[bytes, str, dict]]:
    """Encode whole images by default; opt-in tiles retain every source pixel region."""
    policy = image_transport_policy(image_format, jpeg_quality, image_resize,
                                    image_tile_height, image_tile_overlap)
    if not image_tile_height:
        return [encode_image(contents, filename, image_format, jpeg_quality, image_resize)]
    from PIL import Image
    source_hash = hashlib.sha256(contents).hexdigest()
    with Image.open(io.BytesIO(contents)) as source:
        rgba = source.convert("RGBA")
        rgb = Image.new("RGB", source.size, "white")
        rgb.paste(rgba, mask=rgba.getchannel("A"))
        width, height = source.size
        boxes = []
        top = 0
        while top < height:
            bottom = min(top + image_tile_height, height)
            boxes.append((0, top, width, bottom))
            if bottom == height:
                break
            top = bottom - image_tile_overlap
        parts = []
        for index, box in enumerate(boxes, 1):
            tile = rgb.crop(box)
            raw = jpeg_bytes(tile, jpeg_quality)
            parts.append((raw, "image/jpeg", {
                "source_sha256": source_hash, "source_bytes": len(contents),
                "source_dimensions": [width, height], "transport_policy": policy,
                "tile_index": index, "tile_count": len(boxes), "tile_box": list(box),
                "transmitted_dimensions": list(tile.size), "transmitted_bytes": len(raw),
                "transmitted_mime": "image/jpeg", "transmitted_sha256": hashlib.sha256(raw).hexdigest(),
            }))
    return parts


def build_messages(item: dict, input_root: Path,
                   image_format: str = "original", jpeg_quality: int = 90,
                   image_transports: Optional[List[dict]] = None,
                   image_detail: str = "default", image_resize: str = "none",
                   image_tile_height: int = 0, image_tile_overlap: int = 128) -> List[dict]:
    if image_detail not in {"default", "auto", "low", "high"}:
        raise ValueError("Unknown image detail setting")
    parts = []
    image_count = 0
    for source_index, entry in enumerate(item["screenshots"], 1):
        path = input_root / entry["path"]
        contents = path.read_bytes()
        if hashlib.sha256(contents).hexdigest() != entry["sha256"]:
            raise ValueError(f"Screenshot changed after selection: {path.name}")
        encoded = encode_image_parts(contents, path.name, image_format, jpeg_quality, image_resize,
                                     image_tile_height, image_tile_overlap)
        for raw, mime, metadata in encoded:
            if image_tile_height:
                parts.append({"type": "text", "text": (
                    "Source screenshot %d/%d, tile %d/%d, original pixel box %s. "
                    "Tiles belong to the same screenshot in top-to-bottom order; "
                    "adjacent tiles may overlap." %
                    (source_index, len(item["screenshots"]), metadata["tile_index"],
                     metadata["tile_count"], metadata["tile_box"]))})
                metadata["source_screenshot_index"] = source_index
            if image_detail != "default":
                metadata["requested_detail"] = image_detail
            if image_transports is not None:
                image_transports.append({"path": entry["path"], **metadata})
            image_url = {"url": f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"}
            if image_detail != "default":
                image_url["detail"] = image_detail
            parts.append({"type": "image_url", "image_url": image_url})
            image_count += 1

    prompt_values = {"task": item["task"], "answer": item["answer"], "num": image_count}
    text = re.sub(r"<(task|answer|num)>",
                  lambda match: str(prompt_values[match.group(1)]), USER_PROMPT)
    return [
        {"role": "system", "content": evaluation_system_prompt(
            )},
        {"role": "user", "content": [{"type": "text", "text": text}] + parts
         + [{"type": "text", "text": VERDICT_PROMPT}]},
    ]


class JudgeAPIError(Exception):
    def __init__(self, message: str, attempts: int, http_status: Optional[int] = None,
                 retryable: bool = False):
        super().__init__(message)
        self.attempts = attempts
        self.http_status = http_status
        self.retryable = retryable


class NoRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def redact(value: str, api_key: str = "", endpoint: str = "") -> str:
    if api_key:
        value = value.replace(api_key, "<REDACTED_API_KEY>")
    if endpoint:
        value = value.replace(endpoint, "<MODEL_ENDPOINT>")
    value = re.sub(r"(?i)Bearer\s+[^\s\"'<>]+", "Bearer <REDACTED>", value)
    value = re.sub(r"https?://[^\s\"'<>]+", "<URL>", value)
    return value[:2000]


def retry_after_seconds(value: Optional[str]) -> float:
    if not isinstance(value, str) or not value.strip():
        return 0.0
    try:
        seconds = float(value)
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            seconds = (date - datetime.now(timezone.utc)).total_seconds()
        except (ValueError, TypeError, OverflowError):
            return 0.0
    return max(0.0, seconds) if math.isfinite(seconds) else 0.0


def call_judge(payload: dict, endpoint: str, api_key: str, timeout: float,
               api_retries: int, retry_delay: float, ca_bundle: Optional[str] = None,
               attempt_history: Optional[List[dict]] = None) -> Tuple[dict, int]:
    request = urllib.request.Request(
        endpoint, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key},
        method="POST",
    )
    context = ssl.create_default_context(cafile=ca_bundle)
    opener = urllib.request.build_opener(NoRedirects(), urllib.request.HTTPSHandler(context=context))
    history = attempt_history if attempt_history is not None else []
    for attempt in range(1, api_retries + 2):
        event = {"attempt": attempt, "started_at": utc_now()}
        http_status = None
        server_wait = 0.0
        try:
            with opener.open(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("API response is not a JSON object")
            if data.get("error"):
                raise ValueError("API returned an error object: " + json.dumps(data["error"]))
            history.append({**event, "outcome": "response"})
            return data, attempt
        except urllib.error.HTTPError as error:
            detail = redact(error.read(8192).decode("utf-8", errors="replace"), api_key, endpoint)
            message = f"HTTP {error.code}: {detail}"
            http_status = error.code
            server_wait = retry_after_seconds(error.headers.get("Retry-After") if error.headers else None)
            retryable = error.code in TRANSIENT_HTTP_CODES
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as error:
            message = redact(f"{type(error).__name__}: {error}", api_key, endpoint)
            retryable = True
        except (ValueError, UnicodeError) as error:
            message = redact(str(error), api_key, endpoint)
            history.append({**event, "outcome": "error", "error": message, "retryable": False})
            raise JudgeAPIError(message, attempt) from error
        event.update(outcome="error", error=message, http_status=http_status, retryable=retryable)
        history.append(event)
        if not retryable or attempt > api_retries:
            raise JudgeAPIError(message, attempt, http_status, retryable)
        base_delay = max(retry_delay, 30.0) if http_status == 429 else retry_delay
        wait_seconds = max(server_wait, min(base_delay * (2.0 ** min(attempt - 1, 16)), 300.0))
        event["retry_wait_seconds"] = wait_seconds
        print(f"  transient API error ({http_status or 'transport'}); "
              f"wait {wait_seconds:.0f}s, retry {attempt}/{api_retries}", flush=True)
        time.sleep(wait_seconds)
    raise AssertionError("unreachable")


def evaluate_item(item: dict, args: argparse.Namespace, input_root: Path,
                  endpoint: str, api_key: str) -> dict:
    result = {**item, "evaluated_at": utc_now(), "status": "pending",
              "predicted_label": None, "judge_reasoning": "", "api_attempts": 0,
              "response_model": None, "usage": {}, "error": None,
              "api_attempt_history": []}
    result["screenshot_count"] = len(item["screenshots"])
    if item["input_error"]:
        result.update(status="missing_evidence", predicted_label=0, error=item["input_error"])
        return result
    try:
        result["image_transports"] = []
        payload = {
            "messages": build_messages(item, input_root,
                                       args.image_format, args.jpeg_quality, result["image_transports"],
                                       args.image_detail, args.image_resize,
                                       args.image_tile_height, args.image_tile_overlap),
            "stream": False, "temperature": args.temperature, "max_tokens": args.max_tokens,
        }
        if args.model:
            payload["model"] = args.model
        if args.seed is not None:
            payload["seed"] = args.seed
        if args.thinking != "default":
            payload["chat_template_kwargs"] = {"enable_thinking": args.thinking == "on"}
        if args.image_detail != "default" or args.thinking != "default":
            result["request_options"] = {"image_detail": args.image_detail, "thinking": args.thinking}
        result["attached_image_count"] = len(result["image_transports"])
        result["request_json_bytes"] = len(json.dumps(payload, ensure_ascii=False).encode("utf-8"))
        print("  Request: %d source screenshots -> %d images, format=%s, resize=%s, "
              "tile_height=%d, detail=%s, thinking=%s, JSON size=%.2f MiB" %
              (len(item["screenshots"]), result["attached_image_count"], args.image_format,
               args.image_resize, args.image_tile_height, args.image_detail, args.thinking,
               result["request_json_bytes"] / 1048576), flush=True)
        data, attempts = call_judge(payload, endpoint, api_key, args.timeout,
                                   args.api_retries, args.retry_delay, args.ca_bundle,
                                   result["api_attempt_history"])
        result["api_attempts"] = attempts
        result["response_model"] = data.get("model")
        result["usage"] = data.get("usage") if isinstance(data.get("usage"), dict) else {}
        result["response_id"] = data.get("id")
        if args.purpose == "reevaluation" and "qwen" in str(data.get("model", "")).lower():
            raise ValueError("API returned a Qwen model during non-Qwen reevaluation; rejected")
        choices = data.get("choices")
        if not isinstance(choices, list) or not choices:
            raise ValueError("API response has no choices")
        if not isinstance(choices[0], dict) or not isinstance(choices[0].get("message"), dict):
            raise ValueError("Malformed API choice/message")
        result["finish_reason"] = choices[0].get("finish_reason")
        message = choices[0]["message"]
        content = message.get("content")
        if isinstance(content, list):
            content = "\n".join(p.get("text", "") for p in content if isinstance(p, dict))
        
        # [关键修复] 强制清理前后空格，防止正则匹配失败
        if isinstance(content, str):
            content = content.strip()

        result["response_diagnostics"] = {
            "content_chars": len(content) if isinstance(content, str) else 0,
            "reasoning_content_chars": len(message["reasoning_content"])
            if isinstance(message.get("reasoning_content"), str) else 0,
        }
        if result["finish_reason"] == "length":
            if isinstance(content, str):
                result["judge_reasoning"] = content
            result.update(status="parse_error", predicted_label=None,
                          error="Judge output reached the token limit before a complete verdict; "
                          "not counted. For a pilot, increase --max-tokens in a new output directory.")
            return result
        if not isinstance(content, str) or not content.strip():
            raise ValueError("API response has no textual judge verdict in message.content; "
                             "reasoning_content is not a final verdict")
        result["judge_reasoning"] = content
        label = parse_verdict(content)
        result["predicted_label"] = label
        result["status"] = "success" if label == 1 else "failure" if label == 0 else "parse_error"
        if label is None:
            result["error"] = "No unambiguous final SUCCESS / NOT SUCCESS line; not re-judged."
    except JudgeAPIError as error:
        result.update(status="api_error", error=str(error), api_attempts=error.attempts,
                      http_status=error.http_status, retryable=error.retryable)
    except (OSError, ValueError, KeyError, TypeError) as error:
        result.update(status="evaluation_error", error=redact(str(error), api_key, endpoint))
    return result


def summarize(items: List[dict], results: Dict[str, dict]) -> dict:
    counts = Counter(results[item["task_id"]]["status"] if item["task_id"] in results else "pending"
                     for item in items)
    total = len(items)
    success = counts["success"]
    unresolved = sum(counts[s] for s in ("pending", "api_error", "parse_error", "evaluation_error"))
    usage = Counter()
    for item in items:
        for key, value in results.get(item["task_id"], {}).get("usage", {}).items():
            if isinstance(value, (int, float)):
                usage[key] += value
    return {
        "total_tasks": total, "success": success, "failure": counts["failure"],
        "missing_evidence": counts["missing_evidence"], "api_error": counts["api_error"],
        "parse_error": counts["parse_error"], "evaluation_error": counts["evaluation_error"],
        "pending": counts["pending"], "unresolved": unresolved,
        "complete": unresolved == 0,
        "acceptance_rate_percent": round(100 * success / total, 4) if total and not unresolved else None,
        "provisional_success_over_all_tasks_percent": round(100 * success / total, 4) if total else 0,
        "denominator_policy": "All selected unique tasks; missing evidence counts as unsuccessful; API/parse errors remain unresolved.",
        "usage": dict(usage),
    }


def csv_rows(items: List[dict], results: Dict[str, dict]) -> List[dict]:
    rows = []
    for item in items:
        result = results.get(item["task_id"], {**item, "status": "pending"})
        rows.append({key: result.get(key) for key in CSV_FIELDS})
    return rows


def write_csv(path: Path, rows: List[dict]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8-sig", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def write_reports(output_root: Path, items: List[dict], results: Dict[str, dict], config: dict) -> dict:
    groups = defaultdict(list)
    for item in items:
        groups[item["website"]].append(item)
    by_website = {}
    for website in sorted(groups, key=natural_key):
        subset = groups[website]
        site_summary = {"website": website, "answer_source": config["answer_source"],
                        "prompt_variant": config["prompt_variant"], **summarize(subset, results)}
        site_dir = output_root / "websites" / safe_name(website)
        site_dir.mkdir(parents=True, exist_ok=True)
        atomic_json(site_dir / "summary.json", site_summary)
        atomic_json(site_dir / "results.json", [results.get(i["task_id"], {**i, "status": "pending"}) for i in subset])
        write_csv(site_dir / "results.csv", csv_rows(subset, results))
        by_website[website] = {**site_summary, "files": site_dir.relative_to(output_root).as_posix()}
    summary = {
        "schema_version": SCHEMA_VERSION, "updated_at": utc_now(),
        "purpose": config["purpose"], "model_name": config["model_name"],
        "prompt_source": config["prompt_source"],
        "prompt_variant": config["prompt_variant"],
        "answer_source": config["answer_source"], "answer_policy": config["answer_policy"],
        "official_acceptance_claimed": False,
        "selection_policy": config["selection_policy"],
        "response_models": sorted({str(r["response_model"]) for r in results.values() if r.get("response_model")}),
        **summarize(items, results), "websites": by_website,
    }
    if "image_transport" in config:
        summary["image_transport"] = config["image_transport"]
    if "request_options" in config:
        summary["request_options"] = config["request_options"]
    atomic_json(output_root / "summary.json", summary)
    atomic_json(output_root / "all_results.json", [results.get(i["task_id"], {**i, "status": "pending"}) for i in items])
    write_csv(output_root / "results.csv", csv_rows(items, results))
    rate = summary["acceptance_rate_percent"]
    rate_text = f"{rate:.2f}%" if rate is not None else "INCOMPLETE (not a final score)"
    text = ["# WebVoyager screenshot re-evaluation", "",
            f"Purpose: **{config['purpose']}**. This report does not claim leaderboard approval.", "",
            f"Model: {config['model_name']}; prompt variant: {config['prompt_variant']}.", "",
            f"Answer input: {config['answer_source']}. {config['answer_policy']}", "",
            f"Tasks: {len(items)}; accepted: {summary['success']}; acceptance rate: {rate_text}.", "",
            "Missing evidence is unsuccessful. API/parse/evaluation errors are unresolved, not silently dropped.", "",
            "| Website | Tasks | Accepted | Rejected | Missing evidence | Unresolved | Rate |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    if "image_transport" in config:
        policy = config["image_transport"]
        geometry = ("resized to fit %s; no crop" % policy["max_size"]
                    if policy["resize"] else "original pixel dimensions; no resizing or cropping")
        if policy.get("tiling"):
            tiles = policy["tiling"]
            geometry = ("original-resolution vertical tiles, height %d px, overlap %d px, "
                        "top-to-bottom full coverage; no image region omitted. "
                        "This changes the image layout from original auto_eval" %
                        (tiles["height"], tiles["overlap"]))
        text[1:1] = ["", "Image preprocessing: JPEG quality %d, 4:4:4 chroma; %s. "
                     "JPEG is lossy transport; source artifacts are unchanged." % (policy["quality"], geometry)]
    if "request_options" in config:
        text[1:1] = ["", "API request options: image detail=%s; thinking=%s. "
                     "These options do not change the judging prompt, but may affect model behavior." %
                     (config["request_options"]["image_detail"], config["request_options"]["thinking"])]
    for website, stats in by_website.items():
        site_rate = stats["acceptance_rate_percent"]
        text.append(f"| {website} | {stats['total_tasks']} | {stats['success']} | {stats['failure']} | "
                    f"{stats['missing_evidence']} | {stats['unresolved']} | " +
                    (f"{site_rate:.2f}% |" if site_rate is not None else "incomplete |"))
    text += ["", "Selected task records and image hashes are frozen in selection_manifest.json.",
             "Only the selected final execution is judged; old self-reflection labels are never inputs.",
             "Reports contain task/answer/evidence metadata and are NOT automatically sanitized for publication.", ""]
    (output_root / "SUMMARY.md").write_text("\n".join(text), encoding="utf-8")
    return summary


def load_cached_results(output_root: Path, items: List[dict]) -> Dict[str, dict]:
    selected = {item["task_id"]: item for item in items}
    results = {}
    root = output_root / "judge_results"
    if root.is_dir():
        for path in root.glob("*.json"):
            result = read_json(path)
            task_id = result.get("task_id")
            if task_id not in selected or result.get("fingerprint") != selected[task_id]["fingerprint"]:
                raise ValueError(f"Cached result does not match frozen selection: {path.name}")
            if task_id in results:
                raise ValueError(f"Duplicate cached task result: {task_id}")
            results[task_id] = result
    return results


def add_image_transport_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--image-format", choices=["original", "jpeg"], default="original",
                        help="Request-only JPEG copy or exact original bytes; no source edits")
    parser.add_argument("--jpeg-quality", type=int, default=90,
                        help="JPEG quality 1-100; only used for --image-format jpeg")
    parser.add_argument("--image-resize", choices=["none", "fit"], default="none",
                        help="JPEG only: preserve dimensions (default), or opt in to legacy 1280x1280 fit; "
                             "fit can make long-page text unreadable")
    parser.add_argument("--image-tile-height", type=int, default=0,
                        help="JPEG only: opt-in original-resolution vertical tiles of this height; "
                             "0 disables tiling. Covers all selected images, may increase image/token counts")
    parser.add_argument("--image-tile-overlap", type=int, default=128,
                        help="Vertical overlap in pixels, smaller than tile height; unused when tiling is off")


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--input-root", type=Path, default=Path("outputs/webvoyager"))
    parser.add_argument("--output-dir", type=Path, default=None,
                        help="New directory, or the same directory with --resume")
    parser.add_argument("--endpoint", default=None,
                        help="Full chat/completions URL; defaults to WEBVOYAGER_EVAL_ENDPOINT")
    parser.add_argument("--api-key-env", default="WEBVOYAGER_EVAL_API_KEY")
    parser.add_argument("--model", default=None, help="Optional model field sent to API; omit for route-specific endpoints")
    parser.add_argument("--model-name", default=None, help="Actual judge name for reports; falls back to --model")
    parser.add_argument("--purpose", choices=["pilot", "reevaluation"], default="pilot")
    parser.add_argument("--website", action="append", default=[], help="Repeatable, e.g. Booking or Google_Map")
    parser.add_argument("--task-id", action="append", default=[], help="Repeatable exact task ID")
    parser.add_argument("--limit", type=int, default=0, help="0 = all matching unique tasks")
    parser.add_argument("--expected-tasks", type=int, default=None,
                        help="Optional assertion for selected task count, e.g. 615 for a full run")
    parser.add_argument("--max-attached-imgs", type=int, default=1,
                        help="Last K source screenshots in the selected run, before optional tiling; "
                             "original auto_eval default is 1")
    add_image_transport_arguments(parser)
    parser.add_argument("--image-detail", choices=["default", "auto", "low", "high"], default="default",
                        help="Optional image_url.detail; default omits it. High is not compression")
    parser.add_argument("--thinking", choices=["default", "off", "on"], default="default",
                        help="Optional gateway chat_template_kwargs.enable_thinking; no fallback if rejected")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=None, help="Optional; omitted for gateway compatibility")
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--api-retries", type=int, default=2, help="Additional retries for transient transport/HTTP errors only")
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between task API calls")
    parser.add_argument("--ca-bundle", default=None, help="Optional corporate CA certificate file; TLS verification remains enabled")
    parser.add_argument("--resume", action="store_true", help="Retry API/evaluation errors; never re-judge an existing failure or parse error")
    parser.add_argument("--dry-run", action="store_true", help="Write inventory and pending reports without any API requests")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    if args.limit < 0 or args.max_attached_imgs < 1 or args.api_retries < 0 or args.max_tokens < 1:
        raise ValueError("limit/retries must be nonnegative; image count and max_tokens must be positive")
    if args.timeout <= 0 or args.delay < 0 or args.retry_delay < 0:
        raise ValueError("timeout must be positive; delays cannot be negative")
    transport_policy = image_transport_policy(args.image_format, args.jpeg_quality, args.image_resize,
                                              args.image_tile_height, args.image_tile_overlap)
    input_root = args.input_root.resolve()
    if not input_root.is_dir():
        raise ValueError(f"Input root not found: {input_root}")
    output_root = (args.output_dir or Path("outputs/webvoyager_auto_eval") /
                   datetime.now().strftime("%Y%m%d_%H%M%S")).resolve()
    if is_within(output_root, input_root) or is_within(input_root, output_root):
        raise ValueError("Output directory must be separate from, and not an ancestor of, input artifacts")
    if output_root.exists() and any(output_root.iterdir()) and not args.resume:
        raise ValueError("Output directory is not empty; use a new directory or --resume")
    if args.resume and not (output_root / "evaluation_config.json").is_file():
        raise ValueError("--resume requires an existing evaluation_config.json")

    endpoint = args.endpoint or os.environ.get("WEBVOYAGER_EVAL_ENDPOINT", "")
    if not args.dry_run and not endpoint:
        raise ValueError("Set WEBVOYAGER_EVAL_ENDPOINT or --endpoint")
    if endpoint:
        parsed = urllib.parse.urlparse(endpoint)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Endpoint must be HTTPS without credentials embedded in its URL")
        if parsed.query or parsed.fragment:
            raise ValueError("Endpoint URL must not contain query-string credentials or fragments")
    model_name = args.model_name or args.model or "unspecified-route-model"
    if args.purpose == "reevaluation":
        if model_name == "unspecified-route-model" or "qwen" in (model_name + " " + str(args.model) + " " + endpoint).lower():
            raise ValueError("Reevaluation requires an explicitly named non-Qwen judge; use --purpose pilot for Qwen tests")
    config = {
        "schema_version": SCHEMA_VERSION, "purpose": args.purpose,
        "model_name": model_name, "request_model": args.model,
        "endpoint_sha256": hashlib.sha256(endpoint.encode()).hexdigest(),
        "temperature": args.temperature, "max_tokens": args.max_tokens, "seed": args.seed,
        "max_attached_imgs": args.max_attached_imgs, "prompt_source": PROMPT_SOURCE,
        "answer_source": ANSWER_SOURCE,
        "prompt_variant": "standard",
        "base_system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "system_prompt_sha256": hashlib.sha256(evaluation_system_prompt().encode()).hexdigest(),
        "user_prompt_sha256": hashlib.sha256(USER_PROMPT.encode()).hexdigest(),
        "verdict_prompt_sha256": hashlib.sha256(VERDICT_PROMPT.encode()).hexdigest(),
        "selection_policy": "Newest timestamped task record; highest run_NNN within that record; no success-based selection or fallback.",
        "answer_policy": ANSWER_POLICY,
        "screenshot_policy": "Last K in selected run_manifest sequence; natural filename order when no sequence exists.",
        "websites_filter": args.website, "task_ids_filter": args.task_id, "limit": args.limit,
        "expected_tasks": args.expected_tasks,
    }
    if args.image_format != "original":
        config["image_transport"] = transport_policy
    if args.image_detail != "default" or args.thinking != "default":
        config["request_options"] = {"image_detail": args.image_detail, "thinking": args.thinking}
    grouped = discover_records(input_root)
    items = prepare_selection(grouped, input_root, args.website, args.task_id,
                              args.limit, args.max_attached_imgs)
    if args.expected_tasks is not None and len(items) != args.expected_tasks:
        raise ValueError(f"Expected {args.expected_tasks} selected tasks, found {len(items)}")
    manifest = {"schema_version": SCHEMA_VERSION, "tasks": items}
    if args.resume:
        if read_json(output_root / "evaluation_config.json") != config:
            raise ValueError("Resume configuration changed; create a new output directory instead")
        if read_json(output_root / "selection_manifest.json") != manifest:
            raise ValueError("Source evidence/selection changed since the run was frozen; do not mix evaluations")
    else:
        output_root.mkdir(parents=True, exist_ok=True)
        atomic_json(output_root / "evaluation_config.json", config)
        atomic_json(output_root / "selection_manifest.json", manifest)
        atomic_json(output_root / "prompts.json", {
            "source": PROMPT_SOURCE,
            "prompt_variant": config["prompt_variant"],
            "base_system_prompt": SYSTEM_PROMPT,
            "system_prompt": evaluation_system_prompt(), "user_prompt_template": USER_PROMPT,
            "verdict_prompt": VERDICT_PROMPT,
        })
    results = load_cached_results(output_root, items)
    summary = write_reports(output_root, items, results, config)
    print(f"Discovered {sum(len(r) for r in grouped.values())} records / {len(grouped)} unique tasks.")
    print(f"Selected {len(items)} tasks across {len(summary['websites'])} websites; "
          f"{sum(bool(i['input_error']) for i in items)} missing/invalid evidence.")
    print(f"Purpose: {args.purpose}; model: {model_name}; output: {output_root}")
    print(f"Answer source: {ANSWER_SOURCE}; prompt variant: {config['prompt_variant']}")
    if args.dry_run:
        print("Dry run complete. No API requests; pending tasks are NOT reported as evaluated.")
        return 0
    api_key = os.environ.get(args.api_key_env, "")
    if not api_key and sys.stdin.isatty():
        api_key = getpass.getpass(f"API key ({args.api_key_env}; hidden input): ")
    if not api_key:
        raise ValueError(f"Missing API key: set {args.api_key_env} (never put it in a command argument)")

    response_dir = output_root / "judge_results"
    response_dir.mkdir(exist_ok=True)
    interrupted = False
    try:
        for index, item in enumerate(items, 1):
            cached = results.get(item["task_id"])
            if cached and cached["status"] in TERMINAL_STATUSES:
                continue
            print(f"[{index}/{len(items)}] {item['task_id']} / {item['final_run']}", flush=True)
            result = evaluate_item(item, args, input_root, endpoint, api_key)
            if cached:
                result["previous_infrastructure_errors"] = cached.get("previous_infrastructure_errors", []) + [{
                    "evaluated_at": cached.get("evaluated_at"), "status": cached["status"],
                    "error": cached.get("error"), "api_attempts": cached.get("api_attempts", 0),
                    "api_attempt_history": cached.get("api_attempt_history", []),
                }]
            atomic_json(response_dir / (safe_name(item["task_id"]) + ".json"), result)
            results[item["task_id"]] = result
            summary = write_reports(output_root, items, results, config)
            print(f"  {result['status']}; accepted={summary['success']}/{len(items)}; "
                  f"unresolved={summary['unresolved']}", flush=True)
            if result.get("error"):
                print("  " + result["error"], flush=True)
            if result["status"] == "api_error" and result.get("retryable"):
                print("Stopping after exhausted transient API retries; remaining tasks stay pending. "
                      "Check rate limits/quota before using --resume.", flush=True)
                break
            if result["status"] == "evaluation_error" or (
                result["status"] == "api_error" and
                re.match(r"HTTP (?:400|401|403|404|405|413|415|422)\b", result["error"] or "")
            ):
                print("Stopping on endpoint/authentication/schema error. Fix configuration before continuing.")
                break
            if args.delay and result["api_attempts"]:
                time.sleep(args.delay)
    except KeyboardInterrupt:
        interrupted = True
        print("\nInterrupted. Completed verdicts are saved; use identical options with --resume.")
    finally:
        summary = write_reports(output_root, items, results, config)
    print(f"Accepted: {summary['success']}/{summary['total_tasks']}; unresolved: {summary['unresolved']}")
    if summary["complete"]:
        print(f"Judge acceptance rate: {summary['acceptance_rate_percent']:.2f}% ({args.purpose})")
    else:
        print("INCOMPLETE: no final acceptance rate published; inspect summary.json and resume if appropriate.")
    return 130 if interrupted else 0 if summary["complete"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        raise SystemExit(2)
