"""Tests for the cross-origin (CORS) policy of the API."""

from pathlib import Path
from typing import List

import pytest
from fastapi.testclient import TestClient

from jobs_crm_assistant.api.app import create_app
from jobs_crm_assistant.core.config import CorsSettings

ALLOW_ORIGIN = "access-control-allow-origin"
ALLOW_CREDENTIALS = "access-control-allow-credentials"


def _get_health(origins: List[str], origin: str) -> dict:
    """Request /health from a given origin, with a cookie, and return headers."""
    client = TestClient(create_app(origins))
    client.cookies.set("session", "secret")
    response = client.get("/health", headers={"Origin": origin})
    assert response.status_code == 200
    return dict(response.headers)


def test_default_settings_allow_no_origin(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """With no configuration, no other website may read API responses."""
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    monkeypatch.chdir(tmp_path)

    origins = CorsSettings().cors_origins
    headers = _get_health(origins, "https://evil.example")

    assert origins == []
    assert ALLOW_ORIGIN not in headers


def test_cors_origins_read_from_environment(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """CORS_ORIGINS holds a JSON list of allowed origins."""
    monkeypatch.setenv("CORS_ORIGINS", '["http://localhost:3000"]')
    monkeypatch.chdir(tmp_path)

    assert CorsSettings().cors_origins == ["http://localhost:3000"]


def test_listed_origin_gets_credentials_and_others_get_nothing() -> None:
    """A listed origin may send credentials; an unlisted one gets no access."""
    allowed = _get_health(["https://app.example"], "https://app.example")
    other = _get_health(["https://app.example"], "https://evil.example")

    assert allowed[ALLOW_ORIGIN] == "https://app.example"
    assert allowed[ALLOW_CREDENTIALS] == "true"
    assert ALLOW_ORIGIN not in other


def test_wildcard_origin_never_allows_credentials() -> None:
    """With "*", a cookie-carrying request must not get its origin reflected."""
    headers = _get_health(["*"], "https://evil.example")

    assert headers[ALLOW_ORIGIN] == "*"
    assert ALLOW_CREDENTIALS not in headers


def test_cors_settings_load_beside_other_settings_in_dotenv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The app must start when .env also holds the OpenAI and database settings."""
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "OPENAI_API_KEY=sk-test\n"
        "DATABASE_URL=sqlite:///test.db\n"
        'CORS_ORIGINS=["http://localhost:3000"]\n',
        encoding="utf-8",
    )

    assert CorsSettings().cors_origins == ["http://localhost:3000"]
