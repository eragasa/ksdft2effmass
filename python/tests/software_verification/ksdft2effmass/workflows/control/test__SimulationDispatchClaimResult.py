r"""Software verification of ``SimulationDispatchClaimResult``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-claim result DataObject.

Facet and represented meaning

The result distinguishes replay-verified claim candidates from denied and fail-closed
claim preparation.

Intrinsic and cross-object scope

This module verifies the exact field inventory. Variant behavior belongs to the claim
preparer owner.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence, external execution,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import SimulationDispatchClaimResult

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchClaimResult


class TestSimulationDispatchClaimResult:
    """Own software evidence for the dispatch-claim result."""

    def test_fields__public_contract__is_exact(self) -> None:
        """Keep the exact public field inventory.

        Evidence ID: SV-WFC-DISPATCH-CLAIM-RESULT-001
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "kind",
            "request",
            "authorization_result",
            "predecessor_replay_result",
            "candidate_run",
            "candidate_replay_result",
            "claimed_reservation",
            "diagnostics",
        )
