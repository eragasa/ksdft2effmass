"""Composable verification values for represented model-system analyses."""

from __future__ import annotations

from abc import ABC
from collections.abc import Mapping
from types import MappingProxyType
from typing import final

from ksdft2effmass.verification import BaseVerification, CompositeVerification


class BaseModelAnalysisVerification(BaseVerification, ABC):
    """Own behavior common to authenticated model-analysis verification values."""

    __slots__ = ()

    subject_sha256: str
    visualization_data_sha256: str
    components: tuple[CompositeVerification, ...]

    @final
    def _validate_common_fields(self) -> None:
        """Validate digests, component storage, and global observation identity."""
        self._validate_digest(self.subject_sha256, "subject_sha256")
        self._validate_digest(
            self.visualization_data_sha256,
            "visualization_data_sha256",
        )
        if not isinstance(self.components, tuple):
            raise TypeError("components must be a tuple")
        names: set[str] = set()
        for component in self.components:
            if not isinstance(component, CompositeVerification):
                raise TypeError("components must contain CompositeVerification values")
            overlap = names.intersection(component.observations)
            if overlap:
                raise ValueError(
                    "verification observation names must be globally unique"
                )
            names.update(component.observations)

    @property
    @final
    def passed(self) -> bool:
        """Return whether every model-analysis verification component passes."""
        return all(component.passed for component in self.components)

    @property
    @final
    def checks(self) -> Mapping[str, float]:
        """Return a read-only mapping of operation-qualified discrepancy values."""
        return MappingProxyType(
            {
                name: observation.value.magnitude
                for component in self.components
                for name, observation in component.observations.items()
            }
        )

    @property
    @final
    def check_tolerances(self) -> Mapping[str, float]:
        """Return a read-only mapping of operation-qualified tolerances."""
        return MappingProxyType(
            {
                name: observation.tolerance.magnitude
                for component in self.components
                for name, observation in component.observations.items()
            }
        )

    @final
    def authenticated_visualization_data_sha256(self) -> str:
        """Return the authenticated visualization-data SHA-256 digest.

        Returns
        -------
        str
            Lowercase digest of the exact canonical projection JSON bytes.
        """
        return self.visualization_data_sha256

    @staticmethod
    @final
    def _validate_digest(value: str, name: str) -> None:
        """Require one named value to be a lowercase SHA-256 digest."""
        if (
            type(value) is not str
            or len(value) != 64
            or any(character not in "0123456789abcdef" for character in value)
        ):
            raise ValueError(f"{name} must be a lowercase SHA-256 digest")


class QuadratureVerification(CompositeVerification):
    """Compose verification observations for one represented quadrature rule."""


class VisualizationProjectionVerification(CompositeVerification):
    """Compose correlations for one derived visualization projection."""
