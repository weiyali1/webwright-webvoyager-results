# Judge-Output Parsing and Scoring Correction

## Judge-Side Errors and Scoring Correction

The original evaluation script and all raw judge outputs are preserved
unchanged.

The original harness recorded 11 initial outputs as parse_error and
rejudged them using identical frozen inputs. Its last-line-only parser
missed verdicts followed by explanatory text.

Final scoring was reconstructed from the saved judge texts using the
upstream WebVoyager parsing rule:

- An output containing NOT SUCCESS is unsuccessful.
- Otherwise, an output containing SUCCESS is successful.
- An output containing neither remains unparseable.

Matching is case-sensitive, as in the upstream implementation.
Each task uses its earliest definitive judgment under this rule.

Reparsing the 11 initial outputs identifies two initial failures,
three initial successes, and six initially unparseable outputs.

The five rejudgments following an already parseable initial result
remain published for auditing but are excluded from result selection:

- Apple--21: use the initial SUCCESS.
- ArXiv--38: use the initial NOT SUCCESS.
- ESPN--29: use the initial SUCCESS.
- Google Flights--26: use the initial SUCCESS.
- Google Search--39: use the initial NOT SUCCESS.

Only the six initially unparseable cases use later judgments.

ArXiv--38 changes from success to failure. The other four tasks retain
their final outcome labels, but use their initial evaluation records.

The corrected total is 600 successes, 11 failures, and 4 missing-evidence
tasks out of 615.

Success rate = 600 / 615 × 100% = 97.5609756%, displayed as 97.56%.

All raw records retain their historically saved status fields.
Corrected selections and provenance are recorded in
evaluation/merged_results.json and evaluation/REJUDGMENT_AUDIT.json.

This correction involved no additional model calls or browser-task
executions. The original evaluation script remains unchanged.
