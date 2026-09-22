"""Architecture-v2 immutable harness configuration and canonical JSON actions.

The resolver consumes only caller-supplied paths and bytes. It performs no file,
environment, repository, database, network, clock, or subprocess operation. A valid
configuration is composition data and grants no development or execution authority.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from typing import Never, cast

from .identity import ContentIdentity, SnapshotIdentity
from .pi import PiHarnessConfiguration, PiHarnessConfigurationDeserializer

ResourcePath = str

_DRIVE_RE = re.compile(r"^[A-Za-z]:")
_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{i}" for i in range(1, 10)),
    *(f"LPT{i}" for i in range(1, 10)),
}
_SOURCE_ROLES = ("harness_configuration_source", "pi_project_settings")
_FINDING_CODES = {
    "HARNESS_CONFIGURATION.SOURCE_INVALID",
    "HARNESS_CONFIGURATION.PI_PATH_MISMATCH",
    "HARNESS_CONFIGURATION.PI_SETTINGS_INVALID",
    "HARNESS_CONFIGURATION.RESOURCE_MANIFEST_OUTSIDE_ROOT",
}
_SNAPSHOT_FRAME = b"ksdft2effmass.harness.configuration.snapshot.v1\0"
_HARNESS_CONFIGURATION_SOURCE_PATH = "harness/configuration.json"


class _HarnessResourcePathValidator:
    """Apply the shared lexical Harness resource-path policy without file I/O."""

    __slots__ = ()

    def execute(self, value: str, field: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{field} must be a built-in str")
        if not value:
            raise ValueError(f"{field} must be nonempty")
        if value.startswith("/") or _DRIVE_RE.match(value):
            raise ValueError(f"{field} must be root-relative")
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError(f"{field} must use Unicode NFC")
        if "\\" in value or value.endswith("/") or "//" in value:
            raise ValueError(f"{field} is not a normalized resource path")
        for part in value.split("/"):
            if part in {"", ".", ".."}:
                raise ValueError(f"{field} contains a traversal or empty segment")
            if part.split(".", 1)[0].upper() in _DEVICE_NAMES:
                raise ValueError(f"{field} contains a reserved device name")
        if any(
            ord(char) < 32
            or 0x7F <= ord(char) <= 0x9F
            or ord(char) in {0x2028, 0x2029}
            or 0xD800 <= ord(char) <= 0xDFFF
            for char in value
        ):
            raise ValueError(f"{field} contains a prohibited character")
        return value


@dataclass(frozen=True, slots=True)
class HumanReviewConfiguration:
    """Destinations for transient review packets and optional decision projections."""

    packet_artifact_root: ResourcePath
    decision_projection_root: ResourcePath | None

    def __post_init__(self) -> None:
        _HarnessResourcePathValidator().execute(
            self.packet_artifact_root, "packet_artifact_root"
        )
        if self.decision_projection_root is not None:
            _HarnessResourcePathValidator().execute(
                self.decision_projection_root, "decision_projection_root"
            )
        if self.packet_artifact_root == self.decision_projection_root:
            raise ValueError("human_review paths must be distinct")


@dataclass(frozen=True, slots=True)
class HarnessPersistenceConfiguration:
    """Root-relative development state and deterministic projection paths."""

    state_database_path: ResourcePath
    sql_export_path: ResourcePath
    projection_manifest_path: ResourcePath

    def __post_init__(self) -> None:
        for field, value in (
            ("state_database_path", self.state_database_path),
            ("sql_export_path", self.sql_export_path),
            ("projection_manifest_path", self.projection_manifest_path),
        ):
            _HarnessResourcePathValidator().execute(value, field)
        if (
            len(
                {
                    self.state_database_path,
                    self.sql_export_path,
                    self.projection_manifest_path,
                }
            )
            != 3
        ):
            raise ValueError("persistence paths must be distinct")


@dataclass(frozen=True, slots=True)
class PythonConformanceConfiguration:
    """Explicit maintained Python evidence inputs."""

    pyproject_path: ResourcePath
    test_root: ResourcePath
    profile_matrix_path: ResourcePath
    migration_map_path: ResourcePath

    def __post_init__(self) -> None:
        paths = (
            ("pyproject_path", self.pyproject_path),
            ("test_root", self.test_root),
            ("profile_matrix_path", self.profile_matrix_path),
            ("migration_map_path", self.migration_map_path),
        )
        for field, value in paths:
            _HarnessResourcePathValidator().execute(value, field)
        if len({value for _, value in paths}) != len(paths):
            raise ValueError("python_conformance paths must be distinct")


@dataclass(frozen=True, slots=True)
class HarnessResourceConfiguration:
    """Explicit generic and project-local harness resource inputs."""

    project_profile_path: ResourcePath
    generic_manifest_path: ResourcePath
    generic_root: ResourcePath
    local_manifest_path: ResourcePath
    local_root: ResourcePath

    def __post_init__(self) -> None:
        for field, value in (
            ("project_profile_path", self.project_profile_path),
            ("generic_manifest_path", self.generic_manifest_path),
            ("generic_root", self.generic_root),
            ("local_manifest_path", self.local_manifest_path),
            ("local_root", self.local_root),
        ):
            _HarnessResourcePathValidator().execute(value, field)


@dataclass(frozen=True, slots=True)
class TaskCatalogConfiguration:
    """Immutable categorized Task locations, without discovery or authority.

    Parameters
    ----------
    research_root : str
        Explicit repository-relative POSIX directory for research Tasks.
    simulation_root : str
        Explicit repository-relative POSIX directory for simulation Tasks.
    software_root : str
        Explicit repository-relative POSIX directory for software Tasks.

    Raises
    ------
    TypeError
        A root is not an exact built-in string.
    ValueError
        A root violates the existing Harness resource-path contract, or two
        category roots are equal or nested, including case-folded aliases.

    Notes
    -----
    Roots are nonempty NFC strings without absolute/drive prefixes, backslashes,
    empty or traversal segments, reserved device names, controls or surrogates.
    Inputs are never normalized silently. No defaults, filesystem checks, Task
    classification, execution permissions or scientific parameters are supplied.
    Near-prefix siblings are distinct; actual filesystem aliasing and confinement
    remain the responsibility of the file-reading boundary.
    """

    research_root: ResourcePath
    simulation_root: ResourcePath
    software_root: ResourcePath

    def __post_init__(self) -> None:
        paths = (
            ("research_root", self.research_root),
            ("simulation_root", self.simulation_root),
            ("software_root", self.software_root),
        )
        for field, root in paths:
            _HarnessResourcePathValidator().execute(root, field)
        folded = tuple(root.casefold() for _, root in paths)
        for index, root in enumerate(folded):
            for other in folded[index + 1 :]:
                if (
                    root == other
                    or root.startswith(other + "/")
                    or other.startswith(root + "/")
                ):
                    raise ValueError("Task catalog roots must not overlap or alias")


@dataclass(frozen=True, slots=True)
class HarnessCatalogConfiguration:
    """Explicit categorized Task roots and other Harness catalog roots.

    Parameters
    ----------
    task_catalog : TaskCatalogConfiguration
        Required categorized research, simulation and software Task roots.
    agent_roots : tuple of str
        Nonempty, strictly sorted unique agent catalog roots.
    checkpoint_roots : tuple of str
        Nonempty, strictly sorted unique checkpoint catalog roots.
    skill_roots : tuple of str
        Nonempty, strictly sorted unique skill catalog roots.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        A root is invalid, a root tuple is empty/unsorted/nonunique, or roots
        repeat across catalogs.

    Notes
    -----
    All paths obey the Harness resource-path contract. Categorized Task roots
    additionally reject case-folded equality and ancestor/descendant overlap.
    Other catalogs retain their existing exact distinctness rules. This value
    does not discover files or grant authority.
    """

    task_catalog: TaskCatalogConfiguration
    agent_roots: tuple[ResourcePath, ...]
    checkpoint_roots: tuple[ResourcePath, ...]
    skill_roots: tuple[ResourcePath, ...]

    def __post_init__(self) -> None:
        if type(self.task_catalog) is not TaskCatalogConfiguration:
            raise TypeError("task_catalog must be TaskCatalogConfiguration")
        all_roots = [
            self.task_catalog.research_root,
            self.task_catalog.simulation_root,
            self.task_catalog.software_root,
        ]
        for field, roots in (
            ("agent_roots", self.agent_roots),
            ("checkpoint_roots", self.checkpoint_roots),
            ("skill_roots", self.skill_roots),
        ):
            if type(roots) is not tuple:
                raise TypeError(f"{field} must be a tuple")
            if not roots:
                raise ValueError(f"{field} must be nonempty")
            for root in roots:
                _HarnessResourcePathValidator().execute(root, f"{field} item")
            if roots != tuple(sorted(set(roots))):
                raise ValueError(f"{field} must be strictly sorted and unique")
            all_roots.extend(roots)
        if len(all_roots) != len(set(all_roots)):
            raise ValueError("catalog roots may not repeat across categories")


@dataclass(frozen=True, slots=True)
class HarnessConfigurationSource:
    """Immutable human-authored Harness configuration, without ambient inputs.

    Parameters
    ----------
    schema_version : int
        Exact built-in integer 2 for categorized Task roots;
        booleans, numeric strings and other versions are rejected.
    pi_settings_path : str
        Explicit normalized root-relative path to independently Pi-owned settings.
    human_review : HumanReviewConfiguration
        Immutable review-packet and optional projection locations.
    persistence : HarnessPersistenceConfiguration
        Immutable development-state and generated-projection paths.
    python_conformance : PythonConformanceConfiguration
        Explicit Python evidence configuration paths.
    resources : HarnessResourceConfiguration
        Explicit generic/local resource manifests, roots and project profile.
    catalogs : HarnessCatalogConfiguration
        Exactly one Task layout, agreeing with ``schema_version``, plus existing
        agent, checkpoint and skill roots.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        A version/path is invalid or the version disagrees with the Task layout.

    Notes
    -----
    No format inference, filesystem access, scientific settings or authority is
    encoded. The live repository need not use every representable format.
    """

    schema_version: int
    pi_settings_path: ResourcePath
    human_review: HumanReviewConfiguration
    persistence: HarnessPersistenceConfiguration
    python_conformance: PythonConformanceConfiguration
    resources: HarnessResourceConfiguration
    catalogs: HarnessCatalogConfiguration

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an int excluding bool")
        if self.schema_version != 2:
            raise ValueError("configuration schema_version must equal 2")
        _HarnessResourcePathValidator().execute(
            self.pi_settings_path, "pi_settings_path"
        )
        if type(self.human_review) is not HumanReviewConfiguration:
            raise TypeError("human_review must be HumanReviewConfiguration")
        if type(self.persistence) is not HarnessPersistenceConfiguration:
            raise TypeError("persistence must be HarnessPersistenceConfiguration")
        if type(self.python_conformance) is not PythonConformanceConfiguration:
            raise TypeError("python_conformance must be PythonConformanceConfiguration")
        if type(self.resources) is not HarnessResourceConfiguration:
            raise TypeError("resources must be HarnessResourceConfiguration")
        if type(self.catalogs) is not HarnessCatalogConfiguration:
            raise TypeError("catalogs must be HarnessCatalogConfiguration")


@dataclass(frozen=True, slots=True)
class HarnessConfiguration:
    """Immutable effective Harness configuration, distinct from source provenance.

    Parameters
    ----------
    schema_version : int
        Exact built-in integer 2 for categorized roots;
        booleans and numeric strings are not integers in this contract.
    pi : PiHarnessConfiguration
        Independently versioned, normalized Pi-owned consumed settings subset.
    human_review : HumanReviewConfiguration
        Immutable review-packet and optional projection locations.
    persistence : HarnessPersistenceConfiguration
        Immutable development-state and generated-projection paths.
    python_conformance : PythonConformanceConfiguration
        Explicit Python evidence configuration paths.
    resources : HarnessResourceConfiguration
        Explicit generic/local resource manifests, roots and project profile.
    catalogs : HarnessCatalogConfiguration
        Exactly one Task layout agreeing with the configuration version, plus
        agent, checkpoint and skill roots.

    Raises
    ------
    TypeError
        A field has the wrong exact semantic type.
    ValueError
        The version is unsupported or disagrees with the Task layout.

    Notes
    -----
    Source bindings and the version-1 framed snapshot identity belong to the
    resolution result, not this value's equality or canonical JSON. Configuration
    grants no execution authority and performs no file discovery.
    """

    schema_version: int
    pi: PiHarnessConfiguration
    human_review: HumanReviewConfiguration
    persistence: HarnessPersistenceConfiguration
    python_conformance: PythonConformanceConfiguration
    resources: HarnessResourceConfiguration
    catalogs: HarnessCatalogConfiguration

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an int excluding bool")
        if self.schema_version != 2:
            raise ValueError("configuration schema_version must equal 2")
        if type(self.pi) is not PiHarnessConfiguration:
            raise TypeError("pi must be PiHarnessConfiguration")
        if type(self.human_review) is not HumanReviewConfiguration:
            raise TypeError("human_review must be HumanReviewConfiguration")
        if type(self.persistence) is not HarnessPersistenceConfiguration:
            raise TypeError("persistence must be HarnessPersistenceConfiguration")
        if type(self.python_conformance) is not PythonConformanceConfiguration:
            raise TypeError("python_conformance must be PythonConformanceConfiguration")
        if type(self.resources) is not HarnessResourceConfiguration:
            raise TypeError("resources must be HarnessResourceConfiguration")
        if type(self.catalogs) is not HarnessCatalogConfiguration:
            raise TypeError("catalogs must be HarnessCatalogConfiguration")


@dataclass(frozen=True, slots=True)
class HarnessConfigurationSourceBinding:
    """Role, path, and exact content identity of one resolution input."""

    role: str
    path: ResourcePath
    content_identity: ContentIdentity

    def __post_init__(self) -> None:
        if type(self.role) is not str:
            raise TypeError("role must be a built-in str")
        if self.role not in _SOURCE_ROLES:
            raise ValueError("role is not a supported configuration source role")
        _HarnessResourcePathValidator().execute(self.path, "path")
        if type(self.content_identity) is not ContentIdentity:
            raise TypeError("content_identity must be ContentIdentity")


@dataclass(frozen=True, slots=True)
class HarnessConfigurationResolutionFinding:
    """One stable, sanitized configuration resolution finding."""

    code: str
    path: ResourcePath | None
    message: str

    def __post_init__(self) -> None:
        if type(self.code) is not str:
            raise TypeError("code must be a built-in str")
        if self.code not in _FINDING_CODES:
            raise ValueError("code is not a supported configuration finding code")
        if self.path is not None:
            _HarnessResourcePathValidator().execute(self.path, "path")
        if type(self.message) is not str:
            raise TypeError("message must be a built-in str")
        if not self.message or "\n" in self.message or "\r" in self.message:
            raise ValueError("message must be nonempty sanitized single-line text")


@dataclass(frozen=True, slots=True)
class HarnessConfigurationResolutionResult:
    """Closed success or failure result of exact-source configuration resolution."""

    schema_version: int
    status: str
    source_bindings: tuple[HarnessConfigurationSourceBinding, ...]
    snapshot_identity: SnapshotIdentity | None
    configuration: HarnessConfiguration | None
    findings: tuple[HarnessConfigurationResolutionFinding, ...]

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int:
            raise TypeError("schema_version must be an int excluding bool")
        if self.schema_version != 1:
            raise ValueError("resolution result schema_version must equal 1")
        if type(self.status) is not str:
            raise TypeError("status must be a built-in str")
        if self.status not in {"resolved", "failed"}:
            raise ValueError("status must be resolved or failed")
        if type(self.source_bindings) is not tuple:
            raise TypeError("source_bindings must be a tuple")
        if any(
            type(binding) is not HarnessConfigurationSourceBinding
            for binding in self.source_bindings
        ):
            raise TypeError("source_bindings contain a wrong value type")
        if tuple(binding.role for binding in self.source_bindings) != _SOURCE_ROLES:
            raise ValueError("source_bindings must contain source then Pi settings")
        if (
            self.snapshot_identity is not None
            and type(self.snapshot_identity) is not SnapshotIdentity
        ):
            raise TypeError("snapshot_identity must be SnapshotIdentity")
        if (
            self.configuration is not None
            and type(self.configuration) is not HarnessConfiguration
        ):
            raise TypeError("configuration must be HarnessConfiguration")
        if type(self.findings) is not tuple:
            raise TypeError("findings must be a tuple")
        if any(
            type(finding) is not HarnessConfigurationResolutionFinding
            for finding in self.findings
        ):
            raise TypeError("findings contain a wrong value type")
        if self.findings != tuple(
            sorted(
                set(self.findings),
                key=lambda finding: (finding.code, finding.path or "", finding.message),
            )
        ):
            raise ValueError("findings must be deterministically ordered and unique")
        if self.status == "resolved":
            if (
                self.snapshot_identity is None
                or self.configuration is None
                or self.findings
            ):
                raise ValueError(
                    "resolved result requires snapshot and configuration only"
                )
        elif (
            self.snapshot_identity is not None
            or self.configuration is not None
            or not self.findings
        ):
            raise ValueError("failed result requires findings and no resolved values")


type _JsonValue = (
    None | bool | int | float | str | list[_JsonValue] | dict[str, _JsonValue]
)


@dataclass(frozen=True, slots=True)
class _ConfigurationComponents:
    """Closed decoded sections shared by source and resolved wire records."""

    schema_version: int
    human_review: HumanReviewConfiguration
    persistence: HarnessPersistenceConfiguration
    python_conformance: PythonConformanceConfiguration
    resources: HarnessResourceConfiguration
    catalogs: HarnessCatalogConfiguration


class _HarnessConfigurationJsonCodec:
    """Own the shared strict JSON mechanics of both configuration formats."""

    __slots__ = ()

    @staticmethod
    def unique_members(pairs: list[tuple[str, _JsonValue]]) -> dict[str, _JsonValue]:
        result: dict[str, _JsonValue] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON member")
            result[key] = value
        return result

    @staticmethod
    def reject_constant(value: str) -> Never:
        raise ValueError(f"nonfinite JSON constant: {value}")

    @staticmethod
    def canonical(value: dict[str, _JsonValue]) -> bytes:
        return (
            json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
        ).encode("utf-8")

    def parse(self, payload: bytes) -> dict[str, _JsonValue]:
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("payload must contain UTF-8 JSON") from exc
        if text.startswith("\ufeff"):
            raise ValueError("UTF-8 BOM is prohibited")
        try:
            value = cast(
                _JsonValue,
                json.loads(
                    text,
                    object_pairs_hook=self.unique_members,
                    parse_constant=self.reject_constant,
                ),
            )
        except ValueError as exc:
            raise ValueError("payload must contain strict unique-key JSON") from exc
        if not isinstance(value, dict):
            raise TypeError("top-level JSON value must be an object")
        return value

    @staticmethod
    def members(
        value: _JsonValue, names: tuple[str, ...], field: str
    ) -> dict[str, _JsonValue]:
        if not isinstance(value, dict):
            raise TypeError(f"{field} must be an object")
        if tuple(value) != names:
            raise ValueError(f"{field} must contain exact canonical members in order")
        return value

    @staticmethod
    def string(value: _JsonValue, field: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{field} must be a built-in str")
        return value

    @staticmethod
    def integer(value: _JsonValue, field: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{field} must be an int excluding bool")
        return value

    def optional_string(self, value: _JsonValue, field: str) -> str | None:
        return None if value is None else self.string(value, field)

    def string_tuple(self, value: _JsonValue, field: str) -> tuple[str, ...]:
        if not isinstance(value, list):
            raise TypeError(f"{field} must be an array")
        return tuple(self.string(item, f"{field} item") for item in value)

    def source_mapping(
        self, source: HarnessConfigurationSource
    ) -> dict[str, _JsonValue]:
        return {
            "schema_version": source.schema_version,
            "pi_settings_path": source.pi_settings_path,
            **self.component_mapping(source),
        }

    def configuration_mapping(
        self, configuration: HarnessConfiguration
    ) -> dict[str, _JsonValue]:
        return {
            "schema_version": configuration.schema_version,
            "pi": {
                "schema_version": configuration.pi.schema_version,
                "disabled_agent_runtime_names": list(
                    configuration.pi.disabled_agent_runtime_names
                ),
            },
            **self.component_mapping(configuration),
        }

    def component_mapping(
        self, source: HarnessConfigurationSource | HarnessConfiguration
    ) -> dict[str, _JsonValue]:
        task_catalog = source.catalogs.task_catalog
        catalogs: dict[str, _JsonValue] = {
            "task_catalog": {
                "research_root": task_catalog.research_root,
                "simulation_root": task_catalog.simulation_root,
                "software_root": task_catalog.software_root,
            }
        }
        catalogs.update(
            {
                "agent_roots": list(source.catalogs.agent_roots),
                "checkpoint_roots": list(source.catalogs.checkpoint_roots),
                "skill_roots": list(source.catalogs.skill_roots),
            }
        )
        return {
            "human_review": {
                "packet_artifact_root": source.human_review.packet_artifact_root,
                "decision_projection_root": (
                    source.human_review.decision_projection_root
                ),
            },
            "persistence": {
                "state_database_path": source.persistence.state_database_path,
                "sql_export_path": source.persistence.sql_export_path,
                "projection_manifest_path": source.persistence.projection_manifest_path,
            },
            "python_conformance": {
                "pyproject_path": source.python_conformance.pyproject_path,
                "test_root": source.python_conformance.test_root,
                "profile_matrix_path": source.python_conformance.profile_matrix_path,
                "migration_map_path": source.python_conformance.migration_map_path,
            },
            "resources": {
                "project_profile_path": source.resources.project_profile_path,
                "generic_manifest_path": source.resources.generic_manifest_path,
                "generic_root": source.resources.generic_root,
                "local_manifest_path": source.resources.local_manifest_path,
                "local_root": source.resources.local_root,
            },
            "catalogs": catalogs,
        }

    def decode_components(
        self, value: dict[str, _JsonValue]
    ) -> _ConfigurationComponents:
        version = self.integer(value["schema_version"], "schema_version")
        if version != 2:
            raise ValueError("configuration schema_version must equal 2")
        human = self.members(
            value["human_review"],
            ("packet_artifact_root", "decision_projection_root"),
            "human_review",
        )
        persistence = self.members(
            value["persistence"],
            ("state_database_path", "sql_export_path", "projection_manifest_path"),
            "persistence",
        )
        python = self.members(
            value["python_conformance"],
            (
                "pyproject_path",
                "test_root",
                "profile_matrix_path",
                "migration_map_path",
            ),
            "python_conformance",
        )
        resources = self.members(
            value["resources"],
            (
                "project_profile_path",
                "generic_manifest_path",
                "generic_root",
                "local_manifest_path",
                "local_root",
            ),
            "resources",
        )
        catalogs = self.members(
            value["catalogs"],
            (
                "task_catalog",
                "agent_roots",
                "checkpoint_roots",
                "skill_roots",
            ),
            "catalogs",
        )
        tasks = self.members(
            catalogs["task_catalog"],
            ("research_root", "simulation_root", "software_root"),
            "task_catalog",
        )
        task_catalog = TaskCatalogConfiguration(
            self.string(tasks["research_root"], "research_root"),
            self.string(tasks["simulation_root"], "simulation_root"),
            self.string(tasks["software_root"], "software_root"),
        )
        return _ConfigurationComponents(
            version,
            HumanReviewConfiguration(
                self.string(human["packet_artifact_root"], "packet_artifact_root"),
                self.optional_string(
                    human["decision_projection_root"], "decision_projection_root"
                ),
            ),
            HarnessPersistenceConfiguration(
                self.string(persistence["state_database_path"], "state_database_path"),
                self.string(persistence["sql_export_path"], "sql_export_path"),
                self.string(
                    persistence["projection_manifest_path"], "projection_manifest_path"
                ),
            ),
            PythonConformanceConfiguration(
                self.string(python["pyproject_path"], "pyproject_path"),
                self.string(python["test_root"], "test_root"),
                self.string(python["profile_matrix_path"], "profile_matrix_path"),
                self.string(python["migration_map_path"], "migration_map_path"),
            ),
            HarnessResourceConfiguration(
                self.string(resources["project_profile_path"], "project_profile_path"),
                self.string(
                    resources["generic_manifest_path"], "generic_manifest_path"
                ),
                self.string(resources["generic_root"], "generic_root"),
                self.string(resources["local_manifest_path"], "local_manifest_path"),
                self.string(resources["local_root"], "local_root"),
            ),
            HarnessCatalogConfiguration(
                task_catalog,
                self.string_tuple(catalogs["agent_roots"], "agent_roots"),
                self.string_tuple(catalogs["checkpoint_roots"], "checkpoint_roots"),
                self.string_tuple(catalogs["skill_roots"], "skill_roots"),
            ),
        )


class HarnessConfigurationSourceJsonSerializer:
    """Encode explicit source schema 1 (flat) or 2 (categorized), without I/O.

    Canonical JSON uses exact ordered members, two-space indentation, literal
    UTF-8 Unicode and one final LF. Version 1 retains its original byte spelling.
    """

    __slots__ = ()

    def execute(self, source: HarnessConfigurationSource) -> bytes:
        """Encode one source value without changing its format version.

        Parameters
        ----------
        source : HarnessConfigurationSource
            Exact immutable source, with an intrinsically valid version/layout.

        Returns
        -------
        bytes
            Canonical UTF-8 source JSON, without resolved Pi values or provenance.

        Raises
        ------
        TypeError
            The input is not an exact HarnessConfigurationSource.
        """
        if type(source) is not HarnessConfigurationSource:
            raise TypeError("source must be HarnessConfigurationSource")
        codec = _HarnessConfigurationJsonCodec()
        return codec.canonical(codec.source_mapping(source))


class HarnessConfigurationSourceJsonDeserializer:
    """Decode exact source schema 2 without inference, fallback or file I/O.

    Schema 2 requires ``task_catalog`` with all
    three ordered roots. Mixed layouts, unknown/duplicate/reordered members and
    noncanonical bytes are rejected. Decoding does not establish consumer support.
    """

    __slots__ = ()

    def execute(self, payload: bytes) -> HarnessConfigurationSource:
        """Read one canonical versioned source.

        Parameters
        ----------
        payload : bytes
            Exact canonical UTF-8 JSON, without a byte-order mark.

        Returns
        -------
        HarnessConfigurationSource
            Immutable represented source, retaining its explicit format version.

        Raises
        ------
        TypeError
            The payload or a represented field has the wrong semantic type.
        ValueError
            JSON, members, version, path/layout invariants or canonical bytes fail.
        """
        codec = _HarnessConfigurationJsonCodec()
        value = codec.parse(payload)
        codec.members(
            value,
            (
                "schema_version",
                "pi_settings_path",
                "human_review",
                "persistence",
                "python_conformance",
                "resources",
                "catalogs",
            ),
            "source",
        )
        components = codec.decode_components(value)
        result = HarnessConfigurationSource(
            components.schema_version,
            codec.string(value["pi_settings_path"], "pi_settings_path"),
            components.human_review,
            components.persistence,
            components.python_conformance,
            components.resources,
            components.catalogs,
        )
        if HarnessConfigurationSourceJsonSerializer().execute(result) != payload:
            raise ValueError("payload is not canonical source JSON")
        return result


class HarnessConfigurationJsonSerializer:
    """Encode the resolved configuration in schema 2.

    Canonical JSON uses exact ordered members, two-space indentation, literal
    UTF-8 Unicode and one final LF. Source provenance is deliberately excluded.
    """

    __slots__ = ()

    def execute(self, configuration: HarnessConfiguration) -> bytes:
        """Encode a represented effective configuration without source resolution.

        Parameters
        ----------
        configuration : HarnessConfiguration
            Exact immutable resolved value with an explicit version/layout.

        Returns
        -------
        bytes
            Canonical JSON, excluding source bindings and snapshot identity.

        Raises
        ------
        TypeError
            The input is not an exact HarnessConfiguration.
        """
        if type(configuration) is not HarnessConfiguration:
            raise TypeError("configuration must be HarnessConfiguration")
        codec = _HarnessConfigurationJsonCodec()
        return codec.canonical(codec.configuration_mapping(configuration))


class HarnessConfigurationJsonDeserializer:
    """Decode canonical resolved schema 2 without resolving source files.

    The exact Task layout follows the outer version; normalized Pi settings keep
    their separately owned version. No source identity or authority is inferred.
    """

    __slots__ = ()

    def execute(self, payload: bytes) -> HarnessConfiguration:
        """Read one exact represented effective configuration.

        Parameters
        ----------
        payload : bytes
            Canonical UTF-8 JSON with exact version-specific ordered members.

        Returns
        -------
        HarnessConfiguration
            Immutable represented value, not a newly source-resolved result.

        Raises
        ------
        TypeError
            The payload or a represented field has the wrong semantic type.
        ValueError
            JSON, canonical spelling, members, versions or field invariants fail.
        """
        codec = _HarnessConfigurationJsonCodec()
        value = codec.parse(payload)
        codec.members(
            value,
            (
                "schema_version",
                "pi",
                "human_review",
                "persistence",
                "python_conformance",
                "resources",
                "catalogs",
            ),
            "configuration",
        )
        components = codec.decode_components(value)
        pi = codec.members(
            value["pi"], ("schema_version", "disabled_agent_runtime_names"), "pi"
        )
        result = HarnessConfiguration(
            components.schema_version,
            PiHarnessConfiguration(
                codec.integer(pi["schema_version"], "Pi schema_version"),
                codec.string_tuple(
                    pi["disabled_agent_runtime_names"], "disabled_agent_runtime_names"
                ),
            ),
            components.human_review,
            components.persistence,
            components.python_conformance,
            components.resources,
            components.catalogs,
        )
        if HarnessConfigurationJsonSerializer().execute(result) != payload:
            raise ValueError("payload is not canonical resolved configuration JSON")
        return result


class HarnessConfigurationValidator:
    """Validate compatibility among independently valid configuration components."""

    __slots__ = ()

    def execute(
        self, configuration: HarnessConfiguration
    ) -> tuple[HarnessConfigurationResolutionFinding, ...]:
        if type(configuration) is not HarnessConfiguration:
            raise TypeError("configuration must be HarnessConfiguration")
        pairs = (
            (
                configuration.resources.generic_manifest_path,
                configuration.resources.generic_root,
            ),
            (
                configuration.resources.local_manifest_path,
                configuration.resources.local_root,
            ),
        )
        findings = tuple(
            HarnessConfigurationResolutionFinding(
                "HARNESS_CONFIGURATION.RESOURCE_MANIFEST_OUTSIDE_ROOT",
                manifest,
                "Resource manifest must be lexically beneath its configured root.",
            )
            for manifest, root in pairs
            if not manifest.startswith(root + "/")
        )
        return tuple(
            sorted(
                findings,
                key=lambda finding: (finding.code, finding.path or "", finding.message),
            )
        )


class HarnessConfigurationResolver:
    """Resolve explicit harness and Pi settings bytes into one closed result.

    Harness source/resolved schema 1 is flat and schema 2 is categorized. The
    resolution-result schema and snapshot framing remain version 1. Resolving
    bytes performs no file I/O and grants no execution or migration authority.
    """

    __slots__ = ()

    @staticmethod
    def _binding_mapping(
        binding: HarnessConfigurationSourceBinding,
    ) -> dict[str, _JsonValue]:
        return {
            "role": binding.role,
            "path": binding.path,
            "content_identity": {
                "schema_version": binding.content_identity.schema_version,
                "algorithm": binding.content_identity.algorithm,
                "digest": binding.content_identity.digest,
            },
        }

    def _snapshot_identity(
        self,
        configuration: HarnessConfiguration,
        bindings: tuple[HarnessConfigurationSourceBinding, ...],
    ) -> SnapshotIdentity:
        """Retain the v1 tag, ordered canonical parts and 8-byte size framing."""
        codec = _HarnessConfigurationJsonCodec()
        parts = [HarnessConfigurationJsonSerializer().execute(configuration)]
        parts.extend(
            codec.canonical(self._binding_mapping(binding)) for binding in bindings
        )
        framed = bytearray(_SNAPSHOT_FRAME)
        for part in parts:
            framed.extend(len(part).to_bytes(8, "big"))
            framed.extend(part)
        return SnapshotIdentity(1, "sha256", hashlib.sha256(framed).hexdigest())

    def execute(
        self,
        source_path: ResourcePath,
        source_payload: bytes,
        pi_settings_path: ResourcePath,
        pi_settings_payload: bytes,
    ) -> HarnessConfigurationResolutionResult:
        """Resolve exact supplied bytes and bind their paths and content identities.

        Parameters
        ----------
        source_path : str
            Normalized root-relative identity of the Harness source payload.
        source_payload : bytes
            Canonical Harness source, explicitly schema 2.
        pi_settings_path : str
            Normalized root-relative identity of the supplied Pi settings.
        pi_settings_payload : bytes
            Pi-owned JSON; fields outside its consumed subset retain Pi semantics.

        Returns
        -------
        HarnessConfigurationResolutionResult
            Version-1 closed result. Success retains the source's configuration
            version and a version-1 framed snapshot; failure has findings only.
            Both outcomes retain ordered source bindings and exact SHA-256 digests.

        Raises
        ------
        TypeError
            A path or payload has the wrong exact type.
        ValueError
            A supplied path is lexically invalid. Invalid represented source
            content instead produces a failed result with sanitized findings.
        """
        source_path = _HarnessResourcePathValidator().execute(
            source_path, "source_path"
        )
        pi_settings_path = _HarnessResourcePathValidator().execute(
            pi_settings_path, "pi_settings_path"
        )
        if type(source_payload) is not bytes:
            raise TypeError("source_payload must be bytes")
        if type(pi_settings_payload) is not bytes:
            raise TypeError("pi_settings_payload must be bytes")
        bindings = (
            HarnessConfigurationSourceBinding(
                _SOURCE_ROLES[0],
                source_path,
                ContentIdentity(
                    1, "sha256", hashlib.sha256(source_payload).hexdigest()
                ),
            ),
            HarnessConfigurationSourceBinding(
                _SOURCE_ROLES[1],
                pi_settings_path,
                ContentIdentity(
                    1, "sha256", hashlib.sha256(pi_settings_payload).hexdigest()
                ),
            ),
        )
        try:
            source = HarnessConfigurationSourceJsonDeserializer().execute(
                source_payload
            )
        except TypeError, ValueError:
            finding = HarnessConfigurationResolutionFinding(
                "HARNESS_CONFIGURATION.SOURCE_INVALID",
                source_path,
                "Harness configuration source is invalid.",
            )
            return HarnessConfigurationResolutionResult(
                1, "failed", bindings, None, None, (finding,)
            )
        if source.pi_settings_path != pi_settings_path:
            finding = HarnessConfigurationResolutionFinding(
                "HARNESS_CONFIGURATION.PI_PATH_MISMATCH",
                pi_settings_path,
                "Supplied Pi settings path does not match the configured path.",
            )
            return HarnessConfigurationResolutionResult(
                1, "failed", bindings, None, None, (finding,)
            )
        try:
            pi = PiHarnessConfigurationDeserializer().execute(pi_settings_payload)
        except TypeError, ValueError:
            finding = HarnessConfigurationResolutionFinding(
                "HARNESS_CONFIGURATION.PI_SETTINGS_INVALID",
                pi_settings_path,
                "Pi project settings are invalid for the consumed harness subset.",
            )
            return HarnessConfigurationResolutionResult(
                1, "failed", bindings, None, None, (finding,)
            )
        configuration = HarnessConfiguration(
            source.schema_version,
            pi,
            source.human_review,
            source.persistence,
            source.python_conformance,
            source.resources,
            source.catalogs,
        )
        findings = HarnessConfigurationValidator().execute(configuration)
        if findings:
            return HarnessConfigurationResolutionResult(
                1, "failed", bindings, None, None, findings
            )
        return HarnessConfigurationResolutionResult(
            1,
            "resolved",
            bindings,
            self._snapshot_identity(configuration, bindings),
            configuration,
            (),
        )
