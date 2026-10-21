# Evaluation Methodology

## Task set

The evaluation used all 615 tasks from the WebVoyager-derived
[`browser-control-fable-5`](https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5)
variant. This variant was produced through task filtering and task updates.
Dates in stale tasks were additionally updated before this evaluation.

The exact task definitions used for the evaluation are published in the
[`tasks`](tasks/) directory.

## System

The evaluated system was Webwright + Qwen3.8-Max.

## Judge

The result was evaluated with a custom critical-point judge. The judge used the task's critical points together with screenshots, execution logs, final answers, and saved evidence to determine whether the task was completed successfully.
For each task, the execution agent generated a task-specific critical-point list and judging prompts based on the task definition. 
In stage one, the judge reviewed each execution screenshot individually. For each screenshot, it described which critical points the image supported or contradicted and assigned an evidence score from 1 to 5. In stage two, the judge received the original screenshots, the per-image analyses, and the corresponding execution log, including the final answer recorded in that log. It checked the critical points item by item. The judging prompt required all necessary critical points to be satisfied for a success verdict. The per-image evidence scores were not summed or averaged to produce the final verdict.
Each execution's verdict is stored in final_runs/run_NNN/judge_result.json: predicted_label: 1 means automatic judge acceptance, 0 means judge rejection, and null means the verdict could not be parsed.

## Internal final-run workflow

The `final_runs/run_NNN` directories represent sequential clean executions
inside a single task-level self-healing and verification workflow. They are
not separate benchmark submissions or independently reported benchmark
trials.

During a task, the system may revise its final script and execute it again in
the next `run_NNN` directory when the current execution does not satisfy the
task's critical points. Each internal run directory contains the script,
execution log, screenshots, evidence, final response, and judge result for
that execution.

A task was counted as successful when its selected task-level evaluation
record contained a verified final execution whose `judge_result.json` had
`predicted_label: 1`. Earlier failed internal executions were retained as
audit evidence. Regardless of the number of internal `run_NNN` directories,
each benchmark task contributed at most one result to the reported score.

## Recovery, self-check, and reruns

Every task included an internal self-healing and self-check workflow. A failed
final-script verification could trigger an internal revision followed by
another clean execution within that same task-level workflow.

Tasks affected by stale dates, model API errors, or browser crashes were also
rerun. 

## Score calculation

The numerator counts unique successful benchmark tasks rather than successful
internal executions. Multiple internal final runs belonging to the same task
do not increase the numerator.

The system successfully completed 601 unique tasks out of 615 evaluated tasks:

`601 / 615 = 97.72%`

This is a self-reported system-level success rate.
