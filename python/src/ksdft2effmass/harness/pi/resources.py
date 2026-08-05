"""Resource records, manifest validation, and explicit-root resolution."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from .identity import (
    ArtifactIdentity,
    HarnessInternalError,
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
from .validation import (
    ResourceResolutionResult,
    SerializeJsonRecord,
    ValidationIssue,
    ValidationResult,
    _issue,
    _result,
)

if TYPE_CHECKING:
    from .profiles import ProjectProfile

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
        if self.resource_id in self.dependency_ids:
            raise ValueError("resource cannot depend on itself")


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
        ids = tuple(x.resource_id for x in self.resources)
        if ids != tuple(sorted(ids)) or len(set(ids)) != len(ids):
            raise ValueError("resources must be unique and resource_id-sorted")
        if len({x.path for x in self.resources}) != len(self.resources):
            raise ValueError("resource paths must be unique")


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


def _manifest_maps(
    generic: ResourceManifest, local: ResourceManifest | None
) -> tuple[dict[str, ResourceReference], dict[str, ResourceReference]]:
    return (
        {r.resource_id: r for r in generic.resources},
        {} if local is None else {r.resource_id: r for r in local.resources},
    )


class ValidateResourceManifest:
    """Validate profile binding, overlay direction, compatibility, and closure."""

    __slots__ = ()

    def execute(
        self,
        generic_manifest: ResourceManifest,
        generic_manifest_identity: ArtifactIdentity,
        local_manifest: ResourceManifest | None,
        local_manifest_identity: ArtifactIdentity | None,
        profile: ProjectProfile,
    ) -> ValidationResult:
        from .profiles import ProjectProfile

        if (
            type(generic_manifest) is not ResourceManifest
            or type(generic_manifest_identity) is not ArtifactIdentity
            or type(profile) is not ProjectProfile
        ):
            raise TypeError("invalid manifest validator argument type")
        if local_manifest is not None and type(local_manifest) is not ResourceManifest:
            raise TypeError("local_manifest has wrong type")
        if (
            local_manifest_identity is not None
            and type(local_manifest_identity) is not ArtifactIdentity
        ):
            raise TypeError("local_manifest_identity has wrong type")
        issues = []
        if (
            generic_manifest.layer != "generic"
            or generic_manifest.manifest_id != profile.generic_manifest_id
            or generic_manifest.manifest_version != profile.generic_manifest_version
        ):
            issues.append(
                _issue(
                    "PIH.RESOURCE.MANIFEST_MISMATCH",
                    "Generic manifest does not match the profile.",
                    generic_manifest.manifest_id,
                )
            )
        actual = SerializeJsonRecord().execute(generic_manifest).content_identity
        if actual != generic_manifest_identity:
            issues.append(
                _issue(
                    "PIH.RESOURCE.MANIFEST_MISMATCH",
                    "Generic manifest content identity differs.",
                    generic_manifest.manifest_id,
                )
            )
        expects_local = profile.local_manifest_id is not None
        local_inputs_absent = local_manifest is None and local_manifest_identity is None
        local_inputs_present = (
            local_manifest is not None and local_manifest_identity is not None
        )
        if (expects_local and not local_inputs_present) or (
            not expects_local and not local_inputs_absent
        ):
            issues.append(
                _issue(
                    "PIH.RESOURCE.MANIFEST_MISMATCH",
                    "Local manifest presence does not match profile.",
                )
            )
        if local_manifest is not None:
            if (
                local_manifest.layer != "local"
                or local_manifest.manifest_id != profile.local_manifest_id
                or local_manifest.manifest_version != profile.local_manifest_version
                or local_manifest.extends_manifest_id != generic_manifest.manifest_id
            ):
                issues.append(
                    _issue(
                        "PIH.RESOURCE.MANIFEST_MISMATCH",
                        "Local manifest does not match its profiled base.",
                        local_manifest.manifest_id,
                    )
                )
            if (
                local_manifest_identity is not None
                and SerializeJsonRecord().execute(local_manifest).content_identity
                != local_manifest_identity
            ):
                issues.append(
                    _issue(
                        "PIH.RESOURCE.MANIFEST_MISMATCH",
                        "Local manifest content identity differs.",
                        local_manifest.manifest_id,
                    )
                )
        gm, lm = _manifest_maps(generic_manifest, local_manifest)
        for rid in sorted(set(gm) & set(lm)):
            issues.append(
                _issue(
                    "PIH.RESOURCE.OVERLAY_REPLACEMENT",
                    "Local resource replaces a generic ID.",
                    rid,
                )
            )
        gpaths = {r.path: r.resource_id for r in gm.values()}
        for r in lm.values():
            if r.path in gpaths:
                issues.append(
                    _issue(
                        "PIH.RESOURCE.OVERLAY_REPLACEMENT",
                        "Local resource reuses a generic path.",
                        r.resource_id,
                        r.path,
                        (gpaths[r.path],),
                    )
                )
        supported = set(profile.supported_resource_formats)
        all_ids = set(gm) | set(lm)
        graph: dict[str, tuple[str, ...]] = {}
        for layer, mapping in (("generic", gm), ("local", lm)):
            for rid, r in sorted(mapping.items()):
                if (r.resource_kind, r.format_version) not in supported:
                    issues.append(
                        _issue(
                            "PIH.RESOURCE.VERSION_INCOMPATIBLE",
                            "Resource format is not profiled.",
                            rid,
                            r.path,
                        )
                    )
                for dep in r.dependency_ids:
                    if dep not in all_ids:
                        issues.append(
                            _issue(
                                "PIH.RESOURCE.MISSING_DEPENDENCY",
                                "Dependency is absent.",
                                rid,
                                r.path,
                                (dep,),
                            )
                        )
                    elif layer == "generic" and dep in lm:
                        issues.append(
                            _issue(
                                "PIH.RESOURCE.GENERIC_TO_LOCAL_DEPENDENCY",
                                "Generic resource depends on local resource.",
                                rid,
                                r.path,
                                (dep,),
                            )
                        )
                graph[rid] = r.dependency_ids
        visiting: set[str] = set()
        done: set[str] = set()

        def visit(node: str) -> None:
            if node in visiting:
                issues.append(
                    _issue(
                        "PIH.RESOURCE.DEPENDENCY_CYCLE",
                        "Resource dependency cycle.",
                        node,
                    )
                )
                return
            if node in done:
                return
            visiting.add(node)
            for dep in graph.get(node, ()):
                if dep in graph:
                    visit(dep)
            visiting.remove(node)
            done.add(node)

        for node in sorted(graph):
            visit(node)
        return _result(tuple(issues))


def _confined_file(root: Path, path: str) -> tuple[Path | None, ValidationIssue | None]:
    if (
        not isinstance(root, Path)
        or not root.is_absolute()
        or not root.exists()
        or not root.is_dir()
    ):
        return None, _issue(
            "PIH.PATH.ROOT_INVALID",
            "Explicit root must be an existing absolute directory.",
            path=path,
        )
    resolved_root = root.resolve()
    current = root
    for segment in path.split("/"):
        try:
            names = os.listdir(current)
        except OSError:
            return None, _issue(
                "PIH.PATH.MISSING", "Resource component is missing.", path=path
            )
        if segment not in names:
            if any(n.casefold() == segment.casefold() for n in names):
                return None, _issue(
                    "PIH.PATH.CASE_MISMATCH",
                    "Resource component case differs.",
                    path=path,
                )
            return None, _issue("PIH.PATH.MISSING", "Resource is missing.", path=path)
        current = current / segment
        if current.is_symlink():
            return None, _issue(
                "PIH.PATH.SYMLINK", "Symlink components are prohibited.", path=path
            )
    try:
        resolved = current.resolve()
        resolved.relative_to(resolved_root)
    except OSError, ValueError:
        return None, _issue(
            "PIH.PATH.ESCAPE", "Resolved path escapes its root.", path=path
        )
    if not current.is_file():
        return None, _issue(
            "PIH.PATH.NOT_FILE", "Resource is not a regular file.", path=path
        )
    return current, None


class ResolveResource:
    """Resolve and hash one resource beneath explicit roots."""

    __slots__ = ()

    def execute(
        self,
        resource_id: Identifier,
        generic_root: Path,
        generic_manifest: ResourceManifest,
        generic_manifest_identity: ArtifactIdentity,
        local_root: Path | None,
        local_manifest: ResourceManifest | None,
        local_manifest_identity: ArtifactIdentity | None,
        profile: ProjectProfile,
    ) -> ResourceResolutionResult:
        _require_identifier(resource_id, "resource_id")
        if not isinstance(generic_root, Path) or (
            local_root is not None and not isinstance(local_root, Path)
        ):
            raise TypeError("roots must be pathlib.Path")
        validation = ValidateResourceManifest().execute(
            generic_manifest,
            generic_manifest_identity,
            local_manifest,
            local_manifest_identity,
            profile,
        )
        expects_local = profile.local_manifest_id is not None
        root_presence_matches = (expects_local and local_root is not None) or (
            not expects_local and local_root is None
        )
        if not root_presence_matches:
            validation = _result(
                validation.issues
                + (
                    _issue(
                        "PIH.RESOURCE.MANIFEST_MISMATCH",
                        "Local root presence does not match profile.",
                    ),
                )
            )
        if validation.status == "FAIL":
            return ResourceResolutionResult(None, None, validation)
        gm, lm = _manifest_maps(generic_manifest, local_manifest)
        matches: list[tuple[Path | None, ResourceReference]] = (
            [(generic_root, gm[resource_id])] if resource_id in gm else []
        )
        if resource_id in lm:
            matches.append((local_root, lm[resource_id]))
        if not matches:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.RESOURCE.NOT_FOUND",
                            "Resource ID was not found.",
                            resource_id,
                        ),
                    )
                ),
            )
        if len(matches) != 1:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.RESOURCE.AMBIGUOUS_SELECTION",
                            "Resource ID is ambiguous.",
                            resource_id,
                        ),
                    )
                ),
            )
        root, ref = matches[0]
        if root is None:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.PATH.ROOT_INVALID",
                            "Selected layer has no root.",
                            resource_id,
                            ref.path,
                        ),
                    )
                ),
            )
        path, problem = _confined_file(root, ref.path)
        if problem is not None:
            return ResourceResolutionResult(None, None, _result((problem,)))
        if path is None:
            raise AssertionError("successful confinement must return a path")
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as exc:
            raise HarnessInternalError("ResolveResource", str(exc)) from exc
        if digest != ref.content_identity.digest:
            return ResourceResolutionResult(
                None,
                None,
                _result(
                    (
                        _issue(
                            "PIH.ARTIFACT.HASH_MISMATCH",
                            "Resource bytes differ from identity.",
                            resource_id,
                            ref.path,
                        ),
                    )
                ),
            )
        return ResourceResolutionResult(path, ref, _result())


class ValidateSkillResources:
    """Validate skill descriptors against a validated resource closure."""

    __slots__ = ()

    def execute(
        self,
        descriptors: tuple[SkillDescriptor, ...],
        generic_manifest: ResourceManifest,
        generic_manifest_identity: ArtifactIdentity,
        local_manifest: ResourceManifest | None,
        local_manifest_identity: ArtifactIdentity | None,
        profile: ProjectProfile,
    ) -> ValidationResult:
        _require_tuple(descriptors, "descriptors")
        if any(type(d) is not SkillDescriptor for d in descriptors):
            raise TypeError("descriptors must contain SkillDescriptor")
        base = ValidateResourceManifest().execute(
            generic_manifest,
            generic_manifest_identity,
            local_manifest,
            local_manifest_identity,
            profile,
        )
        if base.status == "FAIL":
            return base
        from .profiles import ProjectProfile

        if type(profile) is not ProjectProfile:
            raise TypeError("profile has wrong type")
        resources = {r.resource_id: r for r in generic_manifest.resources}
        if local_manifest:
            resources.update({r.resource_id: r for r in local_manifest.resources})
        issues = []
        seen = set()
        for d in sorted(descriptors, key=lambda x: x.skill_id):
            if d.skill_id in seen:
                issues.append(
                    _issue("PIH.SKILL.DUPLICATE_ID", "Duplicate skill ID.", d.skill_id)
                )
            seen.add(d.skill_id)
            entry = resources.get(d.entry_resource_id)
            if entry is None:
                issues.append(
                    _issue(
                        "PIH.SKILL.ENTRY_MISSING",
                        "Skill entry is absent.",
                        d.skill_id,
                        related_ids=(d.entry_resource_id,),
                    )
                )
            elif entry.resource_kind != "skill":
                issues.append(
                    _issue(
                        "PIH.SKILL.ENTRY_KIND_INVALID",
                        "Skill entry has wrong kind.",
                        d.skill_id,
                        entry.path,
                        (entry.resource_id,),
                    )
                )
            for rid in d.required_resource_ids:
                if rid not in resources:
                    issues.append(
                        _issue(
                            "PIH.SKILL.CLOSURE_INCOMPLETE",
                            "Required resource is absent.",
                            d.skill_id,
                            related_ids=(rid,),
                        )
                    )
            if (
                d.skill_id,
                d.behavior_version,
            ) not in profile.supported_skill_behaviors:
                issues.append(
                    _issue(
                        "PIH.SKILL.BEHAVIOR_INCOMPATIBLE",
                        "Skill behavior is unsupported.",
                        d.skill_id,
                    )
                )
            if (
                d.authorization_policy_id not in profile.policy_reference_ids
                or d.authorization_policy_id not in d.required_resource_ids
            ):
                issues.append(
                    _issue(
                        "PIH.SKILL.POLICY_INCOMPATIBLE",
                        "Authorization policy is outside the declared closure.",
                        d.skill_id,
                        related_ids=(d.authorization_policy_id,),
                    )
                )
        return _result(tuple(issues))
