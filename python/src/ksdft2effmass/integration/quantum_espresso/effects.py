"""Local Phase-4 effects for the Quantum ESPRESSO integration.

This module owns integration-local input staging, deterministic workspace snapshots,
native-output candidate collection, private terminal-record serialization, and atomic
no-replace publication.  None of these ActionObjects starts or observes a process,
constructs execution authority, retries an operation, or interprets scientific
validity.  Native files and stream bytes remain in the isolated attempt workspace.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath

from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    SimulationExecutionRequestIdentity,
)

from .contracts import (
    QuantumEspressoArtifactDestination,
    QuantumEspressoDiagnosticReportIdentity,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoExecutionInputIdentity,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoPredecessorNativeStateArtifact,
    QuantumEspressoPreparationIdentity,
    QuantumEspressoProcessObservationIdentity,
    QuantumEspressoProgram,
    QuantumEspressoPseudopotentialArtifact,
    QuantumEspressoTerminalRecordIdentity,
    QuantumEspressoTreeArtifactContent,
)
from .execution import (
    LocalQuantumEspressoFileSourceObservation,
    LocalQuantumEspressoPreparedExecution,
    LocalQuantumEspressoResolvedDestination,
    LocalQuantumEspressoResolvedDestinationRole,
    LocalQuantumEspressoTreeSourceObservation,
)

_MAX_U64 = 18_446_744_073_709_551_615
_EMPTY_CONTENT_IDENTITY = ArtifactContentIdentity(
    "sha256", hashlib.sha256(b"").hexdigest(), 0
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoStagingResultIdentity:
    """Identify one exact successful input-staging observation.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("staging result identity must be a built-in str")
        if not self.value:
            raise ValueError("staging result identity must not be empty")


