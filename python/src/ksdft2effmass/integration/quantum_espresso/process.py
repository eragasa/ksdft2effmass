"""Bounded local process entry and exact stream capture for QE integration.

The ActionObject in this module consumes an already prepared and staged attempt. It
runs one exact local process, captures stdout and stderr in distinct no-replace files,
and returns only a complete mechanical observation or a typed rejected/indeterminate
integration failure. It does not classify diagnostics, construct calculator outcomes,
retry, or grant Workflow authority.
"""

from __future__ import annotations

import hashlib
import os
import signal
import stat
import subprocess
import time
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
)

from .contracts import (
    QuantumEspressoDiagnosticChannel,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoNormalProcessExit,
    QuantumEspressoPredecessorNativeStateArtifact,
    QuantumEspressoPreparationIdentity,
    QuantumEspressoProcessObservation,
    QuantumEspressoProcessObservationIdentity,
    QuantumEspressoProcessSignalTermination,
    QuantumEspressoProcessTermination,
    QuantumEspressoProcessTimeout,
    QuantumEspressoPseudopotentialArtifact,
    QuantumEspressoStreamObservation,
    QuantumEspressoTreeArtifactContent,
)
from .effects import (
    QuantumEspressoStagedExecution,
    QuantumEspressoStagingResultIdentity,
    QuantumEspressoWorkspaceSnapshot,
    QuantumEspressoWorkspaceSnapshotFailure,
    QuantumEspressoWorkspaceSnapshotPhase,
    QuantumEspressoWorkspaceSnapshotPublicationFailure,
    QuantumEspressoWorkspaceSnapshotPublicationResult,
    QuantumEspressoWorkspaceSnapshotPublisher,
    QuantumEspressoWorkspaceSnapshotSerializer,
    QuantumEspressoWorkspaceSnapshotter,
)
from .execution import (
    LocalQuantumEspressoPeakResidentBytesUnlimited,
    LocalQuantumEspressoPreparedExecution,
    LocalQuantumEspressoResolvedDestination,
    LocalQuantumEspressoResolvedDestinationRole,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQuantumEspressoStreamArtifactBindings:
    """Bind distinct stream artifact identities to prepared stream destinations.

    Attributes
    ----------
    stdout_artifact_identity
        Exact nominal identity retained for cross-record correlation.
    stderr_artifact_identity
        Exact nominal identity retained for cross-record correlation.
    """

    stdout_artifact_identity: ArtifactIdentity
    stderr_artifact_identity: ArtifactIdentity

    def __post_init__(self) -> None:
        if type(self.stdout_artifact_identity) is not ArtifactIdentity:
            raise TypeError("stdout_artifact_identity must be ArtifactIdentity")
        if type(self.stderr_artifact_identity) is not ArtifactIdentity:
            raise TypeError("stderr_artifact_identity must be ArtifactIdentity")
        if self.stdout_artifact_identity == self.stderr_artifact_identity:
            raise ValueError("stdout and stderr artifact identities must be distinct")


class LocalQuantumEspressoProcessFailureDisposition(StrEnum):
    """Distinguish known pre-entry rejection from post-entry uncertainty."""

    REJECTED = "rejected"
    INDETERMINATE = "indeterminate"


class LocalQuantumEspressoProcessFailureCode(StrEnum):
    """Closed local process-runner integration failure codes."""

    STAGING_MISMATCH = "staging_mismatch"
    MEMORY_LIMIT_UNSUPPORTED = "memory_limit_unsupported"
    EXECUTABLE_CHANGED = "executable_changed"
    BEFORE_SNAPSHOT_FAILED = "before_snapshot_failed"
    STREAM_DESTINATION_EXISTS = "stream_destination_exists"
    INPUT_UNAVAILABLE = "input_unavailable"
    INPUT_IDENTITY_CHANGED = "input_identity_changed"
    SPAWN_FAILED = "spawn_failed"
    LIFECYCLE_UNRESOLVED = "lifecycle_unresolved"
    CAPTURE_FAILED = "capture_failed"
    AFTER_SNAPSHOT_FAILED = "after_snapshot_failed"
    OUTPUT_LIMIT_EXCEEDED = "output_limit_exceeded"


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQuantumEspressoProcessFailure:
    """Represent one rejected or indeterminate local process result.

    Attributes
    ----------
    code
        Closed failure code for this result.
    disposition
        Closed admission disposition for this result.
    preparation_identity
        Exact nominal identity retained for cross-record correlation.
    staging_identity
        Exact nominal identity retained for cross-record correlation.
    process_entered
        Whether the external process effect was entered.
    observed_condition
        Sanitized nonempty mechanical observation; no scientific interpretation.
    """

    code: LocalQuantumEspressoProcessFailureCode
    disposition: LocalQuantumEspressoProcessFailureDisposition
    preparation_identity: QuantumEspressoPreparationIdentity
    staging_identity: QuantumEspressoStagingResultIdentity
    process_entered: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not LocalQuantumEspressoProcessFailureCode:
            raise TypeError("code must be LocalQuantumEspressoProcessFailureCode")
        if type(self.disposition) is not LocalQuantumEspressoProcessFailureDisposition:
            raise TypeError(
                "disposition must be LocalQuantumEspressoProcessFailureDisposition"
            )
        if type(self.preparation_identity) is not QuantumEspressoPreparationIdentity:
            raise TypeError(
                "preparation_identity must be QuantumEspressoPreparationIdentity"
            )
        if type(self.staging_identity) is not QuantumEspressoStagingResultIdentity:
            raise TypeError(
                "staging_identity must be QuantumEspressoStagingResultIdentity"
            )
        if type(self.process_entered) is not bool:
            raise TypeError("process_entered must be a built-in bool")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")
        expected = (
            LocalQuantumEspressoProcessFailureDisposition.INDETERMINATE
            if self.process_entered
            else LocalQuantumEspressoProcessFailureDisposition.REJECTED
        )
        if self.disposition is not expected:
            raise ValueError("failure disposition must agree with process entry")


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQuantumEspressoCapturedProcess:
    """Return one complete mechanical process observation and exact stream bytes.

    Attributes
    ----------
    observation
        Exact ``observation`` value retained by this immutable contract.
    before_snapshot
        Closed deterministic workspace snapshot for the named process phase.
    after_snapshot
        Closed deterministic workspace snapshot for the named process phase.
    stdout_bytes
        Exact bounded bytes captured independently from standard output.
    stderr_bytes
        Exact bounded bytes captured independently from standard error.
    """

    observation: QuantumEspressoProcessObservation
    before_snapshot: QuantumEspressoWorkspaceSnapshot
    after_snapshot: QuantumEspressoWorkspaceSnapshot
    stdout_bytes: bytes
    stderr_bytes: bytes

    def __post_init__(self) -> None:
        if type(self.observation) is not QuantumEspressoProcessObservation:
            raise TypeError("observation must be QuantumEspressoProcessObservation")
        for snapshot, name in (
            (self.before_snapshot, "before_snapshot"),
            (self.after_snapshot, "after_snapshot"),
        ):
            if type(snapshot) is not QuantumEspressoWorkspaceSnapshot:
                raise TypeError(f"{name} must be QuantumEspressoWorkspaceSnapshot")
        if (
            self.before_snapshot.phase
            is not QuantumEspressoWorkspaceSnapshotPhase.BEFORE
        ):
            raise ValueError("before_snapshot must use the before phase")
        if self.after_snapshot.phase is not QuantumEspressoWorkspaceSnapshotPhase.AFTER:
            raise ValueError("after_snapshot must use the after phase")
        for stream_bytes, name in (
            (self.stdout_bytes, "stdout_bytes"),
            (self.stderr_bytes, "stderr_bytes"),
        ):
            if type(stream_bytes) is not bytes:
                raise TypeError(f"{name} must be built-in bytes")
        if self.observation.before_snapshot_identity != self.before_snapshot.identity:
            raise ValueError("before snapshot identity does not match observation")
        if self.observation.after_snapshot_identity != self.after_snapshot.identity:
            raise ValueError("after snapshot identity does not match observation")
        if self.observation.stdout.content_identity != self._identity(
            self.stdout_bytes
        ):
            raise ValueError("stdout bytes do not match observation")
        if self.observation.stderr.content_identity != self._identity(
            self.stderr_bytes
        ):
            raise ValueError("stderr bytes do not match observation")

    @staticmethod
    def _identity(content: bytes) -> ArtifactContentIdentity:
        return ArtifactContentIdentity(
            "sha256", hashlib.sha256(content).hexdigest(), len(content)
        )


type LocalQuantumEspressoProcessResult = (
    LocalQuantumEspressoCapturedProcess | LocalQuantumEspressoProcessFailure
)


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoProcessRunner:
    """Run one prepared deterministic local process with exact separate capture.

    Parameters
    ----------
    observer_version
        Nonempty identity of the process-observation algorithm.
    snapshotter
        Bounded workspace observer used before and after process entry.
    snapshot_serializer
        Serializer for private immutable snapshot-record bytes.
    snapshot_publisher
        Atomic no-replace publisher for the prepared snapshot destinations.

    Notes
    -----
    The runner requires non-writable immutable launch parents, retains and rehashes
    opened executable and stdin descriptors before entry, uses one pre-spawn monotonic
    deadline, monitors aggregate workspace usage while the process is live, and reads
    stream bytes only after a bounded after-snapshot. Snapshot or
    lifecycle uncertainty after entry remains indeterminate. It performs no diagnostic
    classification, retry, or scientific acceptance.
    """

    observer_version: str
    snapshotter: QuantumEspressoWorkspaceSnapshotter
    snapshot_serializer: QuantumEspressoWorkspaceSnapshotSerializer = field(
        default_factory=QuantumEspressoWorkspaceSnapshotSerializer
    )
    snapshot_publisher: QuantumEspressoWorkspaceSnapshotPublisher = field(
        default_factory=lambda: QuantumEspressoWorkspaceSnapshotPublisher(
            "qe-snapshot-publisher:1"
        )
    )

    def __post_init__(self) -> None:
        if type(self.observer_version) is not str:
            raise TypeError("observer_version must be a built-in str")
        if not self.observer_version:
            raise ValueError("observer_version must not be empty")
        if type(self.snapshotter) is not QuantumEspressoWorkspaceSnapshotter:
            raise TypeError("snapshotter must be QuantumEspressoWorkspaceSnapshotter")
        if type(self.snapshot_serializer) is not (
            QuantumEspressoWorkspaceSnapshotSerializer
        ):
            raise TypeError(
                "snapshot_serializer must be QuantumEspressoWorkspaceSnapshotSerializer"
            )
        if type(self.snapshot_publisher) is not (
            QuantumEspressoWorkspaceSnapshotPublisher
        ):
            raise TypeError(
                "snapshot_publisher must be QuantumEspressoWorkspaceSnapshotPublisher"
            )

    def execute(
        self,
        prepared: LocalQuantumEspressoPreparedExecution,
        staged: QuantumEspressoStagedExecution,
        streams: LocalQuantumEspressoStreamArtifactBindings,
    ) -> LocalQuantumEspressoProcessResult:
        """Enter at most one process and return a closed observation or failure."""
        if type(prepared) is not LocalQuantumEspressoPreparedExecution:
            raise TypeError("prepared must be LocalQuantumEspressoPreparedExecution")
        if type(staged) is not QuantumEspressoStagedExecution:
            raise TypeError("staged must be QuantumEspressoStagedExecution")
        if type(streams) is not LocalQuantumEspressoStreamArtifactBindings:
            raise TypeError(
                "streams must be LocalQuantumEspressoStreamArtifactBindings"
            )
        if (
            staged.preparation_identity != prepared.identity
            or staged.workspace != prepared.workspace
        ):
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.STAGING_MISMATCH,
                False,
                "staging identity or workspace does not match preparation",
            )
        executable_path = self._executable_destination(prepared).absolute_path
        try:
            executable_identity = self._file_content_identity(
                executable_path,
                prepared.request.executable_content_identity.byte_count,
            )
        except OSError:
            executable_identity = None
        if (
            executable_identity != prepared.request.executable_content_identity
            or prepared.argv[0] != str(executable_path)
            or not os.access(executable_path, os.X_OK)
        ):
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.EXECUTABLE_CHANGED,
                False,
                "executable identity or runnable state changed after preparation",
            )
        if type(prepared.request.limits.peak_resident_bytes) is not (
            LocalQuantumEspressoPeakResidentBytesUnlimited
        ):
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.MEMORY_LIMIT_UNSUPPORTED,
                False,
                "peak resident-memory enforcement is unavailable",
            )
        before = self.snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.BEFORE
        )
        if type(before) is QuantumEspressoWorkspaceSnapshotFailure:
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.BEFORE_SNAPSHOT_FAILED,
                False,
                "before-workspace snapshot could not be closed",
            )
        assert type(before) is QuantumEspressoWorkspaceSnapshot
        if not self._prepared_inputs_match(prepared, before):
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.INPUT_IDENTITY_CHANGED,
                False,
                "one or more staged input identities changed before process entry",
            )
        before_publication = self._publish_snapshot(prepared, before)
        if type(before_publication) is (
            QuantumEspressoWorkspaceSnapshotPublicationFailure
        ):
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.BEFORE_SNAPSHOT_FAILED,
                False,
                "before-workspace snapshot record could not be published",
            )
        executable_descriptor: int | None = None
        try:
            if (
                prepared.workspace.stat(follow_symlinks=False).st_mode & 0o222
                or executable_path.parent.stat(follow_symlinks=False).st_mode & 0o222
            ):
                raise OSError("staged executable path remains replaceable")
            executable_descriptor = os.open(
                executable_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            )
            executable_metadata = os.fstat(executable_descriptor)
            if not stat.S_ISREG(executable_metadata.st_mode) or not (
                executable_metadata.st_mode & 0o111
            ):
                raise OSError("staged executable descriptor is not executable")
            if (
                self._descriptor_content_identity(
                    executable_descriptor,
                    prepared.request.executable_content_identity.byte_count,
                )
                != prepared.request.executable_content_identity
            ):
                raise OSError("staged executable descriptor identity changed")
        except OSError:
            self._close_descriptors(executable_descriptor)
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.EXECUTABLE_CHANGED,
                False,
                "staged executable could not be opened as the exact launch object",
            )
        stdout_path = self._destination(
            prepared, LocalQuantumEspressoResolvedDestinationRole.STDOUT
        ).absolute_path
        stderr_path = self._destination(
            prepared, LocalQuantumEspressoResolvedDestinationRole.STDERR
        ).absolute_path
        input_path = self._input_destination(prepared).absolute_path
        if any(
            path.exists() or path.is_symlink() for path in (stdout_path, stderr_path)
        ):
            self._close_descriptors(executable_descriptor)
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.STREAM_DESTINATION_EXISTS,
                False,
                "one or more stream destinations already exist",
            )
        input_descriptor: int | None = None
        try:
            if input_path.parent.stat(follow_symlinks=False).st_mode & 0o222:
                raise OSError("staged native input path remains replaceable")
            input_descriptor = os.open(
                input_path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            )
            input_metadata = os.fstat(input_descriptor)
            if not stat.S_ISREG(input_metadata.st_mode):
                raise OSError("native input is not a regular file")
            native_input_content = prepared.request.execution_input.native_input.content
            if type(native_input_content) is not QuantumEspressoFileArtifactContent:
                raise OSError("native input content is not a file identity")
            if (
                self._descriptor_content_identity(
                    input_descriptor,
                    native_input_content.content_identity.byte_count,
                )
                != native_input_content.content_identity
            ):
                raise OSError("native input identity changed before process entry")
            os.lseek(input_descriptor, 0, os.SEEK_SET)
        except OSError:
            self._close_descriptors(executable_descriptor, input_descriptor)
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.INPUT_UNAVAILABLE,
                False,
                "staged native input could not be opened exactly",
            )
        stream_flags = (
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        )
        stdout_descriptor: int | None = None
        stderr_descriptor: int | None = None
        process: subprocess.Popen[bytes] | None = None
        start = time.monotonic_ns()
        try:
            stdout_descriptor = os.open(stdout_path, stream_flags, 0o600)
            stderr_descriptor = os.open(stderr_path, stream_flags, 0o600)
            environment = self._environment(
                prepared.request.executable_configuration.environment_additions
            )
            process = subprocess.Popen(
                prepared.argv,
                cwd=prepared.workspace,
                stdin=input_descriptor,
                stdout=stdout_descriptor,
                stderr=stderr_descriptor,
                env=environment,
                shell=False,
                close_fds=True,
                start_new_session=True,
            )
        except FileExistsError:
            self._close_descriptors(
                executable_descriptor,
                input_descriptor,
                stdout_descriptor,
                stderr_descriptor,
            )
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.STREAM_DESTINATION_EXISTS,
                False,
                "a no-replace stream destination already exists",
            )
        except OSError:
            self._close_descriptors(
                executable_descriptor,
                input_descriptor,
                stdout_descriptor,
                stderr_descriptor,
            )
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.SPAWN_FAILED,
                False,
                "local process creation failed before process entry",
            )
        self._close_descriptors(
            executable_descriptor,
            input_descriptor,
            stdout_descriptor,
            stderr_descriptor,
        )
        assert process is not None
        termination, output_limit_exceeded = self._wait(
            process,
            prepared.workspace,
            start + prepared.request.limits.wall_time_milliseconds * 1_000_000,
            prepared.request.limits.wall_time_milliseconds,
            prepared.request.limits.termination_grace_milliseconds,
            prepared.request.limits.maximum_created_entry_count,
            prepared.request.limits.maximum_created_total_bytes,
        )
        if termination is None:
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.LIFECYCLE_UNRESOLVED,
                True,
                "process lifecycle could not be closed after entry",
            )
        if output_limit_exceeded:
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.OUTPUT_LIMIT_EXCEEDED,
                True,
                "workspace output exceeded a declared operational ceiling",
            )
        duration = time.monotonic_ns() - start
        after = self.snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )
        if type(after) is QuantumEspressoWorkspaceSnapshotFailure:
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.AFTER_SNAPSHOT_FAILED,
                True,
                "after-workspace snapshot could not be closed",
            )
        assert type(after) is QuantumEspressoWorkspaceSnapshot
        after_publication = self._publish_snapshot(prepared, after)
        if type(after_publication) is (
            QuantumEspressoWorkspaceSnapshotPublicationFailure
        ):
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.AFTER_SNAPSHOT_FAILED,
                True,
                "after-workspace snapshot record could not be published",
            )
        stdout_content = self._snapshot_content_identity(
            after, prepared.workspace, stdout_path
        )
        stderr_content = self._snapshot_content_identity(
            after, prepared.workspace, stderr_path
        )
        if stdout_content is None or stderr_content is None:
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.CAPTURE_FAILED,
                True,
                "stream identities are absent from the after snapshot",
            )
        try:
            stdout_bytes = self._read_regular_file(stdout_path, stdout_content)
            stderr_bytes = self._read_regular_file(stderr_path, stderr_content)
        except OSError:
            return self._failure(
                prepared,
                staged,
                LocalQuantumEspressoProcessFailureCode.CAPTURE_FAILED,
                True,
                "one or more bounded stream captures could not be closed exactly",
            )
        argv_identity = self._content_identity(self._framed_bytes(prepared.argv))
        identity = QuantumEspressoProcessObservationIdentity(
            "qe-process-observation-v1:"
            + self._framed_digest(
                (
                    self.observer_version,
                    prepared.identity.value,
                    staged.identity.value,
                    argv_identity.digest,
                    self._termination_key(termination),
                    str(duration),
                    stdout_content.digest,
                    stderr_content.digest,
                    before.identity.value,
                    after.identity.value,
                )
            )
        )
        observation = QuantumEspressoProcessObservation(
            identity=identity,
            execution_input_identity=prepared.request.execution_input.identity,
            executable_configuration_identity=(
                prepared.request.executable_configuration.identity
            ),
            preparation_identity=prepared.identity,
            attempt_identity=prepared.request.execution_input.attempt_identity,
            argv_content_identity=argv_identity,
            termination=termination,
            wall_duration_nanoseconds=duration,
            stdout=QuantumEspressoStreamObservation(
                channel=QuantumEspressoDiagnosticChannel.STDOUT,
                artifact_identity=streams.stdout_artifact_identity,
                content_identity=stdout_content,
            ),
            stderr=QuantumEspressoStreamObservation(
                channel=QuantumEspressoDiagnosticChannel.STDERR,
                artifact_identity=streams.stderr_artifact_identity,
                content_identity=stderr_content,
            ),
            before_snapshot_identity=before.identity,
            after_snapshot_identity=after.identity,
            created_entry_count=after.entry_count,
            created_total_bytes=after.regular_file_total_bytes,
            peak_resident_bytes=None,
            observer_version=self.observer_version,
        )
        return LocalQuantumEspressoCapturedProcess(
            observation=observation,
            before_snapshot=before,
            after_snapshot=after,
            stdout_bytes=stdout_bytes,
            stderr_bytes=stderr_bytes,
        )

    def _publish_snapshot(
        self,
        prepared: LocalQuantumEspressoPreparedExecution,
        snapshot: QuantumEspressoWorkspaceSnapshot,
    ) -> QuantumEspressoWorkspaceSnapshotPublicationResult:
        serialized = self.snapshot_serializer.execute(snapshot)
        content_identity = self._content_identity(serialized)
        return self.snapshot_publisher.execute(
            prepared, snapshot, serialized, content_identity
        )

    @staticmethod
    def _failure(
        prepared: LocalQuantumEspressoPreparedExecution,
        staged: QuantumEspressoStagedExecution,
        code: LocalQuantumEspressoProcessFailureCode,
        entered: bool,
        condition: str,
    ) -> LocalQuantumEspressoProcessFailure:
        return LocalQuantumEspressoProcessFailure(
            code=code,
            disposition=(
                LocalQuantumEspressoProcessFailureDisposition.INDETERMINATE
                if entered
                else LocalQuantumEspressoProcessFailureDisposition.REJECTED
            ),
            preparation_identity=prepared.identity,
            staging_identity=staged.identity,
            process_entered=entered,
            observed_condition=condition,
        )

    @staticmethod
    def _destination(
        prepared: LocalQuantumEspressoPreparedExecution,
        role: LocalQuantumEspressoResolvedDestinationRole,
    ) -> LocalQuantumEspressoResolvedDestination:
        values = tuple(
            value for value in prepared.resolved_destinations if value.role is role
        )
        if len(values) != 1:
            raise RuntimeError("prepared role destination is not unique")
        return values[0]

    @staticmethod
    def _executable_destination(
        prepared: LocalQuantumEspressoPreparedExecution,
    ) -> LocalQuantumEspressoResolvedDestination:
        values = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQuantumEspressoResolvedDestinationRole.EXECUTABLE
        )
        if len(values) != 1:
            raise RuntimeError("prepared executable destination is not unique")
        return values[0]

    @staticmethod
    def _input_destination(
        prepared: LocalQuantumEspressoPreparedExecution,
    ) -> LocalQuantumEspressoResolvedDestination:
        identity = prepared.request.execution_input.native_input.identity.value
        values = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQuantumEspressoResolvedDestinationRole.INPUT_ARTIFACT
            and value.owner_identity == identity
        )
        if len(values) != 1:
            raise RuntimeError("prepared native-input destination is not unique")
        return values[0]

    @classmethod
    def _prepared_inputs_match(
        cls,
        prepared: LocalQuantumEspressoPreparedExecution,
        snapshot: QuantumEspressoWorkspaceSnapshot,
    ) -> bool:
        entries = {entry.relative_path.value: entry for entry in snapshot.entries}
        for source in prepared.request.artifact_sources:
            artifact = source.artifact
            destination = artifact.destination.value
            root_entry = entries.get(destination)
            if root_entry is None:
                return False
            if type(artifact) in (
                QuantumEspressoNativeInputArtifact,
                QuantumEspressoPseudopotentialArtifact,
            ):
                if type(artifact.content) is not QuantumEspressoFileArtifactContent:
                    return False
                if root_entry.content_identity != artifact.content.content_identity:
                    return False
                continue
            if type(artifact) is not QuantumEspressoPredecessorNativeStateArtifact:
                return False
            if type(artifact.content) is not QuantumEspressoTreeArtifactContent:
                return False
            prefix = destination + "/"
            manifest_entries: list[ArtifactManifestEntryIdentity] = []
            for path, entry in entries.items():
                if not path.startswith(prefix):
                    continue
                relative = path[len(prefix) :]
                if entry.entry_type.value == "directory":
                    digest = cls._framed_digest(("directory", relative))
                else:
                    digest = cls._framed_digest(
                        (
                            "regular_file",
                            relative,
                            entry.content_identity.algorithm,
                            entry.content_identity.digest,
                            str(entry.content_identity.byte_count),
                        )
                    )
                manifest_entries.append(
                    ArtifactManifestEntryIdentity("qe-tree-entry-v1:" + digest)
                )
            canonical = tuple(sorted(manifest_entries, key=lambda value: value.value))
            manifest = ArtifactManifestIdentity(
                "qe-tree-manifest-v1:"
                + cls._framed_digest(tuple(value.value for value in canonical))
            )
            if (
                canonical != artifact.content.manifest_entry_identities
                or manifest != artifact.content.manifest_identity
            ):
                return False
        return True

    @staticmethod
    def _environment(additions: tuple[tuple[str, str], ...]) -> dict[str, str]:
        inherited_keys = ("HOME", "LANG", "LC_ALL", "PATH", "TMPDIR")
        environment = {
            key: os.environ[key] for key in inherited_keys if key in os.environ
        }
        environment.update(additions)
        return environment

    @staticmethod
    def _close_descriptors(*descriptors: int | None) -> None:
        for descriptor in descriptors:
            if descriptor is not None:
                try:
                    os.close(descriptor)
                except OSError:
                    pass

    @classmethod
    def _wait(
        cls,
        process: subprocess.Popen[bytes],
        workspace: Path,
        deadline_nanoseconds: int,
        timeout_milliseconds: int,
        grace_milliseconds: int,
        maximum_entry_count: int,
        maximum_total_bytes: int,
    ) -> tuple[QuantumEspressoProcessTermination | None, bool]:
        try:
            while True:
                remaining_nanoseconds = deadline_nanoseconds - time.monotonic_ns()
                if remaining_nanoseconds <= 0:
                    if process.poll() is not None:
                        return (
                            QuantumEspressoProcessTimeout(
                                timeout_milliseconds=timeout_milliseconds,
                                termination_sent=False,
                                kill_sent=False,
                            ),
                            False,
                        )
                    termination_sent, kill_sent = cls._stop_process_group(
                        process, grace_milliseconds
                    )
                    if not termination_sent:
                        return None, False
                    return (
                        QuantumEspressoProcessTimeout(
                            timeout_milliseconds=timeout_milliseconds,
                            termination_sent=True,
                            kill_sent=kill_sent,
                        ),
                        False,
                    )
                return_code = process.poll()
                if return_code is not None:
                    return cls._termination_from_return_code(return_code), False
                usage_within_limits = cls._workspace_usage_within_limits(
                    workspace, maximum_entry_count, maximum_total_bytes
                )
                if usage_within_limits is not True:
                    termination = cls._terminate_process_group(
                        process, grace_milliseconds
                    )
                    return termination, usage_within_limits is False
                time.sleep(min(0.01, remaining_nanoseconds / 1_000_000_000))
        except OSError, subprocess.SubprocessError:
            try:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            except OSError, subprocess.SubprocessError:
                pass
            return None, False

    @staticmethod
    def _workspace_usage_within_limits(
        workspace: Path, maximum_entry_count: int, maximum_total_bytes: int
    ) -> bool | None:
        entry_count = 0
        total_bytes = 0
        pending = [workspace]
        try:
            while pending:
                directory = pending.pop()
                for child in directory.iterdir():
                    if child.is_symlink():
                        return None
                    metadata = child.stat(follow_symlinks=False)
                    entry_count += 1
                    if entry_count > maximum_entry_count:
                        return False
                    if stat.S_ISDIR(metadata.st_mode):
                        pending.append(child)
                    elif stat.S_ISREG(metadata.st_mode):
                        total_bytes += metadata.st_size
                        if total_bytes > maximum_total_bytes:
                            return False
                    else:
                        return None
        except OSError:
            return None
        return True

    @classmethod
    def _terminate_process_group(
        cls, process: subprocess.Popen[bytes], grace_milliseconds: int
    ) -> QuantumEspressoProcessTermination | None:
        termination_sent, _kill_sent = cls._stop_process_group(
            process, grace_milliseconds
        )
        if not termination_sent or process.returncode is None:
            return None
        return cls._termination_from_return_code(process.returncode)

    @staticmethod
    def _stop_process_group(
        process: subprocess.Popen[bytes], grace_milliseconds: int
    ) -> tuple[bool, bool]:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=grace_milliseconds / 1_000)
                return True, False
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
                return True, True
        except OSError, subprocess.SubprocessError:
            return False, False

    @staticmethod
    def _termination_from_return_code(
        return_code: int,
    ) -> QuantumEspressoProcessTermination:
        if return_code >= 0:
            return QuantumEspressoNormalProcessExit(return_code)
        return QuantumEspressoProcessSignalTermination(-return_code)

    @classmethod
    def _read_regular_file(cls, path: Path, expected: ArtifactContentIdentity) -> bytes:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            metadata = os.fstat(descriptor)
            if (
                not stat.S_ISREG(metadata.st_mode)
                or metadata.st_size != expected.byte_count
            ):
                raise OSError("capture size differs from the bounded snapshot")
            blocks: list[bytes] = []
            remaining = expected.byte_count
            while remaining:
                block = os.read(descriptor, min(1024 * 1024, remaining))
                if not block:
                    raise OSError("capture ended before its bounded snapshot size")
                blocks.append(block)
                remaining -= len(block)
            if os.read(descriptor, 1):
                raise OSError("capture exceeds its bounded snapshot size")
            content = b"".join(blocks)
            if cls._content_identity(content) != expected:
                raise OSError("capture identity differs from the bounded snapshot")
            return content
        finally:
            os.close(descriptor)

    @staticmethod
    def _snapshot_content_identity(
        snapshot: QuantumEspressoWorkspaceSnapshot,
        workspace: Path,
        absolute_path: Path,
    ) -> ArtifactContentIdentity | None:
        try:
            relative = absolute_path.relative_to(workspace).as_posix()
        except ValueError:
            return None
        matches = tuple(
            entry.content_identity
            for entry in snapshot.entries
            if entry.relative_path.value == relative
        )
        return matches[0] if len(matches) == 1 else None

    @staticmethod
    def _descriptor_content_identity(
        descriptor: int, maximum_byte_count: int
    ) -> ArtifactContentIdentity:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or before.st_size > maximum_byte_count:
            raise OSError("descriptor is not a bounded regular file")
        digest = hashlib.sha256()
        byte_count = 0
        while True:
            block = os.pread(
                descriptor,
                min(1024 * 1024, maximum_byte_count + 1 - byte_count),
                byte_count,
            )
            if not block:
                break
            byte_count += len(block)
            if byte_count > maximum_byte_count:
                raise OSError("descriptor exceeds its declared byte count")
            digest.update(block)
        after = os.fstat(descriptor)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            raise OSError("descriptor changed during identity observation")
        return ArtifactContentIdentity("sha256", digest.hexdigest(), byte_count)

    @classmethod
    def _file_content_identity(
        cls, path: Path, maximum_byte_count: int
    ) -> ArtifactContentIdentity:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            return cls._descriptor_content_identity(descriptor, maximum_byte_count)
        finally:
            os.close(descriptor)

    @staticmethod
    def _content_identity(content: bytes) -> ArtifactContentIdentity:
        return ArtifactContentIdentity(
            "sha256", hashlib.sha256(content).hexdigest(), len(content)
        )

    @staticmethod
    def _framed_bytes(values: tuple[str, ...]) -> bytes:
        output = bytearray()
        for value in values:
            encoded = value.encode("utf-8")
            output.extend(len(encoded).to_bytes(8, "big"))
            output.extend(encoded)
        return bytes(output)

    @classmethod
    def _framed_digest(cls, values: tuple[str, ...]) -> str:
        return hashlib.sha256(cls._framed_bytes(values)).hexdigest()

    @staticmethod
    def _termination_key(termination: QuantumEspressoProcessTermination) -> str:
        if type(termination) is QuantumEspressoNormalProcessExit:
            return f"exit:{termination.exit_code}"
        if type(termination) is QuantumEspressoProcessSignalTermination:
            return f"signal:{termination.signal_number}"
        assert type(termination) is QuantumEspressoProcessTimeout
        return (
            f"timeout:{termination.timeout_milliseconds}:"
            f"{termination.termination_sent}:{termination.kill_sent}"
        )
