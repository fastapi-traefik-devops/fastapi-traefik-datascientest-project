FROM ghcr.io/astral-sh/uv:0.13.0@sha256:cdc6093146eb3ff6a40107b38f008b789e050e77ad87865e381d9917da55a168 AS uv
FROM python:3.14.8-alpine3.24@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72 AS builder
COPY --from=uv /uv /usr/local/bin/uv
RUN python -m pip uninstall -y pip && rm -rf /usr/local/lib/python3.13/ensurepip
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev --no-install-project
COPY app ./app
COPY scripts ./scripts
COPY alembic.ini ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev --no-install-project

# Test tools are confined to this explicitly selected stage.
FROM builder AS test
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH=/app PYTHONUNBUFFERED=1
RUN apk add --no-cache bash
CMD ["pytest"]

FROM python:3.14.8-alpine3.24@sha256:f6a589d43c42b9e7f7dc67a12d37132491f362859a5d750607710cc56da3bc72 AS runtime
RUN python -m pip uninstall -y pip && rm -rf /usr/local/lib/python3.13/ensurepip
RUN apk add --no-cache bash && addgroup -g 10001 app && adduser -D -H -u 10001 -G app app
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH" PYTHONPATH=/app PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
COPY --from=builder --chown=10001:10001 /app/.venv ./.venv
COPY --from=builder --chown=10001:10001 /app/app/*.py ./app/
COPY --from=builder --chown=10001:10001 /app/app/api ./app/api
COPY --from=builder --chown=10001:10001 /app/app/core ./app/core
COPY --from=builder --chown=10001:10001 /app/app/alembic ./app/alembic
COPY --from=builder --chown=10001:10001 /app/app/email-templates/build ./app/email-templates/build
COPY --from=builder --chown=10001:10001 /app/scripts ./scripts
COPY --from=builder --chown=10001:10001 /app/alembic.ini ./
USER 10001:10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/utils/health-check/', timeout=3)"]
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
