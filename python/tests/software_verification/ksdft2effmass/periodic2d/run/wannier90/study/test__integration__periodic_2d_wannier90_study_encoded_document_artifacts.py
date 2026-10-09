r"""Artifact-owned row-051 Wannier90 study encoded-document evidence.

Evidence profile: claim_bearing

The tests bind maintained study input and result bytes to repository checksum-catalog
identities and verify reviewed import routes. SHA-256 establishes content identity only.
Encoded study axes, case statuses, and observations do not authenticate native files or
execution provenance, establish case completion or convergence, validate localization
or embedding choices, quantify uncertainty, or record acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic2d as periodic2d_facade
from ksdft2effmass.periodic2d.run import wannier90 as wannier90_facade
from ksdft2effmass.periodic2d.run.wannier90 import study as study_facade
from ksdft2effmass.periodic2d.run.wannier90.study import (
    Periodic2DWannier90StudyEncodedDocuments,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DWannier90StudyEncodedDocuments
INPUT_NAME = "wannier90-study-input.json"
RESULT_NAME = "wannier90-study-result.json"
INPUT_SHA256 = "0092895cf1ff970ab3275b976d365e3c4df8c3c4c2a3ad33f4d0eaf9dbf5517a"
RESULT_SHA256 = "a4a400f7610520d75f42af991b5b0eacaaaca53ac5dfd0736f072b918d092e11"


def repository_root() -> Path:
    """Return the repository root containing the maintained calculation artifacts."""
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


class TestPeriodic2DWannier90StudyEncodedDocumentArtifacts:
    """Own retained-artifact and public-route evidence for crosswalk row 051."""

    def test_retained_artifacts__preserve_bytes_and_catalog_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-051-ARTIFACT-001.

        Requirement: The renamed owner preserves maintained Wannier90 study bytes and
        their independently retained checksum-catalog identities.

        Method: Read both compact retained files and the maintained checksum catalog,
        construct the DataObject, and compare byte-object identity and SHA-256 values.

        Oracle: Two reviewed content-identity literals and independent ``SHA256SUMS``
        entries; neither artifact is treated as a numerical or scientific oracle.

        Acceptance: Stored objects are the exact bytes read from both maintained files;
        computed digests match exact expected values and both catalog entries.

        Interpretation: A pass establishes retained-byte and content-identity
        preservation across the row-051 rename.

        Limitations: Digest equality does not establish native-file presence, execution
        provenance, case completion, convergence, decoded correctness, scientific
        validity, UQ, or acceptance.
        """
        retained = repository_root() / "calculations/research-monograph/periodic-2d"
        input_payload = retained.joinpath(INPUT_NAME).read_bytes()
        result_payload = retained.joinpath(RESULT_NAME).read_bytes()
        catalog = checksum_catalog(retained)

        documents = SUT(input_payload, result_payload)
        input_digest = hashlib.sha256(input_payload).hexdigest()
        result_digest = hashlib.sha256(result_payload).hexdigest()

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        # These chains bind byte identity only, not execution or convergence claims.
        assert input_digest == INPUT_SHA256 == catalog[INPUT_NAME]
        assert result_digest == RESULT_SHA256 == catalog[RESULT_NAME]

    def test_public_routes__share_implementation_without_retired_name(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-051-ROUTE-001.

        Requirement: Reviewed periodic-2D facades expose one defining implementation and
        do not retain the former encoded-model name or source module as an alias.

        Method: Compare three facade exports with the defining class, inspect each
        facade, and inspect the former retained-model source path.

        Oracle: The documented three-route facade contract and row-051 removal
        disposition.

        Acceptance: All supported facades expose the exact defining class object, none
        exposes ``Periodic2DWannier90StudyCampaignModel``, and the retired module is
        absent.

        Interpretation: A pass establishes one implementation without a compatibility
        alias or forwarding source module.

        Limitations: Route identity does not authenticate any native or encoded
        scientific result.
        """
        assert study_facade.Periodic2DWannier90StudyEncodedDocuments is SUT
        assert wannier90_facade.Periodic2DWannier90StudyEncodedDocuments is SUT
        assert periodic2d_facade.Periodic2DWannier90StudyEncodedDocuments is SUT
        for facade in (study_facade, wannier90_facade, periodic2d_facade):
            assert not hasattr(facade, "Periodic2DWannier90StudyCampaignModel")
        # Repository history identifies this exact source as the retired owner.
        retired_module = (
            repository_root()
            / "python/src/ksdft2effmass/periodic2d/model/retained"
            / "wannier90_study.py"
        )
        assert not retired_module.exists()
