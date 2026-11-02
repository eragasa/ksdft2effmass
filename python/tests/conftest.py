"""Repository-wide pytest fixtures."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repository_root() -> Path:
    """Return the repository root without depending on a test module's depth."""
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "AGENTS.md").is_file() and (
            candidate / "python" / "pyproject.toml"
        ).is_file():
            return candidate
    raise RuntimeError("could not locate the repository root")
