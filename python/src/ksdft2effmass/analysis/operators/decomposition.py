"""Reusable retained-space decomposition analysis."""

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

from .model_fitting import RetainedModelClassFitResult, RetainedModelClassFitter


@dataclass(frozen=True, slots=True, eq=False)
class KineticPotentialDecompositionResult(BaseTypedRecord):
    """Retain two exact decompositions and declared model-class fits.

    Parameters
    ----------
    physical_kinetic
        Declared physical kinetic matrix in the retained basis.
    physical_potential
        Declared physical potential matrix in the same basis.
    alternative_kinetic
        Illustrative shifted kinetic matrix.
    alternative_potential
        Illustrative complementary shift.
    physical_reconstruction_error
        Canonical norm of ``H - (T_physical + V_physical)``.
    alternative_reconstruction_error
        Canonical norm of ``H - (T_alternative + V_alternative)``.
    model_class_fits
        Ordered scalar, diagonal, tridiagonal, and unrestricted real-symmetric fits.

    Raises
    ------
    TypeError
        A matrix, scalar, or fit value has the wrong domain type.
    ValueError
        Matrix shapes, units, fit order, or fit coordinates disagree.

    Notes
    -----
    Exact reconstruction does not establish a unique physical decomposition. The
    alternative split remains explicitly illustrative.
    """

    physical_kinetic: MatrixQuantity
    physical_potential: MatrixQuantity
    alternative_kinetic: MatrixQuantity
    alternative_potential: MatrixQuantity
    physical_reconstruction_error: ScalarQuantity
    alternative_reconstruction_error: ScalarQuantity
    model_class_fits: tuple[RetainedModelClassFitResult, ...]

    def __post_init__(self) -> None:
        matrices = (
            self.physical_kinetic,
            self.physical_potential,
            self.alternative_kinetic,
            self.alternative_potential,
        )
        if any(not isinstance(value, MatrixQuantity) for value in matrices):
            raise TypeError("decomposition matrices must be MatrixQuantity values")
        if len({value.unit for value in matrices}) != 1:
            raise ValueError("decomposition matrix units must agree")
        if len({value.magnitude.shape for value in matrices}) != 1:
            raise ValueError("decomposition matrix shapes must agree")
        if not isinstance(
            self.physical_reconstruction_error, ScalarQuantity
        ) or not isinstance(self.alternative_reconstruction_error, ScalarQuantity):
            raise TypeError("reconstruction errors must be ScalarQuantity values")
        if (
            self.physical_reconstruction_error.unit != matrices[0].unit
            or self.alternative_reconstruction_error.unit != matrices[0].unit
        ):
            raise ValueError("reconstruction-error and matrix units must agree")
        if not isinstance(self.model_class_fits, tuple) or any(
            not isinstance(value, RetainedModelClassFitResult)
            for value in self.model_class_fits
        ):
            raise TypeError("model_class_fits must contain typed fit results")
        expected_names = ("scalar", "diagonal", "tridiagonal", "real_symmetric")
        if tuple(value.name for value in self.model_class_fits) != expected_names:
            raise ValueError("model-class fits must use the declared ordering")
        if any(
            value.best_fit.unit != matrices[0].unit
            or value.best_fit.magnitude.shape != matrices[0].magnitude.shape
            for value in self.model_class_fits
        ):
            raise ValueError("model-class fits must share decomposition shape and unit")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "physical_kinetic": self.physical_kinetic,
            "physical_potential": self.physical_potential,
            "alternative_kinetic": self.alternative_kinetic,
            "alternative_potential": self.alternative_potential,
            "physical_reconstruction_error": self.physical_reconstruction_error,
            "alternative_reconstruction_error": self.alternative_reconstruction_error,
            "model_class_fits": self.model_class_fits,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "physical_kinetic",
            "physical_potential",
            "alternative_kinetic",
            "alternative_potential",
            "physical_reconstruction_error",
            "alternative_reconstruction_error",
            "model_class_fits",
        }
        if set(values) != required:
            raise ValueError("kinetic-potential decomposition fields do not match")
        physical_kinetic = values["physical_kinetic"]
        physical_potential = values["physical_potential"]
        alternative_kinetic = values["alternative_kinetic"]
        alternative_potential = values["alternative_potential"]
        if (
            not isinstance(physical_kinetic, MatrixQuantity)
            or not isinstance(physical_potential, MatrixQuantity)
            or not isinstance(alternative_kinetic, MatrixQuantity)
            or not isinstance(alternative_potential, MatrixQuantity)
        ):
            raise TypeError("decomposition matrices must decode to MatrixQuantity")
        physical_error = values["physical_reconstruction_error"]
        alternative_error = values["alternative_reconstruction_error"]
        if not isinstance(physical_error, ScalarQuantity) or not isinstance(
            alternative_error, ScalarQuantity
        ):
            raise TypeError("reconstruction errors must decode to ScalarQuantity")
        fits_value = values["model_class_fits"]
        if not isinstance(fits_value, tuple):
            raise TypeError("model_class_fits must decode to a tuple")
        fits: list[RetainedModelClassFitResult] = []
        for value in fits_value:
            if isinstance(value, RetainedModelClassFitResult):
                fits.append(value)
            elif isinstance(value, Mapping):
                fits.append(RetainedModelClassFitResult.from_dict(value))
            else:
                raise TypeError("model-class fits must be typed or mappings")
        return cls(
            physical_kinetic=physical_kinetic,
            physical_potential=physical_potential,
            alternative_kinetic=alternative_kinetic,
            alternative_potential=alternative_potential,
            physical_reconstruction_error=physical_error,
            alternative_reconstruction_error=alternative_error,
            model_class_fits=tuple(fits),
        )


