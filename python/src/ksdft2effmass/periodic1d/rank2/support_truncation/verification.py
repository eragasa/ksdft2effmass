"""Independent in-memory verification for embedded rank-two truncation."""

from __future__ import annotations

from ksdft2effmass.periodic1d.band_equivalence_locality.embedded_subspace.rank2.parent_scale.qualification_verification import (  # noqa: E501
    Periodic1DRank2QualificationVerificationAssessor,
)
from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from .reference import (
    Periodic1DRank2TruncationIndependentReferenceAnalyzer,
)
from .results import (
    Periodic1DRank2SupportTruncationAnalysis,
    Periodic1DRank2TruncationCompleted,
    Periodic1DRank2TruncationQualificationStopped,
)


class EmbeddedSubspaceRank2TruncationVerification(CompositeVerification):
    """Group qualification, conversion, and truncation comparisons."""


class Periodic1DRank2TruncationIndependentVerifier:
    """Compare one truncation result with independent direct finite formulas."""

    __slots__ = ("_observed",)

    def __init__(
        self,
        observed: Periodic1DRank2SupportTruncationAnalysis,
    ) -> None:
        if type(observed) not in (
            Periodic1DRank2TruncationQualificationStopped,
            Periodic1DRank2TruncationCompleted,
        ):
            raise TypeError("observed must be a closed truncation outcome")
        self._observed = observed

    def result(self) -> EmbeddedSubspaceRank2TruncationVerification:
        """Return discrepancies without defining a retained wire format."""
        reference = Periodic1DRank2TruncationIndependentReferenceAnalyzer(
            self._observed.request
        ).execute()
        return Periodic1DRank2TruncationVerificationAssessor(
            observed=self._observed,
            reference=reference,
        ).assess()


class Periodic1DRank2TruncationVerificationAssessor:
    """Compare one observed outcome with one independently rebuilt outcome."""

    __slots__ = ("_observed", "_reference")

    def __init__(
        self,
        *,
        observed: Periodic1DRank2SupportTruncationAnalysis,
        reference: Periodic1DRank2SupportTruncationAnalysis,
    ) -> None:
        for name, outcome in (("observed", observed), ("reference", reference)):
            if type(outcome) not in (
                Periodic1DRank2TruncationQualificationStopped,
                Periodic1DRank2TruncationCompleted,
            ):
                raise TypeError(f"{name} must be one closed truncation outcome")
        self._observed = observed
        self._reference = reference

    def assess(self) -> EmbeddedSubspaceRank2TruncationVerification:
        """Return declared-tolerance defects for the supplied outcome pair."""
        observed = self._observed
        reference = self._reference
        if observed.request != reference.request:
            raise ValueError(
                "independent truncation request does not match observed request"
            )
        tolerance = observed.request.template_request.verification_absolute_tolerance
        observations: dict[str, VerificationObservation] = {
            "outcome_variant_defect": VerificationObservation.dimensionless(
                float(type(observed) is not type(reference)), 0.0
            )
        }
        qualification_verification = Periodic1DRank2QualificationVerificationAssessor(
            observed=observed.qualification,
            reference=reference.qualification,
            tolerance=tolerance,
        ).assess()
        observations.update(qualification_verification.observations)
        if type(observed) is not Periodic1DRank2TruncationCompleted:
            return EmbeddedSubspaceRank2TruncationVerification(observations)
        if type(reference) is not Periodic1DRank2TruncationCompleted:
            return EmbeddedSubspaceRank2TruncationVerification(observations)
        observations.update(
            {
                "evaluation_coordinate_offset_absolute_defect": (
                    VerificationObservation.dimensionless(
                        abs(
                            observed.evaluation_coordinate_offset
                            - reference.evaluation_coordinate_offset
                        ),
                        tolerance,
                    )
                ),
                "minimum_mesh_separation_absolute_defect": (
                    VerificationObservation.dimensionless(
                        abs(
                            observed.minimum_construction_evaluation_separation
                            - reference.minimum_construction_evaluation_separation
                        ),
                        tolerance,
                    )
                ),
                "point_inventory_defect": VerificationObservation.dimensionless(
                    float(
                        tuple(point.amplitude for point in observed.points)
                        != tuple(point.amplitude for point in reference.points)
                    ),
                    0.0,
                ),
                "range_inventory_defect": VerificationObservation.dimensionless(
                    float(
                        tuple(
                            tuple(item.maximum_range for item in point.ranges)
                            for point in observed.points
                        )
                        != tuple(
                            tuple(item.maximum_range for item in point.ranges)
                            for point in reference.points
                        )
                    ),
                    0.0,
                ),
            }
        )
        if len(observed.points) != len(reference.points):
            observations["point_count_defect"] = VerificationObservation.dimensionless(
                float(abs(len(observed.points) - len(reference.points))), 0.0
            )
            return EmbeddedSubspaceRank2TruncationVerification(observations)
        point_names = (
            "reference_nyquist_power",
            "comparison_nyquist_power",
            "reference_ordinary_hermiticity_maximum_defect",
            "comparison_ordinary_hermiticity_maximum_defect",
            "direct_spectral_maximum_defect",
            "comparison_interpolation_hamiltonian_maximum_error",
            "comparison_interpolation_hamiltonian_rms_error",
            "comparison_interpolation_spectral_maximum_error",
            "comparison_interpolation_spectral_rms_error",
        )
        observations["point_scalar_maximum_absolute_defect"] = (
            VerificationObservation.dimensionless(
                max(
                    abs(getattr(candidate, name) - getattr(expected, name))
                    for candidate, expected in zip(
                        observed.points, reference.points, strict=True
                    )
                    for name in point_names
                ),
                tolerance,
            )
        )
        if any(
            len(candidate.ranges) != len(expected.ranges)
            for candidate, expected in zip(
                observed.points, reference.points, strict=True
            )
        ):
            observations["range_count_defect"] = VerificationObservation.dimensionless(
                1.0, 0.0
            )
            return EmbeddedSubspaceRank2TruncationVerification(observations)
        range_names = (
            "reference_ordinary_omitted_power",
            "comparison_ordinary_omitted_power",
            "reference_total_omitted_power",
            "comparison_total_omitted_power",
            "reference_truncation_hamiltonian_maximum_error",
            "reference_truncation_hamiltonian_rms_error",
            "reference_truncation_spectral_maximum_error",
            "reference_truncation_spectral_rms_error",
            "comparison_truncation_hamiltonian_maximum_error",
            "comparison_truncation_hamiltonian_rms_error",
            "comparison_truncation_spectral_maximum_error",
            "comparison_truncation_spectral_rms_error",
            "comparison_total_hamiltonian_maximum_error",
            "comparison_total_hamiltonian_rms_error",
            "comparison_total_spectral_maximum_error",
            "comparison_total_spectral_rms_error",
        )
        observations["range_scalar_maximum_absolute_defect"] = (
            VerificationObservation.dimensionless(
                max(
                    abs(getattr(candidate_range, name) - getattr(expected_range, name))
                    for candidate, expected in zip(
                        observed.points, reference.points, strict=True
                    )
                    for candidate_range, expected_range in zip(
                        candidate.ranges, expected.ranges, strict=True
                    )
                    for name in range_names
                ),
                tolerance,
            )
        )
        return EmbeddedSubspaceRank2TruncationVerification(observations)


__all__ = [
    "EmbeddedSubspaceRank2TruncationVerification",
    "Periodic1DRank2TruncationIndependentVerifier",
    "Periodic1DRank2TruncationVerificationAssessor",
]
