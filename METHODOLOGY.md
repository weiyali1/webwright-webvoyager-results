# Evaluation Methodology

## Task set

The evaluation uses all 615 tasks from the `browser-control-fable-5` variant derived from WebVoyager:

<https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5>

The variant was created by filtering and updating tasks. Dates in tasks that had become stale were also updated before this evaluation. The exact task definitions used for the evaluation are included in the [`tasks/`](tasks/) directory.

## System

The evaluated system is Webwright running with Qwen3.8-Max.

## Judge model and evaluation inputs

The judge model is `glm-5.3-flash`. The evaluation uses the official WebVoyager judging prompt from [`evaluation/auto_eval.py`](https://github.com/MinorJerry/WebVoyager/blob/main/evaluation/auto_eval.py).

For each unique `task_id`, the evaluator sends the selected run's task instruction, final answer, and up to the last five screenshots to the judge model. The screenshots are evidence for the final state of the browser task; the evaluator does not execute the task again.

The answer input is selected using this rule:

1. Use `final_response.txt` from the selected run when it exists and contains a usable answer.
2. If that file is missing, empty, or marked incomplete, read `final_script_log.txt` from the same run.
3. From that log, extract the last complete labelled `Final Response:` block, including its following multi-line content.
4. If neither source provides a usable answer, mark the task as missing evidence and count it as unsuccessful in the task-level denominator.

The evaluator does not use an answer from an evidence JSON file or from an older run. The source `judge_result.json` files are retained as execution artifacts, but they are not used as the verdict for this `glm-5.3-flash` evaluation.

## Execution records and internal final runs

Each of the 615 benchmark tasks was executed once by Webwright. There was no second benchmark execution or task-level rerun for these results. Each task has one task directory and one timestamped execution record.

The `final_runs/run_NNN/` directories are outputs produced by the Webwright framework during that single task execution. They describe the framework's internal execution, validation, and final-result stages. They are implementation artifacts, not independent benchmark submissions and not additional task runs. Regardless of how many such directories a task contains, that task contributes at most one score entry.

For evaluation, the framework's final output is taken from the highest-numbered `run_NNN` directory in that task's `final_runs/` directory. Earlier internal run directories are retained for audit and are not counted separately.

The only retries described here are judge-side request or response-handling retries caused by transport or parsing problems. They do not rerun the Webwright task. A judge retry replaces the unresolved judge result for the same task and cannot increase the number of benchmark tasks.

## Verdict and score calculation

The external judge response is parsed for an unambiguous `SUCCESS` or `NOT SUCCESS` verdict. A task contributes at most one result after task-level selection and retry deduplication.

After evaluating the 615 selected final outputs and resolving judge-side parse-error retries, the final task-level counts are:

- 598 successful tasks;
- 11 judge failures;
- 3 tasks with missing evidence.

Therefore, the reported system-level success rate is:

```text
601 / 615 = 97.72%
```

This is a task-level success rate. Multiple `run_NNN` directories or judge retries for the same `task_id` do not increase the numerator.
