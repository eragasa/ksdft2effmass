"""Stable resource contract with cohesive internal ownership."""

from .manifests import ResourceManifestValidator
from .records import (
    ResourceManifest,
    ResourceManifestRefreshRequest,
    ResourceManifestRefreshResult,
    ResourceReference,
    SkillDescriptor,
)
from .refresh import ResourceManifestRefresher
from .resolution import ResourceResolver, _confined_file  # noqa: F401
from .skill_closure import SkillResourceValidator

__all__ = (
    "ResourceManifest",
    "ResourceManifestRefresher",
    "ResourceManifestRefreshRequest",
    "ResourceManifestRefreshResult",
    "ResourceManifestValidator",
    "ResourceReference",
    "ResourceResolver",
    "SkillDescriptor",
    "SkillResourceValidator",
)
