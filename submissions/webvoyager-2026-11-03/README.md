# Webwright WebVoyager Evaluation Results

Submission: `webvoyager-2026-11-03`

## Results

| Item | Value |
| --- | --- |
| System | Webwright + Qwen3.8-Max |
| Judge model | GLM-5.3-Flash |
| Evaluation type | Self-reported, system-level post-hoc evaluation |
| Total tasks | 615 |
| Success | 601 |
| Failure | 10 |
| Missing evidence | 4 |
| Unresolved judgments | 0 |
| Success rate | 97.72% |

Success rate = 601 / 615 × 100%.

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

## Judge-Side Rejudgments

Eleven tasks initially produced `parse_error` judgments. These tasks were rejudged using identical frozen evaluation inputs.

These judge-side rejudgments are separate from the framework's self-repair process. They do not rerun the browser task or increase the task count.

The merged results preserve the source evaluation file and initial status for each task.

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
