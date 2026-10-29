"""Weighted least-squares hopping fits and explicit route comparison."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from projectkoios.optimization.least_squares.factory import (
    LinearLeastSquaresMethod,
    LinearLeastSquaresSolverFactory,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ModelSystemUnitConverter,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.solidstate import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    ReciprocalOperatorSamples1D,
)


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingLeastSquaresFitResult1D:
    """Retain one weighted reciprocal-to-hopping least-squares fit."""

    source: ReciprocalOperatorSamples1D
    representatives: tuple[int, ...]
    weights: VectorQuantity
    fitted_model: BlockHoppingModel1D
    reconstructed_training: ReciprocalOperatorSamples1D
    design_rank: int
    design_condition_number: float | None
    is_identified: bool
    training_l2_frobenius_residual: float
    training_maximum_frobenius_residual: float

    def __post_init__(self) -> None:
        """Validate model, rank, disposition, and represented residuals."""
        if type(self.source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if not isinstance(self.representatives, tuple) or not self.representatives:
            raise TypeError("representatives must be a nonempty tuple")
        if tuple(sorted(set(self.representatives))) != self.representatives:
            raise ValueError("representatives must be unique and strictly increasing")
        if type(self.weights) is not VectorQuantity:
            raise TypeError("weights must be VectorQuantity")
        if not isinstance(self.weights.unit, Unitless):
            raise ValueError("weights must be unitless")
        if self.weights.magnitude.shape != self.source.coordinates.magnitude.shape:
            raise ValueError("one weight is required per source sample")
        if np.any(self.weights.magnitude <= 0.0):
            raise ValueError("weights must be positive")
        if type(self.fitted_model) is not BlockHoppingModel1D:
            raise TypeError("fitted_model must be BlockHoppingModel1D")
        if self.fitted_model.representatives != self.representatives:
            raise ValueError("fitted_model representatives must match the fit")
        if self.fitted_model.matrix_dimension != self.source.matrix_dimension:
            raise ValueError("fitted_model dimension must match source matrices")
        if type(self.reconstructed_training) is not ReciprocalOperatorSamples1D:
            raise TypeError(
                "reconstructed_training must be ReciprocalOperatorSamples1D"
            )
        if type(self.design_rank) is not int:
            raise TypeError("design_rank must be a built-in int")
        if self.design_rank < 0 or self.design_rank > len(self.representatives):
            raise ValueError("design_rank must lie within coefficient count")
        if self.design_condition_number is not None:
            if type(self.design_condition_number) is not float:
                raise TypeError("design_condition_number must be a built-in float")
            if (
                not np.isfinite(self.design_condition_number)
                or self.design_condition_number < 1.0
            ):
                raise ValueError(
                    "design_condition_number must be finite and at least one"
                )
        if type(self.is_identified) is not bool:
            raise TypeError("is_identified must be a built-in bool")
        if self.is_identified is not (self.design_rank == len(self.representatives)):
            raise ValueError("is_identified must match design rank")
        if self.is_identified is (self.design_condition_number is None):
            raise ValueError(
                "identified fits require a condition number and deficient fits use None"
            )
        for name, value in (
            ("training_l2_frobenius_residual", self.training_l2_frobenius_residual),
            (
                "training_maximum_frobenius_residual",
                self.training_maximum_frobenius_residual,
            ),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        residuals = np.asarray(
            [
                fitted.magnitude - source.magnitude
                for fitted, source in zip(
                    self.reconstructed_training.matrices,
                    self.source.matrices,
                    strict=True,
                )
            ],
            dtype=np.complex128,
        )
        measured_l2 = float(np.linalg.norm(residuals))
        measured_maximum = float(np.max(np.linalg.norm(residuals, axis=(1, 2))))
        if measured_l2 != self.training_l2_frobenius_residual:
            raise ValueError("training_l2_frobenius_residual must match matrices")
        if measured_maximum != self.training_maximum_frobenius_residual:
            raise ValueError("training_maximum_frobenius_residual must match matrices")


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingLeastSquaresFitRequest1D:
    """Bind one represented sample path, hopping basis, and objective weights."""

    source: ReciprocalOperatorSamples1D
    representatives: tuple[int, ...]
    weights: VectorQuantity

    def __post_init__(self) -> None:
        """Admit samples, ordered representatives, and positive unitless weights."""
        if type(self.source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if not isinstance(self.representatives, tuple) or not self.representatives:
            raise TypeError("representatives must be a nonempty tuple")
        if any(type(value) is not int for value in self.representatives):
            raise TypeError("representatives must contain built-in integers")
        if tuple(sorted(set(self.representatives))) != self.representatives:
            raise ValueError("representatives must be unique and strictly increasing")
        if type(self.weights) is not VectorQuantity:
            raise TypeError("weights must be VectorQuantity")
        if not isinstance(self.weights.unit, Unitless):
            raise ValueError("weights must be unitless")
        if self.weights.magnitude.shape != self.source.coordinates.magnitude.shape:
            raise ValueError("one weight is required per source sample")
        if np.any(self.weights.magnitude <= 0.0):
            raise ValueError("weights must be positive")


class BlockHoppingLeastSquaresFitter1D:
    """Adapt one constructor-bound hopping fit to the Optimization owner.

    KSD constructs the unitless Fourier design, converts represented matrices to one
    numeric target matrix, maps owner coefficients back to unit-bearing hopping blocks,
    and independently reconstructs KSD-domain residual diagnostics. Positive input
    weights are objective multipliers and are passed to the owner without pre-scaling.
    """

    __slots__ = ("_request",)

    def __init__(self, request: BlockHoppingLeastSquaresFitRequest1D) -> None:
        if type(request) is not BlockHoppingLeastSquaresFitRequest1D:
            raise TypeError("request must be BlockHoppingLeastSquaresFitRequest1D")
        self._request = request

    @property
    def request(self) -> BlockHoppingLeastSquaresFitRequest1D:
        """Return the complete immutable block-hopping fit request."""
        return self._request

    def execute(self) -> BlockHoppingLeastSquaresFitResult1D:
        """Solve the weighted complex least-squares problem entrywise."""
        source = self.request.source
        representatives = self.request.representatives
        weights = self.request.weights
        normalized_coordinates = (
            source.coordinates.magnitude / source.reciprocal_period.magnitude
        )
        design = np.exp(
            2j
            * np.pi
            * np.outer(
                normalized_coordinates,
                np.asarray(representatives, dtype=np.float64),
            )
        )
        source_values = np.asarray(
            [matrix.magnitude for matrix in source.matrices], dtype=np.complex128
        )
        flattened_targets = source_values.reshape(len(source.matrices), -1)
        solver = LinearLeastSquaresSolverFactory.create(
            LinearLeastSquaresMethod.NUMPY_DENSE
        )
        owner_result = solver.solve(
            tuple(tuple(complex(value) for value in row) for row in design),
            tuple(tuple(complex(value) for value in row) for row in flattened_targets),
            weights=tuple(float(value) for value in weights.magnitude),
            rank_tolerance=None,
        )
        fitted_flat = np.asarray(owner_result.coefficients, dtype=np.complex128)
        blocks = fitted_flat.reshape(
            len(representatives), source.matrix_dimension, source.matrix_dimension
        )
        model = BlockHoppingModel1D(
            source.reciprocal_period,
            representatives,
            tuple(
                ComplexMatrixQuantity(block, source.matrices[0].unit)
                for block in blocks
            ),
        )
        reconstructed = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(model, source.coordinates)
        ).execute()
        residuals = np.asarray(
            [
                fitted.magnitude - target.magnitude
                for fitted, target in zip(
                    reconstructed.matrices, source.matrices, strict=True
                )
            ],
            dtype=np.complex128,
        )
        owner_fitted = np.asarray(
            owner_result.fitted_values, dtype=np.complex128
        ).reshape(source_values.shape)
        for reconstructed_matrix, expected_matrix in zip(
            reconstructed.matrices, owner_fitted, strict=True
        ):
            for actual, expected in zip(
                reconstructed_matrix.magnitude.flat,
                expected_matrix.flat,
                strict=True,
            ):
                if not solver.tolerance.accepts(complex(actual), complex(expected)):
                    raise ValueError(
                        "hopping reconstruction does not match owner fitted values"
                    )
        return BlockHoppingLeastSquaresFitResult1D(
            source,
            representatives,
            weights,
            model,
            reconstructed,
            owner_result.rank,
            owner_result.full_rank_condition_number,
            owner_result.rank == len(representatives),
            float(np.linalg.norm(residuals)),
            float(np.max(np.linalg.norm(residuals, axis=(1, 2)))),
        )


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingModelComparisonResult1D:
    """Retain coefficient and sampled-operator defects between two hopping routes."""

    reference: BlockHoppingModel1D
    candidate: BlockHoppingModel1D
    comparison_coordinates: VectorQuantity
    coefficient_l2_frobenius_defect: ScalarQuantity
    sampled_l2_frobenius_defect: ScalarQuantity
    sampled_maximum_frobenius_defect: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate route compatibility and nonnegative defect quantities."""
        if type(self.reference) is not BlockHoppingModel1D:
            raise TypeError("reference must be BlockHoppingModel1D")
        if type(self.candidate) is not BlockHoppingModel1D:
            raise TypeError("candidate must be BlockHoppingModel1D")
        if self.reference.representatives != self.candidate.representatives:
            raise ValueError("route representatives must agree")
        if self.reference.matrix_dimension != self.candidate.matrix_dimension:
            raise ValueError("route matrix dimensions must agree")
        if type(self.comparison_coordinates) is not VectorQuantity:
            raise TypeError("comparison_coordinates must be VectorQuantity")
        for name, value in (
            (
                "coefficient_l2_frobenius_defect",
                self.coefficient_l2_frobenius_defect,
            ),
            ("sampled_l2_frobenius_defect", self.sampled_l2_frobenius_defect),
            (
                "sampled_maximum_frobenius_defect",
                self.sampled_maximum_frobenius_defect,
            ),
        ):
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if value.unit != self.reference.hopping_blocks[0].unit:
                raise ValueError(f"{name} must use the reference block unit")
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True, eq=False)
class ScalarHermitianHoppingLeastSquaresFitRequest1D:
    """Bind one real scalar sample path, symmetric range, and fit weights."""

    source: ReciprocalOperatorSamples1D
    maximum_range: int
    weights: VectorQuantity

    def __post_init__(self) -> None:
        """Admit scalar Hermitian samples, range, and positive unitless weights."""
        if type(self.source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if self.source.matrix_dimension != 1:
            raise ValueError("source must contain rank-one scalar operators")
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        if type(self.weights) is not VectorQuantity:
            raise TypeError("weights must be VectorQuantity")
        if not isinstance(self.weights.unit, Unitless):
            raise ValueError("weights must be unitless")
        if self.weights.magnitude.shape != self.source.coordinates.magnitude.shape:
            raise ValueError("one weight is required per source sample")
        if np.any(self.weights.magnitude <= 0.0):
            raise ValueError("weights must be positive")
        source_values = np.asarray(
            [matrix.magnitude[0, 0] for matrix in self.source.matrices],
            dtype=np.complex128,
        )
        if np.any(source_values.imag != 0.0):
            raise ValueError("scalar Hermitian source values must be exactly real")


class ScalarHermitianHoppingLeastSquaresFitter1D:
    """Fit one constructor-bound scalar model in a Hermitian hopping basis."""

    __slots__ = ("_request",)

    def __init__(self, request: ScalarHermitianHoppingLeastSquaresFitRequest1D) -> None:
        if type(request) is not ScalarHermitianHoppingLeastSquaresFitRequest1D:
            raise TypeError(
                "request must be ScalarHermitianHoppingLeastSquaresFitRequest1D"
            )
        self._request = request

    @property
    def request(self) -> ScalarHermitianHoppingLeastSquaresFitRequest1D:
        """Return the complete immutable scalar Hermitian fit request."""
        return self._request

    def execute(self) -> BlockHoppingLeastSquaresFitResult1D:
        """Fit one real onsite value and conjugate positive-range pairs."""
        source = self.request.source
        maximum_range = self.request.maximum_range
        weights = self.request.weights
        source_values = np.asarray(
            [matrix.magnitude[0, 0] for matrix in source.matrices],
            dtype=np.complex128,
        )
        normalized_coordinates = (
            source.coordinates.magnitude / source.reciprocal_period.magnitude
        )
        columns = [np.ones(source_values.size, dtype=np.float64)]
        for representative in range(1, maximum_range + 1):
            phases = 2.0 * np.pi * representative * normalized_coordinates
            columns.extend((2.0 * np.cos(phases), -2.0 * np.sin(phases)))
        design = np.column_stack(columns)
        solver = LinearLeastSquaresSolverFactory.create(
            LinearLeastSquaresMethod.NUMPY_DENSE
        )
        owner_result = solver.solve(
            tuple(tuple(float(value) for value in row) for row in design),
            tuple((float(value.real),) for value in source_values),
            weights=tuple(float(value) for value in weights.magnitude),
            rank_tolerance=None,
        )
        parameters = np.asarray(
            owner_result.coefficients,
            dtype=np.complex128,
        ).reshape(-1)
        if np.any(parameters.imag != 0.0):
            raise ValueError("real Hermitian fit returned complex parameters")
        hopping_by_representative: dict[int, complex] = {
            0: complex(float(parameters[0].real), 0.0)
        }
        for representative in range(1, maximum_range + 1):
            parameter_index = 2 * representative - 1
            positive = complex(
                float(parameters[parameter_index].real),
                float(parameters[parameter_index + 1].real),
            )
            hopping_by_representative[representative] = positive
            hopping_by_representative[-representative] = positive.conjugate()
        representatives = tuple(range(-maximum_range, maximum_range + 1))
        model = BlockHoppingModel1D(
            source.reciprocal_period,
            representatives,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray(
                        [[hopping_by_representative[representative]]],
                        dtype=np.complex128,
                    ),
                    source.matrices[0].unit,
                )
                for representative in representatives
            ),
        )
        reconstructed = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(model, source.coordinates)
        ).execute()
        residuals = np.asarray(
            [
                fitted.magnitude - target.magnitude
                for fitted, target in zip(
                    reconstructed.matrices,
                    source.matrices,
                    strict=True,
                )
            ],
            dtype=np.complex128,
        )
        return BlockHoppingLeastSquaresFitResult1D(
            source,
            representatives,
            weights,
            model,
            reconstructed,
            owner_result.rank,
            owner_result.full_rank_condition_number,
            owner_result.rank == len(representatives),
            float(np.linalg.norm(residuals)),
            float(np.max(np.linalg.norm(residuals, axis=(1, 2)))),
        )


