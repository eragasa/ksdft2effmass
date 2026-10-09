r"""Artifact-owned row-049 phase-sweep encoded-document integration evidence.

Evidence profile: claim_bearing

The tests bind maintained periodic-2D phase-sweep input and result bytes to repository
checksum-catalog identities and verify reviewed import routes. SHA-256 establishes
content identity only. Encoded axes and expected observations are retained campaign
content, not qualified numerical oracles, and do not establish sample availability,
execution provenance, decoded correctness, topology, convergence, scientific validity,
uncertainty, or acceptance.
"""

import hashlib
from pathlib import Path

import pytest

import ksdft2effmass.periodic2d as periodic2d_facade
from ksdft2effmass.periodic2d.run.topological import phase_sweep as phase_sweep_facade
from ksdft2effmass.periodic2d.run.topological.phase_sweep import (
    Periodic2DTopologicalPhaseSweepEncodedDocuments,
)

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]
SUT = Periodic2DTopologicalPhaseSweepEncodedDocuments
INPUT_SHA256 = "f8b535250ede7efc79b96682979b72472791172d0662d41a490f8bad2a0a553c"
RESULT_SHA256 = "298532cba30f56518c6578feb187704ad8f031eabdeae468b7ad067d0b286b11"


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


class TestPeriodic2DTopologicalPhaseSweepEncodedDocumentArtifacts:
    """Own retained-artifact and public-route evidence for crosswalk row 049."""

    def test_retained_artifacts__preserve_bytes_and_catalog_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-049-ARTIFACT-001.

        Requirement: The renamed owner preserves maintained phase-sweep bytes and their
        independently retained checksum-catalog identities.

        Method: Read both compact retained files and the maintained checksum catalog,
        construct the DataObject, and compare byte-object identity and SHA-256 values.

        Oracle: Two reviewed content-identity literals and independent ``SHA256SUMS``
        entries; neither artifact is treated as a numerical oracle.

        Acceptance: Stored objects are the exact bytes read from both maintained files;
        computed digests match exact expected values and both catalog entries.

        Interpretation: A pass establishes retained-byte and content-identity
        preservation across the row-049 rename.

        Limitations: Digest equality and encoded expected observations do not establish
        sample availability, provenance, decoded correctness, topology, convergence,
        scientific validity, UQ, or acceptance.
        """
        retained = repository_root() / "calculations/research-monograph/periodic-2d"
        input_payload = retained.joinpath(
            "topological-phase-sweep-input.json"
        ).read_bytes()
        result_payload = retained.joinpath(
            "topological-phase-sweep-result.json"
        ).read_bytes()
        catalog = checksum_catalog(retained)

        documents = SUT(input_payload, result_payload)
        input_digest = hashlib.sha256(input_payload).hexdigest()
        result_digest = hashlib.sha256(result_payload).hexdigest()

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        # These comparisons bind content identity only, not scientific correctness.
        assert (
            input_digest
            == INPUT_SHA256
            == catalog["topological-phase-sweep-input.json"]
        )
        assert (
            result_digest
            == RESULT_SHA256
            == catalog["topological-phase-sweep-result.json"]
        )

    def test_public_routes__share_implementation_without_retired_name(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-049-ROUTE-001.

        Requirement: Reviewed periodic-2D facades expose one defining implementation and
        do not retain the former encoded-model name or source module as an alias.

        Method: Compare both facade exports with the defining class, inspect each
        facade, and inspect the former retained-model source path.

        Oracle: The documented two-route facade contract and row-049 removal
        disposition.

        Acceptance: Both supported facades expose the exact defining class object,
        neither exposes ``Periodic2DTopologicalPhaseSweepCampaignModel``, and the
        retired module is absent.

        Interpretation: A pass establishes one implementation without a compatibility
        alias or forwarding source module.

        Limitations: Route identity does not decode, qualify, or validate either
        payload.
        """
        assert phase_sweep_facade.Periodic2DTopologicalPhaseSweepEncodedDocuments is SUT
        assert periodic2d_facade.Periodic2DTopologicalPhaseSweepEncodedDocuments is SUT
        for facade in (phase_sweep_facade, periodic2d_facade):
            assert not hasattr(facade, "Periodic2DTopologicalPhaseSweepCampaignModel")
        # Test the actual pre-rename owner recorded by repository history.
        retired_module = (
            repository_root()
            / "python/src/ksdft2effmass/periodic2d/model/retained"
            / "topological_phase_sweep.py"
        )
        assert not retired_module.exists()
