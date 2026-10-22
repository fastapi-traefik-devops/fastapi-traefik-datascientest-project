#!/usr/bin/env python3
"""Explicit functional-only publication contract; never masquerades as scanned release."""
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from phase1 import PROFILES, STEPS, TEST_REPORTS, file_sha

DEFERRED = [step for step in (*STEPS, "gitops") if step not in PROFILES["migration"]]
SOURCE_JOBS = {"migration-ci", "app-ci/main"}


def reports(directory):
    result = {}
    for filename in TEST_REPORTS.values():
        root = ET.parse(directory / filename).getroot()
        suites = list(root.iter("testsuite"))
        tests = sum(int(s.get("tests", "0")) for s in suites)
        if not tests or any(int(s.get(k, "0")) for s in suites for k in ("failures", "errors")):
            raise ValueError("Missing or unsuccessful functional test evidence")
        if list(root.iter("failure")) or list(root.iter("error")):
            raise ValueError("Failed functional tests")
        result[filename] = file_sha(directory / filename)
    return result


def write_candidate(directory, sha, gates, job, build):
    directory = Path(directory)
    if job not in SOURCE_JOBS or not re.fullmatch(r"[1-9][0-9]*", str(build)):
        raise ValueError("Unapproved CI source")
    if not re.fullmatch(r"[0-9a-f]{40}", sha) or not set(PROFILES["migration"]) <= set(gates):
        raise ValueError("Incomplete functional gates or source revision")
    manifest = {"version": 1, "kind": "functional-image-candidate", "sha": sha,
                "source": {"job": job, "build": str(build)},
                "gates": list(PROFILES["migration"]), "deferred": DEFERRED,
                "security_scanned": False, "reports": reports(directory),
                "archives": {n: file_sha(directory / f"{n}-ci.tar") for n in ("backend", "frontend")}}
    (directory / "candidate.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (directory / "source-sha.txt").write_text(sha + "\n")
    return manifest


def validate_candidate(directory, sha, job, build):
    directory = Path(directory)
    m = json.loads((directory / "candidate.json").read_text())
    if (m.get("version") != 1 or m.get("kind") != "functional-image-candidate"
            or m.get("sha") != sha or not re.fullmatch(r"[0-9a-f]{40}", sha)
            or job not in SOURCE_JOBS or not re.fullmatch(r"[1-9][0-9]*", str(build))
            or m.get("source") != {"job": job, "build": str(build)}
            or m.get("gates") != list(PROFILES["migration"])
            or m.get("deferred") != DEFERRED or m.get("security_scanned") is not False
            or (directory / "source-sha.txt").read_text().strip() != sha):
        raise ValueError("Invalid functional-only publication contract")
    if m.get("reports") != reports(directory):
        raise ValueError("Test report integrity failure")
    for n in ("backend", "frontend"):
        if m.get("archives", {}).get(n) != file_sha(directory / f"{n}-ci.tar"):
            raise ValueError("Image archive integrity failure")
    return m
