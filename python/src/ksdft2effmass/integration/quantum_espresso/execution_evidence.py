"""Provider observation and record publication for local QE ``pw.x`` attempts."""

from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from projectkoios.simulations.execution import (
    CalculatorExecutionObservation,
    CalculatorExecutionObservationAssembler,
    CalculatorExecutionObservationRequest,
    CalculatorExecutionRecord,
    CalculatorExitDisposition,
    CalculatorNormalExit,
    CalculatorSignalTermination,
    CalculatorTimeout,
    ExecutionStatus,
)

from ksdft2effmass.serialization import StrWireEnum
from ksdft2effmass.workflows import ArtifactContentIdentity

from .contracts import (
    QeNormalProcessExit,
    QeProcessSignalTermination,
    QeProcessTermination,
    QeProcessTimeout,
    QeProgram,
)
from .effects import (
    QeWorkspaceEntryType,
    QeWorkspaceSnapshot,
    QeWorkspaceSnapshotEntry,
    QeWorkspaceSnapshotFailure,
    QeWorkspaceSnapshotPhase,
    QeWorkspaceSnapshotter,
)
from .execution import (
    LocalQeExecutionRecordDestination,
    LocalQePreparedExecution,
    LocalQeResolvedDestination,
    LocalQeResolvedDestinationRole,
)
from .process import LocalQeCapturedProcess


@dataclass(frozen=True, slots=True)
class QePwEvidenceAdapterIdentity:
    """Identify one exact KSD provider-observation adaptation policy."""

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("value must be a built-in str")
        if not self.value:
            raise ValueError("value must not be empty")


class QePwEvidenceFailureCode(StrWireEnum):
    """Closed failure codes for the local ``pw.x`` evidence application."""

    UNSUPPORTED_PROGRAM = "unsupported_program"
    PREPARATION_CORRELATION_MISMATCH = "preparation_correlation_mismatch"
    SNAPSHOT_CORRELATION_MISMATCH = "snapshot_correlation_mismatch"
    PROVIDER_OBSERVATION_REJECTED = "provider_observation_rejected"
    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    DESTINATION_EXISTS = "destination_exists"
    INVALID_DESTINATION = "invalid_destination"
    LIMIT_EXCEEDED = "limit_exceeded"
    PUBLICATION_FAILED = "publication_failed"
    DURABILITY_UNCERTAIN = "durability_uncertain"
    VERIFICATION_FAILED = "verification_failed"
    DIAGNOSTIC_CORRELATION_MISMATCH = "diagnostic_correlation_mismatch"
    NATIVE_OUTPUT_CORRELATION_MISMATCH = "native_output_correlation_mismatch"
    OUTCOME_CORRELATION_MISMATCH = "outcome_correlation_mismatch"
    TERMINAL_CORRELATION_MISMATCH = "terminal_correlation_mismatch"


