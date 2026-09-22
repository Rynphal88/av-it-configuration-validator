# Module Specifications

| Module | Input | Output | Method and safeguard |
|---|---|---|---|
| Input integrity | Candidate scene, approved baseline, input policy | Accepted streams and hashes, or a rejection | Allowlisted file type, size and encoding limits, checksum verification, fail-closed errors |
| Parser/normalizer | Validated text | Canonical path/value records | Deterministic grammar; malformed, missing-value, and duplicate-path rejection |
| Baseline manager | Approved file and manifest | Immutable comparison model | Version and hash binding; read-only access; provenance metadata |
| Comparison/rule engine | Observed model, baseline, rule catalog | Pass/fail rule evaluations | Exact predicates for the eight documented high-risk categories |
| Severity/explanation | Rule result and rationale | Critical, major, minor, or informational finding | Rule-defined rating; expected-versus-observed evidence; no learned classification |
| Report/audit | Findings and run metadata | Human-readable and machine-readable reports | Escaped output; file and ruleset hashes; timestamps; minimum necessary retention |
| Human review | Explainable report and event context | Approve, reject, investigate, or document an exception | Named reviewer; second review for critical dispositions; no automatic remediation |

## Data flow

Data moves forward through the pipeline. Imported content is treated as data and is never executed. The report layer displays rule results but does not recalculate severity. Source scenes and approved baselines are opened read-only, and generated reports are stored separately.

## Safety boundary

The Unit 3 prototype has no live-console client, write-back path, or automatic-remediation command. Its output supports professional judgment; it does not certify an entire production mix.
