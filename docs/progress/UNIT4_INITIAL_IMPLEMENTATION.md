# Unit 4 Initial Implementation

The Unit 4 milestone converts the approved layered design into a demonstrable,
read-only command-line prototype. The implementation adds file-integrity checks,
baseline-bound declarative rules, deterministic text and JSON reporting, and
synthetic demonstration files. The parser and rule engine remain separate, and
the output provides expected-versus-observed evidence for human review.

## Demonstrated functions

1. Input integrity and deterministic parsing reject unsupported, oversized,
   malformed, missing-value, or duplicate-path input.
2. Baseline comparison and rule evaluation identify controlled drift without
   changing the candidate configuration.
3. Explainable reporting displays the rule, path, expected value, observed
   value, severity, and rationale.

## Boundaries

The milestone does not connect to a live console, change a scene file, automate
remediation, or claim field effectiveness. Samples contain synthetic paths and
values only. Human review remains required before any operational action.
