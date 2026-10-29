# Evaluation Methodology


## Task Set

This evaluation used all 615 tasks from the WebVoyager-derived variant `browser-control-fable-5`. The variant was created through task filtering and updates; for dates in tasks that had become stale, they were updated before execution.

The exact task definitions used in this evaluation are published in the [`tasks/`](tasks/) directory.

## Execution System and Evaluation Batch

The evaluated system was Webwright + Qwen3.8-Max.

This evaluation used one independent execution batch and did not combine task records from other batches.

The `final_runs/run_NNN/` directories contain the internal execution, validation, and repair artifacts produced by Webwright during task execution. These directories belong to the same task workflow and do not represent independent benchmark task runs or additional submissions.

For each unique `task_id`, the evaluator selected the highest-numbered `run_NNN` directory under its execution record as the final output. Earlier internal run directories were retained for auditing but were not scored separately. Each task contributed only one final evaluation result.

## Judge Model and Evaluation Inputs

The post-hoc evaluation used `GLM-5.3-Flash` with the official WebVoyager judging prompt.

For each task, the evaluator sent the following to the judge model:

- The task instruction;
- The `answer.txt` in the selected run directory;
- Up to five trailing screenshots from that run directory.

The evaluator did not re-execute the browser task. The original `judge_result.json` files were retained as execution artifacts but were not used as the final verdicts for this post-hoc evaluation.

## Answer Preprocessing

Some `final_response.txt` files contained internal self-evaluation or verdict information, such as:

- `self-reflection judge verdict: PASS`
- `predicted_label`
- `Status: success`

To prevent this content from influencing the external judging, the final answer text was extracted and cleaned before evaluation, and the result was saved as `answer.txt` in the corresponding run directory.

The cleaning covered trailing internal self-evaluation or verdict segments, as well as additional leading success statements. The evaluation stage read only the cleaned `answer.txt` and did not submit the raw response files or full execution logs directly to the judge model as answers.

### Answer Source Selection

1. If `final_response.txt` existed in the selected run directory, it was used as the answer source.
2. If `final_response.txt` did not exist, the final task-answer content was extracted from `final_script_log.txt` in the same run directory.
3. If the above source selection and cleaning process produced no usable answer, the task was marked as `missing_evidence`, retained in the total task count, and counted as unsuccessful.

The fallback to `final_script_log.txt` was triggered by the absence of `final_response.txt`. Answers were not taken from earlier run directories, other execution records, other batches, or evidence JSON files.

During extraction and cleaning, only the task-answer content was retained, and execution logs, internal self-check results, internal verdict information, and text such as `self-reflection judge verdict: PASS` were excluded.

## Judge-Side Errors and Parsing-Error Re-evaluation

`parse_error`, `evaluation_error`, and `api_error` indicate problems encountered when submitting judging requests or processing judging results, such as API timeouts, empty responses, failure to parse a valid `SUCCESS` / `NOT SUCCESS` verdict, or evaluation processing exceptions. These statuses themselves are not directly equivalent to agent task execution failure.

Among them, `parse_error` indicates that the response was not accepted by the parser at the time, and does not necessarily mean that the response contained no verdict at all. The current parser requires a recognizable final verdict to appear on the last non-empty line of the response; if explanatory text follows the verdict, the response may also be recorded as `parse_error`.

In this evaluation, the 6 tasks initially recorded as `parse_error` were re-judged in the independent `parse_error_retry/` output directory. After the first re-evaluation, 1 task still could not be parsed, and this task was subsequently re-judged in `parse_error_retry2/` and ultimately received a `NOT SUCCESS` verdict.

These re-evaluations used the same task instructions, answers, and screenshots, only adding judging requests, without re-executing the browser tasks or changing the selected execution evidence. The above parsing-error re-evaluations were completed in new output directories.

The original judging responses and subsequent re-evaluation results were retained in their respective output directories. The final results were merged by `task_id`, replacing the corresponding unresolved records with the subsequent re-evaluation results; each task was counted only once in the final result.

| Evaluation Stage | Tasks | Success | Failure | Missing Evidence | Parse Error |
| --- | ---: | ---: | ---: | ---: | ---: |
| Initial evaluation | 615 | 593 | 13 | 3 | 6 |
| First parsing-error re-evaluation | 6 | 4 | 1 | 0 | 1 |
| Second parsing-error re-evaluation | 1 | 0 | 1 | 0 | 0 |
| Final merged result | 615 | 597 | 15 | 3 | 0 |

## Missing Evidence and Score Calculation

If the selected run lacked a usable prepared answer or the required execution screenshots, the task was counted as unsuccessful and retained in the denominator of all 615 tasks.

The final statistics after task-level aggregation are as follows:

| Category | Tasks |
| --- | ---: |
| Successful tasks | 597 |
| Tasks judged unsuccessful | 15 |
| Tasks with missing evidence | 3 |
| Unresolved tasks | 0 |
| Total | 615 |

The total number of unsuccessful tasks was 18, including 3 tasks with missing evidence.

The success rate is:

```text
597 / 615 × 100% = 97.07%
```

This is a task-level success rate. Final statistics are calculated over unique task IDs. Judge-side re-evaluations replace unresolved judgments rather than add duplicate task results.
