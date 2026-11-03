# Webwright WebVoyager Results

**Webwright + Qwen3.8-Max: 601/615 tasks, 97.72%.**

This repository publishes a self-reported system-level evaluation on 615 tasks adapted from the [browser-control-fable-5](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5) task collection in omxyz/webvoyager.

Before execution, stale dates in date-sensitive tasks were updated. The agent and external judge used the same updated task instructions. The exact executed and evaluated task definitions are published in this submission. The reported score applies to this date-updated collection of 615 tasks.

The external judge is GLM-5.3-Flash, using the official WebVoyager judging prompt.

Webwright supports self-repair during task execution. Multiple `final_runs/run_NNN` directories preserve internal execution, validation, and repair iterations. Each unique task contributes one final evaluation result.

| Outcome | Tasks |
| --- | ---: |
| Success | 601 |
| Failure | 10 |
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

The 15 ZIP archives contain task records grouped by website.
