"""Mesh coordinates, statuses, and unavailable gauge-alignment results."""

from __future__ import annotations

import numpy as np
from projectkoios.numerics.numpy.validation import NumpyImmutableArrayConstructor
from projectkoios.physkit.numerics.typing.numpy.arrays import RealArray

from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationRequest,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.definition import (
    Periodic1DRankNGaugeAlignment,
)
from ksdft2effmass.periodic1d.rankN.gauge_alignment.status import (
    Periodic1DRankNAlignmentBackendExceptionCode,
    Periodic1DRankNAlignmentStatus,
    Periodic1DRankNAlignmentStatusResult,
    _alignment_status_result,
)

from ..result import Periodic1DRankNGaugeAlignmentMeshResult


def _coordinates(mesh_size: int, offset: float) -> RealArray:
    values = np.asarray(
        -0.5 + (np.arange(mesh_size, dtype=np.float64) + offset) / mesh_size,
        dtype=np.float64,
    )
    return NumpyImmutableArrayConstructor(
        values,
        "coordinates",
        np.dtype(np.float64),
    ).execute()


def _status(
    request: Periodic1DRankNAlignmentCalculationRequest,
    mesh_size: int,
    gauge_alignment: Periodic1DRankNGaugeAlignment,
    status: Periodic1DRankNAlignmentStatus,
    backend_exception_code: (
        Periodic1DRankNAlignmentBackendExceptionCode | None
    ) = None,
) -> Periodic1DRankNAlignmentStatusResult:
    return _alignment_status_result(
        case_identity=request.case_identity,
        retained_rank=request.retained_rank,
        circuit_depth=request.circuit_depth,
        construction_mesh_size=mesh_size,
        gauge_alignment=gauge_alignment,
        status=status,
        backend_exception_code=backend_exception_code,
    )


def _unavailable_gauge_alignment_result(
    status: Periodic1DRankNAlignmentStatusResult,
) -> Periodic1DRankNGaugeAlignmentMeshResult:
    return Periodic1DRankNGaugeAlignmentMeshResult(
        status=status,
        transform_backend_identifier=None,
        transform_backend_version=None,
        fourier_representative_count=None,
        fourier_representative_inventory_ordered_unique=None,
        fourier_inversion_closed=None,
        fourier_index_bijection_pass=None,
        nyquist_mode_disposition=None,
        coefficient_translations=np.empty(0, dtype=np.int64),
        block_raw_frobenius_norms=np.empty(0, dtype=np.float64),
        block_normalized_frobenius_norms=np.empty(0, dtype=np.float64),
        frame_recovery=None,
        known_frame_recovery_pass=None,
        represented_operator_recovery=None,
        known_operator_recovery_pass=None,
        reconstruction=None,
        reconstruction_pass=None,
        interpolation=None,
        final_interpolation_operator_pass=None,
        final_interpolation_spectrum_pass=None,
        parseval_relative_defect=None,
        parseval_pass=None,
        ordinary_hermiticity_defect=None,
        ordinary_hermiticity_pass=None,
        twisted_cyclic_hermiticity_defect=None,
        twisted_cyclic_hermiticity_pass=None,
        supports=(),
        maximum_tail_increase=None,
        all_tail_monotonicity_checks_pass=None,
    )
