r"""Software verification of WorkflowRun control-state and decision records.

Evidence profile: routine

Bounded artifact scope: immutable WorkflowRun authority, dispatch, obligation, and
scientific-decision record families.

Facet and represented meaning

The artifact records externally supplied authority correlations, append-only
reservation and disposition state, closed dispatch observations, and no-Task
scientific-decision request and resolution values without performing effects.

Intrinsic and cross-object scope

Tests cover exact public constructor discrimination, canonical identity tuples,
append-only predecessor rules, closed outcome fields, and no-Task decision provenance.
Complete aggregate and replay correlation belongs to ``WorkflowRunReplayer``.

VVUQ and scientific exclusions

This is software verification only. It establishes no authorization, reservation,
claim, dispatch, human authentication, protected execution, scientific validation,
uncertainty quantification, or human acceptance.
"""

from dataclasses import fields, replace

import pytest

from ksdft2effmass.petrinet.colored import ColoredPetriNetTransitionIdentity
from ksdft2effmass.workflows import (
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskInstanceIdentity,
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ksdft2effmass.workflows.runs import (
    AuthorityContextIdentity,
    AuthorityReservationOutcome,
    AuthorityReservationOutcomeIdentity,
    AuthorityReservationOutcomeKind,
    BoundaryReceiptIdentity,
    DispatchCreationIdempotencyIdentity,
    DispatchDestinationIdentity,
    DispatchOutcomeKind,
    DispatchOutcomeRecord,
    DispatchOutcomeRecordIdentity,
    DispatchResourceScopeIdentity,
    ExecutionGrantIdentity,
    ExecutionGrantRevisionIdentity,
    ObligationDisposition,
    ObligationDispositionIdentity,
    ObligationDispositionKind,
    ObligationIdentity,
    RepresentedScientificDecisionIngressProducer,
    ResponseSourceIdentity,
    ResultObjectContentIdentity,
    ResultObjectReferenceIdentity,
    ResultProducerProvenanceIdentity,
    ScientificDecisionOption,
    ScientificDecisionOptionIdentity,
    ScientificDecisionRecorderIdentity,
    ScientificDecisionRequest,
    ScientificDecisionRequestIdentity,
    ScientificDecisionResolution,
    ScientificDecisionTransitionRecordIdentity,
    ScientificExecutionAuthorityReference,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutionAuthorityStateIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchObligation,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestCorrelation,
    SimulationExecutionRequestCorrelationIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttemptRecordIdentity,
    TaskFailureRecordIdentity,
    WorkflowRunRevisionIdentity,
)

pytestmark = pytest.mark.software_verification


class TestWorkflowRunControlRecords:
    """Own software evidence for WorkflowRun control and decision records."""

    def test_constructor__authority_reservation__requires_append_only_claim(
        self,
    ) -> None:
        """Require a claimed grant state to append after one exact reservation.

        Evidence ID: SV-WFR-CONTROL-001

        Requirement: Reserved and claimed authority states are distinct immutable
        records; claimed names its exact reservation predecessor and performs no effect.

        Acceptance: Reserved and successor claimed records construct, while claimed
        without a predecessor raises ``ValueError``.
        """
        reserved = self.make_reservation(
            identity="reservation.one",
            kind=AuthorityReservationOutcomeKind.RESERVED,
        )
        claimed = self.make_reservation(
            identity="reservation.two",
            kind=AuthorityReservationOutcomeKind.CLAIMED,
            predecessor=reserved.identity,
        )

        assert claimed.predecessor_reservation_identity == reserved.identity
        with pytest.raises(ValueError):
            self.make_reservation(
                identity="reservation.invalid",
                kind=AuthorityReservationOutcomeKind.CLAIMED,
            )

    def test_constructor__dispatch_outcome__enforces_closed_variants(self) -> None:
        """Prohibit fabricated results on rejected or indeterminate dispatch.

        Evidence ID: SV-WFR-CONTROL-002

        Requirement: Confirmed alone references a returned ResultObject; rejected
        references one failure; indeterminate retains reconciliation identities only.

        Acceptance: All valid variants construct and indeterminate with a result raises
        ``ValueError``.
        """
        confirmed = self.make_dispatch_outcome(
            identity="dispatch.confirmed",
            kind=DispatchOutcomeKind.CONFIRMED,
            result_reference_identity=ResultObjectReferenceIdentity("reference.one"),
        )
        rejected = self.make_dispatch_outcome(
            identity="dispatch.rejected",
            kind=DispatchOutcomeKind.REJECTED,
            failure_record_identity=TaskFailureRecordIdentity("failure.one"),
        )
        indeterminate = self.make_dispatch_outcome(
            identity="dispatch.indeterminate",
            kind=DispatchOutcomeKind.INDETERMINATE,
            reconciliation_identity_values=("dispatch-read.one",),
        )

        assert confirmed.result_reference_identity is not None
        assert rejected.failure_record_identity is not None
        assert indeterminate.reconciliation_identity_values == ("dispatch-read.one",)
        with pytest.raises(ValueError):
            self.make_dispatch_outcome(
                identity="dispatch.invalid",
                kind=DispatchOutcomeKind.INDETERMINATE,
                result_reference_identity=ResultObjectReferenceIdentity(
                    "reference.invalid"
                ),
                reconciliation_identity_values=("dispatch-read.one",),
            )

    def test_constructor__dispatch_obligation__retains_effect_free_scope(self) -> None:
        """Retain exact request and resource scope without dispatch behavior.

        Evidence ID: SV-WFR-CONTROL-003

        Requirement: A dispatch obligation is immutable pending-work state with one
        exact destination, canonical resource identities, and creation idempotency.

        Acceptance: Canonically ordered scopes construct and reversed scopes raise
        ``ValueError``.
        """
        correlation = self.make_request_correlation()
        obligation = self.make_obligation()

        assert correlation.obligation_identity == obligation.identity
        assert obligation.resource_scope_identities == (
            DispatchResourceScopeIdentity("resource.cpu"),
            DispatchResourceScopeIdentity("resource.memory"),
        )
        with pytest.raises(ValueError):
            replace(
                obligation,
                resource_scope_identities=tuple(
                    reversed(obligation.resource_scope_identities)
                ),
            )

    def test_constructor__obligation_disposition__requires_completed_predecessor(
        self,
    ) -> None:
        """Require completed disposition to preserve earlier append-only state.

        Evidence ID: SV-WFR-CONTROL-004

        Requirement: Completion appends after an exact earlier disposition and cannot
        erase or authorize redispatch of that record.

        Acceptance: Confirmed then completed records construct, while completed with no
        predecessor raises ``ValueError``.
        """
        confirmed = self.make_disposition(
            identity="disposition.one",
            kind=ObligationDispositionKind.CONFIRMED,
        )
        completed = self.make_disposition(
            identity="disposition.two",
            kind=ObligationDispositionKind.COMPLETED,
            predecessor=confirmed.identity,
        )

        assert completed.predecessor_disposition_identity == confirmed.identity
        with pytest.raises(ValueError):
            self.make_disposition(
                identity="disposition.invalid",
                kind=ObligationDispositionKind.COMPLETED,
            )

    def test_constructor__scientific_decision_request__requires_canonical_options(
        self,
    ) -> None:
        """Require exact canonical options and an exact positive definition version.

        Evidence ID: SV-WFR-CONTROL-005

        Requirement: A scientific-decision request retains one nonempty ordered option
        set and rejects booleans as integer versions.

        Acceptance: Canonical options construct; reversed options and Boolean version
        each raise their documented exception.
        """
        request = self.make_decision_request()

        assert tuple(option.identity.value for option in request.options) == (
            "option.a",
            "option.b",
        )
        with pytest.raises(ValueError):
            replace(request, options=tuple(reversed(request.options)))
        with pytest.raises(TypeError):
            replace(request, definition_version=True)

    def test_constructor__scientific_decision_resolution__owns_no_task_lineage(
        self,
    ) -> None:
        """Retain exact no-Task ingress provenance and append-only correction.

        Evidence ID: SV-WFR-CONTROL-006

        Requirement: A resolution is a ResultObject with request, verbatim response,
        direct source/authority identities, and no Task/activation/attempt fields;
        correction names and supersedes the same exact predecessor.

        Acceptance: Initial and corrected resolutions construct with no prohibited
        lineage fields, while mismatched correction references raise ``ValueError``.
        """
        initial = self.make_resolution("resolution.one")
        corrected = self.make_resolution(
            "resolution.two",
            predecessor=initial.identity,
            supersedes=initial.identity,
        )
        prohibited_fields = {
            "task_instance_identity",
            "activation_identity",
            "operation_identity",
            "attempt_identity",
            "production_identity",
        }

        assert prohibited_fields.isdisjoint(
            field.name for field in fields(RepresentedScientificDecisionIngressProducer)
        )
        assert corrected.predecessor_resolution_identity == initial.identity
        with pytest.raises(ValueError):
            self.make_resolution(
                "resolution.invalid",
                predecessor=initial.identity,
                supersedes=ResultObjectIdentity("resolution.other"),
            )

    @staticmethod
    def make_authority_reference() -> ScientificExecutionAuthorityReference:
        """Construct one exact externally supplied authority reference."""
        return ScientificExecutionAuthorityReference(
            grant_identity=ExecutionGrantIdentity("grant.one"),
            grant_revision_identity=ExecutionGrantRevisionIdentity(
                "grant-revision.one"
            ),
            snapshot_identity=ScientificExecutionAuthoritySnapshotIdentity(
                "authority-snapshot.one"
            ),
            state_identity=ScientificExecutionAuthorityStateIdentity(
                "authority-state.unused"
            ),
        )

    @classmethod
    def make_reservation(
        cls,
        *,
        identity: str,
        kind: AuthorityReservationOutcomeKind,
        predecessor: AuthorityReservationOutcomeIdentity | None = None,
    ) -> AuthorityReservationOutcome:
        """Construct one reservation-state record for variant evidence."""
        return AuthorityReservationOutcome(
            identity=AuthorityReservationOutcomeIdentity(identity),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            workflow_run_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            authority_reference=cls.make_authority_reference(),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.one")
            ),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.started"),
            obligation_identity=ObligationIdentity("obligation.one"),
            expected_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            kind=kind,
            predecessor_reservation_identity=predecessor,
        )

    @staticmethod
    def make_request_correlation() -> SimulationExecutionRequestCorrelation:
        """Construct one exact request-to-WorkflowRun correlation."""
        return SimulationExecutionRequestCorrelation(
            identity=SimulationExecutionRequestCorrelationIdentity("correlation.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.started"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            authorization_result_identity=(
                SimulationExecutionAuthorizationResultIdentity("authorization.one")
            ),
            input_result_reference_identities=(),
        )

    @staticmethod
    def make_obligation() -> SimulationDispatchObligation:
        """Construct one immutable synthetic dispatch obligation."""
        return SimulationDispatchObligation(
            identity=ObligationIdentity("obligation.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            workflow_run_revision_identity=WorkflowRunRevisionIdentity("revision.one"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            destination_identity=DispatchDestinationIdentity("destination.one"),
            resource_scope_identities=(
                DispatchResourceScopeIdentity("resource.cpu"),
                DispatchResourceScopeIdentity("resource.memory"),
            ),
            creation_idempotency_identity=DispatchCreationIdempotencyIdentity(
                "dispatch-create.one"
            ),
        )

    @staticmethod
    def make_dispatch_outcome(
        *,
        identity: str,
        kind: DispatchOutcomeKind,
        result_reference_identity: ResultObjectReferenceIdentity | None = None,
        failure_record_identity: TaskFailureRecordIdentity | None = None,
        reconciliation_identity_values: tuple[str, ...] = (),
    ) -> DispatchOutcomeRecord:
        """Construct one specialized dispatch observation for variant evidence."""
        return DispatchOutcomeRecord(
            identity=DispatchOutcomeRecordIdentity(identity),
            envelope_identity=SimulationDispatchOutcomeIdentity(f"envelope.{identity}"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            task_instance_identity=TaskInstanceIdentity("instance.one"),
            activation_identity=TaskActivationIdentity("activation.one"),
            operation_identity=OperationIdentity("operation.one"),
            attempt_identity=AttemptIdentity("attempt.one"),
            executor_identity=ScientificExecutorIdentity("executor.one"),
            obligation_identity=ObligationIdentity("obligation.one"),
            grant_identity=ExecutionGrantIdentity("grant.one"),
            kind=kind,
            result_reference_identity=result_reference_identity,
            failure_record_identity=failure_record_identity,
            reconciliation_identity_values=reconciliation_identity_values,
        )

    @staticmethod
    def make_disposition(
        *,
        identity: str,
        kind: ObligationDispositionKind,
        predecessor: ObligationDispositionIdentity | None = None,
    ) -> ObligationDisposition:
        """Construct one append-only obligation disposition."""
        return ObligationDisposition(
            identity=ObligationDispositionIdentity(identity),
            obligation_identity=ObligationIdentity("obligation.one"),
            request_identity=SimulationExecutionRequestIdentity("request.one"),
            dispatch_outcome_record_identity=DispatchOutcomeRecordIdentity(
                "dispatch.confirmed"
            ),
            attempt_record_identity=TaskAttemptRecordIdentity("attempt.one.confirmed"),
            kind=kind,
            predecessor_disposition_identity=predecessor,
        )

    @staticmethod
    def make_decision_request() -> ScientificDecisionRequest:
        """Construct one canonical synthetic scientific-decision request."""
        return ScientificDecisionRequest(
            identity=ScientificDecisionRequestIdentity("decision-request.one"),
            question="Select the represented synthetic branch.",
            options=(
                ScientificDecisionOption(
                    ScientificDecisionOptionIdentity("option.a"), "A"
                ),
                ScientificDecisionOption(
                    ScientificDecisionOptionIdentity("option.b"), "B"
                ),
            ),
            declared_scope="synthetic software-verification branch",
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            affected_task_instance_identity=TaskInstanceIdentity("instance.one"),
            affected_transition_identity=ColoredPetriNetTransitionIdentity(
                "decision.ingress"
            ),
            required_response_source_identity=ResponseSourceIdentity("source.one"),
            required_authority_context_identity=AuthorityContextIdentity(
                "authority-context.one"
            ),
            definition_identity="scientific-decision-request.v1",
            definition_version=1,
        )

    @staticmethod
    def make_resolution(
        identity: str,
        *,
        predecessor: ResultObjectIdentity | None = None,
        supersedes: ResultObjectIdentity | None = None,
    ) -> ScientificDecisionResolution:
        """Construct one initial or correcting no-Task resolution."""
        resolution_identity = ResultObjectIdentity(identity)
        source_identity = ResponseSourceIdentity("source.one")
        authority_identity = AuthorityContextIdentity("authority-context.one")
        request_identity = ScientificDecisionRequestIdentity("decision-request.one")
        producer = RepresentedScientificDecisionIngressProducer(
            identity=ResultProducerProvenanceIdentity(f"producer.{identity}"),
            workflow_identity=WorkflowIdentity("workflow.one"),
            workflow_run_identity=WorkflowRunIdentity("run.one"),
            request_identity=request_identity,
            transition_record_identity=ScientificDecisionTransitionRecordIdentity(
                f"transition.{identity}"
            ),
            recorder_identity=ScientificDecisionRecorderIdentity("recorder.v1"),
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            resolution_identity=resolution_identity,
        )
        return ScientificDecisionResolution(
            identity=resolution_identity,
            content_identity=ResultObjectContentIdentity(f"content.{identity}"),
            request_identity=request_identity,
            verbatim_response="A",
            normalized_option_identity=ScientificDecisionOptionIdentity("option.a"),
            response_source_identity=source_identity,
            authority_context_identity=authority_identity,
            boundary_receipt_identity=BoundaryReceiptIdentity("receipt.one"),
            predecessor_resolution_identity=predecessor,
            supersedes_resolution_identity=supersedes,
            producer_provenance=producer,
        )
