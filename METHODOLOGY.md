# Evaluation Methodology

## Task Set

This evaluation used all 615 tasks from `browser-control-fable-5`, a WebVoyager-derived variant:

https://github.com/omxyz/webvoyager/tree/main/benchmark/data/browser-control-fable-5

The variant was created through task filtering and updates. Dates in tasks that had become stale were updated before execution. The exact task definitions used in this evaluation are included in the [`tasks/`](tasks/) directory.

## Execution System

The evaluated system was Webwright + Qwen3.8-Max.

## Judge Model and Evaluation Inputs

The post-hoc evaluation used `glm-5.3-flash` with the official WebVoyager judging prompt from [`evaluation/auto_eval.py`](https://github.com/MinorJerry/WebVoyager/blob/main/evaluation/auto_eval.py).

For each unique `task_id`, the evaluator sent the selected run's task instruction, final answer, and up to the last five screenshots to the judge model. The screenshots provided visual evidence of the task outcome; the evaluator itself did not rerun the browser task.

### Final Answer Extraction

Before evaluation, the final answer was extracted from the selected run's output files and saved as `answer.txt`:

1. Preferentially extract the final answer from `final_response.txt` in the selected run.
2. If that file is missing, extract the final answer from `final_script_log.txt` in the same run.
3. Retain only the answer content, excluding execution logs, internal self-check results, and verdict statements such as `self-reflection judge verdict: PASS`, to prevent those statements from influencing the external judge.
4. If neither source provides a usable answer, mark the task as missing evidence, retain it in the total task count, and count it as unsuccessful.

During evaluation, the evaluator reads only the generated `answer.txt`. It does not directly use raw logs as the answer or supplement the answer with content from evidence JSON files or earlier runs.

The original `judge_result.json` files are retained as execution artifacts but are not used as verdicts for this `glm-5.3-flash` post-hoc evaluation.

## Execution Records and Internal Run Directories

This evaluation used task execution records from the same batch. Failed tasks were not repeatedly rerun until successful. Each task corresponds to one task directory and one timestamped execution record.

The `final_runs/run_NNN/` directories are internal artifacts produced by the Webwright framework during task execution. They record the framework's internal execution, validation, and final-output generation stages. These directories do not represent independent benchmark submissions or additional task-level runs. Regardless of how many such directories a task contains, it contributes at most one final evaluation result.

For evaluation, the highest-numbered `run_NNN` directory within the task's `final_runs/` directory is selected as the final output. Earlier internal run directories are retained for auditing and are not scored separately.

## Judge-Side Retries

The retries described here apply only to judge requests or response processing affected by transport or parsing problems. They do not rerun the Webwright task.

Judge-side retries resolve incomplete evaluations for the same task without increasing the number of benchmark tasks. After retry results are deduplicated by `task_id`, only one final verdict is retained for each task. Multiple judge requests do not cause a task to be counted more than once.

## Verdict and Score Calculation

The evaluator parses the external judge model's response for an unambiguous `SUCCESS` or `NOT SUCCESS` verdict. After task-level selection and retry deduplication, each task contributes at most one result.

After evaluating the selected final outputs for all 615 tasks and resolving judge-side parsing errors through retries, the final counts were:

| Category | Number of Tasks |
| --- | ---: |
| Successful tasks | 597 |
| Tasks judged unsuccessful | 15 |
| Tasks with missing evidence | 3 |
| Total | 615 |

Tasks with missing evidence are counted as unsuccessful and remain in the denominator of all 615 tasks. There are therefore 18 unsuccessful tasks in total, and the system-level success rate is:

597 / 615 × 100% = 97.07%

This is a task-level success rate. Neither multiple internal `run_NNN` directories nor judge-side retries for the same `task_id` increase the total task count or the successful task count.
