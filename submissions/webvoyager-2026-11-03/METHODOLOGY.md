# Evaluation Methodology

## System and Task Collection

- Execution system: Webwright (Qwen3.8-Max).
- Reporting organization: [XYDT](https://www.xydigit.com/).
- Base task collection: [browser-control-fable-5](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5) from omxyz/webvoyager.
- Task preparation: month names were updated in 49 date-sensitive task instructions.
- Evaluated collection: 615 tasks with the updated task instructions.
- Exact executed task definitions: `tasks/`.
- Evaluation type: self-reported, system-level post-hoc evaluation.

All 615 tasks are included in the final denominator.

The exact task definitions used for execution and evaluation are published in `tasks/`. The agent and external judge used the same updated task instructions. The reported score applies to this date-updated collection of 615 tasks.

The [task-definition timing supplement](evidence/report_time/) provides the retained comparison records and their correspondence with the submitted execution records.

## Framework Self-Repair

Webwright performs exploration, script development, execution validation,
and repair within each submitted task record. The agent generates the critical
points and expected answer used by its internal self-reflection judge. Feedback
from that check can trigger script revisions and additional executions within
the same task record, until the self-check passes or the task reaches a budget
or unrecoverable-error condition.

The numbered directories under `final_runs/` record these script execution and
repair iterations within that task workflow. They are internal iterations of one
benchmark task, not additional benchmark tasks.

The run directories present in the submitted task records are retained for
inspection. Each unique task contributes one final evaluation result.

For external evaluation, the run with the largest numeric index is used;
its internal pass/fail label is not consulted, and the evaluator does not
fall back to an earlier run because it was internally marked successful.

Internal validation can still guide script repair and task termination.
It is distinct from the external evaluation used for the reported score.

## Task Execution Budgets and Stopping Policy

The archived `config_snapshot/merged_config.yaml` files for all 615
submitted task records contain the following settings:

| Configuration field | Recorded value |
| --- | --- |
| `agent.step_limit` | 200 |
| `agent.max_run_seconds` | 14400 seconds (4 hours) |
| `agent.max_idle_seconds` | 1800 seconds (30 minutes) |
| `agent.require_self_reflection_success` | `true` |
| `agent.require_task_success_marker` | `true` |

These are configured execution limits and completion requirements,
rather than measurements of the resources consumed by every task.

The step limit applies to the main agent loop. It should not be interpreted
as a limit of 200 browser actions, total model API requests, or final-script
executions. Internal validation calls and API retries are separate operations.

The idle limit concerns the time without a completed agent step.
Normal successful submission is configured to require successful internal
self-reflection and a task-success marker. A task can also terminate without
successful submission when a budget, watchdog, or unrecoverable error
condition is reached.

Internal script execution and repair take place within the task's execution
budget. The maximum observed selected run index of 20 is a property of this
submitted collection, not a configured retry limit.

Additional recovery settings are preserved in each task record's
`config_snapshot/merged_config.yaml`.

Final benchmark outcomes are assigned by the external evaluation,
judgment-selection, and missing-evidence rules, rather than by internal
completion flags.

## Evaluation Inputs

For each task, the evaluator uses the highest-numbered `final_runs/run_NNN` directory.

The judge inputs are:

- The task instruction.
- The selected run's `answer.txt`.
- Up to the last five screenshots from that run.

Screenshot ordering follows the run manifest when available, otherwise natural filename order.

The external evaluator selects the highest-numbered run without consulting internal pass/fail labels and does not fall back to an earlier run because it was internally marked successful.

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

The published evaluator script is preserved unchanged, including the
parsing behavior used when recording the raw evaluation results.

Final scoring was reconstructed offline from the saved judge response
texts using the upstream WebVoyager parsing rule and the judgment-selection
policy described below.

The status fields in `evaluation/raw/` preserve their originally recorded
values. Final task outcomes and selected-record provenance are documented
in `evaluation/merged_results.json` and `evaluation/REJUDGMENT_AUDIT.json`.

This offline reparsing and aggregation step made no additional model calls.

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
