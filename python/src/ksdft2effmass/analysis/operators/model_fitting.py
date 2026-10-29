"""Model-class fitting tools for finite represented operators."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.units import (
    MatrixQuantity,
    ScalarQuantity,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True, eq=False)
class RetainedModelClassFitResult(BaseTypedRecord):
    """Retain one best-fit model, residual, and Frobenius norm.

    Parameters
    ----------
    name
        Stable model-class name.
    best_fit
        Orthogonal Frobenius projection of the target onto the model class.
    unexplained_residual
        Difference between the target and ``best_fit``.
    unexplained_frobenius_norm
        Canonical Frobenius norm of ``unexplained_residual``.

    Raises
    ------
    TypeError
        A field has the wrong domain type.
    ValueError
        Fit, residual, and norm units or matrix shapes disagree.
    """

    name: str
    best_fit: MatrixQuantity
    unexplained_residual: MatrixQuantity
    unexplained_frobenius_norm: ScalarQuantity

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise TypeError("name must be a nonempty string")
        if not isinstance(self.best_fit, MatrixQuantity):
            raise TypeError("best_fit must be MatrixQuantity")
        if not isinstance(self.unexplained_residual, MatrixQuantity):
            raise TypeError("unexplained_residual must be MatrixQuantity")
        if not isinstance(self.unexplained_frobenius_norm, ScalarQuantity):
            raise TypeError("unexplained_frobenius_norm must be ScalarQuantity")
        if self.best_fit.unit != self.unexplained_residual.unit:
            raise ValueError("fit and residual units must agree")
        if self.best_fit.magnitude.shape != self.unexplained_residual.magnitude.shape:
            raise ValueError("fit and residual shapes must agree")
        if self.unexplained_frobenius_norm.unit != self.best_fit.unit:
            raise ValueError("fit norm unit must agree with its matrices")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "name": self.name,
            "best_fit": self.best_fit,
            "unexplained_residual": self.unexplained_residual,
            "unexplained_frobenius_norm": self.unexplained_frobenius_norm,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "name",
            "best_fit",
            "unexplained_residual",
            "unexplained_frobenius_norm",
        }:
            raise ValueError("model-class fit fields do not match")
        name = values["name"]
        best_fit = values["best_fit"]
        residual = values["unexplained_residual"]
        norm = values["unexplained_frobenius_norm"]
        if type(name) is not str:
            raise TypeError("fit name must decode to a built-in string")
        if not isinstance(best_fit, MatrixQuantity) or not isinstance(
            residual, MatrixQuantity
        ):
            raise TypeError("fit matrices must decode to MatrixQuantity")
        if not isinstance(norm, ScalarQuantity):
            raise TypeError("fit norm must decode to ScalarQuantity")
        return cls(
            name=name,
            best_fit=best_fit,
            unexplained_residual=residual,
            unexplained_frobenius_norm=norm,
        )


@dataclass(frozen=True, slots=True, eq=False)
class RetainedModelClassFitRequest:
    """Bind one finite retained-basis matrix for declared model-class fitting."""

    target: MatrixQuantity

    def __post_init__(self) -> None:
        """Admit one square real matrix quantity."""
        if not isinstance(self.target, MatrixQuantity):
            raise TypeError("target must be MatrixQuantity")
        dimension = self.target.magnitude.shape[0]
        if self.target.magnitude.shape != (dimension, dimension):
            raise ValueError("target must be square")


class RetainedModelClassFitter:
    """Fit four model classes for one constructor-bound retained matrix."""

    __slots__ = ("_request",)

    def __init__(self, request: RetainedModelClassFitRequest) -> None:
        if type(request) is not RetainedModelClassFitRequest:
            raise TypeError("request must be RetainedModelClassFitRequest")
        self._request = request

    @property
    def request(self) -> RetainedModelClassFitRequest:
        """Return the complete immutable retained-model fitting request."""
        return self._request

    def execute(self) -> tuple[RetainedModelClassFitResult, ...]:
        """Project a retained matrix onto the declared nested model classes.

        Returns
        -------
        tuple[RetainedModelClassFitResult, ...]
            Fits ordered as scalar, diagonal, tridiagonal, and unrestricted real
            symmetric. Each result retains the projected matrix, unexplained residual,
            and canonical Frobenius norm.

        Notes
        -----
        The diagonal and tridiagonal classes depend on the supplied retained basis.
        The operation does not assign physical meaning to a fitted component.
        """
        target = self.request.target
        matrix = target.magnitude
        dimension = matrix.shape[0]
        rows, columns = np.indices(matrix.shape)
        candidates = (
            (
                "scalar",
                np.eye(dimension) * float(np.trace(matrix) / dimension),
            ),
            ("diagonal", np.diag(np.diag(matrix))),
            (
                "tridiagonal",
                np.where(np.abs(rows - columns) <= 1, matrix, 0.0),
            ),
            ("real_symmetric", matrix.copy()),
        )
        return tuple(
            RetainedModelClassFitResult(
                name=name,
                best_fit=MatrixQuantity(candidate, target.unit),
                unexplained_residual=MatrixQuantity(matrix - candidate, target.unit),
                unexplained_frobenius_norm=ScalarQuantity(
                    float(np.linalg.norm(matrix - candidate, ord="fro")), target.unit
                ),
            )
            for name, candidate in candidates
        )
