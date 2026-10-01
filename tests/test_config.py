"""Tests for loading application settings from the environment."""

from pathlib import Path

import pytest

from jobs_crm_assistant.core.config import Settings

ENV_NAMES = ("OPENAI_API_KEY", "OPENAI_MODEL", "DATABASE_URL", "API_PREFIX", "DEBUG")


@pytest.fixture(autouse=True)
def isolated_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Run each test with no settings in the environment and no .env file."""
    for name in ENV_NAMES:
        monkeypatch.delenv(name, raising=False)
        monkeypatch.delenv(name.lower(), raising=False)
    monkeypatch.chdir(tmp_path)


def test_reads_upper_case_environment_variables(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The usual upper-case variable names must reach the settings."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4o")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test.db")
    monkeypatch.setenv("API_PREFIX", "/api/v2")
    monkeypatch.setenv("DEBUG", "true")

    settings = Settings()

    assert settings.openai_api_key == "sk-test"
    assert settings.openai_model == "gpt-4o"
    assert settings.database_url == "sqlite:///test.db"
    assert settings.api_prefix == "/api/v2"
    assert settings.debug is True


def test_reads_upper_case_names_from_dotenv_file(tmp_path: Path) -> None:
    """An .env file with the usual upper-case names must reach the settings."""
    (tmp_path / ".env").write_text("OPENAI_API_KEY=sk-from-file\n", encoding="utf-8")

    assert Settings().openai_api_key == "sk-from-file"


def test_lower_case_names_still_work(monkeypatch: pytest.MonkeyPatch) -> None:
    """Lower-case names, which worked before, must keep working."""
    monkeypatch.setenv("openai_api_key", "sk-lower")

    assert Settings().openai_api_key == "sk-lower"
