r"""Software verification of definition-only Quantum ESPRESSO Tasks.

These synthetic contracts invoke no executable and establish no numerical or
scientific validation, convergence, uncertainty quantification, or authority.
"""

from dataclasses import FrozenInstanceError, replace

import pytest

import ksdft2effmass.calculators as calculators
import ksdft2effmass.integration.quantum_espresso as qe
import ksdft2effmass.workflows as workflows

pytestmark = pytest.mark.software_verification


class TestQuantumEspressoTaskContracts:
    """Verify the selected nominal QE simulation Task family."""

    @staticmethod
    def _content(character: str, byte_count: int) -> workflows.ArtifactContentIdentity:
        return workflows.ArtifactContentIdentity("sha256", character * 64, byte_count)

    @classmethod
    def _input(
        cls,
        *,
        identity: str,
        program: qe.QuantumEspressoProgram,
        predecessor: bool,
        suffix: str,
    ) -> qe.QuantumEspressoExecutionInput:
        state = ()
        if predecessor:
            state = (
                qe.QuantumEspressoPredecessorNativeStateArtifact(
                    workflows.ArtifactIdentity(f"state.{suffix}"),
                    qe.QuantumEspressoTreeArtifactContent(
                        workflows.ArtifactManifestIdentity(f"manifest.{suffix}"),
                        (workflows.ArtifactManifestEntryIdentity(f"entry.{suffix}"),),
                    ),
                    qe.QuantumEspressoArtifactDestination(f"state/{suffix}.save"),
                    workflows.ResultObjectIdentity(f"result.parent.{suffix}"),
                    workflows.ArtifactManifestEntryIdentity(f"entry.{suffix}"),
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
            predecessor_native_state=state,
            task_definition_identity=workflows.TaskDefinitionIdentity(identity),
            task_instance_identity=workflows.TaskInstanceIdentity(f"instance.{suffix}"),
            activation_identity=workflows.TaskActivationIdentity(
                f"activation.{suffix}"
            ),
            operation_identity=workflows.OperationIdentity(f"operation.{suffix}"),
            attempt_identity=workflows.AttemptIdentity(f"attempt.{suffix}"),
            contract_version="qe-execution-input:1",
        )

    def test_public_api_exports_only_selected_operation_tasks(self) -> None:
        """Keep the four selected Task classes under integration ownership.

        Evidence ID: SV-QE-TASK-001
        """
        defining_module = "ksdft2effmass.integration.quantum_espresso.tasks"
        selected = (
            qe.QuantumEspressoScfTask,
            qe.QuantumEspressoNscfTask,
            qe.QuantumEspressoBandPathTask,
            qe.QuantumEspressoBandsExtractionTask,
        )
        assert all(task_type.__module__ == defining_module for task_type in selected)
        assert not hasattr(calculators, "QuantumEspressoScfTask")
        assert not hasattr(qe, "QuantumEspressoDosTask")

    def test_task_family_retains_inputs_and_fixed_generic_definitions(self) -> None:
        """Own exact QE inputs without retaining calculators or direct execution.

        Evidence ID: SV-QE-TASK-002
        """
        specifications = (
            (
                qe.QuantumEspressoScfTask,
                "quantum-espresso.scf.v1",
                qe.QuantumEspressoProgram.PW,
                False,
            ),
            (
                qe.QuantumEspressoNscfTask,
                "quantum-espresso.nscf.v1",
                qe.QuantumEspressoProgram.PW,
                True,
            ),
            (
                qe.QuantumEspressoBandPathTask,
                "quantum-espresso.band-path.v1",
                qe.QuantumEspressoProgram.PW,
                True,
            ),
            (
                qe.QuantumEspressoBandsExtractionTask,
                "quantum-espresso.bands-extraction.v1",
                qe.QuantumEspressoProgram.BANDS,
                True,
            ),
        )
        for task_type, identity, program, predecessor in specifications:
            execution_input = self._input(
                identity=identity,
                program=program,
                predecessor=predecessor,
                suffix=task_type.__name__,
            )
            task = task_type(execution_input)
            assert isinstance(task, workflows.AbstractSimulationTask)
            assert task.simulation_input is execution_input
            assert task.definition == workflows.TaskDefinition(
                workflows.TaskDefinitionIdentity(identity),
                workflows.TaskExecutionKind.SIMULATION,
            )
            assert not hasattr(task, "calculator")
            assert not hasattr(task, "execute")
            with pytest.raises(FrozenInstanceError):
                task.simulation_input = execution_input  # type: ignore[misc]

    def test_operation_shape_rejects_wrong_program_state_or_identity(self) -> None:
        """Validate operation-specific intrinsic input correlations only.

        Evidence ID: SV-QE-TASK-003
        """
        scf = self._input(
            identity="quantum-espresso.scf.v1",
            program=qe.QuantumEspressoProgram.PW,
            predecessor=False,
            suffix="shape-scf",
        )
        nscf = self._input(
            identity="quantum-espresso.nscf.v1",
            program=qe.QuantumEspressoProgram.PW,
            predecessor=True,
            suffix="shape-nscf",
        )
        with pytest.raises(ValueError, match="must not contain predecessor"):
            qe.QuantumEspressoScfTask(
                replace(scf, predecessor_native_state=nscf.predecessor_native_state)
            )
        with pytest.raises(ValueError, match="requires exactly one predecessor"):
            qe.QuantumEspressoNscfTask(replace(nscf, predecessor_native_state=()))
        with pytest.raises(ValueError, match="must use the bands program role"):
            qe.QuantumEspressoBandsExtractionTask(
                replace(
                    nscf,
                    task_definition_identity=workflows.TaskDefinitionIdentity(
                        "quantum-espresso.bands-extraction.v1"
                    ),
                )
            )
        with pytest.raises(ValueError, match="exact Task definition"):
            qe.QuantumEspressoScfTask(
                replace(
                    scf,
                    task_definition_identity=workflows.TaskDefinitionIdentity(
                        "quantum-espresso.other.v1"
                    ),
                )
            )

    def test_structural_lookalike_is_not_a_simulation_task(self) -> None:
        """Reject structural fallback at the QE Task boundary.

        Evidence ID: SV-QE-TASK-004
        """

        class TaskLookalike:
            identity = workflows.TaskDefinitionIdentity("quantum-espresso.scf.v1")

        assert not isinstance(TaskLookalike(), workflows.AbstractSimulationTask)
