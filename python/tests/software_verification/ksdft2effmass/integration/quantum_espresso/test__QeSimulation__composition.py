r"""Software verification of ``QeSimulation``.

Evidence profile: routine

Bounded artifact scope: immutable construction, exact component correlations, and
operation-specific result-role selection.

Facet and represented meaning

``QeSimulation`` represents application composition of one accepted QE
Task, its exact input and calculator, and a distinct Workflow dispatch-effect
executor.

Intrinsic and cross-object scope

The class is the sole system under test. Tests cover its intrinsic field types,
cross-field correlations, immutability, structural dependencies, and derived result
class. Package exports and inward dependency direction are owned by the contract
facet module.

VVUQ and scientific exclusions

These synthetic software checks invoke neither port and establish no execution
authority, numerical verification, scientific validation, uncertainty quantification,
convergence, physical correctness, production readiness, or human acceptance.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

import ksdft2effmass.integration.quantum_espresso as qe
import ksdft2effmass.workflows as workflows
from ksdft2effmass.calculators.dft.pw import PlaneWaveCalculator
from ksdft2effmass.integration.quantum_espresso import QeSimulation

pytestmark = pytest.mark.software_verification
SUT = QeSimulation


class TestQeSimulation:
    """Own software evidence for ``QeSimulation``."""

    @staticmethod
    def content(character: str, byte_count: int) -> workflows.ArtifactContentIdentity:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide one deterministic synthetic content identity.

        Acceptance: The returned value retains the supplied digest and byte count.
        """
        return workflows.ArtifactContentIdentity("sha256", character * 64, byte_count)

    @classmethod
    def execution_input(
        cls,
        *,
        definition: str,
        program: qe.QeProgram,
        with_predecessor: bool,
        suffix: str,
    ) -> qe.QeExecutionInput:
        """Evidence ID: This helper owns no identifier.

        Requirement: Build one exact synthetic QE operation input.

        Acceptance: The value retains the requested definition, program, predecessor
        shape, and run correlations.
        """
        predecessor_state = (
            (
                qe.QePredecessorNativeStateArtifact(
                    identity=workflows.ArtifactIdentity(f"state.{suffix}"),
                    content=qe.QeTreeArtifactContent(
                        workflows.ArtifactManifestIdentity(f"manifest.{suffix}"),
                        (
                            workflows.ArtifactManifestEntryIdentity(
                                f"manifest-entry.{suffix}"
                            ),
                        ),
                    ),
                    destination=qe.QeArtifactDestination(f"state/{suffix}.save"),
                    predecessor_result_identity=workflows.ResultObjectIdentity(
                        f"predecessor-result.{suffix}"
                    ),
                    predecessor_manifest_entry_identity=(
                        workflows.ArtifactManifestEntryIdentity(
                            f"manifest-entry.{suffix}"
                        )
                    ),
                ),
            )
            if with_predecessor
            else ()
        )
        return qe.QeExecutionInput(
            identity=qe.QeExecutionInputIdentity(f"input.{suffix}"),
            program=program,
            native_input=qe.QeNativeInputArtifact(
                workflows.ArtifactIdentity(f"native-input.{suffix}"),
                qe.QeFileArtifactContent(cls.content("a", 8)),
                qe.QeArtifactDestination(f"input/{suffix}.in"),
            ),
            pseudopotentials=(
                qe.QePseudopotentialArtifact(
                    workflows.ArtifactIdentity(f"pseudo.{suffix}"),
                    qe.QeFileArtifactContent(cls.content("b", 16)),
                    qe.QeArtifactDestination(f"pseudo/{suffix}.UPF"),
                ),
            ),
            predecessor_native_state=predecessor_state,
            task_definition_identity=workflows.TaskDefinitionIdentity(definition),
            task_instance_identity=workflows.TaskInstanceIdentity(
                f"task-instance.{suffix}"
            ),
            activation_identity=workflows.TaskActivationIdentity(
                f"activation.{suffix}"
            ),
            operation_identity=workflows.OperationIdentity(f"operation.{suffix}"),
            attempt_identity=workflows.AttemptIdentity(f"attempt.{suffix}"),
            contract_version="qe-execution-input:1",
        )

    @staticmethod
    def dispatch_effect() -> workflows.SimulationDispatchEffect:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide a structural effect that performs no execution.

        Acceptance: The returned value satisfies ``SimulationDispatchEffect`` and
        raises if a test incorrectly invokes it.
        """

        class NonInvokedEffect:
            @property
            def executor_identity(self) -> workflows.ScientificExecutorIdentity:
                return workflows.ScientificExecutorIdentity("executor.synthetic")

            def execute(
                self,
                request: workflows.SimulationDispatchEffectRequest,
            ) -> workflows.SimulationDispatchOutcome:
                raise AssertionError("Simulation composition must not invoke effects")

        return NonInvokedEffect()

    def test_constructor__composition__binds_exact_scf_components_immutably(
        self,
    ) -> None:
        """Evidence ID: SV-QE-SIM-002

        Requirement: One Simulation binds the identical calculator injected into its
        Task, the equal exact execution input, and one structural Workflow effect,
        without storing an output.

        Acceptance: Construction preserves object bindings, selects the ``pw`` result
        class, satisfies both structural ports, and rejects field reassignment.
        """

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                raise AssertionError(
                    "Simulation composition must not invoke calculators"
                )

        execution_input = self.execution_input(
            definition="quantum-espresso.scf.v1",
            program=qe.QeProgram.PW,
            with_predecessor=False,
            suffix="scf-composition",
        )
        calculator = Calculator()
        task = qe.QeScfTask(execution_input, calculator)
        executor = self.dispatch_effect()

        simulation = SUT(
            task=task,
            execution_input=execution_input,
            calculator=calculator,
            executor=executor,
        )

        assert simulation.task is task
        assert simulation.execution_input is execution_input
        assert simulation.calculator is calculator
        assert simulation.executor is executor
        assert simulation.result_type is qe.QePwResult
        assert isinstance(simulation.calculator, PlaneWaveCalculator)
        assert isinstance(simulation.executor, workflows.SimulationDispatchEffect)
        assert not hasattr(simulation, "result")
        with pytest.raises(FrozenInstanceError):
            simulation.execution_input = execution_input  # type: ignore[misc]

    def test_property__result_type__maps_bands_extraction_without_execution(
        self,
    ) -> None:
        """Evidence ID: SV-QE-SIM-003

        Requirement: Bands extraction selects the immutable bands-result role while
        SCF, NSCF, and band path retain the ``pw`` result role.

        Acceptance: A valid extraction composition reports
        ``QeBandsResult`` and neither injected port is invoked.
        """

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QeBandsResult:
                raise AssertionError("result-role inspection must not execute")

        execution_input = self.execution_input(
            definition="quantum-espresso.bands-extraction.v1",
            program=qe.QeProgram.BANDS,
            with_predecessor=True,
            suffix="bands-composition",
        )
        calculator = Calculator()
        task = qe.QeBandsExtractionTask(execution_input, calculator)

        simulation = qe.QeSimulation(
            task=task,
            execution_input=execution_input,
            calculator=calculator,
            executor=self.dispatch_effect(),
        )

        assert simulation.result_type is qe.QeBandsResult

    def test_constructor__correlation__rejects_substituted_components(self) -> None:
        """Evidence ID: SV-QE-SIM-004

        Requirement: A Simulation cannot substitute another input or calculator for
        the exact values retained by its Task, and every member must satisfy its
        closed semantic type or structural port.

        Acceptance: Input and calculator substitutions raise ``ValueError``; wrong
        Task, input, calculator, and executor semantic types raise ``TypeError``.
        """

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                raise AssertionError("invalid composition must not execute")

        execution_input = self.execution_input(
            definition="quantum-espresso.scf.v1",
            program=qe.QeProgram.PW,
            with_predecessor=False,
            suffix="invalid-composition",
        )
        calculator = Calculator()
        task = qe.QeScfTask(execution_input, calculator)
        executor = self.dispatch_effect()
        other_input = replace(
            execution_input,
            identity=qe.QeExecutionInputIdentity("input.other"),
        )

        with pytest.raises(ValueError, match="same execution input"):
            qe.QeSimulation(
                task=task,
                execution_input=other_input,
                calculator=calculator,
                executor=executor,
            )
        with pytest.raises(ValueError, match="same calculator instance"):
            qe.QeSimulation(
                task=task,
                execution_input=execution_input,
                calculator=Calculator(),
                executor=executor,
            )
        with pytest.raises(TypeError, match="operation-specific"):
            qe.QeSimulation(
                task="invalid",  # type: ignore[arg-type]
                execution_input=execution_input,
                calculator=calculator,
                executor=executor,
            )
        with pytest.raises(TypeError, match="execution_input"):
            qe.QeSimulation(
                task=task,
                execution_input="invalid",  # type: ignore[arg-type]
                calculator=calculator,
                executor=executor,
            )
        with pytest.raises(TypeError, match="PlaneWaveCalculator"):
            qe.QeSimulation(
                task=task,
                execution_input=execution_input,
                calculator="invalid",  # type: ignore[arg-type]
                executor=executor,
            )
        with pytest.raises(TypeError, match="SimulationDispatchEffect"):
            qe.QeSimulation(
                task=task,
                execution_input=execution_input,
                calculator=calculator,
                executor="invalid",  # type: ignore[arg-type]
            )