class QuantumEspressoStagingFailureCode(StrEnum):
    """Closed failure codes for integration-owned input staging."""

    WORKSPACE_EXISTS = "workspace_exists"
    SOURCE_CHANGED = "source_changed"
    SYMLINK_OR_TYPE = "symlink_or_type"
    LIMIT_EXCEEDED = "limit_exceeded"
    DESTINATION_CONFLICT = "destination_conflict"
    IO_FAILED = "io_failed"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoStagingFailure:
    """Represent a fail-closed staging result.

    Attributes
    ----------
    code
        Stable staging failure code.
    preparation_identity
        Exact read-only preparation consumed by the staging attempt.
    related_identity
        Sanitized identity of the artifact or preparation associated with failure.
    workspace_created
        Whether the attempt workspace became observable before failure.
    observed_condition
        Nonempty sanitized failure description containing no native bytes.
    """

    code: QuantumEspressoStagingFailureCode
    preparation_identity: QuantumEspressoPreparationIdentity
    related_identity: str
    workspace_created: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QuantumEspressoStagingFailureCode:
            raise TypeError("code must be QuantumEspressoStagingFailureCode")
        if type(self.preparation_identity) is not QuantumEspressoPreparationIdentity:
            raise TypeError(
                "preparation_identity must be QuantumEspressoPreparationIdentity"
            )
        for value, name in (
            (self.related_identity, "related_identity"),
            (self.observed_condition, "observed_condition"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
        if type(self.workspace_created) is not bool:
            raise TypeError("workspace_created must be a built-in bool")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoStagedExecution:
    """Record exact successful staging into one new isolated workspace.

    Attributes
    ----------
    identity
        Deterministic staging-result identity.
    preparation_identity
        Exact preparation whose source and confinement facts were rechecked.
    workspace
        Newly created absolute attempt workspace.
    staged_artifact_identities
        Canonically ordered identities of all copied input artifacts.
    created_entry_count
        Number of directories and regular files created beneath the workspace.
    created_total_bytes
        Total regular-file bytes present immediately after staging.
    implementation_version
        Nonempty staging algorithm/version identifier.
    """

    identity: QuantumEspressoStagingResultIdentity
    preparation_identity: QuantumEspressoPreparationIdentity
    workspace: Path
    staged_artifact_identities: tuple[ArtifactIdentity, ...]
    created_entry_count: int
    created_total_bytes: int
    implementation_version: str

    def __post_init__(self) -> None:
        if type(self.identity) is not QuantumEspressoStagingResultIdentity:
            raise TypeError("identity must be QuantumEspressoStagingResultIdentity")
        if type(self.preparation_identity) is not QuantumEspressoPreparationIdentity:
            raise TypeError(
                "preparation_identity must be QuantumEspressoPreparationIdentity"
            )
        if not isinstance(self.workspace, Path):
            raise TypeError("workspace must be pathlib.Path")
        if not self.workspace.is_absolute():
            raise ValueError("workspace must be absolute")
        values = self.staged_artifact_identities
        if type(values) is not tuple or any(
            type(value) is not ArtifactIdentity for value in values
        ):
            raise TypeError(
                "staged_artifact_identities must contain ArtifactIdentity values"
            )
        if values != tuple(sorted(values, key=lambda value: value.value)) or len(
            set(values)
        ) != len(values):
            raise ValueError("staged_artifact_identities must be unique and sorted")
        for value, name in (
            (self.created_entry_count, "created_entry_count"),
            (self.created_total_bytes, "created_total_bytes"),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if not 0 <= value <= _MAX_U64:
                raise ValueError(f"{name} must be in the unsigned 64-bit range")
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")


type QuantumEspressoStagingResult = (
    QuantumEspressoStagedExecution | QuantumEspressoStagingFailure
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoInputStager:
    """Stage exact prepared inputs into a new root-confined workspace.

    Parameters
    ----------
    implementation_version
        Nonempty version identity for the staging and re-observation algorithm.

    Notes
    -----
    Staging rechecks all source identities before mutation and all destination
    identities after copying.  It never discovers or mutates a predecessor workspace,
    starts a process, or removes a partially observable failed workspace.
    """

    implementation_version: str

    def __post_init__(self) -> None:
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")

    def execute(
        self, prepared: LocalQuantumEspressoPreparedExecution
    ) -> QuantumEspressoStagingResult:
        """Create the absent workspace and copy every exact input artifact.

        Raises
        ------
        TypeError
            If ``prepared`` is not exactly a prepared execution.
        """
        if type(prepared) is not LocalQuantumEspressoPreparedExecution:
            raise TypeError("prepared must be LocalQuantumEspressoPreparedExecution")
        workspace = prepared.workspace
        if workspace.exists() or workspace.is_symlink():
            return self._failure(
                prepared,
                QuantumEspressoStagingFailureCode.WORKSPACE_EXISTS,
                prepared.identity.value,
                False,
                "attempt workspace is no longer absent",
            )
        if not self._roots_still_confined(prepared):
            return self._failure(
                prepared,
                QuantumEspressoStagingFailureCode.SYMLINK_OR_TYPE,
                prepared.identity.value,
                False,
                "prepared roots or source paths are no longer confined",
            )
        if not self._sources_still_match(prepared):
            return self._failure(
                prepared,
                QuantumEspressoStagingFailureCode.SOURCE_CHANGED,
                prepared.identity.value,
                False,
                "one or more prepared source identities changed",
            )
        projected = self._projected_usage(prepared)
        if projected is None:
            return self._failure(
                prepared,
                QuantumEspressoStagingFailureCode.SYMLINK_OR_TYPE,
                prepared.identity.value,
                False,
                "a source tree contains an unsupported entry",
            )
        entry_count, total_bytes = projected
        limits = prepared.request.limits
        if (
            entry_count > limits.maximum_created_entry_count
            or total_bytes > limits.maximum_created_total_bytes
        ):
            return self._failure(
                prepared,
                QuantumEspressoStagingFailureCode.LIMIT_EXCEEDED,
                prepared.identity.value,
                False,
                "staged inputs and explicit destination directories exceed a "
                "declared ceiling",
            )
        try:
            workspace.mkdir(mode=0o700, exist_ok=False)
            self._create_scaffold(prepared)
            executable_destination = self._executable_destination(prepared)
            self._copy_file(
                prepared.request.executable_path,
                executable_destination.absolute_path,
                destination_mode=0o500,
            )
            for source in prepared.request.artifact_sources:
                destination = self._input_destination(
                    prepared, source.artifact.identity
                )
                if type(source.artifact) in (
                    QuantumEspressoNativeInputArtifact,
                    QuantumEspressoPseudopotentialArtifact,
                ):
                    self._copy_file(
                        source.source,
                        destination.absolute_path,
                        destination_mode=0o600,
                    )
                else:
                    assert (
                        type(source.artifact)
                        is QuantumEspressoPredecessorNativeStateArtifact
                    )
                    self._copy_tree(source.source, destination.absolute_path)
            if not self._destinations_match(prepared):
                return self._failure(
                    prepared,
                    QuantumEspressoStagingFailureCode.SOURCE_CHANGED,
                    prepared.identity.value,
                    True,
                    "one or more staged destination identities differ from preparation",
                )
            self._lock_immutable_launch_paths(prepared)
        except FileExistsError:
            return self._failure(
                prepared,
                QuantumEspressoStagingFailureCode.DESTINATION_CONFLICT,
                prepared.identity.value,
                workspace.exists(),
                "a no-replace staging destination already exists",
            )
        except OSError:
            return self._failure(
                prepared,
                QuantumEspressoStagingFailureCode.IO_FAILED,
                prepared.identity.value,
                workspace.exists(),
                "filesystem staging did not complete determinately",
            )
        identity = QuantumEspressoStagingResultIdentity(
            "qe-input-staging-v1:"
            + self._framed_digest(
                (
                    self.implementation_version,
                    prepared.identity.value,
                    str(entry_count),
                    str(total_bytes),
                    *(
                        value.artifact.identity.value
                        for value in prepared.request.artifact_sources
                    ),
                )
            )
        )
        return QuantumEspressoStagedExecution(
            identity=identity,
            preparation_identity=prepared.identity,
            workspace=workspace,
            staged_artifact_identities=tuple(
                value.artifact.identity for value in prepared.request.artifact_sources
            ),
            created_entry_count=entry_count,
            created_total_bytes=total_bytes,
            implementation_version=self.implementation_version,
        )

    @staticmethod
    def _failure(
        prepared: LocalQuantumEspressoPreparedExecution,
        code: QuantumEspressoStagingFailureCode,
        related: str,
        created: bool,
        condition: str,
    ) -> QuantumEspressoStagingFailure:
        return QuantumEspressoStagingFailure(
            code=code,
            preparation_identity=prepared.identity,
            related_identity=related,
            workspace_created=created,
            observed_condition=condition,
        )

    @staticmethod
    def _executable_destination(
        prepared: LocalQuantumEspressoPreparedExecution,
    ) -> LocalQuantumEspressoResolvedDestination:
        matches = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQuantumEspressoResolvedDestinationRole.EXECUTABLE
        )
        if len(matches) != 1:
            raise OSError("prepared executable destination is not unique")
        return matches[0]

    @staticmethod
    def _input_destination(
        prepared: LocalQuantumEspressoPreparedExecution, identity: ArtifactIdentity
    ) -> LocalQuantumEspressoResolvedDestination:
        matches = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQuantumEspressoResolvedDestinationRole.INPUT_ARTIFACT
            and value.owner_identity == identity.value
        )
        if len(matches) != 1:
            raise OSError("prepared input destination is not unique")
        return matches[0]

    @staticmethod
    def _roots_still_confined(
        prepared: LocalQuantumEspressoPreparedExecution,
    ) -> bool:
        workspace_root = prepared.request.authorized_run_root
        try:
            if (
                workspace_root.is_symlink()
                or not workspace_root.is_dir()
                or workspace_root.resolve(strict=True) != workspace_root
            ):
                return False
            if (
                prepared.workspace.parent.is_symlink()
                or prepared.workspace.parent.resolve(strict=True)
                != prepared.workspace.parent
                or not prepared.workspace.is_relative_to(workspace_root)
            ):
                return False
            return not prepared.request.executable_path.is_symlink() and all(
                not source.source.is_symlink()
                for source in prepared.request.artifact_sources
            )
        except OSError:
            return False

    def _sources_still_match(
        self, prepared: LocalQuantumEspressoPreparedExecution
    ) -> bool:
        try:
            if (
                self._file_identity(prepared.request.executable_path)
                != prepared.executable_content_identity
            ):
                return False
        except OSError:
            return False
        observations = {
            value.artifact_identity: value for value in prepared.source_observations
        }
        for source in prepared.request.artifact_sources:
            observation = observations[source.artifact.identity]
            try:
                if type(observation) is LocalQuantumEspressoFileSourceObservation:
                    if (
                        self._file_identity(source.source)
                        != observation.content_identity
                    ):
                        return False
                else:
                    assert (
                        type(observation) is LocalQuantumEspressoTreeSourceObservation
                    )
                    entries, _ = self._tree_identities(source.source)
                    manifest = ArtifactManifestIdentity(
                        "qe-tree-manifest-v1:"
                        + self._framed_digest(tuple(value.value for value in entries))
                    )
                    if (
                        entries != observation.manifest_entry_identities
                        or manifest != observation.manifest_identity
                    ):
                        return False
            except OSError:
                return False
        return True

    def _destinations_match(
        self, prepared: LocalQuantumEspressoPreparedExecution
    ) -> bool:
        try:
            executable = self._executable_destination(prepared).absolute_path
            if self._file_identity(
                executable
            ) != prepared.executable_content_identity or not os.access(
                executable, os.X_OK
            ):
                return False
        except OSError:
            return False
        for source in prepared.request.artifact_sources:
            artifact = source.artifact
            destination = self._input_destination(
                prepared, artifact.identity
            ).absolute_path
            try:
                if type(artifact) in (
                    QuantumEspressoNativeInputArtifact,
                    QuantumEspressoPseudopotentialArtifact,
                ):
                    assert type(artifact.content) is QuantumEspressoFileArtifactContent
                    if (
                        self._file_identity(destination)
                        != artifact.content.content_identity
                    ):
                        return False
                else:
                    assert (
                        type(artifact) is QuantumEspressoPredecessorNativeStateArtifact
                    )
                    entries, _ = self._tree_identities(destination)
                    manifest = ArtifactManifestIdentity(
                        "qe-tree-manifest-v1:"
                        + self._framed_digest(tuple(value.value for value in entries))
                    )
                    if (
                        entries != artifact.content.manifest_entry_identities
                        or manifest != artifact.content.manifest_identity
                    ):
                        return False
            except OSError:
                return False
        return True

    @classmethod
    def _lock_immutable_launch_paths(
        cls, prepared: LocalQuantumEspressoPreparedExecution
    ) -> None:
        """Remove ordinary write access from immutable launch paths and parents."""
        immutable_paths = [cls._executable_destination(prepared).absolute_path]
        immutable_paths.extend(
            cls._input_destination(prepared, source.artifact.identity).absolute_path
            for source in prepared.request.artifact_sources
            if type(source.artifact)
            in (
                QuantumEspressoNativeInputArtifact,
                QuantumEspressoPseudopotentialArtifact,
            )
        )
        for path in immutable_paths:
            path.chmod(0o500 if path == immutable_paths[0] else 0o400)
        for parent in {path.parent for path in immutable_paths}:
            parent.chmod(0o500)
        prepared.workspace.chmod(0o500)

    def _projected_usage(
        self, prepared: LocalQuantumEspressoPreparedExecution
    ) -> tuple[int, int] | None:
        entries: set[str] = set()
        total_bytes = 0
        for destination in prepared.resolved_destinations:
            path = PurePosixPath(destination.portable_destination.value)
            for parent in path.parents:
                if parent.as_posix() != ".":
                    entries.add(parent.as_posix())
            if destination.role in (
                LocalQuantumEspressoResolvedDestinationRole.WORK,
                LocalQuantumEspressoResolvedDestinationRole.RESULT,
            ):
                entries.add(path.as_posix())
            elif (
                destination.role
                is LocalQuantumEspressoResolvedDestinationRole.EXECUTABLE
            ):
                entries.add(path.as_posix())
                total_bytes += prepared.executable_content_identity.byte_count
        for source in prepared.request.artifact_sources:
            base = PurePosixPath(source.artifact.destination.value)
            if type(source.artifact) in (
                QuantumEspressoNativeInputArtifact,
                QuantumEspressoPseudopotentialArtifact,
            ):
                entries.add(base.as_posix())
                assert (
                    type(source.artifact.content) is QuantumEspressoFileArtifactContent
                )
                total_bytes += source.artifact.content.content_identity.byte_count
            else:
                entries.add(base.as_posix())
                try:
                    descendants = self._tree_paths(source.source)
                except OSError:
                    return None
                for relative, is_file, byte_count in descendants:
                    entries.add((base / relative).as_posix())
                    if is_file:
                        total_bytes += byte_count
        if total_bytes > _MAX_U64:
            return None
        return len(entries), total_bytes

    @staticmethod
    def _tree_paths(root: Path) -> tuple[tuple[PurePosixPath, bool, int], ...]:
        if root.is_symlink():
            raise OSError("tree root symlink is unsupported")
        metadata = root.stat(follow_symlinks=False)
        if not stat.S_ISDIR(metadata.st_mode):
            raise OSError("tree root is not a directory")
        values: list[tuple[PurePosixPath, bool, int]] = []
        pending = [root]
        while pending:
            directory = pending.pop()
            for child in sorted(directory.iterdir(), key=lambda value: value.name):
                if child.is_symlink():
                    raise OSError("symlink is unsupported")
                metadata = child.stat(follow_symlinks=False)
                relative = PurePosixPath(child.relative_to(root).as_posix())
                if stat.S_ISDIR(metadata.st_mode):
                    values.append((relative, False, 0))
                    pending.append(child)
                elif stat.S_ISREG(metadata.st_mode):
                    values.append((relative, True, metadata.st_size))
                else:
                    raise OSError("unsupported source type")
        return tuple(values)

    @staticmethod
    def _create_scaffold(prepared: LocalQuantumEspressoPreparedExecution) -> None:
        directories: set[Path] = set()
        for destination in prepared.resolved_destinations:
            directories.update(
                parent
                for parent in destination.absolute_path.parents
                if parent != prepared.workspace
                and parent.is_relative_to(prepared.workspace)
            )
            if destination.role in (
                LocalQuantumEspressoResolvedDestinationRole.WORK,
                LocalQuantumEspressoResolvedDestinationRole.RESULT,
            ):
                directories.add(destination.absolute_path)
        for directory in sorted(
            directories, key=lambda value: (len(value.parts), str(value))
        ):
            directory.mkdir(mode=0o700, exist_ok=True)

    @classmethod
    def _copy_tree(cls, source: Path, destination: Path) -> None:
        destination.mkdir(mode=0o700, exist_ok=False)
        pending = [(source, destination)]
        while pending:
            source_directory, destination_directory = pending.pop()
            for child in sorted(
                source_directory.iterdir(), key=lambda value: value.name
            ):
                if child.is_symlink():
                    raise OSError("symlink is unsupported")
                metadata = child.stat(follow_symlinks=False)
                target = destination_directory / child.name
                if stat.S_ISDIR(metadata.st_mode):
                    target.mkdir(mode=0o700, exist_ok=False)
                    pending.append((child, target))
                elif stat.S_ISREG(metadata.st_mode):
                    cls._copy_file(child, target, destination_mode=0o600)
                else:
                    raise OSError("unsupported source type")

    @staticmethod
    def _copy_file(source: Path, destination: Path, *, destination_mode: int) -> None:
        source_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        destination_flags = (
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        )
        source_descriptor = os.open(source, source_flags)
        try:
            before = os.fstat(source_descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise OSError("source is not a regular file")
            destination_descriptor = os.open(
                destination, destination_flags, destination_mode
            )
            try:
                while True:
                    block = os.read(source_descriptor, 1024 * 1024)
                    if not block:
                        break
                    view = memoryview(block)
                    while view:
                        written = os.write(destination_descriptor, view)
                        view = view[written:]
                os.fsync(destination_descriptor)
            finally:
                os.close(destination_descriptor)
            after = os.fstat(source_descriptor)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ):
                raise OSError("source changed during copy")
        finally:
            os.close(source_descriptor)

    @classmethod
    def _tree_identities(
        cls, root: Path
    ) -> tuple[tuple[ArtifactManifestEntryIdentity, ...], int]:
        identities: list[ArtifactManifestEntryIdentity] = []
        total_bytes = 0
        for relative, is_file, byte_count in cls._tree_paths(root):
            if is_file:
                content = cls._file_identity(root.joinpath(*relative.parts))
                digest = cls._framed_digest(
                    (
                        "regular_file",
                        relative.as_posix(),
                        content.algorithm,
                        content.digest,
                        str(content.byte_count),
                    )
                )
                total_bytes += byte_count
            else:
                digest = cls._framed_digest(("directory", relative.as_posix()))
            identities.append(
                ArtifactManifestEntryIdentity("qe-tree-entry-v1:" + digest)
            )
        return tuple(sorted(identities, key=lambda value: value.value)), total_bytes

    @staticmethod
    def _file_identity(path: Path) -> ArtifactContentIdentity:
        digest = hashlib.sha256()
        byte_count = 0
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise OSError("path is not a regular file")
            while True:
                block = os.read(descriptor, 1024 * 1024)
                if not block:
                    break
                digest.update(block)
                byte_count += len(block)
            after = os.fstat(descriptor)
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ):
                raise OSError("file changed during observation")
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


class QuantumEspressoWorkspaceEntryType(StrEnum):
    """Closed supported workspace entry types."""

    DIRECTORY = "directory"
    REGULAR_FILE = "regular_file"


class QuantumEspressoWorkspaceSnapshotPhase(StrEnum):
    """Distinguish pre-process and post-process workspace observations."""

    BEFORE = "before"
    AFTER = "after"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoWorkspaceSnapshotEntry:
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
    entry_type: QuantumEspressoWorkspaceEntryType
    relative_path: QuantumEspressoArtifactDestination
    byte_count: int
    content_identity: ArtifactContentIdentity
    symlink_observed: bool

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactManifestEntryIdentity:
            raise TypeError("identity must be ArtifactManifestEntryIdentity")
        if type(self.entry_type) is not QuantumEspressoWorkspaceEntryType:
            raise TypeError("entry_type must be QuantumEspressoWorkspaceEntryType")
        if type(self.relative_path) is not QuantumEspressoArtifactDestination:
            raise TypeError("relative_path must be QuantumEspressoArtifactDestination")
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
        if self.entry_type is QuantumEspressoWorkspaceEntryType.DIRECTORY and (
            self.byte_count != 0 or self.content_identity != _EMPTY_CONTENT_IDENTITY
        ):
            raise ValueError("directory entries use the exact empty-content identity")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoWorkspaceSnapshot:
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
    phase: QuantumEspressoWorkspaceSnapshotPhase
    preparation_identity: QuantumEspressoPreparationIdentity
    execution_input_identity: QuantumEspressoExecutionInputIdentity
    executable_configuration_identity: QuantumEspressoExecutableConfigurationIdentity
    program: QuantumEspressoProgram
    executable_kind: QuantumEspressoExecutableKind
    program_version: str
    entries: tuple[QuantumEspressoWorkspaceSnapshotEntry, ...]
    entry_count: int
    regular_file_total_bytes: int
    implementation_version: str

    def __post_init__(self) -> None:
        expected = (
            (self.identity, ArtifactManifestIdentity, "identity"),
            (self.phase, QuantumEspressoWorkspaceSnapshotPhase, "phase"),
            (
                self.preparation_identity,
                QuantumEspressoPreparationIdentity,
                "preparation_identity",
            ),
            (
                self.execution_input_identity,
                QuantumEspressoExecutionInputIdentity,
                "execution_input_identity",
            ),
            (
                self.executable_configuration_identity,
                QuantumEspressoExecutableConfigurationIdentity,
                "executable_configuration_identity",
            ),
            (self.program, QuantumEspressoProgram, "program"),
            (
                self.executable_kind,
                QuantumEspressoExecutableKind,
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
            type(value) is not QuantumEspressoWorkspaceSnapshotEntry
            for value in self.entries
        ):
            raise TypeError(
                "entries must contain QuantumEspressoWorkspaceSnapshotEntry values"
            )
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


class QuantumEspressoWorkspaceSnapshotFailureCode(StrEnum):
    """Closed workspace-snapshot failure codes."""

    WORKSPACE_UNAVAILABLE = "workspace_unavailable"
    SYMLINK_OR_TYPE = "symlink_or_type"
    ENTRY_LIMIT_EXCEEDED = "entry_limit_exceeded"
    BYTE_LIMIT_EXCEEDED = "byte_limit_exceeded"
    OBSERVATION_FAILED = "observation_failed"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoWorkspaceSnapshotFailure:
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

    code: QuantumEspressoWorkspaceSnapshotFailureCode
    phase: QuantumEspressoWorkspaceSnapshotPhase
    preparation_identity: QuantumEspressoPreparationIdentity
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QuantumEspressoWorkspaceSnapshotFailureCode:
            raise TypeError("code must be QuantumEspressoWorkspaceSnapshotFailureCode")
        if type(self.phase) is not QuantumEspressoWorkspaceSnapshotPhase:
            raise TypeError("phase must be QuantumEspressoWorkspaceSnapshotPhase")
        if type(self.preparation_identity) is not QuantumEspressoPreparationIdentity:
            raise TypeError(
                "preparation_identity must be QuantumEspressoPreparationIdentity"
            )
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


type QuantumEspressoWorkspaceSnapshotResult = (
    QuantumEspressoWorkspaceSnapshot | QuantumEspressoWorkspaceSnapshotFailure
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoWorkspaceSnapshotter:
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
        prepared: LocalQuantumEspressoPreparedExecution,
        phase: QuantumEspressoWorkspaceSnapshotPhase,
    ) -> QuantumEspressoWorkspaceSnapshotResult:
        """Return a closed snapshot or typed observation failure."""
        if type(prepared) is not LocalQuantumEspressoPreparedExecution:
            raise TypeError("prepared must be LocalQuantumEspressoPreparedExecution")
        if type(phase) is not QuantumEspressoWorkspaceSnapshotPhase:
            raise TypeError("phase must be QuantumEspressoWorkspaceSnapshotPhase")
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
                    QuantumEspressoWorkspaceSnapshotFailureCode.WORKSPACE_UNAVAILABLE,
                    "workspace is absent, noncanonical, or not a nonsymlink directory",
                )
            entries: list[QuantumEspressoWorkspaceSnapshotEntry] = []
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
                            QuantumEspressoWorkspaceSnapshotFailureCode.SYMLINK_OR_TYPE,
                            "workspace contains a symlink or unsupported entry",
                        )
                    metadata = child.stat(follow_symlinks=False)
                    if stat.S_ISDIR(metadata.st_mode):
                        entry_type = QuantumEspressoWorkspaceEntryType.DIRECTORY
                        content = _EMPTY_CONTENT_IDENTITY
                        pending.append(child)
                    elif stat.S_ISREG(metadata.st_mode):
                        entry_type = QuantumEspressoWorkspaceEntryType.REGULAR_FILE
                        remaining_bytes = (
                            prepared.request.limits.maximum_created_total_bytes
                            - total_bytes
                        )
                        if metadata.st_size > remaining_bytes:
                            return self._failure(
                                prepared,
                                phase,
                                QuantumEspressoWorkspaceSnapshotFailureCode.BYTE_LIMIT_EXCEEDED,
                                "workspace regular-file bytes exceed their declared "
                                "ceiling",
                            )
                        content = self._file_identity(child, remaining_bytes)
                        total_bytes += content.byte_count
                    else:
                        return self._failure(
                            prepared,
                            phase,
                            QuantumEspressoWorkspaceSnapshotFailureCode.SYMLINK_OR_TYPE,
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
                        QuantumEspressoWorkspaceSnapshotEntry(
                            identity=entry_identity,
                            entry_type=entry_type,
                            relative_path=QuantumEspressoArtifactDestination(relative),
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
                            QuantumEspressoWorkspaceSnapshotFailureCode.ENTRY_LIMIT_EXCEEDED,
                            "workspace entry count exceeds its declared ceiling",
                        )
                    if (
                        total_bytes
                        > prepared.request.limits.maximum_created_total_bytes
                    ):
                        return self._failure(
                            prepared,
                            phase,
                            QuantumEspressoWorkspaceSnapshotFailureCode.BYTE_LIMIT_EXCEEDED,
                            "workspace regular-file bytes exceed their declared "
                            "ceiling",
                        )
        except OSError:
            return self._failure(
                prepared,
                phase,
                QuantumEspressoWorkspaceSnapshotFailureCode.OBSERVATION_FAILED,
                "workspace observation did not complete determinately",
            )
        canonical = tuple(sorted(entries, key=lambda value: value.relative_path.value))
        identity = ArtifactManifestIdentity(
            "qe-workspace-manifest-v1:"
            + self._framed_digest(tuple(value.identity.value for value in canonical))
        )
        return QuantumEspressoWorkspaceSnapshot(
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
        prepared: LocalQuantumEspressoPreparedExecution,
        phase: QuantumEspressoWorkspaceSnapshotPhase,
        code: QuantumEspressoWorkspaceSnapshotFailureCode,
        condition: str,
    ) -> QuantumEspressoWorkspaceSnapshotFailure:
        return QuantumEspressoWorkspaceSnapshotFailure(
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
class QuantumEspressoWorkspaceSnapshotSerializer:
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

    def execute(self, snapshot: QuantumEspressoWorkspaceSnapshot) -> bytes:
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
        if type(snapshot) is not QuantumEspressoWorkspaceSnapshot:
            raise TypeError("snapshot must be QuantumEspressoWorkspaceSnapshot")
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


class QuantumEspressoWorkspaceSnapshotPublicationFailureCode(StrEnum):
    """Closed workspace-snapshot publication failure codes."""

    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    DESTINATION_EXISTS = "destination_exists"
    INVALID_DESTINATION = "invalid_destination"
    LIMIT_EXCEEDED = "limit_exceeded"
    PUBLICATION_FAILED = "publication_failed"
    DURABILITY_UNCERTAIN = "durability_uncertain"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoWorkspaceSnapshotPublicationFailure:
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

    code: QuantumEspressoWorkspaceSnapshotPublicationFailureCode
    snapshot_identity: ArtifactManifestIdentity
    publication_observed: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not (
            QuantumEspressoWorkspaceSnapshotPublicationFailureCode
        ):
            raise TypeError(
                "code must be QuantumEspressoWorkspaceSnapshotPublicationFailureCode"
            )
        if type(self.snapshot_identity) is not ArtifactManifestIdentity:
            raise TypeError("snapshot_identity must be ArtifactManifestIdentity")
        if type(self.publication_observed) is not bool:
            raise TypeError("publication_observed must be a built-in bool")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoPublishedWorkspaceSnapshot:
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


type QuantumEspressoWorkspaceSnapshotPublicationResult = (
    QuantumEspressoPublishedWorkspaceSnapshot
    | QuantumEspressoWorkspaceSnapshotPublicationFailure
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoWorkspaceSnapshotPublisher:
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
        prepared: LocalQuantumEspressoPreparedExecution,
        snapshot: QuantumEspressoWorkspaceSnapshot,
        serialized_record: bytes,
        content_identity: ArtifactContentIdentity,
    ) -> QuantumEspressoWorkspaceSnapshotPublicationResult:
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
        QuantumEspressoWorkspaceSnapshotPublicationResult
            Successful publication evidence or a typed fail-closed result.
        """
        if type(prepared) is not LocalQuantumEspressoPreparedExecution:
            raise TypeError("prepared must be LocalQuantumEspressoPreparedExecution")
        if type(snapshot) is not QuantumEspressoWorkspaceSnapshot:
            raise TypeError("snapshot must be QuantumEspressoWorkspaceSnapshot")
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
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.CONTENT_IDENTITY_MISMATCH,
                snapshot,
                False,
                "serialized snapshot bytes differ from their declared identity",
            )
        role = (
            LocalQuantumEspressoResolvedDestinationRole.BEFORE_SNAPSHOT
            if snapshot.phase is QuantumEspressoWorkspaceSnapshotPhase.BEFORE
            else LocalQuantumEspressoResolvedDestinationRole.AFTER_SNAPSHOT
        )
        destinations = tuple(
            value for value in prepared.resolved_destinations if value.role is role
        )
        if len(destinations) != 1:
            return self._failure(
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.INVALID_DESTINATION,
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
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.INVALID_DESTINATION,
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
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.LIMIT_EXCEEDED,
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
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.INVALID_DESTINATION,
                snapshot,
                False,
                "snapshot destination is not confined to the canonical workspace",
            )
        if target.exists() or target.is_symlink():
            return self._failure(
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.DESTINATION_EXISTS,
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
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.DESTINATION_EXISTS,
                snapshot,
                target.exists(),
                "snapshot or temporary no-replace destination already exists",
            )
        except OSError:
            if temporary.exists() and not temporary.is_symlink():
                temporary.unlink()
            code = (
                QuantumEspressoWorkspaceSnapshotPublicationFailureCode.DURABILITY_UNCERTAIN
                if published
                else (
                    QuantumEspressoWorkspaceSnapshotPublicationFailureCode.PUBLICATION_FAILED
                )
            )
            return self._failure(
                code,
                snapshot,
                published or target.exists(),
                "snapshot publication or durability synchronization failed",
            )
        return QuantumEspressoPublishedWorkspaceSnapshot(
            snapshot_identity=snapshot.identity,
            content_identity=content_identity,
            destination=target,
        )

    @staticmethod
    def _failure(
        code: QuantumEspressoWorkspaceSnapshotPublicationFailureCode,
        snapshot: QuantumEspressoWorkspaceSnapshot,
        observed: bool,
        condition: str,
    ) -> QuantumEspressoWorkspaceSnapshotPublicationFailure:
        return QuantumEspressoWorkspaceSnapshotPublicationFailure(
            code=code,
            snapshot_identity=snapshot.identity,
            publication_observed=observed,
            observed_condition=condition,
        )


class QuantumEspressoNativeOutputRole(StrEnum):
    """Closed roles represented by the initial native-output candidate manifest."""

    STDOUT = "stdout"
    STDERR = "stderr"
    NATIVE_STATE = "native_state"
    NATIVE_RESULT = "native_result"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoNativeOutputCandidateSpecification:
    """Declare one exact workspace candidate for operation/version extraction.

    Attributes
    ----------
    artifact_identity
        Exact nominal identity retained for cross-record correlation.
    role
        Closed integration-owned artifact role.
    relative_path
        Parent-free portable POSIX path relative to the workspace.
    entry_type
        Closed supported regular-file or directory kind.
    required
        Whether absence of this candidate fails native-output collection.
    """

    artifact_identity: ArtifactIdentity
    role: QuantumEspressoNativeOutputRole
    relative_path: QuantumEspressoArtifactDestination
    entry_type: QuantumEspressoWorkspaceEntryType
    required: bool

    def __post_init__(self) -> None:
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if type(self.role) is not QuantumEspressoNativeOutputRole:
            raise TypeError("role must be QuantumEspressoNativeOutputRole")
        if type(self.relative_path) is not QuantumEspressoArtifactDestination:
            raise TypeError("relative_path must be QuantumEspressoArtifactDestination")
        if type(self.entry_type) is not QuantumEspressoWorkspaceEntryType:
            raise TypeError("entry_type must be QuantumEspressoWorkspaceEntryType")
        if type(self.required) is not bool:
            raise TypeError("required must be a built-in bool")
        if self.role in (
            QuantumEspressoNativeOutputRole.STDOUT,
            QuantumEspressoNativeOutputRole.STDERR,
        ) and (
            not self.required
            or self.entry_type is not QuantumEspressoWorkspaceEntryType.REGULAR_FILE
        ):
            raise ValueError("stream candidates must be required regular files")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoNativeOutputExtractionSpecification:
    """Bind explicit output candidates to one program and executable version.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    executable_configuration_identity
        Exact nominal identity retained for cross-record correlation.
    program
        Closed Quantum ESPRESSO program role.
    executable_kind
        Closed real-executable or deterministic-fixture namespace.
    program_version
        Exact admitted executable program version string.
    candidates
        Canonical immutable native-output candidate specifications.
    """

    identity: str
    executable_configuration_identity: QuantumEspressoExecutableConfigurationIdentity
    program: QuantumEspressoProgram
    executable_kind: QuantumEspressoExecutableKind
    program_version: str
    candidates: tuple[QuantumEspressoNativeOutputCandidateSpecification, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not str:
            raise TypeError("identity must be a built-in str")
        if not self.identity:
            raise ValueError("identity must not be empty")
        if (
            type(self.executable_configuration_identity)
            is not QuantumEspressoExecutableConfigurationIdentity
        ):
            raise TypeError(
                "executable_configuration_identity must be "
                "QuantumEspressoExecutableConfigurationIdentity"
            )
        if type(self.program) is not QuantumEspressoProgram:
            raise TypeError("program must be QuantumEspressoProgram")
        if type(self.executable_kind) is not QuantumEspressoExecutableKind:
            raise TypeError("executable_kind must be QuantumEspressoExecutableKind")
        if type(self.program_version) is not str:
            raise TypeError("program_version must be a built-in str")
        if not self.program_version:
            raise ValueError("program_version must not be empty")
        values = self.candidates
        if type(values) is not tuple or any(
            type(value) is not QuantumEspressoNativeOutputCandidateSpecification
            for value in values
        ):
            raise TypeError(
                "candidates must contain "
                "QuantumEspressoNativeOutputCandidateSpecification values"
            )
        if (
            values
            != tuple(sorted(values, key=lambda value: value.artifact_identity.value))
            or len({value.artifact_identity for value in values}) != len(values)
            or len({value.relative_path for value in values}) != len(values)
        ):
            raise ValueError(
                "candidates must be unique and sorted by artifact identity"
            )
        roles = tuple(value.role for value in values)
        if (
            roles.count(QuantumEspressoNativeOutputRole.STDOUT) != 1
            or roles.count(QuantumEspressoNativeOutputRole.STDERR) != 1
        ):
            raise ValueError(
                "specification requires exactly one stdout and stderr candidate"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoNativeOutputManifestEntry:
    """Represent one verified stream or native workspace candidate.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    artifact_identity
        Exact nominal identity retained for cross-record correlation.
    role
        Closed integration-owned artifact role.
    relative_path
        Parent-free portable POSIX path relative to the workspace.
    entry_type
        Closed supported regular-file or directory kind.
    content
        Closed exact file or deterministic tree content contract.
    symlink_observed
        Always false in a successful closed manifest entry.
    """

    identity: ArtifactManifestEntryIdentity
    artifact_identity: ArtifactIdentity
    role: QuantumEspressoNativeOutputRole
    relative_path: QuantumEspressoArtifactDestination
    entry_type: QuantumEspressoWorkspaceEntryType
    content: QuantumEspressoFileArtifactContent | QuantumEspressoTreeArtifactContent
    symlink_observed: bool

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactManifestEntryIdentity:
            raise TypeError("identity must be ArtifactManifestEntryIdentity")
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if type(self.role) is not QuantumEspressoNativeOutputRole:
            raise TypeError("role must be QuantumEspressoNativeOutputRole")
        if type(self.relative_path) is not QuantumEspressoArtifactDestination:
            raise TypeError("relative_path must be QuantumEspressoArtifactDestination")
        if type(self.entry_type) is not QuantumEspressoWorkspaceEntryType:
            raise TypeError("entry_type must be QuantumEspressoWorkspaceEntryType")
        if type(self.symlink_observed) is not bool:
            raise TypeError("symlink_observed must be a built-in bool")
        if self.symlink_observed:
            raise ValueError("verified manifest entries cannot be symlinks")
        expected_content_type = (
            QuantumEspressoFileArtifactContent
            if self.entry_type is QuantumEspressoWorkspaceEntryType.REGULAR_FILE
            else QuantumEspressoTreeArtifactContent
        )
        if type(self.content) is not expected_content_type:
            raise TypeError("content variant must agree with entry_type")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoNativeOutputManifest:
    """Represent verified output candidates without asserting semantic availability.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    preparation_identity
        Exact nominal identity retained for cross-record correlation.
    after_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    extraction_specification_identity
        Exact nominal identity retained for cross-record correlation.
    entries
        Canonical immutable manifest-entry tuple.
    """

    identity: ArtifactManifestIdentity
    preparation_identity: QuantumEspressoPreparationIdentity
    after_snapshot_identity: ArtifactManifestIdentity
    extraction_specification_identity: str
    entries: tuple[QuantumEspressoNativeOutputManifestEntry, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactManifestIdentity:
            raise TypeError("identity must be ArtifactManifestIdentity")
        if type(self.preparation_identity) is not QuantumEspressoPreparationIdentity:
            raise TypeError(
                "preparation_identity must be QuantumEspressoPreparationIdentity"
            )
        if type(self.after_snapshot_identity) is not ArtifactManifestIdentity:
            raise TypeError("after_snapshot_identity must be ArtifactManifestIdentity")
        if type(self.extraction_specification_identity) is not str:
            raise TypeError("extraction_specification_identity must be a built-in str")
        if not self.extraction_specification_identity:
            raise ValueError("extraction_specification_identity must not be empty")
        if type(self.entries) is not tuple or any(
            type(value) is not QuantumEspressoNativeOutputManifestEntry
            for value in self.entries
        ):
            raise TypeError(
                "entries must contain QuantumEspressoNativeOutputManifestEntry values"
            )
        if self.entries != tuple(
            sorted(self.entries, key=lambda value: value.artifact_identity.value)
        ) or len({value.artifact_identity for value in self.entries}) != len(
            self.entries
        ):
            raise ValueError("entries must be unique and sorted by artifact identity")
        roles = tuple(value.role for value in self.entries)
        if (
            roles.count(QuantumEspressoNativeOutputRole.STDOUT) != 1
            or roles.count(QuantumEspressoNativeOutputRole.STDERR) != 1
        ):
            raise ValueError("manifest requires exactly one stdout and stderr entry")


class QuantumEspressoNativeOutputCollectionFailureCode(StrEnum):
    """Closed native-output candidate collection failure codes."""

    NOT_AFTER_SNAPSHOT = "not_after_snapshot"
    BINDING_MISMATCH = "binding_mismatch"
    REQUIRED_CANDIDATE_MISSING = "required_candidate_missing"
    CANDIDATE_TYPE_MISMATCH = "candidate_type_mismatch"
    EMPTY_TREE = "empty_tree"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoNativeOutputCollectionFailure:
    """Represent failure to construct a verified candidate manifest.

    Attributes
    ----------
    code
        Closed failure code for this result.
    after_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    extraction_specification_identity
        Exact nominal identity retained for cross-record correlation.
    related_identity
        Exact nominal identity retained for cross-record correlation.
    """

    code: QuantumEspressoNativeOutputCollectionFailureCode
    after_snapshot_identity: ArtifactManifestIdentity
    extraction_specification_identity: str
    related_identity: str

    def __post_init__(self) -> None:
        if type(self.code) is not QuantumEspressoNativeOutputCollectionFailureCode:
            raise TypeError(
                "code must be QuantumEspressoNativeOutputCollectionFailureCode"
            )
        if type(self.after_snapshot_identity) is not ArtifactManifestIdentity:
            raise TypeError("after_snapshot_identity must be ArtifactManifestIdentity")
        for value, name in (
            (
                self.extraction_specification_identity,
                "extraction_specification_identity",
            ),
            (self.related_identity, "related_identity"),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")


type QuantumEspressoNativeOutputCollectionResult = (
    QuantumEspressoNativeOutputManifest | QuantumEspressoNativeOutputCollectionFailure
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoNativeOutputCollector:
    """Collect explicit operation/version candidates from a closed after-snapshot.

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
        snapshot: QuantumEspressoWorkspaceSnapshot,
        specification: QuantumEspressoNativeOutputExtractionSpecification,
    ) -> QuantumEspressoNativeOutputCollectionResult:
        """Return a verified candidate manifest or a typed collection failure."""
        if type(snapshot) is not QuantumEspressoWorkspaceSnapshot:
            raise TypeError("snapshot must be QuantumEspressoWorkspaceSnapshot")
        if (
            type(specification)
            is not QuantumEspressoNativeOutputExtractionSpecification
        ):
            raise TypeError(
                "specification must be "
                "QuantumEspressoNativeOutputExtractionSpecification"
            )
        if snapshot.phase is not QuantumEspressoWorkspaceSnapshotPhase.AFTER:
            return self._failure(
                snapshot,
                specification,
                QuantumEspressoNativeOutputCollectionFailureCode.NOT_AFTER_SNAPSHOT,
                snapshot.identity.value,
            )
        if (
            snapshot.executable_configuration_identity
            != specification.executable_configuration_identity
            or snapshot.program is not specification.program
            or snapshot.executable_kind is not specification.executable_kind
            or snapshot.program_version != specification.program_version
        ):
            return self._failure(
                snapshot,
                specification,
                QuantumEspressoNativeOutputCollectionFailureCode.BINDING_MISMATCH,
                specification.identity,
            )
        by_path = {value.relative_path: value for value in snapshot.entries}
        entries: list[QuantumEspressoNativeOutputManifestEntry] = []
        for candidate in specification.candidates:
            observed = by_path.get(candidate.relative_path)
            if observed is None:
                if candidate.required:
                    return self._failure(
                        snapshot,
                        specification,
                        QuantumEspressoNativeOutputCollectionFailureCode.REQUIRED_CANDIDATE_MISSING,
                        candidate.artifact_identity.value,
                    )
                continue
            if observed.entry_type is not candidate.entry_type:
                return self._failure(
                    snapshot,
                    specification,
                    QuantumEspressoNativeOutputCollectionFailureCode.CANDIDATE_TYPE_MISMATCH,
                    candidate.artifact_identity.value,
                )
            if observed.entry_type is QuantumEspressoWorkspaceEntryType.REGULAR_FILE:
                content: (
                    QuantumEspressoFileArtifactContent
                    | QuantumEspressoTreeArtifactContent
                ) = QuantumEspressoFileArtifactContent(observed.content_identity)
                content_key = (
                    f"{observed.content_identity.algorithm}:"
                    f"{observed.content_identity.digest}:"
                    f"{observed.content_identity.byte_count}"
                )
            else:
                prefix = candidate.relative_path.value + "/"
                descendants = tuple(
                    value
                    for value in snapshot.entries
                    if value.relative_path.value.startswith(prefix)
                )
                if not descendants:
                    return self._failure(
                        snapshot,
                        specification,
                        QuantumEspressoNativeOutputCollectionFailureCode.EMPTY_TREE,
                        candidate.artifact_identity.value,
                    )
                tree_entries = tuple(
                    sorted(
                        (
                            self._tree_entry(candidate.relative_path, value)
                            for value in descendants
                        ),
                        key=lambda value: value.value,
                    )
                )
                tree_manifest = ArtifactManifestIdentity(
                    "qe-native-output-tree-v1:"
                    + self._framed_digest(tuple(value.value for value in tree_entries))
                )
                content = QuantumEspressoTreeArtifactContent(
                    tree_manifest, tree_entries
                )
                content_key = tree_manifest.value
            entry_identity = ArtifactManifestEntryIdentity(
                "qe-native-output-entry-v1:"
                + self._framed_digest(
                    (
                        candidate.artifact_identity.value,
                        candidate.role.value,
                        candidate.relative_path.value,
                        candidate.entry_type.value,
                        content_key,
                        "symlink:false",
                    )
                )
            )
            entries.append(
                QuantumEspressoNativeOutputManifestEntry(
                    identity=entry_identity,
                    artifact_identity=candidate.artifact_identity,
                    role=candidate.role,
                    relative_path=candidate.relative_path,
                    entry_type=candidate.entry_type,
                    content=content,
                    symlink_observed=False,
                )
            )
        canonical = tuple(
            sorted(entries, key=lambda value: value.artifact_identity.value)
        )
        manifest_identity = ArtifactManifestIdentity(
            "qe-native-output-manifest-v1:"
            + self._framed_digest(
                (
                    self.implementation_version,
                    snapshot.identity.value,
                    specification.identity,
                    *(value.identity.value for value in canonical),
                )
            )
        )
        return QuantumEspressoNativeOutputManifest(
            identity=manifest_identity,
            preparation_identity=snapshot.preparation_identity,
            after_snapshot_identity=snapshot.identity,
            extraction_specification_identity=specification.identity,
            entries=canonical,
        )

    @staticmethod
    def _failure(
        snapshot: QuantumEspressoWorkspaceSnapshot,
        specification: QuantumEspressoNativeOutputExtractionSpecification,
        code: QuantumEspressoNativeOutputCollectionFailureCode,
        related: str,
    ) -> QuantumEspressoNativeOutputCollectionFailure:
        return QuantumEspressoNativeOutputCollectionFailure(
            code=code,
            after_snapshot_identity=snapshot.identity,
            extraction_specification_identity=specification.identity,
            related_identity=related,
        )

    @classmethod
    def _tree_entry(
        cls,
        root: QuantumEspressoArtifactDestination,
        entry: QuantumEspressoWorkspaceSnapshotEntry,
    ) -> ArtifactManifestEntryIdentity:
        relative = (
            PurePosixPath(entry.relative_path.value)
            .relative_to(PurePosixPath(root.value))
            .as_posix()
        )
        return ArtifactManifestEntryIdentity(
            "qe-native-output-tree-entry-v1:"
            + cls._framed_digest(
                (
                    entry.entry_type.value,
                    relative,
                    entry.content_identity.algorithm,
                    entry.content_identity.digest,
                    str(entry.content_identity.byte_count),
                )
            )
        )

    @staticmethod
    def _framed_digest(values: tuple[str, ...]) -> str:
        digest = hashlib.sha256()
        for value in values:
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, "big"))
            digest.update(encoded)
        return digest.hexdigest()


