r"""Software verification of the DFT pseudopotential catalog contract.

Evidence profile: routine

Bounded artifact scope: backend-neutral content-addressed pseudopotential layout,
SQLite metadata catalog, byte verification, and native QE/ABINIT bindings.

Facet and represented meaning

The artifact represents immutable source-library entries, exact native-format file
identities, deterministic external locations, insert-only catalog behavior, and
format-specific calculator references.

Intrinsic and cross-object scope

Tests cover exact field invariants, layout derivation, schema initialization,
transactional recording, round-trip resolution, current-byte verification, deliberate
public exports, and UPF2/PSP8 adapter separation.

VVUQ and scientific exclusions

These tests use synthetic text bytes. They perform no download, pseudopotential
conversion, calculator execution, numerical verification, scientific validation, or
uncertainty quantification and establish no physical equivalence between formats.
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import ksdft2effmass.simulations as simulations
import ksdft2effmass.simulations.abinit as abinit
import ksdft2effmass.simulations.dft as dft
import ksdft2effmass.simulations.quantumespresso as qe
from ksdft2effmass.simulations.abinit import (
    AbinitPseudopotentialAdapter,
    AbinitPseudopotentialReference,
)
from ksdft2effmass.simulations.dft import (
    PseudopotentialArtifact,
    PseudopotentialArtifactFormat,
    PseudopotentialArtifactPathResolver,
    PseudopotentialArtifactVerifier,
    PseudopotentialCatalogEntry,
    PseudopotentialCatalogInitializer,
    PseudopotentialCatalogRecorder,
    PseudopotentialCatalogResolver,
    PseudopotentialCutoffHints,
    PseudopotentialFormalism,
    PseudopotentialLibraryLayout,
    PseudopotentialRelativity,
    PseudopotentialSha256,
    PseudopotentialSourceEntry,
    PseudopotentialVerificationStatus,
)
from ksdft2effmass.simulations.quantumespresso import (
    QuantumEspressoPseudopotentialAdapter,
    QuantumEspressoPseudopotentialReference,
)

pytestmark = pytest.mark.software_verification


class TestPseudopotentialCatalogContract:
    """Own maintained evidence for the cohesive catalog and binding artifact."""

    @staticmethod
    def source_entry() -> PseudopotentialSourceEntry:
        """Construct one synthetic PseudoDojo-like silicon source entry."""
        return PseudopotentialSourceEntry(
            identity="pseudodojo.oncvpsp-v0.5.pbe.nc-sr.stringent.si",
            family="pseudodojo",
            release="oncvpsp-v0.5",
            exchange_correlation="pbe",
            accuracy_tier="stringent",
            element_symbol="Si",
            atomic_number=14,
            formalism=PseudopotentialFormalism.NORM_CONSERVING,
            relativistic_treatment=PseudopotentialRelativity.SCALAR_RELATIVISTIC,
            valence_electrons=4,
            cutoff_hints=PseudopotentialCutoffHints(
                low_hartree=14.0,
                normal_hartree=18.0,
                high_hartree=24.0,
            ),
        )

    @classmethod
    def artifact(
        cls,
        payload: bytes,
        artifact_format: PseudopotentialArtifactFormat,
        filename: str,
    ) -> PseudopotentialArtifact:
        """Construct exact metadata from independently hashed synthetic bytes."""
        return PseudopotentialArtifact(
            source_entry_identity=cls.source_entry().identity,
            content_identity=PseudopotentialSha256(hashlib.sha256(payload).hexdigest()),
            format=artifact_format,
            filename=filename,
            byte_size=len(payload),
            source_url=f"https://example.invalid/pseudos/{filename}",
        )

    @classmethod
    def record(
        cls,
        tmp_path: Path,
        payload: bytes,
        artifact_format: PseudopotentialArtifactFormat,
        filename: str,
    ) -> PseudopotentialCatalogEntry:
        """Initialize scratch, place exact bytes, and invoke the public recorder."""
        layout = PseudopotentialLibraryLayout(tmp_path / "pseudopotentials")
        PseudopotentialCatalogInitializer().execute(layout)
        artifact = cls.artifact(payload, artifact_format, filename)
        path_resolver = PseudopotentialArtifactPathResolver()
        local_path = path_resolver.execute(layout, artifact)
        local_path.parent.mkdir(parents=True)
        local_path.write_bytes(payload)
        return PseudopotentialCatalogRecorder(path_resolver).execute(
            layout, cls.source_entry(), artifact
        )

    def test_public_api__packages__export_owned_catalog_and_adapters(self) -> None:
        """Evidence ID: SV-PSEUDO-CATALOG-001

        Requirement: The root ``simulations`` package is not a broad re-export
        namespace. Generic pseudopotential ownership is exported from
        ``simulations.dft`` while QE and ABINIT export only their native adapters and
        references.

        Acceptance: Generic and backend-specific classes are absent from the root;
        every asserted subpackage attribute is the exact imported class; and no
        backend package substitutes the generic catalog owner.
        """
        assert not hasattr(simulations, "PseudopotentialCatalogEntry")
        assert not hasattr(simulations, "PseudopotentialCatalogRecorder")
        assert not hasattr(simulations, "QuantumEspressoPseudopotentialAdapter")
        assert not hasattr(simulations, "AbinitPseudopotentialAdapter")
        assert dft.PseudopotentialCatalogEntry is PseudopotentialCatalogEntry
        assert (
            dft.PseudopotentialCatalogInitializer is PseudopotentialCatalogInitializer
        )
        assert dft.PseudopotentialCatalogRecorder is PseudopotentialCatalogRecorder
        assert dft.PseudopotentialCatalogResolver is PseudopotentialCatalogResolver
        assert (
            qe.QuantumEspressoPseudopotentialAdapter
            is QuantumEspressoPseudopotentialAdapter
        )
        assert (
            qe.QuantumEspressoPseudopotentialReference
            is QuantumEspressoPseudopotentialReference
        )
        assert abinit.AbinitPseudopotentialAdapter is AbinitPseudopotentialAdapter
        assert abinit.AbinitPseudopotentialReference is AbinitPseudopotentialReference

    def test_property__layout__derives_versioned_non_authoritative_boundaries(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PSEUDO-CATALOG-002

        Requirement: One explicit absolute root deterministically separates payloads,
        manifests, catalog state, backend views, and mutable incoming staging without
        consulting an ambient home directory.

        Acceptance: Every path equals the complete literal root-relative contract and
        initialization creates schema version 1 without payload files.
        """
        layout = PseudopotentialLibraryLayout(tmp_path / "library")

        PseudopotentialCatalogInitializer().execute(layout)

        assert layout.artifacts_root == layout.root / "artifacts" / "sha256"
        assert layout.manifests_root == layout.root / "manifests" / "sets"
        assert layout.catalog_path == (
            layout.root / "catalog" / "pseudopotentials-v1.sqlite3"
        )
        assert layout.views_root / "quantumespresso" == (
            layout.root / "views" / "quantumespresso"
        )
        assert layout.views_root / "abinit" == layout.root / "views" / "abinit"
        assert layout.incoming_root == layout.root / "incoming"
        with sqlite3.connect(layout.catalog_path) as connection:
            version = connection.execute(
                "SELECT value FROM catalog_metadata WHERE key = 'schema_version'"
            ).fetchone()
            payload_count = connection.execute(
                "SELECT COUNT(*) FROM artifacts"
            ).fetchone()
        assert version == ("1",)
        assert payload_count == (0,)

    def test_method__execute__records_resolves_and_verifies_exact_local_bytes(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PSEUDO-CATALOG-003

        Requirement: Recording admits only bytes already present at the complete
        SHA-256 path, stores metadata rather than payload bytes, and resolution
        reconstructs the immutable public records.

        Acceptance: The content path has the exact digest hierarchy, repeated exact
        recording is idempotent, resolution equals the record, and verification
        reports an exact match.
        """
        payload = b"synthetic UPF2 pseudopotential test bytes\n"
        entry = self.record(
            tmp_path, payload, PseudopotentialArtifactFormat.UPF2, "Si.upf"
        )
        layout = PseudopotentialLibraryLayout(tmp_path / "pseudopotentials")
        path_resolver = PseudopotentialArtifactPathResolver()

        repeated = PseudopotentialCatalogRecorder(path_resolver).execute(
            layout, entry.source_entry, entry.artifact
        )
        resolved = PseudopotentialCatalogResolver(path_resolver).execute(
            layout, entry.artifact.content_identity
        )
        verification = PseudopotentialArtifactVerifier().execute(entry)

        digest = entry.artifact.content_identity.digest
        assert entry.local_path == (
            layout.root / "artifacts" / "sha256" / digest[:2] / digest / "Si.upf"
        )
        assert repeated == entry
        assert resolved == entry
        assert verification.status is PseudopotentialVerificationStatus.MATCH
        assert verification.observed_byte_size == len(payload)
        assert verification.observed_sha256 == entry.artifact.content_identity
        assert resolved is not None
        assert resolved.source_entry.cutoff_hints == PseudopotentialCutoffHints(
            low_hartree=14.0,
            normal_hartree=18.0,
            high_hartree=24.0,
        )

        entry.local_path.write_bytes(b"x" * len(payload))
        changed = PseudopotentialArtifactVerifier().execute(entry)
        assert changed.status is PseudopotentialVerificationStatus.SHA256_MISMATCH
        assert changed.observed_byte_size == len(payload)
        assert changed.observed_sha256 != entry.artifact.content_identity

    def test_method__execute__rejects_unverified_or_conflicting_metadata(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PSEUDO-CATALOG-004

        Requirement: The catalog must not record absent, content-mismatched, or
        identity-conflicting artifacts under an accepted source identity.

        Acceptance: Absent bytes, a wrong digest, and changed metadata for an existing
        source identity each raise the stated deterministic exception.
        """
        layout = PseudopotentialLibraryLayout(tmp_path / "library")
        PseudopotentialCatalogInitializer().execute(layout)
        path_resolver = PseudopotentialArtifactPathResolver()
        recorder = PseudopotentialCatalogRecorder(path_resolver)
        payload = b"synthetic psp8 bytes\n"
        artifact = self.artifact(payload, PseudopotentialArtifactFormat.PSP8, "Si.psp8")

        with pytest.raises(FileNotFoundError):
            recorder.execute(layout, self.source_entry(), artifact)

        local_path = path_resolver.execute(layout, artifact)
        local_path.parent.mkdir(parents=True)
        local_path.write_bytes(b"same-size-wrong-data")
        with pytest.raises(ValueError, match="SHA-256|byte size"):
            recorder.execute(layout, self.source_entry(), artifact)

        local_path.write_bytes(payload)
        recorder.execute(layout, self.source_entry(), artifact)
        conflicting_source = PseudopotentialSourceEntry(
            identity=self.source_entry().identity,
            family="different-family",
            release=self.source_entry().release,
            exchange_correlation=self.source_entry().exchange_correlation,
            accuracy_tier=self.source_entry().accuracy_tier,
            element_symbol=self.source_entry().element_symbol,
            atomic_number=self.source_entry().atomic_number,
            formalism=self.source_entry().formalism,
            relativistic_treatment=self.source_entry().relativistic_treatment,
            valence_electrons=self.source_entry().valence_electrons,
            cutoff_hints=self.source_entry().cutoff_hints,
        )
        with pytest.raises(ValueError, match="source entry identity conflicts"):
            recorder.execute(layout, conflicting_source, artifact)

    def test_method__execute__separates_qe_upf2_and_abinit_psp8_bindings(
        self, tmp_path: Path
    ) -> None:
        """Evidence ID: SV-PSEUDO-CATALOG-005

        Requirement: Backend composition retains one shared source-entry identity but
        requires QE-native UPF2 and ABINIT-native PSP8 artifacts with independent
        complete content identities.

        Acceptance: Each adapter returns its exact native reference and rejects the
        opposite native representation.
        """
        upf_entry = self.record(
            tmp_path,
            b"synthetic UPF2 representation\n",
            PseudopotentialArtifactFormat.UPF2,
            "Si.upf",
        )
        psp8_entry = self.record(
            tmp_path,
            b"synthetic PSP8 representation\n",
            PseudopotentialArtifactFormat.PSP8,
            "Si.psp8",
        )

        qe_reference = QuantumEspressoPseudopotentialAdapter().execute(upf_entry)
        abinit_reference = AbinitPseudopotentialAdapter().execute(psp8_entry)

        assert qe_reference.source_entry_identity == self.source_entry().identity
        assert qe_reference.content_identity == upf_entry.artifact.content_identity
        assert qe_reference.local_path == upf_entry.local_path
        assert abinit_reference.source_entry_identity == self.source_entry().identity
        assert abinit_reference.content_identity == psp8_entry.artifact.content_identity
        assert abinit_reference.local_path == psp8_entry.local_path
        assert qe_reference.content_identity != abinit_reference.content_identity
        with pytest.raises(ValueError, match="UPF2"):
            QuantumEspressoPseudopotentialAdapter().execute(psp8_entry)
        with pytest.raises(ValueError, match="PSP8"):
            AbinitPseudopotentialAdapter().execute(upf_entry)

    def test_constructor__types_and_immutability__reject_implicit_coercion(
        self,
    ) -> None:
        """Evidence ID: SV-PSEUDO-CATALOG-006

        Requirement: Public numeric boundaries reject booleans, integers supplied for
        explicit floating-point Hartree values, mutable field assignment, and invalid
        digest representations.

        Acceptance: Wrong semantic types raise ``TypeError``, malformed digests raise
        ``ValueError``, and ordinary mutation raises ``FrozenInstanceError``.
        """
        with pytest.raises(TypeError):
            PseudopotentialCutoffHints(
                low_hartree=14,
                normal_hartree=18.0,
                high_hartree=24.0,
            )
        with pytest.raises(TypeError):
            PseudopotentialSourceEntry(
                identity="invalid.bool.atomic-number",
                family="fixture",
                release="1.0",
                exchange_correlation="pbe",
                accuracy_tier="standard",
                element_symbol="Si",
                atomic_number=True,
                formalism=PseudopotentialFormalism.NORM_CONSERVING,
                relativistic_treatment=(PseudopotentialRelativity.SCALAR_RELATIVISTIC),
                valence_electrons=4,
                cutoff_hints=None,
            )
        with pytest.raises(ValueError):
            PseudopotentialSha256("A" * 64)
        source_entry = self.source_entry()
        with pytest.raises(FrozenInstanceError):
            source_entry.family = "mutated"  # type: ignore[misc]
