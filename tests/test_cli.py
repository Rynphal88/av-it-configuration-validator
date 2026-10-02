import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from av_validator.cli import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.baseline = self.root / "sample-configs/sanitized/approved-baseline.scn"
        self.rules = self.root / "rules/demo_rules.json"

    def test_drift_workflow_evaluates_eight_rules_and_requires_review(self):
        candidate = self.root / "sample-configs/sanitized/candidate-drift.scn"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                ["--candidate", str(candidate), "--baseline", str(self.baseline), "--rules", str(self.rules)]
            )
        report = output.getvalue()
        self.assertEqual(exit_code, 0)
        self.assertIn("Status: FINDINGS", report)
        self.assertIn("Rules evaluated: 8", report)
        self.assertIn("Findings: 4", report)
        self.assertIn("Finding 1: R-001 [CRITICAL]", report)
        self.assertIn("Automated action: NONE", report)

    def test_compliant_workflow_reports_no_protected_path_drift(self):
        candidate = self.root / "sample-configs/sanitized/candidate-compliant.scn"
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                ["--candidate", str(candidate), "--baseline", str(self.baseline), "--rules", str(self.rules)]
            )
        self.assertEqual(exit_code, 0)
        self.assertIn("Status: COMPLIANT", output.getvalue())
        self.assertIn("No protected-path drift was detected.", output.getvalue())

    def test_invalid_candidate_returns_nonzero_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "candidate.txt"
            candidate.write_text("/route/main ON\n", encoding="utf-8")
            errors = io.StringIO()
            with redirect_stderr(errors):
                exit_code = main(
                    ["--candidate", str(candidate), "--baseline", str(self.baseline), "--rules", str(self.rules)]
                )
        self.assertEqual(exit_code, 1)
        self.assertIn("Validation error", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
