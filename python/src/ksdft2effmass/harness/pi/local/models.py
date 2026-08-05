"""Immutable project-local harness records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from .. import (
    AgentDescriptorView,
    ArtifactIdentity,
    ChainView,
    CheckpointRecord,
    ChecksumManifest,
    OwnershipManifestView,
    ProjectProfile,
    ResourceManifest,
    SkillDescriptor,
    TaskReference,
)


@dataclass(frozen=True, slots=True)
class RepositoryRoots:
    """Explicit repository and textual-resource roots.

    Parameters
    ----------
    repository_root
        Absolute path to the repository directory.
    generic_resource_root
        Absolute path to the generic textual-resource directory.
    local_resource_root
        Absolute path to the project-local textual-resource directory.
    """

    repository_root: Path
    generic_resource_root: Path
    local_resource_root: Path

    def __post_init__(self) -> None:
        for name in ("repository_root", "generic_resource_root", "local_resource_root"):
            value = getattr(self, name)
            if not isinstance(value, Path):
                raise TypeError(f"{name} must be pathlib.Path")
            if not value.is_absolute():
                raise ValueError(f"{name} must be an absolute path")
        if not self.generic_resource_root.is_relative_to(self.repository_root):
            raise ValueError("generic_resource_root must be below repository_root")
        if not self.local_resource_root.is_relative_to(self.repository_root):
            raise ValueError("local_resource_root must be below repository_root")
        if self.generic_resource_root == self.local_resource_root:
            raise ValueError("resource roots must be distinct")


@dataclass(frozen=True, slots=True)
class LocalHarnessContext:
    """Validated generic and local composition supplied to local actions."""

    roots: RepositoryRoots
    profile: ProjectProfile
    generic_manifest: ResourceManifest
    generic_manifest_identity: ArtifactIdentity
    local_manifest: ResourceManifest
    local_manifest_identity: ArtifactIdentity

    def __post_init__(self) -> None:
        expected = (
            (self.roots, RepositoryRoots),
            (self.profile, ProjectProfile),
            (self.generic_manifest, ResourceManifest),
            (self.generic_manifest_identity, ArtifactIdentity),
            (self.local_manifest, ResourceManifest),
            (self.local_manifest_identity, ArtifactIdentity),
        )
        if any(type(value) is not kind for value, kind in expected):
            raise TypeError("LocalHarnessContext field has wrong type")


@dataclass(frozen=True, slots=True)
class LocalIssue:
    """One local adapter or routing diagnostic outside the closed H2 registry."""

    code: str
    path: str | None
    detail: str

    def __post_init__(self) -> None:
        if type(self.code) is not str or not self.code.startswith("PIHL."):
            raise ValueError("code must use the PIHL namespace")
        if self.path is not None and type(self.path) is not str:
            raise TypeError("path must be str or None")
        if type(self.detail) is not str:
            raise TypeError("detail must be str")


@dataclass(frozen=True, slots=True)
class LocalValidationResult:
    """Deterministically ordered project-local diagnostics."""

    status: str
    issues: tuple[LocalIssue, ...]

    def __post_init__(self) -> None:
        if self.status not in {"PASS", "FAIL"}:
            raise ValueError("status must be PASS or FAIL")
        if type(self.issues) is not tuple or any(
            type(x) is not LocalIssue for x in self.issues
        ):
            raise TypeError("issues must be a tuple of LocalIssue")
        if self.issues != tuple(
            sorted(self.issues, key=lambda x: (x.code, x.path or "", x.detail))
        ):
            raise ValueError("issues must be deterministically sorted")
        if (self.status == "FAIL") != bool(self.issues):
            raise ValueError("status must agree with issues")


@dataclass(frozen=True, slots=True)
class EvidenceOwnershipRelation:
    """Normalized ownership of one retained Python evidence module.

    Parameters
    ----------
    module_path
        Repository-relative path preserved from the retained manifest.
    evidence_ids
        Sorted evidence identifiers declared by the module.
    ownership_kind
        Accepted primary kind: ``class_owned`` or ``artifact_owned``.
    owner_id
        Preserved class or artifact owner identity.
    relation_kind
        Optional artifact relation kind. The P1 boundary adapter uses
        ``agreement``; ordinary class/artifact ownership has no relation.
    left_side_id, right_side_id
        Optional ordered identities participating in an artifact relation.
    direction
        Optional relation direction. The P1 agreement is nondirectional.
    """

    module_path: str
    evidence_ids: tuple[str, ...]
    ownership_kind: str
    owner_id: str
    relation_kind: str | None = None
    left_side_id: str | None = None
    right_side_id: str | None = None
    direction: str | None = None

    def __post_init__(self) -> None:
        for name in ("module_path", "owner_id"):
            value = getattr(self, name)
            if type(value) is not str or not value:
                raise TypeError(f"{name} must be a nonempty built-in str")
        if self.module_path.startswith("/") or self.module_path.endswith("/"):
            raise ValueError("module_path must be a relative file path")
        if type(self.evidence_ids) is not tuple or any(
            type(value) is not str or not value for value in self.evidence_ids
        ):
            raise TypeError("evidence_ids must be a tuple of nonempty strings")
        if self.evidence_ids != tuple(sorted(set(self.evidence_ids))):
            raise ValueError("evidence_ids must be unique and sorted")
        if self.ownership_kind not in {"class_owned", "artifact_owned"}:
            raise ValueError("ownership_kind must be class_owned or artifact_owned")
        relation_values = (
            self.relation_kind,
            self.left_side_id,
            self.right_side_id,
            self.direction,
        )
        if all(value is None for value in relation_values):
            return
        if any(type(value) is not str or not value for value in relation_values):
            raise ValueError("artifact relation fields must be jointly present")
        if self.ownership_kind != "artifact_owned":
            raise ValueError("only artifact_owned evidence may declare a relation")
        if self.relation_kind != "agreement" or self.direction != "none":
            raise ValueError("unsupported local artifact relation")


_CLOSED_ADAPTER_VALUE_TYPES = (
    AgentDescriptorView,
    ArtifactIdentity,
    ChainView,
    CheckpointRecord,
    ChecksumManifest,
    LocalHarnessContext,
    OwnershipManifestView,
    ProjectProfile,
    ResourceManifest,
    SkillDescriptor,
    TaskReference,
)


def _is_closed_adapter_value(value: object) -> bool:
    """Return whether a value is deterministic and operationally immutable."""
    if value is None or type(value) in {bool, int, str, bytes}:
        return True
    if type(value) is tuple:
        return all(_is_closed_adapter_value(item) for item in value)
    return (
        type(value) in _CLOSED_ADAPTER_VALUE_TYPES
        or type(value) is EvidenceOwnershipRelation
    )


@dataclass(frozen=True, slots=True)
class AdaptationResult:
    """Immutable value produced by a strict local adapter and its diagnostics.

    Values are restricted to the closed generic/local adapter record set,
    immutable scalar leaves, and recursively immutable tuples. Mutable
    containers, paths, sets, mappings, and arbitrary objects are rejected.
    """

    value: object | None
    validation: LocalValidationResult

    def __post_init__(self) -> None:
        if type(self.validation) is not LocalValidationResult:
            raise TypeError("validation must be LocalValidationResult")
        if not _is_closed_adapter_value(self.value):
            raise TypeError("value must be a closed operationally immutable value")
        if self.validation.status == "FAIL" and self.value is not None:
            raise ValueError("failed adaptation must not contain a value")
        if self.validation.status == "PASS" and self.value is None:
            raise ValueError("successful adaptation must contain a value")


class ValidationRoute(StrEnum):
    """Explicit validation implementation route."""

    LEGACY = "legacy"
    SHADOW = "shadow"
    LOCAL = "local"


@dataclass(frozen=True, slots=True)
class RouteConfiguration:
    """Caller-owned route and its explicit rollback target."""

    route: ValidationRoute
    rollback_route: ValidationRoute = ValidationRoute.LEGACY

    def __post_init__(self) -> None:
        if (
            type(self.route) is not ValidationRoute
            or type(self.rollback_route) is not ValidationRoute
        ):
            raise TypeError("routes must be ValidationRoute")
        if self.rollback_route is not ValidationRoute.LEGACY:
            raise ValueError("rollback_route must be legacy")
