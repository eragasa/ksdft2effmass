r"""Software verification of public Quantum ESPRESSO operation-specific Task contracts.

Evidence profile: routine

Bounded artifact scope: the operation-specific SCF, NSCF, band-path, and
bands-extraction Task adapter family.

Facet and represented meaning

The artifact represents four reusable QE scientific operations that retain exact
Workflow, input, predecessor-state, calculator-port, and mechanical-result boundaries.

Intrinsic and cross-object scope

Tests cover fixed operation identities, immutable construction, exact program and
predecessor shapes, Task protocol conformance, Workflow correlation, calculator
port delegation, result typing, and predecessor native-state provenance closure.

VVUQ and scientific exclusions

These synthetic software checks invoke no executable and establish no numerical
verification, scientific validation, uncertainty quantification, convergence,
physical correctness, execution authority, or human acceptance.
"""

from dataclasses import FrozenInstanceError, replace

import pytest
from projectkoios.simulations.execution import CalculatorExitCode

import ksdft2effmass.calculators as calculators
import ksdft2effmass.integration.quantum_espresso as qe
import ksdft2effmass.workflows as workflows

pytestmark = pytest.mark.software_verification


class TestQeTaskContracts:
    """Own software verification of the selected public QE Task family."""

    @staticmethod
    def content(character: str, byte_count: int) -> workflows.ArtifactContentIdentity:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide one deterministic synthetic content identity.

        Acceptance: The returned identity exactly represents the supplied character
        and byte count.
        """
        return workflows.ArtifactContentIdentity("sha256", character * 64, byte_count)

    @classmethod
    def execution_input(
        cls,
        *,
        definition_identity: workflows.TaskDefinitionIdentity,
        program: qe.QeProgram,
        predecessor: qe.QePwResult | None,
        suffix: str,
    ) -> qe.QeExecutionInput:
        """Evidence ID: This helper owns no identifier.

        Requirement: Build one exact synthetic operation input for a test case.

        Acceptance: The value retains the supplied operation, program, predecessor,
        and suffix correlations.
        """
        native = qe.QeNativeInputArtifact(
            workflows.ArtifactIdentity(f"native-input.{suffix}"),
            qe.QeFileArtifactContent(cls.content("a", 8)),
            qe.QeArtifactDestination(f"input/{suffix}.in"),
        )
        pseudo = qe.QePseudopotentialArtifact(
            workflows.ArtifactIdentity(f"pseudo.{suffix}"),
            qe.QeFileArtifactContent(cls.content("b", 16)),
            qe.QeArtifactDestination(f"pseudo/{suffix}.UPF"),
        )
        states: tuple[qe.QePredecessorNativeStateArtifact, ...]
        if predecessor is None:
            states = ()
        else:
            state_entry = predecessor.native_output_entry_identities[0]
            states = (
                qe.QePredecessorNativeStateArtifact(
                    workflows.ArtifactIdentity(f"predecessor-state.{suffix}"),
                    qe.QeTreeArtifactContent(
                        predecessor.native_output_manifest_identity,
                        predecessor.native_output_entry_identities,
                    ),
                    qe.QeArtifactDestination(f"state/{suffix}.save"),
                    predecessor.identity,
                    state_entry,
                ),
            )
        return qe.QeExecutionInput(
            identity=qe.QeExecutionInputIdentity(f"input.{suffix}"),
            program=program,
            native_input=native,
            pseudopotentials=(pseudo,),
            predecessor_native_state=states,
            task_definition_identity=definition_identity,
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

    @classmethod
    def result(
        cls,
        execution_input: qe.QeExecutionInput,
        *,
        suffix: str,
        completed: bool = True,
    ) -> qe.QePwResult | qe.QeBandsResult:
        """Evidence ID: This helper owns no identifier.

        Requirement: Build one internally correlated synthetic mechanical result.

        Acceptance: The result variant matches the execution-input program and its
        evidence satisfies the public constructor contract.
        """
        stdout = cls.content("c", 32)
        stderr = cls.content("d", 0)
        termination = qe.QeNormalProcessExit(CalculatorExitCode(0 if completed else 1))
        process = qe.QeProcessObservation(
            identity=qe.QeProcessObservationIdentity(f"process.{suffix}"),
            execution_input_identity=execution_input.identity,
            executable_configuration_identity=(
                qe.QeExecutableConfigurationIdentity(f"configuration.{suffix}")
            ),
            preparation_identity=qe.QePreparationIdentity(f"preparation.{suffix}"),
            attempt_identity=execution_input.attempt_identity,
            argv_content_identity=cls.content("e", 12),
            termination=termination,
            wall_duration_nanoseconds=1,
            stdout=qe.QeStreamObservation(
                channel=qe.QeDiagnosticChannel.STDOUT,
                artifact_identity=workflows.ArtifactIdentity(f"stdout.{suffix}"),
                content_identity=stdout,
            ),
            stderr=qe.QeStreamObservation(
                channel=qe.QeDiagnosticChannel.STDERR,
                artifact_identity=workflows.ArtifactIdentity(f"stderr.{suffix}"),
                content_identity=stderr,
            ),
            before_snapshot_identity=workflows.ArtifactManifestIdentity(
                f"snapshot.before.{suffix}"
            ),
            after_snapshot_identity=workflows.ArtifactManifestIdentity(
                f"snapshot.after.{suffix}"
            ),
            created_entry_count=2,
            created_total_bytes=32,
            peak_resident_bytes=None,
            observer_version="synthetic-process-observer:1",
        )
        marker = qe.QeOutputMarkerObservation(
            identity=qe.QeOutputMarkerObservationIdentity(f"marker.{suffix}"),
            channel=qe.QeDiagnosticChannel.STDOUT,
            byte_start=0,
            byte_end=8,
            stream_content_identity=stdout,
            span_content_identity=cls.content("f", 8),
            signature_identity="synthetic.completed.v1",
        )
        markers = (marker,) if completed else ()
        report = qe.QeDiagnosticReport(
            identity=qe.QeDiagnosticReportIdentity(f"report.{suffix}"),
            classifier_identity=qe.QeDiagnosticClassifierIdentity(
                "synthetic-classifier:1"
            ),
            executable_configuration_identity=(
                process.executable_configuration_identity
            ),
            executable_kind=qe.QeExecutableKind.DETERMINISTIC_FIXTURE,
            program=execution_input.program,
            program_version=f"fixture-{execution_input.program.value}-v1",
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(),
            completion_markers=markers,
            kind=qe.QeDiagnosticReportKind.CLEAR,
            claim_boundary=("synthetic software verification",),
        )
        outcome: qe.QeCalculatorOutcome
        if completed:
            outcome = qe.QeCompletedOutcome((marker.identity,))
        else:
            outcome = qe.QeProcessFailedOutcome(qe.QeProcessFailureKind.NONZERO_EXIT)
        evidence = qe.QeOperationResultEvidence(
            execution_input=execution_input,
            process_observation=process,
            diagnostic_report=report,
            calculator_outcome=outcome,
            native_output_manifest_identity=workflows.ArtifactManifestIdentity(
                f"native-output.{suffix}"
            ),
            native_output_entry_identities=(
                workflows.ArtifactManifestEntryIdentity(f"entry.state.{suffix}"),
                workflows.ArtifactManifestEntryIdentity(f"entry.stdout.{suffix}"),
            ),
            terminal_record_identity=qe.QeTerminalRecordIdentity(f"terminal.{suffix}"),
        )
        if execution_input.program is qe.QeProgram.PW:
            return qe.QePwResult(
                identity=workflows.ResultObjectIdentity(f"result.{suffix}"),
                execution_input=evidence.execution_input,
                process_observation=evidence.process_observation,
                diagnostic_report=evidence.diagnostic_report,
                calculator_outcome=evidence.calculator_outcome,
                native_output_manifest_identity=(
                    evidence.native_output_manifest_identity
                ),
                native_output_entry_identities=(
                    evidence.native_output_entry_identities
                ),
                execution_record_manifest_entry_identity=(
                    workflows.ArtifactManifestEntryIdentity(
                        f"execution-record.{suffix}"
                    )
                ),
                execution_record_content_identity=cls.content("9", 101),
                execution_record_publication_snapshot_identity=(
                    workflows.ArtifactManifestIdentity(
                        f"execution-publication.{suffix}"
                    )
                ),
                terminal_record_identity=evidence.terminal_record_identity,
                terminal_record_content_identity=cls.content("a", 202),
                contract_version="qe-pw-result:2",
            )
        return qe.QeBandsResult(
            identity=workflows.ResultObjectIdentity(f"result.{suffix}"),
            evidence=evidence,
            contract_version="qe-bands-result:1",
        )

    @classmethod
    def pw_result(
        cls,
        execution_input: qe.QeExecutionInput,
        *,
        suffix: str,
        completed: bool = True,
    ) -> qe.QePwResult:
        """Evidence ID: This helper owns no identifier.

        Requirement: Restrict synthetic result construction to the ``pw`` variant.

        Acceptance: The helper returns an exact ``QePwResult`` or fails.
        """
        result = cls.result(execution_input, suffix=suffix, completed=completed)
        if type(result) is not qe.QePwResult:
            raise ValueError("execution input must use the pw program role")
        return result

    @classmethod
    def bands_result(
        cls,
        execution_input: qe.QeExecutionInput,
        *,
        suffix: str,
    ) -> qe.QeBandsResult:
        """Evidence ID: This helper owns no identifier.

        Requirement: Restrict synthetic result construction to the ``bands`` variant.

        Acceptance: The helper returns an exact ``QeBandsResult`` or
        fails.
        """
        result = cls.result(execution_input, suffix=suffix)
        if type(result) is not qe.QeBandsResult:
            raise ValueError("execution input must use the bands program role")
        return result

    @staticmethod
    def context(
        execution_input: qe.QeExecutionInput,
    ) -> workflows.TaskExecutionContext:
        """Evidence ID: This helper owns no identifier.

        Requirement: Build exact Workflow context for one execution input.

        Acceptance: The context copies every run-scoped input correlation exactly.
        """
        return workflows.TaskExecutionContext(
            workflow_identity=workflows.WorkflowIdentity("workflow.synthetic"),
            workflow_run_identity=workflows.WorkflowRunIdentity("run.synthetic"),
            task_instance_identity=execution_input.task_instance_identity,
            task_activation_identity=execution_input.activation_identity,
            operation_identity=execution_input.operation_identity,
            attempt_identity=execution_input.attempt_identity,
        )

    def test_public_api__package__exports_only_selected_operation_tasks(self) -> None:
        """Evidence ID: SV-QE-TASK-001

        Requirement: The QE integration exports exactly the selected SCF, NSCF,
        band-path, and bands-extraction Task classes, while DOS remains deferred and
        backend-neutral calculators expose no QE types.

        Acceptance: Each selected name resolves to its canonical class; no public QE
        DOS Task exists and the generic calculator root exposes none of the four.
        """
        defining_module = "ksdft2effmass.integration.quantum_espresso.tasks"

        assert qe.QeScfTask.__module__ == defining_module
        assert qe.QeNscfTask.__module__ == defining_module
        assert qe.QeBandPathTask.__module__ == defining_module
        assert qe.QeBandsExtractionTask.__module__ == defining_module
        assert "QeScfTask" in qe.__all__
        assert "QeNscfTask" in qe.__all__
        assert "QeBandPathTask" in qe.__all__
        assert "QeBandsExtractionTask" in qe.__all__
        assert not hasattr(calculators, "QeScfTask")
        assert not hasattr(calculators, "QeNscfTask")
        assert not hasattr(calculators, "QeBandPathTask")
        assert not hasattr(calculators, "QeBandsExtractionTask")
        assert not hasattr(qe, "QeDosTask")
        assert not hasattr(qe, "QuantumEspressoScfTask")
        assert not hasattr(qe, "QuantumEspressoNscfTask")
        assert not hasattr(qe, "QuantumEspressoBandPathTask")
        assert not hasattr(qe, "QuantumEspressoBandsExtractionTask")

    def test_constructor__task_family__has_fixed_identities_and_is_immutable(
        self,
    ) -> None:
        """Evidence ID: SV-QE-TASK-002

        Requirement: Each operation class is an immutable structural Workflow Task
        with one fixed reusable definition identity.

        Acceptance: All four instances satisfy ``Task``, expose the documented exact
        identity, and reject ordinary execution-input reassignment.
        """

        class PwCalculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                raise AssertionError("constructor evidence does not execute")

        class BandsCalculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QeBandsResult:
                raise AssertionError("constructor evidence does not execute")

        scf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=None,
            suffix="scf",
        )
        scf_result = self.pw_result(scf_input, suffix="scf")
        nscf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.nscf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=scf_result,
            suffix="nscf",
        )
        nscf_result = self.pw_result(nscf_input, suffix="nscf")
        band_path_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.band-path.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=nscf_result,
            suffix="band-path",
        )
        band_path_result = self.pw_result(band_path_input, suffix="band-path")
        extraction_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.bands-extraction.v1"
            ),
            program=qe.QeProgram.BANDS,
            predecessor=band_path_result,
            suffix="bands-extraction",
        )
        tasks = (
            qe.QeScfTask(scf_input, PwCalculator()),
            qe.QeNscfTask(nscf_input, PwCalculator()),
            qe.QeBandPathTask(band_path_input, PwCalculator()),
            qe.QeBandsExtractionTask(extraction_input, BandsCalculator()),
        )
        identities = (
            "quantum-espresso.scf.v1",
            "quantum-espresso.nscf.v1",
            "quantum-espresso.band-path.v1",
            "quantum-espresso.bands-extraction.v1",
        )

        assert all(isinstance(task, workflows.Task) for task in tasks)
        assert tuple(task.identity.value for task in tasks) == identities
        with pytest.raises(FrozenInstanceError):
            tasks[0].simulation_input = scf_input  # type: ignore[misc]

    def test_constructor__operation_shape__rejects_wrong_program_or_state(self) -> None:
        """Evidence ID: SV-QE-TASK-003

        Requirement: SCF admits no predecessor state, downstream ``pw`` Tasks admit
        exactly one, bands extraction uses the ``bands`` role, and every input names
        its exact operation definition.

        Acceptance: Each wrong program, state cardinality, or definition partition
        raises ``ValueError`` before calculator invocation.
        """

        class PwCalculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                raise AssertionError("invalid tasks do not execute")

        class BandsCalculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QeBandsResult:
                raise AssertionError("invalid tasks do not execute")

        scf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=None,
            suffix="shape-scf",
        )
        scf_result = self.pw_result(scf_input, suffix="shape-scf")
        nscf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.nscf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=scf_result,
            suffix="shape-nscf",
        )

        with pytest.raises(ValueError, match="must not contain predecessor"):
            qe.QeScfTask(
                replace(
                    scf_input,
                    predecessor_native_state=nscf_input.predecessor_native_state,
                ),
                PwCalculator(),
            )
        with pytest.raises(ValueError, match="requires exactly one predecessor"):
            qe.QeNscfTask(
                replace(nscf_input, predecessor_native_state=()), PwCalculator()
            )
        with pytest.raises(ValueError, match="bands program role"):
            qe.QeBandsExtractionTask(nscf_input, BandsCalculator())
        with pytest.raises(ValueError, match="SCF Task definition"):
            qe.QeScfTask(
                replace(
                    scf_input,
                    task_definition_identity=workflows.TaskDefinitionIdentity(
                        "quantum-espresso.nscf.v1"
                    ),
                ),
                PwCalculator(),
            )
        with pytest.raises(TypeError, match="simulation_input"):
            qe.QeScfTask("invalid", PwCalculator())  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="PlaneWaveCalculator"):
            qe.QeScfTask(scf_input, "invalid")  # type: ignore[arg-type]

    def test_method__execute__scf_delegates_exact_input_and_context(self) -> None:
        """Evidence ID: SV-QE-TASK-004

        Requirement: SCF accepts no predecessor binding and delegates its exact input
        and matching Workflow context through the generic plane-wave port.

        Acceptance: The injected calculator observes the identical input and context,
        is called once, and the Task returns its one exact ``pw`` result.
        """
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=None,
            suffix="execute-scf",
        )
        expected = self.pw_result(execution_input, suffix="execute-scf")
        context = self.context(execution_input)

        class Calculator:
            def __init__(self) -> None:
                self.calls = 0

            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                supplied_context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                assert simulation_input is execution_input
                assert supplied_context is context
                self.calls += 1
                return expected

        calculator = Calculator()
        task = qe.QeScfTask(execution_input, calculator)

        assert task.execute((), context) == (expected,)
        assert calculator.calls == 1
        with pytest.raises(ValueError, match="requires no predecessor"):
            task.execute((workflows.TaskInputBinding("unexpected", expected),), context)
        with pytest.raises(ValueError, match="context must match"):
            task.execute(
                (),
                replace(
                    context,
                    operation_identity=workflows.OperationIdentity("operation.other"),
                ),
            )
        assert calculator.calls == 1

    def test_method__execute__nscf_requires_exact_completed_scf_state(self) -> None:
        """Evidence ID: SV-QE-TASK-005

        Requirement: NSCF accepts exactly one mechanically completed ``scf_result``
        whose retained native-state manifest and entry match the new execution input.

        Acceptance: The exact binding delegates once; wrong binding names, failed
        predecessors, and mismatched native-state result identities raise before the
        calculator is called.
        """
        scf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=None,
            suffix="nscf-parent",
        )
        predecessor = self.pw_result(scf_input, suffix="nscf-parent")
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.nscf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=predecessor,
            suffix="execute-nscf",
        )
        expected = self.pw_result(execution_input, suffix="execute-nscf")

        class Calculator:
            def __init__(self) -> None:
                self.calls = 0

            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                self.calls += 1
                return expected

        calculator = Calculator()
        task = qe.QeNscfTask(execution_input, calculator)
        binding = workflows.TaskInputBinding("scf_result", predecessor)

        assert task.execute((binding,), self.context(execution_input)) == (expected,)
        assert calculator.calls == 1
        with pytest.raises(ValueError, match="scf_result binding"):
            task.execute(
                (workflows.TaskInputBinding("predecessor_result", predecessor),),
                self.context(execution_input),
            )
        failed = self.pw_result(scf_input, suffix="nscf-failed-parent", completed=False)
        failed_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.nscf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=failed,
            suffix="nscf-failed",
        )
        with pytest.raises(ValueError, match="mechanically completed"):
            qe.QeNscfTask(failed_input, calculator).execute(
                (workflows.TaskInputBinding("scf_result", failed),),
                self.context(failed_input),
            )
        state = execution_input.predecessor_native_state[0]
        mismatch_input = replace(
            execution_input,
            predecessor_native_state=(
                replace(
                    state,
                    predecessor_result_identity=workflows.ResultObjectIdentity(
                        "result.other"
                    ),
                ),
            ),
        )
        with pytest.raises(ValueError, match="identify the SCF result"):
            qe.QeNscfTask(mismatch_input, calculator).execute(
                (binding,), self.context(mismatch_input)
            )
        manifest_mismatch_input = replace(
            execution_input,
            predecessor_native_state=(
                replace(
                    state,
                    content=qe.QeTreeArtifactContent(
                        workflows.ArtifactManifestIdentity("native-output.other"),
                        state.content.manifest_entry_identities,
                    ),
                ),
            ),
        )
        with pytest.raises(ValueError, match="belong to the SCF result manifest"):
            qe.QeNscfTask(manifest_mismatch_input, calculator).execute(
                (binding,), self.context(manifest_mismatch_input)
            )
        assert calculator.calls == 1

    def test_method__execute__band_path_accepts_one_explicit_parent(self) -> None:
        """Evidence ID: SV-QE-TASK-006

        Requirement: Band-path execution uses the distinct operation identity and one
        exact completed ``predecessor_result`` without prescribing SCF versus NSCF in
        the reusable Task contract.

        Acceptance: A correlated completed ``pw`` predecessor delegates once and
        returns one exact correlated ``pw`` result.
        """
        parent_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=None,
            suffix="band-parent",
        )
        predecessor = self.pw_result(parent_input, suffix="band-parent")
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.band-path.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=predecessor,
            suffix="execute-band-path",
        )
        expected = self.pw_result(execution_input, suffix="execute-band-path")

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                return expected

        task = qe.QeBandPathTask(execution_input, Calculator())
        binding = workflows.TaskInputBinding("predecessor_result", predecessor)

        assert task.execute((binding,), self.context(execution_input)) == (expected,)

    def test_method__execute__bands_extraction_requires_band_path_result(self) -> None:
        """Evidence ID: SV-QE-TASK-007

        Requirement: Bands extraction accepts one completed ``band_path_result``,
        delegates through a bands-result port, and returns the existing mechanical
        ``QeBandsResult`` variant.

        Acceptance: The exact predecessor and context return one correlated bands
        result; a ``pw`` result from the injected port is rejected as the wrong type.
        """
        band_path_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.band-path.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=None,
            suffix="extraction-parent",
        )
        predecessor = self.pw_result(band_path_input, suffix="extraction-parent")
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.bands-extraction.v1"
            ),
            program=qe.QeProgram.BANDS,
            predecessor=predecessor,
            suffix="execute-extraction",
        )
        expected = self.bands_result(execution_input, suffix="execute-extraction")

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QeBandsResult:
                return expected

        task = qe.QeBandsExtractionTask(execution_input, Calculator())
        binding = workflows.TaskInputBinding("band_path_result", predecessor)

        assert task.execute((binding,), self.context(execution_input)) == (expected,)

        class WrongCalculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                return predecessor

        wrong_task = qe.QeBandsExtractionTask(
            execution_input,
            WrongCalculator(),  # type: ignore[arg-type]
        )
        with pytest.raises(TypeError, match="QeBandsResult"):
            wrong_task.execute((binding,), self.context(execution_input))

    def test_method__execute__rejects_result_for_different_execution_input(
        self,
    ) -> None:
        """Evidence ID: SV-QE-TASK-008

        Requirement: A Task returns only a result whose complete retained execution
        input equals the Task's exact configured input.

        Acceptance: An otherwise valid ``pw`` result correlated to a different input
        raises ``ValueError`` rather than being returned.
        """
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QeProgram.PW,
            predecessor=None,
            suffix="result-correlation",
        )
        other_input = replace(
            execution_input,
            identity=qe.QeExecutionInputIdentity("input.other"),
        )
        other_result = self.pw_result(other_input, suffix="result-other")

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QeExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QePwResult:
                return other_result

        task = qe.QeScfTask(execution_input, Calculator())
        with pytest.raises(ValueError, match="exact execution input"):
            task.execute((), self.context(execution_input))
