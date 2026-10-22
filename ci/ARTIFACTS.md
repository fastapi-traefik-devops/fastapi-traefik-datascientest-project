# Functional-only candidate archives

The 13 migration functional gates remain unchanged. After they all pass,
`phase1.py export-images` saves the two runtime images that passed their smoke
tests. `Jenkinsfile.migration` exposes this only through `EXPORT_IMAGES=true`
(default false); exporting never publishes or deploys.

`candidate.json` binds the application SHA and Jenkins job/build to successful
functional gates, all seven deferred steps, `security_scanned:false`, archive
SHA256 and hashes of nonempty successful native JUnit reports. The trusted writer
must explicitly select `registry.py --mode functional --source-job JOB
--source-build NUMBER`. It checks the candidate against the independently verified
SUCCESS Jenkins run. Default release validation still requires real scan-backed
attestation; there is no implicit fallback. Remote SHA tags remain write-once.
Old CI builds without this contract and archives cannot qualify retroactively.

Run `python3 -B -m unittest discover -s ci -p 'test_*.py'` locally. Tests use
fixture archives/reports and mocked registry commands; they do not run scans,
image builds, publication or deployment. Live artifact export/publication still
requires separate operator approval.
