"""Deprecated compatibility façade for the periodic-1D hopping Workflow.

Canonical periodic-1D campaign families, including the Wannier90 integration, are not
re-exported from this publication-oriented route.
"""

import warnings

from ...periodic_1d import (
    Periodic1DHoppingReductionRequest,
    Periodic1DHoppingReductionResult,
    Periodic1DHoppingReductionWorkflow,
)

warnings.warn(
    "ksdft2effmass.campaigns.research_monograph.periodic_1d is deprecated; "
    "import ksdft2effmass.campaigns.periodic_1d instead",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "Periodic1DHoppingReductionRequest",
    "Periodic1DHoppingReductionResult",
    "Periodic1DHoppingReductionWorkflow",
]
