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
from typing import cast

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


def _require_version(value: object) -> None:
    if type(value) is not int:
        raise TypeError("schema_version must be an int excluding bool")
    if value != 1:
        raise ValueError("schema_version must equal 1")


def _require_path(value: object, field: str) -> str:
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


def _require_exact_type(value: object, expected: type[object], field: str) -> None:
    if type(value) is not expected:
        raise TypeError(f"{field} must be {expected.__name__}")


def _require_distinct(values: tuple[str | None, ...], field: str) -> None:
    present = tuple(value for value in values if value is not None)
    if len(set(present)) != len(present):
        raise ValueError(f"{field} paths must be distinct")


@dataclass(frozen=True, slots=True)
class HumanReviewConfiguration:
    """Destinations for transient review packets and optional decision projections."""

    packet_artifact_root: ResourcePath
    decision_projection_root: ResourcePath | None

    def __post_init__(self) -> None:
        _require_path(self.packet_artifact_root, "packet_artifact_root")
        if self.decision_projection_root is not None:
            _require_path(self.decision_projection_root, "decision_projection_root")
        _require_distinct(
            (self.packet_artifact_root, self.decision_projection_root), "human_review"
        )


@dataclass(frozen=True, slots=True)
class HarnessPersistenceConfiguration:
    """Root-relative development state and deterministic projection paths."""

    state_database_path: ResourcePath
    sql_export_path: ResourcePath
    projection_manifest_path: ResourcePath

    def __post_init__(self) -> None:
        for field in (
            "state_database_path",
            "sql_export_path",
            "projection_manifest_path",
        ):
            _require_path(getattr(self, field), field)
        _require_distinct(
            (
                self.state_database_path,
                self.sql_export_path,
                self.projection_manifest_path,
            ),
            "persistence",
        )


@dataclass(frozen=True, slots=True)
class PythonConformanceConfiguration:
    """Explicit maintained Python evidence inputs."""

    pyproject_path: ResourcePath
    test_root: ResourcePath
    profile_matrix_path: ResourcePath
    migration_map_path: ResourcePath

    def __post_init__(self) -> None:
        values = tuple(getattr(self, field) for field in self.__dataclass_fields__)
        for field, value in zip(self.__dataclass_fields__, values, strict=True):
            _require_path(value, field)
        _require_distinct(values, "python_conformance")


@dataclass(frozen=True, slots=True)
class HarnessResourceConfiguration:
    """Explicit generic and project-local harness resource inputs."""

    project_profile_path: ResourcePath
    generic_manifest_path: ResourcePath
    generic_root: ResourcePath
    local_manifest_path: ResourcePath
    local_root: ResourcePath

    def __post_init__(self) -> None:
        for field in self.__dataclass_fields__:
            _require_path(getattr(self, field), field)


@dataclass(frozen=True, slots=True)
class HarnessCatalogConfiguration:
    """Explicit roots used for deterministic catalog discovery."""

    task_root: ResourcePath
    agent_roots: tuple[ResourcePath, ...]
    checkpoint_roots: tuple[ResourcePath, ...]
    skill_roots: tuple[ResourcePath, ...]

    def __post_init__(self) -> None:
        _require_path(self.task_root, "task_root")
        all_roots: list[str] = [self.task_root]
        for field in ("agent_roots", "checkpoint_roots", "skill_roots"):
            roots = getattr(self, field)
            if type(roots) is not tuple:
                raise TypeError(f"{field} must be a tuple")
            if not roots:
                raise ValueError(f"{field} must be nonempty")
            for root in roots:
                _require_path(root, f"{field} item")
            if roots != tuple(sorted(set(roots))):
                raise ValueError(f"{field} must be strictly sorted and unique")
            all_roots.extend(roots)
        if len(all_roots) != len(set(all_roots)):
            raise ValueError("catalog roots may not repeat across categories")


