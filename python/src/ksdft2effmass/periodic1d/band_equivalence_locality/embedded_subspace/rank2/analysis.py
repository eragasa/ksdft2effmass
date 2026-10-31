"""Analyze the qualified nonflat embedded-subspace rank-two parent."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.numpy.typing import Complex128Array, Float64Array
from projectkoios.optimization.selection.harmonic import (
    PeriodicHarmonic,
    PeriodicHarmonicMaximizer,
    PeriodicHarmonicMaximum,
)
from projectkoios.physkit.solidstate.electronic.frame_transport import (
    ClosedLoopPolarFrameTransporter,
)

from ksdft2effmass.solidstate import GaugeAttack

from ...gauge import Periodic1DRank2SinusoidalGaugeRotation
from .locality import (
    _Periodic1DCyclicHoppingPower,
    _Periodic1DCyclicHoppingPowerAnalyzer,
)
from .parent import _Periodic1DEmbeddedSubspaceRank2ParentConstructor
from .request import Periodic1DEmbeddedSubspaceRank2Request
from .results import (
    Periodic1DEmbeddedSubspaceRank2Analysis,
    Periodic1DEmbeddedSubspaceRank2HoppingPower,
    Periodic1DEmbeddedSubspaceRank2PointAnalysis,
    Periodic1DEmbeddedSubspaceRank2QualifiedParent,
)
from .transport import (
    _Periodic1DEmbeddedSubspaceRank2ParentQualifier,
    _Periodic1DEmbeddedSubspaceRank2QualifiedPreparation,
    _Periodic1DEmbeddedSubspaceRank2UnqualifiedPreparation,
)


@dataclass(frozen=True, slots=True)
class _Periodic1DEmbeddedSubspaceRank2PreparedAnalysis:
    """Own one qualified parent preparation for direct amplitude evaluation."""

    analyzer: Periodic1DEmbeddedSubspaceRank2Analyzer
    coordinates: Float64Array
    retained_matrices: Complex128Array
    traceless_matrices: Complex128Array
    mean_energies: Float64Array
    splitting_scale: float
    qualification: Periodic1DEmbeddedSubspaceRank2QualifiedParent
    reference_powers: tuple[_Periodic1DCyclicHoppingPower, ...]
    reference_nonzero_hopping_weight: float
    reference_parseval_defect: float

    def point(self, amplitude: float) -> Periodic1DEmbeddedSubspaceRank2PointAnalysis:
        """Evaluate one direct gauge-attack amplitude on the prepared parent."""
        return self.analyzer._point(
            coordinates=self.coordinates,
            retained=self.retained_matrices,
            traceless=self.traceless_matrices,
            means=self.mean_energies,
            splitting_scale=self.splitting_scale,
            reference_powers=self.reference_powers,
            reference_nonzero=self.reference_nonzero_hopping_weight,
            reference_parseval_defect=self.reference_parseval_defect,
            amplitude=amplitude,
        )


class Periodic1DEmbeddedSubspaceRank2Analyzer:
    """Analyze gauge-locality effects after explicit parent qualification."""

    __slots__ = ("_harmonic_maximizer", "_request", "_transporter")

    def __init__(
        self,
        *,
        request: Periodic1DEmbeddedSubspaceRank2Request,
        transporter: ClosedLoopPolarFrameTransporter,
    ) -> None:
        if type(request) is not Periodic1DEmbeddedSubspaceRank2Request:
            raise TypeError("request must be Periodic1DEmbeddedSubspaceRank2Request")
        if type(transporter) is not ClosedLoopPolarFrameTransporter:
            raise TypeError("transporter must be ClosedLoopPolarFrameTransporter")
        self._request = request
        self._transporter = transporter
        self._harmonic_maximizer = PeriodicHarmonicMaximizer(
            absolute_degeneracy_tolerance=(
                request.harmonic_absolute_degeneracy_tolerance
            ),
            relative_degeneracy_tolerance=(
                request.harmonic_relative_degeneracy_tolerance
            ),
        )

    @property
    def request(self) -> Periodic1DEmbeddedSubspaceRank2Request:
        """Return the immutable constructor-bound request."""
        return self._request

    def execute(self) -> Periodic1DEmbeddedSubspaceRank2Analysis:
        """Construct, qualify, and analyze the exact embedded-subspace/rank2 parent."""
        preparation = self._prepare()
        if type(preparation) is _Periodic1DEmbeddedSubspaceRank2UnqualifiedPreparation:
            return Periodic1DEmbeddedSubspaceRank2Analysis(
                request=self.request,
                qualification=preparation.qualification,
                points=(),
            )
        if type(preparation) is not _Periodic1DEmbeddedSubspaceRank2PreparedAnalysis:
            raise TypeError("analysis preparation returned an unknown variant")
        return Periodic1DEmbeddedSubspaceRank2Analysis(
            request=self.request,
            qualification=preparation.qualification,
            points=tuple(
                preparation.point(amplitude) for amplitude in self.request.amplitudes
            ),
        )

    def _prepare(
        self,
    ) -> (
        _Periodic1DEmbeddedSubspaceRank2PreparedAnalysis
        | _Periodic1DEmbeddedSubspaceRank2UnqualifiedPreparation
    ):
        parent = _Periodic1DEmbeddedSubspaceRank2ParentConstructor(
            self.request
        ).execute()
        preparation = _Periodic1DEmbeddedSubspaceRank2ParentQualifier(
            request=self.request,
            parent=parent,
            transporter=self._transporter,
        ).execute()
        if type(preparation) is _Periodic1DEmbeddedSubspaceRank2UnqualifiedPreparation:
            return preparation
        if (
            type(preparation)
            is not _Periodic1DEmbeddedSubspaceRank2QualifiedPreparation
        ):
            raise TypeError("parent qualifier returned an unknown preparation variant")
        reference_powers = self._hopping_power_analyzer(
            coordinates=parent.coordinates,
            matrices=preparation.retained_matrices,
        ).execute()
        reference_nonzero = math.fsum(
            item.normalized_squared_frobenius_norm
            for item in reference_powers
            if item.displacement != 0
        )
        return _Periodic1DEmbeddedSubspaceRank2PreparedAnalysis(
            analyzer=self,
            coordinates=parent.coordinates,
            retained_matrices=preparation.retained_matrices,
            traceless_matrices=preparation.traceless_matrices,
            mean_energies=preparation.mean_energies,
            splitting_scale=preparation.splitting_scale,
            qualification=preparation.qualification,
            reference_powers=reference_powers,
            reference_nonzero_hopping_weight=reference_nonzero,
            reference_parseval_defect=self._parseval_defect(
                preparation.retained_matrices,
                reference_powers,
            ),
        )

    def _point(
        self,
        *,
        coordinates: Float64Array,
        retained: Complex128Array,
        traceless: Complex128Array,
        means: Float64Array,
        splitting_scale: float,
        reference_powers: tuple[_Periodic1DCyclicHoppingPower, ...],
        reference_nonzero: float,
        reference_parseval_defect: float,
        amplitude: float,
    ) -> Periodic1DEmbeddedSubspaceRank2PointAnalysis:
        rotation = Periodic1DRank2SinusoidalGaugeRotation(amplitude)
        comparison = GaugeAttack(
            rotation,
            self.request.frame_absolute_tolerance,
        ).apply(
            coordinates=coordinates,
            represented_matrices=retained,
        )
        band_defect = float(
            np.max(
                np.abs(np.linalg.eigvalsh(comparison) - np.linalg.eigvalsh(retained))
            )
        )
        comparison_traceless = comparison - means[:, None, None] * np.eye(
            2, dtype=np.complex128
        )
        maximum, correlation = self._restricted_alignment(
            traceless,
            comparison_traceless,
            splitting_scale,
        )
        if amplitude == 0.0:
            # The declared gauge attack is exactly the identity at zero amplitude.
            correlation = 1.0
        optimal_scale = max(0.0, correlation)
        minimum_squared_loss = splitting_scale * (1.0 - optimal_scale**2)
        operator_threshold = math.sqrt(max(0.0, minimum_squared_loss))
        joint_threshold = math.sqrt(
            max(0.0, 2.0 * splitting_scale * (1.0 - correlation))
        )
        reconstructed_loss = self._reconstructed_loss(
            means=means,
            traceless=traceless,
            comparison=comparison,
            optimal_scale=optimal_scale,
            angle=maximum.canonical_maximizing_argument or 0.0,
        )
        comparison_powers = self._hopping_power_analyzer(
            coordinates=coordinates,
            matrices=comparison,
        ).execute()
        powers = self._paired_powers(reference_powers, comparison_powers)
        comparison_nonzero = math.fsum(
            item.comparison_normalized_squared_frobenius_norm
            for item in powers
            if item.displacement != 0
        )
        return Periodic1DEmbeddedSubspaceRank2PointAnalysis(
            amplitude=amplitude,
            maximum_band_defect=band_defect,
            splitting_scale=splitting_scale,
            harmonic_maximum=maximum,
            discrete_maximum_correlation=correlation,
            minimum_operator_threshold=operator_threshold,
            exact_spectrum_joint_operator_threshold=joint_threshold,
            minimum_loss_reconstruction_defect=abs(
                reconstructed_loss - minimum_squared_loss
            ),
            reference_nonzero_hopping_weight=reference_nonzero,
            comparison_nonzero_hopping_weight=comparison_nonzero,
            reference_parseval_defect=reference_parseval_defect,
            comparison_parseval_defect=self._parseval_defect(
                comparison,
                comparison_powers,
            ),
            hopping_powers=powers,
        )

    def _hopping_power_analyzer(
        self,
        *,
        coordinates: Float64Array,
        matrices: Complex128Array,
    ) -> _Periodic1DCyclicHoppingPowerAnalyzer:
        return _Periodic1DCyclicHoppingPowerAnalyzer(
            coordinates=coordinates,
            matrices=matrices,
            coordinate_absolute_tolerance=self.request.frame_absolute_tolerance,
            reconstruction_absolute_tolerance=self.request.frame_absolute_tolerance,
        )

    def _restricted_alignment(
        self,
        reference: Complex128Array,
        comparison: Complex128Array,
        splitting_scale: float,
    ) -> tuple[PeriodicHarmonicMaximum, float]:
        maximum = self._harmonic_maximizer.maximize(
            self._correlation_harmonic(reference, comparison)
        )
        correlation = maximum.maximum_value / splitting_scale
        roundoff_bound = 32.0 * np.finfo(np.float64).eps
        if correlation > 1.0:
            if correlation - 1.0 > roundoff_bound:
                raise FloatingPointError("maximum correlation exceeds one")
            correlation = 1.0
        elif correlation < -1.0:
            if -1.0 - correlation > roundoff_bound:
                raise FloatingPointError("maximum correlation is below minus one")
            correlation = -1.0
        return maximum, float(correlation)

    @staticmethod
    def _reconstructed_loss(
        *,
        means: Float64Array,
        traceless: Complex128Array,
        comparison: Complex128Array,
        optimal_scale: float,
        angle: float,
    ) -> float:
        global_rotation = np.asarray(
            [
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)],
            ],
            dtype=np.complex128,
        )
        aligned = global_rotation.conj().T @ traceless @ global_rotation
        candidate = (
            means[:, None, None] * np.eye(2, dtype=np.complex128)
            + optimal_scale * aligned
        )
        return float(
            np.mean(np.sum(np.abs(candidate - comparison) ** 2, axis=(1, 2))) / 2.0
        )

    @staticmethod
    def _paired_powers(
        reference: tuple[_Periodic1DCyclicHoppingPower, ...],
        comparison: tuple[_Periodic1DCyclicHoppingPower, ...],
    ) -> tuple[Periodic1DEmbeddedSubspaceRank2HoppingPower, ...]:
        if tuple(item.displacement for item in reference) != tuple(
            item.displacement for item in comparison
        ):
            raise ValueError("reference and comparison hopping inventories differ")
        return tuple(
            Periodic1DEmbeddedSubspaceRank2HoppingPower(
                displacement=reference_item.displacement,
                reference_normalized_squared_frobenius_norm=(
                    reference_item.normalized_squared_frobenius_norm
                ),
                comparison_normalized_squared_frobenius_norm=(
                    comparison_item.normalized_squared_frobenius_norm
                ),
            )
            for reference_item, comparison_item in zip(
                reference,
                comparison,
                strict=True,
            )
        )

    @staticmethod
    def _parseval_defect(
        matrices: Complex128Array,
        powers: tuple[_Periodic1DCyclicHoppingPower, ...],
    ) -> float:
        reciprocal_power = float(
            np.mean(np.sum(np.abs(matrices) ** 2, axis=(1, 2))) / 2.0
        )
        return abs(
            reciprocal_power
            - math.fsum(item.normalized_squared_frobenius_norm for item in powers)
        )

    @staticmethod
    def _correlation_harmonic(
        reference: Complex128Array,
        comparison: Complex128Array,
    ) -> PeriodicHarmonic:
        x_value = reference[:, 0, 1].real
        y_value = -reference[:, 0, 1].imag
        z_value = 0.5 * (reference[:, 0, 0].real - reference[:, 1, 1].real)
        target_x = comparison[:, 0, 1].real
        target_y = -comparison[:, 0, 1].imag
        target_z = 0.5 * (comparison[:, 0, 0].real - comparison[:, 1, 1].real)
        return PeriodicHarmonic(
            offset=float(np.mean(y_value * target_y)),
            cosine_coefficient=float(np.mean(x_value * target_x + z_value * target_z)),
            sine_coefficient=float(np.mean(x_value * target_z - z_value * target_x)),
            harmonic_order=2,
            fundamental_interval_start=-math.pi / 2.0,
        )


__all__ = ["Periodic1DEmbeddedSubspaceRank2Analyzer"]
