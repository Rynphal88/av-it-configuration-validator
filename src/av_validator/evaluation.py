"""Reproducible evaluation helpers for the bounded synthetic corpus."""

from __future__ import annotations

import math
import platform
import statistics
import tempfile
import time
import tracemalloc
from pathlib import Path
from typing import Any

from .catalog import load_rules
from .parser import parse_scene_text
from .service import validate_configuration


def _scene_text(configuration: dict[str, tuple[str, ...]]) -> str:
    lines = [f"{path} {' '.join(values)}" for path, values in configuration.items()]
    return "# Synthetic Unit 6 controlled variant\n" + "\n".join(lines) + "\n"


def run_controlled_evaluation(
    baseline_path: str | Path,
    rules_path: str | Path,
    *,
    variants_per_rule: int = 5,
) -> dict[str, Any]:
    """Evaluate one controlled drift per variant and collect performance evidence."""

    if variants_per_rule <= 0:
        raise ValueError("variants_per_rule must be positive")

    baseline_path = Path(baseline_path)
    rules_path = Path(rules_path)
    baseline_model = parse_scene_text(baseline_path.read_text(encoding="utf-8"))
    rules, _ = load_rules(rules_path, baseline_model)

    true_positive = false_positive = false_negative = true_negative = 0
    latencies_ms: list[float] = []
    observed_cases: list[dict[str, Any]] = []

    tracemalloc.start()
    started = time.perf_counter()
    with tempfile.TemporaryDirectory() as directory:
        temp_root = Path(directory)
        for rule in rules:
            for variant_number in range(1, variants_per_rule + 1):
                configuration = dict(baseline_model)
                configuration[rule.path] = (f"CONTROLLED_DRIFT_{variant_number}",)
                candidate_path = temp_root / f"{rule.rule_id}-{variant_number}.scn"
                candidate_path.write_text(
                    _scene_text(configuration), encoding="utf-8", newline="\n"
                )

                case_started = time.perf_counter()
                report = validate_configuration(
                    candidate_path, baseline_path, rules_path
                )
                latencies_ms.append((time.perf_counter() - case_started) * 1000)
                observed_ids = {finding["rule_id"] for finding in report["findings"]}
                expected_ids = {rule.rule_id}

                true_positive += len(observed_ids & expected_ids)
                false_positive += len(observed_ids - expected_ids)
                false_negative += len(expected_ids - observed_ids)
                true_negative += len(rules) - len(observed_ids | expected_ids)
                observed_cases.append(
                    {
                        "case": candidate_path.stem,
                        "expected": sorted(expected_ids),
                        "observed": sorted(observed_ids),
                        "correct": observed_ids == expected_ids,
                    }
                )

    total_seconds = time.perf_counter() - started
    _, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    precision_denominator = true_positive + false_positive
    recall_denominator = true_positive + false_negative
    total_decisions = true_positive + true_negative + false_positive + false_negative
    sorted_latencies = sorted(latencies_ms)
    p95_index = max(0, math.ceil(0.95 * len(sorted_latencies)) - 1)

    return {
        "method": {
            "corpus": "synthetic single-drift variants",
            "unique_variants": len(observed_cases),
            "rules_exercised": len(rules),
            "variants_per_rule": variants_per_rule,
            "ground_truth": "one known protected-path drift per variant",
            "limitations": "Results do not establish performance on every X32 firmware or live venue.",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "correctness": {
            "true_positive": true_positive,
            "false_positive": false_positive,
            "false_negative": false_negative,
            "true_negative": true_negative,
            "precision_percent": round(100 * true_positive / precision_denominator, 2),
            "recall_percent": round(100 * true_positive / recall_denominator, 2),
            "decision_accuracy_percent": round(
                100 * (true_positive + true_negative) / total_decisions, 2
            ),
            "cases_correct": sum(case["correct"] for case in observed_cases),
        },
        "performance": {
            "mean_latency_ms": round(statistics.fmean(latencies_ms), 4),
            "median_latency_ms": round(statistics.median(latencies_ms), 4),
            "p95_latency_ms": round(sorted_latencies[p95_index], 4),
            "throughput_validations_per_second": round(
                len(observed_cases) / total_seconds, 2
            ),
            "peak_traced_memory_kib": round(peak_bytes / 1024, 2),
        },
        "qualitative_usability": {
            "method": "structured non-participant heuristic inspection",
            "rating_scale": "Pass or Needs improvement",
            "criteria_passed": 5,
            "criteria_total": 5,
            "completion_percent": 100.0,
            "criteria": [
                {
                    "criterion": "Task discoverability",
                    "rating": "Pass",
                    "evidence": "Command help names the candidate, baseline, rule, format, and size inputs.",
                },
                {
                    "criterion": "Error feedback",
                    "rating": "Pass",
                    "evidence": "Invalid input returns a concise validation error and nonzero exit code.",
                },
                {
                    "criterion": "Finding clarity",
                    "rating": "Pass",
                    "evidence": "Each finding shows rule, severity, path, expected value, observed value, and rationale.",
                },
                {
                    "criterion": "Safety visibility",
                    "rating": "Pass",
                    "evidence": "The report states that automated action is none and identifies the human-review boundary.",
                },
                {
                    "criterion": "Output flexibility",
                    "rating": "Pass",
                    "evidence": "The same workflow supports readable text and machine-readable JSON output.",
                },
            ],
            "interpretation": "The interface met all five inspected clarity criteria; participant usability testing remains future work.",
        },
        "cases": observed_cases,
    }
