"""No-replace local input staging for one prepared ``pw.x`` attempt."""

from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from projectkoios.simulations.calculator_input import (
    CalculatorExternalInputRequirement,
    CalculatorInputArtifact,
)

from ksdft2effmass.serialization import StrWireEnum
from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
)

from ..calculator_input import (
    QeCalculatorInputAdmission,
    QeCalculatorInputAdmissionFailure,
    QeCalculatorInputBinding,
)
from ..contracts import (
    QeExecutionInput,
    QeNativeInputArtifact,
    QePreparationIdentity,
)
from ..execution import (
    LocalQeArtifactSource,
    LocalQeExecutionLimits,
    LocalQeFileSourceObservation,
    LocalQePreparedExecution,
    LocalQeResolvedDestination,
    LocalQeResolvedDestinationRole,
    LocalQeTreeSourceObservation,
)

_MAX_U64 = 18_446_744_073_709_551_615


@dataclass(frozen=True, slots=True)
class QeStagingResultIdentity:
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


class QeStagingFailureCode(StrWireEnum):
    """Closed failure codes for integration-owned input staging."""

    INPUT_BINDING_MISMATCH = "input_binding_mismatch"
    WORKSPACE_EXISTS = "workspace_exists"
    SOURCE_CHANGED = "source_changed"
    SYMLINK_OR_TYPE = "symlink_or_type"
    LIMIT_EXCEEDED = "limit_exceeded"
    DESTINATION_CONFLICT = "destination_conflict"
    IO_FAILED = "io_failed"