@dataclass(frozen=True, slots=True, eq=False)
class BlockHoppingModelComparisonRequest1D:
    """Bind two compatible hopping routes and their comparison coordinates."""

    reference: BlockHoppingModel1D
    candidate: BlockHoppingModel1D
    comparison_coordinates: VectorQuantity

    def __post_init__(self) -> None:
        """Admit route basis, period, unit, and coordinate compatibility."""
        if type(self.reference) is not BlockHoppingModel1D:
            raise TypeError("reference must be BlockHoppingModel1D")
        if type(self.candidate) is not BlockHoppingModel1D:
            raise TypeError("candidate must be BlockHoppingModel1D")
        if type(self.comparison_coordinates) is not VectorQuantity:
            raise TypeError("comparison_coordinates must be VectorQuantity")
        if self.comparison_coordinates.magnitude.size == 0:
            raise ValueError("comparison_coordinates must be nonempty")
        if self.reference.representatives != self.candidate.representatives:
            raise ValueError("route representatives must agree")
        if self.reference.matrix_dimension != self.candidate.matrix_dimension:
            raise ValueError("route matrix dimensions must agree")
        candidate_period = ModelSystemUnitConverter.convert_scalar(
            self.candidate.reciprocal_period, self.reference.reciprocal_period.unit
        )
        if candidate_period.magnitude != self.reference.reciprocal_period.magnitude:
            raise ValueError("route reciprocal periods must agree")
        if not ModelSystemUnitConverter.compatible(
            self.reference.hopping_blocks[0].unit,
            self.candidate.hopping_blocks[0].unit,
        ):
            raise ValueError("route block units must be compatible")


