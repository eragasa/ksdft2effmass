r"""Artifact-owned integration evidence for row-055 standalone documents.

Evidence profile: claim_bearing

These tests authenticate maintained compact sources and reconstruct bounded retained
relationships. They do not access external native files or establish convergence,
scientific validation, uncertainty quantification, or acceptance.
"""

import hashlib
from pathlib import Path

import pytest

from ksdft2effmass import periodic2d
from ksdft2effmass.periodic2d.run import wannier90
from ksdft2effmass.periodic2d.run.wannier90 import optimizer_basin
from ksdft2effmass.periodic2d.run.wannier90.optimizer_basin import standalone

pytestmark = [pytest.mark.software_verification, pytest.mark.integration]


class TestPeriodic2DOptimizerStandaloneArtifacts:
    """Own artifact-correlated evidence for crosswalk row 055."""

    def repository_root(self) -> Path:
        """Return the repository root containing retained standalone documents."""
        return Path(__file__).resolve().parents[9]

    def campaign_directory(self) -> Path:
        """Return the maintained optimizer-basin calculation directory."""
        return (
            self.repository_root()
            / "calculations/research-monograph/periodic-2d-optimizer-basin"
        )

    def documents(self) -> standalone.Periodic2DOptimizerStandaloneEncodedDocuments:
        """Load exact maintained proposal, gauge-design, and result bytes."""
        base = self.campaign_directory()
        return standalone.Periodic2DOptimizerStandaloneEncodedDocuments(
            base.joinpath("standalone-study-proposal.json").read_bytes(),
            base.joinpath("standalone-initial-gauges.json").read_bytes(),
            base.joinpath("standalone-result.json").read_bytes(),
        )

    def test_campaign__authenticates_and_reconstructs_retained_negative_result(
        self,
    ) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-ARTIFACT-001.

        Requirement: Exact compact sources reconstruct all initial and continuation
        transitions, group basins, controls, and the preserved negative disposition.

        Acceptance: 256 endpoints, 120 continuations, 196 converged endpoints, and 60
        stopped endpoints pass with the exact retained result identity.
        """
        result = standalone.Periodic2DOptimizerStandaloneCampaign(
            self.documents()
        ).verify(repository_root=self.repository_root())

        assert result.passes
        assert result.endpoint_count == 256
        assert result.continuation_count == 120
        assert result.effective_converged_count == 196
        assert result.final_nonconverged_count == 60
        assert (
            result.retained_result_sha256
            == "add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a"
        )

    def test_documents__match_checksum_catalog_and_exact_identities(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-ARTIFACT-002.

        Requirement: Artifact evidence binds all three exact wires to maintained
        ``SHA256SUMS`` entries.

        Acceptance: Catalog and direct SHA-256 values agree for each owned wire.
        """
        base = self.campaign_directory()
        catalog = {
            path: digest
            for digest, path in (
                line.split(maxsplit=1)
                for line in base.joinpath("SHA256SUMS").read_text().splitlines()
                if line.strip()
            )
        }
        documents = self.documents()
        expected = (
            (
                "standalone-study-proposal.json",
                documents.proposal_payload,
                "d260475252b420d151ebfd7e276e170c1d069e4bbc7ad974d21e911dd6db3485",
            ),
            (
                "standalone-initial-gauges.json",
                documents.initial_gauges_payload,
                "34ebdb57dbcdb3cb72bb3fbc602a12b3c05b58534d1c028047578afceb1a8f4b",
            ),
            (
                "standalone-result.json",
                documents.result_payload,
                "add349df1cccd95fc35c1984a21f58d4d5b49b62ba528377ea0f4245e5d5ce9a",
            ),
        )
        for path, payload, digest in expected:
            assert hashlib.sha256(payload).hexdigest() == digest
            assert catalog[path] == digest

    def test_encoded_document__is_exposed_by_four_reviewed_facades(self) -> None:
        """Evidence ID: SV-PERIODIC-TWO-D-ROW-055-PUBLIC-001.

        Requirement: The defining encoded-document class has four explicit reviewed
        import routes without an alias to its retired model name.

        Acceptance: All four facades expose the same class object and no retired name.
        """
        expected = standalone.Periodic2DOptimizerStandaloneEncodedDocuments
        facades = (periodic2d, wannier90, optimizer_basin, standalone)
        for facade in facades:
            assert facade.Periodic2DOptimizerStandaloneEncodedDocuments is expected
            assert not hasattr(facade, "Periodic2DOptimizerStandaloneCampaignModel")
