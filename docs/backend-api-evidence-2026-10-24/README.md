# FastAPI backend collection and real API evidence

24 October 2026 · Tests originated on the local Linux PC, not on the server.
All executed API requests were GET requests. Application data and server configuration
were unchanged; no login credentials were used, no users/items were created or deleted,
no password reset or email was requested.

Start with [test results and findings](TEST_REPORT.md), the
[screenshot index](evidence/INDEX.md), and the [endpoint guide](ENDPOINT_GUIDE.md).

## Collections

- [Read-only Postman collection](collections/liora-readonly.postman_collection.json):
  9 requests with 27 assertions per environment/route. Suitable for a live run.
- [All backend examples](collections/liora-backend-examples.postman_collection.json):
  all 22 operations from the [captured DEV OpenAPI contract](openapi.dev.json),
  with request bodies and illustrative response examples. Its default host is
  `https://example.invalid`; these examples were **not** executed against live data.
- Credential-free environments: [DEV](environments/dev.postman_environment.json),
  [STAGE](environments/stage.postman_environment.json),
  [PROD](environments/prod.postman_environment.json).

In Postman, select **Import**, choose the collection JSON and an environment JSON,
then choose that environment. Run the read-only collection. Keep any future valid
token/password in local-only values and out of exported files. The all-backend
examples use a separate `example_base_url` variable so selecting a live read-only
environment does not accidentally enable account/data/email operations.

Postman desktop was already installed (Snap 8.12.7, revision 201). No second desktop
installation or Postman account was needed. Newman 6.2.2, the Postman collection
runner, and Swagger UI 5.34.0 were installed locally in the workspace's `.api-tools/`
directory. The desktop app was not used for screenshots. Screenshots show actual
Swagger UI interactions and a clearly labeled viewer of real Newman output.
Neither `node_modules/` nor tool caches are committed.

## Reproduce a read-only run

From the application repository root, install the same pinned tools into a local
directory (no global npm installation required):

```sh
npm install --prefix ../.api-tools --ignore-scripts --no-audit --no-fund \
  newman@6.2.2 swagger-ui-dist@5.34.0
export LIORA_API_TOOLS="$(cd ../.api-tools && pwd)"

node docs/backend-api-evidence-2026-10-24/scripts/run-newman.cjs \
  dev private /tmp/liora-api-new-dev-run
```

Use `stage` or `prod` for the other environments. `public` uses normal DNS;
`private` maps only the selected hostname to `192.168.77.240` inside this process.
Every output directory must be new and outside this evidence tree. The runner
returns nonzero when transport or assertion checks fail. It only loads the fixed
GET collection, not the write/example collection. It follows no redirects and
keeps TLS verification enabled.

The public PROD route also works with the standard Newman CLI:

```sh
../.api-tools/node_modules/.bin/newman run \
  docs/backend-api-evidence-2026-10-24/collections/liora-readonly.postman_collection.json \
  -e docs/backend-api-evidence-2026-10-24/environments/prod.postman_environment.json
```

Normal Postman imports do not include the custom private DNS mapping. On this PC,
public DEV/STAGE fail TLS. Use the supplied private runner/explorer to reproduce
the recorded private tests. Do not disable SSL verification or replace the URL's
hostname with an IP. `curl --resolve` provides an equivalent one-request check:

```sh
curl --resolve dev.liora.aprt.info:443:192.168.77.240 \
  https://dev.liora.aprt.info/api/v1/utils/health-check/
```

## Local graphical API client

```sh
node docs/backend-api-evidence-2026-10-24/scripts/serve-explorer.cjs
```

Open `http://127.0.0.1:18765/`. Select DEV/STAGE/PROD, expand the health request,
click **Try it out**, then **Execute**. The constrained proxy connects from this
PC to the named environment over verified HTTPS. The local HTTP hop is loopback.
It changes no system DNS/hosts/browser certificate settings. It forwards only
allowlisted GET paths and the deliberate invalid-token fixture; it does not
forward real login credentials/tokens. Other operation schemas remain visible,
but write methods cannot be submitted in this client.

`/results` displays saved Newman results. It does not claim that viewing results
reruns a collection. Stop the client with Ctrl+C when finished.

## Evidence integrity

```sh
python3 docs/backend-api-evidence-2026-10-24/scripts/validate-evidence.py
sha256sum -c docs/backend-api-evidence-2026-10-24/SHA256SUMS
```

The [provenance record](evidence/provenance.json) identifies source revision,
installed tools, timestamps and screenshot hashes. All additions are confined to
this new docs directory. Existing docs and application code are preserved.

References: [official Newman installation/run documentation](https://learning.postman.com/docs/collections/using-newman-cli/installing-running-newman),
[Postman collection schemas](https://schema.postman.com/),
[Swagger UI distribution](https://github.com/swagger-api/swagger-ui).
