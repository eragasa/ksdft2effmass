"""Bounded aggregate values in the WorkflowRun wire representation."""

from __future__ import annotations

from ksdft2effmass.petrinet.colored.markings import (
    ColoredPetriNetMarking,
)
from ksdft2effmass.workflows.model import (
    TaskActivation,
    TaskInstance,
)
from ksdft2effmass.workflows.runs.authority import (
    SimulationExecutionAuthorizationResult,
)
from ksdft2effmass.workflows.runs.identities import (
    WorkflowDefinitionReferenceIdentity,
    WorkflowRunReplayResultIdentity,
    WorkflowRuntimeBundleIdentity,
    WorkflowTransitionSequenceIdentity,
)
from ksdft2effmass.workflows.runs.records import (
    AuthorityReservationOutcome,
    DispatchObservationRecord,
    DispatchOutcomeRecord,
    NativeOutputAdmission,
    NestedWorkflowInvocation,
    NestedWorkflowInvocationIntent,
    NestedWorkflowMembership,
    NestedWorkflowTerminalObservation,
    ObligationDisposition,
    ResultDependency,
    ResultObjectReference,
    ResultProductionRecord,
    ScientificDecisionRequest,
    ScientificDecisionWorkflowTransitionRecord,
    ScientificExecutionAuthorityReference,
    SimulationDispatchEntry,
    SimulationDispatchObligation,
    SimulationExecutionRequestCorrelation,
    TaskAttempt,
    TaskFailureRecord,
    TaskInvocationOutcome,
    TaskWorkflowMembership,
    TaskWorkflowTransitionRecord,
)

from ...model import (
    WorkflowIdentity,
    WorkflowRunIdentity,
)
from ...runs.aggregate import WorkflowRun
from ...runs.identities import (
    WorkflowRunRevisionIdentity,
)
from ...runs.records import (
    ScientificDecisionResolution,
)
from ..records import (
    WorkflowEncodedResultValue,
)
from ._base import (
    _ResultJson,
    _RunValue,
    _WorkflowRunWireSerializer,
    _WorkflowRunWireUnsupported,
)


