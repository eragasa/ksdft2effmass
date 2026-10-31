"""Production ordinary-lattice truncation consequences for embedded rank two."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)

from ksdft2effmass.solidstate import (
    BlockHoppingInterpolationRequest1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncationRequest1D,
    BlockHoppingTruncator1D,
    CenteredEvenMeshCyclicToOrdinaryConverter1D,
    CenteredEvenMeshCyclicToOrdinaryRequest1D,
    CenteredUniformReciprocalMesh1D,
    GaugeAttack,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorFourierTransformRequest1D,
    ReciprocalOperatorSamples1D,
)

from ....gauge import Periodic1DRank2SinusoidalGaugeRotation
from ..parent_scale.analysis import (
    Periodic1DRank2Analyzer,
    _Periodic1DRank2PreparedAnalysis,
)
from ..parent_scale.frame_transport import (
    _Periodic1DRank2UnqualifiedPreparation,
)
from .request import Periodic1DRank2TruncationRequest
from .results import (
    Periodic1DRank2TruncationAnalysis,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationPoint,
    Periodic1DRank2TruncationQualificationStopped,
    Periodic1DRank2TruncationRange,
)


@dataclass(frozen=True, slots=True)
class _Errors:
    hamiltonian_maximum: float
    hamiltonian_rms: float
    spectral_maximum: float
    spectral_rms: float


@dataclass(frozen=True, slots=True)
class _ReferenceRange:
    maximum_range: int
    ordinary_omitted_power: float
    errors: _Errors


@dataclass(frozen=True, slots=True)
class _OrdinaryField:
    model: BlockHoppingModel1D
    nyquist_power: float
    maximum_hermiticity_defect: float


class Periodic1DRank2TruncationAnalyzer:
    """Qualify one parent, remove Nyquist, and evaluate ordinary cutoffs."""

    __slots__ = ("_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DRank2TruncationRequest,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not Periodic1DRank2TruncationRequest:
            raise TypeError("request must be a truncation request")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._transporter = transporter

    @property
    def request(self) -> Periodic1DRank2TruncationRequest:
        """Return the immutable constructor-bound request."""
        return self._request

    def execute(self) -> Periodic1DRank2TruncationAnalysis:
        """Return qualification stop or complete truncation consequences."""
        preparation = Periodic1DRank2Analyzer(
            request=self.request.template_request,
            transporter=self._transporter,
        )._prepare()
        if type(preparation) is _Periodic1DRank2UnqualifiedPreparation:
            return Periodic1DRank2TruncationQualificationStopped(
                request=self.request,
                qualification=preparation.qualification,
            )
        if type(preparation) is not _Periodic1DRank2PreparedAnalysis:
            raise TypeError("parent preparation returned an unknown variant")

        evaluation, offset = self._evaluation_coordinates()
        separation = self._minimum_periodic_separation(
            preparation.coordinates, evaluation
        )
        if separation <= np.finfo(np.float64).eps:
            raise FloatingPointError("construction and evaluation meshes overlap")
        reference = self._ordinary_field(
            preparation.coordinates,
            preparation.retained_matrices,
        )
        reference_full = self._interpolate(reference.model, evaluation)
        reference_eigenvalues = self._eigenvalues(reference_full)
        reference_ranges = tuple(
            self._reference_range(
                reference.model,
                evaluation,
                reference_full,
                reference_eigenvalues,
                maximum_range,
            )
            for maximum_range in self.request.maximum_ranges
        )
        points = tuple(
            self._point(
                preparation.coordinates,
                preparation.retained_matrices,
                evaluation,
                reference,
                reference_full,
                reference_eigenvalues,
                reference_ranges,
                amplitude,
            )
            for amplitude in self.request.template_request.amplitudes
        )
        return Periodic1DRank2TruncationCompleted(
            request=self.request,
            qualification=preparation.qualification,
            evaluation_coordinate_offset=offset,
            minimum_construction_evaluation_separation=separation,
            points=points,
        )

    def _point(
        self,
        construction_coordinates: Float64Array,
        construction_reference: Complex128Array,
        evaluation_coordinates: Float64Array,
        reference: _OrdinaryField,
        reference_full: Complex128Array,
        reference_eigenvalues: Float64Array,
        reference_ranges: tuple[_ReferenceRange, ...],
        amplitude: float,
    ) -> Periodic1DRank2TruncationPoint:
        gauge_attack = GaugeAttack(
            Periodic1DRank2SinusoidalGaugeRotation(amplitude),
            self.request.template_request.frame_absolute_tolerance,
        )
        construction_comparison = gauge_attack.apply(
            coordinates=construction_coordinates,
            represented_matrices=construction_reference,
        )
        comparison = self._ordinary_field(
            construction_coordinates, construction_comparison
        )
        comparison_full = self._interpolate(comparison.model, evaluation_coordinates)
        comparison_eigenvalues = self._eigenvalues(comparison_full)
        direct = gauge_attack.apply(
            coordinates=evaluation_coordinates,
            represented_matrices=reference_full,
        )
        direct_eigenvalues = self._eigenvalues(direct)
        interpolation = self._errors(
            comparison_full,
            direct,
            comparison_eigenvalues,
            direct_eigenvalues,
        )
        ranges = tuple(
            self._range(
                comparison.model,
                evaluation_coordinates,
                comparison_full,
                comparison_eigenvalues,
                direct,
                direct_eigenvalues,
                reference_range,
                reference.nyquist_power,
                comparison.nyquist_power,
            )
            for reference_range in reference_ranges
        )
        return Periodic1DRank2TruncationPoint(
            amplitude=amplitude,
            reference_nyquist_power=reference.nyquist_power,
            comparison_nyquist_power=comparison.nyquist_power,
            reference_ordinary_hermiticity_maximum_defect=(
                reference.maximum_hermiticity_defect
            ),
            comparison_ordinary_hermiticity_maximum_defect=(
                comparison.maximum_hermiticity_defect
            ),
            direct_spectral_maximum_defect=float(
                np.max(np.abs(direct_eigenvalues - reference_eigenvalues))
            ),
            comparison_interpolation_hamiltonian_maximum_error=(
                interpolation.hamiltonian_maximum
            ),
            comparison_interpolation_hamiltonian_rms_error=(
                interpolation.hamiltonian_rms
            ),
            comparison_interpolation_spectral_maximum_error=(
                interpolation.spectral_maximum
            ),
            comparison_interpolation_spectral_rms_error=(interpolation.spectral_rms),
            ranges=ranges,
        )

    def _reference_range(
        self,
        model: BlockHoppingModel1D,
        coordinates: Float64Array,
        complete: Complex128Array,
        complete_eigenvalues: Float64Array,
        maximum_range: int,
    ) -> _ReferenceRange:
        truncation = BlockHoppingTruncator1D(
            BlockHoppingTruncationRequest1D(model, maximum_range)
        ).execute()
        truncated = self._interpolate(truncation.truncated, coordinates)
        truncated_eigenvalues = self._eigenvalues(truncated)
        return _ReferenceRange(
            maximum_range=maximum_range,
            ordinary_omitted_power=float(truncation.omitted_block_l2_norm**2 / 2.0),
            errors=self._errors(
                truncated,
                complete,
                truncated_eigenvalues,
                complete_eigenvalues,
            ),
        )

    def _range(
        self,
        model: BlockHoppingModel1D,
        coordinates: Float64Array,
        complete: Complex128Array,
        complete_eigenvalues: Float64Array,
        direct: Complex128Array,
        direct_eigenvalues: Float64Array,
        reference: _ReferenceRange,
        reference_nyquist_power: float,
        comparison_nyquist_power: float,
    ) -> Periodic1DRank2TruncationRange:
        truncation = BlockHoppingTruncator1D(
            BlockHoppingTruncationRequest1D(model, reference.maximum_range)
        ).execute()
        truncated = self._interpolate(truncation.truncated, coordinates)
        truncated_eigenvalues = self._eigenvalues(truncated)
        truncation_errors = self._errors(
            truncated,
            complete,
            truncated_eigenvalues,
            complete_eigenvalues,
        )
        total_errors = self._errors(
            truncated,
            direct,
            truncated_eigenvalues,
            direct_eigenvalues,
        )
        comparison_ordinary_power = float(truncation.omitted_block_l2_norm**2 / 2.0)
        return Periodic1DRank2TruncationRange(
            maximum_range=reference.maximum_range,
            reference_ordinary_omitted_power=reference.ordinary_omitted_power,
            comparison_ordinary_omitted_power=comparison_ordinary_power,
            reference_total_omitted_power=(
                reference.ordinary_omitted_power + reference_nyquist_power
            ),
            comparison_total_omitted_power=(
                comparison_ordinary_power + comparison_nyquist_power
            ),
            reference_truncation_hamiltonian_maximum_error=(
                reference.errors.hamiltonian_maximum
            ),
            reference_truncation_hamiltonian_rms_error=(
                reference.errors.hamiltonian_rms
            ),
            reference_truncation_spectral_maximum_error=(
                reference.errors.spectral_maximum
            ),
            reference_truncation_spectral_rms_error=(reference.errors.spectral_rms),
            comparison_truncation_hamiltonian_maximum_error=(
                truncation_errors.hamiltonian_maximum
            ),
            comparison_truncation_hamiltonian_rms_error=(
                truncation_errors.hamiltonian_rms
            ),
            comparison_truncation_spectral_maximum_error=(
                truncation_errors.spectral_maximum
            ),
            comparison_truncation_spectral_rms_error=(truncation_errors.spectral_rms),
            comparison_total_hamiltonian_maximum_error=(
                total_errors.hamiltonian_maximum
            ),
            comparison_total_hamiltonian_rms_error=total_errors.hamiltonian_rms,
            comparison_total_spectral_maximum_error=total_errors.spectral_maximum,
            comparison_total_spectral_rms_error=total_errors.spectral_rms,
        )

    def _ordinary_field(
        self, coordinates: Float64Array, matrices: Complex128Array
    ) -> _OrdinaryField:
        unit = Unitless()
        period = ScalarQuantity(1.0, unit)
        mesh = CenteredUniformReciprocalMesh1D(period, coordinates.size)
        if not np.allclose(
            mesh.coordinates.magnitude,
            coordinates,
            rtol=0.0,
            atol=self.request.template_request.frame_absolute_tolerance,
        ):
            raise ValueError("construction coordinates differ from the declared mesh")
        transform = ReciprocalOperatorFourierTransformer1D(
            ReciprocalOperatorFourierTransformRequest1D(
                source=ReciprocalOperatorSamples1D(
                    coordinates=mesh.coordinates,
                    reciprocal_period=period,
                    matrices=tuple(
                        ComplexMatrixQuantity(matrix, unit) for matrix in matrices
                    ),
                ),
                mesh=mesh,
                coordinate_absolute_tolerance=(
                    self.request.template_request.frame_absolute_tolerance
                ),
                reconstruction_absolute_tolerance=(
                    self.request.template_request.frame_absolute_tolerance
                ),
            )
        ).execute()
        conversion = CenteredEvenMeshCyclicToOrdinaryConverter1D(
            CenteredEvenMeshCyclicToOrdinaryRequest1D(transform.hopping_model)
        ).execute()
        defect = self._maximum_hermiticity_defect(conversion.ordinary)
        tolerance = self.request.template_request.frame_absolute_tolerance
        if defect > tolerance:
            raise FloatingPointError("ordinary hopping model is not Hermitian")
        return _OrdinaryField(
            model=conversion.ordinary,
            nyquist_power=conversion.conversion_power_per_matrix_dimension,
            maximum_hermiticity_defect=defect,
        )

    @staticmethod
    def _interpolate(
        model: BlockHoppingModel1D, coordinates: Float64Array
    ) -> Complex128Array:
        result = BlockHoppingInterpolator1D(
            BlockHoppingInterpolationRequest1D(
                model=model,
                coordinates=VectorQuantity(coordinates, model.reciprocal_period.unit),
            )
        ).execute()
        return np.asarray(
            [matrix.magnitude for matrix in result.matrices], dtype=np.complex128
        )

    @staticmethod
    def _maximum_hermiticity_defect(model: BlockHoppingModel1D) -> float:
        blocks = {
            representative: block.magnitude
            for representative, block in zip(
                model.representatives, model.hopping_blocks, strict=True
            )
        }
        if any(-representative not in blocks for representative in blocks):
            raise ValueError("ordinary hopping inventory is not conjugate closed")
        return float(
            max(
                np.linalg.norm(block - blocks[-representative].conj().T)
                for representative, block in blocks.items()
            )
        )

    @staticmethod
    def _errors(
        candidate: Complex128Array,
        reference: Complex128Array,
        candidate_eigenvalues: Float64Array,
        reference_eigenvalues: Float64Array,
    ) -> _Errors:
        matrix_difference = candidate - reference
        spectral_difference = candidate_eigenvalues - reference_eigenvalues
        if matrix_difference.shape[0] == 0:
            raise ValueError("error evaluation requires at least one point")
        matrix_powers = np.sum(np.abs(matrix_difference) ** 2, axis=(1, 2))
        matrix_norms = np.sqrt(matrix_powers)
        spectral_maximum = float(np.max(np.abs(spectral_difference)))
        frobenius_maximum = float(np.max(matrix_norms))
        bound_tolerance = (
            32.0
            * np.finfo(np.float64).eps
            * max(1.0, spectral_maximum, frobenius_maximum)
        )
        if spectral_maximum > frobenius_maximum + bound_tolerance:
            raise FloatingPointError("spectral error exceeds the Frobenius bound")
        return _Errors(
            hamiltonian_maximum=frobenius_maximum / math.sqrt(2.0),
            hamiltonian_rms=math.sqrt(float(np.mean(matrix_powers)) / 2.0),
            spectral_maximum=spectral_maximum,
            spectral_rms=math.sqrt(float(np.mean(np.square(spectral_difference)))),
        )

    @staticmethod
    def _eigenvalues(matrices: Complex128Array) -> Float64Array:
        return np.asarray(np.linalg.eigvalsh(matrices), dtype=np.float64)

    def _evaluation_coordinates(self) -> tuple[Float64Array, float]:
        construction_size = self.request.template_request.reciprocal_mesh_size
        evaluation_size = self.request.evaluation_mesh_size
        offset = 1.0 / float(construction_size + 1)
        values = -0.5 + (np.arange(evaluation_size, dtype=np.float64) + offset) / float(
            evaluation_size
        )
        values.setflags(write=False)
        return values, offset

    @staticmethod
    def _minimum_periodic_separation(
        construction: Float64Array, evaluation: Float64Array
    ) -> float:
        differences = np.abs(evaluation[:, None] - construction[None, :])
        wrapped = np.minimum(differences, 1.0 - differences)
        return float(np.min(wrapped))


__all__ = ["Periodic1DRank2TruncationAnalyzer"]
