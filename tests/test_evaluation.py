import unittest
from pathlib import Path

from av_validator.evaluation import run_controlled_evaluation


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]

    def test_controlled_evaluation_exercises_forty_variants(self):
        result = run_controlled_evaluation(
            self.root / "sample-configs/sanitized/approved-baseline.scn",
            self.root / "rules/demo_rules.json",
        )
        self.assertEqual(result["method"]["unique_variants"], 40)
        self.assertEqual(result["method"]["rules_exercised"], 8)
        self.assertEqual(result["correctness"]["cases_correct"], 40)
        self.assertEqual(result["correctness"]["false_positive"], 0)
        self.assertEqual(result["correctness"]["false_negative"], 0)
        self.assertGreater(
            result["performance"]["throughput_validations_per_second"], 0
        )
        self.assertEqual(result["qualitative_usability"]["criteria_passed"], 5)
        self.assertEqual(result["qualitative_usability"]["criteria_total"], 5)

    def test_controlled_evaluation_rejects_nonpositive_variant_count(self):
        with self.assertRaisesRegex(ValueError, "positive"):
            run_controlled_evaluation(
                self.root / "sample-configs/sanitized/approved-baseline.scn",
                self.root / "rules/demo_rules.json",
                variants_per_rule=0,
            )


if __name__ == "__main__":
    unittest.main()
