"""Weighted least-squares hopping fits and explicit route comparison."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
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
        if self.is_identified is not (
            self.design_rank == len(self.representatives)
        ):
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


class BlockHoppingLeastSquaresFitter1D:
    """Fit matrix-valued hopping blocks with explicit positive sample weights."""

    __slots__ = ()

    def execute(
        self,
        source: ReciprocalOperatorSamples1D,
        representatives: tuple[int, ...],
        weights: VectorQuantity,
    ) -> BlockHoppingLeastSquaresFitResult1D:
        """Solve the weighted complex least-squares problem entrywise."""
        if type(source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if not isinstance(representatives, tuple) or not representatives:
            raise TypeError("representatives must be a nonempty tuple")
        if any(type(value) is not int for value in representatives):
            raise TypeError("representatives must contain built-in integers")
        if tuple(sorted(set(representatives))) != representatives:
            raise ValueError("representatives must be unique and strictly increasing")
        if type(weights) is not VectorQuantity:
            raise TypeError("weights must be VectorQuantity")
        if not isinstance(weights.unit, Unitless):
            raise ValueError("weights must be unitless")
        if weights.magnitude.shape != source.coordinates.magnitude.shape:
            raise ValueError("one weight is required per source sample")
        if np.any(weights.magnitude <= 0.0):
            raise ValueError("weights must be positive")
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
        square_root_weights = np.sqrt(weights.magnitude)
        weighted_design = square_root_weights[:, None] * design
        source_values = np.asarray(
            [matrix.magnitude for matrix in source.matrices], dtype=np.complex128
        )
        weighted_targets = square_root_weights[:, None] * source_values.reshape(
            len(source.matrices), -1
        )
        fitted_flat, _, rank, singular_values = np.linalg.lstsq(
            weighted_design, weighted_targets, rcond=None
        )
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
        reconstructed = BlockHoppingInterpolator1D().execute(
            model, source.coordinates
        )
        residuals = np.asarray(
            [
                fitted.magnitude - target.magnitude
                for fitted, target in zip(
                    reconstructed.matrices, source.matrices, strict=True
                )
            ],
            dtype=np.complex128,
        )
        condition = (
            None
            if int(rank) < len(representatives)
            else float(singular_values[0] / singular_values[-1])
        )
        return BlockHoppingLeastSquaresFitResult1D(
            source,
            representatives,
            weights,
            model,
            reconstructed,
            int(rank),
            condition,
            int(rank) == len(representatives),
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


class BlockHoppingModelComparator1D:
    """Compare compatible hopping routes in coefficient and reciprocal spaces."""

    __slots__ = ()

    def execute(
        self,
        reference: BlockHoppingModel1D,
        candidate: BlockHoppingModel1D,
        comparison_coordinates: VectorQuantity,
    ) -> BlockHoppingModelComparisonResult1D:
        """Measure coefficient and interpolated operator Frobenius defects."""
        if type(reference) is not BlockHoppingModel1D:
            raise TypeError("reference must be BlockHoppingModel1D")
        if type(candidate) is not BlockHoppingModel1D:
            raise TypeError("candidate must be BlockHoppingModel1D")
        if type(comparison_coordinates) is not VectorQuantity:
            raise TypeError("comparison_coordinates must be VectorQuantity")
        if comparison_coordinates.magnitude.size == 0:
            raise ValueError("comparison_coordinates must be nonempty")
        if reference.representatives != candidate.representatives:
            raise ValueError("route representatives must agree")
        if reference.matrix_dimension != candidate.matrix_dimension:
            raise ValueError("route matrix dimensions must agree")
        reference_period = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            candidate.reciprocal_period, reference.reciprocal_period.unit
        )
        if reference_period.magnitude != reference.reciprocal_period.magnitude:
            raise ValueError("route reciprocal periods must agree")
        reference_unit = reference.hopping_blocks[0].unit
        candidate_unit = candidate.hopping_blocks[0].unit
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            reference_unit, candidate_unit
        ):
            raise ValueError("route block units must be compatible")
        factor = MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
            candidate_unit, reference_unit
        )
        coefficient_defect = float(
            np.sqrt(
                sum(
                    np.linalg.norm(
                        candidate_block.magnitude * factor
                        - reference_block.magnitude
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
        reference_samples = BlockHoppingInterpolator1D().execute(
            reference, comparison_coordinates
        )
        candidate_samples = BlockHoppingInterpolator1D().execute(
            candidate, comparison_coordinates
        )
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
