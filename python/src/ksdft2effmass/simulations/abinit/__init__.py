"""Public ABINIT Workflow simulation composition contracts.

The subpackage owns project-specific ABINIT composition above the backend-neutral DFT
simulation and ABINIT-native integration boundaries.  Its pseudopotential adapter
binds cataloged PSP8 artifacts without downloading files, invoking ABINIT, or making
scientific compatibility claims.
"""

from .pseudopotentials import (
    AbinitPseudopotentialAdapter,
    AbinitPseudopotentialReference,
)

__all__ = [
    "AbinitPseudopotentialAdapter",
    "AbinitPseudopotentialReference",
]
