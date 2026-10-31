"""Focused verification of embedded rank-two parent qualification."""

from __future__ import annotations

import math

from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from .results import (
    Periodic1DRank2BandTransportBackendFailure,
    Periodic1DRank2BandTransportNumericallyUnresolved,
    Periodic1DRank2BandTransportThresholdFailure,
    Periodic1DRank2ExternalGapFailure,
    Periodic1DRank2Qualification,
    Periodic1DRank2QualifiedParent,
)


class Periodic1DRank2QualificationVerification(CompositeVerification):
    """Group independent qualification-variant comparisons."""


class Periodic1DRank2QualificationVerificationAssessor:
    """Compare one observed qualification with an independent reference."""

    __slots__ = ("_observed", "_reference", "_tolerance")

    def __init__(
        self,
        *,
        observed: Periodic1DRank2Qualification,
        reference: Periodic1DRank2Qualification,
        tolerance: float,
    ) -> None:
        qualification_types = (
            Periodic1DRank2ExternalGapFailure,
            Periodic1DRank2BandTransportBackendFailure,
            Periodic1DRank2BandTransportNumericallyUnresolved,
            Periodic1DRank2BandTransportThresholdFailure,
            Periodic1DRank2QualifiedParent,
        )
        if type(observed) not in qualification_types:
            raise TypeError("observed must be one closed qualification outcome")
        if type(reference) not in qualification_types:
            raise TypeError("reference must be one closed qualification outcome")
        if type(tolerance) is not float:
            raise TypeError("tolerance must be a built-in float")
        if not math.isfinite(tolerance) or tolerance < 0.0:
            raise ValueError("tolerance must be finite and nonnegative")
        self._observed = observed
        self._reference = reference
        self._tolerance = tolerance

    def assess(
        self,
    ) -> Periodic1DRank2QualificationVerification:
        """Return variant-specific qualification discrepancies."""
        observed = self._observed
        reference = self._reference
        observations = {
            "qualification_variant_defect": VerificationObservation.dimensionless(
                value=float(type(observed) is not type(reference)),
                tolerance=0.0,
            ),
            "minimum_external_gap_absolute_defect": (
                VerificationObservation.dimensionless(
                    value=abs(
                        observed.minimum_external_gap - reference.minimum_external_gap
                    ),
                    tolerance=self._tolerance,
                )
            ),
        }
        if type(observed) is not type(reference):
            return Periodic1DRank2QualificationVerification(observations)
        if type(observed) is Periodic1DRank2ExternalGapFailure:
            return Periodic1DRank2QualificationVerification(observations)
        if type(observed) is Periodic1DRank2BandTransportBackendFailure:
            reference_backend = reference
            if type(reference_backend) is not type(observed):
                return Periodic1DRank2QualificationVerification(observations)
            observations["band_transport_backend_payload_defect"] = (
                VerificationObservation.dimensionless(
                    value=float(
                        observed.operation is not reference_backend.operation
                        or observed.reason is not reference_backend.reason
                        or observed.link_index != reference_backend.link_index
                    ),
                    tolerance=0.0,
                )
            )
            return Periodic1DRank2QualificationVerification(observations)
        if type(observed) is Periodic1DRank2BandTransportNumericallyUnresolved:
            reference_unresolved = reference
            if type(reference_unresolved) is not type(observed):
                return Periodic1DRank2QualificationVerification(observations)
            observations["band_transport_status_defect"] = (
                VerificationObservation.dimensionless(
                    value=float(
                        observed.band_transport_status
                        is not reference_unresolved.band_transport_status
                    ),
                    tolerance=0.0,
                )
            )
            observations["minimum_transport_singular_value_absolute_defect"] = (
                VerificationObservation.dimensionless(
                    value=abs(
                        observed.minimum_transport_singular_value
                        - reference_unresolved.minimum_transport_singular_value
                    ),
                    tolerance=self._tolerance,
                )
            )
            return Periodic1DRank2QualificationVerification(observations)
        if type(observed) is Periodic1DRank2BandTransportThresholdFailure:
            reference_threshold = reference
            if type(reference_threshold) is not type(observed):
                return Periodic1DRank2QualificationVerification(observations)
            observations["minimum_transport_singular_value_absolute_defect"] = (
                VerificationObservation.dimensionless(
                    value=abs(
                        observed.minimum_transport_singular_value
                        - reference_threshold.minimum_transport_singular_value
                    ),
                    tolerance=self._tolerance,
                )
            )
            return Periodic1DRank2QualificationVerification(observations)
        if type(observed) is not Periodic1DRank2QualifiedParent:
            return Periodic1DRank2QualificationVerification(observations)
        reference_qualified = reference
        if type(reference_qualified) is not type(observed):
            return Periodic1DRank2QualificationVerification(observations)
        scalar_names = (
            "minimum_transport_singular_value",
            "maximum_transport_rank_cutoff",
            "maximum_transport_unitarity_defect",
            "maximum_primitive_link_frobenius_residual",
            "closure_alignment_residual",
            "closure_alignment_unitarity_defect",
            "maximum_frame_orthonormality_defect",
            "maximum_reference_hermiticity_defect",
        )
        observations["qualification_scalar_maximum_absolute_defect"] = (
            VerificationObservation.dimensionless(
                value=max(
                    abs(getattr(observed, name) - getattr(reference_qualified, name))
                    for name in scalar_names
                ),
                tolerance=self._tolerance,
            )
        )
        observations["closure_phase_maximum_absolute_defect"] = (
            VerificationObservation.dimensionless(
                value=max(
                    abs(candidate - expected)
                    for candidate, expected in zip(
                        observed.closure_holonomy_phases,
                        reference_qualified.closure_holonomy_phases,
                        strict=True,
                    )
                ),
                tolerance=self._tolerance,
            )
        )
        return Periodic1DRank2QualificationVerification(observations)


__all__ = [
    "Periodic1DRank2QualificationVerification",
    "Periodic1DRank2QualificationVerificationAssessor",
]
