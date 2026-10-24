# Real backend API results — 24 October 2026

[Collections and reproduction](README.md) · [Screenshots](evidence/INDEX.md)

## Result

Four Newman runs passed: **36 successful GET requests and 108 passing assertions**.
Two public-path runs failed before HTTP: **18 transport failures**, with 54 dependent
assertion failures caused by missing responses. These are not 54 distinct API bugs.
The independently recorded address probes and interactive UI requests are additional
requests, not included in those Newman counts.

| Environment | Route from this PC | Requests with HTTP response | Assertions | Result |
|---|---|---:|---:|---|
| DEV | Hostname mapped per-process to HAProxy 192.168.77.240 | 9/9 | 27/27 | PASS |
| STAGE | Hostname mapped per-process to HAProxy 192.168.77.240 | 9/9 | 27/27 | PASS |
| PROD | Hostname mapped per-process to HAProxy 192.168.77.240 | 9/9 | 27/27 | PASS |
| PROD | Normal public DNS, observed 151.115.96.5 | 9/9 | 27/27 | PASS |
| DEV | Normal public DNS | 0/9 | 0/27 | TLS handshake failed |
| STAGE | Normal public DNS | 0/9 | 0/27 | TLS handshake failed |

All successful runs used certificate verification. The private route preserved
original HTTPS hostnames, HTTP Host and TLS SNI. It did not use `-k`, `insecure`,
a changed hosts file or a bypassed browser security warning.

## What was verified

Each passing run checked:

| Request | Expected response | Interpretation |
|---|---|---|
| GET /api/v1/utils/health-check/ | 200, JSON true | Backend route responds; this handler itself does not query the DB |
| GET /api/v1/openapi.json | 200 with login/users/items paths | Public backend contract is available |
| GET /api/v1/users/ | 401, Not authenticated | Anonymous user listing rejected |
| GET /api/v1/users/me | 401, Not authenticated | Anonymous profile access rejected |
| GET /api/v1/users/{fixture UUID} | 401, Not authenticated | Anonymous user-by-ID access rejected |
| GET /api/v1/items/ | 401, Not authenticated | Anonymous item listing rejected |
| GET /api/v1/items/{fixture UUID} | 401, Not authenticated | Anonymous item-by-ID access rejected |
| GET /api/v1/users/me with invalid fixture bearer | 403, Could not validate credentials | Invalid token rejected |
| GET /api/v1/route-does-not-exist | 404, Not Found | Unknown route yields backend JSON 404 |

Every request also checked JSON content type. Expected 401/403/404 responses are
passing negative tests. They do not mean authenticated access is broken.

These tests do not establish valid-user login, authenticated CRUD, administrator
permissions, DB recovery, database write persistence, password reset or email
delivery. No valid credential was supplied for this exercise; example operations
are explicitly separate from executed evidence. The /private/users/ local-only
helper is absent from the deployed DEV contract and is not part of the 22 operations.

## Address and TLS findings

[Recorded probes](evidence/results/address-probes.json) identify DNS addresses,
actual connected IPs, curl exit/status, SSL result and timestamps.

- DEV and STAGE direct Traefik VIP **192.168.77.16**: verified HTTPS health 200.
- PROD direct Traefik VIP **192.168.77.17**: verified HTTPS health 200.
- All three through HAProxy **192.168.77.240**: verified HTTPS health 200.
- Public PROD **151.115.96.5**: verified HTTPS health 200.
- Public DEV/STAGE resolved to Cloudflare addresses at probe time. Both IPv4 and
  IPv6 returned TLS alert 40 / curl exit 35, before an HTTP response.
- The deliberate bare-IP HAProxy request also failed its TLS handshake. Host-based
  routing needs the application hostname; this is not evidence of a backend outage.

The evidence locates the DEV/STAGE failure on the public TLS path from this PC:
private ingress routes and the backend respond successfully. It does not establish
whether Cloudflare certificate configuration, DNS/edge routing, or another policy
is responsible. No Cloudflare setting was changed and no global Internet outage
is claimed.

## Tooling and evidence details

Postman Snap 8.12.7 was already present. Newman 6.2.2 and Swagger UI 5.34.0 were
installed locally using npm with lifecycle scripts disabled. Node was 20.5.1;
Python 3 and curl were existing tools. No desktop Postman workspace or login
was created. The importable collections use Postman format 2.1.

The first Newman private attempt hit a local DNS-adapter bug: Node requested an
array of addresses, while the adapter returned a single string. It received zero
HTTP responses. The adapter was corrected to honor `options.all`, then the DEV
collection passed. This failed harness attempt is retained in
[harness-first-attempt.json](evidence/results/harness-first-attempt.json), separately
from API failures. Node's IPv4/IPv6 callback handling did not require TLS relaxation.

Eight original JPEG screenshots were captured through the actual browser:
three health responses, protected profile and items rejections, the installed
client overview, an unexecuted schema payload example, and a viewer of saved real
Newman results. They are not Postman desktop screenshots. Swagger's separate
"Example Value" panels are schema illustrations; only its "Server response"
section records an executed request. No fake successful mutation screenshot exists.

Public logs omit request auth headers except the non-secret invalid-token fixture;
response headers are allowlisted. Public OpenAPI responses are deduplicated into openapi.dev.json and
openapi.stage-prod.json; run records identify the matching file and SHA-256.
No personal users/items, valid access tokens, passwords, server secrets or private
keys were collected or committed.

## OpenAPI variation found

DEV and STAGE/PROD expose the same 22 operations and identical path definitions,
but generated schema components differ. STAGE/PROD add password display formats,
anchor the optional grant_type pattern, and include additional validation-error
fields. See [the recorded comparison](evidence/results/openapi-schema-differences.json)
and [STAGE/PROD contract](openapi.stage-prod.json). This indicates a contract-generation
variation; this task did not inspect deployed package versions to establish its cause.
The full examples explicitly use the captured DEV schema.
