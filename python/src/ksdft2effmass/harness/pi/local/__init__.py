"""Project-local PI harness composition boundary.

The package has no ambient repository discovery or execution side effects. Callers
explicitly provide roots, bytes, and records. Generic policy is consumed through
:mod:`ksdft2effmass.harness.pi`.
"""

from .adapters import (
    AgentRecordAdapter,
    CheckpointRecordAdapter,
    ChecksumCatalogAdapter,
    EvidenceModuleSelector,
    OwnershipManifestAdapter,
    SkillInventoryAdapter,
)
from .context import LocalHarnessContextLoader
from .models import (
    AdaptationResult,
    LocalHarnessContext,
    LocalIssue,
    LocalValidationResult,
    RepositoryRoots,
)
from .task_model import (
    ArchivedTaskSource,
    HarnessTask,
    HarnessTaskDeserializer,
    HarnessTaskGraphValidator,
    HarnessTaskRegistry,
    HarnessTaskSerializer,
)
from .task_selection import (
    DevelopmentTaskSelection,
    DevelopmentTaskSelectionDeserializer,
    DevelopmentTaskSelectionSerializer,
)
from .validation import (
    HarnessValidationCheck,
    HarnessValidationRequest,
    HarnessValidationResult,
    HarnessValidator,
)

__all__ = [
    "AgentRecordAdapter",
    "CheckpointRecordAdapter",
    "ChecksumCatalogAdapter",
    "OwnershipManifestAdapter",
    "SkillInventoryAdapter",
    "AdaptationResult",
    "LocalHarnessContextLoader",
    "LocalHarnessContext",
    "LocalIssue",
    "LocalValidationResult",
    "RepositoryRoots",
    "EvidenceModuleSelector",
    "HarnessValidationRequest",
    "HarnessValidationCheck",
    "HarnessValidationResult",
    "HarnessValidator",
    "ArchivedTaskSource",
    "HarnessTask",
    "HarnessTaskSerializer",
    "HarnessTaskDeserializer",
    "HarnessTaskGraphValidator",
    "HarnessTaskRegistry",
    "DevelopmentTaskSelection",
    "DevelopmentTaskSelectionSerializer",
    "DevelopmentTaskSelectionDeserializer",
]
