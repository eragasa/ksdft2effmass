r"""Software verification of ``WorkflowRunSerializer``.

Bounded artifact scope: direct, any-of and all-of Task activation representations.

Evidence profile: claim_bearing

Facet and represented meaning

One independent literal retains absent/empty gate sets, both automatic modes,
priority ties, gate storage versus selection order and ordered concrete inputs.

Intrinsic and cross-object scope

Public constructor graphs and fixed bytes are separate oracles. These records do
not establish enablement, automatic selection, Task invocation or history closure.

VVUQ and scientific exclusions

Synthetic software verification only; supplied selections and scalar values are
not computed firing, scientific results, authority or accepted evidence.
"""

from dataclasses import replace
from pathlib import Path
from typing import Literal

import pytest
from ksdft2effmass import analysis as q
from ksdft2effmass import workflows as w
from ksdft2effmass.petrinet import colored as c
from ksdft2effmass.workflows import WorkflowRunSerializer

type TaskKind = Literal["all", "any", "direct", "empty-all", "empty-any"]

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunSerializer


class TestWorkflowRunSerializer:
    """Own complete Task-model wires, not Task-selection policy evidence."""

    @staticmethod
    def wire() -> bytes:
        return (
            Path(__file__)
            .with_name("resources")
            .joinpath("workflow-run-task-model-v1.json")
            .read_bytes()
        )

    @staticmethod
    def make_scalar(identity: str, value: float) -> q.ScalarQuantityOfInterestValue:
        evaluator = q.QuantityOfInterestEvaluatorIdentity("synthetic-evaluator:7")
        return q.ScalarQuantityOfInterestValue(
            w.ResultObjectIdentity(identity),
            q.ScalarQuantityOfInterestDefinition(
                q.QuantityOfInterestIdentity("synthetic-qoi"),
                q.QuantityOfInterestSubjectIdentity("synthetic-subject"),
                q.QuantityOfInterestStateSpaceIdentity("synthetic-space"),
                q.QuantityOfInterestConventionIdentity("synthetic-convention"),
                evaluator,
                (
                    q.NormalizedObservationRequirementIdentity("second"),
                    q.NormalizedObservationRequirementIdentity("first"),
                ),
                q.QuantityOfInterestCompleteness.COMPLETE,
                "synthetic-unit",
            ),
            w.ResultObjectIdentity("synthetic-observations"),
            evaluator,
            value,
        )

    @staticmethod
    def make_task(kind: TaskKind) -> w.TaskInstance:
        gates = (
            w.TaskStartGate(
                w.TaskStartGateIdentity("gate-b"),
                5,
                c.ColoredPetriNetTransitionIdentity("transition-b"),
            ),
            w.TaskStartGate(
                w.TaskStartGateIdentity("gate-z"),
                0,
                c.ColoredPetriNetTransitionIdentity("transition-z"),
            ),
            w.TaskStartGate(
                w.TaskStartGateIdentity("gate-a"),
                5,
                c.ColoredPetriNetTransitionIdentity("transition-a"),
            ),
        )
        gate_set = (
            None
            if kind == "direct"
            else w.TaskStartGateSet(
                w.TaskStartGateSetIdentity(f"set-{kind}"),
                w.TaskStartGateSetMode.ALL_OF
                if kind in ("all", "empty-all")
                else w.TaskStartGateSetMode.ANY_OF,
                gates if kind in ("all", "any") else (),
            )
        )
        return w.TaskInstance(
            w.TaskInstanceIdentity(kind),
            w.TaskDefinitionIdentity("task-definition"),
            gate_set,
        )

    @staticmethod
    def make_selection(kind: TaskKind) -> w.TaskActivationSelection:
        identity = c.ColoredPetriNetSelectionResultIdentity("a" * 64)
        if kind == "any":
            return w.AnyOfTaskActivationSelection(
                w.TaskStartGateSetIdentity("set-any"),
                w.TaskGateSelection(
                    w.TaskStartGateIdentity("gate-b"),
                    c.ColoredPetriNetBinding(
                        c.ColoredPetriNetTransitionIdentity("transition-b"), ()
                    ),
                ),
                identity,
            )
        if kind == "all":
            return w.AllOfTaskActivationSelection(
                w.TaskStartGateSetIdentity("set-all"),
                (
                    w.TaskGateSelection(
                        w.TaskStartGateIdentity("gate-z"),
                        c.ColoredPetriNetBinding(
                            c.ColoredPetriNetTransitionIdentity("transition-z"), ()
                        ),
                    ),
                    w.TaskGateSelection(
                        w.TaskStartGateIdentity("gate-a"),
                        c.ColoredPetriNetBinding(
                            c.ColoredPetriNetTransitionIdentity("transition-a"), ()
                        ),
                    ),
                    w.TaskGateSelection(
                        w.TaskStartGateIdentity("gate-b"),
                        c.ColoredPetriNetBinding(
                            c.ColoredPetriNetTransitionIdentity("transition-b"), ()
                        ),
                    ),
                ),
                identity,
            )
        return w.DirectTaskActivationSelection(identity)

    def make_activation(self, kind: TaskKind) -> w.TaskActivation:
        return w.TaskActivation(
            w.TaskActivationIdentity(f"activation-{kind}"),
            w.WorkflowIdentity("workflow"),
            w.WorkflowRunIdentity("run"),
            self.make_task(kind),
            w.OperationIdentity(f"operation-{kind}"),
            w.AttemptIdentity(f"attempt-{kind}"),
            (
                w.TaskInputBinding("z-input", self.make_scalar("other-result", 3.5)),
                w.TaskInputBinding(
                    "a-input", self.make_scalar("synthetic-result", -0.0)
                ),
            ),
            self.make_selection(kind),
        )

    def make_run(self, genesis: w.WorkflowRun) -> w.WorkflowRun:
        return replace(
            genesis,
            task_instances=(
                self.make_task("all"),
                self.make_task("any"),
                self.make_task("direct"),
                self.make_task("empty-all"),
                self.make_task("empty-any"),
            ),
            activations=(
                self.make_activation("all"),
                self.make_activation("any"),
                self.make_activation("direct"),
                self.make_activation("empty-all"),
                self.make_activation("empty-any"),
            ),
        )

    def test_method__serialize__matches_task_model_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-TASK-MODEL-001

        Requirement: Task representations preserve gate and input storage order.

        Method: Serialize a public constructor graph with every activation variant.

        Oracle: Independent literal, including nonlexical inputs and tied priorities.

        Acceptance: Entire canonical payload equals the literal bytes.

        Interpretation: All-of selection order is distinct from gate storage order;
        direct activation retains absent and both empty gate-set variants.

        Limitations: Supplied selections are not proof of computed enablement.
        """
        result = SUT(
            result_codec=q.QuantityOfInterestResultValueSerializer()
        ).serialize(self.make_run(genesis_snapshot.run), genesis_snapshot.binding)
        assert result.status == "encoded", result.failure
        assert result.encoded is not None and result.encoded.payload == self.wire()

    def test_method__deserialize__restores_task_model_literal(
        self, genesis_snapshot: w.WorkflowRunSnapshot
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-TASK-MODEL-002

        Requirement: Decode complete Task models, selections and concrete input values.

        Method: Decode fixed bytes and compare independently constructed public records.

        Oracle: Complete run and binding, including two distinct scalar input values.

        Acceptance: Entire run and commit binding compare equal.

        Interpretation: The codec neither sorts retained inputs nor selects a new gate.

        Limitations: No execution, automatic activation or history closure is tested.
        """
        result = SUT(
            result_codec=q.QuantityOfInterestResultValueSerializer()
        ).deserialize(self.wire())
        assert result.status == "decoded", result.failure
        assert result.run == self.make_run(genesis_snapshot.run)
        assert result.binding == genesis_snapshot.binding

    @pytest.mark.parametrize(
        ("original", "replacement"),
        [
            pytest.param(
                b'"priority":{"fields":{"value":"0x5"},"type":"int"}',
                b'"priority":true',
                id="boolean_gate_priority",
            ),
            pytest.param(
                b'"priority":{"fields":{"value":"0x5"},"type":"int"}',
                b'"priority":{"fields":{"value":"-0x1"},"type":"int"}',
                id="negative_gate_priority",
            ),
            pytest.param(
                b'"value":"gate-b"', b'"value":"gate-a"', id="duplicate_gate_identity"
            ),
            pytest.param(
                b'"identity":{"fields":{"value":"gate-b"},"type":"TaskStartGateIdentity"},"priority":{"fields":{"value":"0x5"},"type":"int"}',
                b'"identity":{"fields":{"value":"gate-b"},"type":"TaskStartGateIdentity"},"priority":{"fields":{"value":"0x1"},"type":"int"}',
                id="all_of_selection_order_stale_after_priority_change",
            ),
            pytest.param(
                b'"binding":{"fields":{"assignments":[],"transition_identity":{"fields":{"value":"transition-b"}',
                b'"binding":{"fields":{"assignments":[],"transition_identity":{"fields":{"value":"foreign-transition"}',
                id="selected_binding_transition_detached",
            ),
            pytest.param(
                b'"mode":{"fields":{"value":"all_of"},"type":"TaskStartGateSetMode"}',
                b'"mode":{"fields":{"value":"any_of"},"type":"TaskStartGateSetMode"}',
                id="all_of_mode_mismatch",
            ),
            pytest.param(
                b'"gate_set_identity":{"fields":{"value":"set-all"},"type":"TaskStartGateSetIdentity"}',
                b'"gate_set_identity":{"fields":{"value":"detached"},"type":"TaskStartGateSetIdentity"}',
                id="selected_gate_set_detached",
            ),
            pytest.param(
                b'"gates":[]',
                b'"gates":[{"fields":{"identity":{"fields":{"value":"new-gate"},"type":"TaskStartGateIdentity"},"priority":{"fields":{"value":"0x0"},"type":"int"},"transition_identity":{"fields":{"value":"new-transition"},"type":"ColoredPetriNetTransitionIdentity"}},"type":"TaskStartGate"}]',
                id="direct_activation_with_nonempty_gate_set",
            ),
            pytest.param(
                b'"name":"z-input"', b'"name":"a-input"', id="duplicate_input_name"
            ),
            pytest.param(b'"name":"z-input"', b'"name":""', id="empty_input_name"),
        ],
    )
    def test_method__deserialize__rejects_task_model_drift(
        self, original: bytes, replacement: bytes
    ) -> None:
        """Evidence ID: SV-WFR-SERIALIZER-TASK-MODEL-003

        Requirement: Task representations obey intrinsic composition correlations.

        Method: Mutate a named literal pattern without altering concrete envelopes.

        Oracle: Public priorities, unique gates/inputs and activation-selection rules.

        Acceptance: Corrupt failure with no partial run or binding.

        Interpretation: JSON validity does not bypass Task-model invariants.

        Limitations: No generic selection, firing or Task invocation is evaluated.
        """
        wire = self.wire()
        assert original in wire
        result = SUT(
            result_codec=q.QuantityOfInterestResultValueSerializer()
        ).deserialize(wire.replace(original, replacement))
        assert result.status == "corrupt"
        assert result.failure is not None
        assert result.run is None and result.binding is None
