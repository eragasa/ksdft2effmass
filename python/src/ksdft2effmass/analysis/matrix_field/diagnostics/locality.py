"""Explicit block-norm and symmetric-range locality diagnostics."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from projectkoios.numerics.validation import exact_nonnegative_float
from projectkoios.physkit.solidstate.tb import FinitePeriodicMatrixFourierSeries

from ..normalization import positive_norm_energy_scale


@dataclass(frozen=True, slots=True)
class FourierMatrixBlockNorm1D:
    """Retain one one-dimensional matrix-block Frobenius norm."""

    translation: int
    raw_frobenius_norm: float
    normalized_frobenius_norm: float

    def __post_init__(self) -> None:
        """Validate exact translation and finite nonnegative norms."""
        if type(self.translation) is not int:
            raise TypeError("translation must be a built-in int")
        exact_nonnegative_float(self.raw_frobenius_norm, "raw_frobenius_norm")
        exact_nonnegative_float(
            self.normalized_frobenius_norm,
            "normalized_frobenius_norm",
        )


@dataclass(frozen=True, slots=True)
class FourierMatrixBlockNormInventory1D:
    """Retain an ordered bounded block-norm view of one physical matrix series."""

    series: FinitePeriodicMatrixFourierSeries
    maximum_range: int
    rank: int
    norm_energy_scale: float
    blocks: tuple[FourierMatrixBlockNorm1D, ...]

    def __post_init__(self) -> None:
        """Correlate every retained norm with the immutable source series."""
        if type(self.series) is not FinitePeriodicMatrixFourierSeries:
            raise TypeError("series must be FinitePeriodicMatrixFourierSeries")
        if self.series.dimension != 1:
            raise ValueError("series must be one dimensional")
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank != self.series.matrix_size:
            raise ValueError("rank must equal the source-series matrix size")
        norm_energy_scale = positive_norm_energy_scale(self.norm_energy_scale)
        if type(self.blocks) is not tuple or any(
            type(block) is not FourierMatrixBlockNorm1D for block in self.blocks
        ):
            raise TypeError("blocks must be a tuple of FourierMatrixBlockNorm1D")
        translations = tuple(block.translation for block in self.blocks)
        source_translations = tuple(
            int(value) for value in self.series.integer_modes[:, 0]
        )
        if source_translations != tuple(sorted(set(source_translations))):
            raise ValueError("source-series translations must be unique and increasing")
        expected_translations = tuple(
            value for value in source_translations if abs(value) <= self.maximum_range
        )
        if translations != expected_translations:
            raise ValueError("blocks must match the bounded source-series inventory")
        source_lookup = {
            int(mode): coefficient
            for mode, coefficient in zip(
                self.series.integer_modes[:, 0],
                self.series.matrix_coefficients,
                strict=True,
            )
        }
        scale = math.sqrt(self.rank) * norm_energy_scale
        for block in self.blocks:
            expected_raw = float(np.linalg.norm(source_lookup[block.translation]))
            if block.raw_frobenius_norm != expected_raw:
                raise ValueError("raw block norm must match the source series")
            if block.normalized_frobenius_norm != expected_raw / scale:
                raise ValueError("normalized block norm is inconsistent")


class FourierMatrixBlockNormInventoryAnalyzer1D:
    """Extract a bounded norm inventory from a physical matrix series."""

    __slots__ = ()

    def execute(
        self,
        series: FinitePeriodicMatrixFourierSeries,
        maximum_range: int,
        norm_energy_scale: float,
    ) -> FourierMatrixBlockNormInventory1D:
        """Return every represented block with ``abs(R) <= maximum_range``."""
        if type(series) is not FinitePeriodicMatrixFourierSeries:
            raise TypeError("series must be FinitePeriodicMatrixFourierSeries")
        if series.dimension != 1:
            raise ValueError("block inventory requires a one-dimensional series")
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        norm_energy_scale = positive_norm_energy_scale(norm_energy_scale)
        translations = tuple(int(value) for value in series.integer_modes[:, 0])
        if translations != tuple(sorted(set(translations))):
            raise ValueError("series translations must be unique and increasing")
        rank = series.matrix_size
        scale = math.sqrt(rank) * norm_energy_scale
        blocks = tuple(
            FourierMatrixBlockNorm1D(
                translation=translation,
                raw_frobenius_norm=raw_norm,
                normalized_frobenius_norm=raw_norm / scale,
            )
            for translation, coefficient in zip(
                translations,
                series.matrix_coefficients,
                strict=True,
            )
            if abs(translation) <= maximum_range
            for raw_norm in (float(np.linalg.norm(coefficient)),)
        )
        return FourierMatrixBlockNormInventory1D(
            series=series,
            maximum_range=maximum_range,
            rank=rank,
            norm_energy_scale=norm_energy_scale,
            blocks=blocks,
        )


@dataclass(frozen=True, slots=True)
class SymmetricRangeTailDiagnostics1D:
    """Retain explicit support and complete-matrix Fourier-tail norms."""

    series: FinitePeriodicMatrixFourierSeries
    maximum_range: int
    retained_translations: tuple[int, ...]
    omitted_translations: tuple[int, ...]
    rank: int
    norm_energy_scale: float
    omitted_squared_frobenius_weight: float
    omitted_frobenius_l2_norm: float
    omitted_block_l1_norm: float
    normalized_omitted_squared_frobenius_weight: float
    normalized_omitted_frobenius_l2_norm: float
    normalized_omitted_block_l1_norm: float

    def __post_init__(self) -> None:
        """Validate support inventories, values, and rank/energy normalizations."""
        if type(self.series) is not FinitePeriodicMatrixFourierSeries:
            raise TypeError("series must be FinitePeriodicMatrixFourierSeries")
        if self.series.dimension != 1:
            raise ValueError("series must be one dimensional")
        if type(self.maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if self.maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        for name, translations in (
            ("retained_translations", self.retained_translations),
            ("omitted_translations", self.omitted_translations),
        ):
            if type(translations) is not tuple or any(
                type(value) is not int for value in translations
            ):
                raise TypeError(f"{name} must be a tuple of built-in integers")
            if translations != tuple(sorted(set(translations))):
                raise ValueError(f"{name} must be unique and increasing")
        if set(self.retained_translations) & set(self.omitted_translations):
            raise ValueError("retained and omitted translations must be disjoint")
        series_translations = tuple(
            int(value) for value in self.series.integer_modes[:, 0]
        )
        if series_translations != tuple(sorted(set(series_translations))):
            raise ValueError("source-series translations must be unique and increasing")
        if any(-value not in series_translations for value in series_translations):
            raise ValueError("source-series translations must be inversion complete")
        if (
            tuple(sorted(self.retained_translations + self.omitted_translations))
            != series_translations
        ):
            raise ValueError("tail inventories must partition the source series")
        expected_retained = tuple(
            value for value in series_translations if abs(value) <= self.maximum_range
        )
        if self.retained_translations != expected_retained:
            raise ValueError("retained translations must equal the symmetric range")
        if any(abs(value) > self.maximum_range for value in self.retained_translations):
            raise ValueError("retained translation exceeds maximum_range")
        if any(abs(value) <= self.maximum_range for value in self.omitted_translations):
            raise ValueError("omitted translation lies inside maximum_range")
        expected_omitted = np.abs(self.series.integer_modes[:, 0]) > self.maximum_range
        expected_block_norms = np.linalg.norm(
            self.series.matrix_coefficients[expected_omitted],
            axis=(-2, -1),
        )
        expected_weight = float(np.sum(expected_block_norms**2))
        expected_l2 = math.sqrt(expected_weight)
        expected_l1 = float(np.sum(expected_block_norms))
        if (
            self.omitted_squared_frobenius_weight,
            self.omitted_frobenius_l2_norm,
            self.omitted_block_l1_norm,
        ) != (expected_weight, expected_l2, expected_l1):
            raise ValueError("tail values must match the source series")
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        if self.rank != self.series.matrix_size:
            raise ValueError("rank must equal the source-series matrix size")
        norm_energy_scale = positive_norm_energy_scale(self.norm_energy_scale)
        for name, value in (
            (
                "omitted_squared_frobenius_weight",
                self.omitted_squared_frobenius_weight,
            ),
            ("omitted_frobenius_l2_norm", self.omitted_frobenius_l2_norm),
            ("omitted_block_l1_norm", self.omitted_block_l1_norm),
            (
                "normalized_omitted_squared_frobenius_weight",
                self.normalized_omitted_squared_frobenius_weight,
            ),
            (
                "normalized_omitted_frobenius_l2_norm",
                self.normalized_omitted_frobenius_l2_norm,
            ),
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
        squared_scale = self.rank * norm_energy_scale**2
        linear_scale = math.sqrt(self.rank) * norm_energy_scale
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
            raise ValueError("normalized tail fields are inconsistent")


class SymmetricRangeTailAnalyzer1D:
    """Measure supplied one-dimensional supports on a physical series."""

    __slots__ = ()

    def execute(
        self,
        series: FinitePeriodicMatrixFourierSeries,
        maximum_range: int,
        norm_energy_scale: float,
    ) -> SymmetricRangeTailDiagnostics1D:
        """Return raw and normalized ``W``, ``N``, and block-``l1`` tails."""
        if type(series) is not FinitePeriodicMatrixFourierSeries:
            raise TypeError("series must be FinitePeriodicMatrixFourierSeries")
        if series.dimension != 1:
            raise ValueError("symmetric range tails require a one-dimensional series")
        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        norm_energy_scale = positive_norm_energy_scale(norm_energy_scale)
        translations = series.integer_modes[:, 0]
        translation_inventory = tuple(int(value) for value in translations)
        if translation_inventory != tuple(sorted(set(translation_inventory))):
            raise ValueError("series translations must be unique and increasing")
        if any(-value not in translation_inventory for value in translation_inventory):
            raise ValueError("series translations must be inversion complete")
        retained_mask = np.abs(translations) <= maximum_range
        omitted = series.matrix_coefficients[~retained_mask]
        block_norms = np.linalg.norm(omitted, axis=(-2, -1))
        weight = float(np.sum(block_norms**2))
        l2_norm = math.sqrt(weight)
        l1_norm = float(np.sum(block_norms))
        rank = series.matrix_size
        squared_scale = rank * norm_energy_scale**2
        linear_scale = math.sqrt(rank) * norm_energy_scale
        return SymmetricRangeTailDiagnostics1D(
            series=series,
            maximum_range=maximum_range,
            retained_translations=tuple(
                int(value) for value in translations[retained_mask]
            ),
            omitted_translations=tuple(
                int(value) for value in translations[~retained_mask]
            ),
            rank=rank,
            norm_energy_scale=norm_energy_scale,
            omitted_squared_frobenius_weight=weight,
            omitted_frobenius_l2_norm=l2_norm,
            omitted_block_l1_norm=l1_norm,
            normalized_omitted_squared_frobenius_weight=weight / squared_scale,
            normalized_omitted_frobenius_l2_norm=l2_norm / linear_scale,
            normalized_omitted_block_l1_norm=l1_norm / linear_scale,
        )


@dataclass(frozen=True, slots=True)
class SymmetricRangeTailMonotonicityDiagnostics1D:
    """Retain positive increases between successive nested range tails."""

    coarse_maximum_range: int
    fine_maximum_range: int
    normalized_squared_weight_increase: float
    normalized_l2_norm_increase: float
    normalized_l1_norm_increase: float
    tolerance: float
    passes: bool

    def __post_init__(self) -> None:
        """Validate nested range identities and the derived pass disposition."""
        if (
            type(self.coarse_maximum_range) is not int
            or type(self.fine_maximum_range) is not int
        ):
            raise TypeError("maximum ranges must be built-in integers")
        if not 0 <= self.coarse_maximum_range < self.fine_maximum_range:
            raise ValueError("maximum ranges must be nonnegative and increasing")
        for name, value in (
            (
                "normalized_squared_weight_increase",
                self.normalized_squared_weight_increase,
            ),
            ("normalized_l2_norm_increase", self.normalized_l2_norm_increase),
            ("normalized_l1_norm_increase", self.normalized_l1_norm_increase),
            ("tolerance", self.tolerance),
        ):
            exact_nonnegative_float(value, name)
        if type(self.passes) is not bool:
            raise TypeError("passes must be a built-in bool")
        expected = (
            max(
                self.normalized_squared_weight_increase,
                self.normalized_l2_norm_increase,
                self.normalized_l1_norm_increase,
            )
            <= self.tolerance
        )
        if self.passes is not expected:
            raise ValueError("passes must match increases and tolerance")


class SymmetricRangeTailMonotonicityAnalyzer1D:
    """Check consecutive nested one-dimensional tail summaries."""

    __slots__ = ()

    def execute(
        self,
        tails: tuple[SymmetricRangeTailDiagnostics1D, ...],
        tolerance: float,
    ) -> tuple[SymmetricRangeTailMonotonicityDiagnostics1D, ...]:
        """Return one increase diagnostic for every consecutive range pair."""
        if type(tails) is not tuple or not tails:
            raise TypeError("tails must be a nonempty tuple")
        if any(type(item) is not SymmetricRangeTailDiagnostics1D for item in tails):
            raise TypeError("tails must contain SymmetricRangeTailDiagnostics1D")
        tolerance = exact_nonnegative_float(tolerance, "tolerance")
        ranges = tuple(item.maximum_range for item in tails)
        if ranges != tuple(sorted(set(ranges))):
            raise ValueError("tail ranges must be unique and increasing")
        first = tails[0]
        if any(
            item.series is not first.series
            or item.rank != first.rank
            or item.norm_energy_scale != first.norm_energy_scale
            for item in tails[1:]
        ):
            raise ValueError("tails must describe one series and normalization")
        results: list[SymmetricRangeTailMonotonicityDiagnostics1D] = []
        for coarse, fine in zip(tails[:-1], tails[1:], strict=True):
            increases = (
                max(
                    0.0,
                    fine.normalized_omitted_squared_frobenius_weight
                    - coarse.normalized_omitted_squared_frobenius_weight,
                ),
                max(
                    0.0,
                    fine.normalized_omitted_frobenius_l2_norm
                    - coarse.normalized_omitted_frobenius_l2_norm,
                ),
                max(
                    0.0,
                    fine.normalized_omitted_block_l1_norm
                    - coarse.normalized_omitted_block_l1_norm,
                ),
            )
            results.append(
                SymmetricRangeTailMonotonicityDiagnostics1D(
                    coarse_maximum_range=coarse.maximum_range,
                    fine_maximum_range=fine.maximum_range,
                    normalized_squared_weight_increase=increases[0],
                    normalized_l2_norm_increase=increases[1],
                    normalized_l1_norm_increase=increases[2],
                    tolerance=tolerance,
                    passes=max(increases) <= tolerance,
                )
            )
        return tuple(results)


__all__ = [
    "FourierMatrixBlockNorm1D",
    "FourierMatrixBlockNormInventory1D",
    "FourierMatrixBlockNormInventoryAnalyzer1D",
    "SymmetricRangeTailAnalyzer1D",
    "SymmetricRangeTailDiagnostics1D",
    "SymmetricRangeTailMonotonicityAnalyzer1D",
    "SymmetricRangeTailMonotonicityDiagnostics1D",
]
