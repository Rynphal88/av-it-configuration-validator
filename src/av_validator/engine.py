"""Explainable rule evaluation for normalized configuration data."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from .models import Finding, Rule


def evaluate_rules(
    configuration: Mapping[str, tuple[str, ...]], rules: Iterable[Rule]
) -> list[Finding]:
    """Return evidence-bearing findings without changing the input mapping."""

    findings: list[Finding] = []
    for rule in rules:
        observed = configuration.get(rule.path)
        if observed != rule.expected:
            findings.append(
                Finding(
                    rule_id=rule.rule_id,
                    name=rule.name,
                    path=rule.path,
                    expected=rule.expected,
                    observed=observed,
                    severity=rule.severity,
                    rationale=rule.rationale,
                )
            )
    return findings
