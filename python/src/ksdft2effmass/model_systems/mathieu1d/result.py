"""Typed result sections for direct Mathieu1D calculations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, cast

import numpy as np
from projectkoios.physkit.units import (
    ComplexVectorQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .configuration import Mathieu1dConfiguration


def _require_unitless(
    value: ScalarQuantity | VectorQuantity | ComplexVectorQuantity | MatrixQuantity,
    name: str,
) -> None:
    if not isinstance(value.unit, Unitless):
        raise ValueError(f"{name} must use Unitless")


def _decoded[
    T: (ScalarQuantity, VectorQuantity, ComplexVectorQuantity, MatrixQuantity)
](values: Mapping[str, SerializableValue], name: str, required: type[T]) -> T:
    value = values[name]
    if not isinstance(value, required):
        raise TypeError(f"{name} must decode to {required.__name__}")
    return value


def _decoded_int_tuple(
    values: Mapping[str, SerializableValue], name: str
) -> tuple[int, ...]:
    value = values[name]
    if not (isinstance(value, tuple) and all(type(item) is int for item in value)):
        raise TypeError(f"{name} must decode to a tuple of ints")
    return value


@dataclass(frozen=True, slots=True, eq=False)
class Mathieu1dRefinementResult(BaseTypedRecord):
    """Retain finite parent-reference and representation-refinement values.

    Parameters
    ----------
    parent_reduced_momenta, parent_reference_energies
        Common sampled momentum inventory and the ordered spectral prefix from the
        larger finite plane-wave reference.
    plane_wave_cutoffs, plane_wave_maximum_errors
        Ordered cutoff inventory and maximum absolute spectral discrepancy per cutoff.
    finite_difference_points, finite_difference_maximum_errors
        Ordered periodic-grid inventory and maximum absolute spectral discrepancy per
        grid size.

    Notes
    -----
    The reference is finite. These discrepancies are not continuum error estimates.
    """

    parent_reduced_momenta: VectorQuantity
    parent_reference_energies: MatrixQuantity
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_maximum_errors: VectorQuantity
    finite_difference_points: tuple[int, ...]
    finite_difference_maximum_errors: VectorQuantity

    def __post_init__(self) -> None:
        for name in (
            "parent_reduced_momenta",
            "plane_wave_maximum_errors",
            "finite_difference_maximum_errors",
        ):
            value = getattr(self, name)
            if not isinstance(value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            _require_unitless(value, name)
        if not isinstance(self.parent_reference_energies, MatrixQuantity):
            raise TypeError("parent_reference_energies must be MatrixQuantity")
        _require_unitless(self.parent_reference_energies, "parent_reference_energies")
        for name in ("plane_wave_cutoffs", "finite_difference_points"):
            value = getattr(self, name)
            if not (
                isinstance(value, tuple)
                and value
                and all(type(item) is int for item in value)
            ):
                raise TypeError(f"{name} must be a nonempty tuple of ints")
            if value != tuple(sorted(set(value))) or value[0] <= 0:
                raise ValueError(f"{name} must be strictly increasing and positive")
        # All refinement channels share the same sampled momenta and spectral prefix;
        # only the represented parent basis or grid changes.
        if self.parent_reference_energies.magnitude.shape[0] != (
            self.parent_reduced_momenta.magnitude.size
        ):
            raise ValueError("parent spectrum rows must match parent coordinates")
        if self.plane_wave_maximum_errors.magnitude.shape != (
            len(self.plane_wave_cutoffs),
        ):
            raise ValueError("plane-wave errors must match cutoffs")
        if self.finite_difference_maximum_errors.magnitude.shape != (
            len(self.finite_difference_points),
        ):
            raise ValueError("finite-difference errors must match grid inventory")
        if np.any(self.plane_wave_maximum_errors.magnitude < 0.0) or np.any(
            self.finite_difference_maximum_errors.magnitude < 0.0
        ):
            raise ValueError("refinement errors must be nonnegative")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_reduced_momenta": self.parent_reduced_momenta,
            "parent_reference_energies": self.parent_reference_energies,
            "plane_wave_cutoffs": self.plane_wave_cutoffs,
            "plane_wave_maximum_errors": self.plane_wave_maximum_errors,
            "finite_difference_points": self.finite_difference_points,
            "finite_difference_maximum_errors": (self.finite_difference_maximum_errors),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "parent_reduced_momenta",
            "parent_reference_energies",
            "plane_wave_cutoffs",
            "plane_wave_maximum_errors",
            "finite_difference_points",
            "finite_difference_maximum_errors",
        }:
            raise ValueError("Mathieu1D refinement fields do not match")
        return cls(
            parent_reduced_momenta=_decoded(
                values, "parent_reduced_momenta", VectorQuantity
            ),
            parent_reference_energies=_decoded(
                values, "parent_reference_energies", MatrixQuantity
            ),
            plane_wave_cutoffs=_decoded_int_tuple(values, "plane_wave_cutoffs"),
            plane_wave_maximum_errors=_decoded(
                values, "plane_wave_maximum_errors", VectorQuantity
            ),
            finite_difference_points=_decoded_int_tuple(
                values, "finite_difference_points"
            ),
            finite_difference_maximum_errors=_decoded(
                values, "finite_difference_maximum_errors", VectorQuantity
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Mathieu1dBandSamplesResult(BaseTypedRecord):
    """Retain disjoint training and evaluation band samples and sampled gaps.

    Parameters
    ----------
    training_reduced_momenta, training_selected_energies, training_upper_energies
        Construction coordinates and the selected and adjacent upper bands used by the
        complete transform and direct fits.
    training_external_gap
        Minimum sampled upper-minus-selected energy on the training inventory.
    evaluation_reduced_momenta, evaluation_selected_energies, evaluation_upper_energies
        Withheld coordinates and corresponding selected and upper-band samples.
    evaluation_external_gap
        Minimum sampled upper-minus-selected energy on the evaluation inventory.

    Notes
    -----
    Sampled positive gaps are diagnostics, not continuum isolation certificates.
    """

    training_reduced_momenta: VectorQuantity
    training_selected_energies: VectorQuantity
    training_upper_energies: VectorQuantity
    training_external_gap: ScalarQuantity
    evaluation_reduced_momenta: VectorQuantity
    evaluation_selected_energies: VectorQuantity
    evaluation_upper_energies: VectorQuantity
    evaluation_external_gap: ScalarQuantity

    def __post_init__(self) -> None:
        for name in (
            "training_reduced_momenta",
            "training_selected_energies",
            "training_upper_energies",
            "evaluation_reduced_momenta",
            "evaluation_selected_energies",
            "evaluation_upper_energies",
        ):
            value = getattr(self, name)
            if not isinstance(value, VectorQuantity):
                raise TypeError(f"{name} must be VectorQuantity")
            _require_unitless(value, name)
        for name in ("training_external_gap", "evaluation_external_gap"):
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            _require_unitless(value, name)
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        # Recompute each stored gap from its authoritative band vectors so a decoded
        # scalar cannot drift from the sample inventory it summarizes.
        for role in ("training", "evaluation"):
            size = getattr(self, f"{role}_reduced_momenta").magnitude.size
            for suffix in ("selected_energies", "upper_energies"):
                if getattr(self, f"{role}_{suffix}").magnitude.shape != (size,):
                    raise ValueError(f"{role} samples must use one common inventory")
            gap = float(
                np.min(
                    getattr(self, f"{role}_upper_energies").magnitude
                    - getattr(self, f"{role}_selected_energies").magnitude
                )
            )
            if getattr(self, f"{role}_external_gap").magnitude != gap:
                raise ValueError(f"{role} external gap must match retained bands")
        training = self.training_reduced_momenta.magnitude
        evaluation = self.evaluation_reduced_momenta.magnitude
        if np.intersect1d(training, evaluation).size:
            raise ValueError("training and evaluation samples must be disjoint")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "training_reduced_momenta": self.training_reduced_momenta,
            "training_selected_energies": self.training_selected_energies,
            "training_upper_energies": self.training_upper_energies,
            "training_external_gap": self.training_external_gap,
            "evaluation_reduced_momenta": self.evaluation_reduced_momenta,
            "evaluation_selected_energies": self.evaluation_selected_energies,
            "evaluation_upper_energies": self.evaluation_upper_energies,
            "evaluation_external_gap": self.evaluation_external_gap,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = {
            "training_reduced_momenta",
            "training_selected_energies",
            "training_upper_energies",
            "training_external_gap",
            "evaluation_reduced_momenta",
            "evaluation_selected_energies",
            "evaluation_upper_energies",
            "evaluation_external_gap",
        }
        if set(values) != fields:
            raise ValueError("Mathieu1D band-sample fields do not match")
        return cls(
            training_reduced_momenta=_decoded(
                values, "training_reduced_momenta", VectorQuantity
            ),
            training_selected_energies=_decoded(
                values, "training_selected_energies", VectorQuantity
            ),
            training_upper_energies=_decoded(
                values, "training_upper_energies", VectorQuantity
            ),
            training_external_gap=_decoded(
                values, "training_external_gap", ScalarQuantity
            ),
            evaluation_reduced_momenta=_decoded(
                values, "evaluation_reduced_momenta", VectorQuantity
            ),
            evaluation_selected_energies=_decoded(
                values, "evaluation_selected_energies", VectorQuantity
            ),
            evaluation_upper_energies=_decoded(
                values, "evaluation_upper_energies", VectorQuantity
            ),
            evaluation_external_gap=_decoded(
                values, "evaluation_external_gap", ScalarQuantity
            ),
        )


@dataclass(frozen=True, slots=True, eq=False)
class Mathieu1dTransformResult(BaseTypedRecord):
    """Retain the complete finite transform and Hermiticity diagnostics.

    Parameters
    ----------
    representatives, hopping_blocks
        Complete centered real-space representative inventory and scalar complex
        Fourier coefficients.
    reconstructed_training
        Inverse-transform values on the construction mesh.
    reconstruction_maximum_error, reconstruction_absolute_tolerance
        Complete-transform discrepancy and admitted tolerance.
    reconstruction_passes
        Disposition correlated with the reconstruction values.
    paired_representatives, missing_opposite_representatives
        Partition of representatives by availability of the periodic negation partner.
    hermiticity_maximum_defect, hermiticity_absolute_tolerance
        Maximum conjugate-pair defect and admitted tolerance.
    hermiticity_passes
        Disposition correlated with structural pairing and the defect tolerance.
    """

    representatives: tuple[int, ...]
    hopping_blocks: ComplexVectorQuantity
    reconstructed_training: ComplexVectorQuantity
    reconstruction_maximum_error: ScalarQuantity
    reconstruction_absolute_tolerance: ScalarQuantity
    reconstruction_passes: bool
    paired_representatives: tuple[int, ...]
    missing_opposite_representatives: tuple[int, ...]
    hermiticity_maximum_defect: ScalarQuantity
    hermiticity_absolute_tolerance: ScalarQuantity
    hermiticity_passes: bool

    def __post_init__(self) -> None:
        for name in (
            "representatives",
            "paired_representatives",
            "missing_opposite_representatives",
        ):
            value = getattr(self, name)
            if not (
                isinstance(value, tuple) and all(type(item) is int for item in value)
            ):
                raise TypeError(f"{name} must be a tuple of ints")
            if value != tuple(sorted(set(value))):
                raise ValueError(f"{name} must be unique and increasing")
        if not self.representatives:
            raise ValueError("representatives must be nonempty")
        for name in ("hopping_blocks", "reconstructed_training"):
            value = getattr(self, name)
            if not isinstance(value, ComplexVectorQuantity):
                raise TypeError(f"{name} must be ComplexVectorQuantity")
            _require_unitless(value, name)
        if self.hopping_blocks.magnitude.shape != (len(self.representatives),):
            raise ValueError("hopping blocks must match representatives")
        for name in (
            "reconstruction_maximum_error",
            "reconstruction_absolute_tolerance",
            "hermiticity_maximum_defect",
            "hermiticity_absolute_tolerance",
        ):
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            _require_unitless(value, name)
            if value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        for name in ("reconstruction_passes", "hermiticity_passes"):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be a built-in bool")
        if self.reconstruction_passes is not (
            self.reconstruction_maximum_error.magnitude
            <= self.reconstruction_absolute_tolerance.magnitude
        ):
            raise ValueError("reconstruction disposition does not match its tolerance")
        # Hermiticity requires both structural closure under periodic negation and a
        # bounded conjugate-pair coefficient defect.
        expected_hermiticity = (
            not self.missing_opposite_representatives
            and self.hermiticity_maximum_defect.magnitude
            <= self.hermiticity_absolute_tolerance.magnitude
        )
        if self.hermiticity_passes is not expected_hermiticity:
            raise ValueError("Hermiticity disposition does not match its diagnostics")
        if set(self.paired_representatives) | set(
            self.missing_opposite_representatives
        ) != set(self.representatives):
            raise ValueError("Hermiticity inventories must partition representatives")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "representatives": self.representatives,
            "hopping_blocks": self.hopping_blocks,
            "reconstructed_training": self.reconstructed_training,
            "reconstruction_maximum_error": self.reconstruction_maximum_error,
            "reconstruction_absolute_tolerance": (
                self.reconstruction_absolute_tolerance
            ),
            "reconstruction_passes": self.reconstruction_passes,
            "paired_representatives": self.paired_representatives,
            "missing_opposite_representatives": (self.missing_opposite_representatives),
            "hermiticity_maximum_defect": self.hermiticity_maximum_defect,
            "hermiticity_absolute_tolerance": self.hermiticity_absolute_tolerance,
            "hermiticity_passes": self.hermiticity_passes,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = {
            "representatives",
            "hopping_blocks",
            "reconstructed_training",
            "reconstruction_maximum_error",
            "reconstruction_absolute_tolerance",
            "reconstruction_passes",
            "paired_representatives",
            "missing_opposite_representatives",
            "hermiticity_maximum_defect",
            "hermiticity_absolute_tolerance",
            "hermiticity_passes",
        }
        if set(values) != fields:
            raise ValueError("Mathieu1D transform fields do not match")
        reconstruction_passes = values["reconstruction_passes"]
        hermiticity_passes = values["hermiticity_passes"]
        if (
            type(reconstruction_passes) is not bool
            or type(hermiticity_passes) is not bool
        ):
            raise TypeError("transform dispositions must decode to bools")
        return cls(
            representatives=_decoded_int_tuple(values, "representatives"),
            hopping_blocks=_decoded(values, "hopping_blocks", ComplexVectorQuantity),
            reconstructed_training=_decoded(
                values, "reconstructed_training", ComplexVectorQuantity
            ),
            reconstruction_maximum_error=_decoded(
                values, "reconstruction_maximum_error", ScalarQuantity
            ),
            reconstruction_absolute_tolerance=_decoded(
                values, "reconstruction_absolute_tolerance", ScalarQuantity
            ),
            reconstruction_passes=reconstruction_passes,
            paired_representatives=_decoded_int_tuple(values, "paired_representatives"),
            missing_opposite_representatives=_decoded_int_tuple(
                values, "missing_opposite_representatives"
            ),
            hermiticity_maximum_defect=_decoded(
                values, "hermiticity_maximum_defect", ScalarQuantity
            ),
            hermiticity_absolute_tolerance=_decoded(
                values, "hermiticity_absolute_tolerance", ScalarQuantity
            ),
            hermiticity_passes=hermiticity_passes,
        )


@dataclass(frozen=True, slots=True, eq=False)
class Mathieu1dRangeResult(BaseTypedRecord):
    """Retain one mediated/direct finite-range reduction and its diagnostics.

    Parameters
    ----------
    maximum_range, representatives
        Symmetric retained range and its complete ordered representative inventory.
    mediated_hopping_blocks, direct_hopping_blocks
        Coefficients from truncating the complete transform and from independently
        fitting the same finite model class.
    training_candidate, evaluation_candidate
        Mediated-route values on construction and withheld coordinate inventories.
    training_maximum_error, evaluation_maximum_error, omitted_block_l2_norm
        Recorded finite approximation errors and discarded coefficient norm.
    parseval_training_squared_residual, parseval_expected_squared_residual
        Observed and omitted-block-predicted squared residuals.
    parseval_absolute_residual, parseval_absolute_tolerance
        Absolute Parseval defect and admitted tolerance.
    parseval_passes
        Disposition correlated with the Parseval values.
    direct_design_rank, direct_design_condition_number, direct_is_identified
        Weighted least-squares design diagnostics.
    direct_training_l2_residual, direct_training_maximum_residual
        Residual norms for the direct fit.
    route_coefficient_l2_defect, route_sampled_l2_defect
        Mediated-versus-direct coefficient and sampled Euclidean discrepancies.
    route_sampled_maximum_defect
        Maximum sampled discrepancy between routes.
    bandwidth, zone_center_curvature
        Finite reconstructed-band shape diagnostics.
    maximum_imaginary_residual, imaginary_absolute_tolerance
        Real-valuedness defect and admitted tolerance.
    band_shape_passes
        Disposition correlated with the imaginary residual.
    """

    maximum_range: int
    representatives: tuple[int, ...]
    mediated_hopping_blocks: ComplexVectorQuantity
    direct_hopping_blocks: ComplexVectorQuantity
    training_candidate: ComplexVectorQuantity
    evaluation_candidate: ComplexVectorQuantity
    training_maximum_error: ScalarQuantity
    evaluation_maximum_error: ScalarQuantity
    omitted_block_l2_norm: ScalarQuantity
    parseval_training_squared_residual: ScalarQuantity
    parseval_expected_squared_residual: ScalarQuantity
    parseval_absolute_residual: ScalarQuantity
    parseval_absolute_tolerance: ScalarQuantity
    parseval_passes: bool
    direct_design_rank: int
    direct_design_condition_number: float
    direct_is_identified: bool
    direct_training_l2_residual: ScalarQuantity
    direct_training_maximum_residual: ScalarQuantity
    route_coefficient_l2_defect: ScalarQuantity
    route_sampled_l2_defect: ScalarQuantity
    route_sampled_maximum_defect: ScalarQuantity
    bandwidth: ScalarQuantity
    zone_center_curvature: ScalarQuantity
    maximum_imaginary_residual: ScalarQuantity
    imaginary_absolute_tolerance: ScalarQuantity
    band_shape_passes: bool

    def __post_init__(self) -> None:
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        if not (
            isinstance(self.representatives, tuple)
            and self.representatives
            and all(type(item) is int for item in self.representatives)
        ):
            raise TypeError("representatives must be a nonempty tuple of ints")
        if self.representatives != tuple(sorted(set(self.representatives))):
            raise ValueError("representatives must be unique and increasing")
        if any(abs(value) > self.maximum_range for value in self.representatives):
            raise ValueError("representatives exceed maximum_range")
        for name in (
            "mediated_hopping_blocks",
            "direct_hopping_blocks",
            "training_candidate",
            "evaluation_candidate",
        ):
            value = getattr(self, name)
            if not isinstance(value, ComplexVectorQuantity):
                raise TypeError(f"{name} must be ComplexVectorQuantity")
            _require_unitless(value, name)
        expected_shape = (len(self.representatives),)
        if self.mediated_hopping_blocks.magnitude.shape != expected_shape or (
            self.direct_hopping_blocks.magnitude.shape != expected_shape
        ):
            raise ValueError("hopping blocks must match representatives")
        scalar_names = (
            "training_maximum_error",
            "evaluation_maximum_error",
            "omitted_block_l2_norm",
            "parseval_training_squared_residual",
            "parseval_expected_squared_residual",
            "parseval_absolute_residual",
            "parseval_absolute_tolerance",
            "direct_training_l2_residual",
            "direct_training_maximum_residual",
            "route_coefficient_l2_defect",
            "route_sampled_l2_defect",
            "route_sampled_maximum_defect",
            "bandwidth",
            "zone_center_curvature",
            "maximum_imaginary_residual",
            "imaginary_absolute_tolerance",
        )
        signed = {"zone_center_curvature"}
        for name in scalar_names:
            value = getattr(self, name)
            if not isinstance(value, ScalarQuantity):
                raise TypeError(f"{name} must be ScalarQuantity")
            _require_unitless(value, name)
            if name not in signed and value.magnitude < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        for name in (
            "parseval_passes",
            "direct_is_identified",
            "band_shape_passes",
        ):
            if type(getattr(self, name)) is not bool:
                raise TypeError(f"{name} must be a built-in bool")
        if self.parseval_passes is not (
            self.parseval_absolute_residual.magnitude
            <= self.parseval_absolute_tolerance.magnitude
        ):
            raise ValueError("Parseval disposition does not match its tolerance")
        if type(self.direct_design_rank) is not int:
            raise TypeError("direct_design_rank must be a built-in int")
        if self.direct_design_rank < 0 or self.direct_design_rank > len(
            self.representatives
        ):
            raise ValueError("direct_design_rank is outside the design extent")
        # Identification is a statement about this declared finite design matrix, not
        # about uniqueness of a continuum or material Hamiltonian.
        if self.direct_is_identified is not (
            self.direct_design_rank == len(self.representatives)
        ):
            raise ValueError("direct_is_identified must match the design rank")
        if type(self.direct_design_condition_number) is not float:
            raise TypeError("direct_design_condition_number must be a built-in float")
        if (
            not np.isfinite(self.direct_design_condition_number)
            or self.direct_design_condition_number < 1.0
        ):
            raise ValueError("direct_design_condition_number must be finite and >= 1")
        if self.band_shape_passes is not (
            self.maximum_imaginary_residual.magnitude
            <= self.imaginary_absolute_tolerance.magnitude
        ):
            raise ValueError("band-shape disposition does not match its tolerance")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {name: getattr(self, name) for name in self._field_names()}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != set(cls._field_names()):
            raise ValueError("Mathieu1D range-result fields do not match")
        maximum_range = values["maximum_range"]
        direct_design_rank = values["direct_design_rank"]
        condition = values["direct_design_condition_number"]
        parseval_passes = values["parseval_passes"]
        identified = values["direct_is_identified"]
        band_shape_passes = values["band_shape_passes"]
        if type(maximum_range) is not int or type(direct_design_rank) is not int:
            raise TypeError("range integer fields must decode to ints")
        if type(condition) is not float:
            raise TypeError("range condition number must decode to float")
        if any(
            type(value) is not bool
            for value in (parseval_passes, identified, band_shape_passes)
        ):
            raise TypeError("range dispositions must decode to bools")
        scalar_names = (
            "training_maximum_error",
            "evaluation_maximum_error",
            "omitted_block_l2_norm",
            "parseval_training_squared_residual",
            "parseval_expected_squared_residual",
            "parseval_absolute_residual",
            "parseval_absolute_tolerance",
            "direct_training_l2_residual",
            "direct_training_maximum_residual",
            "route_coefficient_l2_defect",
            "route_sampled_l2_defect",
            "route_sampled_maximum_defect",
            "bandwidth",
            "zone_center_curvature",
            "maximum_imaginary_residual",
            "imaginary_absolute_tolerance",
        )
        scalars = {
            name: _decoded(values, name, ScalarQuantity) for name in scalar_names
        }
        return cls(
            maximum_range=maximum_range,
            representatives=_decoded_int_tuple(values, "representatives"),
            mediated_hopping_blocks=_decoded(
                values, "mediated_hopping_blocks", ComplexVectorQuantity
            ),
            direct_hopping_blocks=_decoded(
                values, "direct_hopping_blocks", ComplexVectorQuantity
            ),
            training_candidate=_decoded(
                values, "training_candidate", ComplexVectorQuantity
            ),
            evaluation_candidate=_decoded(
                values, "evaluation_candidate", ComplexVectorQuantity
            ),
            training_maximum_error=scalars["training_maximum_error"],
            evaluation_maximum_error=scalars["evaluation_maximum_error"],
            omitted_block_l2_norm=scalars["omitted_block_l2_norm"],
            parseval_training_squared_residual=scalars[
                "parseval_training_squared_residual"
            ],
            parseval_expected_squared_residual=scalars[
                "parseval_expected_squared_residual"
            ],
            parseval_absolute_residual=scalars["parseval_absolute_residual"],
            parseval_absolute_tolerance=scalars["parseval_absolute_tolerance"],
            parseval_passes=cast(bool, parseval_passes),
            direct_design_rank=direct_design_rank,
            direct_design_condition_number=condition,
            direct_is_identified=cast(bool, identified),
            direct_training_l2_residual=scalars["direct_training_l2_residual"],
            direct_training_maximum_residual=scalars[
                "direct_training_maximum_residual"
            ],
            route_coefficient_l2_defect=scalars["route_coefficient_l2_defect"],
            route_sampled_l2_defect=scalars["route_sampled_l2_defect"],
            route_sampled_maximum_defect=scalars["route_sampled_maximum_defect"],
            bandwidth=scalars["bandwidth"],
            zone_center_curvature=scalars["zone_center_curvature"],
            maximum_imaginary_residual=scalars["maximum_imaginary_residual"],
            imaginary_absolute_tolerance=scalars["imaginary_absolute_tolerance"],
            band_shape_passes=cast(bool, band_shape_passes),
        )

    @staticmethod
    def _field_names() -> tuple[str, ...]:
        return (
            "maximum_range",
            "representatives",
            "mediated_hopping_blocks",
            "direct_hopping_blocks",
            "training_candidate",
            "evaluation_candidate",
            "training_maximum_error",
            "evaluation_maximum_error",
            "omitted_block_l2_norm",
            "parseval_training_squared_residual",
            "parseval_expected_squared_residual",
            "parseval_absolute_residual",
            "parseval_absolute_tolerance",
            "parseval_passes",
            "direct_design_rank",
            "direct_design_condition_number",
            "direct_is_identified",
            "direct_training_l2_residual",
            "direct_training_maximum_residual",
            "route_coefficient_l2_defect",
            "route_sampled_l2_defect",
            "route_sampled_maximum_defect",
            "bandwidth",
            "zone_center_curvature",
            "maximum_imaginary_residual",
            "imaginary_absolute_tolerance",
            "band_shape_passes",
        )


@dataclass(frozen=True, slots=True, eq=False)
class Mathieu1dCalculationResult(BaseTypedRecord):
    """Retain one complete direct Mathieu1D finite-reduction calculation.

    Parameters
    ----------
    calculation_family, execution_id, evidence_status, claim_boundary
        Stable family identifier, concrete execution identifier, evidence status, and
        bounded claim attached to these exact result bytes.
    configuration
        Exact authored finite-calculation configuration.
    refinement, bands, transform, ranges
        Correlated finite representation, sampled-band, complete-transform, and
        declared range-study sections.

    Raises
    ------
    TypeError
        Metadata or a scientific section has the wrong domain type.
    ValueError
        Metadata is empty or correlated configuration and result inventories disagree.
    """

    calculation_family: str
    execution_id: str
    evidence_status: str
    claim_boundary: str
    configuration: Mathieu1dConfiguration
    refinement: Mathieu1dRefinementResult
    bands: Mathieu1dBandSamplesResult
    transform: Mathieu1dTransformResult
    ranges: tuple[Mathieu1dRangeResult, ...]

    def __post_init__(self) -> None:
        for name in (
            "calculation_family",
            "execution_id",
            "evidence_status",
            "claim_boundary",
        ):
            value = getattr(self, name)
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if self.calculation_family != "mathieu1d-finite-reduction":
            raise ValueError("calculation_family does not identify Mathieu1D reduction")
        if not isinstance(self.configuration, Mathieu1dConfiguration):
            raise TypeError("configuration must be Mathieu1dConfiguration")
        if not isinstance(self.refinement, Mathieu1dRefinementResult):
            raise TypeError("refinement must be Mathieu1dRefinementResult")
        if not isinstance(self.bands, Mathieu1dBandSamplesResult):
            raise TypeError("bands must be Mathieu1dBandSamplesResult")
        if not isinstance(self.transform, Mathieu1dTransformResult):
            raise TypeError("transform must be Mathieu1dTransformResult")
        if not (
            isinstance(self.ranges, tuple)
            and self.ranges
            and all(isinstance(value, Mathieu1dRangeResult) for value in self.ranges)
        ):
            raise TypeError("ranges must be a nonempty tuple of Mathieu1dRangeResult")
        # The root owns all cross-section correlations. Individual section constructors
        # cannot know which authored inventory the complete result intended to use.
        if tuple(value.maximum_range for value in self.ranges) != (
            self.configuration.hopping_ranges
        ):
            raise ValueError("range results must match the configured inventory")
        if self.refinement.plane_wave_cutoffs != (
            self.configuration.plane_wave_cutoffs
        ):
            raise ValueError("refinement cutoffs must match the configuration")
        if self.refinement.finite_difference_points != (
            self.configuration.finite_difference_points
        ):
            raise ValueError("refinement grids must match the configuration")
        parent_coordinates = np.asarray(
            self.configuration.parent_reduced_momenta,
            dtype=np.float64,
        )
        if not np.array_equal(
            self.refinement.parent_reduced_momenta.magnitude,
            parent_coordinates,
        ):
            raise ValueError("refinement coordinates must match the configuration")
        if self.refinement.parent_reference_energies.magnitude.shape != (
            len(self.configuration.parent_reduced_momenta),
            self.configuration.compared_band_count,
        ):
            raise ValueError(
                "parent spectrum must match configured coordinates and bands"
            )
        training_coordinates = np.asarray(
            self.configuration.training_reduced_momenta,
            dtype=np.float64,
        )
        if not np.array_equal(
            self.bands.training_reduced_momenta.magnitude,
            training_coordinates,
        ):
            raise ValueError("training coordinates must match the configuration")
        evaluation_coordinates = np.asarray(
            self.configuration.evaluation_reduced_momenta,
            dtype=np.float64,
        )
        if not np.array_equal(
            self.bands.evaluation_reduced_momenta.magnitude,
            evaluation_coordinates,
        ):
            raise ValueError("evaluation coordinates must match the configuration")
        # The even mesh fixes one canonical centered half-open representative set;
        # accepting a reordered or incomplete transform would change the wire meaning.
        training_size = self.configuration.reciprocal_training_mesh_size
        expected_complete_representatives = tuple(
            range(-training_size // 2, training_size // 2)
        )
        if self.transform.representatives != expected_complete_representatives:
            raise ValueError("complete representatives must match the training mesh")
        if self.transform.reconstructed_training.magnitude.shape != (training_size,):
            raise ValueError("transform reconstruction must match the training mesh")
        if self.transform.reconstruction_absolute_tolerance.magnitude != (
            self.configuration.reconstruction_absolute_tolerance
        ):
            raise ValueError(
                "transform reconstruction tolerance must match configuration"
            )
        if self.transform.hermiticity_absolute_tolerance.magnitude != (
            self.configuration.hermiticity_absolute_tolerance
        ):
            raise ValueError("transform Hermiticity tolerance must match configuration")
        evaluation_size = len(self.configuration.evaluation_reduced_momenta)
        for value in self.ranges:
            expected_representatives = tuple(
                range(-value.maximum_range, value.maximum_range + 1)
            )
            if value.representatives != expected_representatives:
                raise ValueError("range representatives must be complete and symmetric")
            if value.training_candidate.magnitude.shape != (training_size,):
                raise ValueError("range training candidates must match the mesh")
            if value.evaluation_candidate.magnitude.shape != (evaluation_size,):
                raise ValueError("range evaluation candidates must match evaluation")
            if value.parseval_absolute_tolerance.magnitude != (
                self.configuration.parseval_absolute_tolerance
            ):
                raise ValueError("range Parseval tolerance must match configuration")
            if value.imaginary_absolute_tolerance.magnitude != (
                self.configuration.imaginary_absolute_tolerance
            ):
                raise ValueError("range imaginary tolerance must match configuration")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "calculation_family": self.calculation_family,
            "execution_id": self.execution_id,
            "evidence_status": self.evidence_status,
            "claim_boundary": self.claim_boundary,
            "configuration": self.configuration,
            "refinement": self.refinement,
            "bands": self.bands,
            "transform": self.transform,
            "ranges": self.ranges,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "calculation_family",
            "execution_id",
            "evidence_status",
            "claim_boundary",
            "configuration",
            "refinement",
            "bands",
            "transform",
            "ranges",
        }:
            raise ValueError("Mathieu1D calculation-result fields do not match")
        metadata: dict[str, str] = {}
        for name in (
            "calculation_family",
            "execution_id",
            "evidence_status",
            "claim_boundary",
        ):
            value = values[name]
            if type(value) is not str:
                raise TypeError(f"{name} must decode to a built-in string")
            metadata[name] = value
        mappings: dict[str, Mapping[str, SerializableValue]] = {}
        for name in ("configuration", "refinement", "bands", "transform"):
            value = values[name]
            if not isinstance(value, Mapping):
                raise TypeError(f"{name} must decode to a mapping")
            mappings[name] = value
        ranges_value = values["ranges"]
        if not isinstance(ranges_value, tuple) or any(
            not isinstance(value, Mapping) for value in ranges_value
        ):
            raise TypeError("ranges must decode to a tuple of mappings")
        return cls(
            calculation_family=metadata["calculation_family"],
            execution_id=metadata["execution_id"],
            evidence_status=metadata["evidence_status"],
            claim_boundary=metadata["claim_boundary"],
            configuration=Mathieu1dConfiguration.from_dict(mappings["configuration"]),
            refinement=Mathieu1dRefinementResult.from_dict(mappings["refinement"]),
            bands=Mathieu1dBandSamplesResult.from_dict(mappings["bands"]),
            transform=Mathieu1dTransformResult.from_dict(mappings["transform"]),
            ranges=tuple(
                Mathieu1dRangeResult.from_dict(value) for value in ranges_value
            ),
        )


__all__ = [
    "Mathieu1dBandSamplesResult",
    "Mathieu1dCalculationResult",
    "Mathieu1dRangeResult",
    "Mathieu1dRefinementResult",
    "Mathieu1dTransformResult",
]
