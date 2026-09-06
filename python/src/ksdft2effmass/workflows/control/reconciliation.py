"""Effect-free reconciliation of specialized simulation dispatch observations.

Reconciliation compares explicit runtime observations with one exact claimed dispatch.
It returns a closed result without redispatch, persistence, native-file access, result
ingress, generic colored-Petri-net firing, or scientific interpretation.  Absence of
an established observation is indeterminate rather than rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import final

from ..runs.authority import SimulationDispatchEntryReceipt
from ..runs.identities import (
    DispatchObservationRecordIdentity,
    SimulationDispatchObservationIdentity,
)
from ..runs.records import DispatchObservationKind, DispatchObservationRecord
from .dispatch import (
    SimulationDispatchOutcome,
    SimulationDispatchRequest,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchReconciliationRequest:
    """Request reconciliation of explicit observations for one claimed dispatch.

    Parameters
    ----------
    dispatch_request
        Exact already-claimed dispatch request being reconciled.
    observations
        Zero or more immutable runtime outcomes. Exact duplicate observations are
        idempotent; unequal or uncorrelated observations never select a winner.
    dispatch_entry_receipt
        Exact persistence receipt proving the newly won entry that preceded execution.
    observation_record_identity
        Caller-supplied identity for the append-only reconciliation evidence record.
    reconciliation_identity_values
        Nonempty unique lexical identities of the reads or observations establishing
        this reconciliation operation.
    """

    dispatch_request: SimulationDispatchRequest
    dispatch_entry_receipt: SimulationDispatchEntryReceipt
    observation_record_identity: DispatchObservationRecordIdentity
    observations: tuple[SimulationDispatchOutcome, ...]
    reconciliation_identity_values: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact record types and canonical reconciliation identities."""
        if type(self.dispatch_request) is not SimulationDispatchRequest:
            raise TypeError("dispatch_request must be SimulationDispatchRequest")
        if type(self.dispatch_entry_receipt) is not SimulationDispatchEntryReceipt:
            raise TypeError(
                "dispatch_entry_receipt must be SimulationDispatchEntryReceipt"
            )
        if type(self.observation_record_identity) is not (
            DispatchObservationRecordIdentity
        ):
            raise TypeError(
                "observation_record_identity must be DispatchObservationRecordIdentity"
            )
        if type(self.observations) is not tuple or any(
            type(value) is not SimulationDispatchOutcome for value in self.observations
        ):
            raise TypeError("observations must be a tuple of SimulationDispatchOutcome")
        identities = self.reconciliation_identity_values
        if type(identities) is not tuple or any(
            type(value) is not str for value in identities
        ):
            raise TypeError("reconciliation_identity_values must be a tuple of strings")
        if not identities or any(not value for value in identities):
            raise ValueError(
                "reconciliation_identity_values must contain nonempty strings"
            )
        if identities != tuple(sorted(identities)) or len(set(identities)) != len(
            identities
        ):
            raise ValueError("reconciliation_identity_values must be unique and sorted")
        dispatch = self.dispatch_request
        receipt = self.dispatch_entry_receipt
        claim_receipt = dispatch.claim_commit_receipt
        if (
            receipt.dispatch_entry_identity != dispatch.dispatch_entry_identity
            or receipt.workflow_run_identity
            != dispatch.execution_request.correlation.workflow_run_identity
            or receipt.claim_commit_receipt_identity != claim_receipt.identity
            or receipt.predecessor_revision_identity
            != claim_receipt.committed_revision_identity
            or receipt.committed_revision_identity
            != dispatch.dispatch_entry_revision_identity
            or receipt.claimed_reservation_identity
            != dispatch.claimed_reservation.identity
            or receipt.obligation_identity
            != dispatch.execution_request.obligation.identity
            or receipt.outcome_identity != dispatch.outcome_identity
        ):
            raise ValueError(
                "dispatch_entry_receipt must match the exact dispatch request"
            )


