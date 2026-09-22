"""Compatibility facade for project-local record adapters.

The concrete ActionObjects live with their Task, control-record, ownership,
resource, and evidence contracts.  This module preserves the previously
importable ``ksdft2effmass.harness.pi.local.adapters`` names without owning
adapter behavior or introducing a generic adapter framework.
"""

from .control_record_adapters import AgentRecordAdapter, CheckpointRecordAdapter
from .evidence_adapters import EvidenceModuleSelector
from .ownership_adapters import OwnershipManifestAdapter
from .resource_adapters import ChecksumCatalogAdapter, SkillInventoryAdapter

__all__ = [
    "AgentRecordAdapter",
    "CheckpointRecordAdapter",
    "ChecksumCatalogAdapter",
    "EvidenceModuleSelector",
    "OwnershipManifestAdapter",
    "SkillInventoryAdapter",
]
