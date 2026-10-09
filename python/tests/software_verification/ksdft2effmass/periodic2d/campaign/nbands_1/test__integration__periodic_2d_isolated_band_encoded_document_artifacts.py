r"""Artifact-owned row-046 encoded-document integration evidence.

Evidence profile: claim_bearing

The tests bind the maintained periodic-2D isolated-band input and result bytes to their
repository checksum-catalog identities and verify reviewed import routes. SHA-256
establishes content identity only; it does not establish execution provenance, decoded
correctness, convergence, scientific validity, uncertainty, or acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic2d as periodic2d_facade
import ksdft2effmass.periodic2d.campaign as campaign_facade
from ksdft2effmass.periodic2d.campaign import nbands_1 as nbands_1_facade
from ksdft2effmass.periodic2d.campaign.nbands_1 import (
    Periodic2DIsolatedBandEncodedDocuments,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DIsolatedBandEncodedDocuments
INPUT_SHA256 = "82e9915101e755f7cc77cb8901478f88d878ffaa808732036631b7ae5cfd78ec"
RESULT_SHA256 = "4eb55bde9d456d86bad1d65c8ac60267c07873c6936f8af876b07fd3e1d27be6"


def repository_root() -> Path:
    """Return the repository root containing the maintained calculation artifacts."""
    return Path(__file__).resolve().parents[7]


def checksum_catalog(directory: Path) -> dict[str, str]:
    """Return exact logical-name to SHA-256 entries from the retained catalog."""
    entries: dict[str, str] = {}
    catalog_lines = directory.joinpath("SHA256SUMS").read_text(encoding="utf-8")
    for line in catalog_lines.splitlines():
        if not line:
            continue
        digest, logical_name = line.split(maxsplit=1)
        if logical_name in entries:
            raise ValueError(f"duplicate checksum-catalog name: {logical_name}")
        entries[logical_name] = digest
    return entries


class TestPeriodic2DIsolatedBandEncodedDocumentArtifacts:
    """Own retained-artifact and public-route evidence for crosswalk row 046."""

    def test_retained_artifacts__preserve_bytes_and_catalog_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-046-ARTIFACT-001.

        Requirement: The renamed owner preserves the maintained isolated-band bytes and
        their independently retained checksum-catalog identities.

        Method: Read both compact retained files and the maintained checksum catalog,
        construct the DataObject, and compare byte-object identity and SHA-256 values.

        Oracle: Two reviewed digest literals and the independent ``SHA256SUMS`` entries.

        Acceptance: Stored objects are the exact bytes read from both maintained files;
        computed digests match exact expected values and both catalog entries.

        Interpretation: A pass establishes retained-byte and content-identity
        preservation across the row-046 rename.

        Limitations: Digest equality does not establish provenance, decoded correctness,
        numerical reproduction, scientific validity, UQ, or acceptance.
        """
        retained = repository_root() / "calculations/research-monograph/periodic-2d"
        input_payload = retained.joinpath("input.json").read_bytes()
        result_payload = retained.joinpath("result.json").read_bytes()
        catalog = checksum_catalog(retained)

        documents = SUT(input_payload, result_payload)
        input_digest = hashlib.sha256(input_payload).hexdigest()
        result_digest = hashlib.sha256(result_payload).hexdigest()

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert input_digest == INPUT_SHA256 == catalog["input.json"]
        assert result_digest == RESULT_SHA256 == catalog["result.json"]

    def test_public_routes__share_the_defining_class_without_retired_name(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-046-ROUTE-001.

        Requirement: Reviewed periodic-2D facades expose one defining implementation and
        do not retain the former encoded-model name or source module as an alias.

        Method: Compare all facade exports with the defining class, inspect each facade,
        and inspect the former retained-model source path.

        Oracle: The documented three-route facade contract and row-046 removal
        disposition.

        Acceptance: All supported facades expose the exact defining class object, none
        exposes ``Periodic2DIsolatedBandCampaignModel``, and the retired module is
        absent.

        Interpretation: A pass establishes one implementation without a compatibility
        alias or forwarding source module.

        Limitations: Route identity does not decode or validate either campaign payload.
        """
        assert nbands_1_facade.Periodic2DIsolatedBandEncodedDocuments is SUT
        assert campaign_facade.Periodic2DIsolatedBandEncodedDocuments is SUT
        assert periodic2d_facade.Periodic2DIsolatedBandEncodedDocuments is SUT
        for facade in (nbands_1_facade, campaign_facade, periodic2d_facade):
            assert not hasattr(facade, "Periodic2DIsolatedBandCampaignModel")
        retired_module = (
            repository_root()
            / "python/src/ksdft2effmass/periodic2d/campaign/nbands_1/retained.py"
        )
        assert not retired_module.exists()