class KineticPotentialDecompositionAnalyzer:
    """Compare exact decomposition freedom with restricted model-class fits."""

    __slots__ = ("model_fitter",)

    def __init__(self, model_fitter: RetainedModelClassFitter | None = None) -> None:
        """Construct the decomposition action.

        Parameters
        ----------
        model_fitter
            Explicit retained-space fitter. ``None`` constructs the canonical four-
            class fitter.

        Raises
        ------
        TypeError
            ``model_fitter`` is neither ``None`` nor ``RetainedModelClassFitter``.
        """
        if model_fitter is not None and not isinstance(
            model_fitter, RetainedModelClassFitter
        ):
            raise TypeError("model_fitter must be RetainedModelClassFitter or None")
        self.model_fitter = model_fitter or RetainedModelClassFitter()

    def execute(
        self, reduced_hamiltonian: MatrixQuantity, shift: MatrixQuantity
    ) -> KineticPotentialDecompositionResult:
        """Evaluate the declared physical and shifted decompositions.

        Parameters
        ----------
        reduced_hamiltonian
            Finite real matrix quantity acting in the retained coordinate space.
            For PIAB1D this matrix is the declared physical kinetic operator.
        shift
            Shape- and unit-compatible real-symmetric illustrative reassignment.

        Returns
        -------
        KineticPotentialDecompositionResult
            Exact component matrices, reconstruction errors, and least-Frobenius fits
            of the shift to the declared model classes.

        Raises
        ------
        TypeError
            Either input is not a ``MatrixQuantity``.
        ValueError
            Shapes or units differ, or a retained model-class invariant fails.

        Notes
        -----
        The shifted pair is algebraically exact and carries no physical assignment.
        The operation does not infer a potential from the Hamiltonian.
        """
        if not isinstance(reduced_hamiltonian, MatrixQuantity):
            raise TypeError("reduced_hamiltonian must be MatrixQuantity")
        if not isinstance(shift, MatrixQuantity):
            raise TypeError("shift must be MatrixQuantity")
        hamiltonian = reduced_hamiltonian.magnitude
        shift_matrix = shift.magnitude
        if hamiltonian.shape != shift_matrix.shape:
            raise ValueError("reduced_hamiltonian and shift dimensions must match")
        dimension = hamiltonian.shape[0]
        if hamiltonian.shape != (dimension, dimension):
            raise ValueError("reduced_hamiltonian and shift must be square")
        if reduced_hamiltonian.unit != shift.unit:
            raise ValueError("reduced_hamiltonian and shift units must match")
        physical_kinetic = hamiltonian.copy()
        physical_potential = np.zeros_like(hamiltonian)
        alternative_kinetic = hamiltonian - shift_matrix
        alternative_potential = shift_matrix.copy()
        physical_residual = hamiltonian - physical_kinetic - physical_potential
        alternative_residual = hamiltonian - alternative_kinetic - alternative_potential
        unit = reduced_hamiltonian.unit
        return KineticPotentialDecompositionResult(
            physical_kinetic=MatrixQuantity(physical_kinetic, unit),
            physical_potential=MatrixQuantity(physical_potential, unit),
            alternative_kinetic=MatrixQuantity(alternative_kinetic, unit),
            alternative_potential=MatrixQuantity(alternative_potential, unit),
            physical_reconstruction_error=ScalarQuantity(
                float(np.linalg.norm(physical_residual, ord="fro")), unit
            ),
            alternative_reconstruction_error=ScalarQuantity(
                float(np.linalg.norm(alternative_residual, ord="fro")), unit
            ),
            model_class_fits=self.model_fitter.execute(shift),
        )