class SimulationDispatchReconciliationOutcomeKind(StrEnum):
    """Closed outcome of dispatch reconciliation."""

    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"
    CONFLICT = "conflict"
    ERROR = "error"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchReconciliationResult:
    """Record one closed effect-free dispatch reconciliation result.

    Parameters
    ----------
    kind
        Confirmed, rejected, indeterminate, conflict, or error.
    request
        Exact reconciliation request.
    outcome
        Exact finalizable runtime outcome for confirmed or rejected; absent for
        indeterminate, conflict, and error.
    observation_record
        Exact append-only evidence record produced for every reconciliation result.
    observed_outcome_identities
        Exact observation identities in supplied order. Duplicate identities are
        retained as evidence of idempotent duplicate reads.
    diagnostics
        Empty for confirmed or rejected; nonempty for indeterminate, conflict, or
        error.
    """

    kind: SimulationDispatchReconciliationOutcomeKind
    request: SimulationDispatchReconciliationRequest
    outcome: SimulationDispatchOutcome | None
    observation_record: DispatchObservationRecord
    observed_outcome_identities: tuple[SimulationDispatchObservationIdentity, ...]
    diagnostics: tuple[str, ...]

    def __post_init__(self) -> None:
        """Validate exact result fields and closed variant payloads."""
        if type(self.kind) is not SimulationDispatchReconciliationOutcomeKind:
            raise TypeError("kind must be SimulationDispatchReconciliationOutcomeKind")
        if type(self.request) is not SimulationDispatchReconciliationRequest:
            raise TypeError("request must be SimulationDispatchReconciliationRequest")
        if (
            self.outcome is not None
            and type(self.outcome) is not SimulationDispatchOutcome
        ):
            raise TypeError("outcome must be SimulationDispatchOutcome or None")
        if type(self.observation_record) is not DispatchObservationRecord:
            raise TypeError("observation_record must be DispatchObservationRecord")
        identities = self.observed_outcome_identities
        if type(identities) is not tuple or any(
            type(value) is not SimulationDispatchObservationIdentity
            for value in identities
        ):
            raise TypeError(
                "observed_outcome_identities must be a tuple of "
                "SimulationDispatchObservationIdentity"
            )
        if identities != tuple(
            observation.observation_identity
            for observation in self.request.observations
        ):
            raise ValueError(
                "observed outcome identities must match request observations"
            )
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if any(not value for value in self.diagnostics):
            raise ValueError("diagnostics must not contain empty strings")
        if len(set(self.diagnostics)) != len(self.diagnostics):
            raise ValueError("diagnostics must not contain duplicates")
        from ..runs.records import DispatchOutcomeKind

        expected_observation_kind = DispatchObservationKind(self.kind.value)
        observation = self.observation_record
        dispatch = self.request.dispatch_request
        correlation = dispatch.execution_request.correlation
        if (
            observation.identity != self.request.observation_record_identity
            or observation.workflow_run_identity != correlation.workflow_run_identity
            or observation.request_identity != correlation.request_identity
            or observation.obligation_identity
            != dispatch.execution_request.obligation.identity
            or observation.dispatch_entry_identity
            != self.request.dispatch_entry_receipt.dispatch_entry_identity
            or observation.dispatch_entry_receipt_identity
            != self.request.dispatch_entry_receipt.identity
            or observation.outcome_identity != dispatch.outcome_identity
            or observation.kind is not expected_observation_kind
            or observation.observed_outcomes != self.request.observations
            or observation.reconciliation_identity_values
            != self.request.reconciliation_identity_values
        ):
            raise ValueError(
                "observation record must close over the exact reconciliation request"
            )
        finalizable = {
            SimulationDispatchReconciliationOutcomeKind.CONFIRMED: (
                DispatchOutcomeKind.CONFIRMED
            ),
            SimulationDispatchReconciliationOutcomeKind.REJECTED: (
                DispatchOutcomeKind.REJECTED
            ),
        }
        if self.kind in finalizable:
            if (
                self.outcome is None
                or self.outcome.kind is not finalizable[self.kind]
                or any(
                    observed != self.outcome for observed in self.request.observations
                )
                or self.diagnostics
            ):
                raise ValueError(
                    "confirmed and rejected reconciliation require one exact "
                    "finalizable outcome"
                )
        elif self.outcome is not None or not self.diagnostics:
            raise ValueError(
                "nonfinal reconciliation prohibits an outcome and requires diagnostics"
            )


