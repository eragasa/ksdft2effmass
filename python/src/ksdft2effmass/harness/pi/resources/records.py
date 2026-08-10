"""Immutable resource-domain records and intrinsic invariants."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..identity import (
    ArtifactIdentity,
    Identifier,
    ResourcePath,
    Version,
    _require_builtin_str,
    _require_identifier,
    _require_path,
    _require_sorted_unique,
    _require_tuple,
    _require_version,
)
from ..validation import ValidationResult

_RESOURCE_KINDS = {
    "skill",
    "reference",
    "schema",
    "template",
    "profile",
    "manifest",
    "script",
    "documentation",
}


@dataclass(frozen=True, slots=True)
class ResourceReference:
    """One manifest-addressed regular-file resource."""

    schema_version: int
    resource_id: Identifier
    resource_kind: str
    format_version: Version
    path: ResourcePath
    content_identity: ArtifactIdentity
    dependency_ids: tuple[Identifier, ...]

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.resource_id, "resource_id")
        _require_builtin_str(self.resource_kind, "resource_kind")
        if self.resource_kind not in _RESOURCE_KINDS:
            raise ValueError("unsupported resource_kind")
        _require_version(self.format_version, "format_version")
        _require_path(self.path, "path")
        if type(self.content_identity) is not ArtifactIdentity:
            raise TypeError("content_identity must be ArtifactIdentity")
        _require_tuple(self.dependency_ids, "dependency_ids")
        for x in self.dependency_ids:
            _require_identifier(x, "dependency_id")
        _require_sorted_unique(self.dependency_ids, "dependency_ids")


@dataclass(frozen=True, slots=True)
class ResourceManifest:
    """Canonical generic inventory or extension-only local inventory."""

    schema_version: int
    manifest_id: Identifier
    manifest_version: Version
    layer: str
    extends_manifest_id: Identifier | None
    resources: tuple[ResourceReference, ...]

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.manifest_id, "manifest_id")
        _require_version(self.manifest_version, "manifest_version")
        _require_builtin_str(self.layer, "layer")
        if self.layer not in {"generic", "local"}:
            raise ValueError("layer must be generic or local")
        if self.extends_manifest_id is not None:
            _require_identifier(self.extends_manifest_id, "extends_manifest_id")
        if (self.layer == "generic") != (self.extends_manifest_id is None):
            raise ValueError("generic has no base and local requires one")
        _require_tuple(self.resources, "resources")
        if not self.resources:
            raise ValueError("resources must be nonempty")
        if any(type(x) is not ResourceReference for x in self.resources):
            raise TypeError("resources must contain ResourceReference")
        canonical = tuple(
            sorted(
                self.resources,
                key=lambda resource: (
                    resource.resource_id,
                    resource.path,
                    resource.resource_kind,
                    resource.format_version,
                    resource.content_identity.algorithm,
                    resource.content_identity.digest,
                    resource.dependency_ids,
                ),
            )
        )
        object.__setattr__(self, "resources", canonical)


@dataclass(frozen=True, slots=True)
class ResourceManifestRefreshRequest:
    """Select manifest-declared resources for explicit-root identity refresh.

    Parameters
    ----------
    root
        Absolute caller-selected filesystem root. The action validates its
        existence and confinement properties without consulting the current
        working directory.
    manifest
        Existing immutable manifest whose selected identities will be observed.
    resource_ids
        Nonempty selection of resource identifiers. Values are canonicalized to
        sorted unique tuple storage.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If the root is relative, the selection is empty, or an identifier is
        malformed.
    """

    root: Path
    manifest: ResourceManifest
    resource_ids: tuple[Identifier, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.root, Path):
            raise TypeError("root must be pathlib.Path")
        if not self.root.is_absolute():
            raise ValueError("root must be absolute")
        if type(self.manifest) is not ResourceManifest:
            raise TypeError("manifest must be ResourceManifest")
        _require_tuple(self.resource_ids, "resource_ids")
        if not self.resource_ids:
            raise ValueError("resource_ids must be nonempty")
        for resource_id in self.resource_ids:
            _require_identifier(resource_id, "resource_ids item")
        object.__setattr__(self, "resource_ids", tuple(sorted(set(self.resource_ids))))


@dataclass(frozen=True, slots=True)
class ResourceManifestRefreshResult:
    """Immutable outcome of explicit resource-identity observation.

    Attributes
    ----------
    manifest
        Newly constructed canonical manifest, or ``None`` when validation fails.
    changed_resource_ids
        Sorted unique identifiers whose observed SHA-256 differs from the input
        manifest.
    validation
        Deterministically ordered structural and filesystem findings.

    Notes
    -----
    This result records byte-identity maintenance only. It does not establish
    semantic correctness, scientific validity, provenance truth, or acceptance.
    """

    manifest: ResourceManifest | None
    changed_resource_ids: tuple[Identifier, ...]
    validation: ValidationResult

    def __post_init__(self) -> None:
        if self.manifest is not None and type(self.manifest) is not ResourceManifest:
            raise TypeError("manifest must be ResourceManifest or None")
        _require_tuple(self.changed_resource_ids, "changed_resource_ids")
        for resource_id in self.changed_resource_ids:
            _require_identifier(resource_id, "changed_resource_ids item")
        _require_sorted_unique(self.changed_resource_ids, "changed_resource_ids")
        if type(self.validation) is not ValidationResult:
            raise TypeError("validation must be ValidationResult")
        failed = self.validation.status == "FAIL"
        if failed == (self.manifest is not None):
            raise ValueError("manifest presence must agree with validation status")
        if self.manifest is not None:
            manifest_ids = {
                resource.resource_id for resource in self.manifest.resources
            }
            if not set(self.changed_resource_ids) <= manifest_ids:
                raise ValueError("changed_resource_ids must occur in manifest")
        elif self.changed_resource_ids:
            raise ValueError("failed result must not report changed resources")


@dataclass(frozen=True, slots=True)
class SkillDescriptor:
    """Versioned, data-only resource closure for one operational skill."""

    schema_version: int
    skill_id: Identifier
    behavior_version: Version
    entry_resource_id: Identifier
    trigger_capability_ids: tuple[Identifier, ...]
    required_resource_ids: tuple[Identifier, ...]
    side_effect_class: str
    authorization_policy_id: Identifier
    retry_policy: str
    termination_policy: str

    def __post_init__(self) -> None:
        if _require_version(self.schema_version, "schema_version") != 1:
            raise ValueError("schema_version must equal 1")
        _require_identifier(self.skill_id, "skill_id")
        _require_version(self.behavior_version, "behavior_version")
        _require_identifier(self.entry_resource_id, "entry_resource_id")
        for name in ("trigger_capability_ids", "required_resource_ids"):
            values = getattr(self, name)
            _require_tuple(values, name)
            if not values:
                raise ValueError(f"{name} must be nonempty")
            for x in values:
                _require_identifier(x, name)
            _require_sorted_unique(values, name)
        if self.entry_resource_id not in self.required_resource_ids:
            raise ValueError("required resources must include entry")
        _require_builtin_str(self.side_effect_class, "side_effect_class")
        if self.side_effect_class not in {
            "read_only",
            "local_write",
            "external_effect",
        }:
            raise ValueError("invalid side_effect_class")
        _require_identifier(self.authorization_policy_id, "authorization_policy_id")
        _require_builtin_str(self.retry_policy, "retry_policy")
        if self.retry_policy not in {"none", "explicit_authorization_only"}:
            raise ValueError("invalid retry_policy")
        _require_builtin_str(self.termination_policy, "termination_policy")
        if self.termination_policy != "stop_after_result":
            raise ValueError("invalid termination_policy")
