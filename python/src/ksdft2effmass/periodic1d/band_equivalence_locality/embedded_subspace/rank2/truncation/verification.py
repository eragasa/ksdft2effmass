"""Independent in-memory verification for embedded rank-two truncation."""

from __future__ import annotations

from collections.abc import Mapping

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from ..verification import _add_qualification_observations, _observation
from .reference import (
    Periodic1DEmbeddedSubspaceRank2TruncationIndependentReferenceAnalyzer,
)
from .results import (
    Periodic1DEmbeddedSubspaceRank2TruncationAnalysis,
    Periodic1DEmbeddedSubspaceRank2TruncationCompleted,
    Periodic1DEmbeddedSubspaceRank2TruncationQualificationStopped,
)


class EmbeddedSubspaceRank2TruncationVerification(CompositeVerification):
    """Group qualification, conversion, and truncation comparisons."""


class Periodic1DEmbeddedSubspaceRank2TruncationIndependentVerifier:
    """Compare one truncation result with independent direct finite formulas."""

    __slots__ = ("_observed",)

    def __init__(
        self, observed: Periodic1DEmbeddedSubspaceRank2TruncationAnalysis
    ) -> None:
        if type(observed) not in (
            Periodic1DEmbeddedSubspaceRank2TruncationQualificationStopped,
            Periodic1DEmbeddedSubspaceRank2TruncationCompleted,
        ):
            raise TypeError("observed must be a closed truncation outcome")
        self._observed = observed

    def result(self) -> EmbeddedSubspaceRank2TruncationVerification:
        """Return discrepancies without defining a retained wire format."""
        reference = (
            Periodic1DEmbeddedSubspaceRank2TruncationIndependentReferenceAnalyzer(
                self._observed.request
            ).execute()
        )
        return EmbeddedSubspaceRank2TruncationVerification(
            _compare_truncation(self._observed, reference)
        )


def _compare_truncation(
    observed: Periodic1DEmbeddedSubspaceRank2TruncationAnalysis,
    reference: Periodic1DEmbeddedSubspaceRank2TruncationAnalysis,
) -> Mapping[str, VerificationObservation]:
    if observed.request != reference.request:
        raise ValueError(
            "independent truncation request does not match observed request"
        )
    tolerance = observed.request.template_request.verification_absolute_tolerance
    observations: dict[str, VerificationObservation] = {
        "outcome_variant_defect": _observation(
            float(type(observed) is not type(reference)), 0.0
        ),
        "qualification_variant_defect": _observation(
            float(type(observed.qualification) is not type(reference.qualification)),
            0.0,
        ),
        "minimum_external_gap_absolute_defect": _observation(
            abs(
                observed.qualification.minimum_external_gap
                - reference.qualification.minimum_external_gap
            ),
            tolerance,
        ),
    }
    _add_qualification_observations(
        observations,
        observed.qualification,
        reference.qualification,
        tolerance,
    )
    if type(observed) is not Periodic1DEmbeddedSubspaceRank2TruncationCompleted:
        return observations
    if type(reference) is not Periodic1DEmbeddedSubspaceRank2TruncationCompleted:
        return observations
    observations.update(
        {
            "evaluation_coordinate_offset_absolute_defect": _observation(
                abs(
                    observed.evaluation_coordinate_offset
                    - reference.evaluation_coordinate_offset
                ),
                tolerance,
            ),
            "minimum_mesh_separation_absolute_defect": _observation(
                abs(
                    observed.minimum_construction_evaluation_separation
                    - reference.minimum_construction_evaluation_separation
                ),
                tolerance,
            ),
            "point_inventory_defect": _observation(
                float(
                    tuple(point.amplitude for point in observed.points)
                    != tuple(point.amplitude for point in reference.points)
                ),
                0.0,
            ),
            "range_inventory_defect": _observation(
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
        observations["point_count_defect"] = _observation(
            float(abs(len(observed.points) - len(reference.points))), 0.0
        )
        return observations
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
    observations["point_scalar_maximum_absolute_defect"] = _observation(
        max(
            abs(getattr(candidate, name) - getattr(expected, name))
            for candidate, expected in zip(
                observed.points, reference.points, strict=True
            )
            for name in point_names
        ),
        tolerance,
    )
    if any(
        len(candidate.ranges) != len(expected.ranges)
        for candidate, expected in zip(observed.points, reference.points, strict=True)
    ):
        observations["range_count_defect"] = _observation(1.0, 0.0)
        return observations
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
    observations["range_scalar_maximum_absolute_defect"] = _observation(
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
    return observations


__all__ = [
    "EmbeddedSubspaceRank2TruncationVerification",
    "Periodic1DEmbeddedSubspaceRank2TruncationIndependentVerifier",
]
