"""Independent scientific verification for one embedded rank-two parent scale."""

from __future__ import annotations

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from .qualification_verification import (
    Periodic1DRank2QualificationVerificationAssessor,
)
from .results import Periodic1DRank2Analysis


class EmbeddedSubspaceRank2Verification(CompositeVerification):
    """Group independent parent, transport, alignment, and locality comparisons."""


class Periodic1DRank2AnalysisVerificationAssessor:
    """Compare one observed analysis with its independent reconstruction."""

    __slots__ = ("_observed", "_reference")

    def __init__(
        self,
        observed: Periodic1DRank2Analysis,
        reference: Periodic1DRank2Analysis,
    ) -> None:
        if type(observed) is not Periodic1DRank2Analysis:
            raise TypeError("observed must be an embedded rank-two analysis")
        if type(reference) is not Periodic1DRank2Analysis:
            raise TypeError("reference must be an embedded rank-two analysis")
        self._observed = observed
        self._reference = reference

    def assess(self) -> EmbeddedSubspaceRank2Verification:
        """Return independent analysis discrepancies."""
        observed = self._observed
        reference = self._reference
        if observed.request != reference.request:
            raise ValueError(
                "independent reference request does not match subject request"
            )
        tolerance = observed.request.verification_absolute_tolerance
        observations = dict(
            Periodic1DRank2QualificationVerificationAssessor(
                observed=observed.qualification,
                reference=reference.qualification,
                tolerance=tolerance,
            )
            .assess()
            .observations
        )
        observed_inventory = tuple(point.amplitude for point in observed.points)
        reference_inventory = tuple(point.amplitude for point in reference.points)
        observations["point_inventory_defect"] = VerificationObservation.dimensionless(
            float(observed_inventory != reference_inventory),
            0.0,
        )
        if observed_inventory != reference_inventory or not observed.points:
            return EmbeddedSubspaceRank2Verification(observations)

        scalar_names = (
            "maximum_band_defect",
            "splitting_scale",
            "discrete_maximum_correlation",
            "minimum_operator_threshold",
            "exact_spectrum_joint_operator_threshold",
            "minimum_loss_reconstruction_defect",
            "reference_nonzero_hopping_weight",
            "comparison_nonzero_hopping_weight",
            "reference_parseval_defect",
            "comparison_parseval_defect",
        )
        scalar_defect = max(
            abs(getattr(candidate, name) - getattr(expected, name))
            for candidate, expected in zip(
                observed.points, reference.points, strict=True
            )
            for name in scalar_names
        )
        harmonic_scalar_names = (
            "maximum_value",
            "amplitude",
            "fundamental_period",
            "applied_degeneracy_cutoff",
        )
        harmonic_defect = max(
            defect
            for candidate, expected in zip(
                observed.points, reference.points, strict=True
            )
            for defect in (
                *(
                    abs(
                        getattr(candidate.harmonic_maximum, name)
                        - getattr(expected.harmonic_maximum, name)
                    )
                    for name in harmonic_scalar_names
                ),
                abs(
                    candidate.harmonic_maximum.harmonic.offset
                    - expected.harmonic_maximum.harmonic.offset
                ),
                abs(
                    candidate.harmonic_maximum.harmonic.cosine_coefficient
                    - expected.harmonic_maximum.harmonic.cosine_coefficient
                ),
                abs(
                    candidate.harmonic_maximum.harmonic.sine_coefficient
                    - expected.harmonic_maximum.harmonic.sine_coefficient
                ),
            )
        )
        harmonic_argument_defect = max(
            (
                float(candidate_argument is not expected_argument)
                if candidate_argument is None or expected_argument is None
                else abs(candidate_argument - expected_argument)
            )
            for candidate, expected in zip(
                observed.points, reference.points, strict=True
            )
            for candidate_argument, expected_argument in (
                (
                    candidate.harmonic_maximum.canonical_maximizing_argument,
                    expected.harmonic_maximum.canonical_maximizing_argument,
                ),
            )
        )
        harmonic_identity_defect = float(
            any(
                candidate.harmonic_maximum.harmonic.harmonic_order
                != expected.harmonic_maximum.harmonic.harmonic_order
                or (
                    candidate.harmonic_maximum.harmonic.fundamental_interval_start
                    != expected.harmonic_maximum.harmonic.fundamental_interval_start
                )
                or candidate.harmonic_maximum.status
                is not expected.harmonic_maximum.status
                for candidate, expected in zip(
                    observed.points, reference.points, strict=True
                )
            )
        )
        observed_hopping_inventory = tuple(
            tuple(power.displacement for power in point.hopping_powers)
            for point in observed.points
        )
        reference_hopping_inventory = tuple(
            tuple(power.displacement for power in point.hopping_powers)
            for point in reference.points
        )
        observations.update(
            {
                "point_scalar_maximum_absolute_defect": (
                    VerificationObservation.dimensionless(scalar_defect, tolerance)
                ),
                "harmonic_scalar_maximum_absolute_defect": (
                    VerificationObservation.dimensionless(harmonic_defect, tolerance)
                ),
                "harmonic_argument_maximum_absolute_defect": (
                    VerificationObservation.dimensionless(
                        harmonic_argument_defect, tolerance
                    )
                ),
                "harmonic_identity_defect": VerificationObservation.dimensionless(
                    harmonic_identity_defect, 0.0
                ),
                "hopping_inventory_defect": VerificationObservation.dimensionless(
                    float(observed_hopping_inventory != reference_hopping_inventory),
                    0.0,
                ),
            }
        )
        if observed_hopping_inventory == reference_hopping_inventory:
            hopping_defect = max(
                max(
                    abs(
                        candidate_power.reference_normalized_squared_frobenius_norm
                        - expected_power.reference_normalized_squared_frobenius_norm
                    ),
                    abs(
                        candidate_power.comparison_normalized_squared_frobenius_norm
                        - expected_power.comparison_normalized_squared_frobenius_norm
                    ),
                )
                for candidate, expected in zip(
                    observed.points, reference.points, strict=True
                )
                for candidate_power, expected_power in zip(
                    candidate.hopping_powers,
                    expected.hopping_powers,
                    strict=True,
                )
            )
            observations["hopping_power_maximum_absolute_defect"] = (
                VerificationObservation.dimensionless(hopping_defect, tolerance)
            )
        return EmbeddedSubspaceRank2Verification(observations)


__all__ = [
    "EmbeddedSubspaceRank2Verification",
    "Periodic1DRank2AnalysisVerificationAssessor",
]
