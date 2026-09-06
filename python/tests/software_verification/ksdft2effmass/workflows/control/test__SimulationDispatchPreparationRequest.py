r"""Software verification of ``SimulationDispatchPreparationRequest``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-preparation request DataObject.

Facet and represented meaning

The immutable request owns the exact predecessor, runtime, activation, authority,
record-identity, dependency, and optional retry inputs to effect-free preparation.

Intrinsic and cross-object scope

This module verifies the closed public field inventory. Correlation and replay belong
to ``SimulationDispatchPreparer``.

VVUQ and scientific exclusions

This is software verification only; it establishes no persistence, execution,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.control import SimulationDispatchPreparationRequest

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchPreparationRequest


class TestSimulationDispatchPreparationRequest:
    """Own software evidence for the dispatch-preparation request DataObject."""

    def test_fields__public_contract__is_exact(self) -> None:
        """Keep the closed public request field inventory.

        Evidence ID: SV-WFC-DISPATCH-PREPARATION-REQUEST-001
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "predecessor_run",
            "runtime_bundle",
            "activation",
            "authorization_request",
            "next_revision_identity",
            "started_attempt_record_identity",
            "request_correlation_identity",
            "reservation_identity",
            "creation_idempotency_identity",
            "input_dependencies",
            "retry_of_attempt_identity",
        )
