# Webwright WebVoyager Evaluation Results

Submission: `webvoyager-2026-11-03`

## Results

| Item | Value |
| --- | --- |
| System | webwright（qwen3.8max） |
| Organization | XYDT |
| Judge model | GLM-5.3-Flash |
| Evaluation type | Self-reported, system-level post-hoc evaluation |
| Total tasks | 615 |
| Success | 600 |
| Failure | 11 |
| Missing evidence | 4 |
| Unresolved judgments | 0 |
| Success rate | 97.56% |

Success rate = 600 / 615 × 100%.

Missing-evidence tasks remain in the denominator and count as unsuccessful.

## Task Collection

This evaluation is based on the [browser-control-fable-5](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5) task collection from omxyz/webvoyager.

Before execution, stale dates in date-sensitive tasks were updated. The agent and external judge used the same updated task instructions. The exact executed and evaluated task definitions are published in this submission. The reported score applies to this date-updated collection of 615 tasks.

The exact task definitions used in execution are published in `tasks/`.

## Framework Self-Repair Workflow

Webwright supports self-repair during task execution.

The framework executes the task script, inspects execution results and internal validation feedback, and may revise the script and execute it again to address detected problems.

Multiple `final_runs/run_NNN` directories preserve the artifacts produced during these internal execution, validation, and self-repair iterations, including script snapshots, logs, screenshots, and available evidence.

These internal iterations belong to the same task-level workflow. All available iterations are retained for auditing. Each unique task contributes one final evaluation result.

## External Evaluation

The evaluator uses the highest-numbered `final_runs/run_NNN` directory for each task.

The external judge receives the task instruction, the selected run's `answer.txt`, and up to the last five screenshots, using the official WebVoyager judging prompt.

Selection does not depend on internal success labels. The evaluator does not fall back to an earlier successful run.

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

## Published Materials

- [Exact task collection](tasks/)
- [Evaluation script](evaluator/evaluate_webvoyager.py)
- [Raw evaluation records](evaluation/raw/)
- [Merged final judgments](evaluation/merged_results.json)
- [Final summary](evaluation/summary.json)
- [Evaluation methodology](METHODOLOGY.md)
- [Archive manifest](artifacts/PACKAGING_MANIFEST.json)
- [Archive checksums](artifacts/SHA256SUMS.txt)
- [Execution evidence downloads](https://github.com/weiyali1/webwright-webvoyager-results/releases/tag/webvoyager-2026-11-03)

The 15 ZIP archives contain task records grouped by website.

Reporting date: 2026-11-03.
