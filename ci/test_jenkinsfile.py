"""Static checks for profile selection, triggers and publication in the main Jenkinsfile."""
from pathlib import Path
import re
import unittest

PIPELINE = (Path(__file__).resolve().parents[1] / 'Jenkinsfile').read_text()


class JenkinsfileTests(unittest.TestCase):
    def test_pull_requests_and_nightly_run_full_and_main_runs_release(self):
        self.assertIn("env.CI_PROFILE = (env.CHANGE_ID || nightly || env.BRANCH_NAME != 'main') ? 'full' : 'release'", PIPELINE)
        self.assertIn('hudson.triggers.TimerTrigger$TimerTriggerCause', PIPELINE)
        self.assertIn('python3 ci/phase1.py steps --profile ${env.CI_PROFILE}', PIPELINE)
        self.assertNotIn('--profile migration', PIPELINE)

    def test_only_release_runs_on_main_publish(self):
        self.assertIn("env.PUBLISH = (env.BRANCH_NAME == 'main' && env.CI_PROFILE == 'release') ? 'true' : 'false'", PIPELINE)
        self.assertEqual(PIPELINE.count("when { expression { env.PUBLISH == 'true' } }"), 2)

    def test_main_polls_and_runs_nightly_other_branches_have_no_triggers(self):
        triggers = re.search(r'triggers \{(.*?)\n    \}', PIPELINE, re.S).group(1)
        self.assertIn("pollSCM(env.BRANCH_NAME == 'main' ? 'H/2 * * * *' : '')", triggers)
        self.assertIn("cron(env.BRANCH_NAME == 'main' ? 'H 2 * * *' : '')", triggers)

    def test_publication_hands_over_the_attested_archives(self):
        archived = re.search(r"stage\('Archive attested images'\).*?archiveArtifacts artifacts: '([^']+)'", PIPELINE, re.S).group(1)
        self.assertEqual(set(archived.split(',')), {'.ci-output/*-ci.tar', '.ci-output/gates.json', '.ci-output/source-sha.txt'})
        self.assertNotIn('export-images', PIPELINE)


if __name__ == '__main__':
    unittest.main()
