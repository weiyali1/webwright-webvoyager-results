# Webwright WebVoyager Results

## Result

| System | Organization | Benchmark | Score |
| --- | --- | --- | --- |
| Webwright + Qwen3.8-Max | Independent | browser-control-fable-5 | 601/615 (97.72%) |

This is a self-reported system-level result on all 615 tasks in
`browser-control-fable-5`, a WebVoyager-derived variant produced through task
filtering and task updates. Dates were additionally updated for stale tasks in
this evaluation.

## Evaluation setup

- Benchmark source: <https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5>
- Benchmark variant: 615 WebVoyager-derived tasks after task filtering and task
  updates.
- Evaluation type: self-reported system-level evaluation.
- Evaluator: a custom critical-point judge using task critical points,
  screenshots, and execution logs.
- Each task includes internal self-healing and self-check mechanisms within the
  task run.
- Tasks whose runs failed because of stale dates, model API errors, or browser
  crashes were rerun.

## Result summary

- Total tasks: 615
- Successful tasks: 601
- Unsuccessful tasks: 14
- Success rate: 97.72%

## Public evidence

- [`tasks/`](tasks/) contains the 15 website JSON files defining all 615 tasks
  evaluated in this WebVoyager-derived variant.
- [`results.csv`](results.csv) contains the reported result for every task.
- [`manifest.json`](manifest.json) records the selected run and judge-result
  counts for all 615 tasks.
- [Full task artifacts](https://github.com/weiyali1/webwright-webvoyager-results/releases/tag/webvoyager-2026-10-15)
  are split into 15 website archives. Each task contains its `task.json` and
  `final_runs` evidence, including final answers and screenshots.
- [`SHA256SUMS`](SHA256SUMS) provides checksums for all evidence archives.

Published copies redact local filesystem paths, company model endpoints, and
credential-shaped values. Compiled Python cache files are omitted. Original
evaluation outputs remain unchanged.

## Reporting

- Reporting organization: Independent
- Published: 2026-10-15
