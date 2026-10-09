r"""Artifact-owned integration evidence for row-040 Wannier90 documents.

Evidence profile: claim_bearing

Bounded artifact, split, and route scope
---------------------------------------
The maintained periodic-1D ``composite-input.json``, ``wannier90-result.json``, and
``wannier90-preconditioned-result.json`` files; their ``SHA256SUMS`` entries; the
reviewed encoded-document and native-artifact-group import routes; explicit campaign
composition; and removal of the former ``Periodic1DWannier90IntegrationModel`` module
and exports.

Runtime and scientific boundary
-------------------------------
The tests perform bounded local reads of compact maintained JSON files and import public
Python facades. They neither read external native Wannier90 files nor invoke, discover,
or emulate a Wannier90 executable. Result-kind identity distinguishes exact encoded
wire variants; it does not establish native-file availability, localization convergence,
material validity, or scientific acceptance.

Scientific exclusions
---------------------
A pass establishes retained content identity and the software ownership split only. It
does not authenticate calculation provenance, parse the retained result payloads,
reconstruct Wilson loops, qualify a numerical oracle, establish physical adequacy,
quantify uncertainty, or record acceptance.
"""

import hashlib
from dataclasses import fields
from pathlib import Path

import pytest

from ksdft2effmass.integration.wannier90 import Wannier90NativeArtifact
from ksdft2effmass.periodic1d.campaign import Periodic1DEncodedResultKind
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DWannier90EncodedDocuments as PublicEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DWannier90NativeArtifactGroup as PublicNativeArtifactGroup,
)
from ksdft2effmass.periodic1d.campaign.wannier90 import (
    Periodic1DWannier90EncodedDocuments,
    Periodic1DWannier90Integration,
    Periodic1DWannier90NativeArtifactGroup,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Periodic1DWannier90EncodedDocuments


class TestPeriodic1DWannier90EncodedDocumentArtifacts:
    """Own row-040 retained-file, ownership-split, and route evidence."""

    repository_root = Path(__file__).resolve().parents[7]
    artifact_directory = repository_root / "calculations/research-monograph/periodic-1d"
    input_digest = "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
    initial_result_digest = (
        "d167294da9ebb53173b91fa69f089900f11e03917969bc028b9c0e69db951535"
    )
    preconditioned_result_digest = (
        "c4d6d32f8a52e93c447424b49b649e63fa036117bf88a4f8af6ed4e1d270316c"
    )

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes, bytes]:
        """Read the three maintained row-040 payloads as exact bytes."""
        return (
            (cls.artifact_directory / "composite-input.json").read_bytes(),
            (cls.artifact_directory / "wannier90-result.json").read_bytes(),
            (
                cls.artifact_directory / "wannier90-preconditioned-result.json"
            ).read_bytes(),
        )

    @classmethod
    def _catalog_digests(cls) -> dict[str, str]:
        """Read the maintained checksum catalog without decoding campaign payloads."""
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

    def test_retained_artifacts__preserve_both_exact_wire_variants(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-ARTIFACT-001.

        Requirement: The encoded owner preserves the shared composite input and both
        maintained Wannier90 result variants with explicit, non-inferred kind identity.

        Method: Read the three compact retained artifacts, construct one record for each
        result variant, and compare byte-object identity and computed SHA-256 digests
        with reviewed constants and the maintained checksum catalog.

        Oracle: The three reviewed SHA-256 values, their ``SHA256SUMS`` entries, and the
        explicit enum member paired with each result file.

        Acceptance: Both records retain their supplied byte objects; their exact kinds,
        computed digests, and checksum-catalog entries all match.

        Interpretation: A pass establishes exact retained-byte, content-identity, and
        wire-variant preservation across the row-040 split.

        Limitations: Digest and enum equality do not authenticate provenance, decode
        semantics, establish native-artifact availability or localization convergence,
        validate physics, quantify uncertainty, or record acceptance.
        """
        input_payload, initial_payload, preconditioned_payload = (
            self._retained_payloads()
        )
        initial = SUT(
            input_payload,
            initial_payload,
            Periodic1DEncodedResultKind.WANNIER90,
        )
        preconditioned = SUT(
            input_payload,
            preconditioned_payload,
            Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED,
        )
        catalog = self._catalog_digests()

        assert initial.composite_input_payload is input_payload
        assert preconditioned.composite_input_payload is input_payload
        assert initial.result_payload is initial_payload
        assert preconditioned.result_payload is preconditioned_payload
        assert initial.result_kind is Periodic1DEncodedResultKind.WANNIER90
        assert (
            preconditioned.result_kind
            is Periodic1DEncodedResultKind.WANNIER90_PRECONDITIONED
        )
        assert hashlib.sha256(input_payload).hexdigest() == self.input_digest
        assert hashlib.sha256(initial_payload).hexdigest() == self.initial_result_digest
        assert (
            hashlib.sha256(preconditioned_payload).hexdigest()
            == self.preconditioned_result_digest
        )
        # Catalog agreement binds reviewed constants to maintained content identities;
        # it does not authenticate where or how any calculation was performed.
        assert catalog["composite-input.json"] == self.input_digest
        assert catalog["wannier90-result.json"] == self.initial_result_digest
        assert (
            catalog["wannier90-preconditioned-result.json"]
            == self.preconditioned_result_digest
        )

    def test_ownership_and_public_routes__preserve_explicit_split(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-040-ROUTE-001.

        Requirement: Encoded documents and native files have separate defining owners,
        both reviewed facades expose those owners, and campaign composition is explicit
        without the former aggregate-model route.

        Method: Compare facade exports by object identity, inspect dataclass fields and
        defining modules, compose synthetic explicit state, and inspect retired exports
        and the former source path.

        Oracle: The documented row-040 split and supported import routes.

        Acceptance: The encoded class has no artifact field; the native group contains
        only its explicit group identity and artifact tuple; campaign integration holds
        both exact objects; both facades expose defining classes; retired routes remain
        absent.

        Interpretation: A pass establishes software ownership and composition, not
        correlation or verification of native scientific content.

        Limitations: Synthetic explicit artifacts establish neither retained native-file
        identity nor agreement with either maintained encoded result.
        """
        import ksdft2effmass.campaigns.periodic_1d as transitional
        import ksdft2effmass.campaigns.research_monograph as publication
        import ksdft2effmass.periodic1d.campaign as campaign_facade
        import ksdft2effmass.periodic1d.campaign.wannier90 as leaf_facade

        assert PublicEncodedDocuments is SUT
        assert PublicNativeArtifactGroup is Periodic1DWannier90NativeArtifactGroup
        assert (
            campaign_facade.Periodic1DWannier90Integration
            is Periodic1DWannier90Integration
        )
        assert (
            leaf_facade.Periodic1DWannier90Integration is Periodic1DWannier90Integration
        )
        assert SUT.__module__ == (
            "ksdft2effmass.periodic1d.campaign.wannier90.encoded_documents"
        )
        assert Periodic1DWannier90NativeArtifactGroup.__module__ == (
            "ksdft2effmass.periodic1d.campaign.wannier90.native_artifacts"
        )
        assert [field.name for field in fields(SUT)] == [
            "composite_input_payload",
            "result_payload",
            "result_kind",
        ]
        assert [
            field.name for field in fields(Periodic1DWannier90NativeArtifactGroup)
        ] == ["group_id", "artifacts"]

        documents = SUT(
            b"input",
            b"result",
            Periodic1DEncodedResultKind.WANNIER90,
        )
        artifact = Wannier90NativeArtifact("synthetic.win", b"")
        group = Periodic1DWannier90NativeArtifactGroup("synthetic", (artifact,))
        integration = Periodic1DWannier90Integration(documents, (group,))
        assert integration.encoded_documents is documents
        assert integration.artifact_groups[0] is group

        moved_names = {
            name
            for name in leaf_facade.__all__
            if name.startswith("Periodic1DWannier90")
        }
        assert moved_names
        assert not moved_names & set(transitional.__all__)
        assert not moved_names & set(publication.__all__)
        retired_name = "Periodic1DWannier90IntegrationModel"
        assert not hasattr(transitional, retired_name)
        assert not hasattr(publication, retired_name)
        # A missing export is insufficient when a forwarding implementation remains.
        former_root = (
            self.repository_root / "python/src/ksdft2effmass/campaigns/periodic_1d"
        )
        for relative in (
            "encoded_documents.py",
            "native_artifact_workflows.py",
            "wannier90_results.py",
            "wilson_workflows.py",
            "verification.py",
            "verified_workflows.py",
            "serialization/wannier90.py",
            "run/wannier90",
            "model/integrations/wannier90.py",
        ):
            assert not (former_root / relative).exists()
