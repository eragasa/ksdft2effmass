# ruff: noqa: E501
"""Shared construction support for project-local software verification."""

from __future__ import annotations

from pathlib import Path

from ksdft2effmass.harness.pi.local import (
    LoadLocalHarnessContext,
    LocalHarnessContext,
    RepositoryRoots,
)


def repository_root() -> Path:
    """Return the explicit test repository root; this helper owns no evidence ID."""
    return Path(__file__).resolve().parents[7]


def local_context() -> LocalHarnessContext:
    """Build explicit current-tree context; this helper supports SV-HL evidence."""
    root = repository_root()
    roots = RepositoryRoots(root, root / "harness/pi", root / "harness/local")
    result = LoadLocalHarnessContext().execute(
        roots,
        (root / "harness/local/profiles/ksdft2effmass-v2.json").read_bytes(),
        (root / "harness/pi/resource-manifest.json").read_bytes(),
        (root / "harness/local/resource-manifest.json").read_bytes(),
    )
    assert isinstance(result.value, LocalHarnessContext)
    return result.value
