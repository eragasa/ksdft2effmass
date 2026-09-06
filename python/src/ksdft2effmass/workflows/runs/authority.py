"""Run-owned immutable scientific-execution authority contracts.

The records in this module represent externally issued one-dispatch authority and
an already verified view of its authority source.  The authorizer compares those
immutable records with one exact simulation operation.  It does not authenticate
transport messages, issue or broaden grants, reserve or claim authority, persist
state, invoke a calculator, or establish scientific acceptance.

Times are timezone-aware UTC :class:`datetime.datetime` values.  Authorization is
an exact software-control decision under supplied state; it does not validate the
scientific suitability of a calculation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

from ..artifacts import ArtifactManifestEntryIdentity
from ..model import (
    AttemptIdentity,
    OperationIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
    WorkflowRunIdentity,
)
from .identities import (
    AuthorityReservationOutcomeIdentity,
    DispatchDestinationIdentity,
    DispatchResourceScopeIdentity,
    ObligationIdentity,
    ResultObjectReferenceIdentity,
    ScientificExecutionAuthoritySnapshotIdentity,
    ScientificExecutorIdentity,
    SimulationDispatchEntryIdentity,
    SimulationDispatchEntryReceiptIdentity,
    SimulationDispatchOutcomeIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestIdentity,
    WorkflowRunClaimCommitReceiptIdentity,
    WorkflowRunRevisionIdentity,
)
from .records import ScientificExecutionAuthorityReference


class ScientificExecutionAuthorityVerificationKind(StrEnum):
    """Closed status of one authority-snapshot verification check.

    Attributes
    ----------
    VERIFIED
        The check was completed successfully under the identified resolver.
    FAILED
        The check established that the supplied authority state is unacceptable.
    INDETERMINATE
        The check could not establish either success or failure.
    """

    VERIFIED = "verified"
    FAILED = "failed"
    INDETERMINATE = "indeterminate"


class ScientificExecutionGrantState(StrEnum):
    """Closed represented state of one externally issued execution grant.

    Attributes
    ----------
    UNUSED
        The grant has not been reserved for an obligation.
    RESERVED
        The grant is reserved for exactly one identified obligation.
    CLAIMED
        The reserved grant has been claimed and consumed for authorization.
    REVOKED
        The external authority source represents the grant as revoked.
    """

    UNUSED = "unused"
    RESERVED = "reserved"
    CLAIMED = "claimed"
    REVOKED = "revoked"


@dataclass(frozen=True, slots=True, kw_only=True)
class ScientificExecutionAuthoritySnapshot:
    """Represent an immutable verified view of one authority source.

    Parameters
    ----------
    identity
        Exact authority-snapshot identity.
    source_identity, issuer_identity, trust_configuration_identity
        Nonempty identities of the authority source, grant issuer, and trust
        configuration used by the external resolver.
    content_verification_identity, authentication_verification_identity
        Nonempty identities of the content and authentication checks.
    predecessor_closure_identity, revocation_closure_identity
        Nonempty identities of the predecessor-chain and revocation checks.
    content_verification, authentication_verification
        Closed outcomes of content and authentication checks.
    predecessor_closure, revocation_closure
        Closed outcomes of predecessor and revocation closure checks.
    valid_from, valid_until
        Inclusive authority-source validity interval as timezone-aware UTC values.
    verified_at
        UTC instant at which the represented checks were performed.
    fresh_until
        Inclusive UTC freshness bound.  It must lie between ``verified_at`` and
        ``valid_until``.
    resolver_implementation_identity
        Nonempty exact identity of the external resolver implementation.

    Notes
    -----
    The object records supplied verification outcomes.  It performs no
    cryptographic verification or authority-source access.
    """

    identity: ScientificExecutionAuthoritySnapshotIdentity
    source_identity: str
    issuer_identity: str
    trust_configuration_identity: str
    content_verification_identity: str
    authentication_verification_identity: str
    predecessor_closure_identity: str
    revocation_closure_identity: str
    content_verification: ScientificExecutionAuthorityVerificationKind
    authentication_verification: ScientificExecutionAuthorityVerificationKind
    predecessor_closure: ScientificExecutionAuthorityVerificationKind
    revocation_closure: ScientificExecutionAuthorityVerificationKind
    valid_from: datetime
    valid_until: datetime
    verified_at: datetime
    fresh_until: datetime
    resolver_implementation_identity: str

    def __post_init__(self) -> None:
        """Validate intrinsic snapshot representation and UTC bounds."""
        if type(self.identity) is not ScientificExecutionAuthoritySnapshotIdentity:
            raise TypeError(
                "identity must be ScientificExecutionAuthoritySnapshotIdentity"
            )
        for name in (
            "source_identity",
            "issuer_identity",
            "trust_configuration_identity",
            "content_verification_identity",
            "authentication_verification_identity",
            "predecessor_closure_identity",
            "revocation_closure_identity",
            "resolver_implementation_identity",
        ):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")
        for name in (
            "content_verification",
            "authentication_verification",
            "predecessor_closure",
            "revocation_closure",
        ):
            if type(getattr(self, name)) is not (
                ScientificExecutionAuthorityVerificationKind
            ):
                raise TypeError(
                    f"{name} must be ScientificExecutionAuthorityVerificationKind"
                )
        for name in ("valid_from", "valid_until", "verified_at", "fresh_until"):
            value = getattr(self, name)
            if type(value) is not datetime:
                raise TypeError(f"{name} must be a datetime")
            if value.tzinfo is None or value.utcoffset() != timedelta(0):
                raise ValueError(f"{name} must be timezone-aware UTC")
        if not (
            self.valid_from <= self.verified_at <= self.fresh_until <= self.valid_until
        ):
            raise ValueError(
                "snapshot times must satisfy valid_from <= verified_at <= "
                "fresh_until <= valid_until"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class ScientificExecutionAuthorityGrant:
    """Represent one externally issued grant for one exact simulation dispatch.

    Parameters
    ----------
    authority_reference
        Exact grant, revision, snapshot, and externally supplied state identities.
    authority_source_identity, issuer_identity
        Nonempty identities that must agree with the verified snapshot.
    request_identity, workflow_run_identity
        Exact simulation request and represented Workflow run.
    task_definition_identity, task_instance_identity, activation_identity
        Exact reusable Task, run-scoped Task instance, and selected activation.
    operation_identity, attempt_identity
        Exact operation and bounded attempt authorized by the grant.
    executor_identity, destination_identity
        Exact calculator executor and external destination.
    resource_scope_identities
        Nonempty, unique resource-scope identities in lexical order.
    input_result_reference_identities, input_artifact_entry_identities
        Unique input result and artifact-entry references in lexical order.  Either
        tuple may be empty for a calculation without that input category.
    valid_from, valid_until
        Inclusive grant validity interval as timezone-aware UTC values.
    state
        Current closed grant state.
    reserved_obligation_identity
        Exact obligation for ``reserved`` or ``claimed`` state; absent for
        ``unused`` and optional for externally revoked state.

    Notes
    -----
    Construction represents externally supplied authority and performs no
    reservation, claim, revocation, or external effect.
    """

    authority_reference: ScientificExecutionAuthorityReference
    authority_source_identity: str
    issuer_identity: str
    request_identity: SimulationExecutionRequestIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_definition_identity: TaskDefinitionIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    executor_identity: ScientificExecutorIdentity
    destination_identity: DispatchDestinationIdentity
    resource_scope_identities: tuple[DispatchResourceScopeIdentity, ...]
    input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...]
    input_artifact_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]
    valid_from: datetime
    valid_until: datetime
    state: ScientificExecutionGrantState
    reserved_obligation_identity: ObligationIdentity | None = None

    def __post_init__(self) -> None:
        """Validate intrinsic grant scope, ordering, state, and UTC bounds."""
        expected = (
            (
                self.authority_reference,
                ScientificExecutionAuthorityReference,
                "authority_reference",
            ),
            (
                self.request_identity,
                SimulationExecutionRequestIdentity,
                "request_identity",
            ),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.task_definition_identity,
                TaskDefinitionIdentity,
                "task_definition_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (self.executor_identity, ScientificExecutorIdentity, "executor_identity"),
            (
                self.destination_identity,
                DispatchDestinationIdentity,
                "destination_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        for name in ("authority_source_identity", "issuer_identity"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")
        collections = (
            (
                "resource_scope_identities",
                DispatchResourceScopeIdentity,
                False,
            ),
            (
                "input_result_reference_identities",
                ResultObjectReferenceIdentity,
                True,
            ),
            (
                "input_artifact_entry_identities",
                ArtifactManifestEntryIdentity,
                True,
            ),
        )
        for name, collection_type, allow_empty in collections:
            values = getattr(self, name)
            if type(values) is not tuple or any(
                type(value) is not collection_type for value in values
            ):
                raise TypeError(f"{name} must be a tuple of {collection_type.__name__}")
            if not allow_empty and not values:
                raise ValueError(f"{name} must not be empty")
            if values != tuple(sorted(values, key=lambda value: value.value)) or len(
                set(values)
            ) != len(values):
                raise ValueError(f"{name} must be unique and lexically sorted")
        for name in ("valid_from", "valid_until"):
            value = getattr(self, name)
            if type(value) is not datetime:
                raise TypeError(f"{name} must be a datetime")
            if value.tzinfo is None or value.utcoffset() != timedelta(0):
                raise ValueError(f"{name} must be timezone-aware UTC")
        if self.valid_from > self.valid_until:
            raise ValueError("grant valid_from must not be after valid_until")
        if type(self.state) is not ScientificExecutionGrantState:
            raise TypeError("state must be ScientificExecutionGrantState")
        obligation = self.reserved_obligation_identity
        if obligation is not None and type(obligation) is not ObligationIdentity:
            raise TypeError(
                "reserved_obligation_identity must be ObligationIdentity or None"
            )
        if (
            self.state is ScientificExecutionGrantState.UNUSED
            and obligation is not None
        ):
            raise ValueError("an unused grant cannot name a reserved obligation")
        if (
            self.state
            in {
                ScientificExecutionGrantState.RESERVED,
                ScientificExecutionGrantState.CLAIMED,
            }
            and obligation is None
        ):
            raise ValueError("reserved and claimed grants require one obligation")

    def is_reserved_successor_of(
        self,
        preparation_grant: ScientificExecutionAuthorityGrant,
        obligation_identity: ObligationIdentity,
    ) -> bool:
        """Return whether this reserved view exactly succeeds one unused view.

        The two views must retain the same authority reference, source, issuer,
        dispatch scope, and validity interval.  They may differ only by transition
        from unused state to reservation for ``obligation_identity``.
        """
        if type(preparation_grant) is not ScientificExecutionAuthorityGrant:
            raise TypeError(
                "preparation_grant must be ScientificExecutionAuthorityGrant"
            )
        if type(obligation_identity) is not ObligationIdentity:
            raise TypeError("obligation_identity must be ObligationIdentity")
        return (
            preparation_grant.authority_reference == self.authority_reference
            and preparation_grant.authority_source_identity
            == self.authority_source_identity
            and preparation_grant.issuer_identity == self.issuer_identity
            and preparation_grant.request_identity == self.request_identity
            and preparation_grant.workflow_run_identity == self.workflow_run_identity
            and preparation_grant.task_definition_identity
            == self.task_definition_identity
            and preparation_grant.task_instance_identity == self.task_instance_identity
            and preparation_grant.activation_identity == self.activation_identity
            and preparation_grant.operation_identity == self.operation_identity
            and preparation_grant.attempt_identity == self.attempt_identity
            and preparation_grant.executor_identity == self.executor_identity
            and preparation_grant.destination_identity == self.destination_identity
            and preparation_grant.resource_scope_identities
            == self.resource_scope_identities
            and preparation_grant.input_result_reference_identities
            == self.input_result_reference_identities
            and preparation_grant.input_artifact_entry_identities
            == self.input_artifact_entry_identities
            and preparation_grant.valid_from == self.valid_from
            and preparation_grant.valid_until == self.valid_until
            and preparation_grant.state is ScientificExecutionGrantState.UNUSED
            and preparation_grant.reserved_obligation_identity is None
            and self.state is ScientificExecutionGrantState.RESERVED
            and self.reserved_obligation_identity == obligation_identity
        )


class SimulationExecutionAuthorizationPhase(StrEnum):
    """Closed authorization phase for one simulation dispatch."""

    PREPARATION = "preparation"
    CLAIM = "claim"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationExecutionAuthorizationRequest:
    """Request authorization of one exact simulation operation and phase.

    Parameters
    ----------
    result_identity
        Caller-supplied identity for the deterministic authorization result.
    phase
        Preparation requires an unused grant; claim requires the same grant
        reserved to ``obligation_identity``.
    grant, snapshot
        Exact externally supplied grant and verified authority-source view.
    request_identity, workflow_run_identity
        Exact simulation request and represented run.
    task_definition_identity, task_instance_identity, activation_identity
        Exact Task definition, instance, and activation.
    operation_identity, attempt_identity
        Exact operation and bounded attempt.
    executor_identity, destination_identity, obligation_identity
        Exact executor, destination, and preassigned dispatch obligation.
    resource_scope_identities
        Exact unique resource scopes in lexical order.
    input_result_reference_identities, input_artifact_entry_identities
        Exact unique input references in lexical order.
    evaluated_at
        Explicit timezone-aware UTC instant at which authorization is evaluated.
    """

    result_identity: SimulationExecutionAuthorizationResultIdentity
    phase: SimulationExecutionAuthorizationPhase
    grant: ScientificExecutionAuthorityGrant
    snapshot: ScientificExecutionAuthoritySnapshot
    request_identity: SimulationExecutionRequestIdentity
    workflow_run_identity: WorkflowRunIdentity
    task_definition_identity: TaskDefinitionIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    executor_identity: ScientificExecutorIdentity
    destination_identity: DispatchDestinationIdentity
    obligation_identity: ObligationIdentity
    resource_scope_identities: tuple[DispatchResourceScopeIdentity, ...]
    input_result_reference_identities: tuple[ResultObjectReferenceIdentity, ...]
    input_artifact_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]
    evaluated_at: datetime

    def __post_init__(self) -> None:
        """Validate exact request field types and canonical collections."""
        expected = (
            (
                self.result_identity,
                SimulationExecutionAuthorizationResultIdentity,
                "result_identity",
            ),
            (
                self.grant,
                ScientificExecutionAuthorityGrant,
                "grant",
            ),
            (
                self.snapshot,
                ScientificExecutionAuthoritySnapshot,
                "snapshot",
            ),
            (
                self.request_identity,
                SimulationExecutionRequestIdentity,
                "request_identity",
            ),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.task_definition_identity,
                TaskDefinitionIdentity,
                "task_definition_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (self.activation_identity, TaskActivationIdentity, "activation_identity"),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (self.executor_identity, ScientificExecutorIdentity, "executor_identity"),
            (
                self.destination_identity,
                DispatchDestinationIdentity,
                "destination_identity",
            ),
            (self.obligation_identity, ObligationIdentity, "obligation_identity"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.phase) is not SimulationExecutionAuthorizationPhase:
            raise TypeError("phase must be SimulationExecutionAuthorizationPhase")
        collections = (
            ("resource_scope_identities", DispatchResourceScopeIdentity),
            ("input_result_reference_identities", ResultObjectReferenceIdentity),
            ("input_artifact_entry_identities", ArtifactManifestEntryIdentity),
        )
        for name, collection_type in collections:
            values = getattr(self, name)
            if type(values) is not tuple or any(
                type(value) is not collection_type for value in values
            ):
                raise TypeError(f"{name} must be a tuple of {collection_type.__name__}")
            if values != tuple(sorted(values, key=lambda value: value.value)) or len(
                set(values)
            ) != len(values):
                raise ValueError(f"{name} must be unique and lexically sorted")
        if type(self.evaluated_at) is not datetime:
            raise TypeError("evaluated_at must be a datetime")
        if (
            self.evaluated_at.tzinfo is None
            or self.evaluated_at.utcoffset() != timedelta(0)
        ):
            raise ValueError("evaluated_at must be timezone-aware UTC")


@dataclass(frozen=True, slots=True, kw_only=True)
class WorkflowRunClaimCommitReceipt:
    """Represent typed evidence that persistence committed one claimed revision.

    Parameters
    ----------
    identity
        Exact receipt identity.
    workflow_run_identity
        Stable identity of the committed WorkflowRun.
    committed_revision_identity, predecessor_revision_identity
        Exact committed claim revision and its prepared predecessor.
    claimed_reservation_identity, claim_authorization_result_identity
        Exact claimed lifecycle record and distinct claim-phase authorization result
        contained in the committed revision.
    workflow_run_content_identity
        Nonempty exact content identity supplied by the future Workflow repository.
    persistence_operation_identity, commit_idempotency_identity
        Nonempty exact persistence operation and idempotency identities.
    persistence_implementation_identity
        Nonempty exact persistence implementation identity.

    Notes
    -----
    This immutable receipt records supplied persistence evidence.  It performs no
    repository operation and establishes no external execution or scientific claim.
    """

    identity: WorkflowRunClaimCommitReceiptIdentity
    workflow_run_identity: WorkflowRunIdentity
    committed_revision_identity: WorkflowRunRevisionIdentity
    predecessor_revision_identity: WorkflowRunRevisionIdentity
    claimed_reservation_identity: AuthorityReservationOutcomeIdentity
    claim_authorization_result_identity: SimulationExecutionAuthorizationResultIdentity
    workflow_run_content_identity: str
    persistence_operation_identity: str
    commit_idempotency_identity: str
    persistence_implementation_identity: str

    def __post_init__(self) -> None:
        """Validate exact receipt identities and distinct revision history."""
        expected = (
            (
                self.identity,
                WorkflowRunClaimCommitReceiptIdentity,
                "identity",
            ),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.committed_revision_identity,
                WorkflowRunRevisionIdentity,
                "committed_revision_identity",
            ),
            (
                self.predecessor_revision_identity,
                WorkflowRunRevisionIdentity,
                "predecessor_revision_identity",
            ),
            (
                self.claimed_reservation_identity,
                AuthorityReservationOutcomeIdentity,
                "claimed_reservation_identity",
            ),
            (
                self.claim_authorization_result_identity,
                SimulationExecutionAuthorizationResultIdentity,
                "claim_authorization_result_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if self.committed_revision_identity == self.predecessor_revision_identity:
            raise ValueError("committed revision must differ from predecessor revision")
        for name in (
            "workflow_run_content_identity",
            "persistence_operation_identity",
            "commit_idempotency_identity",
            "persistence_implementation_identity",
        ):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationDispatchEntryReceipt:
    """Represent persistence evidence for one newly won dispatch-entry CAS.

    Parameters
    ----------
    identity, dispatch_entry_identity
        Exact receipt and durable ``SimulationDispatchEntry`` identities.
    workflow_run_identity
        Stable identity of the affected WorkflowRun.
    claim_commit_receipt_identity
        Exact evidence for the committed claimed predecessor.
    predecessor_revision_identity, committed_revision_identity
        Exact claimed revision and distinct dispatch-entered revision.
    claimed_reservation_identity, obligation_identity, outcome_identity
        Exact claim, obligation, and reserved dispatch-outcome correlations.
    workflow_run_content_identity
        Nonempty content identity of the committed dispatch-entered revision.
    persistence_operation_identity, persistence_implementation_identity
        Exact persistence operation and implementation identities.

    Notes
    -----
    Only the newly successful compare-and-swap caller receives this receipt. Replaying
    receipt bytes is not dispatch authority; every adapter invocation must call the
    persistence-owned entry port again.
    """

    identity: SimulationDispatchEntryReceiptIdentity
    dispatch_entry_identity: SimulationDispatchEntryIdentity
    workflow_run_identity: WorkflowRunIdentity
    claim_commit_receipt_identity: WorkflowRunClaimCommitReceiptIdentity
    predecessor_revision_identity: WorkflowRunRevisionIdentity
    committed_revision_identity: WorkflowRunRevisionIdentity
    claimed_reservation_identity: AuthorityReservationOutcomeIdentity
    obligation_identity: ObligationIdentity
    outcome_identity: SimulationDispatchOutcomeIdentity
    workflow_run_content_identity: str
    persistence_operation_identity: str
    persistence_implementation_identity: str

    def __post_init__(self) -> None:
        """Validate exact identities and distinct revision history."""
        expected = (
            (self.identity, SimulationDispatchEntryReceiptIdentity, "identity"),
            (
                self.dispatch_entry_identity,
                SimulationDispatchEntryIdentity,
                "dispatch_entry_identity",
            ),
            (
                self.workflow_run_identity,
                WorkflowRunIdentity,
                "workflow_run_identity",
            ),
            (
                self.claim_commit_receipt_identity,
                WorkflowRunClaimCommitReceiptIdentity,
                "claim_commit_receipt_identity",
            ),
            (
                self.predecessor_revision_identity,
                WorkflowRunRevisionIdentity,
                "predecessor_revision_identity",
            ),
            (
                self.committed_revision_identity,
                WorkflowRunRevisionIdentity,
                "committed_revision_identity",
            ),
            (
                self.claimed_reservation_identity,
                AuthorityReservationOutcomeIdentity,
                "claimed_reservation_identity",
            ),
            (self.obligation_identity, ObligationIdentity, "obligation_identity"),
            (
                self.outcome_identity,
                SimulationDispatchOutcomeIdentity,
                "outcome_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if self.committed_revision_identity == self.predecessor_revision_identity:
            raise ValueError(
                "dispatch-entered revision must differ from claimed predecessor"
            )
        for name in (
            "workflow_run_content_identity",
            "persistence_operation_identity",
            "persistence_implementation_identity",
        ):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must not be empty")


class SimulationExecutionAuthorizationOutcomeKind(StrEnum):
    """Closed outcome of simulation execution authorization."""

    AUTHORIZED = "authorized"
    DENIED = "denied"
    ERROR = "error"


@dataclass(frozen=True, slots=True, kw_only=True)
class SimulationExecutionAuthorizationResult:
    """Record one closed authorization result without performing an effect.

    Parameters
    ----------
    identity
        Exact caller-supplied result identity.
    request
        Exact authorization request evaluated by the authorizer.
    kind
        Authorized, denied, or error outcome.
    authorized_grant_state
        Exact usable state for ``authorized``; otherwise ``None``.
    diagnostics
        Empty for ``authorized`` and nonempty ordered sanitized diagnostics for
        ``denied`` or ``error``.
    authorizer_implementation_identity
        Exact nonempty implementation identity of the authorizer.
    """

    identity: SimulationExecutionAuthorizationResultIdentity
    request: SimulationExecutionAuthorizationRequest
    kind: SimulationExecutionAuthorizationOutcomeKind
    authorized_grant_state: ScientificExecutionGrantState | None
    diagnostics: tuple[str, ...]
    authorizer_implementation_identity: str

    def __post_init__(self) -> None:
        """Validate exact result discrimination and diagnostics."""
        if type(self.identity) is not SimulationExecutionAuthorizationResultIdentity:
            raise TypeError(
                "identity must be SimulationExecutionAuthorizationResultIdentity"
            )
        if type(self.request) is not SimulationExecutionAuthorizationRequest:
            raise TypeError("request must be SimulationExecutionAuthorizationRequest")
        if self.identity != self.request.result_identity:
            raise ValueError("result identity must equal the request result identity")
        if type(self.kind) is not SimulationExecutionAuthorizationOutcomeKind:
            raise TypeError("kind must be SimulationExecutionAuthorizationOutcomeKind")
        state = self.authorized_grant_state
        if state is not None and type(state) is not ScientificExecutionGrantState:
            raise TypeError(
                "authorized_grant_state must be ScientificExecutionGrantState or None"
            )
        if type(self.diagnostics) is not tuple or any(
            type(value) is not str for value in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if any(not value for value in self.diagnostics):
            raise ValueError("diagnostics must not contain empty strings")
        if len(set(self.diagnostics)) != len(self.diagnostics):
            raise ValueError("diagnostics must not contain duplicates")
        if type(self.authorizer_implementation_identity) is not str:
            raise TypeError("authorizer_implementation_identity must be a string")
        if not self.authorizer_implementation_identity:
            raise ValueError("authorizer_implementation_identity must not be empty")
        if self.kind is SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED:
            expected_state = {
                SimulationExecutionAuthorizationPhase.PREPARATION: (
                    ScientificExecutionGrantState.UNUSED
                ),
                SimulationExecutionAuthorizationPhase.CLAIM: (
                    ScientificExecutionGrantState.RESERVED
                ),
            }[self.request.phase]
            if state is not expected_state or self.diagnostics:
                raise ValueError(
                    "authorized result requires the phase-compatible grant state "
                    "and prohibits diagnostics"
                )
        elif state is not None or not self.diagnostics:
            raise ValueError(
                "denied and error results prohibit state and require diagnostics"
            )

    @classmethod
    def evaluate(
        cls,
        request: SimulationExecutionAuthorizationRequest,
    ) -> SimulationExecutionAuthorizationResult:
        """Reproduce the exact deterministic effect-free authorization result."""
        if type(request) is not SimulationExecutionAuthorizationRequest:
            raise TypeError("request must be SimulationExecutionAuthorizationRequest")
        snapshot = request.snapshot
        grant = request.grant
        checks = (
            snapshot.content_verification,
            snapshot.authentication_verification,
            snapshot.predecessor_closure,
            snapshot.revocation_closure,
        )
        if ScientificExecutionAuthorityVerificationKind.INDETERMINATE in checks:
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.ERROR,
                "authority snapshot verification is indeterminate",
            )
        if ScientificExecutionAuthorityVerificationKind.FAILED in checks:
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.DENIED,
                "authority snapshot verification failed",
            )
        if (
            request.evaluated_at < snapshot.valid_from
            or request.evaluated_at > snapshot.valid_until
            or request.evaluated_at > snapshot.fresh_until
            or request.evaluated_at < grant.valid_from
            or request.evaluated_at > grant.valid_until
        ):
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.DENIED,
                "authority state is outside its validity or freshness bounds",
            )
        if (
            snapshot.identity != grant.authority_reference.snapshot_identity
            or snapshot.source_identity != grant.authority_source_identity
            or snapshot.issuer_identity != grant.issuer_identity
        ):
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.DENIED,
                "authority snapshot and grant identities do not agree",
            )
        if not cls._scope_agrees(request, grant):
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.DENIED,
                "grant scope does not match the requested simulation operation",
            )
        expected_state = (
            ScientificExecutionGrantState.UNUSED
            if request.phase is SimulationExecutionAuthorizationPhase.PREPARATION
            else ScientificExecutionGrantState.RESERVED
        )
        if grant.state is ScientificExecutionGrantState.REVOKED:
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.DENIED,
                "execution grant is revoked",
            )
        if grant.state is not expected_state:
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.DENIED,
                "execution grant state is incompatible with authorization phase",
            )
        if (
            request.phase is SimulationExecutionAuthorizationPhase.CLAIM
            and grant.reserved_obligation_identity != request.obligation_identity
        ):
            return cls._non_authorized(
                request,
                SimulationExecutionAuthorizationOutcomeKind.DENIED,
                "reserved grant does not name the requested obligation",
            )
        return cls(
            identity=request.result_identity,
            request=request,
            kind=SimulationExecutionAuthorizationOutcomeKind.AUTHORIZED,
            authorized_grant_state=grant.state,
            diagnostics=(),
            authorizer_implementation_identity=cls.implementation_identity(),
        )

    @staticmethod
    def implementation_identity() -> str:
        """Return the exact supported deterministic authorizer identity."""
        return "ksdft2effmass.workflows.SimulationExecutionAuthorizer.v1"

    @classmethod
    def _non_authorized(
        cls,
        request: SimulationExecutionAuthorizationRequest,
        kind: SimulationExecutionAuthorizationOutcomeKind,
        diagnostic: str,
    ) -> SimulationExecutionAuthorizationResult:
        """Construct one reproducible denied or error result."""
        return cls(
            identity=request.result_identity,
            request=request,
            kind=kind,
            authorized_grant_state=None,
            diagnostics=(diagnostic,),
            authorizer_implementation_identity=cls.implementation_identity(),
        )

    @staticmethod
    def _scope_agrees(
        request: SimulationExecutionAuthorizationRequest,
        grant: ScientificExecutionAuthorityGrant,
    ) -> bool:
        """Return whether all exact operation and scope correlations agree."""
        return (
            request.request_identity == grant.request_identity
            and request.workflow_run_identity == grant.workflow_run_identity
            and request.task_definition_identity == grant.task_definition_identity
            and request.task_instance_identity == grant.task_instance_identity
            and request.activation_identity == grant.activation_identity
            and request.operation_identity == grant.operation_identity
            and request.attempt_identity == grant.attempt_identity
            and request.executor_identity == grant.executor_identity
            and request.destination_identity == grant.destination_identity
            and request.resource_scope_identities == grant.resource_scope_identities
            and request.input_result_reference_identities
            == grant.input_result_reference_identities
            and request.input_artifact_entry_identities
            == grant.input_artifact_entry_identities
        )