@dataclass(frozen=True, slots=True, kw_only=True)
class QePwObservationFailure:
    """Retain one effect-free execution-observation adaptation failure.

    Parameters
    ----------
    code
        Closed failure cause.
    adapter_identity
        Exact KSD adaptation policy identity.
    prepared_execution
        Exact prepared execution supplied to the adapter.
    captured_process
        Exact captured process supplied to the adapter.
    observed_condition
        Sanitized nonempty mechanical condition without native stream bytes.
    """

    code: QePwEvidenceFailureCode
    adapter_identity: QePwEvidenceAdapterIdentity
    prepared_execution: LocalQePreparedExecution
    captured_process: LocalQeCapturedProcess
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QePwEvidenceFailureCode:
            raise TypeError("code must be QePwEvidenceFailureCode")
        if type(self.adapter_identity) is not QePwEvidenceAdapterIdentity:
            raise TypeError("adapter_identity must be QePwEvidenceAdapterIdentity")
        if type(self.prepared_execution) is not LocalQePreparedExecution:
            raise TypeError("prepared_execution must be LocalQePreparedExecution")
        if type(self.captured_process) is not LocalQeCapturedProcess:
            raise TypeError("captured_process must be LocalQeCapturedProcess")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QePwObservation:
    """Retain exact KSD process evidence and its provider-owned observation.

    Parameters
    ----------
    adapter_identity
        Exact KSD adaptation policy identity.
    prepared_execution
        Exact preparation owning command, workspace, and staged-input correlations.
    captured_process
        Exact KSD process, stream, duration, and snapshot evidence.
    provider_observation
        Exact immutable provider observation assembled from those owned facts.

    Notes
    -----
    This binding is not a wire and grants no execution authority. It establishes no
    calculator completion, convergence, scientific validity, or acceptance.
    """

    adapter_identity: QePwEvidenceAdapterIdentity
    prepared_execution: LocalQePreparedExecution
    captured_process: LocalQeCapturedProcess
    provider_observation: CalculatorExecutionObservation

    def __post_init__(self) -> None:
        if type(self.adapter_identity) is not QePwEvidenceAdapterIdentity:
            raise TypeError("adapter_identity must be QePwEvidenceAdapterIdentity")
        if type(self.prepared_execution) is not LocalQePreparedExecution:
            raise TypeError("prepared_execution must be LocalQePreparedExecution")
        if type(self.captured_process) is not LocalQeCapturedProcess:
            raise TypeError("captured_process must be LocalQeCapturedProcess")
        if type(self.provider_observation) is not CalculatorExecutionObservation:
            raise TypeError(
                "provider_observation must be CalculatorExecutionObservation"
            )
        provider = self.provider_observation
        process = self.captured_process.observation
        if not provider.process_entered:
            raise ValueError("captured process requires entered provider evidence")
        if (
            provider.record.command != self.prepared_execution.argv
            or provider.record.working_directory
            != str(self.prepared_execution.workspace)
        ):
            raise ValueError("provider invocation does not match prepared execution")
        if provider.wall_duration_nanoseconds != process.wall_duration_nanoseconds:
            raise ValueError("provider duration does not match captured process")
        if (
            provider.stdout is None
            or provider.stderr is None
            or provider.stdout.content is not self.captured_process.stdout_bytes
            or provider.stderr.content is not self.captured_process.stderr_bytes
            or provider.stdout.content_identity.sha256
            != process.stdout.content_identity.digest
            or provider.stdout.content_identity.byte_size
            != process.stdout.content_identity.byte_count
            or provider.stderr.content_identity.sha256
            != process.stderr.content_identity.digest
            or provider.stderr.content_identity.byte_size
            != process.stderr.content_identity.byte_count
        ):
            raise ValueError("provider streams do not match captured process")
        termination = process.termination
        provider_termination = provider.termination
        if type(termination) is QeNormalProcessExit:
            if (
                type(provider_termination) is not CalculatorNormalExit
                or provider_termination.exit_code != termination.exit_code
            ):
                raise ValueError("provider normal exit does not match captured process")
        elif type(termination) is QeProcessSignalTermination:
            if (
                type(provider_termination) is not CalculatorSignalTermination
                or provider_termination.signal_number != termination.signal_number
            ):
                raise ValueError(
                    "provider signal termination does not match captured process"
                )
        else:
            assert type(termination) is QeProcessTimeout
            if (
                type(provider_termination) is not CalculatorTimeout
                or provider_termination.timeout_seconds
                != termination.timeout_milliseconds / 1000.0
                or provider_termination.termination_sent
                is not termination.termination_sent
                or provider_termination.kill_sent is not termination.kill_sent
            ):
                raise ValueError("provider timeout does not match captured process")


type QePwObservationResult = QePwObservation | QePwObservationFailure


