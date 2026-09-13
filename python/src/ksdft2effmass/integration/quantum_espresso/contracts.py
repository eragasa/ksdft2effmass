"""Public immutable contracts for local Quantum ESPRESSO execution.

The records represent exact QE-native inputs, executable bindings, process and
independent stream observations, version-bound diagnostics, and closed calculator
outcomes. They perform no filesystem access, process invocation, diagnostic
classification, serialization, retry, Workflow CPN transition, or scientific
acceptance. Concrete ActionObjects in this integration consume and produce these
records. The durable terminal-record wire format remains private and revisable.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import ClassVar

from ksdft2effmass.workflows import (
    ArtifactContentIdentity,
    ArtifactIdentity,
    ArtifactManifestEntryIdentity,
    ArtifactManifestIdentity,
    AttemptIdentity,
    OperationIdentity,
    ResultObjectIdentity,
    TaskActivationIdentity,
    TaskDefinitionIdentity,
    TaskInstanceIdentity,
)

_MAX_U64 = 18_446_744_073_709_551_615


@dataclass(frozen=True, slots=True)
class QuantumEspressoExecutionInputIdentity:
    """Identify one exact QE execution input.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("execution input identity value must be a built-in str")
        if not self.value:
            raise ValueError("execution input identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoExecutableConfigurationIdentity:
    """Identify one exact executable configuration.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError(
                "executable configuration identity value must be a built-in str"
            )
        if not self.value:
            raise ValueError(
                "executable configuration identity value must not be empty"
            )


@dataclass(frozen=True, slots=True)
class QuantumEspressoDiagnosticClassifierIdentity:
    """Identify one exact diagnostic-classifier implementation and catalog.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("classifier identity value must be a built-in str")
        if not self.value:
            raise ValueError("classifier identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoPreparationIdentity:
    """Identify one exact read-only local preparation result.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("preparation identity value must be a built-in str")
        if not self.value:
            raise ValueError("preparation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoProcessObservationIdentity:
    """Identify one exact mechanical process observation.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("process observation identity value must be a built-in str")
        if not self.value:
            raise ValueError("process observation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoDiagnosticObservationIdentity:
    """Identify one exact diagnostic observation.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError(
                "diagnostic observation identity value must be a built-in str"
            )
        if not self.value:
            raise ValueError("diagnostic observation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoOutputMarkerObservationIdentity:
    """Identify one exact calculator output-marker observation.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("marker observation identity value must be a built-in str")
        if not self.value:
            raise ValueError("marker observation identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoDiagnosticReportIdentity:
    """Identify one exact diagnostic-classification result.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("diagnostic report identity value must be a built-in str")
        if not self.value:
            raise ValueError("diagnostic report identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoTerminalRecordIdentity:
    """Identify one exact private terminal record.

    Attributes
    ----------
    value
        Nonempty exact nominal identity value.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("terminal record identity value must be a built-in str")
        if not self.value:
            raise ValueError("terminal record identity value must not be empty")


@dataclass(frozen=True, slots=True)
class QuantumEspressoArtifactDestination:
    """Represent one parent-free portable artifact destination.

    Attributes
    ----------
    value
        Parent-free portable POSIX path relative to the prepared workspace.
    """

    value: str

    def __post_init__(self) -> None:
        if type(self.value) is not str:
            raise TypeError("artifact destination value must be a built-in str")
        if not self.value:
            raise ValueError("artifact destination value must not be empty")
        if "\\" in self.value or self.value.startswith(("/", "~")):
            raise ValueError("artifact destination must be a portable relative path")
        path = PurePosixPath(self.value)
        if (
            path.is_absolute()
            or path.as_posix() != self.value
            or any(part in {"", ".", ".."} for part in path.parts)
            or (
                len(self.value) >= 2
                and self.value[0].isalpha()
                and self.value[1] == ":"
            )
        ):
            raise ValueError("artifact destination must be a portable relative path")


class QuantumEspressoProgram(StrEnum):
    """Closed initial QE program roles."""

    PW = "pw"
    BANDS = "bands"


class QuantumEspressoExecutableKind(StrEnum):
    """Distinguish actual QE executables from deterministic test fixtures."""

    QUANTUM_ESPRESSO = "quantum_espresso"
    DETERMINISTIC_FIXTURE = "deterministic_fixture"


@dataclass(frozen=True, slots=True)
class QuantumEspressoFileArtifactContent:
    """Represent exact content of one regular-file input artifact.

    Attributes
    ----------
    content_identity
        Exact nominal identity retained for cross-record correlation.
    """

    content_identity: ArtifactContentIdentity

    def __post_init__(self) -> None:
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")


@dataclass(frozen=True, slots=True)
class QuantumEspressoTreeArtifactContent:
    """Represent exact content of one immutable directory-tree input artifact.

    Attributes
    ----------
    manifest_identity
        Exact nominal identity retained for cross-record correlation.
    manifest_entry_identities
        Canonical immutable tuple of exact nominal identities.
    """

    manifest_identity: ArtifactManifestIdentity
    manifest_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]

    def __post_init__(self) -> None:
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


type QuantumEspressoInputArtifactContent = (
    QuantumEspressoFileArtifactContent | QuantumEspressoTreeArtifactContent
)


@dataclass(frozen=True, slots=True)
class QuantumEspressoNativeInputArtifact:
    """Represent the exact native input file staged for one operation.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    content
        Closed exact file or deterministic tree content contract.
    destination
        Exact destination path or parent-free workspace destination, as declared.
    """

    identity: ArtifactIdentity
    content: QuantumEspressoFileArtifactContent
    destination: QuantumEspressoArtifactDestination

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactIdentity:
            raise TypeError("identity must be ArtifactIdentity")
        if type(self.content) is not QuantumEspressoFileArtifactContent:
            raise TypeError("content must be QuantumEspressoFileArtifactContent")
        if type(self.destination) is not QuantumEspressoArtifactDestination:
            raise TypeError("destination must be QuantumEspressoArtifactDestination")


@dataclass(frozen=True, slots=True)
class QuantumEspressoPseudopotentialArtifact:
    """Represent one exact pseudopotential file staged for an operation.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    content
        Closed exact file or deterministic tree content contract.
    destination
        Exact destination path or parent-free workspace destination, as declared.
    """

    identity: ArtifactIdentity
    content: QuantumEspressoFileArtifactContent
    destination: QuantumEspressoArtifactDestination

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactIdentity:
            raise TypeError("identity must be ArtifactIdentity")
        if type(self.content) is not QuantumEspressoFileArtifactContent:
            raise TypeError("content must be QuantumEspressoFileArtifactContent")
        if type(self.destination) is not QuantumEspressoArtifactDestination:
            raise TypeError("destination must be QuantumEspressoArtifactDestination")


@dataclass(frozen=True, slots=True)
class QuantumEspressoPredecessorNativeStateArtifact:
    """Represent exact admitted predecessor native state for isolated staging.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    content
        Closed exact file or deterministic tree content contract.
    destination
        Exact destination path or parent-free workspace destination, as declared.
    predecessor_result_identity
        Exact nominal identity retained for cross-record correlation.
    predecessor_manifest_entry_identity
        Exact nominal identity retained for cross-record correlation.
    """

    identity: ArtifactIdentity
    content: QuantumEspressoTreeArtifactContent
    destination: QuantumEspressoArtifactDestination
    predecessor_result_identity: ResultObjectIdentity
    predecessor_manifest_entry_identity: ArtifactManifestEntryIdentity

    def __post_init__(self) -> None:
        if type(self.identity) is not ArtifactIdentity:
            raise TypeError("identity must be ArtifactIdentity")
        if type(self.content) is not QuantumEspressoTreeArtifactContent:
            raise TypeError("content must be QuantumEspressoTreeArtifactContent")
        if type(self.destination) is not QuantumEspressoArtifactDestination:
            raise TypeError("destination must be QuantumEspressoArtifactDestination")
        if type(self.predecessor_result_identity) is not ResultObjectIdentity:
            raise TypeError("predecessor_result_identity must be ResultObjectIdentity")
        if type(self.predecessor_manifest_entry_identity) is not (
            ArtifactManifestEntryIdentity
        ):
            raise TypeError(
                "predecessor_manifest_entry_identity must be "
                "ArtifactManifestEntryIdentity"
            )


type QuantumEspressoInputArtifact = (
    QuantumEspressoNativeInputArtifact
    | QuantumEspressoPseudopotentialArtifact
    | QuantumEspressoPredecessorNativeStateArtifact
)


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoExecutionInput:
    """Bind exact operation input artifacts to one Workflow Task attempt.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    program
        Closed Quantum ESPRESSO program role.
    native_input
        Exact native QE input artifact for process stdin.
    pseudopotentials
        Canonical immutable tuple of exact pseudopotential artifacts.
    predecessor_native_state
        Canonical immutable tuple of explicitly correlated predecessor state.
    task_definition_identity
        Exact nominal identity retained for cross-record correlation.
    task_instance_identity
        Exact nominal identity retained for cross-record correlation.
    activation_identity
        Exact nominal identity retained for cross-record correlation.
    operation_identity
        Exact nominal identity retained for cross-record correlation.
    attempt_identity
        Exact nominal identity retained for cross-record correlation.
    contract_version
        Exact public in-memory contract version string.
    """

    identity: QuantumEspressoExecutionInputIdentity
    program: QuantumEspressoProgram
    native_input: QuantumEspressoNativeInputArtifact
    pseudopotentials: tuple[QuantumEspressoPseudopotentialArtifact, ...]
    predecessor_native_state: tuple[QuantumEspressoPredecessorNativeStateArtifact, ...]
    task_definition_identity: TaskDefinitionIdentity
    task_instance_identity: TaskInstanceIdentity
    activation_identity: TaskActivationIdentity
    operation_identity: OperationIdentity
    attempt_identity: AttemptIdentity
    contract_version: str

    def __post_init__(self) -> None:
        expected = (
            (self.identity, QuantumEspressoExecutionInputIdentity, "identity"),
            (self.program, QuantumEspressoProgram, "program"),
            (
                self.native_input,
                QuantumEspressoNativeInputArtifact,
                "native_input",
            ),
            (
                self.task_definition_identity,
                TaskDefinitionIdentity,
                "task_definition_identity",
            ),
            (
                self.task_instance_identity,
                TaskInstanceIdentity,
                "task_instance_identity",
            ),
            (
                self.activation_identity,
                TaskActivationIdentity,
                "activation_identity",
            ),
            (self.operation_identity, OperationIdentity, "operation_identity"),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.pseudopotentials) is not tuple or any(
            type(value) is not QuantumEspressoPseudopotentialArtifact
            for value in self.pseudopotentials
        ):
            raise TypeError(
                "pseudopotentials must be a tuple of "
                "QuantumEspressoPseudopotentialArtifact"
            )
        if type(self.predecessor_native_state) is not tuple or any(
            type(value) is not QuantumEspressoPredecessorNativeStateArtifact
            for value in self.predecessor_native_state
        ):
            raise TypeError(
                "predecessor_native_state must be a tuple of "
                "QuantumEspressoPredecessorNativeStateArtifact"
            )
        artifacts: tuple[QuantumEspressoInputArtifact, ...] = (
            self.native_input,
            *self.pseudopotentials,
            *self.predecessor_native_state,
        )
        artifact_values = tuple(value.identity.value for value in artifacts)
        destinations = tuple(value.destination.value for value in artifacts)
        if len(set(artifact_values)) != len(artifact_values):
            raise ValueError("input artifact identities must be unique")
        if len(set(destinations)) != len(destinations):
            raise ValueError("input artifact destinations must be unique")
        if self.pseudopotentials != tuple(
            sorted(self.pseudopotentials, key=lambda value: value.identity.value)
        ) or len({value.identity for value in self.pseudopotentials}) != len(
            self.pseudopotentials
        ):
            raise ValueError("pseudopotentials must be unique and lexically sorted")
        if self.predecessor_native_state != tuple(
            sorted(
                self.predecessor_native_state,
                key=lambda value: value.identity.value,
            )
        ) or len({value.identity for value in self.predecessor_native_state}) != len(
            self.predecessor_native_state
        ):
            raise ValueError(
                "predecessor_native_state must be unique and lexically sorted"
            )
        if type(self.contract_version) is not str:
            raise TypeError("contract_version must be a built-in str")
        if not self.contract_version:
            raise ValueError("contract_version must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoExecutableConfiguration:
    """Represent one exact executable and diagnostic-classifier binding.

    Attributes
    ----------
    identity
        Exact identity of the complete executable configuration.
    program
        QE program role selected for execution.
    executable_kind
        Actual QE or deterministic-fixture executable namespace.
    executable_content_identity
        Exact SHA-256 and byte-count identity of the admitted executable bytes.
    program_version
        Exact nonempty program-version text whose namespace matches
        ``executable_kind``.
    argument_suffix
        Ordered NUL-free non-shell arguments appended after the executable path.
    environment_additions
        Lexically ordered unique additions restricted to documented thread-control
        keys. Values are retained exactly and must be NUL-free.
    classifier_identity
        Exact diagnostic-classifier catalog identity for the program and version.
    contract_version
        Nonempty identity of this configuration contract.
    """

    _ALLOWED_ENVIRONMENT_ADDITION_KEYS: ClassVar[frozenset[str]] = frozenset(
        {
            "MKL_NUM_THREADS",
            "OMP_NUM_THREADS",
            "OMP_STACKSIZE",
            "OPENBLAS_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
        }
    )

    identity: QuantumEspressoExecutableConfigurationIdentity
    program: QuantumEspressoProgram
    executable_kind: QuantumEspressoExecutableKind
    executable_content_identity: ArtifactContentIdentity
    program_version: str
    argument_suffix: tuple[str, ...]
    environment_additions: tuple[tuple[str, str], ...]
    classifier_identity: QuantumEspressoDiagnosticClassifierIdentity
    contract_version: str

    def __post_init__(self) -> None:
        expected = (
            (
                self.identity,
                QuantumEspressoExecutableConfigurationIdentity,
                "identity",
            ),
            (self.program, QuantumEspressoProgram, "program"),
            (
                self.executable_kind,
                QuantumEspressoExecutableKind,
                "executable_kind",
            ),
            (
                self.executable_content_identity,
                ArtifactContentIdentity,
                "executable_content_identity",
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
        for name in ("program_version", "contract_version"):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must not be empty")
        fixture_version = self.program_version.startswith("fixture-")
        if (
            self.executable_kind is QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE
        ) != fixture_version:
            raise ValueError(
                "program_version namespace must agree with executable_kind"
            )
        if type(self.argument_suffix) is not tuple or any(
            type(value) is not str for value in self.argument_suffix
        ):
            raise TypeError("argument_suffix must be a tuple of built-in str values")
        if any("\x00" in value for value in self.argument_suffix):
            raise ValueError("argument_suffix must not contain NUL characters")
        additions = self.environment_additions
        if type(additions) is not tuple or any(
            type(value) is not tuple
            or len(value) != 2
            or type(value[0]) is not str
            or type(value[1]) is not str
            for value in additions
        ):
            raise TypeError("environment_additions must contain built-in string pairs")
        if any(
            not key or "=" in key or "\x00" in key or "\x00" in value
            for key, value in additions
        ):
            raise ValueError("environment additions contain an invalid key or value")
        unsupported_keys = tuple(
            key
            for key, _value in additions
            if key not in self._ALLOWED_ENVIRONMENT_ADDITION_KEYS
        )
        if unsupported_keys:
            raise ValueError(
                "environment additions contain a key outside the fixed "
                "thread-control allowlist"
            )
        if additions != tuple(sorted(additions, key=lambda value: value[0])) or len(
            {key for key, _ in additions}
        ) != len(additions):
            raise ValueError(
                "environment_additions must have unique lexically sorted keys"
            )


class QuantumEspressoDiagnosticChannel(StrEnum):
    """Closed independently captured diagnostic channels.

    Attributes
    ----------
    STDOUT
        Bytes written through the child process standard-output descriptor.
    STDERR
        Bytes written through the child process standard-error descriptor.
    """

    STDOUT = "stdout"
    STDERR = "stderr"


class QuantumEspressoDiagnosticDisposition(StrEnum):
    """Closed native diagnostic dispositions.

    Attributes
    ----------
    NONBLOCKING
        Recognized notice that does not by itself determine calculator failure.
    FATAL
        Recognized primary calculator-fatal diagnostic.
    SECONDARY_FATAL
        Recognized secondary diagnostic valid only with a primary fatal diagnostic.
    UNRESOLVED
        Nonempty output span not admitted by the exact classifier catalog.
    """

    NONBLOCKING = "nonblocking"
    FATAL = "fatal"
    SECONDARY_FATAL = "secondary_fatal"
    UNRESOLVED = "unresolved"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoStreamObservation:
    """Represent exact content captured from one process stream.

    Attributes
    ----------
    channel
        Independent stdout or stderr channel represented by this record.
    artifact_identity
        Workflow artifact identity assigned to the captured stream.
    content_identity
        Exact SHA-256 digest and byte count of the captured bytes.
    """

    channel: QuantumEspressoDiagnosticChannel
    artifact_identity: ArtifactIdentity
    content_identity: ArtifactContentIdentity

    def __post_init__(self) -> None:
        if type(self.channel) is not QuantumEspressoDiagnosticChannel:
            raise TypeError("channel must be QuantumEspressoDiagnosticChannel")
        if type(self.artifact_identity) is not ArtifactIdentity:
            raise TypeError("artifact_identity must be ArtifactIdentity")
        if type(self.content_identity) is not ArtifactContentIdentity:
            raise TypeError("content_identity must be ArtifactContentIdentity")


@dataclass(frozen=True, slots=True)
class QuantumEspressoNormalProcessExit:
    """Represent one determinate normal process exit.

    Attributes
    ----------
    exit_code
        Nonnegative built-in process exit code. Zero has no calculator-level meaning
        until diagnostics and required native outputs are resolved.
    """

    exit_code: int

    def __post_init__(self) -> None:
        if type(self.exit_code) is not int:
            raise TypeError("exit_code must be a built-in int excluding bool")
        if self.exit_code < 0:
            raise ValueError("exit_code must be nonnegative")


@dataclass(frozen=True, slots=True)
class QuantumEspressoProcessSignalTermination:
    """Represent one determinate process signal termination.

    Attributes
    ----------
    signal_number
        Positive operating-system signal number observed from the child process.
    """

    signal_number: int

    def __post_init__(self) -> None:
        if type(self.signal_number) is not int:
            raise TypeError("signal_number must be a built-in int excluding bool")
        if self.signal_number <= 0:
            raise ValueError("signal_number must be positive")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoProcessTimeout:
    """Represent a determinate timeout and its bounded cleanup actions.

    Attributes
    ----------
    timeout_milliseconds
        Positive configured wall-time ceiling in milliseconds.
    termination_sent
        Whether process-group termination was successfully requested.
    kill_sent
        Whether process-group kill escalation was required after the grace interval.
    """

    timeout_milliseconds: int
    termination_sent: bool
    kill_sent: bool

    def __post_init__(self) -> None:
        if type(self.timeout_milliseconds) is not int:
            raise TypeError(
                "timeout_milliseconds must be a built-in int excluding bool"
            )
        if self.timeout_milliseconds <= 0:
            raise ValueError("timeout_milliseconds must be positive")
        if type(self.termination_sent) is not bool:
            raise TypeError("termination_sent must be a built-in bool")
        if type(self.kill_sent) is not bool:
            raise TypeError("kill_sent must be a built-in bool")
        if self.kill_sent and not self.termination_sent:
            raise ValueError("kill_sent requires termination_sent")


type QuantumEspressoProcessTermination = (
    QuantumEspressoNormalProcessExit
    | QuantumEspressoProcessSignalTermination
    | QuantumEspressoProcessTimeout
)


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoProcessObservation:
    """Represent one complete mechanical process and stream observation.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    execution_input_identity
        Exact nominal identity retained for cross-record correlation.
    executable_configuration_identity
        Exact nominal identity retained for cross-record correlation.
    preparation_identity
        Exact nominal identity retained for cross-record correlation.
    attempt_identity
        Exact nominal identity retained for cross-record correlation.
    argv_content_identity
        Exact nominal identity retained for cross-record correlation.
    termination
        Closed normal-exit, signal, or timeout observation.
    wall_duration_nanoseconds
        Observed wall duration in nonnegative integer nanoseconds from the pre-spawn
        origin.
    stdout
        Exact independently captured stream observation.
    stderr
        Exact independently captured stream observation.
    before_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    after_snapshot_identity
        Exact nominal identity retained for cross-record correlation.
    created_entry_count
        Aggregate entry count in the closed after-process workspace snapshot.
    created_total_bytes
        Aggregate regular-file bytes in the closed after-process workspace snapshot.
    peak_resident_bytes
        Observed nonnegative peak resident bytes, or ``None`` when unavailable. The
        current local runner rejects finite peak-RSS ceilings before process entry and
        records ``None``.
    observer_version
        Nonempty identity of the process-observation implementation.
    """

    identity: QuantumEspressoProcessObservationIdentity
    execution_input_identity: QuantumEspressoExecutionInputIdentity
    executable_configuration_identity: QuantumEspressoExecutableConfigurationIdentity
    preparation_identity: QuantumEspressoPreparationIdentity
    attempt_identity: AttemptIdentity
    argv_content_identity: ArtifactContentIdentity
    termination: QuantumEspressoProcessTermination
    wall_duration_nanoseconds: int
    stdout: QuantumEspressoStreamObservation
    stderr: QuantumEspressoStreamObservation
    before_snapshot_identity: ArtifactManifestIdentity
    after_snapshot_identity: ArtifactManifestIdentity
    created_entry_count: int
    created_total_bytes: int
    peak_resident_bytes: int | None
    observer_version: str

    def __post_init__(self) -> None:
        expected = (
            (self.identity, QuantumEspressoProcessObservationIdentity, "identity"),
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
            (
                self.preparation_identity,
                QuantumEspressoPreparationIdentity,
                "preparation_identity",
            ),
            (self.attempt_identity, AttemptIdentity, "attempt_identity"),
            (
                self.argv_content_identity,
                ArtifactContentIdentity,
                "argv_content_identity",
            ),
            (self.stdout, QuantumEspressoStreamObservation, "stdout"),
            (self.stderr, QuantumEspressoStreamObservation, "stderr"),
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
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        termination_types = (
            QuantumEspressoNormalProcessExit,
            QuantumEspressoProcessSignalTermination,
            QuantumEspressoProcessTimeout,
        )
        if type(self.termination) not in termination_types:
            raise TypeError("termination must be a closed process-termination variant")
        if self.stdout.channel is not QuantumEspressoDiagnosticChannel.STDOUT:
            raise ValueError("stdout observation must use the stdout channel")
        if self.stderr.channel is not QuantumEspressoDiagnosticChannel.STDERR:
            raise ValueError("stderr observation must use the stderr channel")
        for name in (
            "wall_duration_nanoseconds",
            "created_entry_count",
            "created_total_bytes",
        ):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
            if not 0 <= value <= _MAX_U64:
                raise ValueError(f"{name} must be in the unsigned 64-bit range")
        peak = self.peak_resident_bytes
        if peak is not None:
            if type(peak) is not int:
                raise TypeError("peak_resident_bytes must be a built-in int or None")
            if not 0 <= peak <= _MAX_U64:
                raise ValueError(
                    "peak_resident_bytes must be in the unsigned 64-bit range"
                )
        if type(self.observer_version) is not str:
            raise TypeError("observer_version must be a built-in str")
        if not self.observer_version:
            raise ValueError("observer_version must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoDiagnosticObservation:
    """Identify one diagnostic by exact stream span and classified disposition.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    channel
        Independent stdout or stderr channel.
    byte_start
        Zero-based inclusive byte offset in the identified stream.
    byte_end
        Zero-based exclusive byte offset in the identified stream.
    stream_content_identity
        Exact nominal identity retained for cross-record correlation.
    span_content_identity
        Exact nominal identity retained for cross-record correlation.
    signature_identity
        Exact nominal identity retained for cross-record correlation.
    disposition
        Closed admission disposition for this result.
    sanitized_summary
        Bounded diagnostic meaning without raw-path or scientific claims.
    claim_boundary
        Nonempty immutable statements limiting evidentiary interpretation.
    """

    identity: QuantumEspressoDiagnosticObservationIdentity
    channel: QuantumEspressoDiagnosticChannel
    byte_start: int
    byte_end: int
    stream_content_identity: ArtifactContentIdentity
    span_content_identity: ArtifactContentIdentity
    signature_identity: str | None
    disposition: QuantumEspressoDiagnosticDisposition
    sanitized_summary: str
    claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.identity) is not QuantumEspressoDiagnosticObservationIdentity:
            raise TypeError(
                "identity must be QuantumEspressoDiagnosticObservationIdentity"
            )
        if type(self.channel) is not QuantumEspressoDiagnosticChannel:
            raise TypeError("channel must be QuantumEspressoDiagnosticChannel")
        for name in ("byte_start", "byte_end"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
            if not 0 <= value <= _MAX_U64:
                raise ValueError(f"{name} must be in the unsigned 64-bit range")
        if self.byte_end <= self.byte_start:
            raise ValueError("diagnostic byte range must be nonempty")
        if type(self.stream_content_identity) is not ArtifactContentIdentity:
            raise TypeError("stream_content_identity must be ArtifactContentIdentity")
        if type(self.span_content_identity) is not ArtifactContentIdentity:
            raise TypeError("span_content_identity must be ArtifactContentIdentity")
        if self.byte_end > self.stream_content_identity.byte_count:
            raise ValueError("diagnostic byte range exceeds the stream byte count")
        if self.span_content_identity.byte_count != self.byte_end - self.byte_start:
            raise ValueError("span byte count must equal the diagnostic byte range")
        if self.signature_identity is not None:
            if type(self.signature_identity) is not str:
                raise TypeError("signature_identity must be a built-in str or None")
            if not self.signature_identity:
                raise ValueError("signature_identity must not be empty")
        if type(self.disposition) is not QuantumEspressoDiagnosticDisposition:
            raise TypeError("disposition must be QuantumEspressoDiagnosticDisposition")
        if (self.disposition is QuantumEspressoDiagnosticDisposition.UNRESOLVED) != (
            self.signature_identity is None
        ):
            raise ValueError(
                "unresolved diagnostics alone must omit signature_identity"
            )
        if type(self.sanitized_summary) is not str:
            raise TypeError("sanitized_summary must be a built-in str")
        if not self.sanitized_summary:
            raise ValueError("sanitized_summary must not be empty")
        if type(self.claim_boundary) is not tuple or any(
            type(value) is not str for value in self.claim_boundary
        ):
            raise TypeError("claim_boundary must be a tuple of built-in str values")
        if not self.claim_boundary or any(not value for value in self.claim_boundary):
            raise ValueError("claim_boundary must contain nonempty strings")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoOutputMarkerObservation:
    """Identify one recognized completion marker by its exact stream span.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    channel
        Independent stdout or stderr channel.
    byte_start
        Zero-based inclusive byte offset in the identified stream.
    byte_end
        Zero-based exclusive byte offset in the identified stream.
    stream_content_identity
        Exact nominal identity retained for cross-record correlation.
    span_content_identity
        Exact nominal identity retained for cross-record correlation.
    signature_identity
        Exact nominal identity retained for cross-record correlation.
    """

    identity: QuantumEspressoOutputMarkerObservationIdentity
    channel: QuantumEspressoDiagnosticChannel
    byte_start: int
    byte_end: int
    stream_content_identity: ArtifactContentIdentity
    span_content_identity: ArtifactContentIdentity
    signature_identity: str

    def __post_init__(self) -> None:
        if type(self.identity) is not QuantumEspressoOutputMarkerObservationIdentity:
            raise TypeError(
                "identity must be QuantumEspressoOutputMarkerObservationIdentity"
            )
        if type(self.channel) is not QuantumEspressoDiagnosticChannel:
            raise TypeError("channel must be QuantumEspressoDiagnosticChannel")
        for name in ("byte_start", "byte_end"):
            value = getattr(self, name)
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int excluding bool")
            if not 0 <= value <= _MAX_U64:
                raise ValueError(f"{name} must be in the unsigned 64-bit range")
        if self.byte_end <= self.byte_start:
            raise ValueError("marker byte range must be nonempty")
        if type(self.stream_content_identity) is not ArtifactContentIdentity:
            raise TypeError("stream_content_identity must be ArtifactContentIdentity")
        if type(self.span_content_identity) is not ArtifactContentIdentity:
            raise TypeError("span_content_identity must be ArtifactContentIdentity")
        if self.byte_end > self.stream_content_identity.byte_count:
            raise ValueError("marker byte range exceeds the stream byte count")
        if self.span_content_identity.byte_count != self.byte_end - self.byte_start:
            raise ValueError("span byte count must equal the marker byte range")
        if type(self.signature_identity) is not str:
            raise TypeError("signature_identity must be a built-in str")
        if not self.signature_identity:
            raise ValueError("signature_identity must not be empty")


class QuantumEspressoDiagnosticReportKind(StrEnum):
    """Closed aggregate diagnostic-report kinds."""

    CLEAR = "clear"
    FATAL = "fatal"
    UNRESOLVED = "unresolved"
    CONTRADICTORY = "contradictory"


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoDiagnosticReport:
    """Record version-bound classification of both exact process streams.

    Attributes
    ----------
    identity
        Exact nominal identity retained for cross-record correlation.
    classifier_identity
        Exact nominal identity retained for cross-record correlation.
    executable_configuration_identity
        Exact nominal identity retained for cross-record correlation.
    executable_kind
        Closed real-executable or deterministic-fixture namespace.
    program
        Closed Quantum ESPRESSO program role.
    program_version
        Exact admitted executable program version string.
    stdout_content_identity
        Exact nominal identity retained for cross-record correlation.
    stderr_content_identity
        Exact nominal identity retained for cross-record correlation.
    observations
        Canonical immutable diagnostic-observation tuple.
    completion_markers
        Canonical immutable completion-marker tuple.
    kind
        Closed aggregate report or outcome kind.
    claim_boundary
        Nonempty immutable statements limiting evidentiary interpretation.
    """

    identity: QuantumEspressoDiagnosticReportIdentity
    classifier_identity: QuantumEspressoDiagnosticClassifierIdentity
    executable_configuration_identity: QuantumEspressoExecutableConfigurationIdentity
    executable_kind: QuantumEspressoExecutableKind
    program: QuantumEspressoProgram
    program_version: str
    stdout_content_identity: ArtifactContentIdentity
    stderr_content_identity: ArtifactContentIdentity
    observations: tuple[QuantumEspressoDiagnosticObservation, ...]
    completion_markers: tuple[QuantumEspressoOutputMarkerObservation, ...]
    kind: QuantumEspressoDiagnosticReportKind
    claim_boundary: tuple[str, ...]

    def __post_init__(self) -> None:
        expected = (
            (self.identity, QuantumEspressoDiagnosticReportIdentity, "identity"),
            (
                self.classifier_identity,
                QuantumEspressoDiagnosticClassifierIdentity,
                "classifier_identity",
            ),
            (
                self.executable_configuration_identity,
                QuantumEspressoExecutableConfigurationIdentity,
                "executable_configuration_identity",
            ),
            (
                self.executable_kind,
                QuantumEspressoExecutableKind,
                "executable_kind",
            ),
            (self.program, QuantumEspressoProgram, "program"),
            (
                self.stdout_content_identity,
                ArtifactContentIdentity,
                "stdout_content_identity",
            ),
            (
                self.stderr_content_identity,
                ArtifactContentIdentity,
                "stderr_content_identity",
            ),
            (self.kind, QuantumEspressoDiagnosticReportKind, "kind"),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.program_version) is not str:
            raise TypeError("program_version must be a built-in str")
        if not self.program_version:
            raise ValueError("program_version must not be empty")
        fixture_version = self.program_version.startswith("fixture-")
        if (
            self.executable_kind is QuantumEspressoExecutableKind.DETERMINISTIC_FIXTURE
        ) != fixture_version:
            raise ValueError(
                "program_version namespace must agree with executable_kind"
            )
        observations = self.observations
        if type(observations) is not tuple or any(
            type(value) is not QuantumEspressoDiagnosticObservation
            for value in observations
        ):
            raise TypeError(
                "observations must be a tuple of QuantumEspressoDiagnosticObservation"
            )
        expected_observations = tuple(
            sorted(
                observations,
                key=lambda value: (
                    value.channel.value,
                    value.byte_start,
                    value.byte_end,
                    value.identity.value,
                ),
            )
        )
        if observations != expected_observations or len(
            {value.identity for value in observations}
        ) != len(observations):
            raise ValueError("observations must be unique and canonically ordered")
        markers = self.completion_markers
        if type(markers) is not tuple or any(
            type(value) is not QuantumEspressoOutputMarkerObservation
            for value in markers
        ):
            raise TypeError(
                "completion_markers must be a tuple of "
                "QuantumEspressoOutputMarkerObservation"
            )
        expected_markers = tuple(
            sorted(
                markers,
                key=lambda value: (
                    value.channel.value,
                    value.byte_start,
                    value.byte_end,
                    value.identity.value,
                ),
            )
        )
        marker_identities = {value.identity for value in markers}
        if markers != expected_markers or len(marker_identities) != len(markers):
            raise ValueError(
                "completion_markers must be unique and canonically ordered"
            )
        for observation in observations:
            expected_stream = (
                self.stdout_content_identity
                if observation.channel is QuantumEspressoDiagnosticChannel.STDOUT
                else self.stderr_content_identity
            )
            if observation.stream_content_identity != expected_stream:
                raise ValueError(
                    "diagnostic observation must identify its report stream"
                )
        for marker in markers:
            expected_stream = (
                self.stdout_content_identity
                if marker.channel is QuantumEspressoDiagnosticChannel.STDOUT
                else self.stderr_content_identity
            )
            if marker.stream_content_identity != expected_stream:
                raise ValueError("completion marker must identify its report stream")
        dispositions = {value.disposition for value in observations}
        fatal = QuantumEspressoDiagnosticDisposition.FATAL in dispositions
        secondary_fatal = (
            QuantumEspressoDiagnosticDisposition.SECONDARY_FATAL in dispositions
        )
        unresolved = QuantumEspressoDiagnosticDisposition.UNRESOLVED in dispositions
        contradictory = (fatal and bool(markers)) or (secondary_fatal and not fatal)
        valid_kind = {
            QuantumEspressoDiagnosticReportKind.CLEAR: dispositions
            <= {QuantumEspressoDiagnosticDisposition.NONBLOCKING},
            QuantumEspressoDiagnosticReportKind.FATAL: (
                fatal and not unresolved and not markers and not contradictory
            ),
            QuantumEspressoDiagnosticReportKind.UNRESOLVED: (
                unresolved and not contradictory
            ),
            QuantumEspressoDiagnosticReportKind.CONTRADICTORY: contradictory,
        }[self.kind]
        if not valid_kind:
            raise ValueError("diagnostic report kind does not match its observations")
        if type(self.claim_boundary) is not tuple or any(
            type(value) is not str for value in self.claim_boundary
        ):
            raise TypeError("claim_boundary must be a tuple of built-in str values")
        if not self.claim_boundary or any(not value for value in self.claim_boundary):
            raise ValueError("claim_boundary must contain nonempty strings")


class QuantumEspressoProcessFailureKind(StrEnum):
    """Closed determinate process-failure reasons."""

    NONZERO_EXIT = "nonzero_exit"
    SIGNAL = "signal"
    TIMEOUT = "timeout"


@dataclass(frozen=True, slots=True)
class QuantumEspressoCompletedOutcome:
    """Represent mechanically complete QE output eligible for later evaluation.

    Attributes
    ----------
    completion_marker_identities
        Canonical immutable tuple of exact nominal identities.
    """

    completion_marker_identities: tuple[
        QuantumEspressoOutputMarkerObservationIdentity, ...
    ]

    def __post_init__(self) -> None:
        values = self.completion_marker_identities
        if type(values) is not tuple or any(
            type(value) is not QuantumEspressoOutputMarkerObservationIdentity
            for value in values
        ):
            raise TypeError(
                "completion_marker_identities must be a tuple of "
                "QuantumEspressoOutputMarkerObservationIdentity"
            )
        if not values:
            raise ValueError("completion_marker_identities must not be empty")
        if values != tuple(sorted(values, key=lambda value: value.value)) or len(
            set(values)
        ) != len(values):
            raise ValueError(
                "completion_marker_identities must be unique and lexically sorted"
            )


@dataclass(frozen=True, slots=True)
class QuantumEspressoCalculatorFailedOutcome:
    """Represent internally consistent calculator-reported fatal output.

    Attributes
    ----------
    fatal_diagnostic_identities
        Canonical immutable tuple of exact nominal identities.
    """

    fatal_diagnostic_identities: tuple[
        QuantumEspressoDiagnosticObservationIdentity, ...
    ]

    def __post_init__(self) -> None:
        values = self.fatal_diagnostic_identities
        if type(values) is not tuple or any(
            type(value) is not QuantumEspressoDiagnosticObservationIdentity
            for value in values
        ):
            raise TypeError(
                "fatal_diagnostic_identities must be a tuple of "
                "QuantumEspressoDiagnosticObservationIdentity"
            )
        if not values:
            raise ValueError("fatal_diagnostic_identities must not be empty")
        if values != tuple(sorted(values, key=lambda value: value.value)) or len(
            set(values)
        ) != len(values):
            raise ValueError(
                "fatal_diagnostic_identities must be unique and lexically sorted"
            )


@dataclass(frozen=True, slots=True)
class QuantumEspressoProcessFailedOutcome:
    """Represent a determinate process-level failure with unknown retryability.

    Attributes
    ----------
    reason
        Closed mechanical process-failure reason.
    """

    reason: QuantumEspressoProcessFailureKind

    def __post_init__(self) -> None:
        if type(self.reason) is not QuantumEspressoProcessFailureKind:
            raise TypeError("reason must be QuantumEspressoProcessFailureKind")


@dataclass(frozen=True, slots=True)
class QuantumEspressoDiagnosticUnresolvedOutcome:
    """Represent diagnostic or cross-observation state requiring resolution.

    Attributes
    ----------
    diagnostic_identities
        Canonical immutable tuple of exact nominal identities.
    reason_identities
        Canonical immutable tuple of exact nominal identities.
    """

    diagnostic_identities: tuple[QuantumEspressoDiagnosticObservationIdentity, ...]
    reason_identities: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        values = self.diagnostic_identities
        if type(values) is not tuple or any(
            type(value) is not QuantumEspressoDiagnosticObservationIdentity
            for value in values
        ):
            raise TypeError(
                "diagnostic_identities must be a tuple of "
                "QuantumEspressoDiagnosticObservationIdentity"
            )
        if values != tuple(sorted(values, key=lambda value: value.value)) or len(
            set(values)
        ) != len(values):
            raise ValueError(
                "diagnostic_identities must be unique and lexically sorted"
            )
        reasons = self.reason_identities
        if type(reasons) is not tuple or any(
            type(value) is not str for value in reasons
        ):
            raise TypeError("reason_identities must be a tuple of built-in str values")
        if any(not value for value in reasons):
            raise ValueError("reason_identities must contain nonempty values")
        if reasons != tuple(sorted(reasons)) or len(set(reasons)) != len(reasons):
            raise ValueError("reason_identities must be unique and lexically sorted")
        if not values and not reasons:
            raise ValueError(
                "unresolved outcome requires a diagnostic or reason identity"
            )


type QuantumEspressoCalculatorOutcome = (
    QuantumEspressoCompletedOutcome
    | QuantumEspressoCalculatorFailedOutcome
    | QuantumEspressoProcessFailedOutcome
    | QuantumEspressoDiagnosticUnresolvedOutcome
)


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoOperationResultEvidence:
    """Collect exact correlated evidence shared by one QE program result.

    Parameters
    ----------
    execution_input
        Exact immutable QE input and its Task-definition, Task-instance, activation,
        operation, and attempt producer correlations.
    process_observation, diagnostic_report, calculator_outcome
        Closed process, exact-stream diagnostic, and resolved calculator evidence.
    native_output_manifest_identity, native_output_entry_identities
        Exact verified native-output candidate references.
    terminal_record_identity
        Exact private terminal record published before result construction.

    Notes
    -----
    This DataObject is not itself a Workflow ResultObject and carries no continuation,
    retry, or scientific-acceptance decision.
    """

    execution_input: QuantumEspressoExecutionInput
    process_observation: QuantumEspressoProcessObservation
    diagnostic_report: QuantumEspressoDiagnosticReport
    calculator_outcome: QuantumEspressoCalculatorOutcome
    native_output_manifest_identity: ArtifactManifestIdentity
    native_output_entry_identities: tuple[ArtifactManifestEntryIdentity, ...]
    terminal_record_identity: QuantumEspressoTerminalRecordIdentity

    def __post_init__(self) -> None:
        expected = (
            (self.execution_input, QuantumEspressoExecutionInput, "execution_input"),
            (
                self.process_observation,
                QuantumEspressoProcessObservation,
                "process_observation",
            ),
            (
                self.diagnostic_report,
                QuantumEspressoDiagnosticReport,
                "diagnostic_report",
            ),
            (
                self.native_output_manifest_identity,
                ArtifactManifestIdentity,
                "native_output_manifest_identity",
            ),
            (
                self.terminal_record_identity,
                QuantumEspressoTerminalRecordIdentity,
                "terminal_record_identity",
            ),
        )
        for value, nominal_type, name in expected:
            if type(value) is not nominal_type:
                raise TypeError(f"{name} must be {nominal_type.__name__}")
        if type(self.calculator_outcome) not in (
            QuantumEspressoCompletedOutcome,
            QuantumEspressoCalculatorFailedOutcome,
            QuantumEspressoProcessFailedOutcome,
            QuantumEspressoDiagnosticUnresolvedOutcome,
        ):
            raise TypeError("calculator_outcome must be a closed QE outcome variant")
        entries = self.native_output_entry_identities
        if type(entries) is not tuple or any(
            type(value) is not ArtifactManifestEntryIdentity for value in entries
        ):
            raise TypeError(
                "native_output_entry_identities must contain "
                "ArtifactManifestEntryIdentity values"
            )
        if not entries:
            raise ValueError("native_output_entry_identities must not be empty")
        if entries != tuple(sorted(entries, key=lambda value: value.value)) or len(
            set(entries)
        ) != len(entries):
            raise ValueError(
                "native_output_entry_identities must be unique and lexically sorted"
            )
        process = self.process_observation
        report = self.diagnostic_report
        if (
            process.execution_input_identity != self.execution_input.identity
            or process.attempt_identity != self.execution_input.attempt_identity
            or report.executable_configuration_identity
            != process.executable_configuration_identity
            or report.stdout_content_identity != process.stdout.content_identity
            or report.stderr_content_identity != process.stderr.content_identity
        ):
            raise ValueError("operation result evidence correlations must agree")
        outcome = self.calculator_outcome
        report_diagnostics = {value.identity for value in report.observations}
        if (
            report.kind
            in (
                QuantumEspressoDiagnosticReportKind.UNRESOLVED,
                QuantumEspressoDiagnosticReportKind.CONTRADICTORY,
            )
            and type(outcome) is not QuantumEspressoDiagnosticUnresolvedOutcome
        ):
            raise ValueError(
                "unresolved or contradictory reports require unresolved outcomes"
            )
        if type(outcome) is QuantumEspressoCompletedOutcome:
            report_markers = tuple(
                sorted(
                    (value.identity for value in report.completion_markers),
                    key=lambda value: value.value,
                )
            )
            if (
                outcome.completion_marker_identities != report_markers
                or report.kind is not QuantumEspressoDiagnosticReportKind.CLEAR
                or type(process.termination) is not QuantumEspressoNormalProcessExit
                or process.termination.exit_code != 0
            ):
                raise ValueError(
                    "completed outcome must agree with clear zero-exit report markers"
                )
        elif type(outcome) is QuantumEspressoCalculatorFailedOutcome:
            report_fatal = tuple(
                sorted(
                    (
                        value.identity
                        for value in report.observations
                        if value.disposition
                        is QuantumEspressoDiagnosticDisposition.FATAL
                    ),
                    key=lambda value: value.value,
                )
            )
            if (
                outcome.fatal_diagnostic_identities != report_fatal
                or report.kind is not QuantumEspressoDiagnosticReportKind.FATAL
                or type(process.termination) is not QuantumEspressoNormalProcessExit
            ):
                raise ValueError(
                    "calculator-failed outcome diagnostics must equal report fatals"
                )
        elif type(outcome) is QuantumEspressoProcessFailedOutcome:
            termination = process.termination
            expected_reason = (
                QuantumEspressoProcessFailureKind.SIGNAL
                if type(termination) is QuantumEspressoProcessSignalTermination
                else QuantumEspressoProcessFailureKind.TIMEOUT
                if type(termination) is QuantumEspressoProcessTimeout
                else QuantumEspressoProcessFailureKind.NONZERO_EXIT
                if type(termination) is QuantumEspressoNormalProcessExit
                and termination.exit_code != 0
                else None
            )
            if outcome.reason is not expected_reason or (
                outcome.reason is QuantumEspressoProcessFailureKind.NONZERO_EXIT
                and report.kind is not QuantumEspressoDiagnosticReportKind.CLEAR
            ):
                raise ValueError(
                    "process-failed outcome must agree with process termination"
                )
        else:
            assert type(outcome) is QuantumEspressoDiagnosticUnresolvedOutcome
            if any(
                identity not in report_diagnostics
                for identity in outcome.diagnostic_identities
            ):
                raise ValueError(
                    "unresolved outcome diagnostics must belong to the report"
                )


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoPwResult:
    """Represent one immutable result from the configured QE ``pw`` program role.

    Parameters
    ----------
    identity
        Exact Workflow ResultObject identity.
    evidence
        Correlated immutable QE process, diagnostic, outcome, and artifact evidence.
    contract_version
        Nonempty version identity for this result contract.
    """

    identity: ResultObjectIdentity
    evidence: QuantumEspressoOperationResultEvidence
    contract_version: str

    def __post_init__(self) -> None:
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.evidence) is not QuantumEspressoOperationResultEvidence:
            raise TypeError("evidence must be QuantumEspressoOperationResultEvidence")
        if self.evidence.diagnostic_report.program is not QuantumEspressoProgram.PW:
            raise ValueError("pw result evidence must use the pw program role")
        if type(self.contract_version) is not str:
            raise TypeError("contract_version must be a built-in str")
        if not self.contract_version:
            raise ValueError("contract_version must not be empty")


@dataclass(frozen=True, slots=True, kw_only=True)
class QuantumEspressoBandsResult:
    """Represent an immutable result from the configured QE ``bands`` program role.

    Parameters
    ----------
    identity
        Exact Workflow ResultObject identity.
    evidence
        Correlated immutable QE process, diagnostic, outcome, and artifact evidence.
    contract_version
        Nonempty version identity for this result contract.
    """

    identity: ResultObjectIdentity
    evidence: QuantumEspressoOperationResultEvidence
    contract_version: str

    def __post_init__(self) -> None:
        if type(self.identity) is not ResultObjectIdentity:
            raise TypeError("identity must be ResultObjectIdentity")
        if type(self.evidence) is not QuantumEspressoOperationResultEvidence:
            raise TypeError("evidence must be QuantumEspressoOperationResultEvidence")
        if self.evidence.diagnostic_report.program is not QuantumEspressoProgram.BANDS:
            raise ValueError("bands result evidence must use the bands program role")
        if type(self.contract_version) is not str:
            raise TypeError("contract_version must be a built-in str")
        if not self.contract_version:
            raise ValueError("contract_version must not be empty")


type QuantumEspressoOperationResult = (
    QuantumEspressoPwResult | QuantumEspressoBandsResult
)
