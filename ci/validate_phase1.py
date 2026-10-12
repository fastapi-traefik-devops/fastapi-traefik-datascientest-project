#!/usr/bin/env python3
"""Validate Docker CI files only; never contact or mutate a Kubernetes cluster."""
import ast
import json
from pathlib import Path
import re
import subprocess
import yaml

ROOT = Path(__file__).resolve().parents[1]


def main():
    for folder in ("backend/app", "ci", "scripts"):
        for path in (ROOT / folder).rglob("*.py"):
            ast.parse(path.read_text(), filename=str(path))
    for path in (ROOT / "infra/jenkins-host").glob("*.yaml"):
        list(yaml.safe_load_all(path.read_text()))
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        workflow = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        assert workflow.get("jobs"), f"Workflow has no jobs: {path}"
    for name in ("generate-client.yml", "lint-backend.yml", "test-backend.yml", "playwright.yml", "test-docker-compose.yml"):
        workflow = yaml.load((ROOT / ".github/workflows" / name).read_text(), Loader=yaml.BaseLoader)
        assert workflow["permissions"]["contents"] == "read", name
    casc = yaml.safe_load((ROOT / "infra/jenkins-host/jenkins.yaml").read_text())
    assert casc["jenkins"]["numExecutors"] == 0
    assert not casc["jenkins"].get("clouds")
    assert all("inbound" in node["permanent"]["launcher"] for node in casc["jenkins"]["nodes"])
    for name in ("Jenkinsfile", "Jenkinsfile.promote"):
        text = (ROOT / name).read_text()
        assert not re.search(r"agent\s*\{\s*kubernetes\b", text), name
        assert not re.search(r"\b(kubectl|helm|argocd|terraform)\s", text), name
    for image in json.loads((ROOT / "infra/jenkins-host/images.lock.json").read_text()).values():
        assert re.search(r"@sha256:[0-9a-f]{64}$", image), image
    for line in (ROOT / "infra/jenkins-host/plugins.lock.txt").read_text().splitlines():
        assert not line.startswith("kubernetes:"), "Kubernetes agent plugin is retired"
    for path in [*list((ROOT / "ci").glob("*.sh")), *list((ROOT / "backend/scripts").glob("*.sh")), *list((ROOT / "scripts").glob("*.sh"))]:
        shell = "bash" if "bash" in path.read_text().splitlines()[0] else "sh"
        subprocess.run([shell, "-n", str(path)], check=True)
    local_compose = ROOT / ".tools/phase1/docker-compose"
    compose = [str(local_compose)] if local_compose.is_file() else ["docker", "compose"]
    subprocess.run([*compose, "-f", str(ROOT / "infra/jenkins-host/docker-compose.yml"), "config", "--quiet"], check=True)
    print("PASS: Python, shell, JCasC, pinned images/plugins and Docker Compose; Docker-only Jenkins")


if __name__ == "__main__":
    main()