class BlockHoppingModelComparator1D:
    """Compare one constructor-bound pair of compatible hopping routes."""

    __slots__ = ("_request",)

    def __init__(self, request: BlockHoppingModelComparisonRequest1D) -> None:
        if type(request) is not BlockHoppingModelComparisonRequest1D:
            raise TypeError("request must be BlockHoppingModelComparisonRequest1D")
        self._request = request

    @property
    def request(self) -> BlockHoppingModelComparisonRequest1D:
        """Return the complete immutable hopping-route comparison request."""
        return self._request

    def execute(self) -> BlockHoppingModelComparisonResult1D:
        """Measure coefficient and interpolated operator Frobenius defects."""
        reference = self.request.reference
        candidate = self.request.candidate
        comparison_coordinates = self.request.comparison_coordinates
        reference_unit = reference.hopping_blocks[0].unit
        factor = ModelSystemUnitConverter.conversion_factor(
            candidate.hopping_blocks[0].unit, reference_unit
        )
        coefficient_defect = float(
            np.sqrt(
                sum(
                    np.linalg.norm(
                        candidate_block.magnitude * factor - reference_block.magnitude
                    )
                    ** 2
                    for reference_block, candidate_block in zip(
                        reference.hopping_blocks,
                        candidate.hopping_blocks,
                        strict=True,
                    )
                )
            )
        )
        reference_samples = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(reference, comparison_coordinates)
        ).execute()
        candidate_samples = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(candidate, comparison_coordinates)
        ).execute()
        sampled_defects = np.asarray(
            [
                candidate_matrix.magnitude * factor - reference_matrix.magnitude
                for reference_matrix, candidate_matrix in zip(
                    reference_samples.matrices,
                    candidate_samples.matrices,
                    strict=True,
                )
            ],
            dtype=np.complex128,
        )
        return BlockHoppingModelComparisonResult1D(
            reference,
            candidate,
            comparison_coordinates,
            ScalarQuantity(coefficient_defect, reference_unit),
            ScalarQuantity(float(np.linalg.norm(sampled_defects)), reference_unit),
            ScalarQuantity(
                float(np.max(np.linalg.norm(sampled_defects, axis=(1, 2)))),
                reference_unit,
            ),
        )
