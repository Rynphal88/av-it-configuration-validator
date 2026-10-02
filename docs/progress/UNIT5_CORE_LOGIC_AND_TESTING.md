# Unit 5 Core Logic and Testing

The Unit 5 milestone implements the full eight-category sanitized rule catalog,
deterministic finding prioritization, an explicit human-review boundary, and
expanded automated testing. Exact comparisons preserve the rule-defined
severity. Findings are ordered critical, major, minor, and informational for
review, with the rule identifier providing a deterministic tie-breaker.

The report never modifies a scene or recommends an automatic configuration
change. It records `automated_action` as `none`. A critical finding produces a
hold-for-review recommendation, while an authorized person retains the final
operational decision.

## Verification evidence

- End-to-end tests exercise both controlled drift and compliant samples.
- Integrity tests cover extension, size, UTF-8 decoding, byte count, and hash.
- Parser tests cover valid, malformed, duplicate, missing-value, and boundary input.
- Engine tests cover compliant, missing, severity-preserving, and deterministic ordering behavior.
- Reporting tests verify explainable evidence, JSON output, and the human-review boundary.
- CI runs branch coverage and fails below 85 percent.

## Portability correction

The original integrity fixture used `Path.write_text`, which can translate a
line feed to a Windows carriage-return/line-feed pair. That made a byte-exact
test platform-dependent. The fixture now uses `write_bytes`, so the test defines
the intended input bytes identically on Windows and Linux.
