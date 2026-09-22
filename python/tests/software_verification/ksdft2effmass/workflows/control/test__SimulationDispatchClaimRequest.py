r"""Software verification of ``SimulationDispatchClaimRequest``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-claim request DataObject.

Facet and represented meaning

The immutable request owns exact prepared state, runtime, claim authorization, and
caller-supplied successor identities.

Intrinsic and cross-object scope

This module verifies the closed field inventory. Candidate semantics belong to the
claim preparer owner.

VVUQ and scientific exclusions

This is software verification only and establishes no persistence, external execution,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import SimulationDispatchClaimRequest

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchClaimRequest


class TestSimulationDispatchClaimRequest:
    """Own software evidence for the dispatch-claim request."""

    def test_fields__public_contract__is_exact(self) -> None:
        """Keep the exact public field inventory.

        Evidence ID: SV-WFC-DISPATCH-CLAIM-REQUEST-001
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "predecessor_run",
            "runtime_bundle",
            "execution_request",
            "claim_authorization_request",
            "next_revision_identity",
            "claimed_reservation_identity",
        )
