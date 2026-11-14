r"""Software verification of public Quantum ESPRESSO execution value contract.

Evidence profile: routine

Bounded artifact scope: public QE execution identities, exact input artifacts,
process and stream observations, diagnostic reports, and calculator outcomes.

Facet and represented meaning

The artifact represents immutable QE integration values needed by the first local
Quantum ESPRESSO execution slice.

Intrinsic and cross-object scope

Tests cover exact nominal types, portable artifact destinations, closed input and
process variants, executable-kind separation, diagnostic consistency, immutable
outcomes, canonical integration exports, and absence from the generic calculator
package root.

VVUQ and scientific exclusions

This is software verification using synthetic values. It invokes no executable and
establishes no Quantum ESPRESSO compatibility, numerical verification, scientific
validation, uncertainty quantification, physical correctness, or human acceptance.
"""

from dataclasses import FrozenInstanceError, replace

import pytest
from projectkoios.simulations.execution import CalculatorExitCode

import ksdft2effmass.calculators as calculators
import ksdft2effmass.integration.quantum_espresso as quantum_espresso
from ksdft2effmass.integration.quantum_espresso import (
    QeArtifactDestination,
    QeBandsResult,
    QeCalculatorFailedOutcome,
    QeCompletedOutcome,
    QeDiagnosticChannel,
    QeDiagnosticClassifierIdentity,
    QeDiagnosticDisposition,
    QeDiagnosticObservation,
    QeDiagnosticObservationIdentity,
    QeDiagnosticReport,
    QeDiagnosticReportIdentity,
    QeDiagnosticReportKind,
    QeDiagnosticUnresolvedOutcome,
    QeExecutableConfiguration,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeExecutionInput,
    QeExecutionInputIdentity,
    QeFileArtifactContent,
    QeNativeInputArtifact,
    QeNormalProcessExit,
    QeOperationResultEvidence,
    QeOutputMarkerObservation,
    QeOutputMarkerObservationIdentity,
    QePredecessorNativeStateArtifact,
    QePreparationIdentity,
    QeProcessFailedOutcome,
    QeProcessFailureKind,
    QeProcessObservation,
    QeProcessObservationIdentity,
    QeProcessSignalTermination,
    QeProcessTimeout,
    QeProgram,
    QePseudopotentialArtifact,
    QePwResult,
    QeStreamObservation,
    QeTerminalRecordIdentity,
    QeTreeArtifactContent,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    AttemptIdentity,
    OperationIdentity,
    ResultObject,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
)

pytestmark = pytest.mark.software_verification


