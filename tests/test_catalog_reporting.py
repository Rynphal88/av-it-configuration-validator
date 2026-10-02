import json
import tempfile
import unittest
from pathlib import Path

from av_validator.catalog import RuleCatalogError, load_rules
from av_validator.engine import evaluate_rules
from av_validator.integrity import SceneArtifact
from av_validator.reporting import build_report, format_json_report, format_text_report


class CatalogAndReportingTests(unittest.TestCase):
    @staticmethod
    def rule_entry(**overrides):
        entry = {
            "id": "R-001",
            "name": "Main output",
            "path": "/route/main",
            "severity": "critical",
            "rationale": "Protected route",
        }
        entry.update(overrides)
        return entry

    def write_catalog(self, directory, payload):
        path = Path(directory) / "rules.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_catalog_binds_expected_value_from_baseline(self):
        payload = {
            "rules": [
                {
                    "id": "R-001",
                    "name": "Main output",
                    "path": "/route/main",
                    "severity": "critical",
                    "rationale": "Protected route",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rules.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            rules, digest = load_rules(path, {"/route/main": ("ON",)})
        self.assertEqual(rules[0].expected, ("ON",))
        self.assertEqual(len(digest), 64)

    def test_catalog_rejects_path_missing_from_baseline(self):
        payload = {
            "rules": [
                {
                    "id": "R-001",
                    "name": "Main output",
                    "path": "/route/main",
                    "severity": "critical",
                    "rationale": "Protected route",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rules.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(RuleCatalogError, "baseline does not define"):
                load_rules(path, {})

    def test_catalog_rejects_invalid_json_and_empty_rule_list(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rules.json"
            path.write_text("{broken", encoding="utf-8")
            with self.assertRaisesRegex(RuleCatalogError, "valid UTF-8 JSON"):
                load_rules(path, {})
            path = self.write_catalog(directory, {"rules": []})
            with self.assertRaisesRegex(RuleCatalogError, "non-empty rules list"):
                load_rules(path, {})

    def test_catalog_rejects_non_object_and_missing_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_catalog(directory, {"rules": ["not-an-object"]})
            with self.assertRaisesRegex(RuleCatalogError, "must be an object"):
                load_rules(path, {})
            path = self.write_catalog(directory, {"rules": [{"id": "R-001"}]})
            with self.assertRaisesRegex(RuleCatalogError, "missing or invalid fields"):
                load_rules(path, {})

    def test_catalog_rejects_duplicate_id_and_unsupported_severity(self):
        baseline = {"/route/main": ("ON",)}
        with tempfile.TemporaryDirectory() as directory:
            entry = self.rule_entry()
            path = self.write_catalog(directory, {"rules": [entry, entry]})
            with self.assertRaisesRegex(RuleCatalogError, "duplicate rule id"):
                load_rules(path, baseline)
            path = self.write_catalog(
                directory,
                {"rules": [self.rule_entry(severity="emergency")]},
            )
            with self.assertRaisesRegex(RuleCatalogError, "unsupported severity"):
                load_rules(path, baseline)

    def test_report_contains_explainable_evidence(self):
        candidate = SceneArtifact(Path("candidate.scn"), "", 0, "a" * 64)
        baseline = SceneArtifact(Path("baseline.scn"), "", 0, "b" * 64)
        payload = {
            "rules": [
                {
                    "id": "R-001",
                    "name": "Main output",
                    "path": "/route/main",
                    "severity": "critical",
                    "rationale": "Protected route",
                }
            ]
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "rules.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            rules, digest = load_rules(path, {"/route/main": ("ON",)})
        findings = evaluate_rules({"/route/main": ("OFF",)}, rules)
        report = build_report(candidate, baseline, findings, rule_count=1, rules_sha256=digest)
        text = format_text_report(report)
        self.assertIn("Expected: ON", text)
        self.assertIn("Observed: OFF", text)
        self.assertIn("[CRITICAL]", text)
        self.assertIn("Automated action: NONE", text)
        self.assertIn("Hold deployment pending authorized human review.", text)
        self.assertTrue(report["review"]["required"])

    def test_compliant_report_preserves_normal_human_review_boundary(self):
        candidate = SceneArtifact(Path("candidate.scn"), "", 0, "a" * 64)
        baseline = SceneArtifact(Path("baseline.scn"), "", 0, "b" * 64)
        report = build_report(candidate, baseline, [], rule_count=8, rules_sha256="c" * 64)
        self.assertEqual(report["status"], "compliant")
        self.assertFalse(report["review"]["required"])
        self.assertEqual(report["review"]["automated_action"], "none")
        self.assertIn("normal pre-deployment review", report["review"]["recommendation"])
        self.assertEqual(json.loads(format_json_report(report))["rules"]["evaluated"], 8)

    def test_noncritical_finding_requires_review_without_critical_hold(self):
        candidate = SceneArtifact(Path("candidate.scn"), "", 0, "a" * 64)
        baseline = SceneArtifact(Path("baseline.scn"), "", 0, "b" * 64)
        rule = self.rule_entry(severity="major")
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_catalog(directory, {"rules": [rule]})
            rules, digest = load_rules(path, {"/route/main": ("ON",)})
        findings = evaluate_rules({"/route/main": ("OFF",)}, rules)
        report = build_report(candidate, baseline, findings, rule_count=1, rules_sha256=digest)
        self.assertEqual(report["review"]["recommendation"], "Review findings before deployment.")


if __name__ == "__main__":
    unittest.main()
