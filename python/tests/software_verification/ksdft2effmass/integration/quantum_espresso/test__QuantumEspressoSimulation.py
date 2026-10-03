r"""Software verification of immutable ``QuantumEspressoSimulation`` composition."""

from dataclasses import FrozenInstanceError, replace

import pytest

import ksdft2effmass.integration.quantum_espresso as qe
import ksdft2effmass.workflows as workflows
from ksdft2effmass.calculators.dft.pw import AbstractPlaneWaveCalculator

pytestmark = pytest.mark.software_verification


class TestQuantumEspressoSimulation:
    """Verify separate nominal calculator and dispatch-effect composition."""

    class PwCalculator(
        AbstractPlaneWaveCalculator[
            qe.QuantumEspressoExecutionInput, qe.QuantumEspressoPwResult
        ]
    ):
        def execute(
            self,
            simulation_input: qe.QuantumEspressoExecutionInput,
            context: workflows.TaskExecutionContext,
        ) -> qe.QuantumEspressoPwResult:
            del simulation_input, context
            raise AssertionError("composition must not invoke calculators")

    class BandsCalculator(
        AbstractPlaneWaveCalculator[
            qe.QuantumEspressoExecutionInput, qe.QuantumEspressoBandsResult
        ]
    ):
        def execute(
            self,
            simulation_input: qe.QuantumEspressoExecutionInput,
            context: workflows.TaskExecutionContext,
        ) -> qe.QuantumEspressoBandsResult:
            del simulation_input, context
            raise AssertionError("composition must not invoke calculators")

    class Effect(workflows.AbstractSimulationDispatchEffect):
        @property
        def executor_identity(self) -> workflows.ScientificExecutorIdentity:
            return workflows.ScientificExecutorIdentity("executor.synthetic")

        def execute(
            self, request: workflows.SimulationDispatchEffectRequest
        ) -> workflows.SimulationDispatchOutcome:
            del request
            raise AssertionError("composition must not invoke effects")

    @staticmethod
    def _content(character: str, byte_count: int) -> workflows.ArtifactContentIdentity:
        return workflows.ArtifactContentIdentity("sha256", character * 64, byte_count)

    @classmethod
    def _input(
        cls,
        *,
        definition: str,
        program: qe.QuantumEspressoProgram,
        predecessor: bool,
        suffix: str,
    ) -> qe.QuantumEspressoExecutionInput:
        states = ()
        if predecessor:
            entry = workflows.ArtifactManifestEntryIdentity(f"entry.{suffix}")
            states = (
                qe.QuantumEspressoPredecessorNativeStateArtifact(
                    workflows.ArtifactIdentity(f"state.{suffix}"),
                    qe.QuantumEspressoTreeArtifactContent(
                        workflows.ArtifactManifestIdentity(f"manifest.{suffix}"),
                        (entry,),
                    ),
                    qe.QuantumEspressoArtifactDestination(f"state/{suffix}.save"),
                    workflows.ResultObjectIdentity(f"result.parent.{suffix}"),
                    entry,
                ),
            )
        return qe.QuantumEspressoExecutionInput(
            identity=qe.QuantumEspressoExecutionInputIdentity(f"input.{suffix}"),
            program=program,
            native_input=qe.QuantumEspressoNativeInputArtifact(
                workflows.ArtifactIdentity(f"input-artifact.{suffix}"),
                qe.QuantumEspressoFileArtifactContent(cls._content("a", 8)),
                qe.QuantumEspressoArtifactDestination(f"input/{suffix}.in"),
            ),
            pseudopotentials=(
                qe.QuantumEspressoPseudopotentialArtifact(
                    workflows.ArtifactIdentity(f"pseudo.{suffix}"),
                    qe.QuantumEspressoFileArtifactContent(cls._content("b", 16)),
                    qe.QuantumEspressoArtifactDestination(f"pseudo/{suffix}.UPF"),
                ),
            ),
            predecessor_native_state=states,
            task_definition_identity=workflows.TaskDefinitionIdentity(definition),
            task_instance_identity=workflows.TaskInstanceIdentity(f"instance.{suffix}"),
            activation_identity=workflows.TaskActivationIdentity(
                f"activation.{suffix}"
            ),
            operation_identity=workflows.OperationIdentity(f"operation.{suffix}"),
            attempt_identity=workflows.AttemptIdentity(f"attempt.{suffix}"),
            contract_version="qe-execution-input:1",
        )

    def test_constructor_binds_separate_nominal_components_immutably(self) -> None:
        """Retain a definition-only Task, calculator capability, and effect.

        Evidence ID: SV-QE-SIM-002
        """
        execution_input = self._input(
            definition="quantum-espresso.scf.v1",
            program=qe.QuantumEspressoProgram.PW,
            predecessor=False,
            suffix="scf-composition",
        )
        task = qe.QuantumEspressoScfTask(execution_input)
        calculator = self.PwCalculator()
        effect = self.Effect()
        simulation = qe.QuantumEspressoSimulation(
            task=task,
            execution_input=execution_input,
            calculator=calculator,
            executor=effect,
        )

        assert simulation.task is task
        assert simulation.calculator is calculator
        assert simulation.executor is effect
        assert simulation.result_type is qe.QuantumEspressoPwResult
        assert not hasattr(task, "calculator")
        with pytest.raises(FrozenInstanceError):
            simulation.execution_input = execution_input  # type: ignore[misc]

    def test_result_type_maps_bands_extraction_without_execution(self) -> None:
        """Select the immutable bands-result role from the operation Task.

        Evidence ID: SV-QE-SIM-003
        """
        execution_input = self._input(
            definition="quantum-espresso.bands-extraction.v1",
            program=qe.QuantumEspressoProgram.BANDS,
            predecessor=True,
            suffix="bands-composition",
        )
        simulation = qe.QuantumEspressoSimulation(
            task=qe.QuantumEspressoBandsExtractionTask(execution_input),
            execution_input=execution_input,
            calculator=self.BandsCalculator(),
            executor=self.Effect(),
        )
        assert simulation.result_type is qe.QuantumEspressoBandsResult

    def test_constructor_rejects_wrong_correlations_or_structural_ports(self) -> None:
        """Require exact input correlation and explicit nominal capabilities.

        Evidence ID: SV-QE-SIM-004
        """
        execution_input = self._input(
            definition="quantum-espresso.scf.v1",
            program=qe.QuantumEspressoProgram.PW,
            predecessor=False,
            suffix="invalid-composition",
        )
        task = qe.QuantumEspressoScfTask(execution_input)
        other_input = replace(
            execution_input,
            identity=qe.QuantumEspressoExecutionInputIdentity("input.other"),
        )
        with pytest.raises(ValueError, match="same execution input"):
            qe.QuantumEspressoSimulation(
                task=task,
                execution_input=other_input,
                calculator=self.PwCalculator(),
                executor=self.Effect(),
            )
        with pytest.raises(TypeError, match="AbstractPlaneWaveCalculator"):
            qe.QuantumEspressoSimulation(
                task=task,
                execution_input=execution_input,
                calculator=object(),  # type: ignore[arg-type]
                executor=self.Effect(),
            )
        with pytest.raises(TypeError, match="AbstractSimulationDispatchEffect"):
            qe.QuantumEspressoSimulation(
                task=task,
                execution_input=execution_input,
                calculator=self.PwCalculator(),
                executor=object(),  # type: ignore[arg-type]
            )
