"""Root-confined local preparation for Quantum ESPRESSO execution.

This module implements the read-only preparation stage of the local Quantum ESPRESSO
integration. Preparation validates exact executable and input-source identities,
checks path confinement and operational limits, and returns an immutable dry-run-ready
result. It creates no workspace, stages no artifact, opens no output stream, and
invokes no process.

The deterministic tree-manifest convention in this module is integration-local. It is
not the Workflow artifact-manifest wire format and establishes no semantic,
numerical, or scientific validity of native files.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import stat
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath

from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    DispatchDestinationIdentity,
    DispatchResourceScopeIdentity,
    ScientificExecutorIdentity,
    SimulationExecutionAuthorizationResultIdentity,
    SimulationExecutionRequestIdentity,
)

from .contracts import (
    QuantumEspressoArtifactDestination,
    QuantumEspressoDiagnosticClassifierIdentity,
    QuantumEspressoExecutableConfiguration,
    QuantumEspressoExecutableConfigurationIdentity,
    QuantumEspressoExecutableKind,
    QuantumEspressoExecutionInput,
    QuantumEspressoExecutionInputIdentity,
    QuantumEspressoFileArtifactContent,
    QuantumEspressoInputArtifact,
    QuantumEspressoNativeInputArtifact,
    QuantumEspressoPredecessorNativeStateArtifact,
    QuantumEspressoPreparationIdentity,
    QuantumEspressoProgram,
    QuantumEspressoPseudopotentialArtifact,
)

_MAX_U64 = 18_446_744_073_709_551_615
_PREPARATION_CLAIM_BOUNDARY = (
    "read-only local path and identity preparation only",
    "no workspace creation or artifact staging",
    "no process invocation or execution authority",
    "no Quantum ESPRESSO compatibility claim",
    "no numerical or scientific validation",
)


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoPreparationImplementationIdentity:
    """Identify one exact local preparation implementation and version.

    Attributes
    ----------
    value
        Nonempty built-in string identifying the preparation algorithm, including its
        path-confinement and content-identity conventions.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError(
                "preparation implementation identity must be a built-in str"
            )
        if not self.value:
            raise ValueError("preparation implementation identity must not be empty")


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoAttemptWorkspaceName:
    """Represent one parent-free attempt-workspace directory name.

    Attributes
    ----------
    value
        Nonempty built-in string containing exactly one portable POSIX path component.
        Absolute, home-relative, dot, parent, backslash, and drive-prefixed forms are
        rejected.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("attempt workspace name must be a built-in str")
        if not self.value:
            raise ValueError("attempt workspace name must not be empty")
        path = PurePosixPath(self.value)
        if (
            self.value.startswith(("/", "~"))
            or "\\" in self.value
            or path.as_posix() != self.value
            or len(path.parts) != 1
            or path.parts[0] in {"", ".", ".."}
            or (
                len(self.value) >= 2
                and self.value[0].isalpha()
                and self.value[1] == ":"
            )
        ):
            raise ValueError("attempt workspace name must be parent-free portable text")


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoArtifactSource:
    """Bind one exact QE input artifact to one absolute local source.

    Attributes
    ----------
    artifact
        Exact QE-native input, pseudopotential, or predecessor-state artifact record.
    source
        Absolute local path. Preparation requires a nonsymlink regular file for file
        artifacts or a nonsymlink directory tree for predecessor state.
    """

    artifact: QuantumEspressoInputArtifact
    source: Path

    def __post_init__(self) -> None:
        if type(self.artifact) not in (
            QuantumEspressoNativeInputArtifact,
            QuantumEspressoPseudopotentialArtifact,
            QuantumEspressoPredecessorNativeStateArtifact,
        ):
            raise TypeError("artifact must be a closed QuantumEspressoInputArtifact")
        if not isinstance(self.source, Path):
            raise TypeError("source must be pathlib.Path")
        if not self.source.is_absolute():
            raise ValueError("source must be absolute")


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoPeakResidentBytesUnlimited:
    """Represent absence of a peak resident-memory ceiling.

    Attributes
    ----------
    None
        This marker has no fields and requests no finite peak-RSS ceiling.
    """


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoPeakResidentBytesLimit:
    """Represent a positive peak resident-memory ceiling.

    Attributes
    ----------
    byte_count
        Positive built-in integer number of bytes in the unsigned 64-bit range.
    """

    byte_count: int

    def __post_init__(self) -> None:
        if type(self.byte_count) is not int:
            raise TypeError("peak resident byte limit must be a built-in int")
        if not 0 < self.byte_count <= _MAX_U64:
            raise ValueError(
                "peak resident byte limit must be in the positive u64 range"
            )


type LocalQuantumEspressoPeakResidentBytesPolicy = (
    LocalQuantumEspressoPeakResidentBytesUnlimited
    | LocalQuantumEspressoPeakResidentBytesLimit
)
"""Closed present/absent peak resident-memory limit."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQuantumEspressoExecutionLimits:
    """Represent operational ceilings for one local execution attempt.

    Attributes
    ----------
    wall_time_milliseconds
        Positive wall-time ceiling in milliseconds.
    termination_grace_milliseconds
        Positive interval between termination and kill escalation, in milliseconds.
    minimum_free_bytes
        Nonnegative free-space requirement observed before workspace creation.
    maximum_created_entry_count
        Positive ceiling for entries created beneath the attempt workspace.
    maximum_created_total_bytes
        Positive ceiling for total created regular-file bytes.
    peak_resident_bytes
        Closed explicit present/absent peak resident-memory ceiling.

    Notes
    -----
    These ceilings are operational controls, not scientific convergence settings.
    """

    wall_time_milliseconds: int
    termination_grace_milliseconds: int
    minimum_free_bytes: int
    maximum_created_entry_count: int
    maximum_created_total_bytes: int
    peak_resident_bytes: LocalQuantumEspressoPeakResidentBytesPolicy

    def __post_init__(self) -> None:
        positive = (
            "wall_time_milliseconds",
            "termination_grace_milliseconds",
            "maximum_created_entry_count",
            "maximum_created_total_bytes",
        )
        for name in positive:
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if not 0 < value <= _MAX_U64:
                raise ValueError(f"{name} must be in the positive u64 range")
        if type(self.minimum_free_bytes) is not int:
            raise TypeError("minimum_free_bytes must be a built-in int")
        if not 0 <= self.minimum_free_bytes <= _MAX_U64:
            raise ValueError("minimum_free_bytes must be in the unsigned 64-bit range")
        if type(self.peak_resident_bytes) not in (
            LocalQuantumEspressoPeakResidentBytesUnlimited,
            LocalQuantumEspressoPeakResidentBytesLimit,
        ):
            raise TypeError("peak_resident_bytes must be a closed limit policy")


