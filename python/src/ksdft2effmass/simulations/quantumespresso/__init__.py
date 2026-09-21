"""Public Quantum ESPRESSO Workflow simulation composition contracts.

The subpackage owns project-specific Quantum ESPRESSO Workflow simulation identities,
execution-free toolchain recipes, and composition above generic Workflow, toolchain,
and QE-native integration boundaries. It delegates native workspace and process
mechanics to the integration package and owns no installation, compilation, authority
issuance, retry policy, numerical verification, or scientific validation.
"""

from .planning import (
    QuantumEspressoExecution,
    QuantumEspressoExecutionRequest,
    QuantumEspressoPlanner,
)
from .pseudopotentials import (
    QuantumEspressoPseudopotentialAdapter,
    QuantumEspressoPseudopotentialReference,
)
from .run_identity import QuantumEspressoBundledExampleRunIdentity
from .toolchain import (
    QuantumEspressoOpenBlasComparatorBuildPlan,
    QuantumEspressoOpenBlasComparatorBuildPlanner,
    QuantumEspressoOpenBlasComparatorBuildRequest,
)

__all__ = [
    "QuantumEspressoBundledExampleRunIdentity",
    "QuantumEspressoExecution",
    "QuantumEspressoExecutionRequest",
    "QuantumEspressoPlanner",
    "QuantumEspressoPseudopotentialAdapter",
    "QuantumEspressoPseudopotentialReference",
    "QuantumEspressoOpenBlasComparatorBuildPlan",
    "QuantumEspressoOpenBlasComparatorBuildPlanner",
    "QuantumEspressoOpenBlasComparatorBuildRequest",
]
