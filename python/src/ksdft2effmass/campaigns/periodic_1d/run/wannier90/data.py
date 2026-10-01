"""Encapsulating DataObject for one retained Wannier90 integration."""

from dataclasses import dataclass

from ...model.integrations import Periodic1DWannier90IntegrationModel
from .correlate import (
    Periodic1DWannier90IntegrationCorrelationRequest,
    Periodic1DWannier90IntegrationCorrelationResult,
    Periodic1DWannier90IntegrationCorrelator,
)
from .verify import (
    Periodic1DWannier90IntegrationVerificationRequest,
    Periodic1DWannier90IntegrationVerificationResult,
    Periodic1DWannier90IntegrationVerifier,
)


@dataclass(frozen=True, slots=True)
class Periodic1DWannier90Integration:
    """Encapsulate immutable integration state behind cohesive Actionizers.

    Parameters
    ----------
    model
        Retained composite controls, Wannier90 result, variant identity, and any
        explicitly supplied native artifact inventories.

    Notes
    -----
    ``correlate`` checks retained identities and inventories without making a numerical
    claim. ``verify`` additionally requires complete native artifact groups and applies
    explicit bounded Wilson-loop verification controls. Neither operation executes
    Wannier90 or discovers files from ambient paths.
    """

    model: Periodic1DWannier90IntegrationModel

    def __post_init__(self) -> None:
        """Require the exact immutable integration model type."""
        if type(self.model) is not Periodic1DWannier90IntegrationModel:
            raise TypeError("model must be Periodic1DWannier90IntegrationModel")

    def correlate(self) -> Periodic1DWannier90IntegrationCorrelationResult:
        """Correlate retained composite controls and Wannier90 result bytes.

        Returns
        -------
        Periodic1DWannier90IntegrationCorrelationResult
            Typed records and exact payload identities without a numerical claim.
        """
        return Periodic1DWannier90IntegrationCorrelator().execute(
            Periodic1DWannier90IntegrationCorrelationRequest(self.model)
        )

    def verify(
        self,
        *,
        phase_absolute_tolerance: float,
        loop_unitarity_absolute_tolerance: float,
        minimum_active_overlap_singular_value: float,
    ) -> Periodic1DWannier90IntegrationVerificationResult:
        """Authenticate explicit native bytes and verify Wilson-loop evidence.

        Parameters
        ----------
        phase_absolute_tolerance
            Maximum circular Wilson phase-set defect in dimensionless radians.
        loop_unitarity_absolute_tolerance
            Maximum Frobenius unitarity defect for reconstructed Wilson loops.
        minimum_active_overlap_singular_value
            Minimum accepted dimensionless active-overlap singular value.

        Returns
        -------
        Periodic1DWannier90IntegrationVerificationResult
            Authenticated native artifacts and bounded numerical findings.

        Raises
        ------
        ValueError
            If controls are invalid, native artifacts are unavailable or incomplete,
            identities disagree, or represented structures are incompatible.
        """
        return Periodic1DWannier90IntegrationVerifier().execute(
            Periodic1DWannier90IntegrationVerificationRequest(
                self.model,
                phase_absolute_tolerance,
                loop_unitarity_absolute_tolerance,
                minimum_active_overlap_singular_value,
            )
        )
