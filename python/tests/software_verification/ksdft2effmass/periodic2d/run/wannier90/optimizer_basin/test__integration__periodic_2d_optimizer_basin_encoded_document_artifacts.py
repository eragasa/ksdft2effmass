r"""Artifact-owned row-052 optimizer-basin encoded-document evidence.

Evidence profile: claim_bearing

The tests bind maintained optimizer-basin input and result bytes to repository
checksum-catalog identities and verify reviewed import routes. SHA-256 establishes
content identity only. Encoded gauges, basin partitions, completion fields, and the
retained negative convergence disposition do not by themselves authenticate execution
or native files, validate optimizer behavior, prove convergence or a global optimum,
quantify uncertainty, or record scientific acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic2d as periodic2d_facade
from ksdft2effmass.periodic2d.run import wannier90 as wannier90_facade
from ksdft2effmass.periodic2d.run.wannier90 import (
    optimizer_basin as optimizer_basin_facade,
)
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import (
    Periodic2DOptimizerBasinEncodedDocuments,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DOptimizerBasinEncodedDocuments
INPUT_NAME = "study-input.json"
RESULT_NAME = "result.json"
INPUT_SHA256 = "c2e0f601198be51d56da1ccacd03251491480e6602eb5a32633b7be6efd3fa6f"
RESULT_SHA256 = "d3074c086f6d8071bb608cde25b5605b6898b55b749b27c32ae735256299ff85"


def repository_root() -> Path:
    """Return the repository root containing the maintained calculation artifacts."""
    return Path(__file__).resolve().parents[8]


def checksum_catalog(directory: Path) -> dict[str, str]:
    """Return unique logical-name to SHA-256 entries from the retained catalog.

    Parameters
    ----------
    directory
        Maintained optimizer-basin directory containing ``SHA256SUMS``.

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


class TestPeriodic2DOptimizerBasinEncodedDocumentArtifacts:
    """Own retained-artifact and public-route evidence for crosswalk row 052."""

    def test_retained_artifacts__preserve_bytes_and_catalog_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-ARTIFACT-001.

        Requirement: The renamed owner preserves maintained optimizer-basin bytes and
        their independently retained checksum-catalog identities.

        Method: Read both compact retained files and the maintained checksum catalog,
        construct the DataObject, and compare byte-object identity and SHA-256 values.

        Oracle: Two reviewed content-identity literals and independent ``SHA256SUMS``
        entries; neither artifact is treated as a numerical or scientific oracle.

        Acceptance: Stored objects are the exact bytes read from both maintained files;
        computed digests match exact expected values and both catalog entries.

        Interpretation: A pass establishes retained-byte and content-identity
        preservation across the row-052 rename.

        Limitations: Digest equality does not establish native-file presence, execution
        provenance, optimizer validity, convergence, a global optimum, decoded
        correctness, scientific validity, UQ, or acceptance.
        """
        retained = (
            repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )
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
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-052-ROUTE-001.

        Requirement: Reviewed periodic-2D facades expose one defining implementation and
        do not retain the former encoded-model name or source module as an alias.

        Method: Compare three facade exports with the defining class, inspect each
        facade, and inspect the former retained-model source path.

        Oracle: The documented three-route facade contract and row-052 removal
        disposition.

        Acceptance: All supported facades expose the exact defining class object, none
        exposes ``Periodic2DOptimizerBasinCampaignModel``, and the retired module is
        absent.

        Interpretation: A pass establishes one implementation without a compatibility
        alias or forwarding source module.

        Limitations: Route identity does not authenticate any native or encoded
        scientific result.
        """
        assert optimizer_basin_facade.Periodic2DOptimizerBasinEncodedDocuments is SUT
        assert wannier90_facade.Periodic2DOptimizerBasinEncodedDocuments is SUT
        assert periodic2d_facade.Periodic2DOptimizerBasinEncodedDocuments is SUT
        for facade in (optimizer_basin_facade, wannier90_facade, periodic2d_facade):
            assert not hasattr(facade, "Periodic2DOptimizerBasinCampaignModel")
        # Repository history identifies this exact source as the retired owner.
        retired_module = (
            repository_root()
            / "python/src/ksdft2effmass/periodic2d/model/retained"
            / "optimizer_basin.py"
        )
        assert not retired_module.exists()
