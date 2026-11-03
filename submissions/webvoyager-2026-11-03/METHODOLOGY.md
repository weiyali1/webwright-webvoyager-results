# Evaluation Methodology

## System and Task Collection

- Execution system: webwright（qwen3.8max）.
- Base task collection: [browser-control-fable-5](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5) from omxyz/webvoyager.
- Task preparation: stale dates in date-sensitive tasks were updated before execution.
- Evaluated collection: 615 tasks with the updated task instructions.
- Exact executed task definitions: `tasks/`.
- Evaluation type: self-reported, system-level post-hoc evaluation.

All 615 tasks are included in the final denominator.

Before execution, stale dates in date-sensitive tasks were updated. The agent and external judge used the same updated task instructions. The exact executed and evaluated task definitions are published in this submission. The reported score applies to this date-updated collection of 615 tasks.

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

## Judge-Side Errors and Scoring Correction

The original evaluation script and all raw judge outputs are preserved
unchanged.

The original harness recorded 11 initial outputs as parse_error and
rejudged them using identical frozen inputs. Its last-line-only parser
missed verdicts followed by explanatory text.

Final scoring was reconstructed from the saved judge texts using the
upstream WebVoyager parsing rule:

- An output containing NOT SUCCESS is unsuccessful.
- Otherwise, an output containing SUCCESS is successful.
- An output containing neither remains unparseable.

Matching is case-sensitive, as in the upstream implementation.
Each task uses its earliest definitive judgment under this rule.

Reparsing the 11 initial outputs identifies two initial failures,
three initial successes, and six initially unparseable outputs.

The five rejudgments following an already parseable initial result
remain published for auditing but are excluded from result selection:

- Apple--21: use the initial SUCCESS.
- ArXiv--38: use the initial NOT SUCCESS.
- ESPN--29: use the initial SUCCESS.
- Google Flights--26: use the initial SUCCESS.
- Google Search--39: use the initial NOT SUCCESS.

Only the six initially unparseable cases use later judgments.

ArXiv--38 changes from success to failure. The other four tasks retain
their final outcome labels, but use their initial evaluation records.

The corrected total is 600 successes, 11 failures, and 4 missing-evidence
tasks out of 615.

Success rate = 600 / 615 × 100% = 97.5609756%, displayed as 97.56%.

All raw records retain their historically saved status fields.
Corrected selections and provenance are recorded in
evaluation/merged_results.json and evaluation/REJUDGMENT_AUDIT.json.

This correction involved no additional model calls or browser-task
executions. The original evaluation script remains unchanged.

## Scoring

| Outcome | Tasks |
| --- | ---: |
| Success | 600 |
| Failure | 11 |
| Missing evidence | 4 |
| Unresolved | 0 |
| Total | 615 |

Success rate = 600 / 615 × 100% = 97.5610%, displayed as 97.56%.

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
