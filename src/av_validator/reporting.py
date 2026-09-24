"""Deterministic console and JSON reports for validation findings."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from .integrity import SceneArtifact
from .models import Finding


def build_report(
    candidate: SceneArtifact,
    baseline: SceneArtifact,
    findings: list[Finding],
    *,
    rule_count: int,
    rules_sha256: str,
) -> dict[str, Any]:
    """Build a stable, machine-readable report without modifying inputs."""

    severity_counts = Counter(finding.severity.value for finding in findings)
    return {
        "status": "findings" if findings else "compliant",
        "candidate": {
            "name": candidate.path.name,
            "size_bytes": candidate.size_bytes,
            "sha256": candidate.sha256,
        },
        "baseline": {
            "name": baseline.path.name,
            "size_bytes": baseline.size_bytes,
            "sha256": baseline.sha256,
        },
        "rules": {"evaluated": rule_count, "sha256": rules_sha256},
        "summary": {"finding_count": len(findings), "by_severity": dict(sorted(severity_counts.items()))},
        "findings": [
            {
                "rule_id": finding.rule_id,
                "name": finding.name,
                "path": finding.path,
                "expected": list(finding.expected),
                "observed": None if finding.observed is None else list(finding.observed),
                "severity": finding.severity.value,
                "rationale": finding.rationale,
            }
            for finding in findings
        ],
    }


def format_text_report(report: dict[str, Any]) -> str:
    """Format the report for an engineer reviewing a terminal session."""

    lines = [
        "AV/IT Configuration Validation Report",
        "====================================",
        f"Status: {report['status'].upper()}",
        f"Candidate: {report['candidate']['name']} ({report['candidate']['size_bytes']} bytes)",
        f"Candidate SHA-256: {report['candidate']['sha256']}",
        f"Baseline: {report['baseline']['name']}",
        f"Rules evaluated: {report['rules']['evaluated']}",
        f"Findings: {report['summary']['finding_count']}",
    ]
    if not report["findings"]:
        lines.append("No protected-path drift was detected.")
        return "\n".join(lines)

    for number, finding in enumerate(report["findings"], start=1):
        observed = "<missing>" if finding["observed"] is None else " ".join(finding["observed"])
        lines.extend(
            [
                "",
                f"Finding {number}: {finding['rule_id']} [{finding['severity'].upper()}]",
                f"Name: {finding['name']}",
                f"Path: {finding['path']}",
                f"Expected: {' '.join(finding['expected'])}",
                f"Observed: {observed}",
                f"Rationale: {finding['rationale']}",
            ]
        )
    return "\n".join(lines)


def format_json_report(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, sort_keys=True)
