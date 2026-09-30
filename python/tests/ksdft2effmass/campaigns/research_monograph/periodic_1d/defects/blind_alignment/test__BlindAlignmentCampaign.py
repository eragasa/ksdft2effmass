# ruff: noqa: E501
r"""Software verification for ``BlindAlignmentCampaign``.

Evidence profile: claim_bearing

Facet and represented meaning
-----------------------------
The module owns the small public façade that encapsulates version-one documents and
delegates retained decoding, complete campaign calculation, and identity correlation.

Intrinsic and cross-object scope
--------------------------------
The façade resolves authenticated retained baseline artifacts and is therefore marked
as integration evidence. Lower-level records and Actionizers are exercised through the
encapsulated route rather than aggregated at the package boundary.

VVUQ and scientific exclusions
------------------------------
A pass establishes deterministic synthetic-campaign reconstruction and retained
compatibility. It does not validate silicon, establish transferability, or perform
uncertainty quantification.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects import (
    blind_alignment as blind_alignment_package,
)
from ksdft2effmass.campaigns.research_monograph.periodic_1d.defects.blind_alignment import (
    BlindAlignmentCampaign,
    BlindAlignmentCampaignModel,
)

pytestmark = [pytest.mark.integration, pytest.mark.software_verification]
SUT = BlindAlignmentCampaign


class TestBlindAlignmentCampaign:
    """Own the encapsulated public blind-alignment campaign evidence."""

    @staticmethod
    def repository_root() -> Path:
        """Return the repository containing retained campaign artifacts."""
        return Path(__file__).resolve().parents[8]

    def campaign(self) -> BlindAlignmentCampaign:
        """Construct the façade from exact retained documents and an absolute root."""
        root = self.repository_root()
        calculation = root / (
            "calculations/research-monograph/impurity-defect-1d-blind-alignment"
        )
        return SUT(
            BlindAlignmentCampaignModel(
                input_document=(calculation / "input.json").read_bytes(),
                retained_result_document=(calculation / "result.json").read_bytes(),
                repository_root=root,
            )
        )

    def test_method__correlate_retained__reconstructs_complete_result(self) -> None:
        """Evidence ID: NV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-002.

        Requirement: The public façade must reconstruct every version-one case behind
        its encapsulated model and correlate with the retained synthetic result.

        Method: Construct the façade from exact retained bytes and invoke only its
        retained-result and retained-correlation methods.

        Oracle: The immutable retained version-one result and authenticated source
        identities.

        Acceptance: All six case-family counts agree, semantic and canonical-byte
        correlations are true, and both SHA-256 identities agree exactly.

        Interpretation: A pass establishes encapsulated deterministic reconstruction
        of the bounded synthetic blind-alignment campaign under retained controls.

        Limitations: Retained-provenance compatibility reconstruction does not claim
        that the current test ran under the historical adapter. Agreement does not
        validate material physics or uncertainty.
        """
        campaign = self.campaign()

        retained = campaign.retained_result()
        correlation = campaign.correlate_retained()

        assert len(retained.exact_full_rank_cases) == 2
        assert len(retained.noise_sweep) == 6
        assert len(retained.stopping_cases) == 5
        assert len(retained.debugging_diagnostics.conditioning_boundary) == 6
        assert len(retained.debugging_diagnostics.principal_angle_boundary) == 5
        assert len(retained.debugging_diagnostics.energy_anchor_boundary) == 7
        assert correlation.semantic_equal
        assert correlation.canonical_bytes_equal
        assert correlation.calculated_sha256 == correlation.retained_sha256

    def test_package__public_surface__exports_only_campaign_and_model(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-DEFECT-020.

        Requirement: The package boundary must remain a curated encapsulation surface,
        not an aggregate of internal records and Actionizers.

        Method: Inspect the package's explicit export inventory.

        Oracle: The accepted façade-plus-model public boundary.

        Acceptance: ``__all__`` contains exactly the campaign and model names.

        Interpretation: A pass establishes the deliberately narrow supported route.

        Limitations: Defining modules remain importable for maintained implementation
        and evidence code; importability alone does not make them supported API routes.
        """
        assert blind_alignment_package.__all__ == [
            "BlindAlignmentCampaign",
            "BlindAlignmentCampaignModel",
        ]
