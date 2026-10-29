"""Hamiltonian records, subspaces, reduction, diagnostics, and decomposition."""

from .blocks import (
    OrthogonalHamiltonianBlockAnalyzer,
    OrthogonalHamiltonianBlockResult,
)
from .decomposition import HamiltonianDecomposition
from .records import Hamiltonian, HermitianHamiltonian, ReducedHamiltonian
from .reduction import SpectralReduction
from .subspaces import (
    OrthogonalSpectralSubspace,
    OrthogonalSpectralSubspaceSelectionRequest,
    OrthogonalSpectralSubspaceSelector,
    SpectralSubspace,
)
from .verification import HamiltonianVerification, SpectralReductionVerification

__all__ = [
    "Hamiltonian",
    "HamiltonianDecomposition",
    "HamiltonianVerification",
    "HermitianHamiltonian",
    "OrthogonalHamiltonianBlockAnalyzer",
    "OrthogonalHamiltonianBlockResult",
    "OrthogonalSpectralSubspace",
    "OrthogonalSpectralSubspaceSelectionRequest",
    "OrthogonalSpectralSubspaceSelector",
    "ReducedHamiltonian",
    "SpectralReduction",
    "SpectralReductionVerification",
    "SpectralSubspace",
]