@dataclass(frozen=True, slots=True)
class HarnessConfigurationSource:
    """Human-authored harness-owned configuration source value."""

    schema_version: int
    pi_settings_path: ResourcePath
    human_review: HumanReviewConfiguration
    persistence: HarnessPersistenceConfiguration
    python_conformance: PythonConformanceConfiguration
    resources: HarnessResourceConfiguration
    catalogs: HarnessCatalogConfiguration

    def __post_init__(self) -> None:
        _require_version(self.schema_version)
        _require_path(self.pi_settings_path, "pi_settings_path")
        _require_exact_type(self.human_review, HumanReviewConfiguration, "human_review")
        _require_exact_type(
            self.persistence, HarnessPersistenceConfiguration, "persistence"
        )
        _require_exact_type(
            self.python_conformance,
            PythonConformanceConfiguration,
            "python_conformance",
        )
        _require_exact_type(self.resources, HarnessResourceConfiguration, "resources")
        _require_exact_type(self.catalogs, HarnessCatalogConfiguration, "catalogs")


@dataclass(frozen=True, slots=True)
class HarnessConfiguration:
    """Resolved immutable effective harness configuration value."""

    schema_version: int
    pi: PiHarnessConfiguration
    human_review: HumanReviewConfiguration
    persistence: HarnessPersistenceConfiguration
    python_conformance: PythonConformanceConfiguration
    resources: HarnessResourceConfiguration
    catalogs: HarnessCatalogConfiguration

    def __post_init__(self) -> None:
        _require_version(self.schema_version)
        _require_exact_type(self.pi, PiHarnessConfiguration, "pi")
        _require_exact_type(self.human_review, HumanReviewConfiguration, "human_review")
        _require_exact_type(
            self.persistence, HarnessPersistenceConfiguration, "persistence"
        )
        _require_exact_type(
            self.python_conformance,
            PythonConformanceConfiguration,
            "python_conformance",
        )
        _require_exact_type(self.resources, HarnessResourceConfiguration, "resources")
        _require_exact_type(self.catalogs, HarnessCatalogConfiguration, "catalogs")


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
        _require_path(self.path, "path")
        _require_exact_type(self.content_identity, ContentIdentity, "content_identity")


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
            _require_path(self.path, "path")
        if type(self.message) is not str:
            raise TypeError("message must be a built-in str")
        if not self.message or "\n" in self.message or "\r" in self.message:
            raise ValueError("message must be nonempty sanitized single-line text")


def _finding_key(
    finding: HarnessConfigurationResolutionFinding,
) -> tuple[str, str, str]:
    return (finding.code, finding.path or "", finding.message)


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
        _require_version(self.schema_version)
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
        if self.snapshot_identity is not None:
            _require_exact_type(
                self.snapshot_identity, SnapshotIdentity, "snapshot_identity"
            )
        if self.configuration is not None:
            _require_exact_type(
                self.configuration, HarnessConfiguration, "configuration"
            )
        if type(self.findings) is not tuple:
            raise TypeError("findings must be a tuple")
        if any(
            type(finding) is not HarnessConfigurationResolutionFinding
            for finding in self.findings
        ):
            raise TypeError("findings contain a wrong value type")
        if self.findings != tuple(sorted(set(self.findings), key=_finding_key)):
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


class _DuplicateKey(ValueError):
    pass


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKey(key)
        result[key] = value
    return result


def _canonical(value: dict[str, object]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
    ).encode("utf-8")


def _parse_canonical(payload: bytes) -> dict[str, object]:
    if type(payload) is not bytes:
        raise TypeError("payload must be bytes")
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("payload must contain UTF-8 JSON") from exc
    if text.startswith("\ufeff"):
        raise ValueError("UTF-8 BOM is prohibited")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_constant=lambda item: (_ for _ in ()).throw(ValueError(item)),
        )
    except (_DuplicateKey, json.JSONDecodeError, ValueError) as exc:
        raise ValueError("payload must contain strict unique-key JSON") from exc
    if type(value) is not dict:
        raise TypeError("top-level JSON value must be an object")
    return value


def _members(value: object, names: tuple[str, ...], field: str) -> dict[str, object]:
    if type(value) is not dict:
        raise TypeError(f"{field} must be an object")
    if tuple(value) != names:
        raise ValueError(f"{field} must contain exact canonical members in order")
    return value


def _string(value: object, field: str) -> str:
    if type(value) is not str:
        raise TypeError(f"{field} must be a built-in str")
    return value


def _optional_string(value: object, field: str) -> str | None:
    if value is None:
        return None
    return _string(value, field)


