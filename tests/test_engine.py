import unittest

from av_validator.engine import evaluate_rules
from av_validator.models import Rule, Severity


class EngineTests(unittest.TestCase):
    @staticmethod
    def make_rule(rule_id, path, expected, severity):
        return Rule(
            rule_id=rule_id,
            name=f"Rule {rule_id}",
            path=path,
            expected=expected,
            severity=severity,
            rationale="Protected configuration requirement.",
        )

    def test_rule_evaluation_returns_expected_and_observed_evidence(self):
        configuration = {"/route/broadcast": ("OFF",)}
        rule = Rule(
            rule_id="R-006",
            name="Broadcast path enabled",
            path="/route/broadcast",
            expected=("ON",),
            severity=Severity.MAJOR,
            rationale="The approved broadcast service requires this route.",
        )
        findings = evaluate_rules(configuration, [rule])
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].expected, ("ON",))
        self.assertEqual(findings[0].observed, ("OFF",))
        self.assertIs(findings[0].severity, Severity.MAJOR)

    def test_compliant_rule_produces_no_finding(self):
        configuration = {"/route/main": ("ON",)}
        rule = Rule(
            rule_id="R-001",
            name="Main path enabled",
            path="/route/main",
            expected=("ON",),
            severity=Severity.CRITICAL,
            rationale="The protected main service requires this route.",
        )
        self.assertEqual(evaluate_rules(configuration, [rule]), [])

    def test_missing_path_is_reported_without_mutating_configuration(self):
        configuration = {}
        rule = Rule(
            rule_id="R-005",
            name="Critical input present",
            path="/input/critical",
            expected=("LOCAL",),
            severity=Severity.CRITICAL,
            rationale="The approved service requires this source.",
        )
        findings = evaluate_rules(configuration, [rule])
        self.assertEqual(len(findings), 1)
        self.assertIsNone(findings[0].observed)
        self.assertEqual(configuration, {})

    def test_findings_are_prioritized_without_changing_rule_defined_severity(self):
        rules = [
            self.make_rule("R-003", "/minor", ("ON",), Severity.MINOR),
            self.make_rule("R-002", "/major", ("ON",), Severity.MAJOR),
            self.make_rule("R-001", "/critical", ("ON",), Severity.CRITICAL),
            self.make_rule("R-004", "/info", ("ON",), Severity.INFORMATIONAL),
        ]
        findings = evaluate_rules(
            {
                "/minor": ("OFF",),
                "/major": ("OFF",),
                "/critical": ("OFF",),
                "/info": ("OFF",),
            },
            rules,
        )
        self.assertEqual(
            [finding.severity for finding in findings],
            [Severity.CRITICAL, Severity.MAJOR, Severity.MINOR, Severity.INFORMATIONAL],
        )

    def test_rule_id_breaks_equal_severity_ties_deterministically(self):
        rules = [
            self.make_rule("R-008", "/second", ("ON",), Severity.CRITICAL),
            self.make_rule("R-001", "/first", ("ON",), Severity.CRITICAL),
        ]
        findings = evaluate_rules({"/first": ("OFF",), "/second": ("OFF",)}, rules)
        self.assertEqual([finding.rule_id for finding in findings], ["R-001", "R-008"])


if __name__ == "__main__":
    unittest.main()