class TestQeExecutionContract:
    """Own software verification of the public QE execution value contract."""

    @staticmethod
    def content(character: str, byte_count: int) -> ArtifactContentIdentity:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return ArtifactContentIdentity("sha256", character * 64, byte_count)

    @classmethod
    def diagnostic(
        cls,
        *,
        identity: str,
        channel: QeDiagnosticChannel,
        stream: ArtifactContentIdentity,
        start: int,
        end: int,
        disposition: QeDiagnosticDisposition,
        signature: str | None,
    ) -> QeDiagnosticObservation:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QeDiagnosticObservation(
            identity=QeDiagnosticObservationIdentity(identity),
            channel=channel,
            byte_start=start,
            byte_end=end,
            stream_content_identity=stream,
            span_content_identity=cls.content("c", end - start),
            signature_identity=signature,
            disposition=disposition,
            sanitized_summary="synthetic diagnostic",
            claim_boundary=("synthetic software-verification observation",),
        )

    @classmethod
    def marker(
        cls,
        stream: ArtifactContentIdentity,
    ) -> QeOutputMarkerObservation:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QeOutputMarkerObservation(
            identity=QeOutputMarkerObservationIdentity("marker.job-done"),
            channel=QeDiagnosticChannel.STDOUT,
            byte_start=20,
            byte_end=29,
            stream_content_identity=stream,
            span_content_identity=cls.content("d", 9),
            signature_identity="fixture.pw.job-done.v1",
        )

    @classmethod
    def execution_input(cls) -> QeExecutionInput:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        native = QeNativeInputArtifact(
            ArtifactIdentity("input.pw"),
            QeFileArtifactContent(cls.content("a", 16)),
            QeArtifactDestination("input/pw.in"),
        )
        pseudo = QePseudopotentialArtifact(
            ArtifactIdentity("pseudo.si"),
            QeFileArtifactContent(cls.content("b", 32)),
            QeArtifactDestination("pseudo/Si.UPF"),
        )
        state = QePredecessorNativeStateArtifact(
            ArtifactIdentity("state.scf"),
            QeTreeArtifactContent(
                ArtifactManifestIdentity("manifest.scf"),
                (ArtifactManifestEntryIdentity("manifest.scf.entry"),),
            ),
            QeArtifactDestination("work/si.save"),
            ResultObjectIdentity("result.scf"),
            ArtifactManifestEntryIdentity("manifest.scf.entry"),
        )
        return QeExecutionInput(
            identity=QeExecutionInputIdentity("input.bands"),
            program=QeProgram.PW,
            native_input=native,
            pseudopotentials=(pseudo,),
            predecessor_native_state=(state,),
            task_definition_identity=TaskDefinitionIdentity("task.qe.bands"),
            task_instance_identity=TaskInstanceIdentity("task-instance.qe.bands"),
            activation_identity=TaskActivationIdentity("activation.qe.bands"),
            operation_identity=OperationIdentity("operation.qe.bands"),
            attempt_identity=AttemptIdentity("attempt.qe.bands.1"),
            contract_version="qe-execution-input:1",
        )

    def test_artifact__identity_and_path__rejects_erased_or_escaping_values(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXEC-001

        Requirement: QE owner-local identities require nonempty built-in strings and
        artifact destinations are parent-free portable relative POSIX paths.

        Acceptance: Valid values are retained exactly; wrong semantic types raise
        ``TypeError`` and empty, absolute, native, or traversing paths raise
        ``ValueError``.
        """
        identity = QeExecutionInputIdentity("qe.input")
        destination = QeArtifactDestination("pseudo/Si.UPF")

        assert identity.value == "qe.input"
        assert destination.value == "pseudo/Si.UPF"
        with pytest.raises(TypeError):
            QeExecutionInputIdentity(1)  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            QeExecutionInputIdentity("")
        with pytest.raises(ValueError):
            QeArtifactDestination("/tmp/pw.in")
        with pytest.raises(ValueError):
            QeArtifactDestination("../pw.in")
        with pytest.raises(ValueError):
            QeArtifactDestination("input/../pw.in")
        with pytest.raises(ValueError):
            QeArtifactDestination(r"C:\pw.in")

    def test_artifact__input_variants__retain_exact_provenance_and_correlations(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXEC-002

        Requirement: One execution input retains distinct native-input,
        pseudopotential, and predecessor-tree variants plus exact Task correlations.

        Acceptance: Constructed fields equal the independently supplied identities,
        file and tree variants remain distinct, and collections are immutable tuples.
        """
        value = self.execution_input()
        predecessor = value.predecessor_native_state[0]

        assert value.program is QeProgram.PW
        assert type(value.native_input.content) is QeFileArtifactContent
        assert type(predecessor.content) is QeTreeArtifactContent
        assert predecessor.predecessor_result_identity == ResultObjectIdentity(
            "result.scf"
        )
        assert value.attempt_identity == AttemptIdentity("attempt.qe.bands.1")
        assert type(value.pseudopotentials) is tuple
        with pytest.raises(FrozenInstanceError):
            value.contract_version = "replacement"  # type: ignore[misc]

    def test_artifact__input_invariants__reject_duplicate_or_noncanonical_artifacts(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXEC-003

        Requirement: Input artifact identities and destinations are unique, and
        repeated artifact collections use canonical lexical identity order.

        Acceptance: Duplicate destinations, duplicate identities, and reverse lexical
        order each raise ``ValueError``.
        """
        value = self.execution_input()
        first = value.pseudopotentials[0]
        second = QePseudopotentialArtifact(
            ArtifactIdentity("pseudo.as"),
            QeFileArtifactContent(self.content("e", 40)),
            QeArtifactDestination("pseudo/As.UPF"),
        )
        with pytest.raises(ValueError):
            QeExecutionInput(
                identity=value.identity,
                program=value.program,
                native_input=value.native_input,
                pseudopotentials=(first, first),
                predecessor_native_state=value.predecessor_native_state,
                task_definition_identity=value.task_definition_identity,
                task_instance_identity=value.task_instance_identity,
                activation_identity=value.activation_identity,
                operation_identity=value.operation_identity,
                attempt_identity=value.attempt_identity,
                contract_version=value.contract_version,
            )
        duplicate_destination = QePseudopotentialArtifact(
            ArtifactIdentity("pseudo.other"),
            QeFileArtifactContent(self.content("f", 8)),
            value.native_input.destination,
        )
        with pytest.raises(ValueError):
            QeExecutionInput(
                identity=value.identity,
                program=value.program,
                native_input=value.native_input,
                pseudopotentials=(duplicate_destination,),
                predecessor_native_state=value.predecessor_native_state,
                task_definition_identity=value.task_definition_identity,
                task_instance_identity=value.task_instance_identity,
                activation_identity=value.activation_identity,
                operation_identity=value.operation_identity,
                attempt_identity=value.attempt_identity,
                contract_version=value.contract_version,
            )
        with pytest.raises(ValueError):
            QeExecutionInput(
                identity=value.identity,
                program=value.program,
                native_input=value.native_input,
                pseudopotentials=(first, second),
                predecessor_native_state=value.predecessor_native_state,
                task_definition_identity=value.task_definition_identity,
                task_instance_identity=value.task_instance_identity,
                activation_identity=value.activation_identity,
                operation_identity=value.operation_identity,
                attempt_identity=value.attempt_identity,
                contract_version=value.contract_version,
            )

    def test_artifact__executable_configuration__separates_fixture_from_qe_identity(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXEC-004

        Requirement: Executable kind, version namespace, argv suffix, environment,
        content identity, and classifier identity form one exact immutable binding.

        Acceptance: A canonical fixture configuration is retained; mismatched version
        namespaces and unordered, duplicate, or non-allowlisted environment keys
        raise ``ValueError``.
        """
        configuration = QeExecutableConfiguration(
            identity=QeExecutableConfigurationIdentity("fixture.pw"),
            program=QeProgram.PW,
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            executable_content_identity=self.content("1", 200),
            program_version="fixture-pw-v1",
            argument_suffix=("--case", "success"),
            environment_additions=(("OMP_NUM_THREADS", "1"),),
            classifier_identity=QeDiagnosticClassifierIdentity("fixture-classifier:1"),
            contract_version="qe-executable-configuration:1",
        )

        assert configuration.executable_kind is (QeExecutableKind.DETERMINISTIC_FIXTURE)
        with pytest.raises(ValueError):
            QeExecutableConfiguration(
                identity=configuration.identity,
                program=configuration.program,
                executable_kind=QeExecutableKind.QUANTUM_ESPRESSO,
                executable_content_identity=configuration.executable_content_identity,
                program_version="fixture-pw-v1",
                argument_suffix=(),
                environment_additions=(),
                classifier_identity=configuration.classifier_identity,
                contract_version=configuration.contract_version,
            )
        with pytest.raises(ValueError):
            QeExecutableConfiguration(
                identity=configuration.identity,
                program=configuration.program,
                executable_kind=configuration.executable_kind,
                executable_content_identity=configuration.executable_content_identity,
                program_version=configuration.program_version,
                argument_suffix=(),
                environment_additions=(("Z", "1"), ("A", "2")),
                classifier_identity=configuration.classifier_identity,
                contract_version=configuration.contract_version,
            )
        with pytest.raises(ValueError):
            replace(configuration, environment_additions=(("QE_UNBOUNDED", "1"),))

    def test_artifact__process_observation__keeps_streams_and_termination_separate(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXEC-005

        Requirement: Process termination and independently identified stdout/stderr
        artifacts remain separate mechanical facts with exact unsigned observations.

        Acceptance: Normal, signal, and timeout variants remain distinct; swapped
        stream channels and invalid timeout cleanup state are rejected.
        """
        stdout_content = self.content("2", 100)
        stderr_content = self.content("3", 20)
        observation = QeProcessObservation(
            identity=QeProcessObservationIdentity("process.1"),
            execution_input_identity=QeExecutionInputIdentity("input.1"),
            executable_configuration_identity=(
                QeExecutableConfigurationIdentity("executable.1")
            ),
            preparation_identity=QePreparationIdentity("preparation.1"),
            attempt_identity=AttemptIdentity("attempt.1"),
            argv_content_identity=self.content("4", 24),
            termination=QeNormalProcessExit(CalculatorExitCode(0)),
            wall_duration_nanoseconds=50,
            stdout=QeStreamObservation(
                channel=QeDiagnosticChannel.STDOUT,
                artifact_identity=ArtifactIdentity("stream.stdout"),
                content_identity=stdout_content,
            ),
            stderr=QeStreamObservation(
                channel=QeDiagnosticChannel.STDERR,
                artifact_identity=ArtifactIdentity("stream.stderr"),
                content_identity=stderr_content,
            ),
            before_snapshot_identity=ArtifactManifestIdentity("snapshot.before"),
            after_snapshot_identity=ArtifactManifestIdentity("snapshot.after"),
            created_entry_count=2,
            created_total_bytes=120,
            peak_resident_bytes=None,
            observer_version="process-observer:1",
        )

        assert type(observation.termination) is QeNormalProcessExit
        assert type(QeProcessSignalTermination(15)) is (QeProcessSignalTermination)
        timeout = QeProcessTimeout(
            timeout_milliseconds=100,
            termination_sent=True,
            kill_sent=True,
        )
        assert timeout.kill_sent
        with pytest.raises(ValueError):
            QeProcessTimeout(
                timeout_milliseconds=100,
                termination_sent=False,
                kill_sent=True,
            )
        with pytest.raises(ValueError):
            QeProcessObservation(
                identity=observation.identity,
                execution_input_identity=observation.execution_input_identity,
                executable_configuration_identity=(
                    observation.executable_configuration_identity
                ),
                preparation_identity=observation.preparation_identity,
                attempt_identity=observation.attempt_identity,
                argv_content_identity=observation.argv_content_identity,
                termination=observation.termination,
                wall_duration_nanoseconds=observation.wall_duration_nanoseconds,
                stdout=observation.stderr,
                stderr=observation.stdout,
                before_snapshot_identity=observation.before_snapshot_identity,
                after_snapshot_identity=observation.after_snapshot_identity,
                created_entry_count=observation.created_entry_count,
                created_total_bytes=observation.created_total_bytes,
                peak_resident_bytes=observation.peak_resident_bytes,
                observer_version=observation.observer_version,
            )

    def test_artifact__diagnostic_report__enforces_stream_spans_and_closed_kind(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXEC-006

        Requirement: Diagnostic reports retain exact per-stream spans and classifier
        identity, and their closed kind agrees with diagnostic dispositions.

        Acceptance: Clear and unresolved reports construct with matching observations;
        span overflow, wrong stream identity, and mismatched report kind are rejected.
        """
        stdout = self.content("5", 100)
        stderr = self.content("6", 20)
        warning = self.diagnostic(
            identity="diagnostic.warning",
            channel=QeDiagnosticChannel.STDERR,
            stream=stderr,
            start=0,
            end=10,
            disposition=QeDiagnosticDisposition.NONBLOCKING,
            signature="fixture.warning.v1",
        )
        marker = self.marker(stdout)
        clear = QeDiagnosticReport(
            identity=QeDiagnosticReportIdentity("report.clear"),
            classifier_identity=QeDiagnosticClassifierIdentity("fixture-classifier:1"),
            executable_configuration_identity=(
                QeExecutableConfigurationIdentity("fixture.pw")
            ),
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            program=QeProgram.PW,
            program_version="fixture-pw-v1",
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(warning,),
            completion_markers=(marker,),
            kind=QeDiagnosticReportKind.CLEAR,
            claim_boundary=("synthetic software-verification classification",),
        )
        unknown = self.diagnostic(
            identity="diagnostic.unknown",
            channel=QeDiagnosticChannel.STDERR,
            stream=stderr,
            start=10,
            end=20,
            disposition=QeDiagnosticDisposition.UNRESOLVED,
            signature=None,
        )
        unresolved = QeDiagnosticReport(
            identity=QeDiagnosticReportIdentity("report.unresolved"),
            classifier_identity=clear.classifier_identity,
            executable_configuration_identity=clear.executable_configuration_identity,
            executable_kind=clear.executable_kind,
            program=clear.program,
            program_version=clear.program_version,
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(warning, unknown),
            completion_markers=(marker,),
            kind=QeDiagnosticReportKind.UNRESOLVED,
            claim_boundary=clear.claim_boundary,
        )

        assert clear.kind is QeDiagnosticReportKind.CLEAR
        assert unresolved.kind is QeDiagnosticReportKind.UNRESOLVED
        with pytest.raises(ValueError):
            QeDiagnosticReport(
                identity=unresolved.identity,
                classifier_identity=unresolved.classifier_identity,
                executable_configuration_identity=(
                    unresolved.executable_configuration_identity
                ),
                executable_kind=unresolved.executable_kind,
                program=unresolved.program,
                program_version=unresolved.program_version,
                stdout_content_identity=stdout,
                stderr_content_identity=stderr,
                observations=unresolved.observations,
                completion_markers=unresolved.completion_markers,
                kind=QeDiagnosticReportKind.CLEAR,
                claim_boundary=unresolved.claim_boundary,
            )
        fatal = self.diagnostic(
            identity="diagnostic.fatal",
            channel=QeDiagnosticChannel.STDOUT,
            stream=stdout,
            start=0,
            end=10,
            disposition=QeDiagnosticDisposition.FATAL,
            signature="fixture.fatal.v1",
        )
        with pytest.raises(ValueError):
            replace(
                clear,
                observations=(fatal,),
                kind=QeDiagnosticReportKind.FATAL,
            )
        with pytest.raises(ValueError):
            self.diagnostic(
                identity="diagnostic.overflow",
                channel=QeDiagnosticChannel.STDERR,
                stream=stderr,
                start=15,
                end=25,
                disposition=QeDiagnosticDisposition.UNRESOLVED,
                signature=None,
            )

    def test_artifact__outcome_variants__remain_closed_and_nonretrying(self) -> None:
        """Evidence ID: SV-QE-EXEC-007

        Requirement: Completed, calculator-failed, process-failed, and unresolved
        outcomes are distinct immutable variants with no retry operation.

        Acceptance: Each valid variant retains only its applicable state, empty
        evidence collections are rejected, and none exposes ``retry``.
        """
        completed = QeCompletedOutcome(
            (QeOutputMarkerObservationIdentity("marker.job-done"),)
        )
        calculator_failed = QeCalculatorFailedOutcome(
            (QeDiagnosticObservationIdentity("diagnostic.fatal"),)
        )
        process_failed = QeProcessFailedOutcome(QeProcessFailureKind.NONZERO_EXIT)
        unresolved = QeDiagnosticUnresolvedOutcome(
            (QeDiagnosticObservationIdentity("diagnostic.unknown"),)
        )

        assert type(completed) is QeCompletedOutcome
        assert type(calculator_failed) is QeCalculatorFailedOutcome
        assert process_failed.reason is QeProcessFailureKind.NONZERO_EXIT
        assert type(unresolved) is QeDiagnosticUnresolvedOutcome
        assert all(
            not hasattr(value, "retry")
            for value in (completed, calculator_failed, process_failed, unresolved)
        )
        with pytest.raises(ValueError):
            QeCompletedOutcome(())
        with pytest.raises(TypeError):
            QeProcessFailedOutcome("timeout")  # type: ignore[arg-type]

    def test_artifact__program_results__retain_correlated_result_evidence(
        self,
    ) -> None:
        """Evidence ID: SV-QE-EXEC-009

        Requirement: QE ``pw`` and ``bands`` ResultObjects retain exact producer,
        process, diagnostic, outcome, native-manifest, and terminal identities without
        adding retry or scientific acceptance behavior.

        Acceptance: A correlated ``pw`` value implements ``ResultObject`` and rejects
        construction as the distinct ``bands`` variant.
        """
        execution_input = self.execution_input()
        stdout = self.content("a", 40)
        stderr = self.content("b", 0)
        process = QeProcessObservation(
            identity=QeProcessObservationIdentity("process.result"),
            execution_input_identity=execution_input.identity,
            executable_configuration_identity=(
                QeExecutableConfigurationIdentity("configuration.pw")
            ),
            preparation_identity=QePreparationIdentity("preparation.result"),
            attempt_identity=execution_input.attempt_identity,
            argv_content_identity=self.content("e", 10),
            termination=QeNormalProcessExit(CalculatorExitCode(0)),
            wall_duration_nanoseconds=1,
            stdout=QeStreamObservation(
                channel=QeDiagnosticChannel.STDOUT,
                artifact_identity=ArtifactIdentity("artifact.stdout"),
                content_identity=stdout,
            ),
            stderr=QeStreamObservation(
                channel=QeDiagnosticChannel.STDERR,
                artifact_identity=ArtifactIdentity("artifact.stderr"),
                content_identity=stderr,
            ),
            before_snapshot_identity=ArtifactManifestIdentity("snapshot.before"),
            after_snapshot_identity=ArtifactManifestIdentity("snapshot.after"),
            created_entry_count=2,
            created_total_bytes=40,
            peak_resident_bytes=None,
            observer_version="qe-process-observer:1",
        )
        marker = self.marker(stdout)
        report = QeDiagnosticReport(
            identity=QeDiagnosticReportIdentity("report.result"),
            classifier_identity=QeDiagnosticClassifierIdentity("classifier.fixture"),
            executable_configuration_identity=(
                process.executable_configuration_identity
            ),
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            program=QeProgram.PW,
            program_version="fixture-pw-v1",
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(),
            completion_markers=(marker,),
            kind=QeDiagnosticReportKind.CLEAR,
            claim_boundary=("synthetic result evidence",),
        )
        evidence = QeOperationResultEvidence(
            execution_input=execution_input,
            process_observation=process,
            diagnostic_report=report,
            calculator_outcome=QeCompletedOutcome((marker.identity,)),
            native_output_manifest_identity=ArtifactManifestIdentity("native.manifest"),
            native_output_entry_identities=(
                ArtifactManifestEntryIdentity("native.entry.stderr"),
                ArtifactManifestEntryIdentity("native.entry.stdout"),
            ),
            terminal_record_identity=QeTerminalRecordIdentity("terminal.record"),
        )
        result = QePwResult(
            identity=ResultObjectIdentity("result.pw"),
            execution_input=evidence.execution_input,
            process_observation=evidence.process_observation,
            diagnostic_report=evidence.diagnostic_report,
            calculator_outcome=evidence.calculator_outcome,
            native_output_manifest_identity=evidence.native_output_manifest_identity,
            native_output_entry_identities=evidence.native_output_entry_identities,
            execution_record_manifest_entry_identity=ArtifactManifestEntryIdentity(
                "execution.record"
            ),
            execution_record_content_identity=ArtifactContentIdentity(
                "sha256", "9" * 64, 101
            ),
            execution_record_publication_snapshot_identity=ArtifactManifestIdentity(
                "execution.publication"
            ),
            terminal_record_identity=evidence.terminal_record_identity,
            terminal_record_content_identity=ArtifactContentIdentity(
                "sha256", "a" * 64, 202
            ),
            contract_version="qe-pw-result:2",
        )

        assert isinstance(result, ResultObject)
        assert result.process_observation is process
        assert not hasattr(result, "retry")
        with pytest.raises(ValueError):
            QeBandsResult(
                identity=ResultObjectIdentity("result.bands"),
                evidence=evidence,
                contract_version="qe-bands-result:1",
            )
        with pytest.raises(ValueError):
            replace(
                evidence,
                execution_input=replace(
                    execution_input,
                    attempt_identity=AttemptIdentity("attempt.mismatch"),
                ),
            )

    def test_public_api__package__exports_only_from_qe_integration(self) -> None:
        """Evidence ID: SV-QE-EXEC-008

        Requirement: QE execution contracts are public from the canonical integration
        package and do not leak into the backend-neutral calculator package root.

        Acceptance: Representative names resolve to their exact canonical objects and
        remain absent from the calculator package root.
        """
        assert quantum_espresso.QeExecutionInput is QeExecutionInput
        assert quantum_espresso.QeDiagnosticReport is QeDiagnosticReport
        assert "QeExecutionInput" in quantum_espresso.__all__
        assert "QeDiagnosticReport" in quantum_espresso.__all__
        assert "QeCalculatorOutcome" in quantum_espresso.__all__
        assert not hasattr(calculators, "QeExecutionInput")
        assert not hasattr(calculators, "QeDiagnosticReport")
        assert not hasattr(calculators, "QeCalculatorOutcome")
        assert not hasattr(quantum_espresso, "QuantumEspressoExecutionInput")
        assert not hasattr(quantum_espresso, "QuantumEspressoDiagnosticReport")
        assert not hasattr(quantum_espresso, "QuantumEspressoCalculatorOutcome")
