# Historical task-comparison records

This supplement contains four existing local task-comparison files and a file-manager screenshot of their original local modification times.

## Report files

- [report.md](report.md): the historical comparison summary.
- [comparison.json](comparison.json): complete before-and-after definitions for the 49 month-edited tasks and the recorded task-file SHA-256 values.
- [checks.csv](checks.csv): the historical comparison checks for all 615 tasks.
- [github_source.jsonl](github_source.jsonl): the upstream reference retained with the comparison.

## Recorded time sequence

All times below are UTC+08:00.

- The historical report records a comparison time of **October 30, 2026, at 10:43:52**.
- The original four report files currently have local modification times around **10:45:29** on the same day. The file-manager screenshot displays **10:45**.
- Among the 49 edited tasks, the earliest submitted execution-directory timestamp is **11:00:26**, and the earliest saved model-response timestamp is **11:00:41**, both on October 30.
- All 49 corresponding execution-directory and first-response timestamps are later than the recorded report time and those local file-modification times.

![Original report files and displayed local modification times](report_file_times.png)

The screenshot shows the original files' local modification times. Local account information has been redacted; the filenames and displayed modification times are retained.

The times above are taken from the existing local report, original-file metadata, and saved execution records. They describe the original records, not the time this public copy was prepared.

## Content correspondence

The following checks distinguish byte-for-byte file equality from equality of parsed task objects:

- Of the 15 website task-definition files, 13—including `google_flight.json`—have SHA-256 hashes that exactly match the values recorded in the historical report.
- For `Booking.json`, removing one additional newline and two spaces from the current file reproduces the historical SHA-256. All 40 parsed Booking task objects match the definitions reconstructed from the retained comparison records and upstream reference.
- For `Google_Map.json`, removing two additional indentation spaces from the current file reproduces the historical SHA-256. All 40 parsed Google Map task objects likewise match the reconstructed historical definitions.
- The historical report also records a hash for `manifest.json`. That file is not present in the current task-definition directory, so this entry has not been verified. It is separate from the 15 website task-definition files; all 615 task objects are accounted for and match the reconstructed historical definitions.

For all 49 edited tasks, the historical definitions match the published task definitions, the saved execution instructions, and the first saved user messages.

The original report files have not been changed. These public copies retain their contents except that one absolute local project path in report.md has been replaced with <LOCAL_PROJECT> for privacy.
