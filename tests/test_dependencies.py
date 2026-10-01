"""Check that the package declares every third-party module it imports."""

import ast
import re
import sys
from importlib.metadata import packages_distributions
from pathlib import Path
from typing import Set

import pytest
from packaging.requirements import Requirement

tomllib = pytest.importorskip("tomllib")

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "jobs_crm_assistant"


def _normalize(name: str) -> str:
    """Normalize a distribution name as PEP 503 does."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _imported_top_level_modules() -> Set[str]:
    """Return the top-level module names imported anywhere under src/."""
    names: Set[str] = set()
    for path in (ROOT / "src").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names.add(node.module.split(".")[0])
    return names - set(sys.stdlib_module_names) - {PACKAGE}


def test_runtime_imports_are_declared_dependencies() -> None:
    """Every third-party import in src/ must come from a declared dependency."""
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    declared = {
        _normalize(Requirement(spec).name)
        for spec in pyproject["project"]["dependencies"]
    }
    providers = packages_distributions()

    not_installed = []
    not_declared = []
    for module in sorted(_imported_top_level_modules()):
        dists = {_normalize(d) for d in providers.get(module, [])}
        if not dists:
            not_installed.append(module)
        elif not dists & declared:
            not_declared.append(f"{module} (from {', '.join(sorted(dists))})")

    assert not not_installed, f"imported but not installed: {not_installed}"
    assert not not_declared, f"installed but not declared: {not_declared}"
