"""Bounded task values in the WorkflowRun wire representation."""

from __future__ import annotations

from ksdft2effmass.petrinet.colored.firing import (
    ColoredPetriNetFiringResult,
)
from ksdft2effmass.petrinet.colored.markings import (
    ColoredPetriNetBinding,
    ColoredPetriNetTransitionIdentity,
)
from ksdft2effmass.petrinet.colored.selection import (
    ColoredPetriNetSelectionResultIdentity,
)
from ksdft2effmass.workflows.model import (
    AllOfTaskActivationSelection,
    AnyOfTaskActivationSelection,
    AttemptIdentity,
    DirectTaskActivationSelection,
    OperationIdentity,
    TaskActivation,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskGateSelection,
    TaskInputBinding,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
)
from ksdft2effmass.workflows.runs.identities import (
    DispatchOutcomeRecordIdentity,
    ResultProductionRecordIdentity,
    SimulationExecutionRequestCorrelationIdentity,
    SimulationExecutionRequestIdentity,
    TaskAttemptRecordIdentity,
    TaskFailureRecordIdentity,
    TaskInvocationFailureIdentity,
    TaskInvocationOutcomeIdentity,
    TaskWorkflowMembershipIdentity,
    TaskWorkflowTransitionRecordIdentity,
    WorkflowDefinitionReferenceIdentity,
    WorkflowRuntimeBundleIdentity,
    WorkflowTransitionSequenceIdentity,
)
from ksdft2effmass.workflows.runs.records import (
    ResultObjectReference,
    TaskAttempt,
    TaskAttemptStatus,
    TaskFailureRecord,
    TaskInvocationFailure,
    TaskInvocationOutcome,
    TaskInvocationOutcomeKind,
    TaskWorkflowMembership,
    TaskWorkflowTransitionRecord,
)

