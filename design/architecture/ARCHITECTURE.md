# Architecture Blueprint

The system uses a layered, modular pipeline. An engineer selects a candidate scene file and approved baseline through a local interface. The input-integrity module validates size, format, and hash metadata. The parser and normalizer convert only supported path-value records into an internal representation. The baseline comparator identifies drift, while the rule engine evaluates eight high-risk invariants. A deterministic severity and explanation module attaches rule-defined risk and evidence. The report generator produces human-readable and machine-readable outputs. An audit record stores the analyzed file hash, baseline version, rule version, timestamp, and result summary.

Reference data is separated into the approved baseline store and versioned rule catalog. Git records source, requirements, design, tests, and sanitized data. Continuous integration runs automated checks, but no workflow connects to or changes live equipment.
