"""Finite-periodic Fourier analysis for one gauge alignment."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import final

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array, Int64Array
from projectkoios.numerics.numpy.validation import (
    NumpyImmutableArrayConstructor,
    NumpyImmutableArrayValidator,
)
from projectkoios.physkit.solidstate.tb import (
    FinitePeriodicMatrixFourierTensorEvaluator,
    FinitePeriodicMatrixFourierTransformer,
    FinitePeriodicMatrixFourierTransformResult,
    FinitePeriodicMatrixHermiticityAnalyzer,
    FinitePeriodicMatrixParsevalAnalyzer,
    FinitePeriodicMatrixSamples,
)
from projectkoios.physkit.units import Unitless

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    FourierMatrixBlockNormInventoryAnalyzer1D,
    MatrixFieldErrorAnalyzer,
)
from ksdft2effmass.numerical_consistency import NumericalConsistency

from ..band_alignment.composite.diagnostics import Periodic1DRankNMatrixErrorResult
from .nyquist import NyquistModeDispositionEnum
from .request import Periodic1DRankNGaugeAlignmentAnalysisRequest


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNFourierAnalysisRequest:
    """Bind one complete gauge-alignment request for Fourier analysis."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError(
                "analysis_request must be the exact gauge-alignment request"
            )


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DRankNFourierAnalysis(NumericalConsistency):
    """Store Fourier coefficients and their structural diagnostics."""

    analysis_request: Periodic1DRankNGaugeAlignmentAnalysisRequest
    transform: FinitePeriodicMatrixFourierTransformResult
    representative_count: int
    representative_inventory_ordered_unique: bool
    inversion_closed: bool
    index_bijection_pass: bool
    nyquist_mode_disposition: NyquistModeDispositionEnum
    coefficient_translations: Int64Array
    block_raw_frobenius_norms: Float64Array
    block_normalized_frobenius_norms: Float64Array
    reconstruction: Periodic1DRankNMatrixErrorResult
    reconstruction_pass: bool
    parseval_relative_defect: float
    parseval_pass: bool
    ordinary_hermiticity_defect: float
    ordinary_hermiticity_pass: bool
    twisted_cyclic_hermiticity_defect: float
    twisted_cyclic_hermiticity_pass: bool

    def __post_init__(self) -> None:
        if (
            type(self.analysis_request)
            is not Periodic1DRankNGaugeAlignmentAnalysisRequest
        ):
            raise TypeError("analysis_request must be the exact analysis request")
        if type(self.transform) is not FinitePeriodicMatrixFourierTransformResult:
            raise TypeError("transform must be the exact PhysKit transform result")
        if type(self.representative_count) is not int:
            raise TypeError("representative_count must be a built-in integer")
        for value, name in (
            (
                self.representative_inventory_ordered_unique,
                "representative_inventory_ordered_unique",
            ),
            (self.inversion_closed, "inversion_closed"),
            (self.index_bijection_pass, "index_bijection_pass"),
            (self.reconstruction_pass, "reconstruction_pass"),
            (self.parseval_pass, "parseval_pass"),
            (self.ordinary_hermiticity_pass, "ordinary_hermiticity_pass"),
            (
                self.twisted_cyclic_hermiticity_pass,
                "twisted_cyclic_hermiticity_pass",
            ),
        ):
            if type(value) is not bool:
                raise TypeError(f"{name} must be a built-in bool")
        if type(self.nyquist_mode_disposition) is not NyquistModeDispositionEnum:
            raise TypeError("nyquist_mode_disposition must be the exact enum")
        translations = NumpyImmutableArrayValidator(
            self.coefficient_translations,
            "coefficient_translations",
            np.dtype(np.int64),
        ).execute()
        raw_norms = NumpyImmutableArrayValidator(
            self.block_raw_frobenius_norms,
            "block_raw_frobenius_norms",
            np.dtype(np.float64),
        ).execute()
        normalized_norms = NumpyImmutableArrayValidator(
            self.block_normalized_frobenius_norms,
            "block_normalized_frobenius_norms",
            np.dtype(np.float64),
        ).execute()
        if (
            translations.ndim != 1
            or raw_norms.shape != translations.shape
            or normalized_norms.shape != translations.shape
        ):
            raise ValueError("Fourier block inventories must have one vector shape")
        if type(self.reconstruction) is not Periodic1DRankNMatrixErrorResult:
            raise TypeError("reconstruction must be the exact matrix-error record")


