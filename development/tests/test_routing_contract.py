import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEXT = " ".join((ROOT / "scoville-plan" / "SKILL.md").read_text(encoding="utf-8").split())


class RoutingContractTest(unittest.TestCase):
    def test_steps_expose_medium_complexity_instead_of_hiding_it(self):
        for marker in (
            "Treat every unknown low-eligibility fact as at least a `medium` boundary",
            "Write each future Step from the mechanism the worker must perform",
            "Name required search or inventory",
            "rather than only “add reciprocal comments.”",
            "Plan still does not assign the route",
        ):
            self.assertIn(marker, TEXT)


if __name__ == "__main__":
    unittest.main()
