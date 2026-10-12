"""Generate the FastAPI schema with disposable settings and no external service."""
from __future__ import annotations

import json
import os
import secrets

os.environ["ENVIRONMENT"] = "local"
os.environ.setdefault("PROJECT_NAME", "OpenAPI generation")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_USER", "postgres")
os.environ.setdefault("POSTGRES_PASSWORD", secrets.token_urlsafe(24))
os.environ.setdefault("FIRST_SUPERUSER", "schema@example.com")
os.environ.setdefault("FIRST_SUPERUSER_PASSWORD", secrets.token_urlsafe(24))
os.environ.setdefault("SECRET_KEY", secrets.token_urlsafe(32))

from app.main import app  # noqa: E402

print(json.dumps(app.openapi(), sort_keys=True))
