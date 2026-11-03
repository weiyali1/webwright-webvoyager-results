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

The exact task definitions used for execution and evaluation are published in `tasks/`. The agent and external judge used the same updated task instructions. The reported score applies to this date-updated collection of 615 tasks.

## Framework Self-Repair Workflow

Webwright performs exploration, script development, execution validation,
and repair within each submitted task record.

The numbered directories under `final_runs/` record script execution and
repair iterations within that task workflow. Scripts may be executed again
after changes prompted by execution results or internal validation feedback.

The run directories present in the submitted task records are retained for
inspection. Each unique task contributes one final evaluation result.

For external evaluation, the run with the largest numeric index is used;
its internal pass/fail label is not consulted, and the evaluator does not
fall back to an earlier run because it was internally marked successful.

Internal validation can still guide script repair and task termination.
It is distinct from the external evaluation used for the reported score.

In this submitted collection, 360 selected final runs have numeric indices
of 2 or higher, and the maximum selected index is 20. These are recorded
internal iteration indices, not counts of independent benchmark tasks.

## External Evaluation

The evaluator uses the highest-numbered `final_runs/run_NNN` directory for each task.

The external judge receives the task instruction, the selected run's `answer.txt`, and up to the last five screenshots, using the official WebVoyager judging prompt.

The external evaluator selects the highest-numbered run without consulting internal pass/fail labels and does not fall back to an earlier run because it was internally marked successful.

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
