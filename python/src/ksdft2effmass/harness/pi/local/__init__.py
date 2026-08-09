"""Project-local PI harness composition and compatibility boundary.

The package has no ambient repository discovery or execution side effects.
Callers explicitly provide roots, bytes, records, routes, and observations.
All generic policy is consumed through :mod:`ksdft2effmass.harness.pi`.
"""

from .adapters import (
    AgentRecordAdapter,
    ChainRecordAdapter,
    CheckpointRecordAdapter,
    ChecksumCatalogAdapter,
    EvidenceModuleSelector,
    EvidenceOwnershipManifestAdapter,
    OwnershipManifestAdapter,
    SkillInventoryAdapter,
    TaskRecordAdapter,
)
from .context import LocalHarnessContextLoader
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
    LegacyRouteConfigurationPreparer,
    RouteSelection,
    ValidationRouteSelector,
)
from .shadow import (
    LegacyInvocation,
    ShadowObservation,
    ShadowPairComparator,
    ShadowPairResult,
    ShadowReplayResult,
    ShadowSuiteReplayer,
)
from .validation import (
    AdaptedRepositoryRecords,
    LocalRepositoryValidator,
    RepositoryValidationResult,
)

__all__ = [
    "AgentRecordAdapter",
    "ChainRecordAdapter",
    "CheckpointRecordAdapter",
    "ChecksumCatalogAdapter",
    "EvidenceOwnershipManifestAdapter",
    "OwnershipManifestAdapter",
    "SkillInventoryAdapter",
    "TaskRecordAdapter",
    "AdaptationResult",
    "AdaptedRepositoryRecords",
    "ShadowPairComparator",
    "EvidenceOwnershipRelation",
    "LegacyInvocation",
    "LocalHarnessContextLoader",
    "LocalHarnessContext",
    "LocalIssue",
    "LocalValidationResult",
    "ShadowSuiteReplayer",
    "RepositoryRoots",
    "RepositoryValidationResult",
    "LegacyRouteConfigurationPreparer",
    "RouteConfiguration",
    "RouteSelection",
    "EvidenceModuleSelector",
    "ValidationRouteSelector",
    "ShadowObservation",
    "ShadowPairResult",
    "ShadowReplayResult",
    "LocalRepositoryValidator",
    "ValidationRoute",
]
