"""Immutable Pi configuration consumed by the generic harness boundary.

The module represents only the narrow project-settings subset used to determine
repository-declared subagent disablement. Pi owns the complete settings format and
runtime discovery semantics. Deserialization establishes structural software
behavior only; it grants no Task, operation, runtime, or acceptance authority.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .identity import (
    ArtifactIdentity,
    Identifier,
    ResourcePath,
    _require_builtin_str,
    _require_identifier,
    _require_path,
    _require_sorted_unique,
    _require_tuple,
    _require_version,
)


@dataclass(frozen=True, slots=True)
class PiHarnessConfiguration:
    """Normalized Pi project configuration consumed by harness operations.

    Parameters
    ----------
    schema_version
        Version of this normalized Harness representation. The only supported value
        is ``1``.
    disabled_agent_runtime_names
        Exact package-qualified Pi runtime names disabled by project configuration.
        Values must be built-in strings in strictly sorted unique order. The tuple
        represents only disabled names; an explicit JSON ``false`` and an absent
        override are intentionally equivalent.

    Notes
    -----
    This object is not a complete model of ``.pi/settings.json``. It contains no
    runtime inventory, file path, source-byte identity, Task authority, path
    ownership, or operation capability.
    """

    schema_version: int
    disabled_agent_runtime_names: tuple[Identifier, ...]

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_tuple(
            self.disabled_agent_runtime_names, "disabled_agent_runtime_names"
        )
        for runtime_name in self.disabled_agent_runtime_names:
            _require_builtin_str(runtime_name, "disabled agent runtime name")
        _require_sorted_unique(
            self.disabled_agent_runtime_names, "disabled_agent_runtime_names"
        )


@dataclass(frozen=True, slots=True)
class PiHarnessAgentDefinition:
    """One normalized repository agent definition ready for projection.

    Parameters
    ----------
    schema_version
        Version of this normalized definition; currently ``1``.
    name, package, runtime_name
        Exact descriptor name, optional package, and resolved Pi runtime name.
    source_path, source_identity
        Repository-relative descriptor path and exact source-byte identity.
    acceptance_role
        Normalized ``writer`` or ``read_only`` role.
    selected_skills
        Strictly sorted unique descriptor-selected skill names.
    enabled
        Repository-declared enablement after applying ``PiHarnessConfiguration``.
    """

    schema_version: int
    name: Identifier
    package: Identifier | None
    runtime_name: Identifier
    source_path: ResourcePath
    source_identity: ArtifactIdentity
    acceptance_role: str
    selected_skills: tuple[Identifier, ...]
    enabled: bool

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.name, "name")
        if self.package is not None:
            _require_identifier(self.package, "package")
        _require_identifier(self.runtime_name, "runtime_name")
        expected_runtime_name = (
            f"{self.package}.{self.name}" if self.package else self.name
        )
        if self.runtime_name != expected_runtime_name:
            raise ValueError("runtime_name must equal package.name")
        _require_path(self.source_path, "source_path")
        if type(self.source_identity) is not ArtifactIdentity:
            raise TypeError("source_identity must be ArtifactIdentity")
        if self.acceptance_role not in {"writer", "read_only"}:
            raise ValueError("acceptance_role must be writer or read_only")
        _require_tuple(self.selected_skills, "selected_skills")
        for skill in self.selected_skills:
            _require_identifier(skill, "selected skill")
        _require_sorted_unique(self.selected_skills, "selected_skills")
        if type(self.enabled) is not bool:
            raise TypeError("enabled must be bool")


class PiHarnessConfigurationDeserializer:
    """Deserialize the supported Pi project-settings subset from exact JSON bytes.

    The ActionObject performs no file access or runtime discovery. Unknown fields
    outside the consumed subset remain Pi-owned and are ignored. Within
    ``subagents.agentOverrides``, override names and objects are validated because
    they determine whether a ``disabled`` value applies.
    """

    __slots__ = ()

    def execute(self, payload: bytes) -> PiHarnessConfiguration:
        """Return normalized Harness configuration from caller-supplied JSON bytes.

        Parameters
        ----------
        payload
            UTF-8 JSON bytes containing a Pi project-settings object.

        Returns
        -------
        PiHarnessConfiguration
            Version-1 normalized disabled-agent configuration.

        Raises
        ------
        TypeError
            If ``payload`` is not exactly ``bytes`` or a consumed JSON member has the
            wrong semantic type.
        ValueError
            If UTF-8 or JSON decoding fails, an override name is empty, or the
            normalized configuration violates an intrinsic invariant.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        try:
            settings = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("payload must contain UTF-8 JSON") from exc
        if type(settings) is not dict:
            raise TypeError("Pi project settings must contain an object")
        subagents = settings.get("subagents", {})
        if type(subagents) is not dict:
            raise TypeError("subagents settings must contain an object")
        overrides = subagents.get("agentOverrides", {})
        if type(overrides) is not dict:
            raise TypeError("subagents.agentOverrides must contain an object")
        disabled: list[str] = []
        for runtime_name, override in overrides.items():
            if type(runtime_name) is not str:
                raise TypeError("agent override names must be built-in strings")
            _require_builtin_str(runtime_name, "agent override name")
            if type(override) is not dict:
                raise TypeError("agent overrides must contain objects")
            value = override.get("disabled", False)
            if type(value) is not bool:
                raise TypeError("agent override disabled must be boolean")
            if value:
                disabled.append(runtime_name)
        return PiHarnessConfiguration(1, tuple(sorted(disabled)))


