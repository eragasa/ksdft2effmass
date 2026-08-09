"""Resource records, validation, explicit-root identity refresh, and resolution."""

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
    JsonRecordSerializer,
    ResourceResolutionResult,
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


def _manifest_maps(
    generic: ResourceManifest, local: ResourceManifest | None
) -> tuple[dict[str, ResourceReference], dict[str, ResourceReference]]:
    return (
        {r.resource_id: r for r in generic.resources},
        {} if local is None else {r.resource_id: r for r in local.resources},
    )


class ResourceManifestValidator:
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
        actual = JsonRecordSerializer().execute(generic_manifest).content_identity
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
                and JsonRecordSerializer().execute(local_manifest).content_identity
                != local_manifest_identity
            ):
                issues.append(
                    _issue(
                        "PIH.RESOURCE.MANIFEST_MISMATCH",
                        "Local manifest content identity differs.",
                        local_manifest.manifest_id,
                    )
                )
        generic_resources = generic_manifest.resources
        local_resources = () if local_manifest is None else local_manifest.resources

        for resources in (generic_resources, local_resources):
            ids = tuple(resource.resource_id for resource in resources)
            for rid in sorted({value for value in ids if ids.count(value) > 1}):
                issues.append(
                    _issue(
                        "PIH.RESOURCE.DUPLICATE_ID",
                        "Resource ID occurs more than once in one manifest.",
                        rid,
                    )
                )
            paths = tuple(resource.path for resource in resources)
            for path in sorted({value for value in paths if paths.count(value) > 1}):
                related_ids = tuple(
                    sorted(
                        {
                            resource.resource_id
                            for resource in resources
                            if resource.path == path
                        }
                    )
                )
                issues.append(
                    _issue(
                        "PIH.RESOURCE.DUPLICATE_PATH",
                        "Resource path occurs more than once in one manifest.",
                        path=path,
                        related_ids=related_ids,
                    )
                )

        generic_ids = {resource.resource_id for resource in generic_resources}
        local_ids = {resource.resource_id for resource in local_resources}
        for rid in sorted(generic_ids & local_ids):
            issues.append(
                _issue(
                    "PIH.RESOURCE.OVERLAY_REPLACEMENT",
                    "Local resource replaces a generic ID.",
                    rid,
                )
            )
        generic_paths = {resource.path for resource in generic_resources}
        for resource in local_resources:
            if resource.path in generic_paths:
                related_ids = tuple(
                    sorted(
                        {
                            generic.resource_id
                            for generic in generic_resources
                            if generic.path == resource.path
                        }
                    )
                )
                issues.append(
                    _issue(
                        "PIH.RESOURCE.OVERLAY_REPLACEMENT",
                        "Local resource reuses a generic path.",
                        resource.resource_id,
                        resource.path,
                        related_ids,
                    )
                )

        supported = set(profile.supported_resource_formats)
        supported_kinds = {kind for kind, _ in supported}
        all_ids = generic_ids | local_ids
        graph_sets: dict[str, set[str]] = {}
        for layer, resources in (
            ("generic", generic_resources),
            ("local", local_resources),
        ):
            for resource in resources:
                rid = resource.resource_id
                if resource.resource_kind not in supported_kinds:
                    issues.append(
                        _issue(
                            "PIH.RESOURCE.KIND_UNSUPPORTED",
                            "Resource kind is not profiled.",
                            rid,
                            resource.path,
                        )
                    )
                elif (resource.resource_kind, resource.format_version) not in supported:
                    issues.append(
                        _issue(
                            "PIH.RESOURCE.VERSION_INCOMPATIBLE",
                            "Resource format version is not profiled.",
                            rid,
                            resource.path,
                        )
                    )
                valid_edges = graph_sets.setdefault(rid, set())
                for dep in resource.dependency_ids:
                    if dep not in all_ids:
                        issues.append(
                            _issue(
                                "PIH.RESOURCE.MISSING_DEPENDENCY",
                                "Dependency is absent.",
                                rid,
                                resource.path,
                                (dep,),
                            )
                        )
                    elif layer == "generic" and dep in local_ids:
                        issues.append(
                            _issue(
                                "PIH.RESOURCE.GENERIC_TO_LOCAL_DEPENDENCY",
                                "Generic resource depends on local resource.",
                                rid,
                                resource.path,
                                (dep,),
                            )
                        )
                    else:
                        valid_edges.add(dep)
        graph = {
            resource_id: tuple(sorted(dependency_ids))
            for resource_id, dependency_ids in graph_sets.items()
        }
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


