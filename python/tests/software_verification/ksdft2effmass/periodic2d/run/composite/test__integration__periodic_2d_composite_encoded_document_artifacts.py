r"""Artifact-owned row-047 composite encoded-document integration evidence.

Evidence profile: claim_bearing

The tests bind maintained periodic-2D composite input and result bytes to repository
checksum-catalog identities and verify reviewed import routes. SHA-256 establishes
content identity only; it does not establish execution provenance, decoded correctness,
retained-space or frame identity, convergence, scientific validity, uncertainty, or
acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic2d as periodic2d_facade
from ksdft2effmass.periodic2d.run import composite as composite_facade
from ksdft2effmass.periodic2d.run.composite import (
    Periodic2DCompositeEncodedDocuments,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DCompositeEncodedDocuments
INPUT_SHA256 = "4abe583a5198537703f3a9e4937fd93c4c7cd6f46a3eefd302a551b1f0ae7e90"
RESULT_SHA256 = "2bd97c1138e501e0b26f19dd43b3bb1718dc6e4655804f6bc96e853c7fd87792"


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


class TestPeriodic2DCompositeEncodedDocumentArtifacts:
    """Own retained-artifact and public-route evidence for crosswalk row 047."""

    def test_retained_artifacts__preserve_bytes_and_catalog_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-047-ARTIFACT-001.

        Requirement: The renamed owner preserves maintained composite bytes and their
        independently retained checksum-catalog identities.

        Method: Read both compact retained files and the maintained checksum catalog,
        construct the DataObject, and compare byte-object identity and SHA-256 values.

        Oracle: Two reviewed digest literals and the independent ``SHA256SUMS`` entries.

        Acceptance: Stored objects are the exact bytes read from both maintained files;
        computed digests match exact expected values and both catalog entries.

        Interpretation: A pass establishes retained-byte and content-identity
        preservation across the row-047 rename.

        Limitations: Digest equality does not establish provenance, decoded correctness,
        numerical reproduction, scientific validity, UQ, or acceptance.
        """
        retained = repository_root() / "calculations/research-monograph/periodic-2d"
        input_payload = retained.joinpath("composite-input.json").read_bytes()
        result_payload = retained.joinpath("composite-result.json").read_bytes()
        catalog = checksum_catalog(retained)

        documents = SUT(input_payload, result_payload)
        input_digest = hashlib.sha256(input_payload).hexdigest()
        result_digest = hashlib.sha256(result_payload).hexdigest()

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert input_digest == INPUT_SHA256 == catalog["composite-input.json"]
        assert result_digest == RESULT_SHA256 == catalog["composite-result.json"]

    def test_public_routes__share_implementation_without_retired_name(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-047-ROUTE-001.

        Requirement: Reviewed periodic-2D facades expose one defining implementation and
        do not retain the former encoded-model name or source module as an alias.

        Method: Compare both facade exports with the defining class, inspect each
        facade, and inspect the former retained-model source path.

        Oracle: The documented two-route facade contract and row-047 removal
        disposition.

        Acceptance: Both supported facades expose the exact defining class object,
        neither exposes ``Periodic2DCompositeCampaignModel``, and the retired module is
        absent.

        Interpretation: A pass establishes one implementation without a compatibility
        alias or forwarding source module.

        Limitations: Route identity does not decode or validate either campaign payload.
        """
        assert composite_facade.Periodic2DCompositeEncodedDocuments is SUT
        assert periodic2d_facade.Periodic2DCompositeEncodedDocuments is SUT
        for facade in (composite_facade, periodic2d_facade):
            assert not hasattr(facade, "Periodic2DCompositeCampaignModel")
        retired_module = (
            repository_root()
            / "python/src/ksdft2effmass/periodic2d/model/retained/composite.py"
        )
        assert not retired_module.exists()
