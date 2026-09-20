r"""Software verification of ``WorkflowRunSerializer``.

Evidence profile: claim_bearing

Bounded artifact scope: optional collection grammar and independent nested record wires.

Facet and represented meaning

One v1 wire omits both empty new collections, or includes both when either is
nonempty. Independent literal record fragments are not produced by this serializer.

Intrinsic and cross-object scope

These are representation graphs, intentionally not structurally closed histories.
Actual SQLite lifecycle evidence belongs to the atomic repository facet.

VVUQ and scientific exclusions

Synthetic labels establish no retained intent, child replay, effects or science.
"""

from dataclasses import replace
from pathlib import Path
from typing import Literal

import pytest

from ksdft2effmass import workflows as w
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoResultValueSerializer,
)
from ksdft2effmass.workflows import WorkflowRunSerializer

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer

type Variant = Literal["intent", "confirmed", "rejected", "indeterminate"]


class TestWorkflowRunSerializerNestedExtension:
    """Own exact same-v1 spelling and typed reconstruction evidence."""

    @staticmethod
    def make_serializer() -> WorkflowRunSerializer:
        return SUT(
            result_codec=w.WorkflowResultValueSerializer(
                source_codec=QuantumEspressoResultValueSerializer()
            )
        )

    @staticmethod
    def literal(name: str) -> bytes:
        return Path(__file__).with_name("resources").joinpath(name).read_bytes()

    @classmethod
    def extended_wire(cls, variant: Variant) -> bytes:
        """Insert literal fragments in specified lexical field-name order."""
        intent = cls.literal("nested-intent-v1.json")
        terminal = (
            b""
            if variant == "intent"
            else cls.literal(f"nested-terminal-{variant}-v1.json")
        )
        return (
            cls.literal("genesis-record-envelope.json")
            .replace(
                b'"nested_invocations":[]',
                b'"nested_invocation_intents":['
                + intent
                + b'],"nested_invocations":[]',
            )
            .replace(
                b'"nested_memberships":[]',
                b'"nested_memberships":[],"nested_terminal_observations":['
                + terminal
                + b"]",
            )
        )

    @staticmethod
    def intent() -> w.NestedWorkflowInvocationIntent:
        return w.NestedWorkflowInvocationIntent(
            identity=w.NestedWorkflowInvocationIntentIdentity("intent"),
            parent_workflow_run_identity=w.WorkflowRunIdentity("run"),
            parent_revision_identity=w.WorkflowRunRevisionIdentity("genesis"),
            parent_task_instance_identity=w.TaskInstanceIdentity("task"),
            activation_identity=w.TaskActivationIdentity("activation"),
            operation_identity=w.OperationIdentity("operation"),
            attempt_identity=w.AttemptIdentity("attempt"),
            started_attempt_record_identity=w.TaskAttemptRecordIdentity("started"),
            child_workflow_identity=w.WorkflowIdentity("child.workflow"),
            child_workflow_run_identity=w.WorkflowRunIdentity("child"),
            input_result_reference_identities=(),
            child_creation_idempotency_identity=w.ChildWorkflowCreationIdempotencyIdentity(
                "create"
            ),
        )

    @staticmethod
    def observation(
        variant: Literal["confirmed", "rejected", "indeterminate"],
    ) -> w.NestedWorkflowTerminalObservation:
        return w.NestedWorkflowTerminalObservation(
            identity=w.NestedWorkflowObservationIdentity("observation"),
            intent_identity=w.NestedWorkflowInvocationIntentIdentity("intent"),
            parent_workflow_run_identity=w.WorkflowRunIdentity("run"),
            parent_revision_identity=w.WorkflowRunRevisionIdentity("terminal"),
            terminal_attempt_record_identity=w.TaskAttemptRecordIdentity(
                "terminal.attempt"
            ),
            outcome_identity=w.TaskInvocationOutcomeIdentity("outcome"),
            kind=w.NestedWorkflowTerminalObservationKind(variant),
            terminal_child_revision_identity=w.WorkflowRunRevisionIdentity(
                "child.terminal"
            )
            if variant == "confirmed"
            else None,
            replay_equal_child_result_identity=w.WorkflowRunReplayResultIdentity(
                "c" * 64
            )
            if variant == "confirmed"
            else None,
            exported_result_reference_identities=(
                w.ResultObjectReferenceIdentity("export"),
            )
            if variant == "confirmed"
            else (),
            export_admission_dependency_identities=(
                w.ResultDependencyIdentity("admission"),
            )
            if variant == "confirmed"
            else (),
            failure_record_identity=w.TaskFailureRecordIdentity("failure")
            if variant == "rejected"
            else None,
            reconciliation_identity_values=("child.read",)
            if variant == "indeterminate"
            else (),
        )

    @pytest.mark.parametrize(
        "variant",
        (
            pytest.param("intent", id="intent_only"),
            pytest.param("confirmed", id="confirmed_exports"),
            pytest.param("rejected", id="rejected_failure"),
            pytest.param("indeterminate", id="indeterminate_reconciliation"),
        ),
    )
    def test_method__serialize__matches_independent_extension(
        self,
        genesis_run: w.WorkflowRun,
        genesis_snapshot: w.WorkflowRunSnapshot,
        variant: Variant,
    ) -> None:
        """Encode complete nominal records into the one canonical v1 extension.

        Evidence ID: SV-WFR-SERIALIZER-NESTED-EXTENSION-001

        Requirement: Nonempty new collections use the exact 36-field v1 shape
        with both keys and complete explicit record tags, without changing bindings.

        Method: Construct expected records publicly, encode, and independently decode
        handwritten literal fragments embedded in the fixed original genesis wire.

        Oracle: Literal bytes and the independently constructed complete record graph.

        Acceptance: Exact encoded byte equality and reconstructed new tuple equality;
        the original schema identity and commit binding are unchanged.

        Interpretation: The extension is canonical representation, not a migration.

        Limitations: The fixture is deliberately not a closed retained history.
        """
        observations = () if variant == "intent" else (self.observation(variant),)
        run = replace(
            genesis_run,
            nested_invocation_intents=(self.intent(),),
            nested_terminal_observations=observations,
        )
        wire = self.extended_wire(variant)
        serializer = self.make_serializer()
        encoded = serializer.serialize(run, genesis_snapshot.binding)
        assert encoded.encoded is not None, encoded.failure
        assert encoded.encoded.payload == wire
        assert encoded.encoded.schema_identity == "ksdft2effmass.workflow-run:1"
        decoded = serializer.deserialize(wire)
        assert decoded.run is not None, decoded.failure
        assert decoded.binding == genesis_snapshot.binding
        assert decoded.run.nested_invocation_intents == run.nested_invocation_intents
        assert decoded.run.nested_terminal_observations == observations

    def test_method__serialize__preserves_original_unextended_bytes(
        self, genesis_run: w.WorkflowRun, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Omit both empty collections and preserve the existing envelope exactly.

        Evidence ID: SV-WFR-SERIALIZER-NESTED-EXTENSION-002

        Requirement: Both empty default tuples retain the original 34-field wire.

        Method: Encode explicit empty tuples and decode the original literal.

        Oracle: The pre-correction immutable genesis envelope bytes.

        Acceptance: Exact byte equality and both decoded new tuples empty.

        Interpretation: Old stored bytes need no rewriting or invented intent.

        Limitations: One fixed envelope; other old literals have separate owners.
        """
        serializer = self.make_serializer()
        encoded = serializer.serialize(
            replace(
                genesis_run,
                nested_invocation_intents=(),
                nested_terminal_observations=(),
            ),
            genesis_snapshot.binding,
        )
        assert encoded.encoded is not None
        wire = self.literal("genesis-record-envelope.json")
        assert encoded.encoded.payload == wire
        decoded = serializer.deserialize(wire)
        assert decoded.run is not None
        assert decoded.run.nested_invocation_intents == ()
        assert decoded.run.nested_terminal_observations == ()

    def test_method__serialize__preserves_combined_intent_reference(
        self, genesis_run: w.WorkflowRun, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Represent an observation-only extension with the old nominal source tag.

        Evidence ID: SV-WFR-SERIALIZER-NESTED-EXTENSION-004

        Requirement: Observation-only extensions include both collection keys and
        preserve a combined-invocation identity rather than inventing a new intent.

        Method: Replace the nominal tag in the independent observation literal and
        remove its unrelated new intent, then compare a public constructor graph.

        Oracle: The literal old nominal tag, empty intent array and exact bytes.

        Acceptance: Encoding matches the independent wire and decoding retains the
        combined identity type with no synthesized intent records.

        Interpretation: Nominal alternatives survive same-v1 serialization.

        Limitations: This representation-only fixture does not contain a real source.
        """
        wire = (
            self.extended_wire("confirmed")
            .replace(
                b'"nested_invocation_intents":['
                + self.literal("nested-intent-v1.json")
                + b"]",
                b'"nested_invocation_intents":[]',
            )
            .replace(
                b'"NestedWorkflowInvocationIntentIdentity"',
                b'"NestedWorkflowInvocationIdentity"',
            )
        )
        observation = replace(
            self.observation("confirmed"),
            intent_identity=w.NestedWorkflowInvocationIdentity("intent"),
        )
        run = replace(genesis_run, nested_terminal_observations=(observation,))
        encoded = self.make_serializer().serialize(run, genesis_snapshot.binding)
        assert encoded.encoded is not None
        assert encoded.encoded.payload == wire
        decoded = self.make_serializer().deserialize(wire)
        assert decoded.run is not None
        assert decoded.run.nested_invocation_intents == ()
        assert decoded.run.nested_terminal_observations == (observation,)

    @pytest.mark.parametrize(
        "mutation",
        (
            pytest.param("only_intents", id="missing_observation_key"),
            pytest.param("only_observations", id="missing_intent_key"),
            pytest.param("both_empty", id="noncanonical_empty_extension"),
            pytest.param("wrong_tuple", id="noncollection_intents"),
            pytest.param("unknown_key", id="unknown_aggregate_member"),
            pytest.param("wrong_nominal", id="wrong_intent_reference_nominal"),
            pytest.param("missing_record_field", id="incomplete_intent_record"),
        ),
    )
    def test_method__deserialize__rejects_noncanonical_extension(
        self,
        mutation: Literal[
            "only_intents",
            "only_observations",
            "both_empty",
            "wrong_tuple",
            "unknown_key",
            "wrong_nominal",
            "missing_record_field",
        ],
    ) -> None:
        """Reject incomplete, untyped and noncanonical same-v1 spellings.

        Evidence ID: SV-WFR-SERIALIZER-NESTED-EXTENSION-003

        Requirement: Exactly both extension members are present when needed, every
        nested field is typed and complete, and both empty arrays are omitted.

        Method: Apply one exact byte mutation to independent literal wires.

        Oracle: Corrupt without a partial run or binding.

        Acceptance: Every mutation changes the input and returns corrupt with no run.

        Interpretation: The extension does not create alternative canonical spellings.

        Limitations: No history closure, child replay or authority is established.
        """
        original = self.extended_wire("confirmed")
        match mutation:
            case "only_intents":
                wire = original.replace(
                    b',"nested_terminal_observations":['
                    + self.literal("nested-terminal-confirmed-v1.json")
                    + b"]",
                    b"",
                )
            case "only_observations":
                wire = original.replace(
                    b'"nested_invocation_intents":['
                    + self.literal("nested-intent-v1.json")
                    + b"],",
                    b"",
                )
            case "both_empty":
                wire = (
                    self.literal("genesis-record-envelope.json")
                    .replace(
                        b'"nested_invocations":[]',
                        b'"nested_invocation_intents":[],"nested_invocations":[]',
                    )
                    .replace(
                        b'"nested_memberships":[]',
                        b'"nested_memberships":[],"nested_terminal_observations":[]',
                    )
                )
            case "wrong_tuple":
                wire = original.replace(
                    b'"nested_invocation_intents":['
                    + self.literal("nested-intent-v1.json")
                    + b"]",
                    b'"nested_invocation_intents":true',
                )
            case "unknown_key":
                wire = original.replace(
                    b'"nested_invocations":[]', b'"nested_invocations":[],"unknown":[]'
                )
            case "wrong_nominal":
                wire = original.replace(
                    b'"intent_identity":{"fields":{"value":"intent"},"type":"NestedWorkflowInvocationIntentIdentity"}',
                    b'"intent_identity":{"fields":{"value":"intent"},"type":"WorkflowRunIdentity"}',
                )
            case "missing_record_field":
                wire = original.replace(
                    b',"started_attempt_record_identity":{"fields":{"value":"started"},"type":"TaskAttemptRecordIdentity"}',
                    b"",
                )
        assert wire != original
        result = self.make_serializer().deserialize(wire)
        assert result.status == "corrupt", result.failure
        assert result.run is None and result.binding is None
