r"""Software verification of ``SimulationDispatchRequest``.

Evidence profile: routine

Bounded artifact scope: the public already-claimed dispatch request.

Facet and represented meaning

This module verifies the exact prepared request, claim check, claim record, and
outcome identity.

Intrinsic and cross-object scope

Intrinsic phase and claim discrimination belong here; full correlation belongs to
the dispatch adapter.

VVUQ and scientific exclusions

This is software verification only. It establishes no actual persistence claim,
execution, scientific validation, UQ, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    AuthorityReservationOutcomeKind,
    SimulationDispatchRequest,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchRequest


class TestSimulationDispatchRequest:
    """Own software evidence for an already-claimed dispatch request."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose all records needed before entering the effect boundary.

        Evidence ID: SV-WCI-DISPATCH-REQUEST-001

        Requirement: The request declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "execution_request",
            "claim_authorization_request",
            "claimed_reservation",
            "claim_commit_receipt",
            "outcome_identity",
            "dispatch_entry_identity",
            "dispatch_entry_revision_identity",
        )

    def test_constructor__claim__requires_claimed_reservation(self) -> None:
        """Reject a reservation that has not reached claimed state.

        Evidence ID: SV-WCI-DISPATCH-REQUEST-002

        Requirement: Dispatch requests carry an append-only claimed record.

        Acceptance: Replacing the record with reserved kind raises ``ValueError``.
        """
        request = ControlScenarioFactory.dispatch_request()
        reserved = replace(
            request.claimed_reservation,
            kind=AuthorityReservationOutcomeKind.RESERVED,
            predecessor_reservation_identity=None,
        )
        with pytest.raises(ValueError):
            replace(request, claimed_reservation=reserved)
