"""Immutable project-local harness records."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .. import (
    AgentDescriptorView,
    ArtifactIdentity,
    CheckpointRecord,
    ChecksumManifest,
    OwnershipManifestView,
    ProjectProfile,
    ResourceManifest,
    SkillDescriptor,
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
            if ".." in value.parts:
                raise ValueError(f"{name} must not contain parent traversal")
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


_CLOSED_ADAPTER_VALUE_TYPES = (
    AgentDescriptorView,
    ArtifactIdentity,
    CheckpointRecord,
    ChecksumManifest,
    LocalHarnessContext,
    OwnershipManifestView,
    ProjectProfile,
    ResourceManifest,
    SkillDescriptor,
)


def _is_closed_adapter_value(value: object) -> bool:
    """Return whether a value is deterministic and operationally immutable."""
    if value is None or type(value) in {bool, int, str, bytes}:
        return True
    if type(value) is tuple:
        return all(_is_closed_adapter_value(item) for item in value)
    return type(value) in _CLOSED_ADAPTER_VALUE_TYPES


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
