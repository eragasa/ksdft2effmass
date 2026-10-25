"""Typed multi-norm residual observations for PIAB1D grid sweeps."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self, cast

import numpy as np
from projectkoios.physkit.linalg.matrix.norm import MatrixNormEnum
from projectkoios.physkit.units import MatrixQuantity, Unitless

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

if TYPE_CHECKING:
    from .grid_sweep import Piab1dGridSweepDefinition


@dataclass(frozen=True, slots=True, eq=False)
class Piab1dResidualNormSweepResult(BaseTypedRecord):
    """Retain raw and same-grid-normalized residual norms.

    Parameters
    ----------
    definition
        Shared PIAB1D grid-sweep declaration.
    norms
        Exact Frobenius, spectral, and maximum-absolute-entry norm order.
    hamiltonian, consistent, boundary, unmatched, eigensolver
        Nonnegative raw norm matrices indexed by grid and norm.
    consistent_relative, boundary_relative, unmatched_relative, eigensolver_relative
        Unitless raw norms divided by the same-grid Hamiltonian norm.

    Raises
    ------
    TypeError
        A field has the wrong typed representation.
    ValueError
        Norm order, units, shapes, or nonnegativity requirements fail.

    Notes
    -----
    Same-grid normalization improves scale comparison. It does not identify operators
    acting in different finite spaces.
    """

    definition: Piab1dGridSweepDefinition
    norms: tuple[MatrixNormEnum, ...]
    hamiltonian: MatrixQuantity
    consistent: MatrixQuantity
    boundary: MatrixQuantity
    unmatched: MatrixQuantity
    eigensolver: MatrixQuantity
    consistent_relative: MatrixQuantity
    boundary_relative: MatrixQuantity
    unmatched_relative: MatrixQuantity
    eigensolver_relative: MatrixQuantity

    def __post_init__(self) -> None:
        from .grid_sweep import Piab1dGridSweepDefinition

        if not isinstance(self.definition, Piab1dGridSweepDefinition):
            raise TypeError("definition must be Piab1dGridSweepDefinition")
        expected_norms = (
            MatrixNormEnum.frobenius,
            MatrixNormEnum.spectral,
            MatrixNormEnum.maximum_absolute_entry,
        )
        if self.norms != expected_norms:
            raise ValueError("norms must use the canonical matrix-norm ordering")
        shape = (len(self.definition.interior_points), len(expected_norms))
        raw = (
            self.hamiltonian,
            self.consistent,
            self.boundary,
            self.unmatched,
            self.eigensolver,
        )
        relative = (
            self.consistent_relative,
            self.boundary_relative,
            self.unmatched_relative,
            self.eigensolver_relative,
        )
        if any(not isinstance(value, MatrixQuantity) for value in (*raw, *relative)):
            raise TypeError("residual norm observations must be MatrixQuantity values")
        if any(value.magnitude.shape != shape for value in (*raw, *relative)):
            raise ValueError("residual norm matrices must cover every grid and norm")
        if any(np.any(value.magnitude < 0.0) for value in (*raw, *relative)):
            raise ValueError("residual norms must be nonnegative")
        if any(not isinstance(value.unit, Unitless) for value in raw):
            raise ValueError(
                "raw residual norms must use the nondimensional energy unit"
            )
        if any(not isinstance(value.unit, Unitless) for value in relative):
            raise ValueError("relative residual norms must be unitless")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "definition": self.definition,
            "norms": self.norms,
            "hamiltonian": self.hamiltonian,
            "consistent": self.consistent,
            "boundary": self.boundary,
            "unmatched": self.unmatched,
            "eigensolver": self.eigensolver,
            "consistent_relative": self.consistent_relative,
            "boundary_relative": self.boundary_relative,
            "unmatched_relative": self.unmatched_relative,
            "eigensolver_relative": self.eigensolver_relative,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "definition",
            "norms",
            "hamiltonian",
            "consistent",
            "boundary",
            "unmatched",
            "eigensolver",
            "consistent_relative",
            "boundary_relative",
            "unmatched_relative",
            "eigensolver_relative",
        }
        if set(values) != required:
            raise ValueError("residual-norm result fields do not match")
        from .grid_sweep import Piab1dGridSweepDefinition

        definition_value = values["definition"]
        definition = (
            definition_value
            if isinstance(definition_value, Piab1dGridSweepDefinition)
            else Piab1dGridSweepDefinition.from_dict(definition_value)
            if isinstance(definition_value, Mapping)
            else None
        )
        if definition is None:
            raise TypeError("definition must be typed or decode to a mapping")
        norms = values["norms"]
        if not isinstance(norms, tuple) or any(
            not isinstance(value, MatrixNormEnum) for value in norms
        ):
            raise TypeError("norms must decode to a MatrixNormEnum tuple")
        names = tuple(required - {"definition", "norms"})
        if any(not isinstance(values[name], MatrixQuantity) for name in names):
            raise TypeError("residual observations must decode to MatrixQuantity")
        return cls(
            definition=definition,
            norms=norms,
            hamiltonian=cast(MatrixQuantity, values["hamiltonian"]),
            consistent=cast(MatrixQuantity, values["consistent"]),
            boundary=cast(MatrixQuantity, values["boundary"]),
            unmatched=cast(MatrixQuantity, values["unmatched"]),
            eigensolver=cast(MatrixQuantity, values["eigensolver"]),
            consistent_relative=cast(MatrixQuantity, values["consistent_relative"]),
            boundary_relative=cast(MatrixQuantity, values["boundary_relative"]),
            unmatched_relative=cast(MatrixQuantity, values["unmatched_relative"]),
            eigensolver_relative=cast(MatrixQuantity, values["eigensolver_relative"]),
        )
