"""Canonical wire serialization for bounded synthetic-strain diagnostics.

The analysis layer owns the scientific records.  This module owns their explicit JSON
field mapping and canonical byte encoding; it does not calculate or reinterpret any
scientific quantity.
"""

from __future__ import annotations

import json
from typing import TypedDict

from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain import (
    StrainPointDiagnostic,
    SyntheticStrainResult,
)
from ksdft2effmass.analysis.model_adequacy.band_equivalence_locality.strain_response import (  # noqa: E501
    StrainErrorChannels,
    StrainResponseCutoffDiagnostic,
    StrainResponseModel,
    StrainResponsePointDiagnostic,
    SyntheticStrainResponseResult,
)

from .serialization import CanonicalJsonDocument

M0_RESULT_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "gauge-locality-under-synthetic-strain.m0.result.v1"
)
M1_RESULT_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "gauge-locality-under-synthetic-strain.m1.result.v1"
)
M2_RESULT_SCHEMA_ID = (
    "ksdft2effmass.campaign.model-adequacy."
    "gauge-locality-under-synthetic-strain.m2.result.v1"
)


class _M0PointWire(TypedDict):
    distinct_bond_lengths: int
    first_passing_blocks: list[int | None]
    first_passing_radius: list[float | None]
    maximum_bond_length: float
    metric: list[list[float]]
    minimum_bond_length: float
    nyquist_power: float
    ordinary_fourier_power: float
    path_parameter: float
    restricted_alignment_residual: float
    strain_fraction: float


class _M0ResultWire(TypedDict):
    construction_size: int
    maximum_parseval_defect: float
    maximum_rotation_amplitude: float
    maximum_strain_invariance_defect: float
    path: str
    points: list[_M0PointWire]
    schema: str
    status: str
    tail_tolerances: list[float]


class _ErrorChannelsWire(TypedDict):
    maximum_band: float
    maximum_hamiltonian: float
    rms_band: float
    rms_hamiltonian: float


class _ResponseCutoffWire(TypedDict):
    delta_omitted_power: float
    delta_total: _ErrorChannelsWire | None
    delta_truncation: _ErrorChannelsWire | None
    omitted_power: float
    physical_radius: float | None
    retained_blocks: int | None
    tail_tolerance: float
    total: _ErrorChannelsWire | None
    truncation: _ErrorChannelsWire | None


class _ResponsePointWire(TypedDict):
    aligned_strain_perturbation: _ErrorChannelsWire
    cutoffs: list[_ResponseCutoffWire]
    delta_interpolation: _ErrorChannelsWire
    delta_nyquist_power: float
    delta_offsite_power: float
    delta_onsite_power: float
    interpolation: _ErrorChannelsWire
    maximum_hopping_response: float
    maximum_parent_bond_length: float
    maximum_pointwise_frame_alignment_residual: float
    maximum_scalar_strain_component: float
    maximum_traceless_strain_component: float
    metric: list[list[float]]
    minimum_frame_overlap_singular_value: float
    minimum_hopping_response: float
    minimum_parent_bond_length: float
    minimum_sampled_external_isolation_gap: float
    minimum_seed_overlap: float
    nyquist_power: float
    path_parameter: float
    restricted_global_frame_alignment_residual: float
    rms_scalar_strain_component: float
    rms_traceless_strain_component: float
    strain_fraction: float


class _ResponseResultWire(TypedDict):
    construction_size: int
    evaluation_shift: float
    evaluation_size: int
    maximum_rotation_amplitude: float
    model: str
    path: str
    points: list[_ResponsePointWire]
    radial_decay_beta: float
    schema: str
    status: str
    tail_tolerances: list[float]


type _StrainWire = _M0ResultWire | _ResponseResultWire


def _canonical_document(value: _StrainWire) -> CanonicalJsonDocument:
    content = (
        json.dumps(value, allow_nan=False, separators=(",", ":"), sort_keys=True) + "\n"
    ).encode("utf-8")
    return CanonicalJsonDocument(content)


def _matrix_wire(value: tuple[tuple[float, ...], ...]) -> list[list[float]]:
    return [list(row) for row in value]


def _error_wire(value: StrainErrorChannels) -> _ErrorChannelsWire:
    return {
        "maximum_band": value.maximum_band,
        "maximum_hamiltonian": value.maximum_hamiltonian,
        "rms_band": value.rms_band,
        "rms_hamiltonian": value.rms_hamiltonian,
    }


def _m0_point_wire(value: StrainPointDiagnostic) -> _M0PointWire:
    return {
        "distinct_bond_lengths": value.distinct_bond_lengths,
        "first_passing_blocks": list(value.first_passing_blocks),
        "first_passing_radius": list(value.first_passing_radius),
        "maximum_bond_length": value.maximum_bond_length,
        "metric": _matrix_wire(value.metric),
        "minimum_bond_length": value.minimum_bond_length,
        "nyquist_power": value.nyquist_power,
        "ordinary_fourier_power": value.ordinary_fourier_power,
        "path_parameter": value.path_parameter,
        "restricted_alignment_residual": value.restricted_alignment_residual,
        "strain_fraction": value.strain_fraction,
    }


