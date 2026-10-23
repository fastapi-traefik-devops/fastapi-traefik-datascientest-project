"""Static checks for the trusted publisher's STAGE acceptance wiring in Jenkinsfile.promote."""
from pathlib import Path
import re
import unittest

PIPELINE = (Path(__file__).resolve().parents[1] / 'Jenkinsfile.promote').read_text()


def block(text, opening):
    # Return the brace-balanced body that follows the first occurrence of `opening`.
    start = text.index('{', text.index(opening)) + 1
    depth = 1
    for position in range(start, len(text)):
        depth += {'{': 1, '}': -1}.get(text[position], 0)
        if depth == 0:
            return text[start:position]
    raise AssertionError(f'Unbalanced block after {opening}')


class PromotePipelineTests(unittest.TestCase):
    def test_observer_runs_only_for_promoted_stage_inside_the_lock(self):
        locked = block(PIPELINE, "lock(resource: 'liora-stage-promotion')")
        self.assertIn("node('stage-observer')", locked)
        self.assertIn("params.ACTION == 'stage' && readJSON(file: 'stage-request.json').status == 'promoted'", locked)

    def test_observer_never_receives_credentials(self):
        observer = block(PIPELINE, "node('stage-observer')")
        self.assertNotIn('withCredentials', observer)
        self.assertNotIn('publisher-action.sh', observer)
        self.assertIn('stage_acceptance.py', observer)

    def test_receipt_is_written_by_trusted_helper_then_failure_fails_the_build(self):
        locked = block(PIPELINE, "lock(resource: 'liora-stage-promotion')")
        record = locked.index('publisher-action.sh accept-stage')
        verdict = locked.index("status != 'accepted'")
        self.assertLess(locked.index("node('stage-observer')"), record)
        self.assertLess(record, verdict)
        self.assertRegex(locked[verdict:], r"error\('STAGE acceptance failed")

    def test_prod_and_dev_actions_stay_unavailable(self):
        choices = re.search(r"name: 'ACTION', choices: \[([^\]]*)\]", PIPELINE).group(1)
        self.assertEqual(choices, "'publish-only', 'stage'")

    def test_timeout_covers_the_observation_window(self):
        minutes = int(re.search(r'timeout\(time: (\d+), unit: .MINUTES.\)', PIPELINE).group(1))
        self.assertGreaterEqual(minutes, 15 + 30)

    def test_evidence_is_archived(self):
        self.assertIn('stage-acceptance.json', block(PIPELINE, 'post'))


if __name__ == '__main__':
    unittest.main()
