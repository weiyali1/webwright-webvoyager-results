# Webwright WebVoyager Evaluation Results

## Result

| System | Organization | Judge Model | Score |
| --- | --- | --- | --- |
| Webwright + Qwen3.8-Max | Independent | GLM-5.3-Flash (using the official WebVoyager judging prompt) | 597/615 (97.07%) |

## Task Set

This evaluation used all 615 tasks from `browser-control-fable-5`, a WebVoyager-derived task set. This variant was created through task filtering and updates. Dates in tasks that had become stale were updated before execution.

The exact task definitions used in this evaluation are published in the [`tasks/`](tasks/) directory.

## Execution System

The evaluated system was Webwright + Qwen3.8-Max. Each benchmark task was executed once, with the framework able to perform internal validation and repair during that task execution.

The `final_runs/run_NNN/` directories contain the internal execution and validation artifacts produced during this process. They do not represent independent benchmark task runs or additional submissions. Each task contributes only one final evaluation result.

## Judge Model and Evaluation Inputs

The post-hoc evaluation used GLM-5.3-Flash with the official WebVoyager judging prompt.

For each task, the evaluator selected the highest-numbered `final_runs/run_NNN/` directory and sent the task instruction, the contents of that directory's `answer.txt`, and up to the last five screenshots to the judge model.

### Final Answer Extraction

Before evaluation, the final answer was extracted from the selected run's output files and saved as `answer.txt`:

1. Preferentially extract the final answer from `final_response.txt` in the selected run.
2. If that file is missing or does not contain a usable answer, extract the final answer from `final_script_log.txt` in the same run.
3. Retain only the answer content, excluding execution logs, internal self-check results, and verdict statements such as `self-reflection judge verdict: PASS`, to prevent those statements from influencing the external judge.

During evaluation, the evaluator reads only `answer.txt`. It does not directly read `final_response.txt`, `final_script_log.txt`, or other internal verdict files, and it does not fall back to earlier runs for an answer. The original `judge_result.json` files are not used as verdicts for this post-hoc evaluation.

### Judge-Side Errors and Retries

`parse_error`, `evaluation_error`, and `api_error` indicate problems encountered while submitting judge requests or processing their results, such as API timeouts, empty responses, failure to parse a valid `SUCCESS` / `NOT SUCCESS` verdict, or evaluation-processing exceptions. These statuses do not directly indicate that the agent failed to execute the task.

We handle these issues through automatic retries or by resuming evaluation with --resume, with a maximum of three retries. These retries apply only to the judging process for the same task. They do not rerun the benchmark task or increase the total task count.


### Missing Evidence

A task is marked as `missing_evidence` if the selected run's `answer.txt` is missing or empty, or if the required execution screenshots are missing.

Tasks with missing evidence remain in the denominator of all 615 tasks and are counted as unsuccessful. Three tasks fell into this category in this evaluation.

## Evaluation Setup

- Benchmark source: [browser-control-fable-5](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5)
- Task scope: 615 filtered and updated WebVoyager-derived tasks.
- Execution system: Webwright + Qwen3.8-Max.
- Evaluation type: Self-reported, system-level post-hoc evaluation.
- Judge model: GLM-5.3-Flash.
- Judging prompt: The official WebVoyager judging prompt.
- Answer input: `answer.txt` from the selected run.
- Screenshot input: Up to the last five screenshots from the selected run.
- Scoring unit: Each unique task is counted once.

## Result Summary

| Metric | Result |
| --- | ---: |
| Total tasks | 615 |
| Successful tasks | 597 |
| Unsuccessful tasks (including missing evidence) | 18 |
| Of which: missing evidence | 3 |
| Success rate | 97.07% |

The success rate uses all 615 tasks as the denominator:

597 / 615 × 100% = 97.07%

Neither the number of internal run directories nor the number of judge-side retries increases the total task count or the successful task count.

## Public Evidence

- [`tasks/`](tasks/): The 15 website task JSON files used in this evaluation, containing 615 tasks in total.
- [Execution evidence archives](https://github.com/weiyali1/webwright-webvoyager-results/releases/tag/webvoyager-2026-10-26): Separate archives for the 15 websites, provided for auditing execution artifacts, final answers, and screenshots.
- [`eval_result/`](eval_result/): Evaluation results, summary reports, and associated configurations and records.
- [`evaluate_webvoyager.py`](evaluate_webvoyager.py): The script used for this evaluation.
- [`SHA256SUMS`](SHA256SUMS): SHA-256 checksums for the execution evidence archives.

Local filesystem paths, company model endpoints, and credential information have been redacted from the published copies. Compiled Python cache files have been omitted. The original evaluation outputs remain unchanged.

## Reporting Information

- Reporting organization: Independent
- Updated: 2026-10-29