class ResourceManifestRefresher:
    """Refresh selected content identities beneath one explicit root.

    The stateless action resolves only paths already declared by the supplied
    manifest, reuses the same exact-case, nonsymlink, root-confined regular-file
    observation as :class:`ResourceResolver`, and computes SHA-256 from observed
    bytes. It returns a new manifest without discovering resources or writing a
    file.
    """

    __slots__ = ()

    def execute(
        self, request: ResourceManifestRefreshRequest
    ) -> ResourceManifestRefreshResult:
        """Return a canonical manifest proposal for the explicit selection.

        Parameters
        ----------
        request
            Existing manifest, explicit absolute root, and selected resource IDs.

        Returns
        -------
        ResourceManifestRefreshResult
            Proposed immutable manifest, changed identities, and deterministic
            findings. A failed result contains no partial manifest.

        Raises
        ------
        TypeError
            If ``request`` is not exactly ``ResourceManifestRefreshRequest``.
        HarnessInternalError
            If bytes cannot be read after successful path observation.
        """
        if type(request) is not ResourceManifestRefreshRequest:
            raise TypeError("request must be ResourceManifestRefreshRequest")

        by_id: dict[str, list[ResourceReference]] = {}
        for resource in request.manifest.resources:
            by_id.setdefault(resource.resource_id, []).append(resource)

        selected: dict[str, tuple[ResourceReference, Path]] = {}
        issues: list[ValidationIssue] = []
        for resource_id in request.resource_ids:
            matches = by_id.get(resource_id, [])
            if not matches:
                issues.append(
                    _issue(
                        "PIH.RESOURCE.NOT_FOUND",
                        "Resource ID was not found.",
                        resource_id,
                    )
                )
                continue
            if len(matches) != 1:
                issues.append(
                    _issue(
                        "PIH.RESOURCE.AMBIGUOUS_SELECTION",
                        "Resource ID is ambiguous.",
                        resource_id,
                    )
                )
                continue
            reference = matches[0]
            path, problem = _confined_file(request.root, reference.path)
            if problem is not None:
                issues.append(problem)
                continue
            if path is None:
                raise AssertionError("successful confinement must return a path")
            selected[resource_id] = (reference, path)

        validation = _result(tuple(issues))
        if validation.status == "FAIL":
            return ResourceManifestRefreshResult(None, (), validation)

        identities: dict[str, ArtifactIdentity] = {}
        changed_ids: list[str] = []
        for resource_id in request.resource_ids:
            reference, path = selected[resource_id]
            try:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as exc:
                raise HarnessInternalError(
                    "ResourceManifestRefresher", str(exc)
                ) from exc
            identity = ArtifactIdentity(1, "sha256", digest)
            identities[resource_id] = identity
            if identity != reference.content_identity:
                changed_ids.append(resource_id)

        refreshed_resources = tuple(
            ResourceReference(
                resource.schema_version,
                resource.resource_id,
                resource.resource_kind,
                resource.format_version,
                resource.path,
                identities[resource.resource_id],
                resource.dependency_ids,
            )
            if resource.resource_id in identities
            and identities[resource.resource_id] != resource.content_identity
            else resource
            for resource in request.manifest.resources
        )
        refreshed_manifest = ResourceManifest(
            request.manifest.schema_version,
            request.manifest.manifest_id,
            request.manifest.manifest_version,
            request.manifest.layer,
            request.manifest.extends_manifest_id,
            refreshed_resources,
        )
        return ResourceManifestRefreshResult(
            refreshed_manifest, tuple(changed_ids), validation
        )


class ResourceResolver:
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
        validation = ResourceManifestValidator().execute(
            generic_manifest,
            generic_manifest_identity,
            local_manifest,
            local_manifest_identity,
            profile,
        )
        if validation.status == "FAIL":
            return ResourceResolutionResult(None, None, validation)
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
            raise HarnessInternalError("ResourceResolver", str(exc)) from exc
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


class SkillResourceValidator:
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
        base = ResourceManifestValidator().execute(
            generic_manifest,
            generic_manifest_identity,
            local_manifest,
            local_manifest_identity,
            profile,
        )
        if base.status == "FAIL":
            return base
        _require_tuple(descriptors, "descriptors")
        if any(type(d) is not SkillDescriptor for d in descriptors):
            raise TypeError("descriptors must contain SkillDescriptor")
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
