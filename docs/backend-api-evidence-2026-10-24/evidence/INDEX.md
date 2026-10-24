# API evidence index

[Test report](../TEST_REPORT.md) · [Collections/instructions](../README.md)

## Access policy

[Owner-confirmed Cloudflare policy and capture annotations](access-policy.json):
unprotected public DEV/STAGE clients are intentionally blocked. These captures
confirm the expected restriction for the tested client and are excluded from API
availability scoring. Developers use internal or approved Cloudflare-protected access.

## Genuine screenshots

- [01-api-client-overview.jpg](screenshots/01-api-client-overview.jpg) — Installed Swagger UI with the public DEV schema; no execution claim.
- [02-dev-health-live-200.jpg](screenshots/02-dev-health-live-200.jpg) — Actual DEV GET health response, 200 and JSON true.
- [03-stage-health-live-200.jpg](screenshots/03-stage-health-live-200.jpg) — Actual STAGE GET health response, 200 and JSON true.
- [04-prod-health-live-200.jpg](screenshots/04-prod-health-live-200.jpg) — Actual PROD GET health response, 200 and JSON true.
- [05-protected-profile-live-401.jpg](screenshots/05-protected-profile-live-401.jpg) — Actual PROD anonymous profile request rejected with 401.
- [06-protected-items-live-401.jpg](screenshots/06-protected-items-live-401.jpg) — Actual PROD anonymous item list rejected with 401.
- [07-item-payload-example-not-executed.jpg](screenshots/07-item-payload-example-not-executed.jpg) — Schema-derived create-item payload example. POST was not submitted.
- [08-newman-actual-results-matrix.jpg](screenshots/08-newman-actual-results-matrix.jpg) — Historical matrix before Cloudflare policy clarification; its TLS FAILED labels are superseded by the current EXPECTED BLOCK interpretation. Original image preserved.

- [09-newman-expected-cloudflare-block.jpg](screenshots/09-newman-expected-cloudflare-block.jpg) — Current security interpretation: expected public DEV/STAGE restriction, excluded from availability scoring.

## Raw execution records

- [address-probes.json](results/address-probes.json)
- [dev-private.json](results/dev-private.json)
- [dev-private.log](results/dev-private.log)
- [dev-public.json](results/dev-public.json)
- [dev-public.log](results/dev-public.log)
- [harness-first-attempt.json](results/harness-first-attempt.json)
- [prod-private.json](results/prod-private.json)
- [prod-private.log](results/prod-private.log)
- [prod-public.json](results/prod-public.json)
- [prod-public.log](results/prod-public.log)
- [stage-private.json](results/stage-private.json)
- [stage-private.log](results/stage-private.log)
- [stage-public.json](results/stage-public.json)
- [stage-public.log](results/stage-public.log)

- [openapi-schema-differences.json](results/openapi-schema-differences.json)

[Source/tool/screenshot provenance](provenance.json) · [Offline validation](validation.json)
