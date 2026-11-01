"""Immutable rank-two Procrustes selection evidence."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from typing import Self

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array, Int64Array
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor

from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StringWireEnum,
)


class Periodic1DRank2ProcrustesSelectionScope(StringWireEnum):
    """Identify whether one selection acts pointwise or globally."""

    POINTWISE = "pointwise"
    GLOBAL = "global"


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRank2ProcrustesDiagnostics(BaseTypedRecord):
    """Retain rank, objective, integrity, and backend evidence for one selection."""

    scope: Periodic1DRank2ProcrustesSelectionScope
    selection_count: int
    cross_singular_values: Float64Array
    numerical_ranks: Int64Array
    applied_rank_cutoffs: Float64Array
    rank_margins: Float64Array
    spectral_condition_numbers: tuple[float, ...]
    normalized_optimal_residuals: Float64Array
    normalized_objective_maximum: float
    normalized_objective_rms: float
    minimum_rank_margin: float
    maximum_unitarity_defect: float
    maximum_stationarity_defect: float
    maximum_objective_identity_defect: float
    maximum_psd_defect: float
    backend_identifier: str
    backend_version: str

    RETAINED_RANK = 2

    def __post_init__(self) -> None:
        """Admit a complete resolved rank-two selection inventory."""
        if type(self.scope) is not Periodic1DRank2ProcrustesSelectionScope:
            raise TypeError("scope must be the exact rank-two selection scope")
        if type(self.selection_count) is not int:
            raise TypeError("selection_count must be a built-in integer")
        if self.selection_count <= 0:
            raise ValueError("selection_count must be positive")
        if (
            self.scope is Periodic1DRank2ProcrustesSelectionScope.GLOBAL
            and self.selection_count != 1
        ):
            raise ValueError("global Procrustes diagnostics require one selection")
        singular = self._float_array(
            self.cross_singular_values,
            "cross_singular_values",
            ndim=2,
        )
        ranks = self._int_array(self.numerical_ranks, "numerical_ranks")
        cutoffs = self._float_array(
            self.applied_rank_cutoffs,
            "applied_rank_cutoffs",
        )
        margins = self._float_array(self.rank_margins, "rank_margins")
        residuals = self._float_array(
            self.normalized_optimal_residuals,
            "normalized_optimal_residuals",
        )
        if singular.shape != (self.selection_count, self.RETAINED_RANK):
            raise ValueError("cross_singular_values have the wrong selection shape")
        if any(
            values.shape != (self.selection_count,)
            for values in (ranks, cutoffs, margins, residuals)
        ):
            raise ValueError("selection diagnostic arrays have the wrong shape")
        if (
            type(self.spectral_condition_numbers) is not tuple
            or len(self.spectral_condition_numbers) != self.selection_count
        ):
            raise ValueError("spectral condition inventory has the wrong length")
        if (
            bool((singular < 0.0).any())
            or bool((cutoffs < 0.0).any())
            or bool((residuals < 0.0).any())
        ):
            raise ValueError(
                "singular values, cutoffs, and residuals must be nonnegative"
            )
        if bool((ranks != self.RETAINED_RANK).any()):
            raise ValueError(
                "rank-two Procrustes selection must be numerically full rank"
            )
        expected_margins = np.asarray(singular[:, -1] - cutoffs, dtype=np.float64)
        if not np.array_equal(margins, expected_margins):
            raise ValueError("rank_margins are inconsistent")
        expected_conditions = tuple(
            float(values[0] / values[-1]) for values in singular
        )
        if self.spectral_condition_numbers != expected_conditions:
            raise ValueError("spectral_condition_numbers are inconsistent")
        if any(
            type(value) is not float or not isfinite(value) or value < 1.0
            for value in self.spectral_condition_numbers
        ):
            raise ValueError(
                "spectral condition numbers must be finite and at least one"
            )
        expected_maximum = float(np.max(residuals))
        expected_rms = float(np.sqrt(np.mean(residuals**2)))
        expected_margin = float(np.min(margins))
        if self.normalized_objective_maximum != expected_maximum:
            raise ValueError("normalized_objective_maximum is inconsistent")
        if self.normalized_objective_rms != expected_rms:
            raise ValueError("normalized_objective_rms is inconsistent")
        if self.minimum_rank_margin != expected_margin:
            raise ValueError("minimum_rank_margin is inconsistent")
        if self.minimum_rank_margin <= 0.0:
            raise ValueError(
                "rank-two Procrustes selection must have positive rank margin"
            )
        for value, name in (
            (self.maximum_unitarity_defect, "maximum_unitarity_defect"),
            (self.maximum_stationarity_defect, "maximum_stationarity_defect"),
            (
                self.maximum_objective_identity_defect,
                "maximum_objective_identity_defect",
            ),
            (self.maximum_psd_defect, "maximum_psd_defect"),
        ):
            if type(value) is not float or not isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be a finite nonnegative built-in float")
        if type(self.backend_identifier) is not str or not self.backend_identifier:
            raise ValueError("backend_identifier must be a nonempty built-in string")
        if type(self.backend_version) is not str or not self.backend_version:
            raise ValueError("backend_version must be a nonempty built-in string")
        object.__setattr__(self, "cross_singular_values", singular)
        object.__setattr__(self, "numerical_ranks", ranks)
        object.__setattr__(self, "applied_rank_cutoffs", cutoffs)
        object.__setattr__(self, "rank_margins", margins)
        object.__setattr__(self, "normalized_optimal_residuals", residuals)

    @staticmethod
    def _float_array(
        value: Float64Array,
        name: str,
        *,
        ndim: int = 1,
    ) -> Float64Array:
        if not isinstance(value, np.ndarray) or value.ndim != ndim:
            raise ValueError(f"{name} must have {ndim} dimensions")
        return NumpyImmutableArrayConstructor(
            value,
            name,
            np.dtype(np.float64),
        ).execute()

    @staticmethod
    def _int_array(value: Int64Array, name: str) -> Int64Array:
        if not isinstance(value, np.ndarray) or value.ndim != 1:
            raise ValueError(f"{name} must be one dimensional")
        return NumpyImmutableArrayConstructor(
            value,
            name,
            np.dtype(np.int64),
        ).execute()

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "scope": self.scope.to_wire(),
            "selection_count": self.selection_count,
            "cross_singular_values": self.cross_singular_values,
            "numerical_ranks": self.numerical_ranks,
            "applied_rank_cutoffs": self.applied_rank_cutoffs,
            "rank_margins": self.rank_margins,
            "spectral_condition_numbers": self.spectral_condition_numbers,
            "normalized_optimal_residuals": self.normalized_optimal_residuals,
            "normalized_objective_maximum": self.normalized_objective_maximum,
            "normalized_objective_rms": self.normalized_objective_rms,
            "minimum_rank_margin": self.minimum_rank_margin,
            "maximum_unitarity_defect": self.maximum_unitarity_defect,
            "maximum_stationarity_defect": self.maximum_stationarity_defect,
            "maximum_objective_identity_defect": (
                self.maximum_objective_identity_defect
            ),
            "maximum_psd_defect": self.maximum_psd_defect,
            "backend_identifier": self.backend_identifier,
            "backend_version": self.backend_version,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "scope",
            "selection_count",
            "cross_singular_values",
            "numerical_ranks",
            "applied_rank_cutoffs",
            "rank_margins",
            "spectral_condition_numbers",
            "normalized_optimal_residuals",
            "normalized_objective_maximum",
            "normalized_objective_rms",
            "minimum_rank_margin",
            "maximum_unitarity_defect",
            "maximum_stationarity_defect",
            "maximum_objective_identity_defect",
            "maximum_psd_defect",
            "backend_identifier",
            "backend_version",
        }
        if set(values) != required:
            raise ValueError("rank-two Procrustes diagnostic fields do not match")
        scope = values["scope"]
        count = values["selection_count"]
        if type(scope) is not str or type(count) is not int:
            raise TypeError("scope and selection_count decode to wrong types")
        arrays: dict[str, np.ndarray] = {}
        for name in (
            "cross_singular_values",
            "numerical_ranks",
            "applied_rank_cutoffs",
            "rank_margins",
            "normalized_optimal_residuals",
        ):
            value = values[name]
            if not isinstance(value, np.ndarray):
                raise TypeError(f"{name} must decode to numpy.ndarray")
            arrays[name] = value
        conditions = values["spectral_condition_numbers"]
        if not isinstance(conditions, tuple) or any(
            type(value) is not float for value in conditions
        ):
            raise TypeError("spectral_condition_numbers must decode to a float tuple")
        floats: dict[str, float] = {}
        for name in (
            "normalized_objective_maximum",
            "normalized_objective_rms",
            "minimum_rank_margin",
            "maximum_unitarity_defect",
            "maximum_stationarity_defect",
            "maximum_objective_identity_defect",
            "maximum_psd_defect",
        ):
            value = values[name]
            if type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float")
            floats[name] = value
        backend_identifier = values["backend_identifier"]
        backend_version = values["backend_version"]
        if type(backend_identifier) is not str or type(backend_version) is not str:
            raise TypeError("backend evidence must decode to built-in strings")
        return cls(
            scope=Periodic1DRank2ProcrustesSelectionScope.from_wire(scope),
            selection_count=count,
            cross_singular_values=np.asarray(
                arrays["cross_singular_values"], dtype=np.float64
            ),
            numerical_ranks=np.asarray(arrays["numerical_ranks"], dtype=np.int64),
            applied_rank_cutoffs=np.asarray(
                arrays["applied_rank_cutoffs"], dtype=np.float64
            ),
            rank_margins=np.asarray(arrays["rank_margins"], dtype=np.float64),
            spectral_condition_numbers=conditions,
            normalized_optimal_residuals=np.asarray(
                arrays["normalized_optimal_residuals"], dtype=np.float64
            ),
            backend_identifier=backend_identifier,
            backend_version=backend_version,
            **floats,
        )


__all__ = [
    "Periodic1DRank2ProcrustesDiagnostics",
    "Periodic1DRank2ProcrustesSelectionScope",
]
