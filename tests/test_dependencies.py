"""Check that the package declares every third-party module it imports."""

import ast
import re
import sys
from importlib.metadata import packages_distributions
from pathlib import Path
from typing import Any, Dict, List, Set

import pytest
from packaging.requirements import Requirement

tomllib = pytest.importorskip("tomllib")

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = "jobs_crm_assistant"

# Modules that work only when an extra distribution is installed, which a
# scan of top-level imports cannot see.
EXTRA_REQUIREMENTS = {
    "fastapi.testclient": "httpx",
}


def _normalize(name: str) -> str:
    """Normalize a distribution name as PEP 503 does."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _imported_modules(directory: str) -> Set[str]:
    """Return the full module names imported anywhere under a directory."""
    names: Set[str] = set()
    for path in (ROOT / directory).rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names.add(node.module)
    return names


def _pyproject() -> Dict[str, Any]:
    """Return the parsed pyproject.toml."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    data: Dict[str, Any] = tomllib.loads(text)
    return data


def _names(specs: List[str]) -> Set[str]:
    """Return the normalized distribution names of requirement strings."""
    return {_normalize(Requirement(spec).name) for spec in specs}


def _assert_declared(modules: Set[str], declared: Set[str]) -> None:
    """Fail unless every third-party module comes from a declared distribution."""
    top_level = {name.split(".")[0] for name in modules}
    third_party = top_level - set(sys.stdlib_module_names) - {PACKAGE}
    providers = packages_distributions()

    not_installed = []
    not_declared = []
    for module in sorted(third_party):
        dists = {_normalize(d) for d in providers.get(module, [])}
        if not dists:
            not_installed.append(module)
        elif not dists & declared:
            not_declared.append(f"{module} (from {', '.join(sorted(dists))})")
    for module in sorted(modules & EXTRA_REQUIREMENTS.keys()):
        if _normalize(EXTRA_REQUIREMENTS[module]) not in declared:
            not_declared.append(f"{module} (needs {EXTRA_REQUIREMENTS[module]})")

    assert not not_installed, f"imported but not installed: {not_installed}"
    assert not not_declared, f"installed but not declared: {not_declared}"


def test_runtime_imports_are_declared_dependencies() -> None:
    """Every third-party import in src/ must come from a declared dependency."""
    project = _pyproject()["project"]
    _assert_declared(_imported_modules("src"), _names(project["dependencies"]))


def test_test_imports_are_declared_dev_dependencies() -> None:
    """Every third-party import in tests/ must come from a runtime or dev dependency."""
    project = _pyproject()["project"]
    declared = _names(project["dependencies"]) | _names(
        project["optional-dependencies"]["dev"]
    )
    _assert_declared(_imported_modules("tests"), declared)
