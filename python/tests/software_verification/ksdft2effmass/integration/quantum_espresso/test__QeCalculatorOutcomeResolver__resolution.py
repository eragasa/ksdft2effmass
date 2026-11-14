r"""Software verification of ``QeCalculatorOutcomeResolver``.

Evidence profile: routine

Bounded artifact scope: fail-closed cross-record QE calculator-outcome precedence over
synthetic process, diagnostic, and native-output observations.

Facet and represented meaning

The ActionObject resolves only mechanical calculator completion and failure variants.

Intrinsic and cross-object scope

Cases cover completed, calculator-failed, process-failed, unresolved diagnostics,
missing completion markers, and cross-object identity mismatch. Workflow admission,
retry, numerical convergence, and scientific interpretation remain separate.

VVUQ and scientific exclusions

All values are synthetic test data. These tests establish software behavior only and
perform no scientific execution, validation, or uncertainty quantification.
"""

from __future__ import annotations

import hashlib

import pytest
from projectkoios.simulations.execution import CalculatorExitCode

from ksdft2effmass.integration.quantum_espresso import (
    QeArtifactDestination,
    QeCalculatorFailedOutcome,
    QeCalculatorOutcomeResolver,
    QeCompletedOutcome,
    QeDiagnosticCatalog,
    QeDiagnosticChannel,
    QeDiagnosticClassificationRequest,
    QeDiagnosticClassifier,
    QeDiagnosticReport,
    QeDiagnosticReportIdentity,
    QeDiagnosticUnresolvedOutcome,
    QeExecutableConfiguration,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeExecutionInputIdentity,
    QeFileArtifactContent,
    QeNativeOutputCandidateSpecification,
    QeNativeOutputExtractionSpecification,
    QeNativeOutputManifest,
    QeNativeOutputManifestEntry,
    QeNativeOutputRole,
    QeNormalProcessExit,
    QePreparationIdentity,
    QeProcessFailedOutcome,
    QeProcessFailureKind,
    QeProcessObservation,
    QeProcessObservationIdentity,
    QeProcessSignalTermination,
    QeProcessTimeout,
    QeProgram,
    QeStreamObservation,
    QeWorkspaceEntryType,
)
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    AttemptIdentity,
)

pytestmark = pytest.mark.software_verification
SUT = QeCalculatorOutcomeResolver


