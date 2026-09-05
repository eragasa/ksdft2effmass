r"""Software verification of ``SimulationDispatchObligation``.

Evidence profile: routine

Bounded artifact scope: the public ``SimulationDispatchObligation`` contract.

Facet and represented meaning

This module verifies intrinsic represented behavior owned by
``SimulationDispatchObligation``.

Intrinsic and cross-object scope

Constructor and field invariants belong to this class. Complete cross-record replay
and package-export agreement remain with their separate owners.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import (
    SimulationDispatchObligation,
)

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchObligation


class TestSimulationDispatchObligation:
    """Own software evidence for ``SimulationDispatchObligation``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-SIMULATION-DISPATCH-OBLIGATION-001

        Requirement: ``SimulationDispatchObligation`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "workflow_run_identity",
            "workflow_run_revision_identity",
            "request_identity",
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "executor_identity",
            "grant_identity",
            "destination_identity",
            "resource_scope_identities",
            "creation_idempotency_identity",
        )