class LocalQuantumEspressoResolvedDestinationRole(StrEnum):
    """Closed roles for resolved paths beneath an attempt workspace."""

    EXECUTABLE = "executable"
    INPUT_ARTIFACT = "input_artifact"
    STDOUT = "stdout"
    STDERR = "stderr"
    BEFORE_SNAPSHOT = "before_snapshot"
    AFTER_SNAPSHOT = "after_snapshot"
    TERMINAL_RECORD = "terminal_record"
    WORK = "work"
    RESULT = "result"


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoResolvedDestination:
    """Bind one portable destination to its confined absolute local path.

    Attributes
    ----------
    role
        Closed destination role.
    owner_identity
        Nonempty artifact identity or fixed role identity distinguishing destinations
        of the same role.
    portable_destination
        Original parent-free portable path relative to the attempt workspace.
    absolute_path
        Absolute lexical path beneath the prepared workspace.
    """

    role: LocalQuantumEspressoResolvedDestinationRole
    owner_identity: str
    portable_destination: QuantumEspressoArtifactDestination
    absolute_path: Path

    def __post_init__(self) -> None:
        if type(self.role) is not LocalQuantumEspressoResolvedDestinationRole:
            raise TypeError("role must be LocalQuantumEspressoResolvedDestinationRole")
        if type(self.owner_identity) is not str:
            raise TypeError("owner_identity must be a built-in str")
        if not self.owner_identity:
            raise ValueError("owner_identity must not be empty")
        if type(self.portable_destination) is not QuantumEspressoArtifactDestination:
            raise TypeError(
                "portable_destination must be QuantumEspressoArtifactDestination"
            )
        if not isinstance(self.absolute_path, Path):
            raise TypeError("absolute_path must be pathlib.Path")
        if not self.absolute_path.is_absolute():
            raise ValueError("absolute_path must be absolute")


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoFileSourceObservation:
    """Record exact bytes observed for one local regular-file source.

    Attributes
    ----------
    artifact_identity
        Nominal identity of the bound QE input artifact.
    source
        Absolute nonsymlink source path inspected read-only.
    content_identity
        Observed SHA-256 digest and byte count.
    """

    artifact_identity: ArtifactIdentity
    source: Path
    content_identity: ArtifactContentIdentity

    def __post_init__(self) -> None:
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if not isinstance(self.source, Path):
            raise TypeError("source must be pathlib.Path")
        if not self.source.is_absolute():
            raise ValueError("source must be absolute")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoTreeSourceObservation:
    """Record deterministic identity observations for one predecessor-state tree.

    Attributes
    ----------
    artifact_identity
        Nominal identity of the predecessor-state artifact.
    source
        Absolute nonsymlink source directory inspected read-only.
    manifest_identity
        Integration-local deterministic tree-manifest identity.
    manifest_entry_identities
        Nonempty unique lexical tuple of deterministic directory and file entry
        identities.
    entry_count
        Number of represented descendants, including directories and regular files.
    regular_file_total_bytes
        Sum of regular-file byte counts in the tree.
    """

    artifact_identity: ArtifactIdentity
    source: Path
    manifest_identity: ArtifactManifestIdentity
    manifest_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]
    entry_count: int
    regular_file_total_bytes: int

    def __post_init__(self) -> None:
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if not isinstance(self.source, Path):
            raise TypeError("source must be pathlib.Path")
        if not self.source.is_absolute():
            raise ValueError("source must be absolute")
        if type(self.manifest_identity) is not ArtifactManifestIdentity:
            raise TypeError("manifest_identity must be ArtifactManifestIdentity")
        entries = self.manifest_entry_identities
        if type(entries) is not tuple or any(
            type(value) is not ArtifactManifestEntryIdentity for value in entries
        ):
            raise TypeError(
                "manifest_entry_identities must be a tuple of "
                "ArtifactManifestEntryIdentity"
            )
        if not entries:
            raise ValueError("manifest_entry_identities must not be empty")
        if entries != tuple(sorted(entries, key=lambda value: value.value)) or len(
            set(entries)
        ) != len(entries):
            raise ValueError(
                "manifest_entry_identities must be unique and lexically sorted"
            )
        for name in ("entry_count", "regular_file_total_bytes"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if not 0 <= value <= _MAX_U64:
                raise ValueError(f"{name} must be in the unsigned 64-bit range")
        if self.entry_count != len(entries):
            raise ValueError("entry_count must equal manifest entry count")


type LocalQuantumEspressoArtifactSourceObservation = (
    LocalQuantumEspressoFileSourceObservation
    | LocalQuantumEspressoTreeSourceObservation
)
"""Closed exact source-observation variants."""


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoSupportedExecutableBinding:
    """Declare one exact executable/program/classifier combination supported locally.

    Attributes
    ----------
    executable_configuration_identity
        Exact identity of the admitted executable configuration.
    executable_content_identity
        Exact SHA-256 and byte-count identity of the admitted executable bytes.
    program
        QE program role represented by the native input.
    executable_kind
        Actual QE or deterministic-fixture executable namespace.
    program_version
        Exact nonempty version text.
    classifier_identity
        Exact diagnostic classifier implementation/catalog identity.
    """

    executable_configuration_identity: QuantumEspressoExecutableConfigurationIdentity
    executable_content_identity: ArtifactContentIdentity
    program: QuantumEspressoProgram
    executable_kind: QuantumEspressoExecutableKind
    program_version: str
    classifier_identity: QuantumEspressoDiagnosticClassifierIdentity

    def __post_init__(self) -> None:
        expected = (
            (
                self.executable_configuration_identity,
                QuantumEspressoExecutableConfigurationIdentity,
                "executable_configuration_identity",
            ),
            (
                self.executable_content_identity,
                ArtifactContentIdentity,
                "executable_content_identity",
            ),
            (self.program, QuantumEspressoProgram, "program"),
            (
                self.executable_kind,
                QuantumEspressoExecutableKind,
                "executable_kind",
            ),
            (
                self.classifier_identity,
                QuantumEspressoDiagnosticClassifierIdentity,
                "classifier_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.program_version) is not str:
            raise TypeError("program_version must be a built-in str")
        if not self.program_version:
            raise ValueError("program_version must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQuantumEspressoExecutionPreparationRequest:
    """Supply exact read-only inputs for one local QE preparation operation.

    Attributes
    ----------
    execution_input
        Exact QE operation input and Workflow correlations.
    executable_configuration
        Exact QE program, executable-content, argument, environment, and classifier
        binding.
    executable_path
        Absolute local executable path; shell and ambient ``PATH`` lookup are absent.
    executable_content_identity
        Expected exact executable bytes, repeated explicitly at the local boundary.
    executable_destination
        Parent-free destination for a private staged executable copy. Process entry
        uses this copy rather than the mutable source pathname.
    authorized_run_root
        Absolute existing directory beneath which the absent workspace is authorized.
    attempt_workspace_name
        One parent-free child directory name under ``authorized_run_root``.
    artifact_sources
        Unique lexical tuple binding every exact input artifact to one absolute source.
    limits
        Operational resource ceilings.
    stdout_destination, stderr_destination
        Distinct stream artifact destinations beneath the workspace.
    before_snapshot_destination, after_snapshot_destination
        Distinct deterministic snapshot-record destinations.
    terminal_record_destination
        Atomic terminal-record destination.
    work_destination, result_destination
        Distinct mutable work and collected-result directory destinations.
    simulation_execution_request_identity
        Workflow request identity that a later effect must match.
    scientific_executor_identity
        Explicitly selected concrete executor identity.
    dispatch_destination_identity
        Workflow dispatch destination identity.
    dispatch_resource_scope_identity
        Workflow dispatch resource-scope identity.
    authorization_result_identity
        Exact accepted authorization-result identity to correlate later; preparation
        does not interpret it as authority to execute.
    """

    execution_input: QuantumEspressoExecutionInput
    executable_configuration: QuantumEspressoExecutableConfiguration
    executable_path: Path
    executable_content_identity: ArtifactContentIdentity
    executable_destination: QuantumEspressoArtifactDestination
    authorized_run_root: Path
    attempt_workspace_name: LocalQuantumEspressoAttemptWorkspaceName
    artifact_sources: tuple[LocalQuantumEspressoArtifactSource, ...]
    limits: LocalQuantumEspressoExecutionLimits
    stdout_destination: QuantumEspressoArtifactDestination
    stderr_destination: QuantumEspressoArtifactDestination
    before_snapshot_destination: QuantumEspressoArtifactDestination
    after_snapshot_destination: QuantumEspressoArtifactDestination
    terminal_record_destination: QuantumEspressoArtifactDestination
    work_destination: QuantumEspressoArtifactDestination
    result_destination: QuantumEspressoArtifactDestination
    simulation_execution_request_identity: SimulationExecutionRequestIdentity
    scientific_executor_identity: ScientificExecutorIdentity
    dispatch_destination_identity: DispatchDestinationIdentity
    dispatch_resource_scope_identity: DispatchResourceScopeIdentity
    authorization_result_identity: SimulationExecutionAuthorizationResultIdentity

    def __post_init__(self) -> None:
        expected = (
            (self.execution_input, QuantumEspressoExecutionInput, "execution_input"),
            (
                self.executable_configuration,
                QuantumEspressoExecutableConfiguration,
                "executable_configuration",
            ),
            (
                self.executable_content_identity,
                ArtifactContentIdentity,
                "executable_content_identity",
            ),
            (
                self.attempt_workspace_name,
                LocalQuantumEspressoAttemptWorkspaceName,
                "attempt_workspace_name",
            ),
            (
                self.executable_destination,
                QuantumEspressoArtifactDestination,
                "executable_destination",
            ),
            (self.limits, LocalQuantumEspressoExecutionLimits, "limits"),
            (
                self.simulation_execution_request_identity,
                SimulationExecutionRequestIdentity,
                "simulation_execution_request_identity",
            ),
            (
                self.scientific_executor_identity,
                ScientificExecutorIdentity,
                "scientific_executor_identity",
            ),
            (
                self.dispatch_destination_identity,
                DispatchDestinationIdentity,
                "dispatch_destination_identity",
            ),
            (
                self.dispatch_resource_scope_identity,
                DispatchResourceScopeIdentity,
                "dispatch_resource_scope_identity",
            ),
            (
                self.authorization_result_identity,
                SimulationExecutionAuthorizationResultIdentity,
                "authorization_result_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        for path_value, path_name in (
            (self.executable_path, "executable_path"),
            (self.authorized_run_root, "authorized_run_root"),
        ):
            if not isinstance(path_value, Path):
                raise TypeError(f"{path_name} must be pathlib.Path")
            if not path_value.is_absolute():
                raise ValueError(f"{path_name} must be absolute")
        sources = self.artifact_sources
        if type(sources) is not tuple or any(
            type(value) is not LocalQuantumEspressoArtifactSource for value in sources
        ):
            raise TypeError(
                "artifact_sources must be a tuple of LocalQuantumEspressoArtifactSource"
            )
        if sources != tuple(
            sorted(sources, key=lambda value: value.artifact.identity.value)
        ) or len({value.artifact.identity for value in sources}) != len(sources):
            raise ValueError("artifact_sources must be unique and lexically sorted")
        destinations = (
            (self.stdout_destination, "stdout_destination"),
            (self.stderr_destination, "stderr_destination"),
            (self.before_snapshot_destination, "before_snapshot_destination"),
            (self.after_snapshot_destination, "after_snapshot_destination"),
            (self.terminal_record_destination, "terminal_record_destination"),
            (self.work_destination, "work_destination"),
            (self.result_destination, "result_destination"),
        )
        for destination, name in destinations:
            if type(destination) is not QuantumEspressoArtifactDestination:
                raise TypeError(f"{name} must be QuantumEspressoArtifactDestination")


class LocalQuantumEspressoPreparationFailureCode(StrEnum):
    """Closed read-only preparation failure codes."""

    INVALID_CONFINEMENT = "invalid_confinement"
    UNEXPECTED_SYMLINK_OR_TYPE = "unexpected_symlink_or_type"
    MISSING_SOURCE = "missing_source"
    SOURCE_IDENTITY_MISMATCH = "source_identity_mismatch"
    EXECUTABLE_IDENTITY_MISMATCH = "executable_identity_mismatch"
    EXECUTABLE_NOT_RUNNABLE = "executable_not_runnable"
    EXISTING_WORKSPACE = "existing_workspace"
    INSUFFICIENT_FREE_SPACE = "insufficient_free_space"
    UNSUPPORTED_BINDING = "unsupported_binding"
    RESOURCE_OBSERVATION_FAILED = "resource_observation_failed"


class LocalQuantumEspressoPreparationPhase(StrEnum):
    """Closed phases in which read-only preparation may fail."""

    CONFINEMENT = "confinement"
    COMPATIBILITY = "compatibility"
    EXECUTABLE = "executable"
    INPUT_SOURCE = "input_source"
    RESOURCES = "resources"


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQuantumEspressoPreparationFailure:
    """Represent one fail-closed read-only preparation result.

    Attributes
    ----------
    code
        Stable preparation failure code.
    phase
        Preparation phase that could not establish its required fact.
    execution_input_identity
        Exact QE execution input that was not prepared.
    preparation_implementation_identity
        Exact implementation and algorithm identity that produced this result.
    expected_condition, observed_condition
        Nonempty sanitized descriptions without native bytes or environment values.
    related_identities
        Unique lexical identities relevant to the failure.
    claim_boundary
        Explicit statements limiting interpretation of this result.
    """

    code: LocalQuantumEspressoPreparationFailureCode
    phase: LocalQuantumEspressoPreparationPhase
    execution_input_identity: QuantumEspressoExecutionInputIdentity
    preparation_implementation_identity: (
        LocalQuantumEspressoPreparationImplementationIdentity
    )
    expected_condition: str
    observed_condition: str
    related_identities: tuple[str, ...]
    claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        expected = (
            (self.code, LocalQuantumEspressoPreparationFailureCode, "code"),
            (self.phase, LocalQuantumEspressoPreparationPhase, "phase"),
            (
                self.execution_input_identity,
                QuantumEspressoExecutionInputIdentity,
                "execution_input_identity",
            ),
            (
                self.preparation_implementation_identity,
                LocalQuantumEspressoPreparationImplementationIdentity,
                "preparation_implementation_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        for name in ("expected_condition", "observed_condition"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
        for values, name in (
            (self.related_identities, "related_identities"),
            (self.claim_boundary, "claim_boundary"),
        ):
            if type(values) is not tuple or any(
                type(value) is not str for value in values
            ):
                raise TypeError(f"{name} must be a tuple of built-in str values")
            if not values or any(not value for value in values):
                raise ValueError(f"{name} must contain nonempty strings")
        if self.related_identities != tuple(sorted(set(self.related_identities))):
            raise ValueError("related_identities must be unique and lexically sorted")


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQuantumEspressoPreparedExecution:
    """Represent one successful read-only local execution preparation.

    Attributes
    ----------
    identity
        Deterministic identity of the complete preparation observation.
    request
        Exact immutable request that was prepared.
    preparation_implementation_identity
        Exact preparation algorithm identity.
    workspace
        Absolute root-confined workspace path confirmed absent during preparation.
    argv
        Exact non-shell argument vector beginning with the private staged executable
        destination.
    environment_additions
        Exact canonical allowlisted environment additions from the configuration.
    resolved_destinations
        Canonically ordered portable-to-absolute destination bindings.
    executable_content_identity
        Executable bytes observed during preparation.
    source_observations
        Canonically ordered exact file/tree input-source observations.
    required_free_bytes
        Requested minimum free-space observation in bytes.
    observed_free_bytes
        Free bytes observed at the authorized run root.
    """

    identity: QuantumEspressoPreparationIdentity
    request: LocalQuantumEspressoExecutionPreparationRequest
    preparation_implementation_identity: (
        LocalQuantumEspressoPreparationImplementationIdentity
    )
    workspace: Path
    argv: tuple[str, ...]
    environment_additions: tuple[tuple[str, str], ...]
    resolved_destinations: tuple[LocalQuantumEspressoResolvedDestination, ...]
    executable_content_identity: ArtifactContentIdentity
    source_observations: tuple[LocalQuantumEspressoArtifactSourceObservation, ...]
    required_free_bytes: int
    observed_free_bytes: int

    def __post_init__(self) -> None:
        expected = (
            (self.identity, QuantumEspressoPreparationIdentity, "identity"),
            (
                self.request,
                LocalQuantumEspressoExecutionPreparationRequest,
                "request",
            ),
            (
                self.preparation_implementation_identity,
                LocalQuantumEspressoPreparationImplementationIdentity,
                "preparation_implementation_identity",
            ),
            (
                self.executable_content_identity,
                ArtifactContentIdentity,
                "executable_content_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if not isinstance(self.workspace, Path):
            raise TypeError("workspace must be pathlib.Path")
        if not self.workspace.is_absolute():
            raise ValueError("workspace must be absolute")
        if type(self.argv) is not tuple or any(
            type(value) is not str for value in self.argv
        ):
            raise TypeError("argv must be a tuple of built-in str values")
        if not self.argv or any(not value or "\x00" in value for value in self.argv):
            raise ValueError("argv must contain nonempty NUL-free values")
        additions = self.environment_additions
        if type(additions) is not tuple or any(
            type(value) is not tuple
            or len(value) != 2
            or type(value[0]) is not str
            or type(value[1]) is not str
            for value in additions
        ):
            raise TypeError("environment_additions must contain built-in string pairs")
        destinations = self.resolved_destinations
        if type(destinations) is not tuple or any(
            type(value) is not LocalQuantumEspressoResolvedDestination
            for value in destinations
        ):
            raise TypeError(
                "resolved_destinations must contain "
                "LocalQuantumEspressoResolvedDestination values"
            )
        expected_destinations = tuple(
            sorted(
                destinations,
                key=lambda value: (value.role.value, value.owner_identity),
            )
        )
        if destinations != expected_destinations:
            raise ValueError("resolved_destinations must be canonically ordered")
        observations = self.source_observations
        if type(observations) is not tuple or any(
            type(value)
            not in (
                LocalQuantumEspressoFileSourceObservation,
                LocalQuantumEspressoTreeSourceObservation,
            )
            for value in observations
        ):
            raise TypeError("source_observations must be closed observation variants")
        if observations != tuple(
            sorted(observations, key=lambda value: value.artifact_identity.value)
        ):
            raise ValueError("source_observations must be canonically ordered")
        for name in ("required_free_bytes", "observed_free_bytes"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if not 0 <= value <= _MAX_U64:
                raise ValueError(f"{name} must be in the unsigned 64-bit range")
        if self.observed_free_bytes < self.required_free_bytes:
            raise ValueError("observed_free_bytes must satisfy required_free_bytes")


type LocalQuantumEspressoPreparationResult = (
    LocalQuantumEspressoPreparedExecution | LocalQuantumEspressoPreparationFailure
)
"""Closed read-only local preparation result."""


@dataclass(frozen=True, slots=True)
class LocalQuantumEspressoExecutionPreparer:
    """Prepare one exact local QE execution without mutation or process invocation.

    Parameters
    ----------
    implementation_identity
        Exact preparation implementation and version identity.
    supported_bindings
        Nonempty unique canonical tuple of exact program, executable-kind, version,
        and classifier combinations accepted by this composed preparer.

    Notes
    -----
    The ActionObject observes local filesystem state. A successful result is a
    read-only preparation observation, not an execution grant. Staging must recheck
    source and destination facts before mutation to close time-of-check/time-of-use
    gaps.
    """

    implementation_identity: LocalQuantumEspressoPreparationImplementationIdentity
    supported_bindings: tuple[LocalQuantumEspressoSupportedExecutableBinding, ...]

    def __post_init__(self) -> None:
        if type(self.implementation_identity) is not (
            LocalQuantumEspressoPreparationImplementationIdentity
        ):
            raise TypeError(
                "implementation_identity must be "
                "LocalQuantumEspressoPreparationImplementationIdentity"
            )
        values = self.supported_bindings
        if type(values) is not tuple or any(
            type(value) is not LocalQuantumEspressoSupportedExecutableBinding
            for value in values
        ):
            raise TypeError(
                "supported_bindings must contain "
                "LocalQuantumEspressoSupportedExecutableBinding values"
            )
        if not values:
            raise ValueError("supported_bindings must not be empty")
        expected = tuple(
            sorted(
                values,
                key=lambda value: (
                    value.executable_configuration_identity.value,
                    value.executable_content_identity.algorithm,
                    value.executable_content_identity.digest,
                    value.executable_content_identity.byte_count,
                    value.program.value,
                    value.executable_kind.value,
                    value.program_version,
                    value.classifier_identity.value,
                ),
            )
        )
        if values != expected or len(set(values)) != len(values):
            raise ValueError(
                "supported_bindings must be unique and canonically ordered"
            )

    def execute(
        self,
        request: LocalQuantumEspressoExecutionPreparationRequest,
    ) -> LocalQuantumEspressoPreparationResult:
        """Return a prepared execution or a fail-closed read-only failure.

        Parameters
        ----------
        request
            Exact local preparation request.

        Returns
        -------
        LocalQuantumEspressoPreparationResult
            Successful immutable preparation when every required fact is established;
            otherwise a typed failure. No result authorizes process execution.

        Raises
        ------
        TypeError
            If ``request`` is not exactly a preparation request.
        """
        if type(request) is not LocalQuantumEspressoExecutionPreparationRequest:
            raise TypeError(
                "request must be LocalQuantumEspressoExecutionPreparationRequest"
            )
        compatibility_failure = self._check_compatibility(request)
        if compatibility_failure is not None:
            return compatibility_failure
        confinement = self._resolve_confinement(request)
        if isinstance(confinement, LocalQuantumEspressoPreparationFailure):
            return confinement
        workspace, destinations = confinement
        executable_observation = self._inspect_regular_file(
            request=request,
            source=request.executable_path,
            expected=request.executable_content_identity,
            mismatch_code=(
                LocalQuantumEspressoPreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH
            ),
            phase=LocalQuantumEspressoPreparationPhase.EXECUTABLE,
            related_identity=request.executable_configuration.identity.value,
            require_executable=True,
        )
        if type(executable_observation) is LocalQuantumEspressoPreparationFailure:
            return executable_observation
        if executable_observation != (
            request.executable_configuration.executable_content_identity
        ):
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH,
                LocalQuantumEspressoPreparationPhase.EXECUTABLE,
                "configuration and local-boundary executable identities agree",
                "configuration identity differs from observed executable identity",
                (request.executable_configuration.identity.value,),
            )
        source_observations: list[LocalQuantumEspressoArtifactSourceObservation] = []
        for source in request.artifact_sources:
            observation = self._inspect_artifact_source(request, source)
            if isinstance(observation, LocalQuantumEspressoPreparationFailure):
                return observation
            source_observations.append(observation)
        try:
            free_bytes = shutil.disk_usage(request.authorized_run_root).free
        except OSError:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.RESOURCE_OBSERVATION_FAILED,
                LocalQuantumEspressoPreparationPhase.RESOURCES,
                "free-space observation for the authorized run root",
                "free-space observation failed",
                (request.execution_input.identity.value,),
            )
        if free_bytes < request.limits.minimum_free_bytes:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.INSUFFICIENT_FREE_SPACE,
                LocalQuantumEspressoPreparationPhase.RESOURCES,
                "observed free bytes satisfy the declared minimum",
                "observed free bytes are below the declared minimum",
                (request.execution_input.identity.value,),
            )
        executable_destinations = tuple(
            value
            for value in destinations
            if value.role is LocalQuantumEspressoResolvedDestinationRole.EXECUTABLE
        )
        if len(executable_destinations) != 1:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.INVALID_CONFINEMENT,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "one exact staged executable destination",
                "staged executable destination is not unique",
                (request.executable_configuration.identity.value,),
            )
        argv = (
            str(executable_destinations[0].absolute_path),
            *request.executable_configuration.argument_suffix,
        )
        preparation_identity = QuantumEspressoPreparationIdentity(
            "qe-local-preparation-v1:"
            + self._framed_digest(
                (
                    self.implementation_identity.value,
                    request.execution_input.identity.value,
                    request.executable_configuration.identity.value,
                    str(workspace),
                    *argv,
                    *(
                        f"{value.artifact_identity.value}:"
                        f"{self._source_observation_identity(value)}"
                        for value in source_observations
                    ),
                    *(
                        f"{value.role.value}:{value.portable_destination.value}"
                        for value in destinations
                    ),
                    str(free_bytes),
                )
            )
        )
        return LocalQuantumEspressoPreparedExecution(
            identity=preparation_identity,
            request=request,
            preparation_implementation_identity=self.implementation_identity,
            workspace=workspace,
            argv=argv,
            environment_additions=request.executable_configuration.environment_additions,
            resolved_destinations=destinations,
            executable_content_identity=executable_observation,
            source_observations=tuple(source_observations),
            required_free_bytes=request.limits.minimum_free_bytes,
            observed_free_bytes=free_bytes,
        )

    def render_dry_run(self, prepared: LocalQuantumEspressoPreparedExecution) -> str:
        """Render a deterministic sanitized dry-run description.

        Parameters
        ----------
        prepared
            Successful read-only preparation result.

        Returns
        -------
        str
            Line-oriented description ending with one newline. Environment values and
            native file bytes are omitted.

        Raises
        ------
        TypeError
            If ``prepared`` is not exactly a prepared execution.
        """
        if type(prepared) is not LocalQuantumEspressoPreparedExecution:
            raise TypeError("prepared must be LocalQuantumEspressoPreparedExecution")
        lines = [
            f"preparation_identity={prepared.identity.value}",
            f"execution_input_identity={prepared.request.execution_input.identity.value}",
            f"workspace={prepared.workspace}",
        ]
        lines.extend(
            f"argv[{index}]={value}" for index, value in enumerate(prepared.argv)
        )
        lines.extend(
            f"environment_key[{index}]={key}"
            for index, (key, _value) in enumerate(prepared.environment_additions)
        )
        lines.extend(
            "destination["
            f"{value.role.value}:{value.owner_identity}]="
            f"{value.portable_destination.value}"
            for value in prepared.resolved_destinations
        )
        lines.extend(
            f"source[{value.artifact_identity.value}]="
            f"{self._source_observation_identity(value)}"
            for value in prepared.source_observations
        )
        lines.extend(
            (
                f"required_free_bytes={prepared.required_free_bytes}",
                f"observed_free_bytes={prepared.observed_free_bytes}",
                "effect=not_performed",
            )
        )
        return "\n".join(lines) + "\n"

    def _check_compatibility(
        self,
        request: LocalQuantumEspressoExecutionPreparationRequest,
    ) -> LocalQuantumEspressoPreparationFailure | None:
        configuration = request.executable_configuration
        if request.execution_input.program is not configuration.program:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNSUPPORTED_BINDING,
                LocalQuantumEspressoPreparationPhase.COMPATIBILITY,
                "execution input and executable configuration use one program role",
                "program roles differ",
                (
                    request.execution_input.identity.value,
                    configuration.identity.value,
                ),
            )
        binding = LocalQuantumEspressoSupportedExecutableBinding(
            executable_configuration_identity=configuration.identity,
            executable_content_identity=configuration.executable_content_identity,
            program=configuration.program,
            executable_kind=configuration.executable_kind,
            program_version=configuration.program_version,
            classifier_identity=configuration.classifier_identity,
        )
        if binding not in self.supported_bindings:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNSUPPORTED_BINDING,
                LocalQuantumEspressoPreparationPhase.COMPATIBILITY,
                "an explicitly supported program/version/classifier binding",
                "binding is not supported by this preparer",
                (configuration.identity.value,),
            )
        return None

    def _resolve_confinement(
        self,
        request: LocalQuantumEspressoExecutionPreparationRequest,
    ) -> (
        tuple[Path, tuple[LocalQuantumEspressoResolvedDestination, ...]]
        | LocalQuantumEspressoPreparationFailure
    ):
        root = request.authorized_run_root
        if not root.exists():
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.MISSING_SOURCE,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "an existing authorized run root",
                "authorized run root is missing",
                (request.execution_input.identity.value,),
            )
        if self._path_has_symlink(root) or not root.is_dir():
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "a nonsymlink authorized run-root directory",
                "authorized run root has an unsupported type or symlink",
                (request.execution_input.identity.value,),
            )
        try:
            resolved_root = root.resolve(strict=True)
        except OSError:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.INVALID_CONFINEMENT,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "a resolvable authorized run root",
                "authorized run root cannot be resolved",
                (request.execution_input.identity.value,),
            )
        if resolved_root != root:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.INVALID_CONFINEMENT,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "an already canonical authorized run root",
                "authorized run root differs from its canonical path",
                (request.execution_input.identity.value,),
            )
        workspace = root / request.attempt_workspace_name.value
        if workspace.exists() or workspace.is_symlink():
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.EXISTING_WORKSPACE,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "an absent attempt workspace",
                "attempt workspace already exists",
                (request.execution_input.identity.value,),
            )
        role_destinations = (
            (
                LocalQuantumEspressoResolvedDestinationRole.EXECUTABLE,
                request.executable_configuration.identity.value,
                request.executable_destination,
            ),
            (
                LocalQuantumEspressoResolvedDestinationRole.STDOUT,
                "stdout",
                request.stdout_destination,
            ),
            (
                LocalQuantumEspressoResolvedDestinationRole.STDERR,
                "stderr",
                request.stderr_destination,
            ),
            (
                LocalQuantumEspressoResolvedDestinationRole.BEFORE_SNAPSHOT,
                "before_snapshot",
                request.before_snapshot_destination,
            ),
            (
                LocalQuantumEspressoResolvedDestinationRole.AFTER_SNAPSHOT,
                "after_snapshot",
                request.after_snapshot_destination,
            ),
            (
                LocalQuantumEspressoResolvedDestinationRole.TERMINAL_RECORD,
                "terminal_record",
                request.terminal_record_destination,
            ),
            (
                LocalQuantumEspressoResolvedDestinationRole.WORK,
                "work",
                request.work_destination,
            ),
            (
                LocalQuantumEspressoResolvedDestinationRole.RESULT,
                "result",
                request.result_destination,
            ),
        )
        raw_destinations: list[
            tuple[
                LocalQuantumEspressoResolvedDestinationRole,
                str,
                QuantumEspressoArtifactDestination,
            ]
        ] = list(role_destinations)
        raw_destinations.extend(
            (
                LocalQuantumEspressoResolvedDestinationRole.INPUT_ARTIFACT,
                source.artifact.identity.value,
                source.artifact.destination,
            )
            for source in request.artifact_sources
        )
        portable_values = tuple(value.value for _, _, value in raw_destinations)
        if len(set(portable_values)) != len(portable_values):
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.INVALID_CONFINEMENT,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "unique workspace-relative destinations",
                "two or more destinations are equal",
                (request.execution_input.identity.value,),
            )
        resolved: list[LocalQuantumEspressoResolvedDestination] = []
        for role, owner_identity, portable in raw_destinations:
            absolute = workspace.joinpath(*PurePosixPath(portable.value).parts)
            try:
                common = Path(os.path.commonpath((workspace, absolute)))
            except ValueError:
                return self._failure(
                    request,
                    LocalQuantumEspressoPreparationFailureCode.INVALID_CONFINEMENT,
                    LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                    "every destination confined beneath the attempt workspace",
                    "destination confinement comparison failed",
                    (owner_identity,),
                )
            if common != workspace:
                return self._failure(
                    request,
                    LocalQuantumEspressoPreparationFailureCode.INVALID_CONFINEMENT,
                    LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                    "every destination confined beneath the attempt workspace",
                    "destination escapes the attempt workspace",
                    (owner_identity,),
                )
            resolved.append(
                LocalQuantumEspressoResolvedDestination(
                    role=role,
                    owner_identity=owner_identity,
                    portable_destination=portable,
                    absolute_path=absolute,
                )
            )
        expected_artifacts = self._input_artifacts(request.execution_input)
        source_artifacts = tuple(value.artifact for value in request.artifact_sources)
        if len(expected_artifacts) != len(source_artifacts) or any(
            source.artifact != expected
            for source, expected in zip(
                request.artifact_sources,
                sorted(expected_artifacts, key=lambda value: value.identity.value),
                strict=True,
            )
        ):
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.INVALID_CONFINEMENT,
                LocalQuantumEspressoPreparationPhase.CONFINEMENT,
                "exactly one source binding for every execution-input artifact",
                "artifact-source bindings do not equal the execution input",
                (request.execution_input.identity.value,),
            )
        return workspace, tuple(
            sorted(resolved, key=lambda value: (value.role.value, value.owner_identity))
        )

    def _inspect_artifact_source(
        self,
        request: LocalQuantumEspressoExecutionPreparationRequest,
        source: LocalQuantumEspressoArtifactSource,
    ) -> (
        LocalQuantumEspressoArtifactSourceObservation
        | LocalQuantumEspressoPreparationFailure
    ):
        artifact = source.artifact
        if type(artifact) in (
            QuantumEspressoNativeInputArtifact,
            QuantumEspressoPseudopotentialArtifact,
        ):
            assert type(artifact.content) is QuantumEspressoFileArtifactContent
            observation = self._inspect_regular_file(
                request=request,
                source=source.source,
                expected=artifact.content.content_identity,
                mismatch_code=(
                    LocalQuantumEspressoPreparationFailureCode.SOURCE_IDENTITY_MISMATCH
                ),
                phase=LocalQuantumEspressoPreparationPhase.INPUT_SOURCE,
                related_identity=artifact.identity.value,
                require_executable=False,
            )
            if isinstance(observation, LocalQuantumEspressoPreparationFailure):
                return observation
            return LocalQuantumEspressoFileSourceObservation(
                artifact_identity=artifact.identity,
                source=source.source,
                content_identity=observation,
            )
        assert type(artifact) is QuantumEspressoPredecessorNativeStateArtifact
        return self._inspect_tree_source(request, source.source, artifact)

    def _inspect_regular_file(
        self,
        *,
        request: LocalQuantumEspressoExecutionPreparationRequest,
        source: Path,
        expected: ArtifactContentIdentity,
        mismatch_code: LocalQuantumEspressoPreparationFailureCode,
        phase: LocalQuantumEspressoPreparationPhase,
        related_identity: str,
        require_executable: bool,
    ) -> ArtifactContentIdentity | LocalQuantumEspressoPreparationFailure:
        if not source.exists():
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.MISSING_SOURCE,
                phase,
                "an existing nonsymlink regular file",
                "source is missing",
                (related_identity,),
            )
        if self._path_has_symlink(source):
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                phase,
                "a nonsymlink regular file",
                "source path contains a symlink",
                (related_identity,),
            )
        try:
            mode = source.stat(follow_symlinks=False).st_mode
        except OSError:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                phase,
                "an inspectable nonsymlink regular file",
                "source type observation failed",
                (related_identity,),
            )
        if not stat.S_ISREG(mode):
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                phase,
                "a nonsymlink regular file",
                "source is not a regular file",
                (related_identity,),
            )
        if require_executable and not os.access(source, os.X_OK):
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.EXECUTABLE_NOT_RUNNABLE,
                phase,
                "an executable regular file",
                "executable permission is absent",
                (related_identity,),
            )
        try:
            observed = self._file_content_identity(source)
        except OSError:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                phase,
                "a completely readable stable regular file",
                "source byte observation failed",
                (related_identity,),
            )
        if observed != expected:
            return self._failure(
                request,
                mismatch_code,
                phase,
                "observed SHA-256 and byte count equal the declared identity",
                "observed content identity differs from the declared identity",
                (related_identity,),
            )
        return observed

    def _inspect_tree_source(
        self,
        request: LocalQuantumEspressoExecutionPreparationRequest,
        source: Path,
        artifact: QuantumEspressoPredecessorNativeStateArtifact,
    ) -> (
        LocalQuantumEspressoTreeSourceObservation
        | LocalQuantumEspressoPreparationFailure
    ):
        if not source.exists():
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.MISSING_SOURCE,
                LocalQuantumEspressoPreparationPhase.INPUT_SOURCE,
                "an existing nonsymlink predecessor-state directory",
                "source tree is missing",
                (artifact.identity.value,),
            )
        if self._path_has_symlink(source) or not source.is_dir():
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                LocalQuantumEspressoPreparationPhase.INPUT_SOURCE,
                "a nonsymlink directory tree of directories and regular files",
                "source tree has an unsupported root type or symlink",
                (artifact.identity.value,),
            )
        try:
            entries, total_bytes = self._tree_entry_identities(source)
        except OSError:
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                LocalQuantumEspressoPreparationPhase.INPUT_SOURCE,
                "a readable nonsymlink tree containing only directories and files",
                "tree observation failed or encountered an unsupported entry",
                (artifact.identity.value,),
            )
        manifest = ArtifactManifestIdentity(
            "qe-tree-manifest-v1:"
            + self._framed_digest(tuple(value.value for value in entries))
        )
        expected = artifact.content
        if (
            entries != expected.manifest_entry_identities
            or manifest != expected.manifest_identity
        ):
            return self._failure(
                request,
                LocalQuantumEspressoPreparationFailureCode.SOURCE_IDENTITY_MISMATCH,
                LocalQuantumEspressoPreparationPhase.INPUT_SOURCE,
                "observed tree manifest and entries equal declared identities",
                "observed tree identity differs from the declared identity",
                (artifact.identity.value,),
            )
        return LocalQuantumEspressoTreeSourceObservation(
            artifact_identity=artifact.identity,
            source=source,
            manifest_identity=manifest,
            manifest_entry_identities=entries,
            entry_count=len(entries),
            regular_file_total_bytes=total_bytes,
        )

    @classmethod
    def _tree_entry_identities(
        cls,
        root: Path,
    ) -> tuple[tuple[ArtifactManifestEntryIdentity, ...], int]:
        pending = [root]
        identities: list[ArtifactManifestEntryIdentity] = []
        total_bytes = 0
        while pending:
            directory = pending.pop()
            children = sorted(directory.iterdir(), key=lambda value: value.name)
            for child in children:
                if child.is_symlink():
                    raise OSError("symlink entry is unsupported")
                relative = child.relative_to(root).as_posix()
                metadata = child.stat(follow_symlinks=False)
                if stat.S_ISDIR(metadata.st_mode):
                    entry_digest = cls._framed_digest(("directory", relative))
                    identities.append(
                        ArtifactManifestEntryIdentity(
                            "qe-tree-entry-v1:" + entry_digest
                        )
                    )
                    pending.append(child)
                elif stat.S_ISREG(metadata.st_mode):
                    content = cls._file_content_identity(child)
                    entry_digest = cls._framed_digest(
                        (
                            "regular_file",
                            relative,
                            content.algorithm,
                            content.digest,
                            str(content.byte_count),
                        )
                    )
                    identities.append(
                        ArtifactManifestEntryIdentity(
                            "qe-tree-entry-v1:" + entry_digest
                        )
                    )
                    total_bytes += content.byte_count
                    if total_bytes > _MAX_U64:
                        raise OSError("tree byte count exceeds u64")
                else:
                    raise OSError("unsupported tree entry type")
        return tuple(sorted(identities, key=lambda value: value.value)), total_bytes

    @staticmethod
    def _file_content_identity(path: Path) -> ArtifactContentIdentity:
        digest = hashlib.sha256()
        byte_count = 0
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(path, flags)
        try:
            before = os.fstat(descriptor)
            if not stat.S_ISREG(before.st_mode):
                raise OSError("source is not a regular file")
            while True:
                block = os.read(descriptor, 1024 * 1024)
                if not block:
                    break
                digest.update(block)
                byte_count += len(block)
                if byte_count > _MAX_U64:
                    raise OSError("file byte count exceeds u64")
            after = os.fstat(descriptor)
            if (
                before.st_dev,
                before.st_ino,
                before.st_size,
                before.st_mtime_ns,
            ) != (
                after.st_dev,
                after.st_ino,
                after.st_size,
                after.st_mtime_ns,
            ):
                raise OSError("source changed during observation")
        finally:
            os.close(descriptor)
        return ArtifactContentIdentity("sha256", digest.hexdigest(), byte_count)

    @staticmethod
    def _path_has_symlink(path: Path) -> bool:
        current = Path(path.anchor)
        for part in path.parts[1:]:
            current /= part
            try:
                if current.is_symlink():
                    return True
            except OSError:
                return True
        return False

    @staticmethod
    def _input_artifacts(
        execution_input: QuantumEspressoExecutionInput,
    ) -> tuple[QuantumEspressoInputArtifact, ...]:
        return (
            execution_input.native_input,
            *execution_input.pseudopotentials,
            *execution_input.predecessor_native_state,
        )

    @staticmethod
    def _framed_digest(values: tuple[str, ...]) -> str:
        digest = hashlib.sha256()
        for value in values:
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, byteorder="big", signed=False))
            digest.update(encoded)
        return digest.hexdigest()

    @staticmethod
    def _source_observation_identity(
        observation: LocalQuantumEspressoArtifactSourceObservation,
    ) -> str:
        if type(observation) is LocalQuantumEspressoFileSourceObservation:
            return (
                f"{observation.content_identity.algorithm}:"
                f"{observation.content_identity.digest}:"
                f"{observation.content_identity.byte_count}"
            )
        assert type(observation) is LocalQuantumEspressoTreeSourceObservation
        return observation.manifest_identity.value

    def _failure(
        self,
        request: LocalQuantumEspressoExecutionPreparationRequest,
        code: LocalQuantumEspressoPreparationFailureCode,
        phase: LocalQuantumEspressoPreparationPhase,
        expected_condition: str,
        observed_condition: str,
        related_identities: tuple[str, ...],
    ) -> LocalQuantumEspressoPreparationFailure:
        return LocalQuantumEspressoPreparationFailure(
            code=code,
            phase=phase,
            execution_input_identity=request.execution_input.identity,
            preparation_implementation_identity=self.implementation_identity,
            expected_condition=expected_condition,
            observed_condition=observed_condition,
            related_identities=tuple(sorted(set(related_identities))),
            claim_boundary=_PREPARATION_CLAIM_BOUNDARY,
        )
