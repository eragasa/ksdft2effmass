"""Private reusable CPN composition for logical DFT SCF, NSCF, and DOS Tasks.

The composition is effect-free.  It defines three independent reusable Task
identities and their result-availability topology, but performs no Task invocation,
calculator execution, persistence, retry, parsing, convergence decision, or
scientific acceptance.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetArcDefinition,
    ColoredPetriNetArcIdentity,
    ColoredPetriNetBindingVariableIdentity,
    ColoredPetriNetColorDefinition,
    ColoredPetriNetColorIdentity,
    ColoredPetriNetDefinition,
    ColoredPetriNetDefinitionIdentity,
    ColoredPetriNetGuardExpression,
    ColoredPetriNetGuardOperator,
    ColoredPetriNetInputInscription,
    ColoredPetriNetInputMode,
    ColoredPetriNetOutputInscription,
    ColoredPetriNetPlaceDefinition,
    ColoredPetriNetPlaceIdentity,
    ColoredPetriNetTokenPattern,
    ColoredPetriNetTokenTemplate,
    ColoredPetriNetTransitionDefinition,
    ColoredPetriNetTransitionIdentity,
    ColoredPetriNetValueExpression,
    ColoredPetriNetValueExpressionKind,
    ColoredPetriNetValueKind,
)

from .model import (
    TaskDefinitionIdentity,
    TaskInstance,
    TaskInstanceIdentity,
    TaskStartGate,
    TaskStartGateIdentity,
    TaskStartGateSet,
    TaskStartGateSetIdentity,
    TaskStartGateSetMode,
    WorkflowComposition,
    WorkflowIdentity,
)


@dataclass(frozen=True, slots=True)
class DftScfNscfDosCpnCompositionInput:
    """Run-scoped identities for three independent operation Task instances."""

    scf_task_instance_identity: TaskInstanceIdentity
    nscf_task_instance_identity: TaskInstanceIdentity
    dos_task_instance_identity: TaskInstanceIdentity

    def __post_init__(self) -> None:
        """Require exact nominal and distinct Task-instance identities."""
        values = (
            self.scf_task_instance_identity,
            self.nscf_task_instance_identity,
            self.dos_task_instance_identity,
        )
        if any(type(value) is not TaskInstanceIdentity for value in values):
            raise TypeError("Task instance identities must be TaskInstanceIdentity")
        if len(set(values)) != 3:
            raise ValueError("SCF, NSCF, and DOS Task instance identities must differ")


@dataclass(frozen=True, slots=True)
class DftCpnTaskTransitionBinding:
    """Workflow-owned correlation of one Task instance to one CPN transition."""

    task_instance_identity: TaskInstanceIdentity
    transition_identity: ColoredPetriNetTransitionIdentity

    def __post_init__(self) -> None:
        """Validate the exact correlation field types."""
        if type(self.task_instance_identity) is not TaskInstanceIdentity:
            raise TypeError("task_instance_identity must be TaskInstanceIdentity")
        if type(self.transition_identity) is not ColoredPetriNetTransitionIdentity:
            raise TypeError(
                "transition_identity must be ColoredPetriNetTransitionIdentity"
            )


@dataclass(frozen=True, slots=True)
class DftScfNscfDosCpnCompositionResult:
    """Effect-free reusable Task and CPN topology composition result."""

    workflow_composition: WorkflowComposition
    definition: ColoredPetriNetDefinition
    task_transition_bindings: tuple[DftCpnTaskTransitionBinding, ...]

    def __post_init__(self) -> None:
        """Validate the immutable result field types."""
        if type(self.workflow_composition) is not WorkflowComposition:
            raise TypeError("workflow_composition must be WorkflowComposition")
        if type(self.definition) is not ColoredPetriNetDefinition:
            raise TypeError("definition must be ColoredPetriNetDefinition")
        if type(self.task_transition_bindings) is not tuple or any(
            type(value) is not DftCpnTaskTransitionBinding
            for value in self.task_transition_bindings
        ):
            raise TypeError(
                "task_transition_bindings must be a tuple of "
                "DftCpnTaskTransitionBinding"
            )


class DftScfNscfDosCpnComposer:
    """Compose independent reusable SCF, NSCF, and DOS Tasks with a pure CPN."""

    def execute(
        self, composition_input: DftScfNscfDosCpnCompositionInput
    ) -> DftScfNscfDosCpnCompositionResult:
        """Return the exact three-Task composition and dependency definition."""
        if type(composition_input) is not DftScfNscfDosCpnCompositionInput:
            raise TypeError(
                "composition_input must be DftScfNscfDosCpnCompositionInput"
            )
        transitions = {
            name: ColoredPetriNetTransitionIdentity(f"dft.{name}")
            for name in ("scf", "nscf", "dos")
        }
        task_instances = (
            TaskInstance(
                composition_input.scf_task_instance_identity,
                TaskDefinitionIdentity("dft.scf"),
                None,
            ),
            TaskInstance(
                composition_input.nscf_task_instance_identity,
                TaskDefinitionIdentity("dft.nscf"),
                TaskStartGateSet(
                    TaskStartGateSetIdentity("dft.nscf.after-scf"),
                    TaskStartGateSetMode.ALL_OF,
                    (
                        TaskStartGate(
                            TaskStartGateIdentity("dft.nscf.scf-result"),
                            0,
                            transitions["nscf"],
                        ),
                    ),
                ),
            ),
            TaskInstance(
                composition_input.dos_task_instance_identity,
                TaskDefinitionIdentity("dft.dos"),
                TaskStartGateSet(
                    TaskStartGateSetIdentity("dft.dos.after-nscf"),
                    TaskStartGateSetMode.ALL_OF,
                    (
                        TaskStartGate(
                            TaskStartGateIdentity("dft.dos.nscf-result"),
                            0,
                            transitions["dos"],
                        ),
                    ),
                ),
            ),
        )
        workflow_identity = WorkflowIdentity("dft.scf-nscf-dos.v1")
        composition = WorkflowComposition(workflow_identity, task_instances)
        definition = self._definition(transitions)
        bindings = tuple(
            DftCpnTaskTransitionBinding(instance.identity, transitions[name])
            for instance, name in zip(
                task_instances, ("scf", "nscf", "dos"), strict=True
            )
        )
        return DftScfNscfDosCpnCompositionResult(
            composition,
            definition,
            bindings,
        )

    @classmethod
    def _definition(
        cls,
        transitions: dict[str, ColoredPetriNetTransitionIdentity],
    ) -> ColoredPetriNetDefinition:
        """Build the reusable three-transition result-availability topology."""
        color = ColoredPetriNetColorDefinition(
            ColoredPetriNetColorIdentity("workflow-result-identity"),
            (ColoredPetriNetValueKind.STRING,),
        )
        places = {
            name: ColoredPetriNetPlaceDefinition(
                ColoredPetriNetPlaceIdentity(name), (color.identity,)
            )
            for name in (
                "scf.prepared",
                "scf.completed",
                "nscf.prepared",
                "nscf.completed",
                "dos.prepared",
                "dos.completed",
            )
        }
        variables = {
            name: ColoredPetriNetBindingVariableIdentity(name)
            for name in (
                "scf_input",
                "scf_output",
                "nscf_input",
                "nscf_output",
                "dos_input",
                "dos_output",
            )
        }
        always = ColoredPetriNetGuardExpression(ColoredPetriNetGuardOperator.TRUE)
        definitions = {
            "scf": ColoredPetriNetTransitionDefinition(
                transitions["scf"],
                (variables["scf_input"],),
                (variables["scf_output"],),
                always,
            ),
            "nscf": ColoredPetriNetTransitionDefinition(
                transitions["nscf"],
                (variables["scf_output"], variables["nscf_input"]),
                (variables["nscf_output"],),
                always,
            ),
            "dos": ColoredPetriNetTransitionDefinition(
                transitions["dos"],
                (variables["nscf_output"], variables["dos_input"]),
                (variables["dos_output"],),
                always,
            ),
        }
        arcs = (
            cls._input_arc(
                "scf.input",
                places["scf.prepared"],
                definitions["scf"],
                variables["scf_input"],
                color,
                ColoredPetriNetInputMode.CONSUME,
            ),
            cls._output_arc(
                "scf.output",
                places["scf.completed"],
                definitions["scf"],
                variables["scf_output"],
                color,
            ),
            cls._input_arc(
                "nscf.scf-state",
                places["scf.completed"],
                definitions["nscf"],
                variables["scf_output"],
                color,
                ColoredPetriNetInputMode.READ,
            ),
            cls._input_arc(
                "nscf.input",
                places["nscf.prepared"],
                definitions["nscf"],
                variables["nscf_input"],
                color,
                ColoredPetriNetInputMode.CONSUME,
            ),
            cls._output_arc(
                "nscf.output",
                places["nscf.completed"],
                definitions["nscf"],
                variables["nscf_output"],
                color,
            ),
            cls._input_arc(
                "dos.nscf-state",
                places["nscf.completed"],
                definitions["dos"],
                variables["nscf_output"],
                color,
                ColoredPetriNetInputMode.READ,
            ),
            cls._input_arc(
                "dos.input",
                places["dos.prepared"],
                definitions["dos"],
                variables["dos_input"],
                color,
                ColoredPetriNetInputMode.CONSUME,
            ),
            cls._output_arc(
                "dos.output",
                places["dos.completed"],
                definitions["dos"],
                variables["dos_output"],
                color,
            ),
        )
        return ColoredPetriNetDefinition(
            ColoredPetriNetDefinitionIdentity("dft.scf-nscf-dos.v1"),
            (color,),
            tuple(places.values()),
            tuple(definitions.values()),
            arcs,
            tuple(transitions.values()),
        )

    @staticmethod
    def _input_arc(
        identity: str,
        place: ColoredPetriNetPlaceDefinition,
        transition: ColoredPetriNetTransitionDefinition,
        variable: ColoredPetriNetBindingVariableIdentity,
        color: ColoredPetriNetColorDefinition,
        mode: ColoredPetriNetInputMode,
    ) -> ColoredPetriNetArcDefinition:
        """Build one exact input arc for the private composition."""
        return ColoredPetriNetArcDefinition(
            ColoredPetriNetArcIdentity(identity),
            place.identity,
            transition.identity,
            ColoredPetriNetInputInscription(
                mode,
                (ColoredPetriNetTokenPattern(variable, (color.identity,)),),
            ),
        )

    @staticmethod
    def _output_arc(
        identity: str,
        place: ColoredPetriNetPlaceDefinition,
        transition: ColoredPetriNetTransitionDefinition,
        variable: ColoredPetriNetBindingVariableIdentity,
        color: ColoredPetriNetColorDefinition,
    ) -> ColoredPetriNetArcDefinition:
        """Build one exact externally supplied result-output arc."""
        expression = ColoredPetriNetValueExpression(
            ColoredPetriNetValueExpressionKind.VARIABLE,
            variable_identity=variable,
        )
        return ColoredPetriNetArcDefinition(
            ColoredPetriNetArcIdentity(identity),
            place.identity,
            transition.identity,
            output_inscription=ColoredPetriNetOutputInscription(
                (
                    ColoredPetriNetTokenTemplate(
                        color.identity,
                        expression,
                        expression,
                    ),
                )
            ),
        )
