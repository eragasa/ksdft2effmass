"""Typed results for the one-dimensional multiband alignment calculation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityResult1D,
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorResult1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
)
from ksdft2effmass.solid_state import (
    BandFrameAlignmentResult1D,
    BlockHoppingTruncationResult1D,
    PolarBandFrameTransportResult1D,
    ReciprocalOperatorFourierTransformResult1D,
)

from .definition import Periodic1DMultibandAlignmentCalculationDefinition


@dataclass(frozen=True, slots=True)
class Periodic1DMultibandAlignmentDiagnostics:
    """Retain invariant, pointwise, and globally constrained frame diagnostics."""

    transport: PolarBandFrameTransportResult1D
    pointwise_alignment: BandFrameAlignmentResult1D
    constrained_rotation: ComplexMatrixQuantity
    external_gap_minimum: ScalarQuantity
    attack_frame_maximum_frobenius_defect: float
    pointwise_rotation_recovery_maximum_frobenius_defect: float
    constrained_frame_maximum_frobenius_defect: float
    attacked_operator_maximum_frobenius_defect: ScalarQuantity
    pointwise_operator_maximum_frobenius_defect: ScalarQuantity
    constrained_operator_maximum_frobenius_defect: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact diagnostic types, units, and nonnegative values."""
        if type(self.transport) is not PolarBandFrameTransportResult1D:
            raise TypeError("transport must be PolarBandFrameTransportResult1D")
        if type(self.pointwise_alignment) is not BandFrameAlignmentResult1D:
            raise TypeError("pointwise_alignment must be BandFrameAlignmentResult1D")
        if self.pointwise_alignment.reference is not self.transport.transported:
            raise ValueError("pointwise reference must be the transported frame path")
        if type(self.constrained_rotation) is not ComplexMatrixQuantity:
            raise TypeError("constrained_rotation must be ComplexMatrixQuantity")
        if not isinstance(self.constrained_rotation.unit, Unitless):
            raise ValueError("constrained_rotation must be unitless")
        rank = self.transport.transported.rank
        if self.constrained_rotation.magnitude.shape != (rank, rank):
            raise ValueError("constrained_rotation shape must match retained rank")
        identity = np.eye(rank, dtype=np.complex128)
        if not np.allclose(
            self.constrained_rotation.magnitude.conj().T
            @ self.constrained_rotation.magnitude,
            identity,
            rtol=0.0,
            atol=self.transport.transported.orthonormality_absolute_tolerance,
        ):
            raise ValueError("constrained_rotation must be unitary")
        if type(self.external_gap_minimum) is not ScalarQuantity:
            raise TypeError("external_gap_minimum must be ScalarQuantity")
        if self.external_gap_minimum.magnitude < 0.0:
            raise ValueError("external_gap_minimum must be nonnegative")
        for name, numeric_value in (
            (
                "attack_frame_maximum_frobenius_defect",
                self.attack_frame_maximum_frobenius_defect,
            ),
            (
                "pointwise_rotation_recovery_maximum_frobenius_defect",
                self.pointwise_rotation_recovery_maximum_frobenius_defect,
            ),
            (
                "constrained_frame_maximum_frobenius_defect",
                self.constrained_frame_maximum_frobenius_defect,
            ),
        ):
            if type(numeric_value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(numeric_value) or numeric_value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")
        operator_unit = self.external_gap_minimum.unit
        for name, quantity in (
            (
                "attacked_operator_maximum_frobenius_defect",
                self.attacked_operator_maximum_frobenius_defect,
            ),
            (
                "pointwise_operator_maximum_frobenius_defect",
                self.pointwise_operator_maximum_frobenius_defect,
            ),
            (
                "constrained_operator_maximum_frobenius_defect",
                self.constrained_operator_maximum_frobenius_defect,
            ),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{name} must be ScalarQuantity")
            if quantity.unit != operator_unit:
                raise ValueError(f"{name} must use the parent energy unit")
            if quantity.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")


@dataclass(frozen=True, slots=True)
class Periodic1DMultibandAlignmentRangeResult:
    """Retain gauge-resolved finite-range locality and spectral diagnostics."""

    reference_truncation: BlockHoppingTruncationResult1D
    attacked_truncation: BlockHoppingTruncationResult1D
    aligned_truncation: BlockHoppingTruncationResult1D
    reference_training_error: BandApproximationErrorResult1D
    attacked_training_error: BandApproximationErrorResult1D
    aligned_training_error: BandApproximationErrorResult1D
    reference_withheld_error: BandApproximationErrorResult1D
    attacked_withheld_error: BandApproximationErrorResult1D
    aligned_withheld_error: BandApproximationErrorResult1D

    def __post_init__(self) -> None:
        """Require one range and one target for all three gauge channels."""
        truncations = (
            self.reference_truncation,
            self.attacked_truncation,
            self.aligned_truncation,
        )
        if any(
            type(item) is not BlockHoppingTruncationResult1D for item in truncations
        ):
            raise TypeError("all truncations must be BlockHoppingTruncationResult1D")
        if len({item.maximum_range for item in truncations}) != 1:
            raise ValueError("all gauge channels must use one hopping range")
        errors = (
            self.reference_training_error,
            self.attacked_training_error,
            self.aligned_training_error,
            self.reference_withheld_error,
            self.attacked_withheld_error,
            self.aligned_withheld_error,
        )
        if any(type(item) is not BandApproximationErrorResult1D for item in errors):
            raise TypeError("all errors must be BandApproximationErrorResult1D")
        if not (
            self.reference_training_error.target
            is self.attacked_training_error.target
            is self.aligned_training_error.target
        ):
            raise ValueError("training errors must use one target")
        if not (
            self.reference_withheld_error.target
            is self.attacked_withheld_error.target
            is self.aligned_withheld_error.target
        ):
            raise ValueError("withheld errors must use one target")

    @property
    def maximum_range(self) -> int:
        """Return the common symmetric cell range."""
        return self.reference_truncation.maximum_range


@dataclass(frozen=True, slots=True)
class Periodic1DMultibandAlignmentCalculationResult:
    """Retain M2 alignment and locality evidence without material claims."""

    definition: Periodic1DMultibandAlignmentCalculationDefinition
    training_target: BandSpectrumSamples1D
    withheld_target: BandSpectrumSamples1D
    diagnostics: Periodic1DMultibandAlignmentDiagnostics
    reference_transform: ReciprocalOperatorFourierTransformResult1D
    attacked_transform: ReciprocalOperatorFourierTransformResult1D
    aligned_transform: ReciprocalOperatorFourierTransformResult1D
    reference_hermiticity: BlockHoppingHermiticityResult1D
    attacked_hermiticity: BlockHoppingHermiticityResult1D
    aligned_hermiticity: BlockHoppingHermiticityResult1D
    range_study: tuple[Periodic1DMultibandAlignmentRangeResult, ...]

    def __post_init__(self) -> None:
        """Validate correlations, declared inventories, and sample separation."""
        if (
            type(self.definition)
            is not Periodic1DMultibandAlignmentCalculationDefinition
        ):
            raise TypeError(
                "definition must be Periodic1DMultibandAlignmentCalculationDefinition"
            )
        for name, target in (
            ("training_target", self.training_target),
            ("withheld_target", self.withheld_target),
        ):
            if type(target) is not BandSpectrumSamples1D:
                raise TypeError(f"{name} must be BandSpectrumSamples1D")
            if target.band_count != self.definition.retained_rank:
                raise ValueError(f"{name} must contain the retained band group")
        if self.training_target.sample_count != self.definition.reciprocal_mesh_size:
            raise ValueError("training target must use the declared mesh")
        if self.withheld_target.sample_count != self.definition.withheld_mesh_size:
            raise ValueError("withheld target must use the declared mesh")
        parent_period = self.definition.parent_model.hopping_model.reciprocal_period
        expected_training = parent_period.magnitude * (
            -0.5
            + np.arange(self.definition.reciprocal_mesh_size, dtype=np.float64)
            / float(self.definition.reciprocal_mesh_size)
        )
        expected_withheld = parent_period.magnitude * np.asarray(
            self.definition.withheld_reduced_momenta
        )
        for name, target, expected in (
            ("training", self.training_target, expected_training),
            ("withheld", self.withheld_target, expected_withheld),
        ):
            coordinates = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
                target.coordinates, parent_period.unit
            )
            period = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                target.reciprocal_period, parent_period.unit
            )
            if period.magnitude != parent_period.magnitude:
                raise ValueError(f"{name} target reciprocal period does not match")
            if not np.allclose(
                coordinates.magnitude,
                expected,
                rtol=0.0,
                atol=self.definition.coordinate_absolute_tolerance,
            ):
                raise ValueError(f"{name} target coordinates do not match")
        if type(self.diagnostics) is not Periodic1DMultibandAlignmentDiagnostics:
            raise TypeError(
                "diagnostics must be Periodic1DMultibandAlignmentDiagnostics"
            )
        transforms = (
            self.reference_transform,
            self.attacked_transform,
            self.aligned_transform,
        )
        if any(
            type(item) is not ReciprocalOperatorFourierTransformResult1D
            for item in transforms
        ):
            raise TypeError(
                "all transforms must be ReciprocalOperatorFourierTransformResult1D"
            )
        if any(
            item.mesh.point_count != self.definition.reciprocal_mesh_size
            or item.source.matrix_dimension != self.definition.retained_rank
            for item in transforms
        ):
            raise ValueError("transforms must use the declared mesh and retained rank")
        for transform in transforms:
            if transform.mesh is not self.diagnostics.transport.transported.mesh:
                raise ValueError(
                    "transforms and transported frames must share the mesh"
                )
            if transform.coordinate_absolute_tolerance != (
                self.definition.coordinate_absolute_tolerance
            ):
                raise ValueError("transform coordinate tolerance does not match")
            if transform.reconstruction_absolute_tolerance != (
                self.definition.reconstruction_absolute_tolerance
            ):
                raise ValueError("transform reconstruction tolerance does not match")
            if not np.array_equal(
                transform.source.coordinates.magnitude,
                self.training_target.coordinates.magnitude,
            ):
                raise ValueError("transform source coordinates do not match training")
        energy_unit = self.definition.parent_model.hopping_model.hopping_blocks[0].unit
        external_gap_lower_bound = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.definition.external_gap_lower_bound, energy_unit
        )
        external_gap = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.diagnostics.external_gap_minimum, energy_unit
        )
        if external_gap.magnitude < external_gap_lower_bound.magnitude:
            raise ValueError("external-gap diagnostic violates the definition")
        if self.diagnostics.transport.overlap_singular_value_threshold != (
            self.definition.overlap_singular_value_threshold
        ):
            raise ValueError("transport overlap threshold does not match")
        for path in (
            self.diagnostics.transport.source,
            self.diagnostics.transport.transported,
            self.diagnostics.pointwise_alignment.candidate,
            self.diagnostics.pointwise_alignment.aligned,
        ):
            if path.orthonormality_absolute_tolerance != (
                self.definition.orthonormality_absolute_tolerance
            ):
                raise ValueError("frame orthonormality tolerance does not match")
        hermiticity = (
            (self.reference_hermiticity, self.reference_transform),
            (self.attacked_hermiticity, self.attacked_transform),
            (self.aligned_hermiticity, self.aligned_transform),
        )
        for diagnostic, transform in hermiticity:
            if type(diagnostic) is not BlockHoppingHermiticityResult1D:
                raise TypeError(
                    "all Hermiticity channels must be BlockHoppingHermiticityResult1D"
                )
            if diagnostic.model is not transform.hopping_model:
                raise ValueError("Hermiticity channels must analyze their transform")
            tolerance = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                diagnostic.absolute_tolerance, energy_unit
            )
            expected_tolerance = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
                self.definition.hermiticity_absolute_tolerance, energy_unit
            )
            if tolerance.magnitude != expected_tolerance.magnitude:
                raise ValueError("Hermiticity tolerance does not match the definition")
        if not isinstance(self.range_study, tuple) or any(
            type(item) is not Periodic1DMultibandAlignmentRangeResult
            for item in self.range_study
        ):
            raise TypeError("range_study must be a typed tuple")
        if tuple(item.maximum_range for item in self.range_study) != (
            self.definition.hopping_ranges
        ):
            raise ValueError("range results must match declared hopping ranges")
        for item in self.range_study:
            if item.reference_truncation.source is not (
                self.reference_transform.hopping_model
            ):
                raise ValueError("reference truncation source does not match")
            if item.attacked_truncation.source is not (
                self.attacked_transform.hopping_model
            ):
                raise ValueError("attacked truncation source does not match")
            if item.aligned_truncation.source is not (
                self.aligned_transform.hopping_model
            ):
                raise ValueError("aligned truncation source does not match")
            if item.reference_training_error.target is not self.training_target:
                raise ValueError("training diagnostics must use the training target")
            if item.reference_withheld_error.target is not self.withheld_target:
                raise ValueError("withheld diagnostics must use the withheld target")
        training = self.training_target.coordinates.magnitude
        withheld = self.withheld_target.coordinates.magnitude
        if training.shape == withheld.shape and np.array_equal(training, withheld):
            raise ValueError("training and withheld coordinates must remain distinct")


__all__ = [
    "Periodic1DMultibandAlignmentCalculationResult",
    "Periodic1DMultibandAlignmentDiagnostics",
    "Periodic1DMultibandAlignmentRangeResult",
]
