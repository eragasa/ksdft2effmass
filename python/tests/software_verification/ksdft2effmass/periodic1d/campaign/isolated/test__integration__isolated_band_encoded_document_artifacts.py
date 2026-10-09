r"""Artifact-owned integration evidence for rows 037 and 058.

Evidence profile: claim_bearing

Bounded artifact and route scope
--------------------------------
The maintained periodic-1D ``input.json`` and ``result.json`` files, their
``SHA256SUMS`` entries, the canonical campaign and leaf import routes, and removal
of transitional source modules and facades.

Runtime boundary
----------------
The tests perform bounded local reads of compact maintained files and import public
Python facades. They do not discover external data, invoke calculators, decode campaign
semantics, or reconstruct numerical channels.

Scientific exclusions
---------------------
A pass establishes retained content identity and migration-route behavior only. It does
not authenticate calculation provenance, establish decoded semantic correctness,
scientific validation, uncertainty quantification, or acceptance.
"""

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

import ksdft2effmass.periodic1d.campaign as campaign_facade
import ksdft2effmass.periodic1d.campaign.isolated as isolated_facade
from ksdft2effmass.periodic1d.campaign import (
    Periodic1DIsolatedBandEncodedDocuments as CampaignFacadeEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.isolated import (
    Periodic1DIsolatedBandEncodedDocuments as LeafFacadeEncodedDocuments,
)
from ksdft2effmass.periodic1d.campaign.isolated.encoded_documents import (
    Periodic1DIsolatedBandEncodedDocuments,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = Periodic1DIsolatedBandEncodedDocuments


class TestPeriodic1DIsolatedBandEncodedDocumentArtifacts:
    """Own row-037 retained-file and supported-route integration evidence."""

    repository_root = Path(__file__).resolve().parents[7]
    artifact_directory = repository_root / "calculations/research-monograph/periodic-1d"
    input_digest = "ae17de790380dee76693e984b96fbb22773a40440e267d3e77b4543cafaad6fb"
    result_digest = "37a4619e3a6ebf1c8ec9fac9f4c7cb5398ffe27254003529f736987c5f0bf71c"

    @classmethod
    def _retained_payloads(cls) -> tuple[bytes, bytes]:
        """Read the two maintained row-037 payloads as exact bytes."""
        return (
            (cls.artifact_directory / "input.json").read_bytes(),
            (cls.artifact_directory / "result.json").read_bytes(),
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
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-ROW-037-ARTIFACT-001.

        Requirement: The renamed owner preserves the exact maintained isolated input
        and result byte objects and their reviewed SHA-256 content identities.

        Method: Read both compact artifacts, construct the DataObject, and compare
        object identity and computed digests with the maintained checksum catalog.

        Oracle: The two reviewed SHA-256 values and their ``SHA256SUMS`` entries.

        Acceptance: Both fields retain the supplied objects and both computed and
        catalog digests equal the reviewed values.

        Interpretation: A pass establishes exact retained-byte and content-identity
        preservation across the row-037 rename.

        Limitations: Digest equality establishes content identity only, not provenance,
        decoded semantics, convergence, physical adequacy, UQ, or acceptance.
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
        assert catalog["input.json"] == self.input_digest
        assert catalog["result.json"] == self.result_digest

    def test_public_routes__share_implementation_without_transitional_aliases(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-CAMPAIGN-ISOLATED-ROW-058-ROUTE-001.

        Requirement: Canonical campaign facades expose the defining class while the
        transitional campaign and publication facades do not preserve aliases.

        Method: Compare canonical exports by identity, inspect transitional facades,
        and check the former implementation paths.

        Oracle: The row-058 canonical-move disposition and no-alias policy.

        Acceptance: Every leaf export is identical through the campaign facade,
        neither transitional facade exposes any leaf symbol, and the former
        implementation modules are absent.

        Interpretation: A pass establishes one canonical implementation without a
        compatibility alias.

        Limitations: Import-route identity does not validate payload meaning or any
        campaign consumer.
        """
        import ksdft2effmass.campaigns.periodic_1d as transitional_campaigns
        import ksdft2effmass.campaigns.research_monograph as publication_facade

        assert CampaignFacadeEncodedDocuments is SUT
        assert LeafFacadeEncodedDocuments is SUT
        assert set(isolated_facade.__all__) <= set(campaign_facade.__all__)
        for name in isolated_facade.__all__:
            defining_owner = getattr(isolated_facade, name)
            assert getattr(campaign_facade, name) is defining_owner
            assert not hasattr(transitional_campaigns, name)
            assert not hasattr(publication_facade, name)
        former_root = (
            self.repository_root / "python/src/ksdft2effmass/campaigns/periodic_1d"
        )
        former_paths = (
            "isolated.py",
            "isolated_results.py",
            "isolated_calculation_workflows.py",
            "isolated_verification.py",
            "isolated_verified_workflows.py",
            "isolated_replay.py",
            "run/isolated",
            "serialization/isolated.py",
        )
        for relative_path in former_paths:
            assert not (former_root / relative_path).exists()

    def test_public_import__does_not_initialize_transitional_campaign_package(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC1D-CAMPAIGN-ISOLATED-ROW-058-ROUTE-002.

        Requirement: Canonical row-058 ownership must not depend transitively on the
        transitional underscored periodic-1D campaign package.

        Method: Import the canonical facade in a fresh interpreter and inspect loaded
        module names.

        Oracle: The required canonical-to-transitional dependency direction.

        Acceptance: No loaded module belongs to
        ``ksdft2effmass.campaigns.periodic_1d``.

        Interpretation: A pass establishes import-time package independence.

        Limitations: Module absence does not establish scientific correctness or
        validate any retained campaign result.
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