class TestQeCalculatorOutcomeResolver:
    """Own fail-closed calculator-outcome resolution verification."""

    @staticmethod
    def content_identity(content: bytes) -> ArtifactContentIdentity:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return ArtifactContentIdentity(
            "sha256", hashlib.sha256(content).hexdigest(), len(content)
        )

    @classmethod
    def configuration(cls) -> QeExecutableConfiguration:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        catalog = QeDiagnosticCatalog.fixture_pw_v1()
        return QeExecutableConfiguration(
            identity=QeExecutableConfigurationIdentity("fixture.configuration"),
            program=QeProgram.PW,
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            executable_content_identity=cls.content_identity(b"fixture executable"),
            program_version="fixture-pw-v1",
            argument_suffix=("--fixture-mode",),
            environment_additions=(),
            classifier_identity=catalog.classifier_identity,
            contract_version="qe-executable-configuration:1",
        )

    @classmethod
    def report(cls, stdout: bytes, stderr: bytes) -> QeDiagnosticReport:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        configuration = cls.configuration()
        return QeDiagnosticClassifier(QeDiagnosticCatalog.fixture_pw_v1()).execute(
            QeDiagnosticClassificationRequest(
                report_identity=QeDiagnosticReportIdentity("diagnostic.report"),
                configuration=configuration,
                stdout=stdout,
                stderr=stderr,
                stdout_content_identity=cls.content_identity(stdout),
                stderr_content_identity=cls.content_identity(stderr),
                claim_boundary=("synthetic outcome-resolution fixture",),
            )
        )

    @classmethod
    def specification(
        cls,
    ) -> QeNativeOutputExtractionSpecification:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QeNativeOutputExtractionSpecification(
            identity="fixture-output-specification:1",
            executable_configuration_identity=cls.configuration().identity,
            program=QeProgram.PW,
            executable_kind=QeExecutableKind.DETERMINISTIC_FIXTURE,
            program_version="fixture-pw-v1",
            candidates=(
                QeNativeOutputCandidateSpecification(
                    artifact_identity=ArtifactIdentity("artifact.stderr"),
                    role=QeNativeOutputRole.STDERR,
                    relative_path=QeArtifactDestination("streams/stderr"),
                    entry_type=QeWorkspaceEntryType.REGULAR_FILE,
                    required=True,
                ),
                QeNativeOutputCandidateSpecification(
                    artifact_identity=ArtifactIdentity("artifact.stdout"),
                    role=QeNativeOutputRole.STDOUT,
                    relative_path=QeArtifactDestination("streams/stdout"),
                    entry_type=QeWorkspaceEntryType.REGULAR_FILE,
                    required=True,
                ),
            ),
        )

    @classmethod
    def process(
        cls,
        stdout: bytes,
        stderr: bytes,
        termination: (
            QeNormalProcessExit | QeProcessSignalTermination | QeProcessTimeout
        ),
        *,
        configuration_identity: str = "fixture.configuration",
    ) -> QeProcessObservation:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return QeProcessObservation(
            identity=QeProcessObservationIdentity("process.observation"),
            execution_input_identity=QeExecutionInputIdentity("execution.input"),
            executable_configuration_identity=(
                QeExecutableConfigurationIdentity(configuration_identity)
            ),
            preparation_identity=QePreparationIdentity("preparation"),
            attempt_identity=AttemptIdentity("attempt"),
            argv_content_identity=cls.content_identity(b"argv"),
            termination=termination,
            wall_duration_nanoseconds=1,
            stdout=QeStreamObservation(
                channel=QeDiagnosticChannel.STDOUT,
                artifact_identity=ArtifactIdentity("artifact.stdout"),
                content_identity=cls.content_identity(stdout),
            ),
            stderr=QeStreamObservation(
                channel=QeDiagnosticChannel.STDERR,
                artifact_identity=ArtifactIdentity("artifact.stderr"),
                content_identity=cls.content_identity(stderr),
            ),
            before_snapshot_identity=ArtifactManifestIdentity("snapshot.before"),
            after_snapshot_identity=ArtifactManifestIdentity("snapshot.after"),
            created_entry_count=2,
            created_total_bytes=len(stdout) + len(stderr),
            peak_resident_bytes=None,
            observer_version="qe-process-observer:1",
        )

    @classmethod
    def manifest(cls, stdout: bytes, stderr: bytes) -> QeNativeOutputManifest:
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        entries = (
            QeNativeOutputManifestEntry(
                identity=ArtifactManifestEntryIdentity("manifest.entry.stderr"),
                artifact_identity=ArtifactIdentity("artifact.stderr"),
                role=QeNativeOutputRole.STDERR,
                relative_path=QeArtifactDestination("streams/stderr"),
                entry_type=QeWorkspaceEntryType.REGULAR_FILE,
                content=QeFileArtifactContent(cls.content_identity(stderr)),
                symlink_observed=False,
            ),
            QeNativeOutputManifestEntry(
                identity=ArtifactManifestEntryIdentity("manifest.entry.stdout"),
                artifact_identity=ArtifactIdentity("artifact.stdout"),
                role=QeNativeOutputRole.STDOUT,
                relative_path=QeArtifactDestination("streams/stdout"),
                entry_type=QeWorkspaceEntryType.REGULAR_FILE,
                content=QeFileArtifactContent(cls.content_identity(stdout)),
                symlink_observed=False,
            ),
        )
        return QeNativeOutputManifest(
            identity=ArtifactManifestIdentity("native.output.manifest"),
            preparation_identity=QePreparationIdentity("preparation"),
            after_snapshot_identity=ArtifactManifestIdentity("snapshot.after"),
            extraction_specification_identity="fixture-output-specification:1",
            entries=entries,
        )

    @classmethod
    def resolve(
        cls,
        stdout: bytes,
        stderr: bytes,
        termination: (
            QeNormalProcessExit | QeProcessSignalTermination | QeProcessTimeout
        ),
        *,
        configuration_identity: str = "fixture.configuration",
    ) -> (
        QeCompletedOutcome
        | QeCalculatorFailedOutcome
        | QeProcessFailedOutcome
        | QeDiagnosticUnresolvedOutcome
    ):
        """Evidence ID: This helper owns no identifier.

        Requirement: Provide deterministic typed support for this module's test owners.

        Acceptance: Behavior remains exact and confined to the calling test.
        """
        return SUT("qe-calculator-outcome-resolver:1").execute(
            cls.process(
                stdout,
                stderr,
                termination,
                configuration_identity=configuration_identity,
            ),
            cls.report(stdout, stderr),
            cls.manifest(stdout, stderr),
            cls.specification(),
        )

    def test_method__execute__clear_exit_zero_with_marker_returns_completed(
        self,
    ) -> None:
        """Evidence ID: SV-QE-OUTCOME-001

        Requirement: Only clear exit-zero output with a recognized completion marker
        and required candidate closure is completion eligible.

        Acceptance: The exact marker identity is retained by ``completed``.
        """
        outcome = self.resolve(
            b"JOB DONE.\n",
            b"DIAGNOSTIC: NONBLOCKING synthetic floating-point notice\n",
            QeNormalProcessExit(CalculatorExitCode(0)),
        )

        assert type(outcome) is QeCompletedOutcome
        assert len(outcome.completion_marker_identities) == 1

    def test_method__execute__recognized_fatal_returns_calculator_failed(self) -> None:
        """Evidence ID: SV-QE-OUTCOME-002

        Requirement: Internally consistent recognized fatal output has calculator
        precedence over a nonzero normal exit.

        Acceptance: ``calculator_failed`` retains the exact fatal diagnostic.
        """
        outcome = self.resolve(
            b"DIAGNOSTIC: FATAL c_bands too many bands are not converged\n",
            b"DIAGNOSTIC: SECONDARY synthetic MPI_ABORT\n",
            QeNormalProcessExit(CalculatorExitCode(1)),
        )

        assert type(outcome) is QeCalculatorFailedOutcome
        assert len(outcome.fatal_diagnostic_identities) == 1

    def test_method__execute__clear_nonzero_exit_returns_process_failed(self) -> None:
        """Evidence ID: SV-QE-OUTCOME-003

        Requirement: Nonzero normal exit without recognized fatal diagnostics is a
        process failure.

        Acceptance: The reason is exactly ``nonzero_exit``.
        """
        outcome = self.resolve(
            b"FIXTURE FAILED\n", b"", QeNormalProcessExit(CalculatorExitCode(3))
        )

        assert type(outcome) is QeProcessFailedOutcome
        assert outcome.reason is QeProcessFailureKind.NONZERO_EXIT

    def test_method__execute__signal_or_timeout_returns_process_failed(self) -> None:
        """Evidence ID: SV-QE-OUTCOME-004

        Requirement: Closed signal and timeout observations remain distinct process
        failures regardless of a clear diagnostic report.

        Acceptance: Each termination maps to its exact process-failure reason.
        """
        signal_outcome = self.resolve(
            b"JOB DONE.\n", b"", QeProcessSignalTermination(15)
        )
        timeout_outcome = self.resolve(
            b"",
            b"",
            QeProcessTimeout(
                timeout_milliseconds=30,
                termination_sent=True,
                kill_sent=False,
            ),
        )

        assert type(signal_outcome) is QeProcessFailedOutcome
        assert signal_outcome.reason is QeProcessFailureKind.SIGNAL
        assert type(timeout_outcome) is QeProcessFailedOutcome
        assert timeout_outcome.reason is QeProcessFailureKind.TIMEOUT

    def test_method__execute__unknown_diagnostic_returns_unresolved(self) -> None:
        """Evidence ID: SV-QE-OUTCOME-005

        Requirement: Unknown diagnostic text fails closed before process precedence.

        Acceptance: ``diagnostic_unresolved`` retains the unknown observation.
        """
        outcome = self.resolve(
            b"JOB DONE.\n",
            b"DIAGNOSTIC: UNKNOWN fixture\n",
            QeNormalProcessExit(CalculatorExitCode(0)),
        )

        assert type(outcome) is QeDiagnosticUnresolvedOutcome
        assert len(outcome.diagnostic_identities) == 1
        assert outcome.reason_identities

    def test_method__execute__missing_marker_or_identity_mismatch_returns_unresolved(
        self,
    ) -> None:
        """Evidence ID: SV-QE-OUTCOME-006

        Requirement: Missing completion evidence and cross-record identity mismatch
        never fall through to completion.

        Acceptance: Both cases return deterministic reason-bearing unresolved values.
        """
        missing = self.resolve(
            b"ordinary output\n", b"", QeNormalProcessExit(CalculatorExitCode(0))
        )
        mismatch = self.resolve(
            b"JOB DONE.\n",
            b"",
            QeNormalProcessExit(CalculatorExitCode(0)),
            configuration_identity="different.configuration",
        )

        assert type(missing) is QeDiagnosticUnresolvedOutcome
        assert missing.diagnostic_identities == ()
        assert missing.reason_identities
        assert type(mismatch) is QeDiagnosticUnresolvedOutcome
        assert mismatch.reason_identities != missing.reason_identities
