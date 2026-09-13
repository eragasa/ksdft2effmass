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

import ksdft2effmass.calculators as calculators
import ksdft2effmass.integration.quantum_espresso as quantum_espresso
from ksdft2effmass.integration.quantum_espresso import (
    QuantumEspressoArtifactDestination,
    QuantumEspressoBandsResult,
    QuantumEspressoCalculatorFailedOutcome,
    QuantumEspressoCompletedOutcome,
    QuantumEspressoDiagnosticChannel,
    QuantumEspressoDiagnosticClassifierIdentity,
    QuantumEspressoDiagnosticDisposition,
    QuantumEspressoDiagnosticObservation,
    QuantumEspressoDiagnosticObservationIdentity,
    QuantumEspressoDiagnosticReport,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoDiagnosticReportKind,
    QuantumEspressoDiagnosticUnresolvedOutcome,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoExecutionInput,
    QuantumEspressoExecutionInputIdentity,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoNormalProcessExit,
    QuantumEspressoOperationResultEvidence,
    QuantumEspressoOutputMarkerObservation,
    QuantumEspressoOutputMarkerObservationIdentity,
    QuantumEspressoPredecessorNativeStateArtifact,
    QuantumEspressoPreparationIdentity,
    QuantumEspressoProcessFailedOutcome,
    QuantumEspressoProcessFailureKind,
    QuantumEspressoProcessObservation,
    QuantumEspressoProcessObservationIdentity,
    QuantumEspressoProcessSignalTermination,
    QuantumEspressoProcessTimeout,
    QuantumEspressoProgram,
    QuantumEspressoPseudopotentialArtifact,
    QuantumEspressoPwResult,
    QuantumEspressoStreamObservation,
    QuantumEspressoTerminalRecordIdentity,
    QuantumEspressoTreeArtifactContent,
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


class TestQuantumEspressoExecutionContract:
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
        channel: QuantumEspressoDiagnosticChannel,
        stream: ArtifactContentIdentity,
        start: int,
        end: int,
        disposition: QuantumEspressoDiagnosticDisposition,
        signature: str | None,
    ) -> QuantumEspressoDiagnosticObservation:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QuantumEspressoDiagnosticObservation(
            identity=QuantumEspressoDiagnosticObservationIdentity(identity),
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
    ) -> QuantumEspressoOutputMarkerObservation:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QuantumEspressoOutputMarkerObservation(
            identity=QuantumEspressoOutputMarkerObservationIdentity("marker.job-done"),
            channel=QuantumEspressoDiagnosticChannel.STDOUT,
            byte_start=20,
            byte_end=29,
            stream_content_identity=stream,
            span_content_identity=cls.content("d", 9),
            signature_identity="fixture.pw.job-done.v1",
        )

    @classmethod
    def execution_input(cls) -> QuantumEspressoExecutionInput:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        native = QuantumEspressoNativeInputArtifact(
            ArtifactIdentity("input.pw"),
            QuantumEspressoFileArtifactContent(cls.content("a", 16)),
            QuantumEspressoArtifactDestination("input/pw.in"),
        )
        pseudo = QuantumEspressoPseudopotentialArtifact(
            ArtifactIdentity("pseudo.si"),
            QuantumEspressoFileArtifactContent(cls.content("b", 32)),
            QuantumEspressoArtifactDestination("pseudo/Si.UPF"),
        )
        state = QuantumEspressoPredecessorNativeStateArtifact(
            ArtifactIdentity("state.scf"),
            QuantumEspressoTreeArtifactContent(
                ArtifactManifestIdentity("manifest.scf"),
                (ArtifactManifestEntryIdentity("manifest.scf.entry"),),
            ),
            QuantumEspressoArtifactDestination("work/si.save"),
            ResultObjectIdentity("result.scf"),
            ArtifactManifestEntryIdentity("manifest.scf.entry"),
        )
        return QuantumEspressoExecutionInput(
            identity=QuantumEspressoExecutionInputIdentity("input.bands"),
            program=QuantumEspressoProgram.PW,
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
        identity = QuantumEspressoExecutionInputIdentity("qe.input")
        destination = QuantumEspressoArtifactDestination("pseudo/Si.UPF")

        assert identity.value == "qe.input"
        assert destination.value == "pseudo/Si.UPF"
        with pytest.raises(TypeError):
            QuantumEspressoExecutionInputIdentity(1)  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            QuantumEspressoExecutionInputIdentity("")
        with pytest.raises(ValueError):
            QuantumEspressoArtifactDestination("/tmp/pw.in")
        with pytest.raises(ValueError):
            QuantumEspressoArtifactDestination("../pw.in")
        with pytest.raises(ValueError):
            QuantumEspressoArtifactDestination("input/../pw.in")
        with pytest.raises(ValueError):
            QuantumEspressoArtifactDestination(r"C:\pw.in")

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

        assert value.program is QuantumEspressoProgram.PW
        assert type(value.native_input.content) is QuantumEspressoFileArtifactContent
        assert type(predecessor.content) is QuantumEspressoTreeArtifactContent
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
        second = QuantumEspressoPseudopotentialArtifact(
            ArtifactIdentity("pseudo.as"),
            QuantumEspressoFileArtifactContent(self.content("e", 40)),
            QuantumEspressoArtifactDestination("pseudo/As.UPF"),
        )
        with pytest.raises(ValueError):
            QuantumEspressoExecutionInput(
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
        duplicate_destination = QuantumEspressoPseudopotentialArtifact(
            ArtifactIdentity("pseudo.other"),
            QuantumEspressoFileArtifactContent(self.content("f", 8)),
            value.native_input.destination,
        )
        with pytest.raises(ValueError):
            QuantumEspressoExecutionInput(
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
            QuantumEspressoExecutionInput(
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
        configuration = QuantumEspressoExecutableConfiguration(
            identity=QuantumEspressoExecutableConfigurationIdentity("fixture.pw"),
            program=QuantumEspressoProgram.PW,
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            executable_content_identity=self.content("1", 200),
            program_version="fixture-pw-v1",
            argument_suffix=("--case", "success"),
            environment_additions=(("OMP_NUM_THREADS", "1"),),
            classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                "fixture-classifier:1"
            ),
            contract_version="qe-executable-configuration:1",
        )

        assert configuration.executable_kind is (
            QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE
        )
        with pytest.raises(ValueError):
            QuantumEspressoExecutableConfiguration(
                identity=configuration.identity,
                program=configuration.program,
                executable_kind=QuantumEspressoExecutableKind.QUANTUM_ESPRESSO,
                executable_content_identity=configuration.executable_content_identity,
                program_version="fixture-pw-v1",
                argument_suffix=(),
                environment_additions=(),
                classifier_identity=configuration.classifier_identity,
                contract_version=configuration.contract_version,
            )
        with pytest.raises(ValueError):
            QuantumEspressoExecutableConfiguration(
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
        observation = QuantumEspressoProcessObservation(
            identity=QuantumEspressoProcessObservationIdentity("process.1"),
            execution_input_identity=QuantumEspressoExecutionInputIdentity("input.1"),
            executable_configuration_identity=(
                QuantumEspressoExecutableConfigurationIdentity("executable.1")
            ),
            preparation_identity=QuantumEspressoPreparationIdentity("preparation.1"),
            attempt_identity=AttemptIdentity("attempt.1"),
            argv_content_identity=self.content("4", 24),
            termination=QuantumEspressoNormalProcessExit(0),
            wall_duration_nanoseconds=50,
            stdout=QuantumEspressoStreamObservation(
                channel=QuantumEspressoDiagnosticChannel.STDOUT,
                artifact_identity=ArtifactIdentity("stream.stdout"),
                content_identity=stdout_content,
            ),
            stderr=QuantumEspressoStreamObservation(
                channel=QuantumEspressoDiagnosticChannel.STDERR,
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

        assert type(observation.termination) is QuantumEspressoNormalProcessExit
        assert type(QuantumEspressoProcessSignalTermination(15)) is (
            QuantumEspressoProcessSignalTermination
        )
        timeout = QuantumEspressoProcessTimeout(
            timeout_milliseconds=100,
            termination_sent=True,
            kill_sent=True,
        )
        assert timeout.kill_sent
        with pytest.raises(ValueError):
            QuantumEspressoProcessTimeout(
                timeout_milliseconds=100,
                termination_sent=False,
                kill_sent=True,
            )
        with pytest.raises(ValueError):
            QuantumEspressoProcessObservation(
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
            channel=QuantumEspressoDiagnosticChannel.STDERR,
            stream=stderr,
            start=0,
            end=10,
            disposition=QuantumEspressoDiagnosticDisposition.NONBLOCKING,
            signature="fixture.warning.v1",
        )
        marker = self.marker(stdout)
        clear = QuantumEspressoDiagnosticReport(
            identity=QuantumEspressoDiagnosticReportIdentity("report.clear"),
            classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                "fixture-classifier:1"
            ),
            executable_configuration_identity=(
                QuantumEspressoExecutableConfigurationIdentity("fixture.pw")
            ),
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            program=QuantumEspressoProgram.PW,
            program_version="fixture-pw-v1",
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(warning,),
            completion_markers=(marker,),
            kind=QuantumEspressoDiagnosticReportKind.CLEAR,
            claim_boundary=("synthetic software-verification classification",),
        )
        unknown = self.diagnostic(
            identity="diagnostic.unknown",
            channel=QuantumEspressoDiagnosticChannel.STDERR,
            stream=stderr,
            start=10,
            end=20,
            disposition=QuantumEspressoDiagnosticDisposition.UNRESOLVED,
            signature=None,
        )
        unresolved = QuantumEspressoDiagnosticReport(
            identity=QuantumEspressoDiagnosticReportIdentity("report.unresolved"),
            classifier_identity=clear.classifier_identity,
            executable_configuration_identity=clear.executable_configuration_identity,
            executable_kind=clear.executable_kind,
            program=clear.program,
            program_version=clear.program_version,
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(warning, unknown),
            completion_markers=(marker,),
            kind=QuantumEspressoDiagnosticReportKind.UNRESOLVED,
            claim_boundary=clear.claim_boundary,
        )

        assert clear.kind is QuantumEspressoDiagnosticReportKind.CLEAR
        assert unresolved.kind is QuantumEspressoDiagnosticReportKind.UNRESOLVED
        with pytest.raises(ValueError):
            QuantumEspressoDiagnosticReport(
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
                kind=QuantumEspressoDiagnosticReportKind.CLEAR,
                claim_boundary=unresolved.claim_boundary,
            )
        fatal = self.diagnostic(
            identity="diagnostic.fatal",
            channel=QuantumEspressoDiagnosticChannel.STDOUT,
            stream=stdout,
            start=0,
            end=10,
            disposition=QuantumEspressoDiagnosticDisposition.FATAL,
            signature="fixture.fatal.v1",
        )
        with pytest.raises(ValueError):
            replace(
                clear,
                observations=(fatal,),
                kind=QuantumEspressoDiagnosticReportKind.FATAL,
            )
        with pytest.raises(ValueError):
            self.diagnostic(
                identity="diagnostic.overflow",
                channel=QuantumEspressoDiagnosticChannel.STDERR,
                stream=stderr,
                start=15,
                end=25,
                disposition=QuantumEspressoDiagnosticDisposition.UNRESOLVED,
                signature=None,
            )

    def test_artifact__outcome_variants__remain_closed_and_nonretrying(self) -> None:
        """Evidence ID: SV-QE-EXEC-007

        Requirement: Completed, calculator-failed, process-failed, and unresolved
        outcomes are distinct immutable variants with no retry operation.

        Acceptance: Each valid variant retains only its applicable state, empty
        evidence collections are rejected, and none exposes ``retry``.
        """
        completed = QuantumEspressoCompletedOutcome(
            (QuantumEspressoOutputMarkerObservationIdentity("marker.job-done"),)
        )
        calculator_failed = QuantumEspressoCalculatorFailedOutcome(
            (QuantumEspressoDiagnosticObservationIdentity("diagnostic.fatal"),)
        )
        process_failed = QuantumEspressoProcessFailedOutcome(
            QuantumEspressoProcessFailureKind.NONZERO_EXIT
        )
        unresolved = QuantumEspressoDiagnosticUnresolvedOutcome(
            (QuantumEspressoDiagnosticObservationIdentity("diagnostic.unknown"),)
        )

        assert type(completed) is QuantumEspressoCompletedOutcome
        assert type(calculator_failed) is QuantumEspressoCalculatorFailedOutcome
        assert process_failed.reason is QuantumEspressoProcessFailureKind.NONZERO_EXIT
        assert type(unresolved) is QuantumEspressoDiagnosticUnresolvedOutcome
        assert all(
            not hasattr(value, "retry")
            for value in (completed, calculator_failed, process_failed, unresolved)
        )
        with pytest.raises(ValueError):
            QuantumEspressoCompletedOutcome(())
        with pytest.raises(TypeError):
            QuantumEspressoProcessFailedOutcome("timeout")  # type: ignore[arg-type]

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
        process = QuantumEspressoProcessObservation(
            identity=QuantumEspressoProcessObservationIdentity("process.result"),
            execution_input_identity=execution_input.identity,
            executable_configuration_identity=(
                QuantumEspressoExecutableConfigurationIdentity("configuration.pw")
            ),
            preparation_identity=QuantumEspressoPreparationIdentity(
                "preparation.result"
            ),
            attempt_identity=execution_input.attempt_identity,
            argv_content_identity=self.content("e", 10),
            termination=QuantumEspressoNormalProcessExit(0),
            wall_duration_nanoseconds=1,
            stdout=QuantumEspressoStreamObservation(
                channel=QuantumEspressoDiagnosticChannel.STDOUT,
                artifact_identity=ArtifactIdentity("artifact.stdout"),
                content_identity=stdout,
            ),
            stderr=QuantumEspressoStreamObservation(
                channel=QuantumEspressoDiagnosticChannel.STDERR,
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
        report = QuantumEspressoDiagnosticReport(
            identity=QuantumEspressoDiagnosticReportIdentity("report.result"),
            classifier_identity=QuantumEspressoDiagnosticClassifierIdentity(
                "classifier.fixture"
            ),
            executable_configuration_identity=(
                process.executable_configuration_identity
            ),
            executable_kind=QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE,
            program=QuantumEspressoProgram.PW,
            program_version="fixture-pw-v1",
            stdout_content_identity=stdout,
            stderr_content_identity=stderr,
            observations=(),
            completion_markers=(marker,),
            kind=QuantumEspressoDiagnosticReportKind.CLEAR,
            claim_boundary=("synthetic result evidence",),
        )
        evidence = QuantumEspressoOperationResultEvidence(
            execution_input=execution_input,
            process_observation=process,
            diagnostic_report=report,
            calculator_outcome=QuantumEspressoCompletedOutcome((marker.identity,)),
            native_output_manifest_identity=ArtifactManifestIdentity("native.manifest"),
            native_output_entry_identities=(
                ArtifactManifestEntryIdentity("native.entry.stderr"),
                ArtifactManifestEntryIdentity("native.entry.stdout"),
            ),
            terminal_record_identity=QuantumEspressoTerminalRecordIdentity(
                "terminal.record"
            ),
        )
        result = QuantumEspressoPwResult(
            identity=ResultObjectIdentity("result.pw"),
            evidence=evidence,
            contract_version="qe-pw-result:1",
        )

        assert isinstance(result, ResultObject)
        assert result.evidence.process_observation is process
        assert not hasattr(result, "retry")
        with pytest.raises(ValueError):
            QuantumEspressoBandsResult(
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
        assert (
            quantum_espresso.QuantumEspressoExecutionInput
            is QuantumEspressoExecutionInput
        )
        assert (
            quantum_espresso.QuantumEspressoDiagnosticReport
            is QuantumEspressoDiagnosticReport
        )
        assert "QuantumEspressoExecutionInput" in quantum_espresso.__all__
        assert "QuantumEspressoDiagnosticReport" in quantum_espresso.__all__
        assert "QuantumEspressoCalculatorOutcome" in quantum_espresso.__all__
        assert not hasattr(calculators, "QuantumEspressoExecutionInput")
        assert not hasattr(calculators, "QuantumEspressoDiagnosticReport")
        assert not hasattr(calculators, "QuantumEspressoCalculatorOutcome")
