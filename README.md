# AV/IT Configuration Validator

This repository supports the MSIT 5910 capstone project **Design and Evaluation of an Automated Configuration Validation System for Professional AV IT Environments: An ASEL Case Study**.

**Repository:** https://github.com/Rynphal88/av-it-configuration-validator

The project is a bounded, read-only proof of concept for validating selected Behringer X32 `.scn` configuration data. It is designed to compare a proposed configuration with an approved baseline, execute a catalog of high-risk rules, classify findings, and produce an explainable report for human review.

## Current status

Unit 5 core-logic milestone. The repository contains the architecture, requirements, traceability matrix, an eight-rule sanitized catalog, read-only input checks, deterministic parsing and severity prioritization, explainable report output, automated tests with coverage enforcement, and assignment documentation. It is not production-ready and does not control or modify a live console.

## Safety and scope boundaries

- No live-console communication
- No automatic configuration changes
- No execution of imported file content
- No unsanitized production scene files in the repository
- No artistic or tonal recommendations
- Human approval remains mandatory before deployment

## Repository layout

```text
src/                    Source-code scaffold
tests/                  Automated unit tests
docs/requirements/      System requirements and traceability
docs/progress/          Milestones and design-phase progress
docs/submissions/       Unit 3 Word-document deliverables
design/architecture/    Architecture diagram and design notes
rules/                  Sanitized validation-rule schema
sample-configs/         Sanitized or synthetic test data only
reports/                Generated validation and evaluation reports
.github/workflows/      Continuous-integration configuration
```

## Branching model

- `main`: reviewed, stable academic milestones
- `develop`: integrated design and implementation work
- `feature/*`: focused changes merged into `develop`

Changes are committed with action-oriented messages. Feature work is reviewed before promotion to `develop`, and stable milestones are promoted to `main` after tests and documentation checks pass.

## Local verification

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python -m coverage run --branch --source=src/av_validator -m unittest discover -s tests -v
python -m coverage report --show-missing
```

## Unit 4 demonstration

The demonstration uses only synthetic files. From the repository root, run:

```bash
PYTHONPATH=src python -m av_validator \
  --candidate sample-configs/sanitized/candidate-drift.scn \
  --baseline sample-configs/sanitized/approved-baseline.scn \
  --rules rules/demo_rules.json
```

The report identifies four controlled routing deviations and shows the rule,
protected path, expected value, observed value, severity, and rationale. Replace
`candidate-drift.scn` with `candidate-compliant.scn` to demonstrate a compliant
result. Critical findings are presented first, but their rule-defined severity is
not changed. The report records that no automated action occurs and that an
authorized person must review findings. The command reads candidate and baseline
files without modifying them.

On Windows PowerShell, use the following one-line commands after installing the
project with `python -m pip install -e .`:

```powershell
python -m av_validator --candidate sample-configs/sanitized/candidate-drift.scn --baseline sample-configs/sanitized/approved-baseline.scn --rules rules/demo_rules.json
python -m av_validator --candidate sample-configs/sanitized/candidate-compliant.scn --baseline sample-configs/sanitized/approved-baseline.scn --rules rules/demo_rules.json
```

## License and data

Only original code, documentation, and sanitized examples should be published. Vendor documentation and authorized ASEL configuration data remain outside this repository unless redistribution is explicitly permitted.
