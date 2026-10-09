r"""Artifact-owned row-050 balanced Wannier90 encoded-document evidence.

Evidence profile: claim_bearing

The tests bind one maintained encoded result to its repository checksum-catalog identity
and verify reviewed import routes. SHA-256 establishes content identity only. The
encoded result does not imply an input document, native-file presence, execution
provenance, localization convergence, decoded correctness, scientific validity,
uncertainty quantification, or acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic2d as periodic2d_facade
from ksdft2effmass.periodic2d.run import wannier90 as wannier90_facade
from ksdft2effmass.periodic2d.run.wannier90 import balanced as balanced_facade
from ksdft2effmass.periodic2d.run.wannier90.balanced import (
    Periodic2DWannier90BalancedEncodedDocuments,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DWannier90BalancedEncodedDocuments
RESULT_NAME = "wannier90-balanced-result.json"
RESULT_SHA256 = "422e53b012fb824164e3f03e67eeef6f5a013ce6f17da942ddc3f2d477b06e93"


def repository_root() -> Path:
    """Return the repository root containing the maintained calculation artifact."""
    return Path(__file__).resolve().parents[8]


def checksum_catalog(directory: Path) -> dict[str, str]:
    """Return unique logical-name to SHA-256 entries from the retained catalog.

    Parameters
    ----------
    directory
        Maintained periodic-2D artifact directory containing ``SHA256SUMS``.

    Returns
    -------
    dict[str, str]
        Fresh mapping from exact catalog names to declared digest strings.

    Raises
    ------
    ValueError
        If the catalog repeats a logical name.
    """
    entries: dict[str, str] = {}
    catalog_lines = directory.joinpath("SHA256SUMS").read_text(encoding="utf-8")
    for line in catalog_lines.splitlines():
        if not line:
            continue
        digest, logical_name = line.split(maxsplit=1)
        # Duplicate names would make the retained evidence binding ambiguous.
        if logical_name in entries:
            raise ValueError(f"duplicate checksum-catalog name: {logical_name}")
        entries[logical_name] = digest
    return entries


class TestPeriodic2DWannier90BalancedEncodedDocumentArtifact:
    """Own retained-artifact and public-route evidence for crosswalk row 050."""

    def test_retained_artifact__preserves_bytes_and_catalog_identity(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-050-ARTIFACT-001.

        Requirement: The renamed owner preserves the maintained balanced-result bytes
        and their independently retained checksum-catalog identity.

        Method: Read the compact retained result and checksum catalog, construct the
        DataObject, and compare byte-object identity and SHA-256 values.

        Oracle: One reviewed content-identity literal and an independent ``SHA256SUMS``
        entry; the artifact is not treated as a numerical or scientific oracle.

        Acceptance: The stored object is the exact bytes read from the maintained file,
        and its computed digest matches the expected value and catalog entry.

        Interpretation: A pass establishes retained-byte and content-identity
        preservation across the row-050 rename.

        Limitations: Digest equality does not establish native-file presence, execution
        provenance, localization convergence, decoded correctness, scientific validity,
        UQ, or acceptance.
        """
        retained = repository_root() / "calculations/research-monograph/periodic-2d"
        result_payload = retained.joinpath(RESULT_NAME).read_bytes()
        catalog = checksum_catalog(retained)

        documents = SUT(result_payload)
        result_digest = hashlib.sha256(result_payload).hexdigest()

        assert documents.result_payload is result_payload
        # This chain binds content identity only, not Wannier90 execution provenance.
        assert result_digest == RESULT_SHA256 == catalog[RESULT_NAME]

    def test_public_routes__share_implementation_without_retired_name(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-050-ROUTE-001.

        Requirement: Reviewed periodic-2D facades expose one defining implementation and
        do not retain the former encoded-model name or source module as an alias.

        Method: Compare three facade exports with the defining class, inspect each
        facade, and inspect the former retained-model source path.

        Oracle: The documented three-route facade contract and row-050 removal
        disposition.

        Acceptance: All supported facades expose the exact defining class object,
        none exposes ``Periodic2DWannier90BalancedCampaignModel``, and the retired
        module is absent.

        Interpretation: A pass establishes one implementation without a compatibility
        alias or forwarding source module.

        Limitations: Route identity does not authenticate any native or encoded
        scientific result.
        """
        assert balanced_facade.Periodic2DWannier90BalancedEncodedDocuments is SUT
        assert wannier90_facade.Periodic2DWannier90BalancedEncodedDocuments is SUT
        assert periodic2d_facade.Periodic2DWannier90BalancedEncodedDocuments is SUT
        for facade in (balanced_facade, wannier90_facade, periodic2d_facade):
            assert not hasattr(facade, "Periodic2DWannier90BalancedCampaignModel")
        # Repository history identifies this exact source as the retired owner.
        retired_module = (
            repository_root()
            / "python/src/ksdft2effmass/periodic2d/model/retained"
            / "wannier90_balanced.py"
        )
        assert not retired_module.exists()