def _response_cutoff_wire(
    value: StrainResponseCutoffDiagnostic,
) -> _ResponseCutoffWire:
    return {
        "delta_omitted_power": value.delta_omitted_power,
        "delta_total": (
            None if value.delta_total is None else _error_wire(value.delta_total)
        ),
        "delta_truncation": (
            None
            if value.delta_truncation is None
            else _error_wire(value.delta_truncation)
        ),
        "omitted_power": value.omitted_power,
        "physical_radius": value.physical_radius,
        "retained_blocks": value.retained_blocks,
        "tail_tolerance": value.tail_tolerance,
        "total": None if value.total is None else _error_wire(value.total),
        "truncation": (
            None if value.truncation is None else _error_wire(value.truncation)
        ),
    }


def _response_point_wire(
    value: StrainResponsePointDiagnostic,
) -> _ResponsePointWire:
    return {
        "aligned_strain_perturbation": _error_wire(value.aligned_strain_perturbation),
        "cutoffs": [_response_cutoff_wire(item) for item in value.cutoffs],
        "delta_interpolation": _error_wire(value.delta_interpolation),
        "delta_nyquist_power": value.delta_nyquist_power,
        "delta_offsite_power": value.delta_offsite_power,
        "delta_onsite_power": value.delta_onsite_power,
        "interpolation": _error_wire(value.interpolation),
        "maximum_hopping_response": value.maximum_hopping_response,
        "maximum_parent_bond_length": value.maximum_parent_bond_length,
        "maximum_pointwise_frame_alignment_residual": (
            value.maximum_pointwise_frame_alignment_residual
        ),
        "maximum_scalar_strain_component": value.maximum_scalar_strain_component,
        "maximum_traceless_strain_component": (
            value.maximum_traceless_strain_component
        ),
        "metric": _matrix_wire(value.metric),
        "minimum_frame_overlap_singular_value": (
            value.minimum_frame_overlap_singular_value
        ),
        "minimum_hopping_response": value.minimum_hopping_response,
        "minimum_parent_bond_length": value.minimum_parent_bond_length,
        "minimum_sampled_external_isolation_gap": (
            value.minimum_sampled_external_isolation_gap
        ),
        "minimum_seed_overlap": value.minimum_seed_overlap,
        "nyquist_power": value.nyquist_power,
        "path_parameter": value.path_parameter,
        "restricted_global_frame_alignment_residual": (
            value.restricted_global_frame_alignment_residual
        ),
        "rms_scalar_strain_component": value.rms_scalar_strain_component,
        "rms_traceless_strain_component": value.rms_traceless_strain_component,
        "strain_fraction": value.strain_fraction,
    }


class SyntheticStrainResultSerializer:
    """Encode bounded M0 gauge-locality diagnostics as canonical JSON."""

    __slots__ = ()

    def execute(self, value: SyntheticStrainResult) -> CanonicalJsonDocument:
        """Return the explicit canonical M0 result document."""

        if type(value) is not SyntheticStrainResult:
            raise TypeError("value must be SyntheticStrainResult")
        wire: _M0ResultWire = {
            "construction_size": value.construction_size,
            "maximum_parseval_defect": value.maximum_parseval_defect,
            "maximum_rotation_amplitude": value.maximum_rotation_amplitude,
            "maximum_strain_invariance_defect": (
                value.maximum_strain_invariance_defect
            ),
            "path": value.path.value,
            "points": [_m0_point_wire(point) for point in value.points],
            "schema": M0_RESULT_SCHEMA_ID,
            "status": value.status,
            "tail_tolerances": list(value.tail_tolerances),
        }
        return _canonical_document(wire)


class SyntheticStrainResponseResultSerializer:
    """Encode bounded M1/M2 response diagnostics as canonical JSON."""

    __slots__ = ()

    def execute(self, value: SyntheticStrainResponseResult) -> CanonicalJsonDocument:
        """Return the explicit canonical M1 or M2 result document."""

        if type(value) is not SyntheticStrainResponseResult:
            raise TypeError("value must be SyntheticStrainResponseResult")
        schema = (
            M1_RESULT_SCHEMA_ID
            if value.model is StrainResponseModel.M1_FROZEN
            else M2_RESULT_SCHEMA_ID
        )
        wire: _ResponseResultWire = {
            "construction_size": value.construction_size,
            "evaluation_shift": value.evaluation_shift,
            "evaluation_size": value.evaluation_size,
            "maximum_rotation_amplitude": value.maximum_rotation_amplitude,
            "model": value.model.value,
            "path": value.path.value,
            "points": [_response_point_wire(point) for point in value.points],
            "radial_decay_beta": value.radial_decay_beta,
            "schema": schema,
            "status": value.status,
            "tail_tolerances": list(value.tail_tolerances),
        }
        return _canonical_document(wire)


__all__ = [
    "M0_RESULT_SCHEMA_ID",
    "M1_RESULT_SCHEMA_ID",
    "M2_RESULT_SCHEMA_ID",
    "SyntheticStrainResponseResultSerializer",
    "SyntheticStrainResultSerializer",
]
