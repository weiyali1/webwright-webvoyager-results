# Evaluation Methodology

## System and Task Collection

- Execution system: Webwright + Qwen3.8-Max.
- Task collection: 615 filtered and updated WebVoyager-derived browser-control-fable-5 tasks.
- Exact executed task definitions: `tasks/`.
- Evaluation type: self-reported, system-level post-hoc evaluation.

All 615 tasks are included in the final denominator.

## Framework Self-Repair

Webwright supports task-level self-repair.

After executing a task script, the framework inspects execution results and internal validation feedback. When problems are detected, it may revise the script and execute it again.

The numbered directories under `final_runs/` preserve artifacts from these internal execution and self-repair iterations. Multiple numbered runs do not increase the benchmark task count.

All available internal iterations are retained for auditing. Each unique task contributes one final evaluation result.

## Evaluation Inputs

For each task, the evaluator uses the highest-numbered `final_runs/run_NNN` directory.

The judge inputs are:

- The task instruction.
- The selected run's `answer.txt`.
- Up to the last five screenshots from that run.

Screenshot ordering follows the run manifest when available, otherwise natural filename order.

The evaluator does not choose runs according to internal success labels and does not fall back to earlier successful runs.

It does not use `final_response.txt`, execution logs, or internal judge verdict files as substitute answer inputs.

## External Judge Configuration

| Setting | Value |
| --- | --- |
| Judge model | glm-5.3-flash |
| Recorded configuration purpose | pilot |
| Judging prompt | Official WebVoyager judging prompt |
| Maximum attached source screenshots | 5 |
| Request image format | JPEG |
| JPEG quality | 85 |
| Request image resizing | Fit within 1280 × 1280 |
| Image tiling | Disabled |
| Image detail option | Default |
| Thinking option | On |
| Temperature | 0.0 |
| Maximum output tokens | 32768 |
| Seed | Not set |

Source screenshots are retained. JPEG conversion and resizing apply to request-time image transport.

Exact prompts, configurations, image transport metadata, and judge outputs are retained in `evaluation/raw/`.

Judging prompt source:
https://github.com/MinorJerry/WebVoyager/blob/main/evaluation/auto_eval.py

## Judge-Side Errors and Rejudgments

There are 615 first-evaluation records and 11 task-level parse-error rejudgments.

Only tasks whose initial judgment had `parse_error` are replaced by these rejudgments. The initial and retry input fingerprints are identical.

These rejudgments concern the external judging process. They do not rerun browser tasks or add benchmark tasks.

The final merged results contain one judgment per unique task and preserve evaluation-source provenance. Raw first-evaluation and retry files remain unchanged.

## Scoring

| Outcome | Tasks |
| --- | ---: |
| Success | 601 |
| Failure | 10 |
| Missing evidence | 4 |
| Unresolved | 0 |
| Total | 615 |

Success rate = 601 / 615 × 100% = 97.7236%, displayed as 97.72%.

Missing evidence counts as unsuccessful and remains in the denominator.

The missing-evidence tasks are:

- Amazon--15
- Coursera--27
- Google Flights--23
- Google Map--33

## Public Execution Records

Confirmed local identifiers, API-key values, and model/browser connection addresses were redacted from the public execution-copy text.

Compiled caches and runtime browser-session symlinks were excluded by the public exporter. Execution evidence was otherwise retained.

The public task instructions, selected answers, and selected screenshot files were checked against the frozen evaluation inputs.
