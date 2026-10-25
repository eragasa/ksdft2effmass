"""Composable verification values for represented model-system analyses."""

from __future__ import annotations

from ksdft2effmass.verification import CompositeVerification


class QuadratureVerification(CompositeVerification):
    """Compose verification observations for one represented quadrature rule."""


class VisualizationProjectionVerification(CompositeVerification):
    """Compose correlations for one derived visualization projection."""