class QuantumEspressoTerminalStatus(StrEnum):
    """Closed calculator-level statuses admitted to a private terminal record."""

    COMPLETED = "completed"
    CALCULATOR_FAILED = "calculator_failed"
    PROCESS_FAILED = "process_failed"
    DIAGNOSTIC_UNRESOLVED = "diagnostic_unresolved"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoTerminalRecord:
    """Represent exact identities written to one private version-1 terminal record.

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
    diagnostic_report_identity
        Exact nominal identity retained for cross-record correlation.
    native_output_manifest_identity
        Exact nominal identity retained for cross-record correlation.
    """

    identity: QuantumEspressoTerminalRecordIdentity
    status: QuantumEspressoTerminalStatus
    simulation_execution_request_identity: SimulationExecutionRequestIdentity
    execution_input_identity: QuantumEspressoExecutionInputIdentity
    preparation_identity: QuantumEspressoPreparationIdentity
    process_observation_identity: QuantumEspressoProcessObservationIdentity
    stdout_artifact_identity: ArtifactIdentity
    stdout_content_identity: ArtifactContentIdentity
    stderr_artifact_identity: ArtifactIdentity
    stderr_content_identity: ArtifactContentIdentity
    before_snapshot_identity: ArtifactManifestIdentity
    after_snapshot_identity: ArtifactManifestIdentity
    diagnostic_report_identity: QuantumEspressoDiagnosticReportIdentity
    native_output_manifest_identity: ArtifactManifestIdentity

    def __post_init__(self) -> None:
        expected = (
            (self.identity, QuantumEspressoTerminalRecordIdentity, "identity"),
            (self.status, QuantumEspressoTerminalStatus, "status"),
            (
                self.simulation_execution_request_identity,
                SimulationExecutionRequestIdentity,
                "simulation_execution_request_identity",
            ),
            (
                self.execution_input_identity,
                QuantumEspressoExecutionInputIdentity,
                "execution_input_identity",
            ),
            (
                self.preparation_identity,
                QuantumEspressoPreparationIdentity,
                "preparation_identity",
            ),
            (
                self.process_observation_identity,
                QuantumEspressoProcessObservationIdentity,
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
                self.diagnostic_report_identity,
                QuantumEspressoDiagnosticReportIdentity,
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


@dataclass(frozen=True, slots=True)
class QuantumEspressoTerminalRecordSerializer:
    """Serialize private ``qe-local-terminal-record-v1`` canonical JSON bytes.

    Attributes
    ----------
    wire_version
        Fixed integration-private terminal-record wire discriminator.
    """

    wire_version: str = "qe-local-terminal-record-v1"

    def __post_init__(self) -> None:
        if type(self.wire_version) is not str:
            raise TypeError("wire_version must be a built-in str")
        if self.wire_version != "qe-local-terminal-record-v1":
            raise ValueError("only qe-local-terminal-record-v1 is supported")

    def execute(self, record: QuantumEspressoTerminalRecord) -> bytes:
        """Return deterministic UTF-8 canonical JSON ending in one newline."""
        if type(record) is not QuantumEspressoTerminalRecord:
            raise TypeError("record must be QuantumEspressoTerminalRecord")
        values: dict[str, str] = {
            "after_snapshot_identity": record.after_snapshot_identity.value,
            "before_snapshot_identity": record.before_snapshot_identity.value,
            "diagnostic_report_identity": record.diagnostic_report_identity.value,
            "execution_input_identity": record.execution_input_identity.value,
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
        return (
            json.dumps(
                values, ensure_ascii=False, separators=(",", ":"), sort_keys=True
            )
            + "\n"
        ).encode("utf-8")

    @staticmethod
    def _content_identity(identity: ArtifactContentIdentity) -> str:
        return f"{identity.algorithm}:{identity.digest}:{identity.byte_count}"


class QuantumEspressoTerminalPublicationFailureCode(StrEnum):
    """Closed atomic terminal publication failure codes."""

    CONTENT_IDENTITY_MISMATCH = "content_identity_mismatch"
    DESTINATION_EXISTS = "destination_exists"
    INVALID_DESTINATION = "invalid_destination"
    LIMIT_EXCEEDED = "limit_exceeded"
    PUBLICATION_FAILED = "publication_failed"
    DURABILITY_UNCERTAIN = "durability_uncertain"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoTerminalPublicationFailure:
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

    code: QuantumEspressoTerminalPublicationFailureCode
    terminal_record_identity: QuantumEspressoTerminalRecordIdentity
    publication_observed: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QuantumEspressoTerminalPublicationFailureCode:
            raise TypeError(
                "code must be QuantumEspressoTerminalPublicationFailureCode"
            )
        if (
            type(self.terminal_record_identity)
            is not QuantumEspressoTerminalRecordIdentity
        ):
            raise TypeError(
                "terminal_record_identity must be QuantumEspressoTerminalRecordIdentity"
            )
        if type(self.publication_observed) is not bool:
            raise TypeError("publication_observed must be a built-in bool")
        if type(self.observed_condition) is not str:
            raise TypeError("observed_condition must be a built-in str")
        if not self.observed_condition:
            raise ValueError("observed_condition must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoPublishedTerminalRecord:
    """Record one successful same-directory atomic no-replace publication.

    Attributes
    ----------
    terminal_record_identity
        Exact nominal identity retained for cross-record correlation.
    content_identity
        Exact nominal identity retained for cross-record correlation.
    destination
        Exact destination path or parent-free workspace destination, as declared.
    """

    terminal_record_identity: QuantumEspressoTerminalRecordIdentity
    content_identity: ArtifactContentIdentity
    destination: Path

    def __post_init__(self) -> None:
        if (
            type(self.terminal_record_identity)
            is not QuantumEspressoTerminalRecordIdentity
        ):
            raise TypeError(
                "terminal_record_identity must be QuantumEspressoTerminalRecordIdentity"
            )
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")
        if not isinstance(self.destination, Path):
            raise TypeError("destination must be pathlib.Path")
        if not self.destination.is_absolute():
            raise ValueError("destination must be absolute")


type QuantumEspressoTerminalPublicationResult = (
    QuantumEspressoPublishedTerminalRecord | QuantumEspressoTerminalPublicationFailure
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoTerminalRecordPublisher:
    """Atomically publish one new private terminal record without replacement.

    Parameters
    ----------
    implementation_version
        Nonempty identity of the same-directory hard-link publication algorithm.
    snapshotter
        Bounded observer used to close current workspace usage before mutation.
    """

    implementation_version: str
    snapshotter: QuantumEspressoWorkspaceSnapshotter

    def __post_init__(self) -> None:
        if type(self.implementation_version) is not str:
            raise TypeError("implementation_version must be a built-in str")
        if not self.implementation_version:
            raise ValueError("implementation_version must not be empty")
        if type(self.snapshotter) is not QuantumEspressoWorkspaceSnapshotter:
            raise TypeError("snapshotter must be QuantumEspressoWorkspaceSnapshotter")

    def execute(
        self,
        prepared: LocalQuantumEspressoPreparedExecution,
        terminal_record_identity: QuantumEspressoTerminalRecordIdentity,
        serialized_record: bytes,
        content_identity: ArtifactContentIdentity,
    ) -> QuantumEspressoTerminalPublicationResult:
        """Publish exact bytes with one same-directory atomic hard-link operation."""
        if type(prepared) is not LocalQuantumEspressoPreparedExecution:
            raise TypeError("prepared must be LocalQuantumEspressoPreparedExecution")
        if type(terminal_record_identity) is not QuantumEspressoTerminalRecordIdentity:
            raise TypeError(
                "terminal_record_identity must be QuantumEspressoTerminalRecordIdentity"
            )
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
                QuantumEspressoTerminalPublicationFailureCode.CONTENT_IDENTITY_MISMATCH,
                terminal_record_identity,
                False,
                "serialized terminal bytes differ from their declared identity",
            )
        destinations = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQuantumEspressoResolvedDestinationRole.TERMINAL_RECORD
        )
        if len(destinations) != 1:
            return self._failure(
                QuantumEspressoTerminalPublicationFailureCode.INVALID_DESTINATION,
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
                QuantumEspressoTerminalPublicationFailureCode.INVALID_DESTINATION,
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
                    QuantumEspressoTerminalPublicationFailureCode.INVALID_DESTINATION,
                    terminal_record_identity,
                    False,
                    "terminal destination is not confined to the canonical workspace",
                )
        except OSError:
            return self._failure(
                QuantumEspressoTerminalPublicationFailureCode.INVALID_DESTINATION,
                terminal_record_identity,
                False,
                "terminal destination confinement could not be established",
            )
        if target.exists() or target.is_symlink():
            return self._failure(
                QuantumEspressoTerminalPublicationFailureCode.DESTINATION_EXISTS,
                terminal_record_identity,
                True,
                "terminal destination already exists and was not replaced",
            )
        current = self.snapshotter.execute(
            prepared, QuantumEspressoWorkspaceSnapshotPhase.AFTER
        )
        if isinstance(current, QuantumEspressoWorkspaceSnapshotFailure):
            return self._failure(
                QuantumEspressoTerminalPublicationFailureCode.PUBLICATION_FAILED,
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
                QuantumEspressoTerminalPublicationFailureCode.LIMIT_EXCEEDED,
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
                QuantumEspressoTerminalPublicationFailureCode.DESTINATION_EXISTS,
                terminal_record_identity,
                target.exists(),
                "terminal or temporary no-replace destination already exists",
            )
        except OSError:
            if temporary.exists() and not temporary.is_symlink():
                temporary.unlink()
            code = (
                QuantumEspressoTerminalPublicationFailureCode.DURABILITY_UNCERTAIN
                if published
                else QuantumEspressoTerminalPublicationFailureCode.PUBLICATION_FAILED
            )
            return self._failure(
                code,
                terminal_record_identity,
                published or target.exists(),
                "terminal publication or durability synchronization failed",
            )
        return QuantumEspressoPublishedTerminalRecord(
            terminal_record_identity=terminal_record_identity,
            content_identity=content_identity,
            destination=target,
        )

    @staticmethod
    def _link(source: Path, destination: Path) -> None:
        os.link(source, destination, follow_symlinks=False)

    @staticmethod
    def _failure(
        code: QuantumEspressoTerminalPublicationFailureCode,
        identity: QuantumEspressoTerminalRecordIdentity,
        observed: bool,
        condition: str,
    ) -> QuantumEspressoTerminalPublicationFailure:
        return QuantumEspressoTerminalPublicationFailure(
            code=code,
            terminal_record_identity=identity,
            publication_observed=observed,
            observed_condition=condition,
        )
