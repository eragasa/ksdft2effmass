"""One-way compatibility exports for development Task selection.

Architecture-v2 selection values and wire actions are owned by
:mod:`ksdft2effmass.harness.task_selection`. New code imports the v2 owner directly;
this module preserves existing project-local imports during migration.
"""

from ...task_selection import (
    DevelopmentTaskSelection,
    DevelopmentTaskSelectionDeserializer,
    DevelopmentTaskSelectionSerializer,
)

__all__ = (
    "DevelopmentTaskSelection",
    "DevelopmentTaskSelectionSerializer",
    "DevelopmentTaskSelectionDeserializer",
)
