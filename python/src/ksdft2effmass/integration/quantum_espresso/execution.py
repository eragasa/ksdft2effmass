"""Root-confined local preparation for Quantum ESPRESSO execution.

This module implements the read-only preparation stage of the local Quantum ESPRESSO
integration. Preparation validates exact executable, external-resource, and
predecessor-state identities, checks path confinement and operational limits, and
returns an immutable dry-run-ready result. Provider-owned native-input bytes require
no local source path. Preparation creates no workspace, stages no artifact, opens no
output stream, and invokes no process.

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
from pathlib import Path, PurePosixPath

from projectkoios.simulations.calculator.input import (
    CalculatorExternalInputRequirement,
)
from projectkoios.simulations.execution import (
    CalculatorExecutablePreparationFailure,
    CalculatorExecutablePreparationFailureCode,
    CalculatorExecutablePreparer,
    CalculatorPreparedExecutable,
)

from ksdft2effmass.serialization import StrWireEnum
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

from .calculator_input import (
    QeCalculatorInputBinding,
    QeExternalInputResourceBinding,
)
from .contracts import (
    QeArtifactDestination,
    QeDiagnosticClassifierIdentity,
    QeExecutableConfiguration,
    QeExecutableConfigurationIdentity,
    QeExecutableKind,
    QeExecutionInput,
    QeExecutionInputIdentity,
    QeNativeInputArtifact,
    QePredecessorNativeStateArtifact,
    QePreparationIdentity,
    QeProgram,
)
from .executable_binding import QeExecutableBindingAdapter

_MAX_U64 = 18_446_744_073_709_551_615
_PREPARATION_CLAIM_BOUNDARY = (
    "read-only local path and identity preparation only",
    "no workspace creation or artifact staging",
    "no process invocation or execution authority",
    "no Quantum ESPRESSO compatibility claim",
    "no numerical or scientific validation",
)


@dataclass(frozen=True, slots=True)
class LocalQePreparationImplementationIdentity:
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
class LocalQeAttemptWorkspaceName:
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
class LocalQeArtifactSource:
    """Bind one admitted external artifact identity to an absolute local source.

    Attributes
    ----------
    artifact_identity
        Exact KSD Workflow-facing artifact identity. Provider external requirements or
        KSD predecessor records own content and deployment metadata separately.
    source
        Absolute local path. Preparation requires a nonsymlink regular file for a
        provider external input or a nonsymlink directory tree for predecessor state.

    Notes
    -----
    The source binding copies no provider filename, byte count, SHA-256, format,
    provenance, stable identity, or element metadata.
    """

    artifact_identity: ArtifactIdentity
    source: Path

    def __post_init__(self) -> None:
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if not isinstance(self.source, Path):
            raise TypeError("source must be pathlib.Path")
        if not self.source.is_absolute():
            raise ValueError("source must be absolute")


@dataclass(frozen=True, slots=True)
class LocalQePeakResidentBytesUnlimited:
    """Represent absence of a peak resident-memory ceiling.

    Attributes
    ----------
    None
        This marker has no fields and requests no finite peak-RSS ceiling.
    """


@dataclass(frozen=True, slots=True)
class LocalQePeakResidentBytesLimit:
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


type LocalQePeakResidentBytesPolicy = (
    LocalQePeakResidentBytesUnlimited | LocalQePeakResidentBytesLimit
)
"""Closed present/absent peak resident-memory limit."""


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQeExecutionLimits:
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
    peak_resident_bytes: LocalQePeakResidentBytesPolicy

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
            LocalQePeakResidentBytesUnlimited,
            LocalQePeakResidentBytesLimit,
        ):
            raise TypeError("peak_resident_bytes must be a closed limit policy")


class LocalQeResolvedDestinationRole(StrWireEnum):
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
class LocalQeResolvedDestination:
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

    role: LocalQeResolvedDestinationRole
    owner_identity: str
    portable_destination: QeArtifactDestination
    absolute_path: Path

    def __post_init__(self) -> None:
        if type(self.role) is not LocalQeResolvedDestinationRole:
            raise TypeError("role must be LocalQeResolvedDestinationRole")
        if type(self.owner_identity) is not str:
            raise TypeError("owner_identity must be a built-in str")
        if not self.owner_identity:
            raise ValueError("owner_identity must not be empty")
        if type(self.portable_destination) is not QeArtifactDestination:
            raise TypeError("portable_destination must be QeArtifactDestination")
        if not isinstance(self.absolute_path, Path):
            raise TypeError("absolute_path must be pathlib.Path")
        if not self.absolute_path.is_absolute():
            raise ValueError("absolute_path must be absolute")


@dataclass(frozen=True, slots=True)
class LocalQeExecutionRecordDestination:
    """Own the confined destination of one provider execution record.

    Parameters
    ----------
    portable_destination
        Parent-free path relative to the prepared attempt workspace.
    absolute_path
        Exact absolute lexical path confined beneath that workspace.
    """

    portable_destination: QeArtifactDestination
    absolute_path: Path

    def __post_init__(self) -> None:
        if type(self.portable_destination) is not QeArtifactDestination:
            raise TypeError("portable_destination must be QeArtifactDestination")
        if not isinstance(self.absolute_path, Path):
            raise TypeError("absolute_path must be pathlib.Path")
        if not self.absolute_path.is_absolute():
            raise ValueError("absolute_path must be absolute")


@dataclass(frozen=True, slots=True)
class LocalQeFileSourceObservation:
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
class LocalQeTreeSourceObservation:
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


type LocalQeArtifactSourceObservation = (
    LocalQeFileSourceObservation | LocalQeTreeSourceObservation
)
"""Closed exact source-observation variants."""


@dataclass(frozen=True, slots=True)
class LocalQeSupportedExecutableBinding:
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

    executable_configuration_identity: QeExecutableConfigurationIdentity
    executable_content_identity: ArtifactContentIdentity
    program: QeProgram
    executable_kind: QeExecutableKind
    program_version: str
    classifier_identity: QeDiagnosticClassifierIdentity

    def __post_init__(self) -> None:
        expected = (
            (
                self.executable_configuration_identity,
                QeExecutableConfigurationIdentity,
                "executable_configuration_identity",
            ),
            (
                self.executable_content_identity,
                ArtifactContentIdentity,
                "executable_content_identity",
            ),
            (self.program, QeProgram, "program"),
            (
                self.executable_kind,
                QeExecutableKind,
                "executable_kind",
            ),
            (
                self.classifier_identity,
                QeDiagnosticClassifierIdentity,
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
class LocalQeExecutionPreparationRequest:
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
    external_artifact_sources
        Unique lexical tuple binding every pseudopotential and predecessor-state
        artifact to one absolute source. Native input has no local source binding.
    limits
        Operational resource ceilings.
    stdout_destination, stderr_destination
        Distinct stream artifact destinations beneath the workspace.
    before_snapshot_destination, after_snapshot_destination
        Distinct deterministic snapshot-record destinations.
    execution_record_destination
        Provider-owned canonical execution-record destination.
    terminal_record_destination
        Atomic KSD terminal-record destination.
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

    execution_input: QeExecutionInput
    executable_configuration: QeExecutableConfiguration
    executable_path: Path
    executable_content_identity: ArtifactContentIdentity
    executable_destination: QeArtifactDestination
    authorized_run_root: Path
    attempt_workspace_name: LocalQeAttemptWorkspaceName
    external_artifact_sources: tuple[LocalQeArtifactSource, ...]
    limits: LocalQeExecutionLimits
    stdout_destination: QeArtifactDestination
    stderr_destination: QeArtifactDestination
    before_snapshot_destination: QeArtifactDestination
    after_snapshot_destination: QeArtifactDestination
    execution_record_destination: QeArtifactDestination
    terminal_record_destination: QeArtifactDestination
    work_destination: QeArtifactDestination
    result_destination: QeArtifactDestination
    simulation_execution_request_identity: SimulationExecutionRequestIdentity
    scientific_executor_identity: ScientificExecutorIdentity
    dispatch_destination_identity: DispatchDestinationIdentity
    dispatch_resource_scope_identity: DispatchResourceScopeIdentity
    authorization_result_identity: SimulationExecutionAuthorizationResultIdentity

    def __post_init__(self) -> None:
        expected = (
            (self.execution_input, QeExecutionInput, "execution_input"),
            (
                self.executable_configuration,
                QeExecutableConfiguration,
                "executable_configuration",
            ),
            (
                self.executable_content_identity,
                ArtifactContentIdentity,
                "executable_content_identity",
            ),
            (
                self.attempt_workspace_name,
                LocalQeAttemptWorkspaceName,
                "attempt_workspace_name",
            ),
            (
                self.executable_destination,
                QeArtifactDestination,
                "executable_destination",
            ),
            (self.limits, LocalQeExecutionLimits, "limits"),
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
        sources: tuple[LocalQeArtifactSource, ...] = self.external_artifact_sources
        if type(sources) is not tuple or any(
            type(value) is not LocalQeArtifactSource for value in sources
        ):
            raise TypeError(
                "external_artifact_sources must be a tuple of LocalQeArtifactSource"
            )
        if sources != tuple(
            sorted(sources, key=lambda value: value.artifact_identity.value)
        ) or len({value.artifact_identity for value in sources}) != len(sources):
            raise ValueError(
                "external_artifact_sources must be unique and lexically sorted"
            )
        destinations = (
            (self.stdout_destination, "stdout_destination"),
            (self.stderr_destination, "stderr_destination"),
            (self.before_snapshot_destination, "before_snapshot_destination"),
            (self.after_snapshot_destination, "after_snapshot_destination"),
            (self.execution_record_destination, "execution_record_destination"),
            (self.terminal_record_destination, "terminal_record_destination"),
            (self.work_destination, "work_destination"),
            (self.result_destination, "result_destination"),
        )
        for destination, name in destinations:
            if type(destination) is not QeArtifactDestination:
                raise TypeError(f"{name} must be QeArtifactDestination")


class LocalQePreparationFailureCode(StrWireEnum):
    """Closed read-only preparation failure codes."""

    INVALID_CONFINEMENT = "invalid_confinement"
    UNEXPECTED_SYMLINK_OR_TYPE = "unexpected_symlink_or_type"
    MISSING_SOURCE = "missing_source"
    INPUT_BINDING_MISMATCH = "input_binding_mismatch"
    SOURCE_IDENTITY_MISMATCH = "source_identity_mismatch"
    EXECUTABLE_IDENTITY_MISMATCH = "executable_identity_mismatch"
    EXECUTABLE_NOT_RUNNABLE = "executable_not_runnable"
    EXISTING_WORKSPACE = "existing_workspace"
    INSUFFICIENT_FREE_SPACE = "insufficient_free_space"
    UNSUPPORTED_BINDING = "unsupported_binding"
    RESOURCE_OBSERVATION_FAILED = "resource_observation_failed"
    EXECUTABLE_OBSERVATION_FAILED = "executable_observation_failed"


class LocalQePreparationPhase(StrWireEnum):
    """Closed phases in which read-only preparation may fail."""

    CONFINEMENT = "confinement"
    COMPATIBILITY = "compatibility"
    EXECUTABLE = "executable"
    INPUT_SOURCE = "input_source"
    RESOURCES = "resources"


@dataclass(frozen=True, slots=True, kw_only=True)
class LocalQePreparationFailure:
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

    code: LocalQePreparationFailureCode
    phase: LocalQePreparationPhase
    execution_input_identity: QeExecutionInputIdentity
    preparation_implementation_identity: LocalQePreparationImplementationIdentity
    expected_condition: str
    observed_condition: str
    related_identities: tuple[str, ...]
    claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        expected = (
            (self.code, LocalQePreparationFailureCode, "code"),
            (self.phase, LocalQePreparationPhase, "phase"),
            (
                self.execution_input_identity,
                QeExecutionInputIdentity,
                "execution_input_identity",
            ),
            (
                self.preparation_implementation_identity,
                LocalQePreparationImplementationIdentity,
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
class LocalQePreparedExecution:
    """Represent one successful read-only local execution preparation.

    Attributes
    ----------
    identity
        Deterministic identity of the complete preparation observation.
    request
        Exact immutable request that was prepared.
    calculator_input_binding
        Exact admitted provider-input and KSD correlation binding whose primary bytes
        and external requirements govern preparation.
    preparation_implementation_identity
        Exact preparation algorithm identity.
    workspace
        Absolute root-confined workspace path confirmed absent during preparation.
    argv
        Exact non-shell argument vector beginning with the private staged executable
        destination.
    environment_additions
        Exact canonical allowlisted environment additions from the configuration.
    execution_record_destination
        Exact object-owned provider execution-record destination.
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

    identity: QePreparationIdentity
    request: LocalQeExecutionPreparationRequest
    calculator_input_binding: QeCalculatorInputBinding
    preparation_implementation_identity: LocalQePreparationImplementationIdentity
    workspace: Path
    argv: tuple[str, ...]
    environment_additions: tuple[tuple[str, str], ...]
    execution_record_destination: LocalQeExecutionRecordDestination
    resolved_destinations: tuple[LocalQeResolvedDestination, ...]
    executable_content_identity: ArtifactContentIdentity
    source_observations: tuple[LocalQeArtifactSourceObservation, ...]
    required_free_bytes: int
    observed_free_bytes: int

    def __post_init__(self) -> None:
        expected = (
            (self.identity, QePreparationIdentity, "identity"),
            (
                self.request,
                LocalQeExecutionPreparationRequest,
                "request",
            ),
            (
                self.calculator_input_binding,
                QeCalculatorInputBinding,
                "calculator_input_binding",
            ),
            (
                self.preparation_implementation_identity,
                LocalQePreparationImplementationIdentity,
                "preparation_implementation_identity",
            ),
            (
                self.execution_record_destination,
                LocalQeExecutionRecordDestination,
                "execution_record_destination",
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
        if self.calculator_input_binding.execution_input is not (
            self.request.execution_input
        ):
            raise ValueError(
                "calculator_input_binding must retain the prepared execution input"
            )
        if not isinstance(self.workspace, Path):
            raise TypeError("workspace must be pathlib.Path")
        if not self.workspace.is_absolute():
            raise ValueError("workspace must be absolute")
        if (
            self.execution_record_destination.portable_destination
            != self.request.execution_record_destination
            or not self.execution_record_destination.absolute_path.is_relative_to(
                self.workspace
            )
        ):
            raise ValueError(
                "execution_record_destination must match and remain beneath workspace"
            )
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
            type(value) is not LocalQeResolvedDestination for value in destinations
        ):
            raise TypeError(
                "resolved_destinations must contain LocalQeResolvedDestination values"
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
                LocalQeFileSourceObservation,
                LocalQeTreeSourceObservation,
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


type LocalQePreparationResult = LocalQePreparedExecution | LocalQePreparationFailure
"""Closed read-only local preparation result."""


@dataclass(frozen=True, slots=True)
class LocalQeExecutionPreparer:
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

    implementation_identity: LocalQePreparationImplementationIdentity
    supported_bindings: tuple[LocalQeSupportedExecutableBinding, ...]

    def __post_init__(self) -> None:
        if type(self.implementation_identity) is not (
            LocalQePreparationImplementationIdentity
        ):
            raise TypeError(
                "implementation_identity must be "
                "LocalQePreparationImplementationIdentity"
            )
        values = self.supported_bindings
        if type(values) is not tuple or any(
            type(value) is not LocalQeSupportedExecutableBinding for value in values
        ):
            raise TypeError(
                "supported_bindings must contain "
                "LocalQeSupportedExecutableBinding values"
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
        request: LocalQeExecutionPreparationRequest,
        calculator_input_binding: QeCalculatorInputBinding,
    ) -> LocalQePreparationResult:
        """Return a prepared execution or a fail-closed read-only failure.

        Parameters
        ----------
        request
            Exact local preparation request.
        calculator_input_binding
            Exact admitted provider-input binding. Provider primary bytes and external
            requirements remain authoritative for input content identities.

        Returns
        -------
        LocalQePreparationResult
            Successful immutable preparation when every required fact is established;
            otherwise a typed failure. No result authorizes process execution.

        Raises
        ------
        TypeError
            If ``request`` is not exactly a preparation request.
        """
        if type(request) is not LocalQeExecutionPreparationRequest:
            raise TypeError("request must be LocalQeExecutionPreparationRequest")
        if type(calculator_input_binding) is not QeCalculatorInputBinding:
            raise TypeError("calculator_input_binding must be QeCalculatorInputBinding")
        if calculator_input_binding.execution_input is not request.execution_input:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INPUT_BINDING_MISMATCH,
                LocalQePreparationPhase.INPUT_SOURCE,
                "provider input binding retains the exact execution input",
                "provider input binding retains a different execution input",
                (request.execution_input.identity.value,),
            )
        compatibility_failure = self._check_compatibility(request)
        if compatibility_failure is not None:
            return compatibility_failure
        confinement = self._resolve_confinement(request, calculator_input_binding)
        if isinstance(confinement, LocalQePreparationFailure):
            return confinement
        workspace, destinations, execution_record_destination = confinement
        executable_observation = self._inspect_executable(request)
        if type(executable_observation) is LocalQePreparationFailure:
            return executable_observation
        assert type(executable_observation) is ArtifactContentIdentity
        source_observations: list[LocalQeArtifactSourceObservation] = []
        for source in request.external_artifact_sources:
            observation = self._inspect_artifact_source(
                request, calculator_input_binding, source
            )
            if isinstance(observation, LocalQePreparationFailure):
                return observation
            source_observations.append(observation)
        try:
            free_bytes = shutil.disk_usage(request.authorized_run_root).free
        except OSError:
            return self._failure(
                request,
                LocalQePreparationFailureCode.RESOURCE_OBSERVATION_FAILED,
                LocalQePreparationPhase.RESOURCES,
                "free-space observation for the authorized run root",
                "free-space observation failed",
                (request.execution_input.identity.value,),
            )
        if free_bytes < request.limits.minimum_free_bytes:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INSUFFICIENT_FREE_SPACE,
                LocalQePreparationPhase.RESOURCES,
                "observed free bytes satisfy the declared minimum",
                "observed free bytes are below the declared minimum",
                (request.execution_input.identity.value,),
            )
        executable_destinations = tuple(
            value
            for value in destinations
            if value.role is LocalQeResolvedDestinationRole.EXECUTABLE
        )
        if len(executable_destinations) != 1:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                LocalQePreparationPhase.CONFINEMENT,
                "one exact staged executable destination",
                "staged executable destination is not unique",
                (request.executable_configuration.identity.value,),
            )
        argv = (
            str(executable_destinations[0].absolute_path),
            *request.executable_configuration.argument_suffix,
        )
        native_input: QeNativeInputArtifact = request.execution_input.native_input
        native_content_identity: ArtifactContentIdentity = (
            native_input.content.content_identity
        )
        preparation_identity = QePreparationIdentity(
            "qe-local-preparation-v1:"
            + self._framed_digest(
                (
                    self.implementation_identity.value,
                    request.execution_input.identity.value,
                    calculator_input_binding.admission_policy_identity.value,
                    calculator_input_binding.calculator_input.input_id,
                    calculator_input_binding.provider_record_sha256,
                    request.executable_configuration.identity.value,
                    str(workspace),
                    *argv,
                    f"native:{native_input.identity.value}:"
                    f"{native_input.destination.value}:"
                    f"{native_content_identity.algorithm}:"
                    f"{native_content_identity.digest}:"
                    f"{native_content_identity.byte_count}",
                    *(
                        f"{value.artifact_identity.value}:"
                        f"{self._source_observation_identity(value)}"
                        for value in source_observations
                    ),
                    *(
                        f"{value.role.value}:{value.portable_destination.value}"
                        for value in destinations
                    ),
                    "provider_execution_record:"
                    + execution_record_destination.portable_destination.value,
                    str(free_bytes),
                )
            )
        )
        return LocalQePreparedExecution(
            identity=preparation_identity,
            request=request,
            calculator_input_binding=calculator_input_binding,
            preparation_implementation_identity=self.implementation_identity,
            workspace=workspace,
            argv=argv,
            environment_additions=request.executable_configuration.environment_additions,
            execution_record_destination=execution_record_destination,
            resolved_destinations=destinations,
            executable_content_identity=executable_observation,
            source_observations=tuple(source_observations),
            required_free_bytes=request.limits.minimum_free_bytes,
            observed_free_bytes=free_bytes,
        )

    def render_dry_run(self, prepared: LocalQePreparedExecution) -> str:
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
        if type(prepared) is not LocalQePreparedExecution:
            raise TypeError("prepared must be LocalQePreparedExecution")
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
        lines.append(
            "provider_execution_record_destination="
            + prepared.execution_record_destination.portable_destination.value
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
        request: LocalQeExecutionPreparationRequest,
    ) -> LocalQePreparationFailure | None:
        configuration = request.executable_configuration
        if request.execution_input.program is not configuration.program:
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNSUPPORTED_BINDING,
                LocalQePreparationPhase.COMPATIBILITY,
                "execution input and executable configuration use one program role",
                "program roles differ",
                (
                    request.execution_input.identity.value,
                    configuration.identity.value,
                ),
            )
        binding = LocalQeSupportedExecutableBinding(
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
                LocalQePreparationFailureCode.UNSUPPORTED_BINDING,
                LocalQePreparationPhase.COMPATIBILITY,
                "an explicitly supported program/version/classifier binding",
                "binding is not supported by this preparer",
                (configuration.identity.value,),
            )
        return None

    def _resolve_confinement(
        self,
        request: LocalQeExecutionPreparationRequest,
        calculator_input_binding: QeCalculatorInputBinding,
    ) -> (
        tuple[
            Path,
            tuple[LocalQeResolvedDestination, ...],
            LocalQeExecutionRecordDestination,
        ]
        | LocalQePreparationFailure
    ):
        root = request.authorized_run_root
        if not root.exists():
            return self._failure(
                request,
                LocalQePreparationFailureCode.MISSING_SOURCE,
                LocalQePreparationPhase.CONFINEMENT,
                "an existing authorized run root",
                "authorized run root is missing",
                (request.execution_input.identity.value,),
            )
        if self._path_has_symlink(root) or not root.is_dir():
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                LocalQePreparationPhase.CONFINEMENT,
                "a nonsymlink authorized run-root directory",
                "authorized run root has an unsupported type or symlink",
                (request.execution_input.identity.value,),
            )
        try:
            resolved_root = root.resolve(strict=True)
        except OSError:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                LocalQePreparationPhase.CONFINEMENT,
                "a resolvable authorized run root",
                "authorized run root cannot be resolved",
                (request.execution_input.identity.value,),
            )
        if resolved_root != root:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                LocalQePreparationPhase.CONFINEMENT,
                "an already canonical authorized run root",
                "authorized run root differs from its canonical path",
                (request.execution_input.identity.value,),
            )
        workspace = root / request.attempt_workspace_name.value
        if workspace.exists() or workspace.is_symlink():
            return self._failure(
                request,
                LocalQePreparationFailureCode.EXISTING_WORKSPACE,
                LocalQePreparationPhase.CONFINEMENT,
                "an absent attempt workspace",
                "attempt workspace already exists",
                (request.execution_input.identity.value,),
            )
        role_destinations = (
            (
                LocalQeResolvedDestinationRole.EXECUTABLE,
                request.executable_configuration.identity.value,
                request.executable_destination,
            ),
            (
                LocalQeResolvedDestinationRole.STDOUT,
                "stdout",
                request.stdout_destination,
            ),
            (
                LocalQeResolvedDestinationRole.STDERR,
                "stderr",
                request.stderr_destination,
            ),
            (
                LocalQeResolvedDestinationRole.BEFORE_SNAPSHOT,
                "before_snapshot",
                request.before_snapshot_destination,
            ),
            (
                LocalQeResolvedDestinationRole.AFTER_SNAPSHOT,
                "after_snapshot",
                request.after_snapshot_destination,
            ),
            (
                LocalQeResolvedDestinationRole.TERMINAL_RECORD,
                "terminal_record",
                request.terminal_record_destination,
            ),
            (
                LocalQeResolvedDestinationRole.WORK,
                "work",
                request.work_destination,
            ),
            (
                LocalQeResolvedDestinationRole.RESULT,
                "result",
                request.result_destination,
            ),
        )
        raw_destinations: list[
            tuple[
                LocalQeResolvedDestinationRole,
                str,
                QeArtifactDestination,
            ]
        ] = list(role_destinations)
        native_input: QeNativeInputArtifact = request.execution_input.native_input
        raw_destinations.append(
            (
                LocalQeResolvedDestinationRole.INPUT_ARTIFACT,
                native_input.identity.value,
                native_input.destination,
            )
        )
        raw_destinations.extend(
            (
                LocalQeResolvedDestinationRole.INPUT_ARTIFACT,
                resource.artifact_identity.value,
                resource.destination,
            )
            for resource in calculator_input_binding.external_input_resources
        )
        raw_destinations.extend(
            (
                LocalQeResolvedDestinationRole.INPUT_ARTIFACT,
                predecessor.identity.value,
                predecessor.destination,
            )
            for predecessor in request.execution_input.predecessor_native_state
        )
        portable_values = (
            *(value.value for _, _, value in raw_destinations),
            request.execution_record_destination.value,
        )
        if len(set(portable_values)) != len(portable_values):
            return self._failure(
                request,
                LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                LocalQePreparationPhase.CONFINEMENT,
                "unique workspace-relative destinations",
                "two or more destinations are equal",
                (request.execution_input.identity.value,),
            )
        resolved: list[LocalQeResolvedDestination] = []
        for role, owner_identity, portable in raw_destinations:
            absolute = workspace.joinpath(*PurePosixPath(portable.value).parts)
            try:
                common = Path(os.path.commonpath((workspace, absolute)))
            except ValueError:
                return self._failure(
                    request,
                    LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                    LocalQePreparationPhase.CONFINEMENT,
                    "every destination confined beneath the attempt workspace",
                    "destination confinement comparison failed",
                    (owner_identity,),
                )
            if common != workspace:
                return self._failure(
                    request,
                    LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                    LocalQePreparationPhase.CONFINEMENT,
                    "every destination confined beneath the attempt workspace",
                    "destination escapes the attempt workspace",
                    (owner_identity,),
                )
            resolved.append(
                LocalQeResolvedDestination(
                    role=role,
                    owner_identity=owner_identity,
                    portable_destination=portable,
                    absolute_path=absolute,
                )
            )
        execution_record_absolute: Path = workspace.joinpath(
            *PurePosixPath(request.execution_record_destination.value).parts
        )
        try:
            execution_record_common: Path = Path(
                os.path.commonpath((workspace, execution_record_absolute))
            )
        except ValueError:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                LocalQePreparationPhase.CONFINEMENT,
                "the execution-record destination confined beneath the workspace",
                "execution-record destination confinement comparison failed",
                (request.execution_input.identity.value,),
            )
        if execution_record_common != workspace:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                LocalQePreparationPhase.CONFINEMENT,
                "the execution-record destination confined beneath the workspace",
                "execution-record destination escapes the attempt workspace",
                (request.execution_input.identity.value,),
            )
        execution_record_destination = LocalQeExecutionRecordDestination(
            portable_destination=request.execution_record_destination,
            absolute_path=execution_record_absolute,
        )
        expected_external_identities: tuple[ArtifactIdentity, ...] = tuple(
            sorted(
                (
                    *(
                        value.artifact_identity
                        for value in calculator_input_binding.external_input_resources
                    ),
                    *(
                        value.identity
                        for value in request.execution_input.predecessor_native_state
                    ),
                ),
                key=lambda value: value.value,
            )
        )
        source_identities: tuple[ArtifactIdentity, ...] = tuple(
            value.artifact_identity for value in request.external_artifact_sources
        )
        if source_identities != expected_external_identities:
            return self._failure(
                request,
                LocalQePreparationFailureCode.INVALID_CONFINEMENT,
                LocalQePreparationPhase.CONFINEMENT,
                "exactly one external source binding for every pseudopotential and "
                "predecessor-state artifact",
                "external artifact-source bindings do not equal the execution input",
                (request.execution_input.identity.value,),
            )
        return (
            workspace,
            tuple(
                sorted(
                    resolved,
                    key=lambda value: (value.role.value, value.owner_identity),
                )
            ),
            execution_record_destination,
        )

    def _inspect_executable(
        self,
        request: LocalQeExecutionPreparationRequest,
    ) -> ArtifactContentIdentity | LocalQePreparationFailure:
        configuration = request.executable_configuration
        if request.executable_content_identity != (
            configuration.executable_content_identity
        ):
            return self._failure(
                request,
                LocalQePreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH,
                LocalQePreparationPhase.EXECUTABLE,
                "configuration and local-boundary executable identities agree",
                "configuration and local-boundary executable identities differ",
                (configuration.identity.value,),
            )
        if self._path_has_symlink(request.executable_path):
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                LocalQePreparationPhase.EXECUTABLE,
                "an executable path with no symbolic-link component",
                "executable path contains a symbolic link",
                (configuration.identity.value,),
            )
        try:
            binding = QeExecutableBindingAdapter().execute(
                configuration, request.executable_path
            )
        except ValueError:
            return self._failure(
                request,
                LocalQePreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH,
                LocalQePreparationPhase.EXECUTABLE,
                "a provider-valid exact executable identity and absolute path",
                "configuration cannot form a provider executable binding",
                (configuration.identity.value,),
            )
        result = CalculatorExecutablePreparer(binding).prepare()
        if type(result) is CalculatorExecutablePreparationFailure:
            return self._provider_executable_failure(request, result)
        assert type(result) is CalculatorPreparedExecutable
        return request.executable_content_identity

    def _provider_executable_failure(
        self,
        request: LocalQeExecutionPreparationRequest,
        failure: CalculatorExecutablePreparationFailure,
    ) -> LocalQePreparationFailure:
        code_map = {
            CalculatorExecutablePreparationFailureCode.MISSING: (
                LocalQePreparationFailureCode.MISSING_SOURCE,
                "an existing nonsymlink regular executable",
            ),
            CalculatorExecutablePreparationFailureCode.SYMBOLIC_LINK: (
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                "a nonsymlink regular executable",
            ),
            CalculatorExecutablePreparationFailureCode.NOT_REGULAR: (
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                "a regular executable file",
            ),
            CalculatorExecutablePreparationFailureCode.NOT_EXECUTABLE: (
                LocalQePreparationFailureCode.EXECUTABLE_NOT_RUNNABLE,
                "a regular file with an executable mode bit",
            ),
            CalculatorExecutablePreparationFailureCode.BYTE_SIZE_MISMATCH: (
                LocalQePreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH,
                "observed executable byte size equals the declared identity",
            ),
            CalculatorExecutablePreparationFailureCode.SHA256_MISMATCH: (
                LocalQePreparationFailureCode.EXECUTABLE_IDENTITY_MISMATCH,
                "observed executable SHA-256 equals the declared identity",
            ),
            CalculatorExecutablePreparationFailureCode.OBSERVATION_FAILED: (
                LocalQePreparationFailureCode.EXECUTABLE_OBSERVATION_FAILED,
                "a complete read-only executable observation",
            ),
        }
        local_code, expected_condition = code_map[failure.code]
        return self._failure(
            request,
            local_code,
            LocalQePreparationPhase.EXECUTABLE,
            expected_condition,
            failure.observed_condition,
            (request.executable_configuration.identity.value,),
        )

    def _inspect_artifact_source(
        self,
        request: LocalQeExecutionPreparationRequest,
        calculator_input_binding: QeCalculatorInputBinding,
        source: LocalQeArtifactSource,
    ) -> LocalQeArtifactSourceObservation | LocalQePreparationFailure:
        resources_by_identity: dict[
            ArtifactIdentity, QeExternalInputResourceBinding
        ] = {
            value.artifact_identity: value
            for value in calculator_input_binding.external_input_resources
        }
        resource: QeExternalInputResourceBinding | None = resources_by_identity.get(
            source.artifact_identity
        )
        if resource is not None:
            requirement: CalculatorExternalInputRequirement = (
                resource.external_requirement
            )
            expected: ArtifactContentIdentity = ArtifactContentIdentity(
                "sha256", requirement.sha256, requirement.byte_size
            )
            observation: ArtifactContentIdentity | LocalQePreparationFailure = (
                self._inspect_regular_file(
                    request=request,
                    source=source.source,
                    expected=expected,
                    mismatch_code=(
                        LocalQePreparationFailureCode.SOURCE_IDENTITY_MISMATCH
                    ),
                    phase=LocalQePreparationPhase.INPUT_SOURCE,
                    related_identity=source.artifact_identity.value,
                )
            )
            if isinstance(observation, LocalQePreparationFailure):
                return observation
            return LocalQeFileSourceObservation(
                artifact_identity=source.artifact_identity,
                source=source.source,
                content_identity=observation,
            )
        predecessors_by_identity: dict[
            ArtifactIdentity, QePredecessorNativeStateArtifact
        ] = {
            value.identity: value
            for value in request.execution_input.predecessor_native_state
        }
        predecessor: QePredecessorNativeStateArtifact = predecessors_by_identity[
            source.artifact_identity
        ]
        return self._inspect_tree_source(request, source.source, predecessor)

    def _inspect_regular_file(
        self,
        *,
        request: LocalQeExecutionPreparationRequest,
        source: Path,
        expected: ArtifactContentIdentity,
        mismatch_code: LocalQePreparationFailureCode,
        phase: LocalQePreparationPhase,
        related_identity: str,
    ) -> ArtifactContentIdentity | LocalQePreparationFailure:
        if not source.exists():
            return self._failure(
                request,
                LocalQePreparationFailureCode.MISSING_SOURCE,
                phase,
                "an existing nonsymlink regular file",
                "source is missing",
                (related_identity,),
            )
        if self._path_has_symlink(source):
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
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
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                phase,
                "an inspectable nonsymlink regular file",
                "source type observation failed",
                (related_identity,),
            )
        if not stat.S_ISREG(mode):
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                phase,
                "a nonsymlink regular file",
                "source is not a regular file",
                (related_identity,),
            )
        try:
            observed = self._file_content_identity(source)
        except OSError:
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
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
        request: LocalQeExecutionPreparationRequest,
        source: Path,
        artifact: QePredecessorNativeStateArtifact,
    ) -> LocalQeTreeSourceObservation | LocalQePreparationFailure:
        if not source.exists():
            return self._failure(
                request,
                LocalQePreparationFailureCode.MISSING_SOURCE,
                LocalQePreparationPhase.INPUT_SOURCE,
                "an existing nonsymlink predecessor-state directory",
                "source tree is missing",
                (artifact.identity.value,),
            )
        if self._path_has_symlink(source) or not source.is_dir():
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                LocalQePreparationPhase.INPUT_SOURCE,
                "a nonsymlink directory tree of directories and regular files",
                "source tree has an unsupported root type or symlink",
                (artifact.identity.value,),
            )
        try:
            entries, total_bytes = self._tree_entry_identities(source)
        except OSError:
            return self._failure(
                request,
                LocalQePreparationFailureCode.UNEXPECTED_SYMLINK_OR_TYPE,
                LocalQePreparationPhase.INPUT_SOURCE,
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
                LocalQePreparationFailureCode.SOURCE_IDENTITY_MISMATCH,
                LocalQePreparationPhase.INPUT_SOURCE,
                "observed tree manifest and entries equal declared identities",
                "observed tree identity differs from the declared identity",
                (artifact.identity.value,),
            )
        return LocalQeTreeSourceObservation(
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
    def _framed_digest(values: tuple[str, ...]) -> str:
        digest = hashlib.sha256()
        for value in values:
            encoded = value.encode("utf-8")
            digest.update(len(encoded).to_bytes(8, byteorder="big", signed=False))
            digest.update(encoded)
        return digest.hexdigest()

    @staticmethod
    def _source_observation_identity(
        observation: LocalQeArtifactSourceObservation,
    ) -> str:
        if type(observation) is LocalQeFileSourceObservation:
            return (
                f"{observation.content_identity.algorithm}:"
                f"{observation.content_identity.digest}:"
                f"{observation.content_identity.byte_count}"
            )
        assert type(observation) is LocalQeTreeSourceObservation
        return observation.manifest_identity.value

    def _failure(
        self,
        request: LocalQeExecutionPreparationRequest,
        code: LocalQePreparationFailureCode,
        phase: LocalQePreparationPhase,
        expected_condition: str,
        observed_condition: str,
        related_identities: tuple[str, ...],
    ) -> LocalQePreparationFailure:
        return LocalQePreparationFailure(
            code=code,
            phase=phase,
            execution_input_identity=request.execution_input.identity,
            preparation_implementation_identity=self.implementation_identity,
            expected_condition=expected_condition,
            observed_condition=observed_condition,
            related_identities=tuple(sorted(set(related_identities))),
            claim_boundary=_PREPARATION_CLAIM_BOUNDARY,
        )
