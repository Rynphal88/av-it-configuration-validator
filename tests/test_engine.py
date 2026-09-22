import unittest

from av_validator.engine import evaluate_rules
from av_validator.models import Rule, Severity


class EngineTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
