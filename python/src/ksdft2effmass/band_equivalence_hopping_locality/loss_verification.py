"""Independent-consistency verification for finite-rank locality losses."""

from __future__ import annotations

from ksdft2effmass.numerical_consistency import NumericalConsistency
from ksdft2effmass.verification import CompositeVerification, VerificationObservation

from .loss_value import BandEquivalenceHoppingLocalityLoss

_LOSS_VERIFICATION_ABSOLUTE_TOLERANCE = 1.0e-10


class BandEquivalenceHoppingLocalityLossVerification(
    CompositeVerification, NumericalConsistency
):
    """Retain agreement with an independent direct finite-sum reconstruction."""


class BandEquivalenceHoppingLocalityLossVerifier:
    """Compare production and independent values of one typed loss definition."""

    __slots__ = ("_independent", "_production", "_tolerance")

    def __init__(
        self,
        *,
        production: BandEquivalenceHoppingLocalityLoss,
        independent: BandEquivalenceHoppingLocalityLoss,
    ) -> None:
        if type(production) is not BandEquivalenceHoppingLocalityLoss:
            raise TypeError("production must be BandEquivalenceHoppingLocalityLoss")
        if type(independent) is not BandEquivalenceHoppingLocalityLoss:
            raise TypeError("independent must be BandEquivalenceHoppingLocalityLoss")
        if production.definition != independent.definition:
            raise ValueError("production and independent loss definitions differ")
        self._production = production
        self._independent = independent
        self._tolerance = _LOSS_VERIFICATION_ABSOLUTE_TOLERANCE

    def result(self) -> BandEquivalenceHoppingLocalityLossVerification:
        """Return dimensionless operator- and spectral-loss discrepancies."""
        return BandEquivalenceHoppingLocalityLossVerification(
            {
                "operator_loss": VerificationObservation.dimensionless(
                    abs(
                        self._production.operator_loss - self._independent.operator_loss
                    ),
                    self._tolerance,
                ),
                "spectral_loss": VerificationObservation.dimensionless(
                    abs(
                        self._production.spectral_loss - self._independent.spectral_loss
                    ),
                    self._tolerance,
                ),
            }
        )


__all__ = [
    "BandEquivalenceHoppingLocalityLossVerification",
    "BandEquivalenceHoppingLocalityLossVerifier",
]