class _WorkflowRunAggregateWireSerializer(_WorkflowRunWireSerializer):
    """Encode and decode the closed aggregate value family."""

    def _encode_aggregate(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if type(value) is WorkflowDefinitionReferenceIdentity:
            return self._record(
                "WorkflowDefinitionReferenceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowIdentity:
            return self._record(
                "WorkflowIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRun:
            return self._record(
                "WorkflowRun",
                {
                    "identity": self._encode(value.identity, seen),
                    "revision_identity": self._encode(value.revision_identity, seen),
                    "predecessor_revision_identity": self._encode(
                        value.predecessor_revision_identity, seen
                    ),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "definition_reference_identity": self._encode(
                        value.definition_reference_identity, seen
                    ),
                    "runtime_bundle_identity": self._encode(
                        value.runtime_bundle_identity, seen
                    ),
                    "schema_version": self._encode(value.schema_version, seen),
                    "adapter_implementation_identity": self._encode(
                        value.adapter_implementation_identity, seen
                    ),
                    "task_instances": self._encode(value.task_instances, seen),
                    "task_memberships": self._encode(value.task_memberships, seen),
                    "nested_memberships": self._encode(value.nested_memberships, seen),
                    "nested_invocations": self._encode(value.nested_invocations, seen),
                    **(
                        {
                            "nested_invocation_intents": self._encode(
                                value.nested_invocation_intents, seen
                            ),
                            "nested_terminal_observations": self._encode(
                                value.nested_terminal_observations, seen
                            ),
                        }
                        if value.nested_invocation_intents
                        or value.nested_terminal_observations
                        else {}
                    ),
                    "activations": self._encode(value.activations, seen),
                    "attempts": self._encode(value.attempts, seen),
                    "outcomes": self._encode(value.outcomes, seen),
                    "result_references": self._encode(value.result_references, seen),
                    "result_productions": self._encode(value.result_productions, seen),
                    "native_output_admissions": self._encode(
                        value.native_output_admissions, seen
                    ),
                    "result_dependencies": self._encode(
                        value.result_dependencies, seen
                    ),
                    "failures": self._encode(value.failures, seen),
                    "authorization_results": self._encode(
                        value.authorization_results, seen
                    ),
                    "authority_references": self._encode(
                        value.authority_references, seen
                    ),
                    "execution_request_correlations": self._encode(
                        value.execution_request_correlations, seen
                    ),
                    "authority_reservations": self._encode(
                        value.authority_reservations, seen
                    ),
                    "dispatch_obligations": self._encode(
                        value.dispatch_obligations, seen
                    ),
                    "dispatch_entries": self._encode(value.dispatch_entries, seen),
                    "dispatch_observations": self._encode(
                        value.dispatch_observations, seen
                    ),
                    "dispatch_outcomes": self._encode(value.dispatch_outcomes, seen),
                    "obligation_dispositions": self._encode(
                        value.obligation_dispositions, seen
                    ),
                    "scientific_decision_requests": self._encode(
                        value.scientific_decision_requests, seen
                    ),
                    "scientific_decision_resolutions": self._encode(
                        value.scientific_decision_resolutions, seen
                    ),
                    "initial_marking": self._encode(value.initial_marking, seen),
                    "current_marking": self._encode(value.current_marking, seen),
                    "transitions": self._encode(value.transitions, seen),
                },
            )
        if type(value) is WorkflowRunIdentity:
            return self._record(
                "WorkflowRunIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRunReplayResultIdentity:
            return self._record(
                "WorkflowRunReplayResultIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRunRevisionIdentity:
            return self._record(
                "WorkflowRunRevisionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowRuntimeBundleIdentity:
            return self._record(
                "WorkflowRuntimeBundleIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is WorkflowTransitionSequenceIdentity:
            return self._record(
                "WorkflowTransitionSequenceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        raise _WorkflowRunWireUnsupported

    def _decode_aggregate(
        self, tag: str, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        record: _RunValue
        if tag == "WorkflowDefinitionReferenceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowDefinitionReferenceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRun":
            if not isinstance(wire, dict):
                raise TypeError("WorkflowRun wire must be a record")
            raw_run_fields = wire["fields"]
            extension_names = (
                ("nested_invocation_intents", "nested_terminal_observations")
                if isinstance(raw_run_fields, dict)
                and (
                    "nested_invocation_intents" in raw_run_fields
                    or "nested_terminal_observations" in raw_run_fields
                )
                else ()
            )
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "revision_identity",
                    "predecessor_revision_identity",
                    "workflow_identity",
                    "definition_reference_identity",
                    "runtime_bundle_identity",
                    "schema_version",
                    "adapter_implementation_identity",
                    "task_instances",
                    "task_memberships",
                    "nested_memberships",
                    "nested_invocations",
                    "activations",
                    "attempts",
                    "outcomes",
                    "result_references",
                    "result_productions",
                    "native_output_admissions",
                    "result_dependencies",
                    "failures",
                    "authorization_results",
                    "authority_references",
                    "execution_request_correlations",
                    "authority_reservations",
                    "dispatch_obligations",
                    "dispatch_entries",
                    "dispatch_observations",
                    "dispatch_outcomes",
                    "obligation_dispositions",
                    "scientific_decision_requests",
                    "scientific_decision_resolutions",
                    "initial_marking",
                    "current_marking",
                    "transitions",
                    *extension_names,
                ),
            )
            record = WorkflowRun(
                identity=self._exact(
                    self._decode(fields["identity"], seen), WorkflowRunIdentity
                ),
                revision_identity=self._exact(
                    self._decode(fields["revision_identity"], seen),
                    WorkflowRunRevisionIdentity,
                ),
                predecessor_revision_identity=self._parse_NestedWorkflowInvocation_terminal_child_revision_identity(
                    self._decode(fields["predecessor_revision_identity"], seen)
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                definition_reference_identity=self._exact(
                    self._decode(fields["definition_reference_identity"], seen),
                    WorkflowDefinitionReferenceIdentity,
                ),
                runtime_bundle_identity=self._exact(
                    self._decode(fields["runtime_bundle_identity"], seen),
                    WorkflowRuntimeBundleIdentity,
                ),
                schema_version=self._exact(
                    self._decode(fields["schema_version"], seen), int
                ),
                adapter_implementation_identity=self._exact(
                    self._decode(fields["adapter_implementation_identity"], seen), str
                ),
                task_instances=tuple(
                    self._exact(item, TaskInstance)
                    for item in self._items(
                        self._decode(fields["task_instances"], seen)
                    )
                ),
                task_memberships=tuple(
                    self._exact(item, TaskWorkflowMembership)
                    for item in self._items(
                        self._decode(fields["task_memberships"], seen)
                    )
                ),
                nested_memberships=tuple(
                    self._exact(item, NestedWorkflowMembership)
                    for item in self._items(
                        self._decode(fields["nested_memberships"], seen)
                    )
                ),
                nested_invocations=tuple(
                    self._exact(item, NestedWorkflowInvocation)
                    for item in self._items(
                        self._decode(fields["nested_invocations"], seen)
                    )
                ),
                nested_invocation_intents=(
                    tuple(
                        self._exact(item, NestedWorkflowInvocationIntent)
                        for item in self._items(
                            self._decode(fields["nested_invocation_intents"], seen)
                        )
                    )
                    if extension_names
                    else ()
                ),
                nested_terminal_observations=(
                    tuple(
                        self._exact(item, NestedWorkflowTerminalObservation)
                        for item in self._items(
                            self._decode(fields["nested_terminal_observations"], seen)
                        )
                    )
                    if extension_names
                    else ()
                ),
                activations=tuple(
                    self._exact(item, TaskActivation)
                    for item in self._items(self._decode(fields["activations"], seen))
                ),
                attempts=tuple(
                    self._exact(item, TaskAttempt)
                    for item in self._items(self._decode(fields["attempts"], seen))
                ),
                outcomes=tuple(
                    self._exact(item, TaskInvocationOutcome)
                    for item in self._items(self._decode(fields["outcomes"], seen))
                ),
                result_references=tuple(
                    self._exact(item, ResultObjectReference)
                    for item in self._items(
                        self._decode(fields["result_references"], seen)
                    )
                ),
                result_productions=tuple(
                    self._exact(item, ResultProductionRecord)
                    for item in self._items(
                        self._decode(fields["result_productions"], seen)
                    )
                ),
                native_output_admissions=tuple(
                    self._exact(item, NativeOutputAdmission)
                    for item in self._items(
                        self._decode(fields["native_output_admissions"], seen)
                    )
                ),
                result_dependencies=tuple(
                    self._exact(item, ResultDependency)
                    for item in self._items(
                        self._decode(fields["result_dependencies"], seen)
                    )
                ),
                failures=tuple(
                    self._exact(item, TaskFailureRecord)
                    for item in self._items(self._decode(fields["failures"], seen))
                ),
                authorization_results=tuple(
                    self._exact(item, SimulationExecutionAuthorizationResult)
                    for item in self._items(
                        self._decode(fields["authorization_results"], seen)
                    )
                ),
                authority_references=tuple(
                    self._exact(item, ScientificExecutionAuthorityReference)
                    for item in self._items(
                        self._decode(fields["authority_references"], seen)
                    )
                ),
                execution_request_correlations=tuple(
                    self._exact(item, SimulationExecutionRequestCorrelation)
                    for item in self._items(
                        self._decode(fields["execution_request_correlations"], seen)
                    )
                ),
                authority_reservations=tuple(
                    self._exact(item, AuthorityReservationOutcome)
                    for item in self._items(
                        self._decode(fields["authority_reservations"], seen)
                    )
                ),
                dispatch_obligations=tuple(
                    self._exact(item, SimulationDispatchObligation)
                    for item in self._items(
                        self._decode(fields["dispatch_obligations"], seen)
                    )
                ),
                dispatch_entries=tuple(
                    self._exact(item, SimulationDispatchEntry)
                    for item in self._items(
                        self._decode(fields["dispatch_entries"], seen)
                    )
                ),
                dispatch_observations=tuple(
                    self._exact(item, DispatchObservationRecord)
                    for item in self._items(
                        self._decode(fields["dispatch_observations"], seen)
                    )
                ),
                dispatch_outcomes=tuple(
                    self._exact(item, DispatchOutcomeRecord)
                    for item in self._items(
                        self._decode(fields["dispatch_outcomes"], seen)
                    )
                ),
                obligation_dispositions=tuple(
                    self._exact(item, ObligationDisposition)
                    for item in self._items(
                        self._decode(fields["obligation_dispositions"], seen)
                    )
                ),
                scientific_decision_requests=tuple(
                    self._exact(item, ScientificDecisionRequest)
                    for item in self._items(
                        self._decode(fields["scientific_decision_requests"], seen)
                    )
                ),
                scientific_decision_resolutions=tuple(
                    self._exact(item, ScientificDecisionResolution)
                    for item in self._items(
                        self._decode(fields["scientific_decision_resolutions"], seen)
                    )
                ),
                initial_marking=self._exact(
                    self._decode(fields["initial_marking"], seen),
                    ColoredPetriNetMarking,
                ),
                current_marking=self._exact(
                    self._decode(fields["current_marking"], seen),
                    ColoredPetriNetMarking,
                ),
                transitions=tuple(
                    self._parse_WorkflowRun_transitions_item(item)
                    for item in self._items(self._decode(fields["transitions"], seen))
                ),
            )
            return record
        if tag == "WorkflowRunIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRunIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRunReplayResultIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRunReplayResultIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRunRevisionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRunRevisionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowRuntimeBundleIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowRuntimeBundleIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "WorkflowTransitionSequenceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = WorkflowTransitionSequenceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        raise _WorkflowRunWireUnsupported

    def _parse_WorkflowRun_transitions_item(
        self, value: _RunValue
    ) -> TaskWorkflowTransitionRecord | ScientificDecisionWorkflowTransitionRecord:
        if type(value) is TaskWorkflowTransitionRecord:
            return self._exact(value, TaskWorkflowTransitionRecord)
        if type(value) is ScientificDecisionWorkflowTransitionRecord:
            return self._exact(value, ScientificDecisionWorkflowTransitionRecord)
        raise TypeError("wrong closed field variant")
