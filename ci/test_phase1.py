"""Gate profiles and attestation, on a temporary Git repository; no Docker or network."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import phase1
from phase1 import GATES, PROFILES, RELEASE_GATES, STEPS

ROOT = Path(__file__).resolve().parents[1]


class ProfileTests(unittest.TestCase):
    def test_full_profile_runs_every_gate_and_gitops(self):
        self.assertEqual(PROFILES["full"], (*GATES, "gitops"))
        self.assertEqual(len(GATES), 18)

    def test_release_profile_keeps_artifact_and_supply_chain_gates(self):
        self.assertEqual(PROFILES["release"][-1], "attest")
        for gate in ("secrets", "backend-security", "frontend-security", "backend-image-smoke",
                     "frontend-image-smoke", "backend-image-security", "frontend-image-security"):
            self.assertIn(gate, RELEASE_GATES)
        for gate in ("backend-unit", "backend-integration", "frontend-tests"):
            self.assertNotIn(gate, RELEASE_GATES)

    def test_migration_only_runs_functional_gates_in_original_order(self):
        deferred = {"secrets", "backend-security", "frontend-security",
                    "backend-image-security", "frontend-image-security", "attest"}
        self.assertEqual(PROFILES["migration"], tuple(s for s in STEPS if s not in deferred))
        self.assertEqual(len(PROFILES["migration"]), 13)
        self.assertNotIn("gitops", PROFILES["migration"])
        self.assertFalse(RELEASE_GATES <= set(PROFILES["migration"]))

    def test_profiles_only_use_known_steps(self):
        for steps in PROFILES.values():
            self.assertTrue(set(steps) <= {*STEPS, "gitops"})
            self.assertEqual(len(steps), len(set(steps)))

    def test_steps_command_prints_the_profile(self):
        output = subprocess.check_output(["python3", "-B", str(ROOT / "ci/phase1.py"), "steps", "--profile", "release"],
                                         text=True)
        self.assertEqual(tuple(output.split()), PROFILES["release"])


class AttestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "infra/jenkins-host").mkdir(parents=True)
        shutil.copy(ROOT / "infra/jenkins-host/images.lock.json", self.root / "infra/jenkins-host/")
        for args in (["init", "-q"], ["-c", "user.name=T", "-c", "user.email=t@example.invalid",
                                      "commit", "-q", "--allow-empty", "-m", "fixture"]):
            subprocess.run(["git", "-C", str(self.root), *args], check=True)
        self.ci = phase1.CI(self.root)
        reports = self.ci.reports
        for name in ("secrets-history.json", "secrets-tree.json"):
            (reports / name).write_text("[]")
        for component in ("backend", "frontend"):
            (reports / f"{component}-image-security.json").write_text(json.dumps({"Results": []}))
            (reports / f"{component}-ci.tar").write_bytes(component.encode())

    def attest_after(self, passed):
        self.ci.state["passed"] = list(passed)
        self.ci.step("attest")
        return json.loads((self.ci.reports / "gates.json").read_text())

    def test_release_run_attests_release_gates(self):
        manifest = self.attest_after(RELEASE_GATES)
        self.assertEqual(set(manifest["gates"]), RELEASE_GATES)
        self.assertEqual(manifest["sha"], self.ci.sha)

    def test_full_run_attests_all_18_gates(self):
        passing = '<testsuite><testcase name="ok"/></testsuite>'
        for name in phase1.TEST_REPORTS.values():
            (self.ci.reports / name).write_text(passing)
        manifest = self.attest_after([*GATES, "gitops"])
        self.assertEqual(manifest["gates"], sorted(GATES))

    def test_missing_release_gate_refuses_attestation(self):
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            self.attest_after(RELEASE_GATES - {"backend-image-security"})

    def test_passed_test_gate_needs_its_report(self):
        with self.assertRaises(FileNotFoundError):
            self.attest_after([*RELEASE_GATES, "backend-unit"])

    def test_failing_test_report_refuses_attestation(self):
        (self.ci.reports / "backend-unit.xml").write_text('<testsuite><testcase name="x"><failure/></testcase></testsuite>')
        with self.assertRaisesRegex(RuntimeError, "failing test results"):
            self.attest_after([*RELEASE_GATES, "backend-unit"])


if __name__ == "__main__":
    unittest.main()
