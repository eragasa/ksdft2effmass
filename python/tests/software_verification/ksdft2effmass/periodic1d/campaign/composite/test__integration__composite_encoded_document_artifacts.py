r"""Artifact-owned integration evidence for row-038 encoded documents.

Evidence profile: claim_bearing

Bounded artifact and route scope
--------------------------------
The maintained periodic-1D ``composite-input.json`` and ``composite-result.json``
files, their ``SHA256SUMS`` entries, the two canonical public import routes, and
removal of the former model and transitional campaign exports.

Runtime boundary
----------------
The tests perform bounded local reads of compact maintained files and import public
Python facades. They do not discover external data, invoke calculators, decode campaign
semantics, or reconstruct numerical channels.

Scientific exclusions
---------------------
A pass establishes retained content identity and migration-route behavior only. It does
not authenticate calculation provenance; define retained groups, frames, projectors,
or operators; establish decoded semantic correctness, scientific validation,
uncertainty quantification, or acceptance.
"""

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from ksdft2effmass.periodic1d.campaign import (
    Periodic1DCompositeEncodedDocuments as CampaignFacadeEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.composite import (
    Periodic1DCompositeEncodedDocuments,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Periodic1DCompositeEncodedDocuments


class TestPeriodic1DCompositeEncodedDocumentArtifacts:
    """Own row-038 retained-file and supported-route integration evidence."""

    repository_root = Path(__file__).resolve().parents[7]
    artifact_directory = repository_root / "calculations/research-monograph/periodic-1d"
    input_digest = "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
    result_digest = "9231057d96be5e7277e5d76d7272a9bad0a00b02996b7e989164ab619e19c02f"

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes]:
        """Read the two maintained row-038 payloads as exact bytes."""
        return (
            (cls.artifact_directory / "composite-input.json").read_bytes(),
            (cls.artifact_directory / "composite-result.json").read_bytes(),
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

    def test_retained_artifacts__preserve_exact_bytes_and_catalog_identities(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-038-ARTIFACT-001.

        Requirement: The renamed owner preserves the exact maintained composite input
        and result byte objects and their reviewed SHA-256 content identities.

        Method: Read both compact artifacts, construct the DataObject, and compare
        object identity and computed digests with the maintained checksum catalog.

        Oracle: The two reviewed SHA-256 values and their ``SHA256SUMS`` entries.

        Acceptance: Both fields retain the supplied objects and both computed and
        catalog digests equal the reviewed values.

        Interpretation: A pass establishes exact retained-byte and content-identity
        preservation across the row-038 rename.

        Limitations: Digest equality establishes content identity only, not provenance,
        decoded semantics, retained-space identity, physical adequacy, UQ, or
        acceptance.
        """
        input_payload, result_payload = self._retained_payloads()
        documents = SUT(input_payload, result_payload)
        catalog = self._catalog_digests()

        assert documents.input_payload is input_payload
        assert documents.result_payload is result_payload
        assert hashlib.sha256(documents.input_payload).hexdigest() == self.input_digest
        assert (
            hashlib.sha256(documents.result_payload).hexdigest() == self.result_digest
        )
        # Bind reviewed constants to the maintained checksum catalog, not provenance.
        assert catalog["composite-input.json"] == self.input_digest
        assert catalog["composite-result.json"] == self.result_digest

    def test_public_routes__share_implementation_without_retired_route(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-038-ROUTE-001.

        Requirement: Both canonical facades expose the defining class object while
        former model, transitional campaign, and publication exports remain absent.

        Method: Compare canonical facade exports by object identity and inspect the
        former facades and model source path.

        Oracle: The documented canonical routes and rows 038/059 removal dispositions.

        Acceptance: Both canonical exports are the defining class; former facades
        expose neither current nor retired names; and no forwarding model module exists.

        Interpretation: A pass establishes one supported implementation without a
        compatibility alias.

        Limitations: Import-route identity does not validate payload meaning or any
        campaign consumer.
        """
        import ksdft2effmass.campaigns.periodic_1d as periodic_1d
        import ksdft2effmass.campaigns.research_monograph as research_monograph
        import ksdft2effmass.periodic1d.campaign.composite as composite

        assert CampaignFacadeEncodedDocuments is SUT
        assert composite.Periodic1DCompositeEncodedDocuments is SUT
        for name in composite.__all__:
            assert getattr(composite, name) is getattr(
                __import__("ksdft2effmass.periodic1d.campaign", fromlist=[name]),
                name,
            )
            assert not hasattr(periodic_1d, name)
            assert not hasattr(research_monograph, name)
        assert not hasattr(periodic_1d, "Periodic1DCompositeCampaignModel")
        assert not hasattr(research_monograph, "Periodic1DCompositeCampaignModel")
        # Missing exports are insufficient if forwarding implementation modules survive.
        former_root = (
            self.repository_root / "python/src/ksdft2effmass/campaigns/periodic_1d"
        )
        former_paths = (
            "composite.py",
            "composite_adoption.py",
            "composite_results.py",
            "composite_verification.py",
            "composite_verified_workflows.py",
            "run/composite",
            "serialization/composite.py",
            "model/retained/composite.py",
        )
        for relative_path in former_paths:
            assert not (former_root / relative_path).exists()

    def test_public_import__does_not_initialize_transitional_campaign_package(
        self,
    ) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-059-ROUTE-002.

        Requirement: Canonical row-059 ownership must not depend transitively on the
        former underscored periodic-1D campaign package.

        Acceptance: Importing the canonical campaign facade in a fresh interpreter
        initializes no ``ksdft2effmass.campaigns.periodic_1d`` module.

        Limitations: Import independence does not establish numerical or scientific
        correctness.
        """
        script = """
import sys
import ksdft2effmass.periodic1d.campaign
loaded = [
    name
    for name in sys.modules
    if name.startswith("ksdft2effmass.campaigns.periodic_1d")
]
if loaded:
    raise SystemExit("unexpected transitional modules: " + ", ".join(sorted(loaded)))
"""
        completed = subprocess.run(
            [sys.executable, "-c", script],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )

        assert completed.returncode == 0, completed.stderr
