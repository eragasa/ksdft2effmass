"""Parent-model diagnostics and their rank-N band-alignment analysis."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self, final

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.physkit.numerics.typing.numpy.arrays import ComplexArray

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    MatrixFieldErrorAnalyzer,
    MatrixFieldHermiticityAnalyzer,
    MatrixFieldIsometryAnalyzer,
    MatrixProjectorFieldAnalyzer,
)
from ksdft2effmass.periodic1d.rankN._record_admission import (
    _decoded_float,
    _finite_nonnegative,
    _float_array,
    _nonempty,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.mesh_sample import (
    Periodic1DRankNConstructionMeshSample,
)
from ksdft2effmass.periodic1d.rankN.band_equivalence_hopping_locality.request import (
    Periodic1DRankNBandEquivalenceHoppingLocalityRequest,
)
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNModelDiagnostics(BaseTypedRecord):
    """Retain analytic-gap, sampled-gap, structure, and recovery diagnostics."""

    case_identity: str
    retained_rank: int
    circuit_depth: int
    construction_mesh_size: int
    exact_analytic_isolation_gap: float
    sampled_isolation_gaps: Float64Array
    exact_analytic_transformation_angle_maximum: float
    sampled_transformation_angle_maxima: Float64Array
    parent_hermiticity_defect: float
    reference_frame_isometry_defect: float
    gauge_unitarity_defect: float
    gauge_transformed_frame_isometry_defect: float
    gauge_transformed_projector_equality_defect: float
    reference_projector_hermiticity_defect: float
    reference_projector_idempotency_defect: float
    reference_operator_recovery_defect: float
    reference_spectrum_recovery_defect: float
    gauge_transformed_operator_recovery_defect: float
    gauge_transformed_spectrum_recovery_defect: float
    oracle_frame_recovery_defect: float
    oracle_operator_recovery_defect: float

    def __post_init__(self) -> None:
        _nonempty(self.case_identity, "case_identity")
        for integer_value, name, inventory in (
            (
                self.retained_rank,
                "retained_rank",
                Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS,
            ),
            (
                self.circuit_depth,
                "circuit_depth",
                Periodic1DRankNAlignmentConfiguration.CIRCUIT_DEPTHS,
            ),
            (
                self.construction_mesh_size,
                "construction_mesh_size",
                Periodic1DRankNAlignmentConfiguration.CONSTRUCTION_MESH_SIZES,
            ),
        ):
            if type(integer_value) is not int:
                raise TypeError(f"{name} must be a built-in integer")
            if integer_value not in inventory:
                raise ValueError(f"{name} must be in the frozen inventory")
        expected_case_identity = f"r{self.retained_rank:02d}-L{self.circuit_depth:02d}"
        if self.case_identity != expected_case_identity:
            raise ValueError("case_identity is inconsistent with rank and depth")
        sampled = _float_array(
            self.sampled_isolation_gaps,
            "sampled_isolation_gaps",
        )
        if sampled.shape != (
            len(Periodic1DRankNAlignmentConfiguration.CONSTRUCTION_MESH_SIZES),
        ):
            raise ValueError(
                "sampled_isolation_gaps must cover every construction mesh"
            )
        if bool((sampled < self.exact_analytic_isolation_gap).any()):
            raise ValueError(
                "sampled isolation gaps must respect the analytic certificate"
            )
        sampled_angles = _float_array(
            self.sampled_transformation_angle_maxima,
            "sampled_transformation_angle_maxima",
        )
        if sampled_angles.shape != sampled.shape:
            raise ValueError(
                "sampled transformation angles must cover every construction mesh"
            )
        if bool(
            (sampled_angles > self.exact_analytic_transformation_angle_maximum).any()
        ):
            raise ValueError(
                "sampled transformation angle exceeds the analytic certificate"
            )
        for value, name in (
            (self.exact_analytic_isolation_gap, "exact_analytic_isolation_gap"),
            (
                self.exact_analytic_transformation_angle_maximum,
                "exact_analytic_transformation_angle_maximum",
            ),
            (self.parent_hermiticity_defect, "parent_hermiticity_defect"),
            (
                self.reference_frame_isometry_defect,
                "reference_frame_isometry_defect",
            ),
            (self.gauge_unitarity_defect, "gauge_unitarity_defect"),
            (
                self.gauge_transformed_frame_isometry_defect,
                "gauge_transformed_frame_isometry_defect",
            ),
            (
                self.gauge_transformed_projector_equality_defect,
                "gauge_transformed_projector_equality_defect",
            ),
            (
                self.reference_projector_hermiticity_defect,
                "reference_projector_hermiticity_defect",
            ),
            (
                self.reference_projector_idempotency_defect,
                "reference_projector_idempotency_defect",
            ),
            (
                self.reference_operator_recovery_defect,
                "reference_operator_recovery_defect",
            ),
            (
                self.reference_spectrum_recovery_defect,
                "reference_spectrum_recovery_defect",
            ),
            (
                self.gauge_transformed_operator_recovery_defect,
                "gauge_transformed_operator_recovery_defect",
            ),
            (
                self.gauge_transformed_spectrum_recovery_defect,
                "gauge_transformed_spectrum_recovery_defect",
            ),
            (self.oracle_frame_recovery_defect, "oracle_frame_recovery_defect"),
            (
                self.oracle_operator_recovery_defect,
                "oracle_operator_recovery_defect",
            ),
        ):
            _finite_nonnegative(value, name)
        object.__setattr__(self, "sampled_isolation_gaps", sampled)
        object.__setattr__(self, "sampled_transformation_angle_maxima", sampled_angles)

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "case_identity": self.case_identity,
            "retained_rank": self.retained_rank,
            "circuit_depth": self.circuit_depth,
            "construction_mesh_size": self.construction_mesh_size,
            "exact_analytic_isolation_gap": self.exact_analytic_isolation_gap,
            "sampled_isolation_gaps": self.sampled_isolation_gaps,
            "exact_analytic_transformation_angle_maximum": (
                self.exact_analytic_transformation_angle_maximum
            ),
            "sampled_transformation_angle_maxima": (
                self.sampled_transformation_angle_maxima
            ),
            "parent_hermiticity_defect": self.parent_hermiticity_defect,
            "reference_frame_isometry_defect": self.reference_frame_isometry_defect,
            "gauge_unitarity_defect": self.gauge_unitarity_defect,
            "gauge_transformed_frame_isometry_defect": (
                self.gauge_transformed_frame_isometry_defect
            ),
            "gauge_transformed_projector_equality_defect": (
                self.gauge_transformed_projector_equality_defect
            ),
            "reference_projector_hermiticity_defect": (
                self.reference_projector_hermiticity_defect
            ),
            "reference_projector_idempotency_defect": (
                self.reference_projector_idempotency_defect
            ),
            "reference_operator_recovery_defect": (
                self.reference_operator_recovery_defect
            ),
            "reference_spectrum_recovery_defect": (
                self.reference_spectrum_recovery_defect
            ),
            "gauge_transformed_operator_recovery_defect": (
                self.gauge_transformed_operator_recovery_defect
            ),
            "gauge_transformed_spectrum_recovery_defect": (
                self.gauge_transformed_spectrum_recovery_defect
            ),
            "oracle_frame_recovery_defect": self.oracle_frame_recovery_defect,
            "oracle_operator_recovery_defect": self.oracle_operator_recovery_defect,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "case_identity",
            "retained_rank",
            "circuit_depth",
            "construction_mesh_size",
            "exact_analytic_isolation_gap",
            "sampled_isolation_gaps",
            "exact_analytic_transformation_angle_maximum",
            "sampled_transformation_angle_maxima",
            "parent_hermiticity_defect",
            "reference_frame_isometry_defect",
            "gauge_unitarity_defect",
            "gauge_transformed_frame_isometry_defect",
            "gauge_transformed_projector_equality_defect",
            "reference_projector_hermiticity_defect",
            "reference_projector_idempotency_defect",
            "reference_operator_recovery_defect",
            "reference_spectrum_recovery_defect",
            "gauge_transformed_operator_recovery_defect",
            "gauge_transformed_spectrum_recovery_defect",
            "oracle_frame_recovery_defect",
            "oracle_operator_recovery_defect",
        }:
            raise ValueError("model diagnostic fields do not match")
        sampled = values["sampled_isolation_gaps"]
        sampled_angles = values["sampled_transformation_angle_maxima"]
        case_identity = values["case_identity"]
        rank = values["retained_rank"]
        circuit_depth = values["circuit_depth"]
        construction_mesh_size = values["construction_mesh_size"]
        if not isinstance(sampled, np.ndarray) or not isinstance(
            sampled_angles, np.ndarray
        ):
            raise TypeError("sampled diagnostics must decode to numpy.ndarray")
        if type(case_identity) is not str:
            raise TypeError("case_identity must decode to a built-in string")
        if (
            type(rank) is not int
            or type(circuit_depth) is not int
            or type(construction_mesh_size) is not int
        ):
            raise TypeError("rank, depth, and mesh size must decode to integers")
        return cls(
            case_identity=case_identity,
            retained_rank=rank,
            circuit_depth=circuit_depth,
            construction_mesh_size=construction_mesh_size,
            exact_analytic_isolation_gap=_decoded_float(
                values["exact_analytic_isolation_gap"],
                "exact_analytic_isolation_gap",
            ),
            sampled_isolation_gaps=sampled,
            exact_analytic_transformation_angle_maximum=_decoded_float(
                values["exact_analytic_transformation_angle_maximum"],
                "exact_analytic_transformation_angle_maximum",
            ),
            sampled_transformation_angle_maxima=sampled_angles,
            parent_hermiticity_defect=_decoded_float(
                values["parent_hermiticity_defect"], "parent_hermiticity_defect"
            ),
            reference_frame_isometry_defect=_decoded_float(
                values["reference_frame_isometry_defect"],
                "reference_frame_isometry_defect",
            ),
            gauge_unitarity_defect=_decoded_float(
                values["gauge_unitarity_defect"], "gauge_unitarity_defect"
            ),
            gauge_transformed_frame_isometry_defect=_decoded_float(
                values["gauge_transformed_frame_isometry_defect"],
                "gauge_transformed_frame_isometry_defect",
            ),
            gauge_transformed_projector_equality_defect=_decoded_float(
                values["gauge_transformed_projector_equality_defect"],
                "gauge_transformed_projector_equality_defect",
            ),
            reference_projector_hermiticity_defect=_decoded_float(
                values["reference_projector_hermiticity_defect"],
                "reference_projector_hermiticity_defect",
            ),
            reference_projector_idempotency_defect=_decoded_float(
                values["reference_projector_idempotency_defect"],
                "reference_projector_idempotency_defect",
            ),
            reference_operator_recovery_defect=_decoded_float(
                values["reference_operator_recovery_defect"],
                "reference_operator_recovery_defect",
            ),
            reference_spectrum_recovery_defect=_decoded_float(
                values["reference_spectrum_recovery_defect"],
                "reference_spectrum_recovery_defect",
            ),
            gauge_transformed_operator_recovery_defect=_decoded_float(
                values["gauge_transformed_operator_recovery_defect"],
                "gauge_transformed_operator_recovery_defect",
            ),
            gauge_transformed_spectrum_recovery_defect=_decoded_float(
                values["gauge_transformed_spectrum_recovery_defect"],
                "gauge_transformed_spectrum_recovery_defect",
            ),
            oracle_frame_recovery_defect=_decoded_float(
                values["oracle_frame_recovery_defect"],
                "oracle_frame_recovery_defect",
            ),
            oracle_operator_recovery_defect=_decoded_float(
                values["oracle_operator_recovery_defect"],
                "oracle_operator_recovery_defect",
            ),
        )


@dataclass(frozen=True, slots=True)
class Periodic1DRankNModelDiagnosticsRequest:
    """Bind one calculation request to one consistent construction-mesh sample."""

    calculation_request: Periodic1DRankNBandEquivalenceHoppingLocalityRequest
    sample: Periodic1DRankNConstructionMeshSample

    def __post_init__(self) -> None:
        if (
            type(self.calculation_request)
            is not Periodic1DRankNBandEquivalenceHoppingLocalityRequest
        ):
            raise TypeError("calculation_request must be the exact rank-N request")
        if type(self.sample) is not Periodic1DRankNConstructionMeshSample:
            raise TypeError("sample must be the exact construction-mesh sample")
        sample = self.sample
        request = self.calculation_request
        if (
            sample.parent_model.band_subspace_rank != request.retained_rank
            or sample.gauge_transformation.circuit_depth != request.circuit_depth
            or self.sample.construction_mesh_size
            not in request.configuration.construction_mesh_sizes
        ):
            raise ValueError("sample must match the calculation request")


@final
class Periodic1DRankNModelDiagnosticsAnalyzer:
    """Evaluate parent-model structure and direct-recovery diagnostics."""

    __slots__ = ("_request",)

    def __init__(self, request: Periodic1DRankNModelDiagnosticsRequest) -> None:
        if type(request) is not Periodic1DRankNModelDiagnosticsRequest:
            raise TypeError("request must be the exact model-diagnostics request")
        self._request = request

    @property
    def request(self) -> Periodic1DRankNModelDiagnosticsRequest:
        """Return the immutable model-diagnostics request."""
        return self._request

    def execute(self) -> Periodic1DRankNModelDiagnostics:
        """Return diagnostics after enforcing the declared structure thresholds."""
        calculation_request = self._request.calculation_request
        sample = self._request.sample
        parent_model = sample.parent_model
        gauge_transformation = sample.gauge_transformation
        coordinates = sample.coordinates
        reference_frames = sample.reference_frames
        gauge_transformed_frames = sample.gauge_transformed_frames
        energy = calculation_request.controls.energy_reference
        parent = parent_model.parent_hamiltonians(coordinates)
        exact = parent_model.exact_reduced_hamiltonians(coordinates)
        gauge_transformed = gauge_transformation.transform_operators(
            coordinates,
            exact,
        )
        gauge = gauge_transformation.unitaries(coordinates)
        reference_recovered = _adjoint(reference_frames) @ parent @ reference_frames
        gauge_transformed_recovered = (
            _adjoint(gauge_transformed_frames) @ parent @ gauge_transformed_frames
        )
        oracle_frames = gauge_transformed_frames @ _adjoint(gauge)
        oracle_operator = _right_basis_change(gauge_transformed, _adjoint(gauge))
        parent_hermiticity = MatrixFieldHermiticityAnalyzer(parent, energy).execute()
        reference_isometry = MatrixFieldIsometryAnalyzer().execute(reference_frames)
        gauge_transformed_isometry = MatrixFieldIsometryAnalyzer().execute(
            gauge_transformed_frames
        )
        gauge_isometry = MatrixFieldIsometryAnalyzer().execute(gauge)
        projectors = reference_frames @ _adjoint(reference_frames)
        gauge_transformed_projectors = gauge_transformed_frames @ _adjoint(
            gauge_transformed_frames
        )
        gauge_transformed_projector_equality = float(
            np.max(
                np.linalg.norm(
                    gauge_transformed_projectors - projectors,
                    axis=(-2, -1),
                )
            )
        )
        projector = MatrixProjectorFieldAnalyzer().execute(projectors)
        reference_error = MatrixFieldErrorAnalyzer(
            approximation=reference_recovered,
            reference=exact,
            norm_energy_scale=energy,
        ).result()
        gauge_transformed_error = MatrixFieldErrorAnalyzer(
            approximation=gauge_transformed_recovered,
            reference=gauge_transformed,
            norm_energy_scale=energy,
        ).result()
        gauge_transformed_spectrum = MatrixFieldErrorAnalyzer(
            approximation=gauge_transformed,
            reference=exact,
            norm_energy_scale=energy,
        ).result()
        oracle_error = MatrixFieldErrorAnalyzer(
            approximation=oracle_operator,
            reference=exact,
            norm_energy_scale=energy,
        ).result()
        oracle_frame = float(
            np.max(np.linalg.norm(oracle_frames - reference_frames, axis=(-2, -1)))
            / math.sqrt(parent_model.band_subspace_rank)
        )
        sampled_gaps = []
        sampled_transformation_angles = []
        for mesh_size in calculation_request.configuration.construction_mesh_sizes:
            mesh_coordinates = (
                calculation_request.configuration.construction_coordinates(mesh_size)
            )
            retained = parent_model.retained_energies(mesh_coordinates)
            exterior = parent_model.exterior_energies(mesh_coordinates)
            sampled_gaps.append(
                float(np.min(np.min(exterior, axis=1) - np.max(retained, axis=1)))
            )
            sampled_transformation_angles.append(
                gauge_transformation.sampled_angle_maximum(mesh_coordinates)
            )
        diagnostics = Periodic1DRankNModelDiagnostics(
            case_identity=calculation_request.case_identity,
            retained_rank=parent_model.band_subspace_rank,
            circuit_depth=gauge_transformation.circuit_depth,
            construction_mesh_size=sample.construction_mesh_size,
            exact_analytic_isolation_gap=parent_model.exact_isolation_gap,
            sampled_isolation_gaps=np.asarray(sampled_gaps, dtype=np.float64),
            exact_analytic_transformation_angle_maximum=(
                gauge_transformation.exact_angle_maximum
            ),
            sampled_transformation_angle_maxima=np.asarray(
                sampled_transformation_angles,
                dtype=np.float64,
            ),
            parent_hermiticity_defect=(
                parent_hermiticity.normalized_maximum_frobenius_defect
            ),
            reference_frame_isometry_defect=(
                reference_isometry.normalized_maximum_frobenius_defect
            ),
            gauge_unitarity_defect=(gauge_isometry.normalized_maximum_frobenius_defect),
            gauge_transformed_frame_isometry_defect=(
                gauge_transformed_isometry.normalized_maximum_frobenius_defect
            ),
            gauge_transformed_projector_equality_defect=gauge_transformed_projector_equality,
            reference_projector_hermiticity_defect=(
                projector.normalized_maximum_hermiticity_frobenius_defect
            ),
            reference_projector_idempotency_defect=(
                projector.normalized_maximum_idempotency_frobenius_defect
            ),
            reference_operator_recovery_defect=(
                reference_error.normalized_matrix_frobenius_maximum
            ),
            reference_spectrum_recovery_defect=(
                reference_error.normalized_ordered_spectrum_maximum
            ),
            gauge_transformed_operator_recovery_defect=(
                gauge_transformed_error.normalized_matrix_frobenius_maximum
            ),
            gauge_transformed_spectrum_recovery_defect=(
                gauge_transformed_spectrum.normalized_ordered_spectrum_maximum
            ),
            oracle_frame_recovery_defect=oracle_frame,
            oracle_operator_recovery_defect=(
                oracle_error.normalized_matrix_frobenius_maximum
            ),
        )
        maximum_structure_defect = max(
            diagnostics.parent_hermiticity_defect,
            diagnostics.reference_frame_isometry_defect,
            diagnostics.gauge_unitarity_defect,
            diagnostics.gauge_transformed_frame_isometry_defect,
            diagnostics.gauge_transformed_projector_equality_defect,
            diagnostics.reference_projector_hermiticity_defect,
            diagnostics.reference_projector_idempotency_defect,
        )
        if (
            maximum_structure_defect
            > calculation_request.controls.model_structure_tolerance
        ):
            raise ValueError("parent model structure exceeds the frozen tolerance")
        maximum_recovery_defect = max(
            diagnostics.reference_operator_recovery_defect,
            diagnostics.reference_spectrum_recovery_defect,
            diagnostics.gauge_transformed_operator_recovery_defect,
            diagnostics.gauge_transformed_spectrum_recovery_defect,
            diagnostics.oracle_frame_recovery_defect,
            diagnostics.oracle_operator_recovery_defect,
        )
        if (
            maximum_recovery_defect
            > calculation_request.controls.direct_recovery_tolerance
        ):
            raise ValueError("parent model recovery exceeds the frozen tolerance")
        return diagnostics


def _adjoint(value: ComplexArray) -> ComplexArray:
    """Return the adjoint over the final two array axes."""
    return np.swapaxes(value.conjugate(), -1, -2)


def _right_basis_change(
    matrices: ComplexArray,
    right_unitaries: ComplexArray,
) -> ComplexArray:
    """Apply one right-basis change to a matrix field."""
    return np.asarray(
        _adjoint(right_unitaries) @ matrices @ right_unitaries,
        dtype=np.complex128,
    )


__all__ = [
    "Periodic1DRankNModelDiagnostics",
    "Periodic1DRankNModelDiagnosticsAnalyzer",
    "Periodic1DRankNModelDiagnosticsRequest",
]
