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

## Final Judgment Selection

Each unique task contributes one final evaluation result.

Final results use the earliest saved judge output that provides a
definitive verdict under the upstream WebVoyager parsing rule:

- An output containing NOT SUCCESS is counted as failure.
- Otherwise, an output containing SUCCESS is counted as success.
- An output containing neither remains unparseable.

Matching is case-sensitive.

ArXiv--38 is counted as failure based on its first judge output,
which states NOT SUCCESS. Its later SUCCESS output is retained
for auditing and is not used for scoring.

For six tasks whose initial outputs were unparseable, subsequent
judgments using identical frozen inputs provide the final results.

Five additional judgments are retained but excluded from result
selection because the corresponding initial outputs already
provided parseable verdicts.

Tasks with missing evidence remain in the denominator and count
as unsuccessful.

The final results are 600 successes, 11 failures, and 4
missing-evidence tasks out of 615, yielding a success rate of 97.56%.

Selected judgments and their provenance are recorded in
evaluation/merged_results.json and evaluation/REJUDGMENT_AUDIT.json.
All saved judge outputs remain available in evaluation/raw/.

Further audit details are available in
[the scoring correction report](SCORING_CORRECTION.md).

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
