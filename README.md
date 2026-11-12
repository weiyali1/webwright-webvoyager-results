# Webwright WebVoyager Results

**Webwright (Qwen3.8-Max): 600/615 tasks, 97.56%.**

This repository publishes a self-reported system-level evaluation on 615 tasks adapted from the [browser-control-fable-5](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5) task collection in omxyz/webvoyager.

Reported by [XYDT](https://www.xydigit.com/).

The exact task definitions used for execution and evaluation are published in [`tasks/`](submissions/webvoyager-2026-11-03/tasks/). The agent and external judge used the same updated task instructions. The reported score applies to this date-updated collection of 615 tasks.

The external judge is GLM-5.3-Flash, using the official WebVoyager judging prompt.

Webwright uses an agent-generated self-verification and repair loop during task execution. The agent writes the internal critical points and expected answer; feedback can trigger script revisions and additional runs within the same task record. Multiple `final_runs/run_NNN` directories preserve these internal iterations, while each unique task contributes one final evaluation result.

| Outcome | Tasks |
| --- | ---: |
| Success | 600 |
| Failure | 11 |
| Missing evidence | 4 |
| Total | 615 |

- [Complete results and framework workflow](submissions/webvoyager-2026-11-03/README.md)
- [Evaluation methodology](submissions/webvoyager-2026-11-03/METHODOLOGY.md)
- [Exact task collection](submissions/webvoyager-2026-11-03/tasks/)
- [Evaluation script](submissions/webvoyager-2026-11-03/evaluator/evaluate_webvoyager.py)
- [Raw evaluation records](submissions/webvoyager-2026-11-03/evaluation/raw/)
- [Merged final judgments](submissions/webvoyager-2026-11-03/evaluation/merged_results.json)
- [Final summary](submissions/webvoyager-2026-11-03/evaluation/summary.json)
- [Execution evidence downloads](https://github.com/weiyali1/webwright-webvoyager-results/releases/tag/webvoyager-2026-11-03)
- [Task-definition timing supplement](submissions/webvoyager-2026-11-03/evidence/report_time/)

The 15 ZIP archives contain task records grouped by website.

## Scoring correction

The score is corrected to 600/615 (97.56%) after reinterpreting the saved judge outputs. The original evaluation script and raw records are unchanged. See [the correction report](submissions/webvoyager-2026-11-03/SCORING_CORRECTION.md).
