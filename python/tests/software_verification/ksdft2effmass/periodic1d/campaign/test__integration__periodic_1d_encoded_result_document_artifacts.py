r"""Artifact-owned row-045 evidence for periodic-1D encoded results.

Evidence profile: claim_bearing

Bounded artifact scope
----------------------
Six maintained Appendix G result wires, their explicit result-kind pairing, reviewed
SHA-256 catalog identities, complete immutable JSON adaptation, current facade identity,
and retired encoded-result terminology.

Scientific exclusions
---------------------
A pass establishes content identity and software adaptation only. It does not establish
calculation provenance, native-file availability, convergence, decoded scientific
correctness, material validity, transferability, UQ, or acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.campaigns.periodic_1d as transitional_package
import ksdft2effmass.campaigns.research_monograph as publication_package
import ksdft2effmass.periodic1d.campaign as canonical_package
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DCampaignJsonDecoder,
    Periodic1DEncodedResultDocument,
    Periodic1DEncodedResultJsonSerializer,
    Periodic1DEncodedResultKind,
)
from ksdft2effmass.serialization.json import ImmutableJsonArray, ImmutableJsonObject

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
type NestedKind = type[ImmutableJsonArray] | type[ImmutableJsonObject]
RESULT_CASES = (
    pytest.param(
        Periodic1DEncodedResultKind.ISOLATED_BAND,
        "result.json",
        "37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c",
        "research-monograph.periodic-1d.isolated-band.v1",
        "isolated_band_reduction",
        ImmutableJsonObject,
        id="isolated-band",
    ),
    pytest.param(
        Periodic1DEncodedResultKind.STRESS,
        "stress-result.json",
        "5897e16570609f3b2ad2fb5cdefb39b8da9df6395e42796d8c5af77734cba394",
        "research-monograph.periodic-1d.stress.v1",
        "mesh_band_and_isolation_stress",
        ImmutableJsonArray,
        id="reduction-challenge-historical-stress-wire",
    ),
    pytest.param(
        Periodic1DEncodedResultKind.COMPOSITE,
        "composite-result.json",
        "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f",
        "research-monograph.periodic-1d.composite.v1",
        "groups",
        ImmutableJsonArray,
        id="composite",
    ),
    pytest.param(
        Periodic1DEncodedResultKind.WANNIER90,
        "wannier90-result.json",
        "d167294da9ebb53173b91fa69f089900f11e03917969bc028b9c0e69db951535",
        "research-monograph.periodic-1d.wannier90.v1",
        "groups",
        ImmutableJsonArray,
        id="wannier90",
    ),
    pytest.param(
        Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
        "wannier90-preconditioned-result.json",
        "c4d6d32f8a52e93c447424b49b649e63fa036117bf88a4f8af6ed4e1d270316c",
        "research-monograph.periodic-1d.wannier90.v1",
        "groups",
        ImmutableJsonArray,
        id="wannier90-preconditioned",
    ),
    pytest.param(
        Periodic1DEncodedResultKind.WANNIER90_CONVERGENCE_ATTEMPT,
        "wannier90-convergence-attempt.json",
        "54dc87a1f341a4f57116dcdf456a060e8d7b482b92d9596c6022cbe647347b3a",
        "research-monograph.periodic-1d.wannier90.convergence-attempt-1",
        "stages",
        ImmutableJsonArray,
        id="wannier90-convergence-attempt",
    ),
)


class TestPeriodic1DEncodedResultDocumentArtifacts:
    """Own retained-file and facade evidence for row 045."""

    repository_root = Path(__file__).resolve().parents[6]
    artifact_directory = repository_root / "calculations/research-monograph/periodic-1d"

    @classmethod
    def _catalog_digests(cls) -> dict[str, str]:
        """Read the maintained checksum catalog without decoding its result wires."""
        return {
            path: digest
            for digest, path in (
                line.split(maxsplit=1)
                for line in (cls.artifact_directory / "SHA256SUMS")
                .read_text(encoding="utf-8")
                .splitlines()
                if line
            )
        }

    @pytest.mark.parametrize(
        (
            "kind",
            "filename",
            "digest",
            "record_id",
            "nested_field",
            "nested_kind",
        ),
        RESULT_CASES,
    )
    def test_retained_artifacts__preserve_exact_sources_and_catalog_identities(
        self,
        kind: Periodic1DEncodedResultKind,
        filename: str,
        digest: str,
        record_id: str,
        nested_field: str,
        nested_kind: NestedKind,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-ARTIFACT-001.

        Requirement: Every demonstrated result wire retains exact bytes, explicit kind,
        complete immutable JSON meaning, and its reviewed checksum-catalog identity.

        Acceptance: Source object identity, digest, catalog entry, record identity,
        nested shape, and canonical semantic reconstruction agree for all six wires.
        """
        payload = (self.artifact_directory / filename).read_bytes()
        serializer = Periodic1DEncodedResultJsonSerializer(kind)

        document = serializer.deserialize(payload)
        reconstructed = serializer.deserialize(serializer.serialize(document))

        assert document.source_document is payload
        assert hashlib.sha256(document.source_document).hexdigest() == digest
        assert document.source_sha256 == digest
        assert self._catalog_digests()[filename] == digest
        assert document.kind is kind
        assert document.record_id == record_id
        assert type(document.root.field(nested_field)) is nested_kind
        assert reconstructed.root == document.root
        assert reconstructed.record_id == document.record_id

    def test_public_routes__share_defining_classes_without_retired_names(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-045-ROUTE-001.

        Requirement: The canonical facade exposes defining encoded-result owners,
        while transitional, publication, and retired compatibility routes remain absent.

        Acceptance: The canonical facade shares exact class identities. Transitional
        facades expose neither current nor retired shared-result symbols, and no
        ``decode``/``encode`` forwarding method exists.
        """
        assert (
            canonical_package.Periodic1DEncodedResultDocument
            is Periodic1DEncodedResultDocument
        )
        assert (
            canonical_package.Periodic1DEncodedResultJsonSerializer
            is Periodic1DEncodedResultJsonSerializer
        )
        assert (
            canonical_package.Periodic1DEncodedResultKind is Periodic1DEncodedResultKind
        )
        for package in (transitional_package, publication_package):
            assert not hasattr(package, "Periodic1DCampaignJsonDecoder")
            assert not hasattr(package, "Periodic1DEncodedResultDocument")
            assert not hasattr(package, "Periodic1DEncodedResultJsonSerializer")
            assert not hasattr(package, "Periodic1DEncodedResultKind")
            assert not hasattr(package, "Periodic1DRetainedResultDocument")
            assert not hasattr(package, "Periodic1DRetainedResultJsonSerializer")
            assert not hasattr(package, "Periodic1DRetainedResultKind")
            assert not hasattr(package, "Periodic1DJsonArray")
            assert not hasattr(package, "Periodic1DJsonObject")
            assert not hasattr(package, "Periodic1DJsonScalar")
            assert not hasattr(package, "Periodic1DJsonValue")
        assert Periodic1DCampaignJsonDecoder.__module__ == (
            "ksdft2effmass.periodic1d.campaign.serialization.decoding"
        )
        former_root = (
            self.repository_root / "python/src/ksdft2effmass/campaigns/periodic_1d"
        )
        assert not (former_root / "result_documents.py").exists()
        assert not (former_root / "serialization/decoding.py").exists()
        assert not (former_root / "serialization/documents.py").exists()
        assert not hasattr(Periodic1DEncodedResultJsonSerializer, "decode")
        assert not hasattr(Periodic1DEncodedResultJsonSerializer, "encode")
