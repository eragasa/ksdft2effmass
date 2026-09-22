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

import ksdft2effmass.calculators as calculators
import ksdft2effmass.integration.quantum_espresso as qe
import ksdft2effmass.workflows as workflows

pytestmark = pytest.mark.software_verification


class TestQuantumEspressoTaskContracts:
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
        program: qe.QuantumEspressoProgram,
        predecessor: qe.QuantumEspressoPwResult | None,
        suffix: str,
    ) -> qe.QuantumEspressoExecutionInput:
        """Evidence ID: This helper owns no identifier.

        Requirement: Build one exact synthetic operation input for a test case.

        Acceptance: The value retains the supplied operation, program, predecessor,
        and suffix correlations.
        """
        native = qe.QuantumEspressoNativeInputArtifact(
            workflows.ArtifactIdentity(f"native-input.{suffix}"),
            qe.QuantumEspressoFileArtifactContent(cls.content("a", 8)),
            qe.QuantumEspressoArtifactDestination(f"input/{suffix}.in"),
        )
        pseudo = qe.QuantumEspressoPseudopotentialArtifact(
            workflows.ArtifactIdentity(f"pseudo.{suffix}"),
            qe.QuantumEspressoFileArtifactContent(cls.content("b", 16)),
            qe.QuantumEspressoArtifactDestination(f"pseudo/{suffix}.UPF"),
        )
        states: tuple[qe.QuantumEspressoPredecessorNativeStateArtifact, ...]
        if predecessor is None:
            states = ()
        else:
            evidence = predecessor.evidence
            state_entry = evidence.native_output_entry_identities[0]
            states = (
                qe.QuantumEspressoPredecessorNativeStateArtifact(
                    workflows.ArtifactIdentity(f"predecessor-state.{suffix}"),
                    qe.QuantumEspressoTreeArtifactContent(
                        evidence.native_output_manifest_identity,
                        evidence.native_output_entry_identities,
                    ),
                    qe.QuantumEspressoArtifactDestination(f"state/{suffix}.save"),
                    predecessor.identity,
                    state_entry,
                ),
            )
        return qe.QuantumEspressoExecutionInput(
            identity=qe.QuantumEspressoExecutionInputIdentity(f"input.{suffix}"),
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
        execution_input: qe.QuantumEspressoExecutionInput,
        *,
        suffix: str,
        completed: bool = True,
    ) -> qe.QuantumEspressoPwResult | qe.QuantumEspressoBandsResult:
        """Evidence ID: This helper owns no identifier.

        Requirement: Build one internally correlated synthetic mechanical result.

        Acceptance: The result variant matches the execution-input program and its
        evidence satisfies the public constructor contract.
        """
        stdout = cls.content("c", 32)
        stderr = cls.content("d", 0)
        termination = qe.QuantumEspressoNormalProcessExit(0 if completed else 1)
        process = qe.QuantumEspressoProcessObservation(
            identity=qe.QuantumEspressoProcessObservationIdentity(f"process.{suffix}"),
            execution_input_identity=execution_input.identity,
            executable_configuration_identity=(
                qe.QuantumEspressoExecutableConfigurationIdentity(
                    f"configuration.{suffix}"
                )
            ),
            preparation_identity=qe.QuantumEspressoPreparationIdentity(
                f"preparation.{suffix}"
            ),
            attempt_identity=execution_input.attempt_identity,
            argv_content_identity=cls.content("e", 12),
            termination=termination,
            wall_duration_nanoseconds=1,
            stdout=qe.QuantumEspressoStreamObservation(
                channel=qe.QuantumEspressoDiagnosticChannel.STDOUT,
                artifact_identity=workflows.ArtifactIdentity(f"stdout.{suffix}"),
                content_identity=stdout,
            ),
            stderr=qe.QuantumEspressoStreamObservation(
                channel=qe.QuantumEspressoDiagnosticChannel.STDERR,
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
        marker = qe.QuantumEspressoOutputMarkerObservation(
            identity=qe.QuantumEspressoOutputMarkerObservationIdentity(
                f"marker.{suffix}"
            ),
            channel=qe.QuantumEspressoDiagnosticChannel.STDOUT,
            byte_start=0,
            byte_end=8,
            stream_content_identity=stdout,
            span_content_identity=cls.content("f", 8),
            signature_identity="synthetic.completed.v1",
        )
        markers = (marker,) if completed else ()
        report = qe.QuantumEspressoDiagnosticReport(
            identity=qe.QuantumEspressoDiagnosticReportIdentity(f"report.{suffix}"),
            classifier_identity=qe.QuantumEspressoDiagnosticClassifierIdentity(
                "synthetic-classifier:1"
            ),
            executable_configuration_identity=(
                process.executable_configuration_identity
            ),
            executable_kind=qe.QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            program=execution_input.program,
            program_version=f"fixture-{execution_input.program.value}-v1",
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(),
            completion_markers=markers,
            kind=qe.QuantumEspressoDiagnosticReportKind.CLEAR,
            claim_boundary=("synthetic software verification",),
        )
        outcome: qe.QuantumEspressoCalculatorOutcome
        if completed:
            outcome = qe.QuantumEspressoCompletedOutcome((marker.identity,))
        else:
            outcome = qe.QuantumEspressoProcessFailedOutcome(
                qe.QuantumEspressoProcessFailureKind.NONZERO_EXIT
            )
        evidence = qe.QuantumEspressoOperationResultEvidence(
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
            terminal_record_identity=qe.QuantumEspressoTerminalRecordIdentity(
                f"terminal.{suffix}"
            ),
        )
        if execution_input.program is qe.QuantumEspressoProgram.PW:
            return qe.QuantumEspressoPwResult(
                identity=workflows.ResultObjectIdentity(f"result.{suffix}"),
                evidence=evidence,
                contract_version="qe-pw-result:1",
            )
        return qe.QuantumEspressoBandsResult(
            identity=workflows.ResultObjectIdentity(f"result.{suffix}"),
            evidence=evidence,
            contract_version="qe-bands-result:1",
        )

    @classmethod
    def pw_result(
        cls,
        execution_input: qe.QuantumEspressoExecutionInput,
        *,
        suffix: str,
        completed: bool = True,
    ) -> qe.QuantumEspressoPwResult:
        """Evidence ID: This helper owns no identifier.

        Requirement: Restrict synthetic result construction to the ``pw`` variant.

        Acceptance: The helper returns an exact ``QuantumEspressoPwResult`` or fails.
        """
        result = cls.result(execution_input, suffix=suffix, completed=completed)
        if type(result) is not qe.QuantumEspressoPwResult:
            raise ValueError("execution input must use the pw program role")
        return result

    @classmethod
    def bands_result(
        cls,
        execution_input: qe.QuantumEspressoExecutionInput,
        *,
        suffix: str,
    ) -> qe.QuantumEspressoBandsResult:
        """Evidence ID: This helper owns no identifier.

        Requirement: Restrict synthetic result construction to the ``bands`` variant.

        Acceptance: The helper returns an exact ``QuantumEspressoBandsResult`` or
        fails.
        """
        result = cls.result(execution_input, suffix=suffix)
        if type(result) is not qe.QuantumEspressoBandsResult:
            raise ValueError("execution input must use the bands program role")
        return result

    @staticmethod
    def context(
        execution_input: qe.QuantumEspressoExecutionInput,
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

        assert qe.QuantumEspressoScfTask.__module__ == defining_module
        assert qe.QuantumEspressoNscfTask.__module__ == defining_module
        assert qe.QuantumEspressoBandPathTask.__module__ == defining_module
        assert qe.QuantumEspressoBandsExtractionTask.__module__ == defining_module
        assert "QuantumEspressoScfTask" in qe.__all__
        assert "QuantumEspressoNscfTask" in qe.__all__
        assert "QuantumEspressoBandPathTask" in qe.__all__
        assert "QuantumEspressoBandsExtractionTask" in qe.__all__
        assert not hasattr(calculators, "QuantumEspressoScfTask")
        assert not hasattr(calculators, "QuantumEspressoNscfTask")
        assert not hasattr(calculators, "QuantumEspressoBandPathTask")
        assert not hasattr(calculators, "QuantumEspressoBandsExtractionTask")
        assert not hasattr(qe, "QuantumEspressoDosTask")

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
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoPwResult:
                raise AssertionError("constructor evidence does not execute")

        class BandsCalculator:
            def execute(
                self,
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoBandsResult:
                raise AssertionError("constructor evidence does not execute")

        scf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=None,
            suffix="scf",
        )
        scf_result = self.pw_result(scf_input, suffix="scf")
        nscf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.nscf.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=scf_result,
            suffix="nscf",
        )
        nscf_result = self.pw_result(nscf_input, suffix="nscf")
        band_path_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.band-path.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=nscf_result,
            suffix="band-path",
        )
        band_path_result = self.pw_result(band_path_input, suffix="band-path")
        extraction_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.bands-extraction.v1"
            ),
            program=qe.QuantumEspressoProgram.BANDS,
            predecessor=band_path_result,
            suffix="bands-extraction",
        )
        tasks = (
            qe.QuantumEspressoScfTask(scf_input, PwCalculator()),
            qe.QuantumEspressoNscfTask(nscf_input, PwCalculator()),
            qe.QuantumEspressoBandPathTask(band_path_input, PwCalculator()),
            qe.QuantumEspressoBandsExtractionTask(extraction_input, BandsCalculator()),
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
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoPwResult:
                raise AssertionError("invalid tasks do not execute")

        class BandsCalculator:
            def execute(
                self,
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoBandsResult:
                raise AssertionError("invalid tasks do not execute")

        scf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.scf.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=None,
            suffix="shape-scf",
        )
        scf_result = self.pw_result(scf_input, suffix="shape-scf")
        nscf_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.nscf.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=scf_result,
            suffix="shape-nscf",
        )

        with pytest.raises(ValueError, match="must not contain predecessor"):
            qe.QuantumEspressoScfTask(
                replace(
                    scf_input,
                    predecessor_native_state=nscf_input.predecessor_native_state,
                ),
                PwCalculator(),
            )
        with pytest.raises(ValueError, match="requires exactly one predecessor"):
            qe.QuantumEspressoNscfTask(
                replace(nscf_input, predecessor_native_state=()), PwCalculator()
            )
        with pytest.raises(ValueError, match="bands program role"):
            qe.QuantumEspressoBandsExtractionTask(nscf_input, BandsCalculator())
        with pytest.raises(ValueError, match="SCF Task definition"):
            qe.QuantumEspressoScfTask(
                replace(
                    scf_input,
                    task_definition_identity=workflows.TaskDefinitionIdentity(
                        "quantum-espresso.nscf.v1"
                    ),
                ),
                PwCalculator(),
            )
        with pytest.raises(TypeError, match="simulation_input"):
            qe.QuantumEspressoScfTask("invalid", PwCalculator())  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="PlaneWaveCalculator"):
            qe.QuantumEspressoScfTask(scf_input, "invalid")  # type: ignore[arg-type]

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
            program=qe.QuantumEspressoProgram.PW,
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
                simulation_input: qe.QuantumEspressoExecutionInput,
                supplied_context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoPwResult:
                assert simulation_input is execution_input
                assert supplied_context is context
                self.calls += 1
                return expected

        calculator = Calculator()
        task = qe.QuantumEspressoScfTask(execution_input, calculator)

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
            program=qe.QuantumEspressoProgram.PW,
            predecessor=None,
            suffix="nscf-parent",
        )
        predecessor = self.pw_result(scf_input, suffix="nscf-parent")
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.nscf.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=predecessor,
            suffix="execute-nscf",
        )
        expected = self.pw_result(execution_input, suffix="execute-nscf")

        class Calculator:
            def __init__(self) -> None:
                self.calls = 0

            def execute(
                self,
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoPwResult:
                self.calls += 1
                return expected

        calculator = Calculator()
        task = qe.QuantumEspressoNscfTask(execution_input, calculator)
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
            program=qe.QuantumEspressoProgram.PW,
            predecessor=failed,
            suffix="nscf-failed",
        )
        with pytest.raises(ValueError, match="mechanically completed"):
            qe.QuantumEspressoNscfTask(failed_input, calculator).execute(
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
            qe.QuantumEspressoNscfTask(mismatch_input, calculator).execute(
                (binding,), self.context(mismatch_input)
            )
        manifest_mismatch_input = replace(
            execution_input,
            predecessor_native_state=(
                replace(
                    state,
                    content=qe.QuantumEspressoTreeArtifactContent(
                        workflows.ArtifactManifestIdentity("native-output.other"),
                        state.content.manifest_entry_identities,
                    ),
                ),
            ),
        )
        with pytest.raises(ValueError, match="belong to the SCF result manifest"):
            qe.QuantumEspressoNscfTask(manifest_mismatch_input, calculator).execute(
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
            program=qe.QuantumEspressoProgram.PW,
            predecessor=None,
            suffix="band-parent",
        )
        predecessor = self.pw_result(parent_input, suffix="band-parent")
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.band-path.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=predecessor,
            suffix="execute-band-path",
        )
        expected = self.pw_result(execution_input, suffix="execute-band-path")

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoPwResult:
                return expected

        task = qe.QuantumEspressoBandPathTask(execution_input, Calculator())
        binding = workflows.TaskInputBinding("predecessor_result", predecessor)

        assert task.execute((binding,), self.context(execution_input)) == (expected,)

    def test_method__execute__bands_extraction_requires_band_path_result(self) -> None:
        """Evidence ID: SV-QE-TASK-007

        Requirement: Bands extraction accepts one completed ``band_path_result``,
        delegates through a bands-result port, and returns the existing mechanical
        ``QuantumEspressoBandsResult`` variant.

        Acceptance: The exact predecessor and context return one correlated bands
        result; a ``pw`` result from the injected port is rejected as the wrong type.
        """
        band_path_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.band-path.v1"
            ),
            program=qe.QuantumEspressoProgram.PW,
            predecessor=None,
            suffix="extraction-parent",
        )
        predecessor = self.pw_result(band_path_input, suffix="extraction-parent")
        execution_input = self.execution_input(
            definition_identity=workflows.TaskDefinitionIdentity(
                "quantum-espresso.bands-extraction.v1"
            ),
            program=qe.QuantumEspressoProgram.BANDS,
            predecessor=predecessor,
            suffix="execute-extraction",
        )
        expected = self.bands_result(execution_input, suffix="execute-extraction")

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoBandsResult:
                return expected

        task = qe.QuantumEspressoBandsExtractionTask(execution_input, Calculator())
        binding = workflows.TaskInputBinding("band_path_result", predecessor)

        assert task.execute((binding,), self.context(execution_input)) == (expected,)

        class WrongCalculator:
            def execute(
                self,
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoPwResult:
                return predecessor

        wrong_task = qe.QuantumEspressoBandsExtractionTask(
            execution_input,
            WrongCalculator(),  # type: ignore[arg-type]
        )
        with pytest.raises(TypeError, match="QuantumEspressoBandsResult"):
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
            program=qe.QuantumEspressoProgram.PW,
            predecessor=None,
            suffix="result-correlation",
        )
        other_input = replace(
            execution_input,
            identity=qe.QuantumEspressoExecutionInputIdentity("input.other"),
        )
        other_result = self.pw_result(other_input, suffix="result-other")

        class Calculator:
            def execute(
                self,
                simulation_input: qe.QuantumEspressoExecutionInput,
                context: workflows.TaskExecutionContext,
            ) -> qe.QuantumEspressoPwResult:
                return other_result

        task = qe.QuantumEspressoScfTask(execution_input, Calculator())
        with pytest.raises(ValueError, match="exact execution input"):
            task.execute((), self.context(execution_input))
