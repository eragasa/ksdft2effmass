"""Composable verification values for reusable numerical analyses."""

from __future__ import annotations

from ksdft2effmass.verification import CompositeVerification


class EigensystemVerification(CompositeVerification):
    """Compose verification observations for one represented eigensystem."""


class RelativeErrorConvergenceVerification(CompositeVerification):
    """Compose verification observations for relative-error convergence data."""


class TailProbabilitySelectionVerification(CompositeVerification):
    """Compose verification observations for a finite tail selection."""


class KineticPotentialDecompositionVerification(CompositeVerification):
    """Compose verification observations for a kinetic-potential decomposition."""


class DiagnosticVerification(CompositeVerification):
    """Compose verification observations for serialized diagnostics."""