@dataclass(frozen=True, slots=True, kw_only=True)
class QeStagingFailure:
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

    code: QeStagingFailureCode
    preparation_identity: QePreparationIdentity
    related_identity: str
    workspace_created: bool
    observed_condition: str

    def __post_init__(self) -> None:
        if type(self.code) is not QeStagingFailureCode:
            raise TypeError("code must be QeStagingFailureCode")
        if type(self.preparation_identity) is not QePreparationIdentity:
            raise TypeError("preparation_identity must be QePreparationIdentity")
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
class QeStagedExecution:
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
        Canonically ordered identities of all staged input artifacts.
    created_entry_count
        Number of directories and regular files created beneath the workspace.
    created_total_bytes
        Total regular-file bytes present immediately after staging.
    implementation_version
        Nonempty staging algorithm/version identifier.
    """

    identity: QeStagingResultIdentity
    preparation_identity: QePreparationIdentity
    workspace: Path
    staged_artifact_identities: tuple[ArtifactIdentity, ...]
    created_entry_count: int
    created_total_bytes: int
    implementation_version: str

    def __post_init__(self) -> None:
        if type(self.identity) is not QeStagingResultIdentity:
            raise TypeError("identity must be QeStagingResultIdentity")
        if type(self.preparation_identity) is not QePreparationIdentity:
            raise TypeError("preparation_identity must be QePreparationIdentity")
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


type QeStagingResult = QeStagedExecution | QeStagingFailure


@dataclass(frozen=True, slots=True)
class QeInputStager:
    """Stage exact prepared inputs into a new root-confined workspace.

    Parameters
    ----------
    implementation_version
        Nonempty version identity for the staging and re-observation algorithm.

    Notes
    -----
    Staging writes native input bytes from the admitted provider binding, rechecks the
    executable and remaining external or predecessor source identities before
    mutation, and rechecks every destination identity afterward. It never discovers or
    mutates a predecessor workspace, starts a process, or removes a partially
    observable failed workspace.
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
        calculator_input_binding: QeCalculatorInputBinding,
    ) -> QeStagingResult:
        """Create the absent workspace and stage every exact input artifact.

        The native calculator input bytes are written directly from the admitted
        provider record. External pseudopotentials and predecessor trees remain
        explicitly correlated local resources.

        Raises
        ------
        TypeError
            If either argument does not have its exact required type.
        """
        if type(prepared) is not LocalQePreparedExecution:
            raise TypeError("prepared must be LocalQePreparedExecution")
        if type(calculator_input_binding) is not QeCalculatorInputBinding:
            raise TypeError("calculator_input_binding must be QeCalculatorInputBinding")
        if calculator_input_binding is not prepared.calculator_input_binding:
            return self._failure(
                prepared,
                QeStagingFailureCode.INPUT_BINDING_MISMATCH,
                prepared.request.execution_input.identity.value,
                False,
                "staging did not receive the exact prepared calculator input binding",
            )
        if (
            calculator_input_binding.execution_input
            is not prepared.request.execution_input
        ):
            return self._failure(
                prepared,
                QeStagingFailureCode.INPUT_BINDING_MISMATCH,
                prepared.request.execution_input.identity.value,
                False,
                "calculator input binding does not retain the prepared execution input",
            )
        readmission: QeCalculatorInputBinding | QeCalculatorInputAdmissionFailure = (
            QeCalculatorInputAdmission(
                calculator_input_binding.admission_policy_identity
            ).execute(
                calculator_input_binding.calculator_input,
                prepared.request.execution_input,
            )
        )
        if type(readmission) is QeCalculatorInputAdmissionFailure:
            return self._failure(
                prepared,
                QeStagingFailureCode.INPUT_BINDING_MISMATCH,
                prepared.request.execution_input.identity.value,
                False,
                "calculator input binding no longer satisfies its admission policy",
            )
        if type(readmission) is not QeCalculatorInputBinding:
            raise TypeError(
                "calculator input readmission returned an unsupported result"
            )
        workspace: Path = prepared.workspace
        if workspace.exists() or workspace.is_symlink():
            return self._failure(
                prepared,
                QeStagingFailureCode.WORKSPACE_EXISTS,
                prepared.identity.value,
                False,
                "attempt workspace is no longer absent",
            )
        if not self._roots_still_confined(prepared):
            return self._failure(
                prepared,
                QeStagingFailureCode.SYMLINK_OR_TYPE,
                prepared.identity.value,
                False,
                "prepared roots or source paths are no longer confined",
            )
        if not self._sources_still_match(prepared):
            return self._failure(
                prepared,
                QeStagingFailureCode.SOURCE_CHANGED,
                prepared.identity.value,
                False,
                "one or more prepared source identities changed",
            )
        projected: tuple[int, int] | None = self._projected_usage(prepared)
        if projected is None:
            return self._failure(
                prepared,
                QeStagingFailureCode.SYMLINK_OR_TYPE,
                prepared.identity.value,
                False,
                "a source tree contains an unsupported entry",
            )
        entry_count: int
        total_bytes: int
        entry_count, total_bytes = projected
        limits: LocalQeExecutionLimits = prepared.request.limits
        if (
            entry_count > limits.maximum_created_entry_count
            or total_bytes > limits.maximum_created_total_bytes
        ):
            return self._failure(
                prepared,
                QeStagingFailureCode.LIMIT_EXCEEDED,
                prepared.identity.value,
                False,
                "staged inputs and explicit destination directories exceed a "
                "declared ceiling",
            )
        try:
            workspace.mkdir(mode=0o700, exist_ok=False)
            self._create_scaffold(prepared)
            executable_destination: LocalQeResolvedDestination = (
                self._executable_destination(prepared)
            )
            self._copy_file(
                prepared.request.executable_path,
                executable_destination.absolute_path,
                destination_mode=0o500,
            )
            primary_input: CalculatorInputArtifact = (
                calculator_input_binding.primary_input_artifact
            )
            native_destination: LocalQeResolvedDestination = self._input_destination(
                prepared, prepared.request.execution_input.native_input.identity
            )
            self._write_bytes(
                primary_input.content,
                native_destination.absolute_path,
                destination_mode=0o600,
            )
            external_artifact_sources: tuple[LocalQeArtifactSource, ...] = (
                prepared.request.external_artifact_sources
            )
            provider_resource_identities: frozenset[ArtifactIdentity] = frozenset(
                value.artifact_identity
                for value in calculator_input_binding.external_input_resources
            )
            predecessor_identities: frozenset[ArtifactIdentity] = frozenset(
                value.identity
                for value in prepared.request.execution_input.predecessor_native_state
            )
            for source in external_artifact_sources:
                destination: LocalQeResolvedDestination = self._input_destination(
                    prepared, source.artifact_identity
                )
                if source.artifact_identity in provider_resource_identities:
                    self._copy_file(
                        source.source,
                        destination.absolute_path,
                        destination_mode=0o600,
                    )
                elif source.artifact_identity in predecessor_identities:
                    self._copy_tree(source.source, destination.absolute_path)
                else:
                    raise TypeError("prepared artifact has an unsupported identity")
            if not self._destinations_match(prepared):
                return self._failure(
                    prepared,
                    QeStagingFailureCode.SOURCE_CHANGED,
                    prepared.identity.value,
                    True,
                    "one or more staged destination identities differ from preparation",
                )
            self._lock_immutable_launch_paths(prepared)
        except FileExistsError:
            return self._failure(
                prepared,
                QeStagingFailureCode.DESTINATION_CONFLICT,
                prepared.identity.value,
                workspace.exists(),
                "a no-replace staging destination already exists",
            )
        except OSError:
            return self._failure(
                prepared,
                QeStagingFailureCode.IO_FAILED,
                prepared.identity.value,
                workspace.exists(),
                "filesystem staging did not complete determinately",
            )
        identity: QeStagingResultIdentity = QeStagingResultIdentity(
            "qe-input-staging-v1:"
            + self._framed_digest(
                (
                    self.implementation_version,
                    prepared.identity.value,
                    calculator_input_binding.calculator_input.input_id,
                    calculator_input_binding.calculator_input.sha256,
                    str(entry_count),
                    str(total_bytes),
                    *(
                        value.value
                        for value in self._input_artifact_identities(prepared)
                    ),
                )
            )
        )
        return QeStagedExecution(
            identity=identity,
            preparation_identity=prepared.identity,
            workspace=workspace,
            staged_artifact_identities=self._input_artifact_identities(prepared),
            created_entry_count=entry_count,
            created_total_bytes=total_bytes,
            implementation_version=self.implementation_version,
        )

    @staticmethod
    def _failure(
        prepared: LocalQePreparedExecution,
        code: QeStagingFailureCode,
        related: str,
        created: bool,
        condition: str,
    ) -> QeStagingFailure:
        return QeStagingFailure(
            code=code,
            preparation_identity=prepared.identity,
            related_identity=related,
            workspace_created=created,
            observed_condition=condition,
        )

    @staticmethod
    def _executable_destination(
        prepared: LocalQePreparedExecution,
    ) -> LocalQeResolvedDestination:
        matches = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQeResolvedDestinationRole.EXECUTABLE
        )
        if len(matches) != 1:
            raise OSError("prepared executable destination is not unique")
        return matches[0]

    @staticmethod
    def _input_destination(
        prepared: LocalQePreparedExecution, identity: ArtifactIdentity
    ) -> LocalQeResolvedDestination:
        matches = tuple(
            value
            for value in prepared.resolved_destinations
            if value.role is LocalQeResolvedDestinationRole.INPUT_ARTIFACT
            and value.owner_identity == identity.value
        )
        if len(matches) != 1:
            raise OSError("prepared input destination is not unique")
        return matches[0]

    def _input_artifact_identities(
        self, prepared: LocalQePreparedExecution
    ) -> tuple[ArtifactIdentity, ...]:
        execution_input: QeExecutionInput = prepared.request.execution_input
        values: tuple[ArtifactIdentity, ...] = (
            execution_input.native_input.identity,
            *(
                value.artifact_identity
                for value in prepared.calculator_input_binding.external_input_resources
            ),
            *(value.identity for value in execution_input.predecessor_native_state),
        )
        return tuple(sorted(values, key=lambda value: value.value))

    @staticmethod
    def _roots_still_confined(
        prepared: LocalQePreparedExecution,
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
                for source in prepared.request.external_artifact_sources
            )
        except OSError:
            return False

    def _sources_still_match(self, prepared: LocalQePreparedExecution) -> bool:
        try:
            if (
                self._file_identity(prepared.request.executable_path)
                != prepared.executable_content_identity
            ):
                return False
        except OSError:
            return False
        observations: dict[
            ArtifactIdentity,
            LocalQeFileSourceObservation | LocalQeTreeSourceObservation,
        ] = {value.artifact_identity: value for value in prepared.source_observations}
        for source in prepared.request.external_artifact_sources:
            observation: LocalQeFileSourceObservation | LocalQeTreeSourceObservation = (
                observations[source.artifact_identity]
            )
            try:
                if type(observation) is LocalQeFileSourceObservation:
                    if (
                        self._file_identity(source.source)
                        != observation.content_identity
                    ):
                        return False
                else:
                    assert type(observation) is LocalQeTreeSourceObservation
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

    def _destinations_match(self, prepared: LocalQePreparedExecution) -> bool:
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
        binding: QeCalculatorInputBinding = prepared.calculator_input_binding
        primary: CalculatorInputArtifact = binding.primary_input_artifact
        native: QeNativeInputArtifact = prepared.request.execution_input.native_input
        native_destination: Path = self._input_destination(
            prepared, native.identity
        ).absolute_path
        try:
            native_identity: ArtifactContentIdentity = self._file_identity(
                native_destination
            )
            if (
                native_identity.byte_count != primary.byte_size
                or native_identity.digest != primary.sha256
            ):
                return False
            for resource in binding.external_input_resources:
                destination: Path = self._input_destination(
                    prepared, resource.artifact_identity
                ).absolute_path
                requirement: CalculatorExternalInputRequirement = (
                    resource.external_requirement
                )
                observed: ArtifactContentIdentity = self._file_identity(destination)
                if (
                    observed.byte_count != requirement.byte_size
                    or observed.digest != requirement.sha256
                ):
                    return False
            for (
                predecessor
            ) in prepared.request.execution_input.predecessor_native_state:
                destination = self._input_destination(
                    prepared, predecessor.identity
                ).absolute_path
                entries, _ = self._tree_identities(destination)
                manifest = ArtifactManifestIdentity(
                    "qe-tree-manifest-v1:"
                    + self._framed_digest(tuple(value.value for value in entries))
                )
                if (
                    entries != predecessor.content.manifest_entry_identities
                    or manifest != predecessor.content.manifest_identity
                ):
                    return False
        except OSError:
            return False
        return True

    def _lock_immutable_launch_paths(self, prepared: LocalQePreparedExecution) -> None:
        """Remove ordinary write access from immutable launch paths and parents."""
        immutable_paths: list[Path] = [
            self._executable_destination(prepared).absolute_path
        ]
        native_identity: ArtifactIdentity = (
            prepared.request.execution_input.native_input.identity
        )
        immutable_input_identities: tuple[ArtifactIdentity, ...] = (
            native_identity,
            *(
                value.artifact_identity
                for value in prepared.calculator_input_binding.external_input_resources
            ),
        )
        immutable_paths.extend(
            self._input_destination(prepared, identity).absolute_path
            for identity in immutable_input_identities
        )
        for path in immutable_paths:
            path.chmod(0o500 if path == immutable_paths[0] else 0o400)
        for parent in {path.parent for path in immutable_paths}:
            parent.chmod(0o500)
        prepared.workspace.chmod(0o500)

    def _projected_usage(
        self, prepared: LocalQePreparedExecution
    ) -> tuple[int, int] | None:
        entries: set[str] = set()
        total_bytes = 0
        for destination in prepared.resolved_destinations:
            path = PurePosixPath(destination.portable_destination.value)
            for parent in path.parents:
                if parent.as_posix() != ".":
                    entries.add(parent.as_posix())
            if destination.role in (
                LocalQeResolvedDestinationRole.WORK,
                LocalQeResolvedDestinationRole.RESULT,
            ):
                entries.add(path.as_posix())
            elif destination.role is LocalQeResolvedDestinationRole.EXECUTABLE:
                entries.add(path.as_posix())
                total_bytes += prepared.executable_content_identity.byte_count
        external_sources_by_identity: dict[ArtifactIdentity, LocalQeArtifactSource] = {
            source.artifact_identity: source
            for source in prepared.request.external_artifact_sources
        }
        native: QeNativeInputArtifact = prepared.request.execution_input.native_input
        native_base: PurePosixPath = PurePosixPath(native.destination.value)
        entries.add(native_base.as_posix())
        total_bytes += (
            prepared.calculator_input_binding.primary_input_artifact.byte_size
        )
        for resource in prepared.calculator_input_binding.external_input_resources:
            resource_base: PurePosixPath = PurePosixPath(resource.destination.value)
            entries.add(resource_base.as_posix())
            total_bytes += resource.external_requirement.byte_size
        for predecessor in prepared.request.execution_input.predecessor_native_state:
            base: PurePosixPath = PurePosixPath(predecessor.destination.value)
            entries.add(base.as_posix())
            source: LocalQeArtifactSource = external_sources_by_identity[
                predecessor.identity
            ]
            try:
                descendants: tuple[tuple[PurePosixPath, bool, int], ...] = (
                    self._tree_paths(source.source)
                )
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
    def _create_scaffold(prepared: LocalQePreparedExecution) -> None:
        directories: set[Path] = set()
        for destination in prepared.resolved_destinations:
            directories.update(
                parent
                for parent in destination.absolute_path.parents
                if parent != prepared.workspace
                and parent.is_relative_to(prepared.workspace)
            )
            if destination.role in (
                LocalQeResolvedDestinationRole.WORK,
                LocalQeResolvedDestinationRole.RESULT,
            ):
                directories.add(destination.absolute_path)
        for directory in sorted(
            directories, key=lambda value: (len(value.parts), str(value))
        ):
            directory.mkdir(mode=0o700, exist_ok=True)

    def _write_bytes(
        self, content: bytes, destination: Path, *, destination_mode: int
    ) -> None:
        destination_flags: int = (
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        )
        destination_descriptor: int = os.open(
            destination, destination_flags, destination_mode
        )
        try:
            view: memoryview = memoryview(content)
            while view:
                written: int = os.write(destination_descriptor, view)
                view = view[written:]
            os.fsync(destination_descriptor)
        finally:
            os.close(destination_descriptor)

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
