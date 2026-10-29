# WebVoyager screenshot re-evaluation

API request options: image detail=default; thinking=on. These options do not change the judging prompt, but may affect model behavior.

Image preprocessing: JPEG quality 85, 4:4:4 chroma; resized to fit 1280x1280; no crop. JPEG is lossy transport; source artifacts are unchanged.

Purpose: **pilot**. This report does not claim leaderboard approval.

Model: glm-5.3-flash; prompt variant: standard.

Answer input: answer.txt only. Use only the selected run's answer.txt. If answer.txt is absent or empty, the task is missing an answer. Never read final_response.txt, final_script_log.txt, evidence files, or older runs.

Tasks: 615; accepted: 593; acceptance rate: INCOMPLETE (not a final score).

Missing evidence is unsuccessful. API/parse/evaluation errors are unresolved, not silently dropped.

| Website | Tasks | Accepted | Rejected | Missing evidence | Unresolved | Rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Allrecipes | 40 | 39 | 1 | 0 | 0 | 97.50% |
| Amazon | 40 | 32 | 4 | 3 | 1 | incomplete |
| Apple | 40 | 40 | 0 | 0 | 0 | 100.00% |
| ArXiv | 43 | 42 | 0 | 0 | 1 | incomplete |
| BBC News | 39 | 39 | 0 | 0 | 0 | 100.00% |
| Booking | 40 | 39 | 1 | 0 | 0 | 97.50% |
| Cambridge Dictionary | 41 | 41 | 0 | 0 | 0 | 100.00% |
| Coursera | 40 | 40 | 0 | 0 | 0 | 100.00% |
| ESPN | 44 | 43 | 0 | 0 | 1 | incomplete |
| GitHub | 41 | 39 | 1 | 0 | 1 | incomplete |
| Google Flights | 40 | 37 | 3 | 0 | 0 | 92.50% |
| Google Map | 40 | 40 | 0 | 0 | 0 | 100.00% |
| Google Search | 42 | 39 | 3 | 0 | 0 | 92.86% |
| Huggingface | 39 | 38 | 0 | 0 | 1 | incomplete |
| Wolfram Alpha | 46 | 45 | 0 | 0 | 1 | incomplete |

Selected task records and image hashes are frozen in selection_manifest.json.
Only the selected final execution is judged; old self-reflection labels are never inputs.
Reports contain task/answer/evidence metadata and are NOT automatically sanitized for publication.
