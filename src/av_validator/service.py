"""Application service that composes the validation modules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .catalog import load_rules
from .engine import evaluate_rules
from .integrity import read_scene_file
from .parser import parse_scene_text
from .reporting import build_report


def validate_configuration(
    candidate_path: str | Path,
    baseline_path: str | Path,
    rules_path: str | Path,
    *,
    max_scene_bytes: int = 2_000_000,
) -> dict[str, Any]:
    """Run the complete read-only validation workflow and return its report."""

    candidate = read_scene_file(candidate_path, max_bytes=max_scene_bytes)
    baseline = read_scene_file(baseline_path, max_bytes=max_scene_bytes)
    candidate_model = parse_scene_text(candidate.text, max_chars=max_scene_bytes)
    baseline_model = parse_scene_text(baseline.text, max_chars=max_scene_bytes)
    rules, rules_sha256 = load_rules(rules_path, baseline_model)
    findings = evaluate_rules(candidate_model, rules)
    return build_report(
        candidate,
        baseline,
        findings,
        rule_count=len(rules),
        rules_sha256=rules_sha256,
    )
