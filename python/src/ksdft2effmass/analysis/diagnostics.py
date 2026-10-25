"""Typed observations and nominal actions for scientific diagnostics."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.units import ScalarQuantity, VectorQuantity

from ksdft2effmass.serialization import SerializableValue


@dataclass(frozen=True, slots=True)
class MatrixNormDiagnosticOptions:
    """Record the selected matrix norm for one matrix diagnostic."""

    matrix_norm: MatrixNormEnum

    def __post_init__(self) -> None:
        if not isinstance(self.matrix_norm, MatrixNormEnum):
            raise TypeError("matrix_norm must be MatrixNormEnum")

    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return the typed option mapping without JSON normalization."""
        return {"matrix_norm": self.matrix_norm}

    @classmethod
    def from_dict(
        cls, values: Mapping[str, SerializableValue]
    ) -> MatrixNormDiagnosticOptions:
        """Reconstruct matrix-norm options from a typed mapping."""
        if set(values) != {"matrix_norm"}:
            raise ValueError("matrix-norm option fields do not match the contract")
        matrix_norm = values["matrix_norm"]
        if not isinstance(matrix_norm, MatrixNormEnum):
            raise TypeError("matrix_norm must be MatrixNormEnum")
        return cls(matrix_norm=matrix_norm)


@dataclass(frozen=True, slots=True, eq=False)
class DiagnosticObservation:
    """Retain one diagnostic value and its explicit comparison policy."""

    value: ScalarQuantity | VectorQuantity
    atol: ScalarQuantity
    rtol: float
    options: MatrixNormDiagnosticOptions | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.value, ScalarQuantity | VectorQuantity):
            raise TypeError("value must be ScalarQuantity or VectorQuantity")
        values = np.asarray(self.value.magnitude)
        if np.any(~np.isfinite(values)):
            raise ValueError("diagnostic values must be finite")
        if np.any(values < 0.0):
            raise ValueError("diagnostic values must be nonnegative")
        if not isinstance(self.atol, ScalarQuantity):
            raise TypeError("atol must be ScalarQuantity")
        if not np.isfinite(self.atol.magnitude) or self.atol.magnitude < 0.0:
            raise ValueError("atol must be finite and nonnegative")
        if self.atol.unit != self.value.unit:
            raise ValueError("atol and value must use the same unit")
        if type(self.rtol) is not float:
            raise TypeError("rtol must be a built-in float")
        if not np.isfinite(self.rtol) or self.rtol < 0.0:
            raise ValueError("rtol must be finite and nonnegative")
        if self.options is not None and not isinstance(
            self.options, MatrixNormDiagnosticOptions
        ):
            raise TypeError("options must be MatrixNormDiagnosticOptions or None")

    def to_dict(self) -> Mapping[str, SerializableValue]:
        """Return the typed observation mapping without JSON normalization."""
        return {
            "value": self.value,
            "atol": self.atol,
            "rtol": self.rtol,
            "options": self.options,
        }

    @classmethod
    def from_dict(
        cls, values: Mapping[str, SerializableValue]
    ) -> DiagnosticObservation:
        """Reconstruct one observation from a typed mapping."""
        if set(values) != {"value", "atol", "rtol", "options"}:
            raise ValueError("diagnostic observation fields do not match the contract")
        value = values["value"]
        atol = values["atol"]
        rtol = values["rtol"]
        options_value = values["options"]
        if not isinstance(value, ScalarQuantity | VectorQuantity):
            raise TypeError("value must be a scalar or vector quantity")
        if not isinstance(atol, ScalarQuantity):
            raise TypeError("atol must be ScalarQuantity")
        if type(rtol) is not float:
            raise TypeError("rtol must be a built-in float")
        options: MatrixNormDiagnosticOptions | None
        if options_value is None:
            options = None
        elif isinstance(options_value, Mapping):
            options = MatrixNormDiagnosticOptions.from_dict(options_value)
        else:
            raise TypeError("options must be a typed mapping or None")
        return cls(value=value, atol=atol, rtol=rtol, options=options)


class BaseDiagnosticAnalyzer[DiagnosticMethodT: Enum](ABC):
    """Define the nominal action contract for one scientific diagnostic."""

    __slots__ = ()

    @property
    @abstractmethod
    def method(self) -> DiagnosticMethodT:
        """Return the diagnostic method implemented by this action."""

    @abstractmethod
    def result(self) -> DiagnosticObservation:
        """Return the immutable diagnostic observation."""
