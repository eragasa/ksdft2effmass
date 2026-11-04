"""Private terminal-record serialization and no-replace publication."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from ksdft2effmass.serialization import StrWireEnum
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    SimulationExecutionRequestIdentity,
)

from ..contracts import (
    QeDiagnosticReportIdentity,
    QeExecutionInputIdentity,
    QePreparationIdentity,
    QeProcessObservationIdentity,
    QeTerminalRecordIdentity,
)
from ..execution import (
    LocalQePreparedExecution,
    LocalQeResolvedDestinationRole,
)
from .workspace import (
    QeWorkspaceSnapshotFailure,
    QeWorkspaceSnapshotPhase,
    QeWorkspaceSnapshotter,
)


class QeTerminalStatus(StrWireEnum):
    """Closed calculator-level statuses admitted to a private terminal record."""

    COMPLETED = "completed"
    CALCULATOR_FAILED = "calculator_failed"
    PROCESS_FAILED = "process_failed"
    DIAGNOSTIC_UNRESOLVED = "diagnostic_unresolved"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeTerminalRecord:
    """Represent exact identities written to one private version-2 terminal record.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    status
        Closed terminal operation status.
    simulation_execution_request_identity
        Exact nominal identity retained for cross-record correlation.
    execution_input_identity
        Exact nominal identity retained for cross-record correlation.
    preparation_identity
        Exact nominal identity retained for cross-record correlation.
    process_observation_identity
        Exact nominal identity retained for cross-record correlation.
    stdout_artifact_identity
        Exact nominal identity retained for cross-record correlation.
    stdout_content_identity
        Exact nominal identity retained for cross-record correlation.
    stderr_artifact_identity
        Exact nominal identity retained for cross-record correlation.
    stderr_content_identity
        Exact nominal identity retained for cross-record correlation.
    before_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    after_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    execution_record_manifest_entry_identity
        Exact verified manifest entry for the provider-owned execution record.
    execution_record_content_identity
        Exact byte identity of the provider-owned execution record.
    execution_record_publication_snapshot_identity
        Exact post-publication workspace snapshot identity.
    diagnostic_report_identity
        Exact nominal identity retained for cross-record correlation.
    native_output_manifest_identity
        Exact nominal identity retained for cross-record correlation.
    """

    identity: QeTerminalRecordIdentity
    status: QeTerminalStatus
    simulation_execution_request_identity: SimulationExecutionRequestIdentity
    execution_input_identity: QeExecutionInputIdentity
    preparation_identity: QePreparationIdentity
    process_observation_identity: QeProcessObservationIdentity
    stdout_artifact_identity: ArtifactIdentity
    stdout_content_identity: ArtifactContentIdentity
    stderr_artifact_identity: ArtifactIdentity
    stderr_content_identity: ArtifactContentIdentity
    before_snapshot_identity: ArtifactManifestIdentity
    after_snapshot_identity: ArtifactManifestIdentity
    execution_record_manifest_entry_identity: ArtifactManifestEntryIdentity
    execution_record_content_identity: ArtifactContentIdentity
    execution_record_publication_snapshot_identity: ArtifactManifestIdentity
    diagnostic_report_identity: QeDiagnosticReportIdentity
    native_output_manifest_identity: ArtifactManifestIdentity

    def __post_init__(self) -> None:
        expected = (
            (self.identity, QeTerminalRecordIdentity, "identity"),
            (self.status, QeTerminalStatus, "status"),
            (
                self.simulation_execution_request_identity,
                SimulationExecutionRequestIdentity,
                "simulation_execution_request_identity",
            ),
            (
                self.execution_input_identity,
                QeExecutionInputIdentity,
                "execution_input_identity",
            ),
            (
                self.preparation_identity,
                QePreparationIdentity,
                "preparation_identity",
            ),
            (
                self.process_observation_identity,
                QeProcessObservationIdentity,
                "process_observation_identity",
            ),
            (
                self.stdout_artifact_identity,
                ArtifactIdentity,
                "stdout_artifact_identity",
            ),
            (
                self.stdout_content_identity,
                ArtifactContentIdentity,
                "stdout_content_identity",
            ),
            (
                self.stderr_artifact_identity,
                ArtifactIdentity,
                "stderr_artifact_identity",
            ),
            (
                self.stderr_content_identity,
                ArtifactContentIdentity,
                "stderr_content_identity",
            ),
            (
                self.before_snapshot_identity,
                ArtifactManifestIdentity,
                "before_snapshot_identity",
            ),
            (
                self.after_snapshot_identity,
                ArtifactManifestIdentity,
                "after_snapshot_identity",
            ),
            (
                self.execution_record_manifest_entry_identity,
                ArtifactManifestEntryIdentity,
                "execution_record_manifest_entry_identity",
            ),
            (
                self.execution_record_content_identity,
                ArtifactContentIdentity,
                "execution_record_content_identity",
            ),
            (
                self.execution_record_publication_snapshot_identity,
                ArtifactManifestIdentity,
                "execution_record_publication_snapshot_identity",
            ),
            (
                self.diagnostic_report_identity,
                QeDiagnosticReportIdentity,
                "diagnostic_report_identity",
            ),
            (
                self.native_output_manifest_identity,
                ArtifactManifestIdentity,
                "native_output_manifest_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")


@dataclass(frozen=True, slots=True, kw_only=True)
class QeTerminalRecordArtifact:
    """Retain one exact serialized private terminal record.

    Parameters
    ----------
    serializer_wire_version
        Exact private terminal-wire version.
    record
        Exact immutable terminal record represented by the bytes.
    content, content_identity
        Canonical bytes and their exact SHA-256/byte-count identity.
    """

    serializer_wire_version: str
    record: QeTerminalRecord
    content: bytes
    content_identity: ArtifactContentIdentity

    def __post_init__(self) -> None:
        if type(self.serializer_wire_version) is not str:
            raise TypeError("serializer_wire_version must be a built-in str")
        if self.serializer_wire_version != "qe-local-terminal-record-v2":
            raise ValueError("serializer_wire_version must identify terminal record v2")
        if type(self.record) is not QeTerminalRecord:
            raise TypeError("record must be QeTerminalRecord")
        if type(self.content) is not bytes:
            raise TypeError("content must be built-in bytes")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")
        observed = ArtifactContentIdentity(
            "sha256", hashlib.sha256(self.content).hexdigest(), len(self.content)
        )
        if self.content_identity != observed:
            raise ValueError("content_identity must identify the exact terminal bytes")


@dataclass(frozen=True, slots=True)
class QeTerminalRecordSerializer:
    """Serialize private ``qe-local-terminal-record-v2`` canonical JSON bytes.

    Attributes
    ----------
    wire_version
        Fixed integration-private terminal-record wire discriminator.
    """

    wire_version: str = "qe-local-terminal-record-v2"

    def __post_init__(self) -> None:
        if type(self.wire_version) is not str:
            raise TypeError("wire_version must be a built-in str")
        if self.wire_version != "qe-local-terminal-record-v2":
            raise ValueError("only qe-local-terminal-record-v2 is supported")

    def execute(self, record: QeTerminalRecord) -> QeTerminalRecordArtifact:
        """Return one exact immutable terminal-record artifact."""
        if type(record) is not QeTerminalRecord:
            raise TypeError("record must be QeTerminalRecord")
        values: dict[str, str] = {
            "after_snapshot_identity": record.after_snapshot_identity.value,
            "before_snapshot_identity": record.before_snapshot_identity.value,
            "diagnostic_report_identity": record.diagnostic_report_identity.value,
            "execution_input_identity": record.execution_input_identity.value,
            "execution_record_content_identity": self._content_identity(
                record.execution_record_content_identity
            ),
            "execution_record_manifest_entry_identity": (
                record.execution_record_manifest_entry_identity.value
            ),
            "execution_record_publication_snapshot_identity": (
                record.execution_record_publication_snapshot_identity.value
            ),
            "native_output_manifest_identity": (
                record.native_output_manifest_identity.value
            ),
            "preparation_identity": record.preparation_identity.value,
            "process_observation_identity": record.process_observation_identity.value,
            "record_identity": record.identity.value,
            "simulation_execution_request_identity": (
                record.simulation_execution_request_identity.value
            ),
            "status": record.status.value,
            "stderr_artifact_identity": record.stderr_artifact_identity.value,
            "stderr_content_identity": self._content_identity(
                record.stderr_content_identity
            ),
            "stdout_artifact_identity": record.stdout_artifact_identity.value,
            "stdout_content_identity": self._content_identity(
                record.stdout_content_identity
            ),
            "wire_version": self.wire_version,
        }
        content = (
            json.dumps(
                values, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            )
            + "\n"
        ).encode("utf-8")
        return QeTerminalRecordArtifact(
            serializer_wire_version=self.wire_version,
            record=record,
            content=content,
            content_identity=ArtifactContentIdentity(
                "sha256", hashlib.sha256(content).hexdigest(), len(content)
            ),
        )

    @staticmethod
    def _content_identity(identity: ArtifactContentIdentity) -> str:
        return f"{identity.algorithm}:{identity.digest}:{identity.byte_count}"


class QeTerminalPublicationFailureCode(StrWireEnum):
    """Closed atomic terminal publication failure codes."""

    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    DESTINATION_EXISTS = "destination_exists"
    INVALID_DESTINATION = "invalid_destination"
    LIMIT_EXCEEDED = "limit_exceeded"
    PUBLICATION_FAILED = "publication_failed"
    DURABILITY_UNCERTAIN = "durability_uncertain"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeTerminalPublicationFailure:
    """Represent a failed or durability-uncertain terminal publication.

    Attributes
    ----------
    code
        Closed failure code for this result.
    terminal_record_identity
        Exact nominal identity retained for cross-record correlation.
    publication_observed
        Whether the final publication destination was observed after failure.
    observed_condition
        Sanitized nonempty mechanical observation; no scientific interpretation.
    """

    code: QeTerminalPublicationFailureCode
    terminal_record_identity: QeTerminalRecordIdentity
    publication_observed: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QeTerminalPublicationFailureCode:
            raise TypeError("code must be QeTerminalPublicationFailureCode")
        if type(self.terminal_record_identity) is not QeTerminalRecordIdentity:
            raise TypeError("terminal_record_identity must be QeTerminalRecordIdentity")
        if type(self.publication_observed) is not bool:
            raise TypeError("publication_observed must be a built-in bool")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QePublishedTerminalRecord:
    """Record one successful same-directory atomic no-replace publication.

    Attributes
    ----------
    record_artifact
        Exact immutable version-2 terminal record and canonical bytes.
    destination
        Exact destination path or parent-free workspace destination, as declared.
    """

    record_artifact: QeTerminalRecordArtifact
    destination: Path

    def __post_init__(self) -> None:
        if type(self.record_artifact) is not QeTerminalRecordArtifact:
            raise TypeError("record_artifact must be QeTerminalRecordArtifact")
        if not isinstance(self.destination, Path):
            raise TypeError("destination must be pathlib.Path")
        if not self.destination.is_absolute():
            raise ValueError("destination must be absolute")


type QeTerminalPublicationResult = (
    QePublishedTerminalRecord | QeTerminalPublicationFailure
)


@dataclass(frozen=True, slots=True)
class QeTerminalRecordPublisher:
    """Atomically publish one new private terminal record without replacement.

    Parameters
    ----------
    implementation_version
        Nonempty identity of the same-directory hard-link publication algorithm.
    snapshotter
        Bounded observer used to close current workspace usage before mutation.
    """

    implementation_version: str
    snapshotter: QeWorkspaceSnapshotter

    def __post_init__(self) -> None:
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")
        if type(self.snapshotter) is not QeWorkspaceSnapshotter:
            raise TypeError("snapshotter must be QeWorkspaceSnapshotter")

    def execute(
        self,
        prepared: LocalQePreparedExecution,
        record_artifact: QeTerminalRecordArtifact,
    ) -> QeTerminalPublicationResult:
        """Publish exact bytes with one same-directory atomic hard-link operation."""
        if type(prepared) is not LocalQePreparedExecution:
            raise TypeError("prepared must be LocalQePreparedExecution")
        if type(record_artifact) is not QeTerminalRecordArtifact:
            raise TypeError("record_artifact must be QeTerminalRecordArtifact")
        terminal_record_identity = record_artifact.record.identity
        serialized_record = record_artifact.content
        content_identity = record_artifact.content_identity
        observed = ArtifactContentIdentity(
            "sha256",
            hashlib.sha256(serialized_record).hexdigest(),
            len(serialized_record),
        )
        if observed != content_identity:
            return self._failure(
                QeTerminalPublicationFailureCode.CONTENT_IDENTITY_MISMATCH,
                terminal_record_identity,
                False,
                "serialized terminal bytes differ from their declared identity",
            )
        destinations = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQeResolvedDestinationRole.TERMINAL_RECORD
        )
        if len(destinations) != 1:
            return self._failure(
                QeTerminalPublicationFailureCode.INVALID_DESTINATION,
                terminal_record_identity,
                False,
                "prepared terminal destination is not unique",
            )
        resolved = destinations[0]
        portable = PurePosixPath(resolved.portable_destination.value)
        target = resolved.absolute_path
        if (
            not portable.parts
            or portable.parts[0] != "records"
            or target.parent.is_symlink()
            or not target.parent.is_dir()
        ):
            return self._failure(
                QeTerminalPublicationFailureCode.INVALID_DESTINATION,
                terminal_record_identity,
                False,
                "terminal destination must have an existing nonsymlink parent "
                "beneath records",
            )
        try:
            if (
                prepared.workspace.resolve(strict=True) != prepared.workspace
                or target.parent.resolve(strict=True) != target.parent
                or not target.parent.is_relative_to(prepared.workspace)
            ):
                return self._failure(
                    QeTerminalPublicationFailureCode.INVALID_DESTINATION,
                    terminal_record_identity,
                    False,
                    "terminal destination is not confined to the canonical workspace",
                )
        except OSError:
            return self._failure(
                QeTerminalPublicationFailureCode.INVALID_DESTINATION,
                terminal_record_identity,
                False,
                "terminal destination confinement could not be established",
            )
        if target.exists() or target.is_symlink():
            return self._failure(
                QeTerminalPublicationFailureCode.DESTINATION_EXISTS,
                terminal_record_identity,
                True,
                "terminal destination already exists and was not replaced",
            )
        current = self.snapshotter.execute(prepared, QeWorkspaceSnapshotPhase.AFTER)
        if isinstance(current, QeWorkspaceSnapshotFailure):
            return self._failure(
                QeTerminalPublicationFailureCode.PUBLICATION_FAILED,
                terminal_record_identity,
                False,
                "workspace usage could not be closed before terminal publication",
            )
        limits = prepared.request.limits
        if (
            current.entry_count + 2 > limits.maximum_created_entry_count
            or current.regular_file_total_bytes + 2 * len(serialized_record)
            > limits.maximum_created_total_bytes
        ):
            return self._failure(
                QeTerminalPublicationFailureCode.LIMIT_EXCEEDED,
                terminal_record_identity,
                False,
                "terminal publication would exceed a declared workspace ceiling",
            )
        temporary = target.parent / (
            "."
            + target.name
            + "."
            + hashlib.sha256(terminal_record_identity.value.encode("utf-8")).hexdigest()
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
                view = memoryview(serialized_record)
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
                target.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
            )
            try:
                os.fsync(directory_descriptor)
            finally:
                os.close(directory_descriptor)
        except FileExistsError:
            if temporary.exists() and not temporary.is_symlink():
                temporary.unlink()
            return self._failure(
                QeTerminalPublicationFailureCode.DESTINATION_EXISTS,
                terminal_record_identity,
                target.exists(),
                "terminal or temporary no-replace destination already exists",
            )
        except OSError:
            if temporary.exists() and not temporary.is_symlink():
                temporary.unlink()
            code = (
                QeTerminalPublicationFailureCode.DURABILITY_UNCERTAIN
                if published
                else QeTerminalPublicationFailureCode.PUBLICATION_FAILED
            )
            return self._failure(
                code,
                terminal_record_identity,
                published or target.exists(),
                "terminal publication or durability synchronization failed",
            )
        return QePublishedTerminalRecord(
            record_artifact=record_artifact,
            destination=target,
        )

    @staticmethod
    def _link(source: Path, destination: Path) -> None:
        os.link(source, destination, follow_symlinks=False)

    @staticmethod
    def _failure(
        code: QeTerminalPublicationFailureCode,
        identity: QeTerminalRecordIdentity,
        observed: bool,
        condition: str,
    ) -> QeTerminalPublicationFailure:
        return QeTerminalPublicationFailure(
            code=code,
            terminal_record_identity=identity,
            publication_observed=observed,
            observed_condition=condition,
        )