@dataclass(frozen=True, slots=True)
class QePwEvidenceAdapter:
    """Adapt object-owned KSD process facts into exact provider evidence.

    Parameters
    ----------
    identity
        Exact KSD adaptation policy identity.
    provider_assembler
        Effect-free provider owner of execution-observation assembly and the retained
        ``execution.json`` wire.
    """

    identity: QePwEvidenceAdapterIdentity
    provider_assembler: CalculatorExecutionObservationAssembler

    def __post_init__(self) -> None:
        if type(self.identity) is not QePwEvidenceAdapterIdentity:
            raise TypeError("identity must be QePwEvidenceAdapterIdentity")
        if type(self.provider_assembler) is not (
            CalculatorExecutionObservationAssembler
        ):
            raise TypeError(
                "provider_assembler must be CalculatorExecutionObservationAssembler"
            )

    def execute(
        self,
        prepared_execution: LocalQePreparedExecution,
        captured_process: LocalQeCapturedProcess,
    ) -> QePwObservationResult:
        """Return exact provider evidence or one typed fail-closed result."""
        if type(prepared_execution) is not LocalQePreparedExecution:
            raise TypeError("prepared_execution must be LocalQePreparedExecution")
        if type(captured_process) is not LocalQeCapturedProcess:
            raise TypeError("captured_process must be LocalQeCapturedProcess")
        process = captured_process.observation
        if (
            prepared_execution.request.executable_configuration.program
            is not QeProgram.PW
        ):
            return self._failure(
                QePwEvidenceFailureCode.UNSUPPORTED_PROGRAM,
                prepared_execution,
                captured_process,
                "the pw.x evidence application does not admit another QE program",
            )
        if (
            process.preparation_identity != prepared_execution.identity
            or process.execution_input_identity
            != prepared_execution.request.execution_input.identity
            or process.executable_configuration_identity
            != prepared_execution.request.executable_configuration.identity
            or process.attempt_identity
            != prepared_execution.request.execution_input.attempt_identity
        ):
            return self._failure(
                QePwEvidenceFailureCode.PREPARATION_CORRELATION_MISMATCH,
                prepared_execution,
                captured_process,
                "captured process lineage differs from the prepared execution",
            )
        if (
            process.before_snapshot_identity
            != captured_process.before_snapshot.identity
            or process.after_snapshot_identity
            != captured_process.after_snapshot.identity
            or captured_process.before_snapshot.preparation_identity
            != prepared_execution.identity
            or captured_process.after_snapshot.preparation_identity
            != prepared_execution.identity
        ):
            return self._failure(
                QePwEvidenceFailureCode.SNAPSHOT_CORRELATION_MISMATCH,
                prepared_execution,
                captured_process,
                "captured snapshot lineage differs from the process observation",
            )
        record: CalculatorExecutionRecord = self._record(
            prepared_execution, captured_process
        )
        provider_termination = self._provider_termination(process.termination)
        try:
            provider_observation: CalculatorExecutionObservation = (
                self.provider_assembler.action(
                    request=CalculatorExecutionObservationRequest(
                        record=record,
                        record_filename="execution.json",
                        process_entered=True,
                        termination=provider_termination,
                        wall_duration_nanoseconds=process.wall_duration_nanoseconds,
                        stdout_bytes=captured_process.stdout_bytes,
                        stderr_bytes=captured_process.stderr_bytes,
                    )
                )
            )
        except ValueError:
            return self._failure(
                QePwEvidenceFailureCode.PROVIDER_OBSERVATION_REJECTED,
                prepared_execution,
                captured_process,
                "provider observation rejected the exact KSD terminal correlation",
            )
        return QePwObservation(
            adapter_identity=self.identity,
            prepared_execution=prepared_execution,
            captured_process=captured_process,
            provider_observation=provider_observation,
        )

    def _record(
        self,
        prepared_execution: LocalQePreparedExecution,
        captured_process: LocalQeCapturedProcess,
    ) -> CalculatorExecutionRecord:
        termination = captured_process.observation.termination
        status: ExecutionStatus
        returncode: int | None
        if type(termination) is QeNormalProcessExit:
            status = (
                ExecutionStatus.succeeded
                if termination.disposition is CalculatorExitDisposition.succeeded
                else ExecutionStatus.failed
            )
            returncode = termination.exit_code.value
        elif type(termination) is QeProcessSignalTermination:
            status = ExecutionStatus.failed
            returncode = -termination.signal_number
        else:
            assert type(termination) is QeProcessTimeout
            status = ExecutionStatus.timed_out
            returncode = None
        stdout = self._destination(
            prepared_execution, LocalQeResolvedDestinationRole.STDOUT
        )
        stderr = self._destination(
            prepared_execution, LocalQeResolvedDestinationRole.STDERR
        )
        input_filenames: tuple[str, ...] = tuple(
            sorted(
                PurePosixPath(value.portable_destination.value).name
                for value in prepared_execution.resolved_destinations
                if value.role is LocalQeResolvedDestinationRole.INPUT_ARTIFACT
            )
        )
        return CalculatorExecutionRecord(
            command=prepared_execution.argv,
            working_directory=str(prepared_execution.workspace),
            status=status,
            returncode=returncode,
            stdout_filename=PurePosixPath(stdout.portable_destination.value).name,
            stderr_filename=PurePosixPath(stderr.portable_destination.value).name,
            required_input_filenames=input_filenames,
        )

    def _provider_termination(
        self, termination: QeProcessTermination
    ) -> CalculatorNormalExit | CalculatorSignalTermination | CalculatorTimeout:
        if type(termination) is QeNormalProcessExit:
            return CalculatorNormalExit(termination.exit_code)
        if type(termination) is QeProcessSignalTermination:
            return CalculatorSignalTermination(termination.signal_number)
        assert type(termination) is QeProcessTimeout
        return CalculatorTimeout(
            timeout_seconds=termination.timeout_milliseconds / 1000.0,
            termination_sent=termination.termination_sent,
            kill_sent=termination.kill_sent,
        )

    def _destination(
        self,
        prepared_execution: LocalQePreparedExecution,
        role: LocalQeResolvedDestinationRole,
    ) -> LocalQeResolvedDestination:
        values: tuple[LocalQeResolvedDestination, ...] = tuple(
            value
            for value in prepared_execution.resolved_destinations
            if value.role is role
        )
        if len(values) != 1:
            raise ValueError("prepared execution destination role is not unique")
        return values[0]

    def _failure(
        self,
        code: QePwEvidenceFailureCode,
        prepared_execution: LocalQePreparedExecution,
        captured_process: LocalQeCapturedProcess,
        observed_condition: str,
    ) -> QePwObservationFailure:
        return QePwObservationFailure(
            code=code,
            adapter_identity=self.identity,
            prepared_execution=prepared_execution,
            captured_process=captured_process,
            observed_condition=observed_condition,
        )


