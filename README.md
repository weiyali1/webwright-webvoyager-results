# Webwright WebVoyager Results

## Result

| System | Organization | Judge | Score |
| --- | --- | --- | --- |
| Webwright + Qwen3.8-Max | Independent |  GLM-5.3-Flash (Official Prompts) | 598/615 (97.23%) |


Task set
The evaluation used all 615 tasks from the WebVoyager-derived browser-control-fable-5 variant. This variant was produced through task filtering and task updates. Dates in stale tasks were additionally updated before this evaluation.

The exact task definitions used for the evaluation are published in the tasks directory.

Execution System
The evaluated execution system was Webwright + Qwen3.8-Max. This system is responsible for navigating the browser, generating task-specific critical-point lists, and executing the tasks to produce screenshots, logs, evidence, and final answers.

Judge / Evaluation Model
The evaluation results were assessed using GLM-5.3-Flash acting as the judge, utilizing the official judging prompts (the custom critical-point judge prompts provided by the benchmark). The judge used the task's critical points together with screenshots, execution logs, final answers, and saved evidence to determine whether the task was completed successfully.

## Evaluation setup

- Benchmark source: <https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5>
- Benchmark variant: 615 WebVoyager-derived tasks after task filtering and task
  updates.
- Evaluation type: self-reported system-level evaluation.
- Evaluator: Evaluation was performed using GLM-5.3-Flash with the official WebVoyager judging prompts. 


## Result summary

- Total tasks: 615
- Successful tasks: 598
- Unsuccessful tasks: 17
- Success rate: 97.23%

## Public evidence

- [`tasks/`](tasks/) contains the 15 website JSON files defining all 615 tasks
  evaluated in this WebVoyager-derived variant.
  counts for all 615 tasks.
- [Full task artifacts](https://github.com/weiyali1/webwright-webvoyager-results/releases/tag/webvoyager-2026-10-26)
  are split into 15 website archives. Each task contains its `task.json` and
  `final_runs` evidence, including final answers and screenshots.
- [`SHA256SUMS`](SHA256SUMS) provides checksums for all evidence archives.

Published copies redact local filesystem paths, company model endpoints, and
credential-shaped values. Compiled Python cache files are omitted. Original
evaluation outputs remain unchanged.

## Reporting

- Reporting organization: Independent
- Published: 2026-10-26