from ...model import (
    WorkflowIdentity,
    WorkflowRunIdentity,
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


class _WorkflowRunTaskWireSerializer(_WorkflowRunWireSerializer):
    """Encode and decode the closed task value family."""

    def _encode_task(
        self, value: _RunValue, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _ResultJson:
        if type(value) is TaskAttemptStatus:
            return self._record("TaskAttemptStatus", {"value": value.value})
        if type(value) is TaskInvocationOutcomeKind:
            return self._record("TaskInvocationOutcomeKind", {"value": value.value})
        if type(value) is TaskStartGateSetMode:
            return self._record("TaskStartGateSetMode", {"value": value.value})
        if type(value) is AllOfTaskActivationSelection:
            return self._record(
                "AllOfTaskActivationSelection",
                {
                    "gate_set_identity": self._encode(value.gate_set_identity, seen),
                    "selected_gates": self._encode(value.selected_gates, seen),
                    "selection_result_identity": self._encode(
                        value.selection_result_identity, seen
                    ),
                },
            )
        if type(value) is AnyOfTaskActivationSelection:
            return self._record(
                "AnyOfTaskActivationSelection",
                {
                    "gate_set_identity": self._encode(value.gate_set_identity, seen),
                    "selected_gate": self._encode(value.selected_gate, seen),
                    "selection_result_identity": self._encode(
                        value.selection_result_identity, seen
                    ),
                },
            )
        if type(value) is AttemptIdentity:
            return self._record(
                "AttemptIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is DirectTaskActivationSelection:
            return self._record(
                "DirectTaskActivationSelection",
                {
                    "selection_result_identity": self._encode(
                        value.selection_result_identity, seen
                    ),
                },
            )
        if type(value) is OperationIdentity:
            return self._record(
                "OperationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskActivation:
            return self._record(
                "TaskActivation",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_instance": self._encode(value.task_instance, seen),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "inputs": self._encode(value.inputs, seen),
                    "selection": self._encode(value.selection, seen),
                },
            )
        if type(value) is TaskActivationIdentity:
            return self._record(
                "TaskActivationIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskAttempt:
            return self._record(
                "TaskAttempt",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "status": self._encode(value.status, seen),
                    "predecessor_attempt_record_identity": self._encode(
                        value.predecessor_attempt_record_identity, seen
                    ),
                    "retry_of_attempt_identity": self._encode(
                        value.retry_of_attempt_identity, seen
                    ),
                    "child_workflow_run_identity": self._encode(
                        value.child_workflow_run_identity, seen
                    ),
                },
            )
        if type(value) is TaskAttemptRecordIdentity:
            return self._record(
                "TaskAttemptRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskDefinitionIdentity:
            return self._record(
                "TaskDefinitionIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskFailureRecord:
            return self._record(
                "TaskFailureRecord",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "failure": self._encode(value.failure, seen),
                    "request_identity": self._encode(value.request_identity, seen),
                    "child_workflow_run_identity": self._encode(
                        value.child_workflow_run_identity, seen
                    ),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is TaskFailureRecordIdentity:
            return self._record(
                "TaskFailureRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskGateSelection:
            return self._record(
                "TaskGateSelection",
                {
                    "gate_identity": self._encode(value.gate_identity, seen),
                    "binding": self._encode(value.binding, seen),
                },
            )
        if type(value) is TaskInputBinding:
            return self._record(
                "TaskInputBinding",
                {
                    "name": self._encode(value.name, seen),
                    "result": self._encode(value.result, seen),
                },
            )
        if type(value) is TaskInstance:
            return self._record(
                "TaskInstance",
                {
                    "identity": self._encode(value.identity, seen),
                    "definition_identity": self._encode(
                        value.definition_identity, seen
                    ),
                    "start_gate_set": self._encode(value.start_gate_set, seen),
                },
            )
        if type(value) is TaskInstanceIdentity:
            return self._record(
                "TaskInstanceIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskInvocationFailure:
            return self._record(
                "TaskInvocationFailure",
                {
                    "identity": self._encode(value.identity, seen),
                    "code": self._encode(value.code, seen),
                    "operation_phase": self._encode(value.operation_phase, seen),
                    "diagnostic": self._encode(value.diagnostic, seen),
                    "retryable": self._encode(value.retryable, seen),
                    "claim_boundary": self._encode(value.claim_boundary, seen),
                },
            )
        if type(value) is TaskInvocationFailureIdentity:
            return self._record(
                "TaskInvocationFailureIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskInvocationOutcome:
            return self._record(
                "TaskInvocationOutcome",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "kind": self._encode(value.kind, seen),
                    "results": self._encode(value.results, seen),
                    "production_record_identities": self._encode(
                        value.production_record_identities, seen
                    ),
                    "failure_record_identity": self._encode(
                        value.failure_record_identity, seen
                    ),
                    "dispatch_outcome_record_identity": self._encode(
                        value.dispatch_outcome_record_identity, seen
                    ),
                    "reconciliation_identity_values": self._encode(
                        value.reconciliation_identity_values, seen
                    ),
                },
            )
        if type(value) is TaskInvocationOutcomeIdentity:
            return self._record(
                "TaskInvocationOutcomeIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskStartGate:
            return self._record(
                "TaskStartGate",
                {
                    "identity": self._encode(value.identity, seen),
                    "priority": self._encode(value.priority, seen),
                    "transition_identity": self._encode(
                        value.transition_identity, seen
                    ),
                },
            )
        if type(value) is TaskStartGateIdentity:
            return self._record(
                "TaskStartGateIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskStartGateSet:
            return self._record(
                "TaskStartGateSet",
                {
                    "identity": self._encode(value.identity, seen),
                    "mode": self._encode(value.mode, seen),
                    "gates": self._encode(value.gates, seen),
                },
            )
        if type(value) is TaskStartGateSetIdentity:
            return self._record(
                "TaskStartGateSetIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskWorkflowMembership:
            return self._record(
                "TaskWorkflowMembership",
                {
                    "identity": self._encode(value.identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "task_instance_identity": self._encode(
                        value.task_instance_identity, seen
                    ),
                },
            )
        if type(value) is TaskWorkflowMembershipIdentity:
            return self._record(
                "TaskWorkflowMembershipIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        if type(value) is TaskWorkflowTransitionRecord:
            return self._record(
                "TaskWorkflowTransitionRecord",
                {
                    "identity": self._encode(value.identity, seen),
                    "sequence_identity": self._encode(value.sequence_identity, seen),
                    "sequence_index": self._encode(value.sequence_index, seen),
                    "workflow_identity": self._encode(value.workflow_identity, seen),
                    "workflow_run_identity": self._encode(
                        value.workflow_run_identity, seen
                    ),
                    "definition_reference_identity": self._encode(
                        value.definition_reference_identity, seen
                    ),
                    "runtime_bundle_identity": self._encode(
                        value.runtime_bundle_identity, seen
                    ),
                    "activation_identity": self._encode(
                        value.activation_identity, seen
                    ),
                    "operation_identity": self._encode(value.operation_identity, seen),
                    "attempt_identity": self._encode(value.attempt_identity, seen),
                    "terminal_attempt_record_identity": self._encode(
                        value.terminal_attempt_record_identity, seen
                    ),
                    "outcome_identity": self._encode(value.outcome_identity, seen),
                    "result_production_identities": self._encode(
                        value.result_production_identities, seen
                    ),
                    "firing_result": self._encode(value.firing_result, seen),
                    "request_correlation_identity": self._encode(
                        value.request_correlation_identity, seen
                    ),
                    "dispatch_outcome_record_identity": self._encode(
                        value.dispatch_outcome_record_identity, seen
                    ),
                },
            )
        if type(value) is TaskWorkflowTransitionRecordIdentity:
            return self._record(
                "TaskWorkflowTransitionRecordIdentity",
                {
                    "value": self._encode(value.value, seen),
                },
            )
        raise _WorkflowRunWireUnsupported

    def _decode_task(
        self, tag: str, wire: _ResultJson, seen: dict[str, WorkflowEncodedResultValue]
    ) -> _RunValue:
        record: _RunValue
        if tag == "TaskAttemptStatus":
            return TaskAttemptStatus(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "TaskInvocationOutcomeKind":
            return TaskInvocationOutcomeKind(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "TaskStartGateSetMode":
            return TaskStartGateSetMode(
                self._string(self._fields(wire, tag, ("value",))["value"])
            )
        if tag == "AllOfTaskActivationSelection":
            fields = self._fields(
                wire,
                tag,
                ("gate_set_identity", "selected_gates", "selection_result_identity"),
            )
            record = AllOfTaskActivationSelection(
                gate_set_identity=self._exact(
                    self._decode(fields["gate_set_identity"], seen),
                    TaskStartGateSetIdentity,
                ),
                selected_gates=tuple(
                    self._exact(item, TaskGateSelection)
                    for item in self._items(
                        self._decode(fields["selected_gates"], seen)
                    )
                ),
                selection_result_identity=self._exact(
                    self._decode(fields["selection_result_identity"], seen),
                    ColoredPetriNetSelectionResultIdentity,
                ),
            )
            return record
        if tag == "AnyOfTaskActivationSelection":
            fields = self._fields(
                wire,
                tag,
                ("gate_set_identity", "selected_gate", "selection_result_identity"),
            )
            record = AnyOfTaskActivationSelection(
                gate_set_identity=self._exact(
                    self._decode(fields["gate_set_identity"], seen),
                    TaskStartGateSetIdentity,
                ),
                selected_gate=self._exact(
                    self._decode(fields["selected_gate"], seen), TaskGateSelection
                ),
                selection_result_identity=self._exact(
                    self._decode(fields["selection_result_identity"], seen),
                    ColoredPetriNetSelectionResultIdentity,
                ),
            )
            return record
        if tag == "AttemptIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = AttemptIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "DirectTaskActivationSelection":
            fields = self._fields(wire, tag, ("selection_result_identity",))
            record = DirectTaskActivationSelection(
                selection_result_identity=self._exact(
                    self._decode(fields["selection_result_identity"], seen),
                    ColoredPetriNetSelectionResultIdentity,
                ),
            )
            return record
        if tag == "OperationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = OperationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskActivation":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_identity",
                    "workflow_run_identity",
                    "task_instance",
                    "operation_identity",
                    "attempt_identity",
                    "inputs",
                    "selection",
                ),
            )
            record = TaskActivation(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskActivationIdentity
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_instance=self._exact(
                    self._decode(fields["task_instance"], seen), TaskInstance
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                inputs=tuple(
                    self._exact(item, TaskInputBinding)
                    for item in self._items(self._decode(fields["inputs"], seen))
                ),
                selection=self._parse_TaskActivation_selection(
                    self._decode(fields["selection"], seen)
                ),
            )
            return record
        if tag == "TaskActivationIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskActivationIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskAttempt":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "status",
                    "predecessor_attempt_record_identity",
                    "retry_of_attempt_identity",
                    "child_workflow_run_identity",
                ),
            )
            record = TaskAttempt(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskAttemptRecordIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                status=self._exact(
                    self._decode(fields["status"], seen), TaskAttemptStatus
                ),
                predecessor_attempt_record_identity=self._parse_TaskAttempt_predecessor_attempt_record_identity(
                    self._decode(fields["predecessor_attempt_record_identity"], seen)
                ),
                retry_of_attempt_identity=self._parse_TaskAttempt_retry_of_attempt_identity(
                    self._decode(fields["retry_of_attempt_identity"], seen)
                ),
                child_workflow_run_identity=self._parse_ResultDependency_producer_workflow_run_identity(
                    self._decode(fields["child_workflow_run_identity"], seen)
                ),
            )
            return record
        if tag == "TaskAttemptRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskAttemptRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskDefinitionIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskDefinitionIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskFailureRecord":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "task_instance_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "terminal_attempt_record_identity",
                    "failure",
                    "request_identity",
                    "child_workflow_run_identity",
                    "claim_boundary",
                ),
            )
            record = TaskFailureRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskFailureRecordIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                terminal_attempt_record_identity=self._exact(
                    self._decode(fields["terminal_attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                failure=self._exact(
                    self._decode(fields["failure"], seen), TaskInvocationFailure
                ),
                request_identity=self._parse_TaskFailureRecord_request_identity(
                    self._decode(fields["request_identity"], seen)
                ),
                child_workflow_run_identity=self._parse_ResultDependency_producer_workflow_run_identity(
                    self._decode(fields["child_workflow_run_identity"], seen)
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "TaskFailureRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskFailureRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskGateSelection":
            fields = self._fields(wire, tag, ("gate_identity", "binding"))
            record = TaskGateSelection(
                gate_identity=self._exact(
                    self._decode(fields["gate_identity"], seen), TaskStartGateIdentity
                ),
                binding=self._exact(
                    self._decode(fields["binding"], seen), ColoredPetriNetBinding
                ),
            )
            return record
        if tag == "TaskInputBinding":
            fields = self._fields(wire, tag, ("name", "result"))
            record = TaskInputBinding(
                name=self._exact(self._decode(fields["name"], seen), str),
                result=self._as_result(self._decode(fields["result"], seen)),
            )
            return record
        if tag == "TaskInstance":
            fields = self._fields(
                wire, tag, ("identity", "definition_identity", "start_gate_set")
            )
            record = TaskInstance(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskInstanceIdentity
                ),
                definition_identity=self._exact(
                    self._decode(fields["definition_identity"], seen),
                    TaskDefinitionIdentity,
                ),
                start_gate_set=self._parse_TaskInstance_start_gate_set(
                    self._decode(fields["start_gate_set"], seen)
                ),
            )
            return record
        if tag == "TaskInstanceIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskInstanceIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskInvocationFailure":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "code",
                    "operation_phase",
                    "diagnostic",
                    "retryable",
                    "claim_boundary",
                ),
            )
            record = TaskInvocationFailure(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskInvocationFailureIdentity,
                ),
                code=self._exact(self._decode(fields["code"], seen), str),
                operation_phase=self._exact(
                    self._decode(fields["operation_phase"], seen), str
                ),
                diagnostic=self._exact(self._decode(fields["diagnostic"], seen), str),
                retryable=self._parse_TaskInvocationFailure_retryable(
                    self._decode(fields["retryable"], seen)
                ),
                claim_boundary=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["claim_boundary"], seen)
                    )
                ),
            )
            return record
        if tag == "TaskInvocationFailureIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskInvocationFailureIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskInvocationOutcome":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "terminal_attempt_record_identity",
                    "kind",
                    "results",
                    "production_record_identities",
                    "failure_record_identity",
                    "dispatch_outcome_record_identity",
                    "reconciliation_identity_values",
                ),
            )
            record = TaskInvocationOutcome(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskInvocationOutcomeIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                terminal_attempt_record_identity=self._exact(
                    self._decode(fields["terminal_attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                kind=self._exact(
                    self._decode(fields["kind"], seen), TaskInvocationOutcomeKind
                ),
                results=tuple(
                    self._exact(item, ResultObjectReference)
                    for item in self._items(self._decode(fields["results"], seen))
                ),
                production_record_identities=tuple(
                    self._exact(item, ResultProductionRecordIdentity)
                    for item in self._items(
                        self._decode(fields["production_record_identities"], seen)
                    )
                ),
                failure_record_identity=self._parse_DispatchOutcomeRecord_failure_record_identity(
                    self._decode(fields["failure_record_identity"], seen)
                ),
                dispatch_outcome_record_identity=self._parse_TaskInvocationOutcome_dispatch_outcome_record_identity(
                    self._decode(fields["dispatch_outcome_record_identity"], seen)
                ),
                reconciliation_identity_values=tuple(
                    self._exact(item, str)
                    for item in self._items(
                        self._decode(fields["reconciliation_identity_values"], seen)
                    )
                ),
            )
            return record
        if tag == "TaskInvocationOutcomeIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskInvocationOutcomeIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskStartGate":
            fields = self._fields(
                wire, tag, ("identity", "priority", "transition_identity")
            )
            record = TaskStartGate(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskStartGateIdentity
                ),
                priority=self._exact(self._decode(fields["priority"], seen), int),
                transition_identity=self._exact(
                    self._decode(fields["transition_identity"], seen),
                    ColoredPetriNetTransitionIdentity,
                ),
            )
            return record
        if tag == "TaskStartGateIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskStartGateIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskStartGateSet":
            fields = self._fields(wire, tag, ("identity", "mode", "gates"))
            record = TaskStartGateSet(
                identity=self._exact(
                    self._decode(fields["identity"], seen), TaskStartGateSetIdentity
                ),
                mode=self._exact(
                    self._decode(fields["mode"], seen), TaskStartGateSetMode
                ),
                gates=tuple(
                    self._exact(item, TaskStartGate)
                    for item in self._items(self._decode(fields["gates"], seen))
                ),
            )
            return record
        if tag == "TaskStartGateSetIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskStartGateSetIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskWorkflowMembership":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "workflow_run_identity",
                    "workflow_identity",
                    "task_instance_identity",
                ),
            )
            record = TaskWorkflowMembership(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskWorkflowMembershipIdentity,
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                task_instance_identity=self._exact(
                    self._decode(fields["task_instance_identity"], seen),
                    TaskInstanceIdentity,
                ),
            )
            return record
        if tag == "TaskWorkflowMembershipIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskWorkflowMembershipIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        if tag == "TaskWorkflowTransitionRecord":
            fields = self._fields(
                wire,
                tag,
                (
                    "identity",
                    "sequence_identity",
                    "sequence_index",
                    "workflow_identity",
                    "workflow_run_identity",
                    "definition_reference_identity",
                    "runtime_bundle_identity",
                    "activation_identity",
                    "operation_identity",
                    "attempt_identity",
                    "terminal_attempt_record_identity",
                    "outcome_identity",
                    "result_production_identities",
                    "firing_result",
                    "request_correlation_identity",
                    "dispatch_outcome_record_identity",
                ),
            )
            record = TaskWorkflowTransitionRecord(
                identity=self._exact(
                    self._decode(fields["identity"], seen),
                    TaskWorkflowTransitionRecordIdentity,
                ),
                sequence_identity=self._exact(
                    self._decode(fields["sequence_identity"], seen),
                    WorkflowTransitionSequenceIdentity,
                ),
                sequence_index=self._exact(
                    self._decode(fields["sequence_index"], seen), int
                ),
                workflow_identity=self._exact(
                    self._decode(fields["workflow_identity"], seen), WorkflowIdentity
                ),
                workflow_run_identity=self._exact(
                    self._decode(fields["workflow_run_identity"], seen),
                    WorkflowRunIdentity,
                ),
                definition_reference_identity=self._exact(
                    self._decode(fields["definition_reference_identity"], seen),
                    WorkflowDefinitionReferenceIdentity,
                ),
                runtime_bundle_identity=self._exact(
                    self._decode(fields["runtime_bundle_identity"], seen),
                    WorkflowRuntimeBundleIdentity,
                ),
                activation_identity=self._exact(
                    self._decode(fields["activation_identity"], seen),
                    TaskActivationIdentity,
                ),
                operation_identity=self._exact(
                    self._decode(fields["operation_identity"], seen), OperationIdentity
                ),
                attempt_identity=self._exact(
                    self._decode(fields["attempt_identity"], seen), AttemptIdentity
                ),
                terminal_attempt_record_identity=self._exact(
                    self._decode(fields["terminal_attempt_record_identity"], seen),
                    TaskAttemptRecordIdentity,
                ),
                outcome_identity=self._exact(
                    self._decode(fields["outcome_identity"], seen),
                    TaskInvocationOutcomeIdentity,
                ),
                result_production_identities=tuple(
                    self._exact(item, ResultProductionRecordIdentity)
                    for item in self._items(
                        self._decode(fields["result_production_identities"], seen)
                    )
                ),
                firing_result=self._exact(
                    self._decode(fields["firing_result"], seen),
                    ColoredPetriNetFiringResult,
                ),
                request_correlation_identity=self._parse_TaskWorkflowTransitionRecord_request_correlation_identity(
                    self._decode(fields["request_correlation_identity"], seen)
                ),
                dispatch_outcome_record_identity=self._parse_TaskInvocationOutcome_dispatch_outcome_record_identity(
                    self._decode(fields["dispatch_outcome_record_identity"], seen)
                ),
            )
            return record
        if tag == "TaskWorkflowTransitionRecordIdentity":
            fields = self._fields(wire, tag, ("value",))
            record = TaskWorkflowTransitionRecordIdentity(
                value=self._exact(self._decode(fields["value"], seen), str),
            )
            return record
        raise _WorkflowRunWireUnsupported

    def _parse_TaskActivation_selection(
        self, value: _RunValue
    ) -> (
        DirectTaskActivationSelection
        | AnyOfTaskActivationSelection
        | AllOfTaskActivationSelection
    ):
        if type(value) is DirectTaskActivationSelection:
            return self._exact(value, DirectTaskActivationSelection)
        if type(value) is AnyOfTaskActivationSelection:
            return self._exact(value, AnyOfTaskActivationSelection)
        if type(value) is AllOfTaskActivationSelection:
            return self._exact(value, AllOfTaskActivationSelection)
        raise TypeError("wrong closed field variant")

    def _parse_TaskAttempt_predecessor_attempt_record_identity(
        self, value: _RunValue
    ) -> TaskAttemptRecordIdentity | None:
        if type(value) is TaskAttemptRecordIdentity:
            return self._exact(value, TaskAttemptRecordIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskAttempt_retry_of_attempt_identity(
        self, value: _RunValue
    ) -> AttemptIdentity | None:
        if type(value) is AttemptIdentity:
            return self._exact(value, AttemptIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskFailureRecord_request_identity(
        self, value: _RunValue
    ) -> SimulationExecutionRequestIdentity | None:
        if type(value) is SimulationExecutionRequestIdentity:
            return self._exact(value, SimulationExecutionRequestIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskInstance_start_gate_set(
        self, value: _RunValue
    ) -> TaskStartGateSet | None:
        if type(value) is TaskStartGateSet:
            return self._exact(value, TaskStartGateSet)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskInvocationFailure_retryable(self, value: _RunValue) -> bool | None:
        if type(value) is bool:
            return self._exact(value, bool)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskInvocationOutcome_dispatch_outcome_record_identity(
        self, value: _RunValue
    ) -> DispatchOutcomeRecordIdentity | None:
        if type(value) is DispatchOutcomeRecordIdentity:
            return self._exact(value, DispatchOutcomeRecordIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")

    def _parse_TaskWorkflowTransitionRecord_request_correlation_identity(
        self, value: _RunValue
    ) -> SimulationExecutionRequestCorrelationIdentity | None:
        if type(value) is SimulationExecutionRequestCorrelationIdentity:
            return self._exact(value, SimulationExecutionRequestCorrelationIdentity)
        if value is None:
            return None
        raise TypeError("wrong closed field variant")
