#!/usr/bin/env python3
"""Trusted Git writer. Never execute code from a selected application revision."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile

REPO = 'https://github.com/fastapi-traefik-devops/fastapi-traefik-datascientest-project.git'
REGISTRY = 'ghcr.io/fastapi-traefik-devops/fastapi-'


def run(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def git(*args, cwd=None):
    return run('git', *args, cwd=cwd)


def digest(image):
    return run('crane', 'digest', image)


def set_images(path, sha, digests):
    # Deliberately edit only image fields; preserve human-maintained overlay YAML.
    text = path.read_text()
    for name in ('backend', 'frontend'):
        pattern = rf'(  newName: {REGISTRY}{name}\n)  newTag: [^\n]+(?:\n  digest: [^\n]+)?'
        text, count = re.subn(pattern, rf'\g<1>  newTag: sha-{sha}\n  digest: {digests[name]}', text)
        if count != 1:
            raise RuntimeError(f'Expected exactly one {name} image entry in {path}')
    path.write_text(text)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('environment', choices=['dev', 'stage', 'prod'])
    p.add_argument('sha')
    p.add_argument('--release', default='')
    args = p.parse_args()
    if not re.fullmatch(r'[0-9a-f]{40}', args.sha):
        p.error('full SHA required')
    if args.environment == 'prod' and not re.fullmatch(r'v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', args.release):
        p.error('production requires vX.Y.Z')
    digests = {n: digest(f'{REGISTRY}{n}:sha-{args.sha}') for n in ('backend', 'frontend')}
    if not all(re.fullmatch(r'sha256:[0-9a-f]{64}', d) for d in digests.values()):
        raise RuntimeError('Unexpected registry digest')
    # A fixed trusted implementation is used; the target checkout is data only.
    with tempfile.TemporaryDirectory(prefix='gitops-') as directory:
        git('clone', '--quiet', '--no-checkout', REPO, directory)
        git('checkout', '--quiet', '-B', 'promotion', 'origin/main', cwd=directory)
        if args.environment != 'dev':
            git('merge-base', '--is-ancestor', args.sha, 'origin/main', cwd=directory)
        if args.environment == 'prod':
            git('fetch', '--quiet', 'origin', f'refs/tags/{args.release}:refs/tags/{args.release}', cwd=directory)
            if git('rev-parse', f'{args.release}^{{commit}}', cwd=directory) != args.sha:
                raise RuntimeError('Release tag moved or disagrees with selected SHA')
            # Evidence that this exact digest pair was recorded in stage Git history.
            # Human approval additionally verifies Argo health/smoke tests; Jenkins has no cluster access.
            found = False
            for commit in git('log', '--format=%H', 'origin/main', '--', 'deploy/overlays/stage/promotion.json', cwd=directory).splitlines():
                record = json.loads(git('show', f'{commit}:deploy/overlays/stage/promotion.json', cwd=directory))
                if record['sha'] == args.sha and record['digests'] == digests:
                    found = True
                    break
            if not found:
                raise RuntimeError('This digest pair has never been promoted to stage')
            for name, expected in digests.items():
                target = f'{REGISTRY}{name}:{args.release}'
                existing = subprocess.run(['crane', 'digest', target], text=True, capture_output=True)
                if existing.returncode == 0:
                    if existing.stdout.strip() != expected:
                        raise RuntimeError('Refusing to overwrite existing release tag')
                elif 'MANIFEST_UNKNOWN' in existing.stderr or 'NAME_UNKNOWN' in existing.stderr:
                    run('crane', 'tag', f'{REGISTRY}{name}@{expected}', args.release)
                else:
                    raise RuntimeError('Registry lookup failed; refusing to treat it as missing')
                if digest(target) != expected:
                    raise RuntimeError('Release digest mismatch')
        for attempt in range(5):
            git('fetch', '--quiet', 'origin', 'main', cwd=directory)
            git('reset', '--hard', 'origin/main', cwd=directory)
            overlay = Path(directory) / 'deploy' / 'overlays' / args.environment
            record_path = overlay / 'promotion.json'
            if args.environment == 'stage':
                # Reject delayed builds when newer application/CI changes have reached main.
                changed = git('diff', '--name-only', args.sha, 'origin/main', cwd=directory).splitlines()
                if any(not (f.startswith(('deploy/', 'argocd/')) or f.endswith('.md')) for f in changed):
                    print('Stage promotion superseded by newer source on main')
                    return
                if record_path.exists():
                    old = json.loads(record_path.read_text())['sha']
                    if old != args.sha:
                        git('merge-base', '--is-ancestor', old, args.sha, cwd=directory)
            set_images(overlay / 'kustomization.yaml', args.sha, digests)
            record_path.write_text(json.dumps({'sha': args.sha, 'digests': digests, 'release': args.release}, indent=2) + '\n')
            # Run the original trusted validator, never scripts from the data checkout.
            run('sh', str(Path(__file__).resolve().parent / 'validate.sh'), cwd=directory)
            git('add', f'deploy/overlays/{args.environment}', cwd=directory)
            if not git('diff', '--cached', '--name-only', cwd=directory):
                print('Desired state already matches')
                return
            if args.environment == 'prod':
                branch = f'release/{args.release}'
                ref = f'refs/remotes/origin/{branch}'
                exists = subprocess.run(['git', 'show-ref', '--verify', '--quiet', ref], cwd=directory)
                if exists.returncode == 0:
                    for filename in ('promotion.json', 'kustomization.yaml'):
                        existing = git('show', f'{ref}:deploy/overlays/prod/{filename}', cwd=directory)
                        if existing != (overlay / filename).read_text().strip():
                            raise RuntimeError('Existing release branch differs; review it manually, never overwrite')
                    print(f'Existing review branch: {branch}')
                    return
            git('-c', 'user.name=Jenkins GitOps', '-c', 'user.email=jenkins-gitops@users.noreply.github.com',
                'commit', '-m', f'gitops({args.environment}): promote {args.sha} {args.release}'.strip(), cwd=directory)
            if args.environment == 'prod':
                branch = f'release/{args.release}'
                # Never force-push or merge. A human opens/reviews the PR.
                git('push', 'origin', f'HEAD:refs/heads/{branch}', cwd=directory)
                print(f'Open reviewed PR: {REPO.removesuffix(".git")}/compare/main...{branch}')
                return
            result = subprocess.run(['git', 'push', 'origin', 'HEAD:refs/heads/main'], cwd=directory)
            if result.returncode == 0:
                return
        raise RuntimeError('Main advanced repeatedly; rerun promotion')


if __name__ == '__main__':
    main()
