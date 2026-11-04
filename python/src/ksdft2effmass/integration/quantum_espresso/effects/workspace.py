"""Bounded immutable workspace observation and snapshot publication."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from pathlib import Path

from ksdft2effmass.serialization import StrWireEnum
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
)

from ..contracts import (
    QeArtifactDestination,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeExecutionInputIdentity,
    QePreparationIdentity,
    QeProgram,
)
from ..execution import (
    LocalQePreparedExecution,
    LocalQeResolvedDestinationRole,
)

_MAX_U64 = 18_446_744_073_709_551_615
_EMPTY_CONTENT_IDENTITY = ArtifactContentIdentity(
    "sha256", hashlib.sha256(b"").hexdigest(), 0
)


class QeWorkspaceEntryType(StrWireEnum):
    """Closed supported workspace entry types."""

    DIRECTORY = "directory"
    REGULAR_FILE = "regular_file"


class QeWorkspaceSnapshotPhase(StrWireEnum):
    """Distinguish pre-process and post-process workspace observations."""

    BEFORE = "before"
    AFTER = "after"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeWorkspaceSnapshotEntry:
    """Represent one deterministic nonsymlink workspace entry.

    Attributes
    ----------
    identity
        Deterministic identity derived from type, path, and content identity.
    entry_type
        Supported directory or regular-file kind.
    relative_path
        Canonical path relative to the prepared workspace.
    byte_count
        Regular-file byte count, or zero for a directory.
    content_identity
        Exact regular-file identity, or the fixed empty identity for a directory.
    symlink_observed
        Always false for a successful entry; symlinks fail snapshot closure.
    """

    identity: ArtifactManifestEntryIdentity
    entry_type: QeWorkspaceEntryType
    relative_path: QeArtifactDestination
    byte_count: int
    content_identity: ArtifactContentIdentity
    symlink_observed: bool

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactManifestEntryIdentity:
            raise TypeError("identity must be ArtifactManifestEntryIdentity")
        if type(self.entry_type) is not QeWorkspaceEntryType:
            raise TypeError("entry_type must be QeWorkspaceEntryType")
        if type(self.relative_path) is not QeArtifactDestination:
            raise TypeError("relative_path must be QeArtifactDestination")
        if type(self.byte_count) is not int:
            raise TypeError("byte_count must be a built-in int")
        if not 0 <= self.byte_count <= _MAX_U64:
            raise ValueError("byte_count must be in the unsigned 64-bit range")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")
        if self.content_identity.byte_count != self.byte_count:
            raise ValueError("content identity byte count must equal entry byte count")
        if type(self.symlink_observed) is not bool:
            raise TypeError("symlink_observed must be a built-in bool")
        if self.symlink_observed:
            raise ValueError("successful snapshot entries cannot be symlinks")
        if self.entry_type is QeWorkspaceEntryType.DIRECTORY and (
            self.byte_count != 0 or self.content_identity != _EMPTY_CONTENT_IDENTITY
        ):
            raise ValueError("directory entries use the exact empty-content identity")


@dataclass(frozen=True, slots=True, kw_only=True)
class QeWorkspaceSnapshot:
    """Represent one closed deterministic workspace manifest.

    Attributes
    ----------
    identity
        Manifest identity derived from the canonical entry identities.
    phase
        Whether the observation occurred before or after process entry.
    preparation_identity, execution_input_identity,
    executable_configuration_identity
        Exact preparation and executable lineage represented by the snapshot.
    program, executable_kind, program_version
        Exact program-role and executable namespace/version correlation.
    entries
        Entries sorted by portable relative path.
    entry_count
        Exact number of represented directory and regular-file entries.
    regular_file_total_bytes
        Sum of represented regular-file bytes.
    implementation_version
        Nonempty snapshot algorithm identity.
    """

    identity: ArtifactManifestIdentity
    phase: QeWorkspaceSnapshotPhase
    preparation_identity: QePreparationIdentity
    execution_input_identity: QeExecutionInputIdentity
    executable_configuration_identity: QeExecutableConfigurationIdentity
    program: QeProgram
    executable_kind: QeExecutableKind
    program_version: str
    entries: tuple[QeWorkspaceSnapshotEntry, ...]
    entry_count: int
    regular_file_total_bytes: int
    implementation_version: str

    def __post_init__(self) -> None:
        expected = (
            (self.identity, ArtifactManifestIdentity, "identity"),
            (self.phase, QeWorkspaceSnapshotPhase, "phase"),
            (
                self.preparation_identity,
                QePreparationIdentity,
                "preparation_identity",
            ),
            (
                self.execution_input_identity,
                QeExecutionInputIdentity,
                "execution_input_identity",
            ),
            (
                self.executable_configuration_identity,
                QeExecutableConfigurationIdentity,
                "executable_configuration_identity",
            ),
            (self.program, QeProgram, "program"),
            (
                self.executable_kind,
                QeExecutableKind,
                "executable_kind",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.program_version) is not str:
            raise TypeError("program_version must be a built-in str")
        if not self.program_version:
            raise ValueError("program_version must not be empty")
        if type(self.entries) is not tuple or any(
            type(value) is not QeWorkspaceSnapshotEntry for value in self.entries
        ):
            raise TypeError("entries must contain QeWorkspaceSnapshotEntry values")
        if self.entries != tuple(
            sorted(self.entries, key=lambda value: value.relative_path.value)
        ) or len({value.relative_path for value in self.entries}) != len(self.entries):
            raise ValueError("entries must be unique and sorted by portable path")
        if (
            type(self.entry_count) is not int
            or type(self.regular_file_total_bytes) is not int
        ):
            raise TypeError("snapshot counts must be built-in ints")
        if self.entry_count != len(self.entries):
            raise ValueError("entry_count must equal the number of entries")
        if self.regular_file_total_bytes != sum(
            value.byte_count for value in self.entries
        ):
            raise ValueError(
                "regular_file_total_bytes must equal represented file bytes"
            )
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")


class QeWorkspaceSnapshotFailureCode(StrWireEnum):
    """Closed workspace-snapshot failure codes."""

    WORKSPACE_UNAVAILABLE = "workspace_unavailable"
    SYMLINK_OR_TYPE = "symlink_or_type"
    ENTRY_LIMIT_EXCEEDED = "entry_limit_exceeded"
    BYTE_LIMIT_EXCEEDED = "byte_limit_exceeded"
    OBSERVATION_FAILED = "observation_failed"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeWorkspaceSnapshotFailure:
    """Represent failure to close one deterministic workspace observation.

    Attributes
    ----------
    code
        Closed failure code for this result.
    phase
        Closed before-process or after-process snapshot phase.
    preparation_identity
        Exact nominal identity retained for cross-record correlation.
    observed_condition
        Sanitized nonempty mechanical observation; no scientific interpretation.
    """

    code: QeWorkspaceSnapshotFailureCode
    phase: QeWorkspaceSnapshotPhase
    preparation_identity: QePreparationIdentity
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QeWorkspaceSnapshotFailureCode:
            raise TypeError("code must be QeWorkspaceSnapshotFailureCode")
        if type(self.phase) is not QeWorkspaceSnapshotPhase:
            raise TypeError("phase must be QeWorkspaceSnapshotPhase")
        if type(self.preparation_identity) is not QePreparationIdentity:
            raise TypeError("preparation_identity must be QePreparationIdentity")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


type QeWorkspaceSnapshotResult = QeWorkspaceSnapshot | QeWorkspaceSnapshotFailure


@dataclass(frozen=True, slots=True)
class QeWorkspaceSnapshotter:
    """Produce deterministic bounded manifests of one prepared workspace.

    Attributes
    ----------
    implementation_version
        Nonempty identity of the owning deterministic implementation.
    """

    implementation_version: str

    def __post_init__(self) -> None:
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")

    def execute(
        self,
        prepared: LocalQePreparedExecution,
        phase: QeWorkspaceSnapshotPhase,
    ) -> QeWorkspaceSnapshotResult:
        """Return a closed snapshot or typed observation failure."""
        if type(prepared) is not LocalQePreparedExecution:
            raise TypeError("prepared must be LocalQePreparedExecution")
        if type(phase) is not QeWorkspaceSnapshotPhase:
            raise TypeError("phase must be QeWorkspaceSnapshotPhase")
        workspace = prepared.workspace
        try:
            if (
                workspace.is_symlink()
                or not workspace.is_dir()
                or workspace.resolve(strict=True) != workspace
            ):
                return self._failure(
                    prepared,
                    phase,
                    QeWorkspaceSnapshotFailureCode.WORKSPACE_UNAVAILABLE,
                    "workspace is absent, noncanonical, or not a nonsymlink directory",
                )
            entries: list[QeWorkspaceSnapshotEntry] = []
            total_bytes = 0
            pending = [workspace]
            while pending:
                directory = pending.pop()
                for child in sorted(directory.iterdir(), key=lambda value: value.name):
                    relative = child.relative_to(workspace).as_posix()
                    if child.is_symlink():
                        return self._failure(
                            prepared,
                            phase,
                            QeWorkspaceSnapshotFailureCode.SYMLINK_OR_TYPE,
                            "workspace contains a symlink or unsupported entry",
                        )
                    metadata = child.stat(follow_symlinks=False)
                    if stat.S_ISDIR(metadata.st_mode):
                        entry_type = QeWorkspaceEntryType.DIRECTORY
                        content = _EMPTY_CONTENT_IDENTITY
                        pending.append(child)
                    elif stat.S_ISREG(metadata.st_mode):
                        entry_type = QeWorkspaceEntryType.REGULAR_FILE
                        remaining_bytes = (
                            prepared.request.limits.maximum_created_total_bytes
                            - total_bytes
                        )
                        if metadata.st_size > remaining_bytes:
                            return self._failure(
                                prepared,
                                phase,
                                QeWorkspaceSnapshotFailureCode.BYTE_LIMIT_EXCEEDED,
                                "workspace regular-file bytes exceed their declared "
                                "ceiling",
                            )
                        content = self._file_identity(child, remaining_bytes)
                        total_bytes += content.byte_count
                    else:
                        return self._failure(
                            prepared,
                            phase,
                            QeWorkspaceSnapshotFailureCode.SYMLINK_OR_TYPE,
                            "workspace contains a symlink or unsupported entry",
                        )
                    entry_identity = ArtifactManifestEntryIdentity(
                        "qe-workspace-entry-v1:"
                        + self._framed_digest(
                            (
                                entry_type.value,
                                relative,
                                content.algorithm,
                                content.digest,
                                str(content.byte_count),
                            )
                        )
                    )
                    entries.append(
                        QeWorkspaceSnapshotEntry(
                            identity=entry_identity,
                            entry_type=entry_type,
                            relative_path=QeArtifactDestination(relative),
                            byte_count=content.byte_count,
                            content_identity=content,
                            symlink_observed=False,
                        )
                    )
                    if (
                        len(entries)
                        > prepared.request.limits.maximum_created_entry_count
                    ):
                        return self._failure(
                            prepared,
                            phase,
                            QeWorkspaceSnapshotFailureCode.ENTRY_LIMIT_EXCEEDED,
                            "workspace entry count exceeds its declared ceiling",
                        )
                    if (
                        total_bytes
                        > prepared.request.limits.maximum_created_total_bytes
                    ):
                        return self._failure(
                            prepared,
                            phase,
                            QeWorkspaceSnapshotFailureCode.BYTE_LIMIT_EXCEEDED,
                            "workspace regular-file bytes exceed their declared "
                            "ceiling",
                        )
        except OSError:
            return self._failure(
                prepared,
                phase,
                QeWorkspaceSnapshotFailureCode.OBSERVATION_FAILED,
                "workspace observation did not complete determinately",
            )
        canonical = tuple(sorted(entries, key=lambda value: value.relative_path.value))
        identity = ArtifactManifestIdentity(
            "qe-workspace-manifest-v1:"
            + self._framed_digest(tuple(value.identity.value for value in canonical))
        )
        return QeWorkspaceSnapshot(
            identity=identity,
            phase=phase,
            preparation_identity=prepared.identity,
            execution_input_identity=prepared.request.execution_input.identity,
            executable_configuration_identity=prepared.request.executable_configuration.identity,
            program=prepared.request.executable_configuration.program,
            executable_kind=prepared.request.executable_configuration.executable_kind,
            program_version=prepared.request.executable_configuration.program_version,
            entries=canonical,
            entry_count=len(canonical),
            regular_file_total_bytes=total_bytes,
            implementation_version=self.implementation_version,
        )

    @staticmethod
    def _failure(
        prepared: LocalQePreparedExecution,
        phase: QeWorkspaceSnapshotPhase,
        code: QeWorkspaceSnapshotFailureCode,
        condition: str,
    ) -> QeWorkspaceSnapshotFailure:
        return QeWorkspaceSnapshotFailure(
            code=code,
            phase=phase,
            preparation_identity=prepared.identity,
            observed_condition=condition,
        )

    @staticmethod
    def _file_identity(path: Path, maximum_byte_count: int) -> ArtifactContentIdentity:
        digest = hashlib.sha256()
        byte_count = 0
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode) or before.st_size > maximum_byte_count:
                raise OSError("entry is not a bounded regular file")
            while True:
                block = os.read(descriptor, min(1024 * 1024, maximum_byte_count + 1))
                if not block:
                    break
                byte_count += len(block)
                if byte_count > maximum_byte_count:
                    raise OSError("entry exceeds the remaining byte ceiling")
                digest.update(block)
            after = os.fstat(descriptor)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ):
                raise OSError("entry changed during observation")
        finally:
            os.close(descriptor)
        return ArtifactContentIdentity("sha256", digest.hexdigest(), byte_count)

    @staticmethod
    def _framed_digest(values: tuple[str, ...]) -> str:
        digest = hashlib.sha256()
        for value in values:
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
        return digest.hexdigest()


@dataclass(frozen=True, slots=True)
class QeWorkspaceSnapshotSerializer:
    """Serialize private ``qe-workspace-snapshot-v1`` canonical JSON bytes.

    Parameters
    ----------
    wire_version
        Fixed private wire-version discriminator. This is not a public persistence or
        cross-language contract.
    """

    wire_version: str = "qe-workspace-snapshot-v1"

    def __post_init__(self) -> None:
        if type(self.wire_version) is not str:
            raise TypeError("wire_version must be a built-in str")
        if self.wire_version != "qe-workspace-snapshot-v1":
            raise ValueError("only qe-workspace-snapshot-v1 is supported")

    def execute(self, snapshot: QeWorkspaceSnapshot) -> bytes:
        """Return deterministic UTF-8 canonical JSON ending in one newline.

        Parameters
        ----------
        snapshot
            Exact immutable workspace observation to serialize.

        Returns
        -------
        bytes
            Canonical private JSON bytes sorted by field name.
        """
        if type(snapshot) is not QeWorkspaceSnapshot:
            raise TypeError("snapshot must be QeWorkspaceSnapshot")
        entries = [
            {
                "byte_count": entry.byte_count,
                "content_identity": self._content_identity(entry.content_identity),
                "entry_identity": entry.identity.value,
                "entry_type": entry.entry_type.value,
                "relative_path": entry.relative_path.value,
                "symlink_observed": entry.symlink_observed,
            }
            for entry in snapshot.entries
        ]
        values: dict[str, bool | int | str | list[dict[str, bool | int | str]]] = {
            "entry_count": snapshot.entry_count,
            "entries": entries,
            "executable_configuration_identity": (
                snapshot.executable_configuration_identity.value
            ),
            "execution_input_identity": snapshot.execution_input_identity.value,
            "implementation_version": snapshot.implementation_version,
            "phase": snapshot.phase.value,
            "preparation_identity": snapshot.preparation_identity.value,
            "program": snapshot.program.value,
            "program_version": snapshot.program_version,
            "regular_file_total_bytes": snapshot.regular_file_total_bytes,
            "snapshot_identity": snapshot.identity.value,
            "wire_version": self.wire_version,
        }
        return (
            json.dumps(
                values, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            )
            + "\n"
        ).encode("utf-8")

    @staticmethod
    def _content_identity(identity: ArtifactContentIdentity) -> str:
        return f"{identity.algorithm}:{identity.digest}:{identity.byte_count}"


class QeWorkspaceSnapshotPublicationFailureCode(StrWireEnum):
    """Closed workspace-snapshot publication failure codes."""

    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    DESTINATION_EXISTS = "destination_exists"
    INVALID_DESTINATION = "invalid_destination"
    LIMIT_EXCEEDED = "limit_exceeded"
    PUBLICATION_FAILED = "publication_failed"
    DURABILITY_UNCERTAIN = "durability_uncertain"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeWorkspaceSnapshotPublicationFailure:
    """Represent a failed or durability-uncertain snapshot publication.

    Attributes
    ----------
    code
        Closed publication failure reason.
    snapshot_identity
        Exact snapshot whose record was not determinately published.
    publication_observed
        Whether the final destination was observed despite failure.
    observed_condition
        Sanitized nonempty mechanical failure description.
    """

    code: QeWorkspaceSnapshotPublicationFailureCode
    snapshot_identity: ArtifactManifestIdentity
    publication_observed: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not (QeWorkspaceSnapshotPublicationFailureCode):
            raise TypeError("code must be QeWorkspaceSnapshotPublicationFailureCode")
        if type(self.snapshot_identity) is not ArtifactManifestIdentity:
            raise TypeError("snapshot_identity must be ArtifactManifestIdentity")
        if type(self.publication_observed) is not bool:
            raise TypeError("publication_observed must be a built-in bool")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QePublishedWorkspaceSnapshot:
    """Record one successful atomic no-replace snapshot publication.

    Attributes
    ----------
    snapshot_identity
        Exact published snapshot identity.
    content_identity
        SHA-256 and byte-count identity of the private serialized record.
    destination
        Absolute prepared destination created by the publication.
    """

    snapshot_identity: ArtifactManifestIdentity
    content_identity: ArtifactContentIdentity
    destination: Path

    def __post_init__(self) -> None:
        if type(self.snapshot_identity) is not ArtifactManifestIdentity:
            raise TypeError("snapshot_identity must be ArtifactManifestIdentity")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")
        if not isinstance(self.destination, Path):
            raise TypeError("destination must be pathlib.Path")
        if not self.destination.is_absolute():
            raise ValueError("destination must be absolute")


type QeWorkspaceSnapshotPublicationResult = (
    QePublishedWorkspaceSnapshot | QeWorkspaceSnapshotPublicationFailure
)


@dataclass(frozen=True, slots=True)
class QeWorkspaceSnapshotPublisher:
    """Atomically publish one private snapshot record without replacement.

    Parameters
    ----------
    implementation_version
        Nonempty identity of the same-directory hard-link publication algorithm.

    Notes
    -----
    Publication verifies serialized content identity, lineage, confinement, and
    transient two-entry/two-byte-count headroom under the declared ceilings. It never
    replaces an existing destination.
    """

    implementation_version: str

    def __post_init__(self) -> None:
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")

    def execute(
        self,
        prepared: LocalQePreparedExecution,
        snapshot: QeWorkspaceSnapshot,
        serialized_record: bytes,
        content_identity: ArtifactContentIdentity,
    ) -> QeWorkspaceSnapshotPublicationResult:
        """Publish exact snapshot bytes with an atomic no-replace hard link.

        Parameters
        ----------
        prepared
            Exact preparation owning the confined snapshot destination.
        snapshot
            Snapshot whose phase selects the before or after destination.
        serialized_record
            Canonical private record bytes.
        content_identity
            Expected exact identity of ``serialized_record``.

        Returns
        -------
        QeWorkspaceSnapshotPublicationResult
            Successful publication evidence or a typed fail-closed result.
        """
        if type(prepared) is not LocalQePreparedExecution:
            raise TypeError("prepared must be LocalQePreparedExecution")
        if type(snapshot) is not QeWorkspaceSnapshot:
            raise TypeError("snapshot must be QeWorkspaceSnapshot")
        if type(serialized_record) is not bytes:
            raise TypeError("serialized_record must be built-in bytes")
        if type(content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")
        observed = ArtifactContentIdentity(
            "sha256",
            hashlib.sha256(serialized_record).hexdigest(),
            len(serialized_record),
        )
        if observed != content_identity:
            return self._failure(
                QeWorkspaceSnapshotPublicationFailureCode.CONTENT_IDENTITY_MISMATCH,
                snapshot,
                False,
                "serialized snapshot bytes differ from their declared identity",
            )
        role = (
            LocalQeResolvedDestinationRole.BEFORE_SNAPSHOT
            if snapshot.phase is QeWorkspaceSnapshotPhase.BEFORE
            else LocalQeResolvedDestinationRole.AFTER_SNAPSHOT
        )
        destinations = tuple(
            value for value in prepared.resolved_destinations if value.role is role
        )
        if len(destinations) != 1:
            return self._failure(
                QeWorkspaceSnapshotPublicationFailureCode.INVALID_DESTINATION,
                snapshot,
                False,
                "prepared snapshot destination is not unique",
            )
        target = destinations[0].absolute_path
        if (
            snapshot.preparation_identity != prepared.identity
            or target.parent.is_symlink()
            or not target.parent.is_dir()
        ):
            return self._failure(
                QeWorkspaceSnapshotPublicationFailureCode.INVALID_DESTINATION,
                snapshot,
                False,
                "snapshot lineage or destination parent is invalid",
            )
        limits = prepared.request.limits
        if (
            snapshot.entry_count + 2 > limits.maximum_created_entry_count
            or snapshot.regular_file_total_bytes + 2 * len(serialized_record)
            > limits.maximum_created_total_bytes
        ):
            return self._failure(
                QeWorkspaceSnapshotPublicationFailureCode.LIMIT_EXCEEDED,
                snapshot,
                False,
                "snapshot publication would exceed a declared workspace ceiling",
            )
        try:
            if (
                prepared.workspace.resolve(strict=True) != prepared.workspace
                or target.parent.resolve(strict=True) != target.parent
                or not target.parent.is_relative_to(prepared.workspace)
            ):
                raise OSError("snapshot destination is not confined")
        except OSError:
            return self._failure(
                QeWorkspaceSnapshotPublicationFailureCode.INVALID_DESTINATION,
                snapshot,
                False,
                "snapshot destination is not confined to the canonical workspace",
            )
        if target.exists() or target.is_symlink():
            return self._failure(
                QeWorkspaceSnapshotPublicationFailureCode.DESTINATION_EXISTS,
                snapshot,
                True,
                "snapshot destination already exists and was not replaced",
            )
        temporary = target.parent / (
            "."
            + target.name
            + "."
            + hashlib.sha256(snapshot.identity.value.encode("utf-8")).hexdigest()
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
            os.link(temporary, target, follow_symlinks=False)
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
                QeWorkspaceSnapshotPublicationFailureCode.DESTINATION_EXISTS,
                snapshot,
                target.exists(),
                "snapshot or temporary no-replace destination already exists",
            )
        except OSError:
            if temporary.exists() and not temporary.is_symlink():
                temporary.unlink()
            code = (
                QeWorkspaceSnapshotPublicationFailureCode.DURABILITY_UNCERTAIN
                if published
                else (QeWorkspaceSnapshotPublicationFailureCode.PUBLICATION_FAILED)
            )
            return self._failure(
                code,
                snapshot,
                published or target.exists(),
                "snapshot publication or durability synchronization failed",
            )
        return QePublishedWorkspaceSnapshot(
            snapshot_identity=snapshot.identity,
            content_identity=content_identity,
            destination=target,
        )

    @staticmethod
    def _failure(
        code: QeWorkspaceSnapshotPublicationFailureCode,
        snapshot: QeWorkspaceSnapshot,
        observed: bool,
        condition: str,
    ) -> QeWorkspaceSnapshotPublicationFailure:
        return QeWorkspaceSnapshotPublicationFailure(
            code=code,
            snapshot_identity=snapshot.identity,
            publication_observed=observed,
            observed_condition=condition,
        )
