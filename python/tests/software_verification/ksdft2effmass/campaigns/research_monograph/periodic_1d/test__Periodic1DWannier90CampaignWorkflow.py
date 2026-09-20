r"""Software verification of ``Periodic1DWannier90CampaignWorkflow``.

Evidence profile: claim_bearing

Bounded artifact scope: retained Appendix G Wannier90/composite correlation.

Facet and represented meaning

Composite group controls, preconditioned Wilson-center outcomes, and identities are
included.

Intrinsic and cross-object scope

The retained result provenance and group inventories are bound to the composite input.

VVUQ and scientific exclusions

The Workflow performs no external execution, material validation, or UQ.
"""

from pathlib import Path

import pytest

from ksdft2effmass.campaigns.research_monograph import (
    Periodic1DRetainedResultKind,
    Periodic1DWannier90CampaignWorkflow,
    Periodic1DWannier90CampaignWorkflowRequest,
)

pytestmark = pytest.mark.software_verification
SUT = Periodic1DWannier90CampaignWorkflow


class TestPeriodic1DWannier90CampaignWorkflow:
    """Own retained Wannier90 Wilson campaign integration evidence."""

    def test_method__execute__correlates_preconditioned_result(self) -> None:
        """Evidence ID: SV-CAMPAIGN-PERIODIC-ONE-D-016

        Requirement: A Wannier90 result binds to its exact composite input and groups.

        Method: Execute the read-only Workflow over retained preconditioned bytes.

        Oracle: Independent SHA-256 identities and exact group inventory.

        Acceptance: Input/result hashes agree and both groups report convergence.

        Interpretation: A pass establishes retained preconditioned integration.

        Limitations: It does not reauthenticate native files or rerun Wannier90.

        Provenance: Retained Appendix G composite and preconditioned artifacts.
        """
        root = Path(__file__).resolve().parents[7]
        directory = root / "calculations/research-monograph/periodic-1d"

        result = SUT().execute(
            Periodic1DWannier90CampaignWorkflowRequest(
                (directory / "composite-input.json").read_bytes(),
                (directory / "wannier90-preconditioned-result.json").read_bytes(),
                Periodic1DRetainedResultKind.WANNIER90_PRECONDITIONED,
            )
        )

        assert result.composite_input_sha256 == (
            "2ce60a96b72747a820c68b05aa9dbe0beaecb5de03fd5e336c9c77cc7bf5fc20"
        )
        assert result.result_sha256 == (
            "c4d6d32f8a52e93c447424b49b649e63fa036117bf88a4f8af6ed4e1d270316c"
        )
        assert all(
            group.convergence_criterion_satisfied
            for group in result.campaign_result.groups
        )
