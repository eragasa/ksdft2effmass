"""Composable verification values for represented model-system analyses."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ksdft2effmass.verification import BaseVerification, CompositeVerification


class BaseModelAnalysisVerification(BaseVerification, ABC):
    """Require one authenticated visualization binding for model analysis."""

    __slots__ = ()

    @property
    @abstractmethod
    def passed(self) -> bool:
        """Return whether every model-analysis verification component passes."""

    @abstractmethod
    def authenticated_visualization_data_sha256(self) -> str:
        """Return the authenticated visualization-data SHA-256 digest.

        Returns
        -------
        str
            Lowercase digest of the exact canonical projection JSON bytes.
        """


class QuadratureVerification(CompositeVerification):
    """Compose verification observations for one represented quadrature rule."""


class VisualizationProjectionVerification(CompositeVerification):
    """Compose correlations for one derived visualization projection."""
