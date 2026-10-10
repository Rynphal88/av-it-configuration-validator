# Unit 6 Integration, Evaluation, and Deployment Planning

## Integrated workflow

The `validate_configuration` application service composes the input-integrity,
parser, rule-catalog, comparison, prioritization, and reporting modules. The CLI
calls that service for both text and JSON output, so the interactive and
machine-readable paths use the same core logic. All candidate and baseline
inputs remain read-only, and the report always records `automated_action` as
`none`.

## Controlled evaluation

`tools/run_evaluation.py` creates 40 temporary, synthetic single-drift variants:
five variants for each of the eight protected-path rules. Ground truth is known
before execution. The harness records confusion-matrix counts, precision,
recall, decision accuracy, mean/median/p95 latency, throughput, and peak traced
Python memory. It also applies a five-item, non-participant heuristic inspection
to task discoverability, error feedback, finding clarity, safety visibility,
and output flexibility. These results are bounded evidence, not a claim about
all X32 firmware versions, live venues, or participant usability.

## Deployment selection

The selected method is a versioned Docker image run locally or on an internal,
access-controlled host. The image is reproducible, runs as a non-root user, and
accepts scene and rule paths through read-only mounts. A managed public-cloud
service is unnecessary for this proof of concept and would expand the data and
network threat surface. Direct workstation installation remains useful for
development but offers weaker environment consistency.

## Human decision boundary

Automated severity is deterministic triage based on the approved rule catalog;
it is not an operational command. A finding shows expected and observed values,
rule rationale, and file hashes. An authorized engineer reviews every finding.
Critical exceptions or dismissals require a second reviewer in the intended
workflow, and no code path writes to a scene file or console.
