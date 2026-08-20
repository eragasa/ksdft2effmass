r"""Software verification of canonical QEXSD integration ownership.

Evidence profile: routine

Bounded artifact scope: canonical integration imports and legacy forwarding identity.

Facet and represented meaning

The artifact identifies the canonical QEXSD source, native document, and parser owners.

Intrinsic and cross-object scope

Public export identity, compatibility forwarding, and forbidden neutral-package
imports are covered; semantic adaptation and schema-v1 serialization are separate.

VVUQ and scientific exclusions

These tests establish software ownership only, not scientific interpretation,
validation, convergence, or uncertainty quantification.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import ksdft2effmass.integration.quantumespresso.qexsd as canonical
import ksdft2effmass.integration.quantumespresso.qexsd.records as canonical_records
import ksdft2effmass.io.quantum_espresso.qexsd as legacy
import ksdft2effmass.io.quantum_espresso.qexsd.records as legacy_records

pytestmark = pytest.mark.software_verification


def test_public_api__package__exports_exact_native_qexsd_surface() -> None:
    """Evidence ID: SV-QEXSD-001

    Requirement: Canonical QEXSD integration exports only source, native document,
    and parser ActionObject contracts.

    Acceptance: Ordered ``__all__`` and defining modules match exactly.
    """
    assert tuple(canonical.__all__) == (
        "QexsdDocument",
        "QexsdDocumentParser",
        "QexsdSource",
    )
    assert canonical.QexsdSource.__module__ == (
        "ksdft2effmass.integration.quantumespresso.qexsd.records"
    )
    assert canonical.QexsdDocument.__module__ == (
        "ksdft2effmass.integration.quantumespresso.qexsd.records"
    )
    assert canonical.QexsdDocumentParser.__module__ == (
        "ksdft2effmass.integration.quantumespresso.qexsd.parsing"
    )


def test_public_api__compatibility__legacy_imports_forward_exact_identity() -> None:
    """Evidence ID: SV-QEXSD-002

    Requirement: The accepted v1 import path forwards to canonical objects without
    duplicating parser or native-record policy.

    Acceptance: Every retained legacy object is identical to its canonical owner.
    """
    assert legacy.QexsdSource is canonical.QexsdSource
    assert legacy.QexsdDocument is canonical.QexsdDocument
    assert legacy.QexsdDocumentParser is canonical.QexsdDocumentParser
    assert legacy.ParseQexsdDocument is canonical.QexsdDocumentParser
    assert legacy_records.SpeciesDeclaration is canonical_records.SpeciesDeclaration
    assert legacy_records.AtomDeclaration is canonical_records.AtomDeclaration
    assert legacy_records.Spectrum is canonical_records.Spectrum
    assert legacy_records.Vector3 is canonical_records.Vector3
    assert legacy_records.Vector3Sequence is canonical_records.Vector3Sequence


def test_artifact__dependency__neutral_packages_import_no_qexsd_owner() -> None:
    """Evidence ID: SV-QEXSD-003

    Requirement: Neutral periodic and Kohn--Sham packages import neither canonical
    integration nor legacy QEXSD modules.

    Acceptance: Static imports under both neutral package trees contain no forbidden
    integration or QEXSD prefix.
    """
    source_root = Path(canonical.__file__).resolve().parents[3]
    neutral_paths = tuple(
        (source_root / name).rglob("*.py") for name in ("periodic", "ksdft")
    )
    paths = tuple(path for group in neutral_paths for path in group)
    trees = tuple(ast.parse(path.read_text(encoding="utf-8")) for path in paths)
    nodes = tuple(node for tree in trees for node in ast.walk(tree))
    direct = {
        alias.name
        for node in nodes
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    from_names = {
        node.module
        for node in nodes
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    absolute_from_names = {
        node.module + "." + alias.name
        for node in nodes
        if isinstance(node, ast.ImportFrom)
        and node.level == 0
        and node.module is not None
        for alias in node.names
    }
    relative_names = {
        (node.module + "." + alias.name if node.module else alias.name)
        for node in nodes
        if isinstance(node, ast.ImportFrom) and node.level > 0
        for alias in node.names
    }
    forbidden = (
        "ksdft2effmass.integration",
        "ksdft2effmass.io.quantum_espresso.qexsd",
    )
    assert not any(
        name.startswith(forbidden)
        for name in direct | from_names | absolute_from_names
    )
    assert not any(
        name.startswith(("integration", "io.quantum_espresso.qexsd"))
        for name in relative_names
    )
