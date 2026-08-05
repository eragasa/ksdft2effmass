"""Project-local PI harness composition and compatibility boundary.

The package has no ambient repository discovery or execution side effects.
Callers explicitly provide roots, bytes, records, routes, and observations.
All generic policy is consumed through :mod:`ksdft2effmass.harness.pi`.
"""

from .adapters import (
    AdaptAgentRecords,
    AdaptChainRecord,
    AdaptCheckpointRecords,
    AdaptChecksumCatalog,
    AdaptEvidenceOwnershipManifest,
    AdaptOwnershipManifest,
    AdaptSkillInventory,
    AdaptTaskRecords,
    SelectEvidenceModules,
)
from .context import LoadLocalHarnessContext
from .models import (
    AdaptationResult,
    EvidenceOwnershipRelation,
    LocalHarnessContext,
    LocalIssue,
    LocalValidationResult,
    RepositoryRoots,
    RouteConfiguration,
    ValidationRoute,
)
from .routing import (
    RollBackValidationRoute,
    RouteSelection,
    SelectValidationRoute,
)
from .shadow import (
    CompareShadowPair,
    LegacyInvocation,
    ReplayShadowSuite,
    ShadowObservation,
    ShadowPairResult,
    ShadowReplayResult,
)
from .validation import (
    AdaptedRepositoryRecords,
    RepositoryValidationResult,
    ValidateLocalRepository,
)

__all__ = [
    "AdaptAgentRecords",
    "AdaptChainRecord",
    "AdaptCheckpointRecords",
    "AdaptChecksumCatalog",
    "AdaptEvidenceOwnershipManifest",
    "AdaptOwnershipManifest",
    "AdaptSkillInventory",
    "AdaptTaskRecords",
    "AdaptationResult",
    "AdaptedRepositoryRecords",
    "CompareShadowPair",
    "EvidenceOwnershipRelation",
    "LegacyInvocation",
    "LoadLocalHarnessContext",
    "LocalHarnessContext",
    "LocalIssue",
    "LocalValidationResult",
    "ReplayShadowSuite",
    "RepositoryRoots",
    "RepositoryValidationResult",
    "RollBackValidationRoute",
    "RouteConfiguration",
    "RouteSelection",
    "SelectEvidenceModules",
    "SelectValidationRoute",
    "ShadowObservation",
    "ShadowPairResult",
    "ShadowReplayResult",
    "ValidateLocalRepository",
    "ValidationRoute",
]
