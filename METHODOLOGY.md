# Evaluation Methodology

## Task set

The evaluation used all 615 tasks from the
[`browser-control-fable-5`](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5)
task set. Dates in stale tasks were updated before evaluation.

## System

The evaluated system was Webwright + Qwen3.8-Max.

## Judge

The result was evaluated with a custom critical-point judge. The judge used
the task's critical points together with screenshots and execution logs to
determine whether the task was completed successfully.

## Recovery, self-check, and reruns

Every task run included internal self-healing and self-check mechanisms. A
task was rerun when its run failed because of a stale date, a model API error,
or a browser crash.

## Score

The system successfully completed 601 of 615 tasks, producing a self-reported
system-level success rate of 97.72%.