class PiHarnessAgentDefinitionResolver:
    """Resolve one descriptor and configuration into a projection-ready definition.

    The ActionObject parses only the frontmatter fields consumed by Harness control.
    It performs no file access, persistence, Task assignment, or Pi runtime discovery.
    """

    __slots__ = ()

    def execute(
        self,
        source_path: ResourcePath,
        payload: bytes,
        configuration: PiHarnessConfiguration,
    ) -> PiHarnessAgentDefinition:
        """Return one normalized agent definition from explicit immutable inputs.

        Parameters
        ----------
        source_path
            Repository-relative descriptor path.
        payload
            Exact UTF-8 Markdown descriptor bytes.
        configuration
            Normalized project configuration applied by exact runtime name.

        Returns
        -------
        PiHarnessAgentDefinition
            Projection-ready normalized definition.

        Raises
        ------
        TypeError
            If an input or consumed field has the wrong semantic type.
        ValueError
            If frontmatter is absent, incomplete, unsupported, or inconsistent.
        """
        _require_path(source_path, "source_path")
        if type(payload) is not bytes:
            raise TypeError("payload must be bytes")
        if type(configuration) is not PiHarnessConfiguration:
            raise TypeError("configuration must be PiHarnessConfiguration")
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("descriptor must contain UTF-8") from exc
        if not text.startswith("---\n"):
            raise ValueError("descriptor must start with frontmatter")
        end = text.find("\n---\n", 4)
        if end < 0:
            raise ValueError("descriptor frontmatter must be closed")
        frontmatter: dict[str, str] = {}
        for line in text[4:end].splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                frontmatter[key.strip()] = value.strip()
        try:
            name = frontmatter["name"]
            raw_role = frontmatter["acceptanceRole"]
        except KeyError as exc:
            raise ValueError("descriptor lacks name or acceptanceRole") from exc
        package = frontmatter.get("package") or None
        runtime_name = f"{package}.{name}" if package else name
        roles = {"writer": "writer", "read-only": "read_only"}
        if raw_role not in roles:
            raise ValueError("unsupported acceptanceRole")
        skills = tuple(
            sorted(
                skill.strip()
                for skill in frontmatter.get("skills", "").split(",")
                if skill.strip()
            )
        )
        digest = hashlib.sha256(payload).hexdigest()
        return PiHarnessAgentDefinition(
            1,
            name,
            package,
            runtime_name,
            source_path,
            ArtifactIdentity(1, "sha256", digest),
            roles[raw_role],
            skills,
            runtime_name not in configuration.disabled_agent_runtime_names,
        )