@final
class SimulationDispatchReconciler:
    """Reconcile explicit observations without retrying a simulation dispatch."""

    @staticmethod
    def execute(
        request: SimulationDispatchReconciliationRequest,
    ) -> SimulationDispatchReconciliationResult:
        """Reconcile zero, duplicate, conflicting, or invalid observations."""
        if type(request) is not SimulationDispatchReconciliationRequest:
            raise TypeError("request must be SimulationDispatchReconciliationRequest")
        observed_identities = tuple(
            observation.observation_identity for observation in request.observations
        )
        if not request.observations:
            kind = SimulationDispatchReconciliationOutcomeKind.INDETERMINATE
            return SimulationDispatchReconciliationResult(
                kind=kind,
                request=request,
                outcome=None,
                observation_record=SimulationDispatchReconciler._observation_record(
                    request, kind
                ),
                observed_outcome_identities=(),
                diagnostics=(
                    "no correlated dispatch observation established completion",
                ),
            )
        if any(
            not SimulationDispatchReconciler._observation_agrees(
                request.dispatch_request, observation
            )
            for observation in request.observations
        ):
            kind = SimulationDispatchReconciliationOutcomeKind.ERROR
            return SimulationDispatchReconciliationResult(
                kind=kind,
                request=request,
                outcome=None,
                observation_record=SimulationDispatchReconciler._observation_record(
                    request, kind
                ),
                observed_outcome_identities=observed_identities,
                diagnostics=(
                    "a dispatch observation does not match the claimed request",
                ),
            )
        observations_by_identity: dict[
            SimulationDispatchObservationIdentity, SimulationDispatchOutcome
        ] = {}
        for observation in request.observations:
            existing = observations_by_identity.get(observation.observation_identity)
            if existing is not None and existing != observation:
                kind = SimulationDispatchReconciliationOutcomeKind.ERROR
                return SimulationDispatchReconciliationResult(
                    kind=kind,
                    request=request,
                    outcome=None,
                    observation_record=(
                        SimulationDispatchReconciler._observation_record(request, kind)
                    ),
                    observed_outcome_identities=observed_identities,
                    diagnostics=(
                        "one dispatch observation identity names unequal content",
                    ),
                )
            observations_by_identity[observation.observation_identity] = observation
        first = request.observations[0]
        if any(observation != first for observation in request.observations[1:]):
            kind = SimulationDispatchReconciliationOutcomeKind.CONFLICT
            return SimulationDispatchReconciliationResult(
                kind=kind,
                request=request,
                outcome=None,
                observation_record=SimulationDispatchReconciler._observation_record(
                    request, kind
                ),
                observed_outcome_identities=observed_identities,
                diagnostics=("distinct correlated dispatch observations conflict",),
            )
        from ..runs.records import DispatchOutcomeKind

        kind = {
            DispatchOutcomeKind.CONFIRMED: (
                SimulationDispatchReconciliationOutcomeKind.CONFIRMED
            ),
            DispatchOutcomeKind.REJECTED: (
                SimulationDispatchReconciliationOutcomeKind.REJECTED
            ),
            DispatchOutcomeKind.INDETERMINATE: (
                SimulationDispatchReconciliationOutcomeKind.INDETERMINATE
            ),
        }[first.kind]
        finalizable = kind in {
            SimulationDispatchReconciliationOutcomeKind.CONFIRMED,
            SimulationDispatchReconciliationOutcomeKind.REJECTED,
        }
        return SimulationDispatchReconciliationResult(
            kind=kind,
            request=request,
            outcome=first if finalizable else None,
            observation_record=SimulationDispatchReconciler._observation_record(
                request, kind
            ),
            observed_outcome_identities=observed_identities,
            diagnostics=()
            if finalizable
            else ("dispatch completion remains indeterminate",),
        )

    @staticmethod
    def _observation_record(
        request: SimulationDispatchReconciliationRequest,
        kind: SimulationDispatchReconciliationOutcomeKind,
    ) -> DispatchObservationRecord:
        """Construct the exact append-only evidence record for reconciliation."""
        dispatch = request.dispatch_request
        correlation = dispatch.execution_request.correlation
        return DispatchObservationRecord(
            identity=request.observation_record_identity,
            workflow_run_identity=correlation.workflow_run_identity,
            request_identity=correlation.request_identity,
            obligation_identity=dispatch.execution_request.obligation.identity,
            dispatch_entry_identity=(
                request.dispatch_entry_receipt.dispatch_entry_identity
            ),
            dispatch_entry_receipt_identity=request.dispatch_entry_receipt.identity,
            outcome_identity=dispatch.outcome_identity,
            kind=DispatchObservationKind(kind.value),
            observed_outcomes=request.observations,
            reconciliation_identity_values=request.reconciliation_identity_values,
        )

    @staticmethod
    def _observation_agrees(
        request: SimulationDispatchRequest,
        observation: SimulationDispatchOutcome,
    ) -> bool:
        """Return whether one observation closes over the exact claimed dispatch."""
        correlation = request.execution_request.correlation
        obligation = request.execution_request.obligation
        grant_identity = request.claim_authorization_request.grant.authority_reference
        return (
            observation.identity == request.outcome_identity
            and observation.request_identity == correlation.request_identity
            and observation.workflow_run_identity == correlation.workflow_run_identity
            and observation.task_instance_identity == correlation.task_instance_identity
            and observation.activation_identity == correlation.activation_identity
            and observation.operation_identity == correlation.operation_identity
            and observation.attempt_identity == correlation.attempt_identity
            and observation.executor_identity == correlation.executor_identity
            and observation.obligation_identity == obligation.identity
            and observation.grant_identity == grant_identity.grant_identity
        )
