"""Project-local PI harness composition boundary.

The package has no ambient repository discovery or execution side effects. Callers
explicitly provide roots, bytes, and records. Generic policy is consumed through
:mod:`ksdft2effmass.harness.pi`.
"""

from .adapters import (
    AgentRecordAdapter,
    ChainRecordAdapter,
    CheckpointRecordAdapter,
    ChecksumCatalogAdapter,
    EvidenceModuleSelector,
    OwnershipManifestAdapter,
    SkillInventoryAdapter,
    TaskRecordAdapter,
)
from .context import LocalHarnessContextLoader
from .dbcontrol import (
    HarnessControlMigrationRequest,
    HarnessControlMigrationResult,
    HarnessControlMigrator,
    HarnessControlVerificationFinding,
    HarnessControlVerificationResult,
    HarnessControlVerifier,
)
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
    HarnessTaskSerializer,
)
from .validation import (
    HarnessValidationCheck,
    HarnessValidationRequest,
    HarnessValidationResult,
    HarnessValidator,
)

__all__ = [
    "AgentRecordAdapter",
    "ChainRecordAdapter",
    "CheckpointRecordAdapter",
    "ChecksumCatalogAdapter",
    "OwnershipManifestAdapter",
    "SkillInventoryAdapter",
    "TaskRecordAdapter",
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
    "HarnessControlMigrationRequest",
    "HarnessControlMigrationResult",
    "HarnessControlMigrator",
    "HarnessControlVerificationFinding",
    "HarnessControlVerificationResult",
    "HarnessControlVerifier",
]