@dataclass(frozen=True, slots=True)
class QePwEvidencePublisherIdentity:
    """Nominal identity of one execution-record publication implementation."""

    value: str

    def __post_init__(self) -> None:
        """Validate the non-empty implementation identity."""
        if not isinstance(self.value, str):
            raise TypeError("value must be str")
        if self.value == "":
            raise ValueError("value must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QePwPublicationFailure:
    """Retain one failed or uncertain provider-record publication."""

    code: QePwEvidenceFailureCode
    publisher_identity: QePwEvidencePublisherIdentity
    observation_binding: QePwObservation
    publication_observed: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QePwEvidenceFailureCode:
            raise TypeError("code must be QePwEvidenceFailureCode")
        if type(self.publisher_identity) is not QePwEvidencePublisherIdentity:
            raise TypeError("publisher_identity must be QePwEvidencePublisherIdentity")
        if type(self.observation_binding) is not QePwObservation:
            raise TypeError("observation_binding must be QePwObservation")
        if type(self.publication_observed) is not bool:
            raise TypeError("publication_observed must be a built-in bool")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QePwPublishedEvidence:
    """Retain exact provider observation and verified record publication evidence."""

    publisher_identity: QePwEvidencePublisherIdentity
    observation_binding: QePwObservation
    destination: LocalQeExecutionRecordDestination
    content_identity: ArtifactContentIdentity
    publication_snapshot: QeWorkspaceSnapshot
    publication_entry: QeWorkspaceSnapshotEntry

    def __post_init__(self) -> None:
        if type(self.publisher_identity) is not QePwEvidencePublisherIdentity:
            raise TypeError("publisher_identity must be QePwEvidencePublisherIdentity")
        if type(self.observation_binding) is not QePwObservation:
            raise TypeError("observation_binding must be QePwObservation")
        if type(self.destination) is not LocalQeExecutionRecordDestination:
            raise TypeError("destination must be LocalQeExecutionRecordDestination")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")
        if type(self.publication_snapshot) is not QeWorkspaceSnapshot:
            raise TypeError("publication_snapshot must be QeWorkspaceSnapshot")
        if type(self.publication_entry) is not QeWorkspaceSnapshotEntry:
            raise TypeError("publication_entry must be QeWorkspaceSnapshotEntry")
        prepared = self.observation_binding.prepared_execution
        provider_artifact = (
            self.observation_binding.provider_observation.record_artifact
        )
        if self.destination is not prepared.execution_record_destination:
            raise ValueError("destination must be the prepared destination instance")
        if (
            self.content_identity.algorithm != "sha256"
            or self.content_identity.digest != provider_artifact.content_identity.sha256
            or self.content_identity.byte_count
            != provider_artifact.content_identity.byte_size
        ):
            raise ValueError("content_identity must equal the provider record artifact")
        if (
            self.publication_snapshot.preparation_identity != prepared.identity
            or self.publication_entry not in self.publication_snapshot.entries
            or self.publication_entry.entry_type
            is not QeWorkspaceEntryType.REGULAR_FILE
            or self.publication_entry.relative_path
            != self.destination.portable_destination
            or self.publication_entry.content_identity != self.content_identity
        ):
            raise ValueError(
                "publication snapshot entry must exactly represent the provider record"
            )

    @property
    def prepared_execution(self) -> LocalQePreparedExecution:
        """Return the exact prepared execution retained by the observation binding."""
        return self.observation_binding.prepared_execution

    @property
    def captured_process(self) -> LocalQeCapturedProcess:
        """Return the exact captured process retained by the observation binding."""
        return self.observation_binding.captured_process

    @property
    def provider_observation(self) -> CalculatorExecutionObservation:
        """Return the exact provider observation retained before publication."""
        return self.observation_binding.provider_observation


type QePwPublicationResult = QePwPublishedEvidence | QePwPublicationFailure


@dataclass(frozen=True, slots=True)
class QePwEvidencePublisher:
    """Publish and independently verify canonical provider execution-record bytes."""

    identity: QePwEvidencePublisherIdentity
    snapshotter: QeWorkspaceSnapshotter

    def __post_init__(self) -> None:
        if type(self.identity) is not QePwEvidencePublisherIdentity:
            raise TypeError("identity must be QePwEvidencePublisherIdentity")
        if type(self.snapshotter) is not QeWorkspaceSnapshotter:
            raise TypeError("snapshotter must be QeWorkspaceSnapshotter")

    def execute(self, observation_binding: QePwObservation) -> QePwPublicationResult:
        """Publish provider bytes and close exact no-replace manifest evidence."""
        if type(observation_binding) is not QePwObservation:
            raise TypeError("observation_binding must be QePwObservation")
        prepared = observation_binding.prepared_execution
        provider_artifact = observation_binding.provider_observation.record_artifact
        destination = prepared.execution_record_destination
        content_identity = ArtifactContentIdentity(
            "sha256",
            provider_artifact.content_identity.sha256,
            provider_artifact.content_identity.byte_size,
        )
        observed_identity = ArtifactContentIdentity(
            "sha256",
            hashlib.sha256(provider_artifact.content).hexdigest(),
            len(provider_artifact.content),
        )
        if observed_identity != content_identity:
            return self._failure(
                QePwEvidenceFailureCode.CONTENT_IDENTITY_MISMATCH,
                observation_binding,
                False,
                "provider execution-record bytes differ from their identity",
            )
        portable = PurePosixPath(destination.portable_destination.value)
        target = destination.absolute_path
        if (
            not portable.parts
            or portable.parts[0] != "records"
            or portable.name != provider_artifact.filename
            or target.name != provider_artifact.filename
            or target.parent.is_symlink()
            or not target.parent.is_dir()
        ):
            return self._failure(
                QePwEvidenceFailureCode.INVALID_DESTINATION,
                observation_binding,
                False,
                "execution-record destination must match the provider filename "
                "beneath an existing nonsymlink records directory",
            )
        try:
            if (
                prepared.workspace.resolve(strict=True) != prepared.workspace
                or target.parent.resolve(strict=True) != target.parent
                or not target.parent.is_relative_to(prepared.workspace)
            ):
                return self._failure(
                    QePwEvidenceFailureCode.INVALID_DESTINATION,
                    observation_binding,
                    False,
                    "execution-record destination is not confined to the workspace",
                )
        except OSError:
            return self._failure(
                QePwEvidenceFailureCode.INVALID_DESTINATION,
                observation_binding,
                False,
                "execution-record destination confinement could not be established",
            )
        if target.exists() or target.is_symlink():
            return self._failure(
                QePwEvidenceFailureCode.DESTINATION_EXISTS,
                observation_binding,
                True,
                "execution-record destination already exists and was not replaced",
            )
        current = self.snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.AFTER)
        if type(current) is QeWorkspaceSnapshotFailure:
            return self._failure(
                QePwEvidenceFailureCode.PUBLICATION_FAILED,
                observation_binding,
                False,
                "workspace usage could not be closed before record publication",
            )
        if type(current) is not QeWorkspaceSnapshot:
            raise TypeError("workspace snapshotter returned an unsupported result")
        limits = prepared.request.limits
        if (
            current.entry_count + 2 > limits.maximum_created_entry_count
            or current.regular_file_total_bytes + 2 * len(provider_artifact.content)
            > limits.maximum_created_total_bytes
        ):
            return self._failure(
                QePwEvidenceFailureCode.LIMIT_EXCEEDED,
                observation_binding,
                False,
                "execution-record publication would exceed a workspace ceiling",
            )
        temporary = target.parent / (
            "."
            + target.name
            + "."
            + hashlib.sha256(
                (
                    self.identity.value
                    + observation_binding.adapter_identity.value
                    + prepared.identity.value
                ).encode("utf-8")
            ).hexdigest()
            + ".tmp"
        )
        published = False
        try:
            descriptor = os.open(
                temporary,
                os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
                0o600,
            )
            try:
                view = memoryview(provider_artifact.content)
                while view:
                    written = os.write(descriptor, view)
                    view = view[written:]
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
            self._link(temporary, target)
            published = True
            temporary.unlink()
            directory_descriptor = os.open(
                target.parent,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        except FileExistsError:
            if temporary.exists() and not temporary.is_symlink():
                temporary.unlink()
            return self._failure(
                QePwEvidenceFailureCode.DESTINATION_EXISTS,
                observation_binding,
                target.exists(),
                "execution-record or temporary destination already exists",
            )
        except OSError:
            if temporary.exists() and not temporary.is_symlink():
                temporary.unlink()
            return self._failure(
                QePwEvidenceFailureCode.DURABILITY_UNCERTAIN
                if published
                else QePwEvidenceFailureCode.PUBLICATION_FAILED,
                observation_binding,
                published or target.exists(),
                "execution-record publication or synchronization failed",
            )
        publication_snapshot = self.snapshotter.execute(
            prepared, QeWorkspaceSnapshotPhase.AFTER
        )
        if type(publication_snapshot) is QeWorkspaceSnapshotFailure:
            return self._failure(
                QePwEvidenceFailureCode.DURABILITY_UNCERTAIN,
                observation_binding,
                True,
                "published execution-record workspace evidence could not be closed",
            )
        if type(publication_snapshot) is not QeWorkspaceSnapshot:
            raise TypeError("workspace snapshotter returned an unsupported result")
        entries: tuple[QeWorkspaceSnapshotEntry, ...] = tuple(
            entry
            for entry in publication_snapshot.entries
            if entry.relative_path == destination.portable_destination
        )
        if len(entries) != 1:
            return self._failure(
                QePwEvidenceFailureCode.VERIFICATION_FAILED,
                observation_binding,
                True,
                "published execution-record entry is absent or duplicated",
            )
        entry = entries[0]
        if (
            entry.entry_type is not QeWorkspaceEntryType.REGULAR_FILE
            or entry.content_identity != content_identity
            or entry.byte_count != len(provider_artifact.content)
        ):
            return self._failure(
                QePwEvidenceFailureCode.VERIFICATION_FAILED,
                observation_binding,
                True,
                "published execution-record bytes differ from provider evidence",
            )
        try:
            descriptor = os.open(
                target,
                os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0),
            )
            try:
                metadata = os.fstat(descriptor)
                if not stat.S_ISREG(metadata.st_mode):
                    raise OSError("execution-record destination is not regular")
                retained = bytearray()
                while True:
                    chunk = os.read(descriptor, 1024 * 1024)
                    if not chunk:
                        break
                    retained.extend(chunk)
            finally:
                os.close(descriptor)
        except OSError:
            return self._failure(
                QePwEvidenceFailureCode.VERIFICATION_FAILED,
                observation_binding,
                True,
                "published execution-record bytes could not be independently read",
            )
        retained_identity = ArtifactContentIdentity(
            "sha256", hashlib.sha256(retained).hexdigest(), len(retained)
        )
        if retained_identity != content_identity:
            return self._failure(
                QePwEvidenceFailureCode.VERIFICATION_FAILED,
                observation_binding,
                True,
                "independent execution-record identity verification failed",
            )
        return QePwPublishedEvidence(
            publisher_identity=self.identity,
            observation_binding=observation_binding,
            destination=destination,
            content_identity=content_identity,
            publication_snapshot=publication_snapshot,
            publication_entry=entry,
        )

    def _link(self, source: Path, destination: Path) -> None:
        os.link(source, destination, follow_symlinks=False)

    def _failure(
        self,
        code: QePwEvidenceFailureCode,
        binding: QePwObservation,
        observed: bool,
        condition: str,
    ) -> QePwPublicationFailure:
        return QePwPublicationFailure(
            code=code,
            publisher_identity=self.identity,
            observation_binding=binding,
            publication_observed=observed,
            observed_condition=condition,
        )
