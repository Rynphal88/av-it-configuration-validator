# Requirements Traceability Matrix

This matrix connects the Unit 3 requirements to design modules and current or planned verification evidence. “Planned” means that the requirement belongs to the later implementation or controlled-evaluation stage; it is not presented as a completed result.

| Requirement | Responsible module | Verification evidence | Unit 3 status |
|---|---|---|---|
| FR-01–FR-02 | Input integrity | Type, size, readability, malformed-input, and integrity tests | Size and malformed-input tests implemented; file-level checks planned |
| FR-03–FR-04 | Parser/normalizer | Valid path/value, quoted-value, duplicate-path, and missing-value tests | Foundational tests implemented |
| FR-05–FR-06 | Baseline comparator and rule engine | Compliant, drift, missing-path, and eight-category rule fixtures | Engine scaffold tested; full catalog fixtures planned |
| FR-07–FR-08 | Severity/explanation | Rule-defined severity and expected-versus-observed assertions | Foundational evidence test implemented |
| FR-09 | Report/audit | HTML/JSON schema, escaping, hash, version, and timestamp checks | Planned |
| FR-10 | Human review | Read-only inspection and disposition workflow test | Design control established; workflow test planned |
| NFR-01 | End-to-end pipeline | Monotonic processing-time measurement | Planned for at least 40 controlled variants |
| NFR-02 | Evaluation harness | Precision and recall confusion matrix | Planned; target is at least 90% for each measure |
| NFR-03 | All processing modules | Repeated-run equality and fail-closed negative tests | Partially implemented |
| NFR-04 | Report/human review | Explanation-completeness and reviewer-usability checklist | Planned |
| NFR-05–NFR-06 | Input, report, repository | Threat tests and repository/data inspection | Design controls implemented; expanded tests planned |
| NFR-07–NFR-09 | Architecture and build | Module tests, catalog-extension test, documented Python environment | Architecture and CI scaffold implemented |

## Human decision boundary

Automated severity is a documented triage recommendation. A finding cannot modify a scene or a console. Critical dispositions require an authorized reviewer, and the intended operational workflow calls for a second reviewer before a critical finding is dismissed or an exception is approved.