def _string_tuple(value: object, field: str) -> tuple[str, ...]:
    if type(value) is not list:
        raise TypeError(f"{field} must be an array")
    if any(type(item) is not str for item in value):
        raise TypeError(f"{field} items must be built-in strings")
    return tuple(value)


def _source_object(source: HarnessConfigurationSource) -> dict[str, object]:
    return {
        "schema_version": source.schema_version,
        "pi_settings_path": source.pi_settings_path,
        "human_review": {
            "packet_artifact_root": source.human_review.packet_artifact_root,
            "decision_projection_root": source.human_review.decision_projection_root,
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
        "catalogs": {
            "task_root": source.catalogs.task_root,
            "agent_roots": list(source.catalogs.agent_roots),
            "checkpoint_roots": list(source.catalogs.checkpoint_roots),
            "skill_roots": list(source.catalogs.skill_roots),
        },
    }


def _configuration_object(configuration: HarnessConfiguration) -> dict[str, object]:
    source = HarnessConfigurationSource(
        configuration.schema_version,
        "placeholder",
        configuration.human_review,
        configuration.persistence,
        configuration.python_conformance,
        configuration.resources,
        configuration.catalogs,
    )
    source_value = _source_object(source)
    return {
        "schema_version": configuration.schema_version,
        "pi": {
            "schema_version": configuration.pi.schema_version,
            "disabled_agent_runtime_names": list(
                configuration.pi.disabled_agent_runtime_names
            ),
        },
        "human_review": source_value["human_review"],
        "persistence": source_value["persistence"],
        "python_conformance": source_value["python_conformance"],
        "resources": source_value["resources"],
        "catalogs": source_value["catalogs"],
    }


def _decode_components(
    value: dict[str, object], *, resolved: bool
) -> dict[str, object]:
    human = _members(
        value["human_review"],
        ("packet_artifact_root", "decision_projection_root"),
        "human_review",
    )
    persistence = _members(
        value["persistence"],
        ("state_database_path", "sql_export_path", "projection_manifest_path"),
        "persistence",
    )
    python = _members(
        value["python_conformance"],
        ("pyproject_path", "test_root", "profile_matrix_path", "migration_map_path"),
        "python_conformance",
    )
    resources = _members(
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
    catalogs = _members(
        value["catalogs"],
        ("task_root", "agent_roots", "checkpoint_roots", "skill_roots"),
        "catalogs",
    )
    components: dict[str, object] = {
        "schema_version": value["schema_version"],
        "human_review": HumanReviewConfiguration(
            _string(human["packet_artifact_root"], "packet_artifact_root"),
            _optional_string(
                human["decision_projection_root"], "decision_projection_root"
            ),
        ),
        "persistence": HarnessPersistenceConfiguration(
            *(
                _string(persistence[name], name)
                for name in (
                    "state_database_path",
                    "sql_export_path",
                    "projection_manifest_path",
                )
            )
        ),
        "python_conformance": PythonConformanceConfiguration(
            *(
                _string(python[name], name)
                for name in (
                    "pyproject_path",
                    "test_root",
                    "profile_matrix_path",
                    "migration_map_path",
                )
            )
        ),
        "resources": HarnessResourceConfiguration(
            *(
                _string(resources[name], name)
                for name in (
                    "project_profile_path",
                    "generic_manifest_path",
                    "generic_root",
                    "local_manifest_path",
                    "local_root",
                )
            )
        ),
        "catalogs": HarnessCatalogConfiguration(
            _string(catalogs["task_root"], "task_root"),
            _string_tuple(catalogs["agent_roots"], "agent_roots"),
            _string_tuple(catalogs["checkpoint_roots"], "checkpoint_roots"),
            _string_tuple(catalogs["skill_roots"], "skill_roots"),
        ),
    }
    _require_version(components["schema_version"])
    if resolved:
        pi = _members(
            value["pi"],
            ("schema_version", "disabled_agent_runtime_names"),
            "pi",
        )
        components["pi"] = PiHarnessConfiguration(
            cast(int, pi["schema_version"]),
            _string_tuple(
                pi["disabled_agent_runtime_names"],
                "disabled_agent_runtime_names",
            ),
        )
    else:
        components["pi_settings_path"] = _string(
            value["pi_settings_path"], "pi_settings_path"
        )
    return components


class HarnessConfigurationSourceJsonSerializer:
    """Emit canonical human-authored source JSON bytes."""

    __slots__ = ()

    def execute(self, source: HarnessConfigurationSource) -> bytes:
        if type(source) is not HarnessConfigurationSource:
            raise TypeError("source must be HarnessConfigurationSource")
        return _canonical(_source_object(source))


class HarnessConfigurationSourceJsonDeserializer:
    """Strictly decode canonical human-authored source JSON bytes."""

    __slots__ = ()

    def execute(self, payload: bytes) -> HarnessConfigurationSource:
        value = _parse_canonical(payload)
        _members(
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
        components = _decode_components(value, resolved=False)
        result = HarnessConfigurationSource(
            cast(int, components["schema_version"]),
            cast(str, components["pi_settings_path"]),
            cast(HumanReviewConfiguration, components["human_review"]),
            cast(HarnessPersistenceConfiguration, components["persistence"]),
            cast(PythonConformanceConfiguration, components["python_conformance"]),
            cast(HarnessResourceConfiguration, components["resources"]),
            cast(HarnessCatalogConfiguration, components["catalogs"]),
        )
        if HarnessConfigurationSourceJsonSerializer().execute(result) != payload:
            raise ValueError("payload is not canonical source JSON")
        return result


class HarnessConfigurationJsonSerializer:
    """Emit canonical resolved configuration snapshot JSON bytes."""

    __slots__ = ()

    def execute(self, configuration: HarnessConfiguration) -> bytes:
        if type(configuration) is not HarnessConfiguration:
            raise TypeError("configuration must be HarnessConfiguration")
        return _canonical(_configuration_object(configuration))


class HarnessConfigurationJsonDeserializer:
    """Strictly decode represented canonical resolved configuration JSON bytes."""

    __slots__ = ()

    def execute(self, payload: bytes) -> HarnessConfiguration:
        value = _parse_canonical(payload)
        _members(
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
        components = _decode_components(value, resolved=True)
        result = HarnessConfiguration(
            cast(int, components["schema_version"]),
            cast(PiHarnessConfiguration, components["pi"]),
            cast(HumanReviewConfiguration, components["human_review"]),
            cast(HarnessPersistenceConfiguration, components["persistence"]),
            cast(PythonConformanceConfiguration, components["python_conformance"]),
            cast(HarnessResourceConfiguration, components["resources"]),
            cast(HarnessCatalogConfiguration, components["catalogs"]),
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
        return tuple(sorted(findings, key=_finding_key))


def _binding_object(binding: HarnessConfigurationSourceBinding) -> dict[str, object]:
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
    configuration: HarnessConfiguration,
    bindings: tuple[HarnessConfigurationSourceBinding, ...],
) -> SnapshotIdentity:
    """Hash the v1 tag plus each canonical part framed by an 8-byte big-endian size.

    The parts are the resolved-configuration JSON followed by source-binding JSON in
    result order. The tag, length encoding, part order, and canonical JSON bytes form
    the complete version-1 snapshot framing contract.
    """
    parts = [HarnessConfigurationJsonSerializer().execute(configuration)]
    parts.extend(_canonical(_binding_object(binding)) for binding in bindings)
    framed = bytearray(_SNAPSHOT_FRAME)
    for part in parts:
        framed.extend(len(part).to_bytes(8, "big"))
        framed.extend(part)
    return SnapshotIdentity(1, "sha256", hashlib.sha256(framed).hexdigest())


class HarnessConfigurationResolver:
    """Resolve explicit harness and Pi settings bytes into one closed result."""

    __slots__ = ()

    def execute(
        self,
        source_path: ResourcePath,
        source_payload: bytes,
        pi_settings_path: ResourcePath,
        pi_settings_payload: bytes,
    ) -> HarnessConfigurationResolutionResult:
        source_path = _require_path(source_path, "source_path")
        pi_settings_path = _require_path(pi_settings_path, "pi_settings_path")
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
            1,
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
            _snapshot_identity(configuration, bindings),
            configuration,
            (),
        )
