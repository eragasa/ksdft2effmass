r"""Software verification of ``ScientificExecutionAuthorityGrant``.

Evidence profile: routine

Bounded artifact scope: the public one-dispatch authority-grant DataObject.

Facet and represented meaning

This module verifies exact grant scope and intrinsic lifecycle discrimination.

Intrinsic and cross-object scope

Grant field and state invariants belong here; operation compatibility belongs to the
authorizer.

VVUQ and scientific exclusions

This is software verification only. It issues no authority, performs no reservation
or execution, and establishes no scientific validation, UQ, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.workflows import (
    ScientificExecutionAuthorityGrant,
    ScientificExecutionGrantState,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = ScientificExecutionAuthorityGrant


class TestScientificExecutionAuthorityGrant:
    """Own software evidence for one-dispatch grant state."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact dispatch and input scope.

        Evidence ID: SV-WCI-AUTHORITY-GRANT-001

        Requirement: The grant declares exactly the documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "authority_reference",
            "authority_source_identity",
            "issuer_identity",
            "request_identity",
            "workflow_run_identity",
            "task_definition_identity",
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "executor_identity",
            "destination_identity",
            "resource_scope_identities",
            "input_result_reference_identities",
            "input_artifact_entry_identities",
            "valid_from",
            "valid_until",
            "state",
            "reserved_obligation_identity",
        )

    def test_constructor__grant_state__requires_exact_obligation_variant(self) -> None:
        """Bind reserved and claimed grants to one obligation only.

        Evidence ID: SV-WCI-AUTHORITY-GRANT-002

        Requirement: Reserved and claimed grants require an obligation while unused
        grants prohibit one.

        Acceptance: Valid unused and reserved grants construct; removing the reserved
        obligation raises ``ValueError``.
        """
        unused = ControlScenarioFactory.grant(
            state=ScientificExecutionGrantState.UNUSED
        )
        reserved = ControlScenarioFactory.grant(
            state=ScientificExecutionGrantState.RESERVED
        )
        assert unused.reserved_obligation_identity is None
        assert reserved.reserved_obligation_identity is not None
        with pytest.raises(ValueError):
            replace(reserved, reserved_obligation_identity=None)
