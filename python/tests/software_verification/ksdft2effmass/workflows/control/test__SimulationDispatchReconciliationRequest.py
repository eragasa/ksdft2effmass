r"""Software verification of ``SimulationDispatchReconciliationRequest``.

Evidence profile: routine

Bounded artifact scope: the public dispatch-reconciliation request DataObject.

Facet and represented meaning

This module verifies exact claimed-dispatch, observation, and reconciliation-read
inputs.

Intrinsic and cross-object scope

Request types and canonical identities belong here; observation agreement belongs to
the reconciler.

VVUQ and scientific exclusions

This is software verification only. It performs no external read, execution,
scientific validation, uncertainty quantification, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows import (
    DispatchObservationRecordIdentity,
    SimulationDispatchReconciliationRequest,
)

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = SimulationDispatchReconciliationRequest


class TestSimulationDispatchReconciliationRequest:
    """Own software evidence for reconciliation inputs."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose dispatch, observations, and reconciliation identities.

        Evidence ID: SV-WCI-RECONCILIATION-REQUEST-001

        Requirement: The request declares exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "dispatch_request",
            "dispatch_entry_receipt",
            "observation_record_identity",
            "observations",
            "reconciliation_identity_values",
        )

    def test_constructor__reconciliation_identities__require_canonical_nonempty(
        self,
    ) -> None:
        """Reject empty or noncanonical reconciliation evidence.

        Evidence ID: SV-WCI-RECONCILIATION-REQUEST-002

        Requirement: Every request names nonempty, unique, lexically sorted read or
        observation identities.

        Acceptance: Empty and reversed identity tuples each raise ``ValueError``.
        """
        dispatch = ControlScenarioFactory.dispatch_request()
        with pytest.raises(ValueError):
            SUT(
                dispatch_request=dispatch,
                dispatch_entry_receipt=(
                    ControlScenarioFactory.dispatch_entry_receipt(dispatch)
                ),
                observation_record_identity=DispatchObservationRecordIdentity(
                    "observation-record.empty"
                ),
                observations=(),
                reconciliation_identity_values=(),
            )
        with pytest.raises(ValueError):
            SUT(
                dispatch_request=dispatch,
                dispatch_entry_receipt=(
                    ControlScenarioFactory.dispatch_entry_receipt(dispatch)
                ),
                observation_record_identity=DispatchObservationRecordIdentity(
                    "observation-record.reversed"
                ),
                observations=(),
                reconciliation_identity_values=("read.z", "read.a"),
            )
