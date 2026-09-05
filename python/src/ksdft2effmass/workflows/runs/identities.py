"""Nominal identities for immutable represented Workflow runs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowDefinitionReferenceIdentity:
    """Identify one exact immutable Workflow definition reference.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "Workflow definition reference identity value must be a string"
            )
        if not self.value:
            raise ValueError(
                "Workflow definition reference identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class TaskWorkflowTransitionRecordIdentity:
    """Identify one exact task-origin Workflow transition record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("task transition record identity value must be a string")
        if not self.value:
            raise ValueError("task transition record identity value must not be empty")


@dataclass(frozen=True, slots=True)
class WorkflowRunRevisionIdentity:
    """Identify one immutable revision of a represented Workflow run.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  It is distinct from the stable
        :class:`WorkflowRunIdentity` and selects no persistence representation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("workflow run revision identity value must be a string")
        if not self.value:
            raise ValueError("workflow run revision identity value must not be empty")


@dataclass(frozen=True, slots=True)
class TaskAttemptRecordIdentity:
    """Identify one append-only state record for a stable Task attempt.

    Parameters
    ----------
    value
        Nonempty owner-local identity. Multiple state records may share one
        :class:`~ksdft2effmass.workflows.AttemptIdentity`, but each record identity
        is unique within its WorkflowRun history.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("task attempt record identity value must be a string")
        if not self.value:
            raise ValueError("task attempt record identity value must not be empty")


@dataclass(frozen=True, slots=True)
class TaskFailureRecordIdentity:
    """Identify one aggregate-correlated Task failure record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("task failure record identity value must be a string")
        if not self.value:
            raise ValueError("task failure record identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultObjectReferenceIdentity:
    """Identify one WorkflowRun correlation for a concrete ResultObject.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result reference identity value must be a string")
        if not self.value:
            raise ValueError("result reference identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultObjectContentIdentity:
    """Identify the immutable represented content of one ResultObject.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied by the result's owning domain.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result content identity value must be a string")
        if not self.value:
            raise ValueError("result content identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultObjectTypeIdentity:
    """Identify one concrete ResultObject contract and version.

    Parameters
    ----------
    value
        Nonempty exact built-in string naming the versioned result contract.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result type identity value must be a string")
        if not self.value:
            raise ValueError("result type identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultObjectDomainIdentity:
    """Identify the domain owner of one concrete ResultObject contract.

    Parameters
    ----------
    value
        Nonempty exact built-in string naming the responsible domain.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result domain identity value must be a string")
        if not self.value:
            raise ValueError("result domain identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultProducerProvenanceIdentity:
    """Identify one closed Workflow-owned ResultObject producer record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result producer identity value must be a string")
        if not self.value:
            raise ValueError("result producer identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultProducerEvidenceIdentity:
    """Identify exact retained evidence for non-Workflow result provenance.

    Parameters
    ----------
    value
        Nonempty exact built-in string identifying actual retained evidence.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result producer evidence identity value must be a string")
        if not self.value:
            raise ValueError(
                "result producer evidence identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class ExternalResultProducerIdentity:
    """Identify one declared producer outside represented Workflow state.

    Parameters
    ----------
    value
        Nonempty exact built-in string identifying the external producer.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("external result producer identity value must be a string")
        if not self.value:
            raise ValueError(
                "external result producer identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class ExternalProducerAttemptIdentity:
    """Identify one actual attempt by a non-Workflow external producer.

    Parameters
    ----------
    value
        Nonempty exact built-in string identifying the external attempt.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("external producer attempt identity value must be a string")
        if not self.value:
            raise ValueError(
                "external producer attempt identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class RetainedResultSourceIdentity:
    """Identify one actual retained or legacy ResultObject source.

    Parameters
    ----------
    value
        Nonempty exact built-in string identifying the retained source.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("retained result source identity value must be a string")
        if not self.value:
            raise ValueError("retained result source identity value must not be empty")


@dataclass(frozen=True, slots=True)
class HumanResultAuthorIdentity:
    """Identify the declared author of one human-authored ResultObject.

    Parameters
    ----------
    value
        Nonempty exact built-in string identifying the declared author.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("human result author identity value must be a string")
        if not self.value:
            raise ValueError("human result author identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultProductionRecordIdentity:
    """Identify one exact Task result-production correlation.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result production identity value must be a string")
        if not self.value:
            raise ValueError("result production identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResultDependencyIdentity:
    """Identify one explicit ResultObject-to-Task dependency edge.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("result dependency identity value must be a string")
        if not self.value:
            raise ValueError("result dependency identity value must not be empty")


@dataclass(frozen=True, slots=True)
class TaskWorkflowMembershipIdentity:
    """Identify one ordinary within-run Task membership record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("task Workflow membership identity value must be a string")
        if not self.value:
            raise ValueError(
                "task Workflow membership identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class NestedWorkflowMembershipIdentity:
    """Identify one parent-to-distinct-child Workflow membership record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "nested Workflow membership identity value must be a string"
            )
        if not self.value:
            raise ValueError(
                "nested Workflow membership identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class NestedWorkflowInvocationIdentity:
    """Identify one exact parent invocation of a distinct child Workflow run.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "nested Workflow invocation identity value must be a string"
            )
        if not self.value:
            raise ValueError(
                "nested Workflow invocation identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class ChildWorkflowCreationIdempotencyIdentity:
    """Identify one exact child-creation request for reconciliation.

    Parameters
    ----------
    value
        Nonempty exact built-in string used for idempotent child creation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "child creation idempotency identity value must be a string"
            )
        if not self.value:
            raise ValueError(
                "child creation idempotency identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class NestedWorkflowObservationIdentity:
    """Identify one terminal or indeterminate child-run observation.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "nested Workflow observation identity value must be a string"
            )
        if not self.value:
            raise ValueError(
                "nested Workflow observation identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class SimulationExecutionRequestCorrelationIdentity:
    """Identify one exact simulation request correlation record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("request correlation identity value must be a string")
        if not self.value:
            raise ValueError("request correlation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class SimulationExecutionRequestIdentity:
    """Identify one externally prepared simulation execution request.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with the request.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("simulation request identity value must be a string")
        if not self.value:
            raise ValueError("simulation request identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ScientificExecutorIdentity:
    """Identify the exact externally selected scientific executor.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with dispatch state.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("scientific executor identity value must be a string")
        if not self.value:
            raise ValueError("scientific executor identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ExecutionGrantIdentity:
    """Identify one externally issued exact-dispatch authority grant.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with authority state.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("execution grant identity value must be a string")
        if not self.value:
            raise ValueError("execution grant identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ExecutionGrantRevisionIdentity:
    """Identify one immutable revision of an execution grant.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with authority state.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("execution grant revision identity value must be a string")
        if not self.value:
            raise ValueError(
                "execution grant revision identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class ScientificExecutionAuthoritySnapshotIdentity:
    """Identify one externally verified scientific-authority snapshot.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied as represented authority state.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("authority snapshot identity value must be a string")
        if not self.value:
            raise ValueError("authority snapshot identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ScientificExecutionAuthorityStateIdentity:
    """Identify the exact externally supplied grant state.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied as represented authority state.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("authority state identity value must be a string")
        if not self.value:
            raise ValueError("authority state identity value must not be empty")


@dataclass(frozen=True, slots=True)
class SimulationExecutionAuthorizationResultIdentity:
    """Identify one exact externally produced authorization result.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with request correlation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("authorization result identity value must be a string")
        if not self.value:
            raise ValueError("authorization result identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ObligationIdentity:
    """Identify one durable simulation dispatch obligation.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("obligation identity value must be a string")
        if not self.value:
            raise ValueError("obligation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class AuthorityReservationOutcomeIdentity:
    """Identify one append-only grant reservation or claim record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("reservation outcome identity value must be a string")
        if not self.value:
            raise ValueError("reservation outcome identity value must not be empty")


@dataclass(frozen=True, slots=True)
class DispatchOutcomeRecordIdentity:
    """Identify one aggregate-owned specialized dispatch outcome record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("dispatch outcome record identity value must be a string")
        if not self.value:
            raise ValueError("dispatch outcome record identity value must not be empty")


@dataclass(frozen=True, slots=True)
class SimulationDispatchOutcomeIdentity:
    """Identify one specialized dispatch envelope supplied to WorkflowRun.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with dispatch state.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("dispatch envelope identity value must be a string")
        if not self.value:
            raise ValueError("dispatch envelope identity value must not be empty")


@dataclass(frozen=True, slots=True)
class DispatchDestinationIdentity:
    """Identify the immutable external dispatch destination.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with the obligation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("dispatch destination identity value must be a string")
        if not self.value:
            raise ValueError("dispatch destination identity value must not be empty")


@dataclass(frozen=True, slots=True)
class DispatchResourceScopeIdentity:
    """Identify one immutable externally authorized resource scope.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied with the obligation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("dispatch resource scope identity value must be a string")
        if not self.value:
            raise ValueError("dispatch resource scope identity value must not be empty")


@dataclass(frozen=True, slots=True)
class DispatchCreationIdempotencyIdentity:
    """Identify one exact obligation-creation request.

    Parameters
    ----------
    value
        Nonempty exact built-in string used for idempotent creation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("dispatch idempotency identity value must be a string")
        if not self.value:
            raise ValueError("dispatch idempotency identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ObligationDispositionIdentity:
    """Identify one append-only obligation-disposition record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("obligation disposition identity value must be a string")
        if not self.value:
            raise ValueError("obligation disposition identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ScientificDecisionRequestIdentity:
    """Identify one exact scientific-decision request.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "scientific decision request identity value must be a string"
            )
        if not self.value:
            raise ValueError(
                "scientific decision request identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class ScientificDecisionOptionIdentity:
    """Identify one option within a scientific-decision request.

    Parameters
    ----------
    value
        Nonempty exact built-in string unique within the request.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError(
                "scientific decision option identity value must be a string"
            )
        if not self.value:
            raise ValueError(
                "scientific decision option identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class ScientificDecisionTransitionRecordIdentity:
    """Identify one no-Task scientific-decision transition record.

    Parameters
    ----------
    value
        Nonempty exact built-in string with owner-local identity semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("decision transition identity value must be a string")
        if not self.value:
            raise ValueError("decision transition identity value must not be empty")


@dataclass(frozen=True, slots=True)
class WorkflowTransitionSequenceIdentity:
    """Identify one canonical position in a WorkflowRun transition history.

    Parameters
    ----------
    value
        Nonempty exact built-in string unique within the run history.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("transition sequence identity value must be a string")
        if not self.value:
            raise ValueError("transition sequence identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ResponseSourceIdentity:
    """Identify the direct application-boundary response source.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied by the application boundary.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("response source identity value must be a string")
        if not self.value:
            raise ValueError("response source identity value must not be empty")


@dataclass(frozen=True, slots=True)
class AuthorityContextIdentity:
    """Identify the direct application-boundary authority context.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied by the application boundary.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("authority context identity value must be a string")
        if not self.value:
            raise ValueError("authority context identity value must not be empty")


@dataclass(frozen=True, slots=True)
class BoundaryReceiptIdentity:
    """Identify actually available application-boundary supporting evidence.

    Parameters
    ----------
    value
        Nonempty exact built-in string supplied when evidence exists.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("boundary receipt identity value must be a string")
        if not self.value:
            raise ValueError("boundary receipt identity value must not be empty")


@dataclass(frozen=True, slots=True)
class ScientificDecisionRecorderIdentity:
    """Identify the exact scientific-decision recorder implementation/version.

    Parameters
    ----------
    value
        Nonempty exact built-in string naming recorder semantics.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("decision recorder identity value must be a string")
        if not self.value:
            raise ValueError("decision recorder identity value must not be empty")


@dataclass(frozen=True, slots=True)
class WorkflowRuntimeBundleIdentity:
    """Identify one exact immutable collection of replay dependencies.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  This identity does not imply that the
        referenced versions are supported by the current implementation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("workflow runtime bundle identity value must be a string")
        if not self.value:
            raise ValueError("workflow runtime bundle identity value must not be empty")


@dataclass(frozen=True, slots=True)
class TaskInvocationOutcomeIdentity:
    """Identify one closed generic invocation outcome.

    Parameters
    ----------
    value
        Nonempty owner-local identity for one activation, operation, and attempt.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("task invocation outcome identity value must be a string")
        if not self.value:
            raise ValueError("task invocation outcome identity value must not be empty")


@dataclass(frozen=True, slots=True)
class TaskInvocationFailureIdentity:
    """Identify one Task-domain structured failure retained by Workflow control.

    Parameters
    ----------
    value
        Nonempty owner-local identity.  The producing Task domain owns the failure
        code vocabulary; WorkflowRun preserves it without reinterpretation.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the exact owner-local identity value."""
        if type(self.value) is not str:
            raise TypeError("task invocation failure identity value must be a string")
        if not self.value:
            raise ValueError("task invocation failure identity value must not be empty")


@dataclass(frozen=True, slots=True)
class WorkflowRunReplayResultIdentity:
    """Content-identify one closed WorkflowRun replay result.

    Parameters
    ----------
    value
        Exactly 64 lowercase hexadecimal SHA-256 characters derived by
        :class:`WorkflowRunReplayer`.  This identity is not a serialized run format.
    """

    value: str

    def __post_init__(self) -> None:
        """Validate the fixed lowercase SHA-256 representation."""
        if type(self.value) is not str:
            raise TypeError("workflow replay result identity value must be a string")
        if len(self.value) != 64 or any(
            character not in "0123456789abcdef" for character in self.value
        ):
            raise ValueError(
                "workflow replay result identity must be a lowercase SHA-256 digest"
            )
