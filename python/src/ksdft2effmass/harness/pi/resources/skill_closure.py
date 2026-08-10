"""Skill descriptor and resource-closure validation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..identity import ArtifactIdentity, _require_tuple
from ..validation import ValidationResult, _issue, _result
from .manifests import ResourceManifestValidator
from .records import ResourceManifest, SkillDescriptor

if TYPE_CHECKING:
    from ..profiles import ProjectProfile


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
        from ..profiles import ProjectProfile

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
