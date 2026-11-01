"""Immutable rank-N hopping-locality diagnostic values."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Self

from projectkoios.numerics.validation import exact_nonnegative_float

from ksdft2effmass.analysis.matrix_field.diagnostics import (
    SymmetricRangeTailDiagnostics1D,
)
from ksdft2effmass.periodic1d.hopping_locality import Periodic1DHoppingLocality
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationControls,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.translations import (
    Periodic1DOrdinaryTranslationInventory,
    Periodic1DSymmetricTranslationRange,
)


@dataclass(frozen=True, slots=True)
class Periodic1DRankNHoppingTailResult(Periodic1DHoppingLocality):
    """Describe coefficient weight outside one diagnostic symmetric range.

    This value characterizes the distribution of an unchanged Fourier series. It does
    not represent removal of the coefficients outside ``maximum_range``.
    """

    maximum_range: int
    rank: int
    norm_energy_scale: float
    retained_translations: tuple[int, ...]
    omitted_translations: tuple[int, ...]
    omitted_squared_frobenius_weight: float
    normalized_omitted_squared_frobenius_weight: float
    omitted_frobenius_l2_norm: float
    normalized_omitted_frobenius_l2_norm: float
    omitted_block_l1_norm: float
    normalized_omitted_block_l1_norm: float

    def __post_init__(self) -> None:
        """Validate exact inventories and rank-energy normalization identities."""
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if (
            self.maximum_range
            not in Periodic1DRankNAlignmentCalculationControls.SUPPORT_RADII
        ):
            raise ValueError("maximum_range must be in the frozen diagnostic inventory")
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank not in Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS:
            raise ValueError("rank must be in the frozen retained-rank inventory")
        if type(self.norm_energy_scale) is not float:
            raise TypeError("norm_energy_scale must be a built-in float")
        if self.norm_energy_scale != (
            Periodic1DRankNAlignmentCalculationControls.ENERGY_REFERENCE
        ):
            raise ValueError("norm_energy_scale must equal the frozen normalization")
        for name, translations in (
            ("retained_translations", self.retained_translations),
            ("omitted_translations", self.omitted_translations),
        ):
            if type(translations) is not tuple or not all(
                type(value) is int for value in translations
            ):
                raise TypeError(f"{name} must be a tuple of built-in integers")
            if translations != tuple(sorted(set(translations))):
                raise ValueError(f"{name} must be unique and increasing")
        diagnostic_range = Periodic1DSymmetricTranslationRange(self.maximum_range)
        if self.retained_translations != diagnostic_range.translations:
            raise ValueError("retained translations must equal the diagnostic range")
        if set(self.retained_translations) & set(self.omitted_translations):
            raise ValueError("retained and omitted translations must be disjoint")
        if not all(
            abs(value) > self.maximum_range for value in self.omitted_translations
        ):
            raise ValueError(
                "omitted translations must lie outside the diagnostic range"
            )
        complete_inventory = tuple(
            sorted(self.retained_translations + self.omitted_translations)
        )
        Periodic1DOrdinaryTranslationInventory(complete_inventory)
        for name, value in (
            (
                "omitted_squared_frobenius_weight",
                self.omitted_squared_frobenius_weight,
            ),
            (
                "normalized_omitted_squared_frobenius_weight",
                self.normalized_omitted_squared_frobenius_weight,
            ),
            ("omitted_frobenius_l2_norm", self.omitted_frobenius_l2_norm),
            (
                "normalized_omitted_frobenius_l2_norm",
                self.normalized_omitted_frobenius_l2_norm,
            ),
            ("omitted_block_l1_norm", self.omitted_block_l1_norm),
            (
                "normalized_omitted_block_l1_norm",
                self.normalized_omitted_block_l1_norm,
            ),
        ):
            exact_nonnegative_float(value, name)
        if self.omitted_frobenius_l2_norm != math.sqrt(
            self.omitted_squared_frobenius_weight
        ):
            raise ValueError("omitted l2 norm must be the square root of the weight")
        squared_scale = self.rank * self.norm_energy_scale**2
        linear_scale = math.sqrt(self.rank) * self.norm_energy_scale
        normalized = (
            self.normalized_omitted_squared_frobenius_weight,
            self.normalized_omitted_frobenius_l2_norm,
            self.normalized_omitted_block_l1_norm,
        )
        expected = (
            self.omitted_squared_frobenius_weight / squared_scale,
            self.omitted_frobenius_l2_norm / linear_scale,
            self.omitted_block_l1_norm / linear_scale,
        )
        if normalized != expected:
            raise ValueError("normalized hopping-tail fields are inconsistent")

    @property
    def diagnostic_range(self) -> Periodic1DSymmetricTranslationRange:
        """Return the neutral symmetric range used by this tail diagnostic."""
        return Periodic1DSymmetricTranslationRange(self.maximum_range)

    @property
    def complete_translation_inventory(
        self,
    ) -> Periodic1DOrdinaryTranslationInventory:
        """Return the typed complete ordinary translation inventory."""
        return Periodic1DOrdinaryTranslationInventory(
            tuple(sorted(self.retained_translations + self.omitted_translations))
        )

    @classmethod
    def from_diagnostics(
        cls,
        diagnostics: SymmetricRangeTailDiagnostics1D,
    ) -> Self:
        """Copy one admitted generic tail diagnostic into the periodic rank-N value."""
        if type(diagnostics) is not SymmetricRangeTailDiagnostics1D:
            raise TypeError("diagnostics must be SymmetricRangeTailDiagnostics1D")
        return cls(
            maximum_range=diagnostics.maximum_range,
            rank=diagnostics.rank,
            norm_energy_scale=diagnostics.norm_energy_scale,
            retained_translations=diagnostics.retained_translations,
            omitted_translations=diagnostics.omitted_translations,
            omitted_squared_frobenius_weight=(
                diagnostics.omitted_squared_frobenius_weight
            ),
            normalized_omitted_squared_frobenius_weight=(
                diagnostics.normalized_omitted_squared_frobenius_weight
            ),
            omitted_frobenius_l2_norm=diagnostics.omitted_frobenius_l2_norm,
            normalized_omitted_frobenius_l2_norm=(
                diagnostics.normalized_omitted_frobenius_l2_norm
            ),
            omitted_block_l1_norm=diagnostics.omitted_block_l1_norm,
            normalized_omitted_block_l1_norm=(
                diagnostics.normalized_omitted_block_l1_norm
            ),
        )


__all__ = ["Periodic1DRankNHoppingTailResult"]