@final
class Periodic1DRankNFourierAnalyzer:
    """Transform one represented-operator field and test Fourier identities."""

    __slots__ = ("_request",)

    def __init__(
        self,
        *,
        request: Periodic1DRankNFourierAnalysisRequest,
    ) -> None:
        if type(request) is not Periodic1DRankNFourierAnalysisRequest:
            raise TypeError("request must be Periodic1DRankNFourierAnalysisRequest")
        self._request = request

    @property
    def request(self) -> Periodic1DRankNFourierAnalysisRequest:
        """Return the exact Fourier-analysis request bound to this action."""
        return self._request

    def execute(self) -> Periodic1DRankNFourierAnalysis:
        """Return Fourier coefficients and structural diagnostics."""
        analysis_request = self._request.analysis_request
        calculation_request = analysis_request.calculation_request
        controls = calculation_request.controls
        model = analysis_request.model
        coordinates = analysis_request.aligned_fields.coordinates
        represented_operators = analysis_request.aligned_fields.represented_operators
        source = FinitePeriodicMatrixSamples.from_array(
            mesh=analysis_request.mesh,
            matrix_samples=represented_operators,
            energy_unit=Unitless(),
            energy_reference=calculation_request.energy_reference_identifier,
            basis_identifier=calculation_request.represented_basis_identifier,
        )
        transform = FinitePeriodicMatrixFourierTransformer(source=source).result()
        integer_modes = np.asarray(transform.series.integer_modes[:, 0], dtype=np.int64)
        expected_modes = np.arange(
            -(analysis_request.mesh.size // 2),
            analysis_request.mesh.size // 2 + 1,
            dtype=np.int64,
        )
        mode_inventory = {int(value) for value in integer_modes}
        representative_inventory_ordered_unique = bool(
            np.array_equal(integer_modes, expected_modes)
        )
        inversion_closed = mode_inventory == {-value for value in mode_inventory}
        index_bijection_pass = (
            np.unique(np.mod(integer_modes, analysis_request.mesh.size)).size
            == analysis_request.mesh.size
        )
        reconstruction_values = (
            FinitePeriodicMatrixFourierTensorEvaluator(
                series=transform.series,
                coordinate_axes=(coordinates,),
                maximum_working_elements=controls.maximum_working_elements,
            )
            .result()
            .matrix_values
        )
        reconstruction_diagnostics = MatrixFieldErrorAnalyzer(
            approximation=reconstruction_values,
            reference=represented_operators,
            norm_energy_scale=controls.energy_reference,
        ).result()
        reconstruction = Periodic1DRankNMatrixErrorResult.from_diagnostics(
            reconstruction_diagnostics
        )
        parseval = FinitePeriodicMatrixParsevalAnalyzer(transform=transform).result()
        parseval_scale = max(
            parseval.sample_mean_squared_frobenius_norm.magnitude,
            controls.saturation_denominator_floor,
        )
        parseval_relative_defect = parseval.absolute_defect.magnitude / parseval_scale
        hermiticity = FinitePeriodicMatrixHermiticityAnalyzer(
            transform=transform
        ).result()
        normalization = math.sqrt(model.retained_rank) * controls.energy_reference
        ordinary_hermiticity_defect = (
            hermiticity.ordinary_maximum_frobenius_defect.magnitude / normalization
        )
        twisted_cyclic_hermiticity_defect = (
            hermiticity.twisted_cyclic_maximum_frobenius_defect.magnitude
            / normalization
        )
        blocks = FourierMatrixBlockNormInventoryAnalyzer1D().execute(
            transform.series,
            controls.maximum_recorded_block_range,
            controls.energy_reference,
        )
        return Periodic1DRankNFourierAnalysis(
            analysis_request=analysis_request,
            transform=transform,
            representative_count=transform.series.term_count,
            representative_inventory_ordered_unique=(
                representative_inventory_ordered_unique
            ),
            inversion_closed=inversion_closed,
            index_bijection_pass=index_bijection_pass,
            nyquist_mode_disposition=(NyquistModeDispositionEnum.ABSENT_ON_ODD_MESH),
            coefficient_translations=NumpyImmutableArrayConstructor(
                np.asarray(
                    [block.translation for block in blocks.blocks],
                    dtype=np.int64,
                ),
                "coefficient_translations",
                np.dtype(np.int64),
            ).execute(),
            block_raw_frobenius_norms=NumpyImmutableArrayConstructor(
                np.asarray(
                    [block.raw_frobenius_norm for block in blocks.blocks],
                    dtype=np.float64,
                ),
                "block_raw_frobenius_norms",
                np.dtype(np.float64),
            ).execute(),
            block_normalized_frobenius_norms=NumpyImmutableArrayConstructor(
                np.asarray(
                    [block.normalized_frobenius_norm for block in blocks.blocks],
                    dtype=np.float64,
                ),
                "block_normalized_frobenius_norms",
                np.dtype(np.float64),
            ).execute(),
            reconstruction=reconstruction,
            reconstruction_pass=(
                reconstruction.normalized_matrix_frobenius_maximum
                <= controls.fourier_consistency_tolerance
            ),
            parseval_relative_defect=parseval_relative_defect,
            parseval_pass=(
                parseval_relative_defect <= controls.fourier_consistency_tolerance
            ),
            ordinary_hermiticity_defect=ordinary_hermiticity_defect,
            ordinary_hermiticity_pass=(
                ordinary_hermiticity_defect <= controls.fourier_consistency_tolerance
            ),
            twisted_cyclic_hermiticity_defect=twisted_cyclic_hermiticity_defect,
            twisted_cyclic_hermiticity_pass=(
                twisted_cyclic_hermiticity_defect
                <= controls.fourier_consistency_tolerance
            ),
        )


__all__ = [
    "Periodic1DRankNFourierAnalysis",
    "Periodic1DRankNFourierAnalysisRequest",
    "Periodic1DRankNFourierAnalyzer",
]
