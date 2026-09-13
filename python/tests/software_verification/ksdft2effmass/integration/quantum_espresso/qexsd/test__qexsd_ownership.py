r"""Software verification of canonical QEXSD integration ownership.

Evidence profile: routine

Bounded artifact scope: canonical integration ownership and removed legacy-I/O
namespace.

Facet and represented meaning

The artifact identifies the canonical QEXSD source, native document, and parser owners.

Intrinsic and cross-object scope

Public export identity, legacy-path absence, and forbidden neutral-package imports are
covered; semantic adaptation and schema-v1 serialization are separate.

VVUQ and scientific exclusions

These tests establish software ownership only, not scientific interpretation,
validation, convergence, or uncertainty quantification.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import ksdft2effmass.integration.quantum_espresso.qexsd as canonical

pytestmark = pytest.mark.software_verification


class TestQexsdOwnership:
    """Own this module's maintained software-verification evidence."""

    def test_public_api__package__exports_exact_native_qexsd_surface(self) -> None:
        """Evidence ID: SV-QEXSD-001

        Requirement: Canonical QEXSD integration exports source, native document,
        parser, and schema-version-1 translation contracts, with no ununderscored
        namespace.

        Acceptance: Ordered ``__all__`` and defining modules match exactly, and the
        removed compatibility package directory is absent.
        """
        assert tuple(canonical.__all__) == (
            "ConstructQexsdKohnShamPlaneWaveRecord",
            "QuantumEspressoXsdDocumentParser",
            "QexsdDocument",
            "QexsdSource",
        )
        assert canonical.QexsdSource.__module__ == (
            "ksdft2effmass.integration.quantum_espresso.qexsd.records"
        )
        assert canonical.QexsdDocument.__module__ == (
            "ksdft2effmass.integration.quantum_espresso.qexsd.records"
        )
        assert canonical.QuantumEspressoXsdDocumentParser.__module__ == (
            "ksdft2effmass.integration.quantum_espresso.qexsd.parsing"
        )
        assert not hasattr(canonical, "QexsdDocumentParser")
        assert not hasattr(canonical, "ParseQexsdDocument")
        integration_root = Path(canonical.__file__).resolve().parents[2]
        assert not (integration_root / "quantumespresso").exists()

    def test_public_api__legacy_io_path__is_absent(self) -> None:
        """Evidence ID: SV-QEXSD-002

        Requirement: The former ``io.quantum_espresso.qexsd`` forwarding path is
        removed.

        Acceptance: No legacy-I/O package directory remains beneath the source root.
        """
        package_root = Path(canonical.__file__).resolve().parents[3]
        assert not (package_root / "io" / "quantum_espresso" / "qexsd").exists()

    def test_artifact__dependency__neutral_packages_import_no_qexsd_owner(self) -> None:
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
            "ksdft2effmass.integration.quantum_espresso.qexsd",
        )
        assert not any(
            name.startswith(forbidden)
            for name in direct | from_names | absolute_from_names
        )
        assert not any(
            name.startswith(("integration", "io.quantum_espresso.qexsd"))
            for name in relative_names
        )
