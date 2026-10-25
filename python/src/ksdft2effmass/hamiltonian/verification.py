"""Reusable verification values for Hamiltonians and spectral reductions."""

from __future__ import annotations

from ksdft2effmass.verification import CompositeVerification


class HamiltonianVerification(CompositeVerification):
    """Compose verification observations for one represented Hamiltonian."""


class SpectralReductionVerification(CompositeVerification):
    """Compose verification observations for one spectral reduction."""
