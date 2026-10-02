"""Command-line entry point for the Unit 4 initial prototype."""

from __future__ import annotations

import argparse
import sys

from .catalog import RuleCatalogError, load_rules
from .engine import evaluate_rules
from .integrity import InputIntegrityError, read_scene_file
from .parser import SceneParseError, parse_scene_text
from .reporting import build_report, format_json_report, format_text_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only validation of a sanitized X32 scene against an approved baseline."
    )
    parser.add_argument("--candidate", required=True, help="candidate .scn file")
    parser.add_argument("--baseline", required=True, help="approved baseline .scn file")
    parser.add_argument("--rules", required=True, help="declarative JSON rule catalog")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        candidate = read_scene_file(args.candidate)
        baseline = read_scene_file(args.baseline)
        candidate_model = parse_scene_text(candidate.text)
        baseline_model = parse_scene_text(baseline.text)
        rules, rules_sha256 = load_rules(args.rules, baseline_model)
        findings = evaluate_rules(candidate_model, rules)
        report = build_report(
            candidate,
            baseline,
            findings,
            rule_count=len(rules),
            rules_sha256=rules_sha256,
        )
    except (InputIntegrityError, SceneParseError, RuleCatalogError, OSError) as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 1

    formatter = format_json_report if args.format == "json" else format_text_report
    print(formatter(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
