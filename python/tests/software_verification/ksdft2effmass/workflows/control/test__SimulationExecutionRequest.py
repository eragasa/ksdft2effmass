r"""Software verification of ``SimulationExecutionRequest``.

Evidence profile: routine

Bounded artifact scope: the public prepared simulation execution request.

Facet and represented meaning

This module verifies closure of preparation authorization, request correlation, and
durable obligation.

Intrinsic and cross-object scope

The request owns exact preparation joins. Persistence and execution remain separate.

VVUQ and scientific exclusions

This is software verification only. It performs no persistence, calculation,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    SimulationExecutionAuthorizationOutcomeKind,
    SimulationExecutionRequest,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationExecutionRequest


class TestSimulationExecutionRequest:
    """Own software evidence for the prepared execution request."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose correlation, obligation, and preparation authorization.

        Evidence ID: SV-WCI-EXECUTION-REQUEST-001

        Requirement: The request declares exactly its three documented records.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "correlation",
            "obligation",
            "preparation_authorization",
        )

    def test_constructor__preparation__requires_authorized_unused_grant(self) -> None:
        """Reject non-authorized preparation state.

        Evidence ID: SV-WCI-EXECUTION-REQUEST-002

        Requirement: A prepared request closes only over authorized unused authority.

        Acceptance: Replacing the authorization with a denied variant raises
        ``ValueError``.
        """
        request = ControlScenarioFactory.execution_request()
        denied = replace(
            request.preparation_authorization,
            kind=SimulationExecutionAuthorizationOutcomeKind.DENIED,
            authorized_grant_state=None,
            diagnostics=("denied",),
        )
        with pytest.raises(ValueError):
            replace(request, preparation_authorization=denied)
