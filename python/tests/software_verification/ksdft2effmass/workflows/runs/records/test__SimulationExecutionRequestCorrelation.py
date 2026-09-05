r"""Software verification of ``SimulationExecutionRequestCorrelation``.

Evidence profile: routine

Bounded artifact scope: the public ``SimulationExecutionRequestCorrelation`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``SimulationExecutionRequestCorrelation``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import SimulationExecutionRequestCorrelation

pytestmark = pytest.mark.software_verification
SUT = SimulationExecutionRequestCorrelation


class TestSimulationExecutionRequestCorrelation:
    """Own software evidence for ``SimulationExecutionRequestCorrelation``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-SIMULATION-EXECUTION-REQUEST-CORRELATION-001

        Requirement: ``SimulationExecutionRequestCorrelation`` declares exactly
        its documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "workflow_run_identity",
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "attempt_record_identity",
            "request_identity",
            "executor_identity",
            "obligation_identity",
            "grant_identity",
            "authorization_result_identity",
            "input_result_reference_identities",
        )
