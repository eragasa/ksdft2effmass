"""Reusable final representation boundary for verification values."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Self

import numpy as np
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    VectorQuantity,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


class BaseVerification(BaseTypedRecord):
    """Identify a verification while inheriting final representation boundaries."""

    __slots__ = ()


class VisualizationVerification(BaseVerification, ABC):
    """Expose only the verification values required to authenticate rendering."""

    __slots__ = ()

    @property
    @abstractmethod
    def passed(self) -> bool:
        """Return whether the complete concrete verification passed."""

    @abstractmethod
    def authenticated_visualization_data_sha256(self) -> str:
        """Return the digest of the authenticated canonical projection bytes."""


@dataclass(frozen=True, slots=True)
class VerificationObservation(BaseVerification):
    """Retain one nonnegative discrepancy and its absolute tolerance."""

    value: ScalarQuantity
    tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        if not isinstance(self.value, ScalarQuantity):
            raise TypeError("verification value must be ScalarQuantity")
        if not isinstance(self.tolerance, ScalarQuantity):
            raise TypeError("verification tolerance must be ScalarQuantity")
        if self.value.unit != self.tolerance.unit:
            raise ValueError("verification value and tolerance units must agree")
        if not np.isfinite(self.value.magnitude) or self.value.magnitude < 0.0:
            raise ValueError("verification value must be finite and nonnegative")
        if not np.isfinite(self.tolerance.magnitude) or self.tolerance.magnitude < 0.0:
            raise ValueError("verification tolerance must be finite and nonnegative")

    @property
    def passed(self) -> bool:
        """Return whether the discrepancy satisfies its tolerance."""
        return self.value.magnitude <= self.tolerance.magnitude

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"value": self.value, "tolerance": self.tolerance}

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        if set(values) != {"value", "tolerance"}:
            raise ValueError("verification observation fields do not match")
        value = values["value"]
        tolerance = values["tolerance"]
        if not isinstance(value, ScalarQuantity) or not isinstance(
            tolerance, ScalarQuantity
        ):
            raise TypeError(
                "verification observation values must decode to ScalarQuantity"
            )
        return cls(value=value, tolerance=tolerance)


type VerificationComparableQuantity = (
    ScalarQuantity
    | VectorQuantity
    | ComplexVectorQuantity
    | MatrixQuantity
    | ComplexMatrixQuantity
)


@dataclass(frozen=True, slots=True)
class MaximumAbsoluteErrorComparison:
    """Calculate one unit-preserving maximum absolute discrepancy."""

    observed: VerificationComparableQuantity
    reference: VerificationComparableQuantity
    tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        supported_types = (
            ScalarQuantity
            | VectorQuantity
            | ComplexVectorQuantity
            | MatrixQuantity
            | ComplexMatrixQuantity
        )
        if not isinstance(self.observed, supported_types):
            raise TypeError("observed must be a supported model-system quantity")
        if not isinstance(self.reference, supported_types):
            raise TypeError("reference must be a supported model-system quantity")
        if not isinstance(self.tolerance, ScalarQuantity):
            raise TypeError("tolerance must be ScalarQuantity")
        if self.observed.unit != self.reference.unit:
            raise ValueError("observed and reference units must agree")
        if self.tolerance.unit != self.observed.unit:
            raise ValueError("comparison tolerance unit must agree with its values")
        if not np.isfinite(self.tolerance.magnitude) or self.tolerance.magnitude < 0.0:
            raise ValueError("comparison tolerance must be finite and nonnegative")
        observed = np.asarray(self.observed.magnitude)
        reference = np.asarray(self.reference.magnitude)
        if observed.shape != reference.shape:
            raise ValueError("observed and reference shapes must agree")
        if observed.size == 0:
            raise ValueError("comparison values must be nonempty")

    def result(self) -> VerificationObservation:
        """Return the maximum absolute discrepancy and declared tolerance."""
        observed = np.asarray(self.observed.magnitude)
        reference = np.asarray(self.reference.magnitude)
        difference = float(np.max(np.abs(observed - reference)))
        return VerificationObservation(
            value=ScalarQuantity(difference, self.observed.unit),
            tolerance=self.tolerance,
        )


@dataclass(frozen=True, slots=True)
class CompositeVerification(BaseVerification):
    """Compose a nonempty, uniquely named set of verification observations."""

    observations: Mapping[str, VerificationObservation]

    def __post_init__(self) -> None:
        if not isinstance(self.observations, Mapping):
            raise TypeError("observations must be a mapping")
        if not self.observations:
            raise ValueError("observations must not be empty")
        copied: dict[str, VerificationObservation] = {}
        for name, observation in self.observations.items():
            if type(name) is not str or not name:
                raise TypeError("observation names must be nonempty built-in strings")
            if not isinstance(observation, VerificationObservation):
                raise TypeError("observations must contain VerificationObservation")
            copied[name] = observation
        object.__setattr__(self, "observations", MappingProxyType(copied))

    @classmethod
    def evaluate(
        cls,
        comparisons: Mapping[str, MaximumAbsoluteErrorComparison],
    ) -> Self:
        """Calculate named observations from reusable maximum-error comparisons."""
        if not isinstance(comparisons, Mapping):
            raise TypeError("comparisons must be a mapping")
        return cls(
            observations={
                name: comparison.result() for name, comparison in comparisons.items()
            }
        )

    @property
    def passed(self) -> bool:
        """Return whether every composed observation passes."""
        return all(observation.passed for observation in self.observations.values())

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "observations": {
                name: observation.to_dict()
                for name, observation in self.observations.items()
            }
        }

    @classmethod
    def _from_mapping(
        cls,
        values: Mapping[str, SerializableValue],
    ) -> Self:
        if set(values) != {"observations"}:
            raise ValueError("composite verification fields do not match")
        observations_value = values["observations"]
        if not isinstance(observations_value, Mapping):
            raise TypeError("observations must decode to a mapping")
        observations: dict[str, VerificationObservation] = {}
        for name, observation_value in observations_value.items():
            if type(name) is not str or not isinstance(observation_value, Mapping):
                raise TypeError("decoded observations must map strings to mappings")
            observations[name] = VerificationObservation.from_dict(observation_value)
        return cls(observations=observations)
