"""Resource manifest compatibility and dependency-closure validation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..identity import ArtifactIdentity
from ..validation import JsonRecordSerializer, ValidationResult, _issue, _result
from .records import ResourceManifest, ResourceReference

if TYPE_CHECKING:
    from ..profiles import ProjectProfile


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
        from ..profiles import ProjectProfile

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
