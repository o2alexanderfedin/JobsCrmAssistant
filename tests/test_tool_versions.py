"""Check that tools in the dev extra match the pre-commit hooks."""

import re
from pathlib import Path
from typing import Dict

import pytest

tomllib = pytest.importorskip("tomllib")

ROOT = Path(__file__).resolve().parent.parent

# Two versions of a formatter rewrite files back and forth, and two
# versions of mypy disagree about the same code.
HOOK_REPOS = {
    "black": "https://github.com/psf/black",
    "isort": "https://github.com/pycqa/isort",
    "mypy": "https://github.com/pre-commit/mirrors-mypy",
}


def _hook_revisions() -> Dict[str, str]:
    """Return the rev of each tool's repo in .pre-commit-config.yaml."""
    text = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    revisions = {}
    for tool, repo in HOOK_REPOS.items():
        match = re.search(rf"-\s+repo:\s*{re.escape(repo)}\s*\n\s+rev:\s*v?(\S+)", text)
        assert match, f"no pre-commit hook for {tool}"
        revisions[tool] = match.group(1)
    return revisions


def _dev_pins() -> Dict[str, str]:
    """Return the exact version pinned for each tool in the dev extra."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    dev = tomllib.loads(text)["project"]["optional-dependencies"]["dev"]
    pins = {}
    for spec in dev:
        match = re.fullmatch(r"([A-Za-z0-9_.-]+)\s*==\s*(\S+)", spec)
        if match:
            pins[match.group(1).lower()] = match.group(2)
    return pins


@pytest.mark.parametrize("tool", sorted(HOOK_REPOS))
def test_dev_extra_pins_tool_to_hook_version(tool: str) -> None:
    """The dev extra must install the same tool version as pre-commit."""
    revisions = _hook_revisions()
    pins = _dev_pins()

    assert tool in pins, f"{tool} is not pinned with == in the dev extra"
    assert pins[tool] == revisions[tool]
