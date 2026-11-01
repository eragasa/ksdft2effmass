"""Immutable rank-N symmetric-support truncation results."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

from projectkoios.physkit.periodic.lattice.finite_domain import (
    LatticeDimension,
    LatticeDisplacement,
)

from ksdft2effmass.periodic1d.rankN._record_admission import (
    _decoded_bool,
    _decoded_float,
    _finite_nonnegative,
    _mapping_value,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.calculation import (
    Periodic1DRankNAlignmentCalculationControls,
)
from ksdft2effmass.periodic1d.rankN.band_alignment.configuration import (
    Periodic1DRankNAlignmentConfiguration,
)
from ksdft2effmass.periodic1d.rankN.diagnostics import (
    Periodic1DRankNMatrixComparisonResult,
)
from ksdft2effmass.periodic1d.support_truncation import (
    Periodic1DSupportTruncation,
)
from ksdft2effmass.real_space_support_truncation import ConjugateClosedSupport
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


@dataclass(frozen=True, slots=True)
class Periodic1DRankNSupportResult(
    BaseTypedRecord,
    Periodic1DSupportTruncation,
):
    """Retain one symmetric support and its separate error channels."""

    maximum_range: int
    rank: int
    energy_reference: float
    retained_translations: tuple[int, ...]
    omitted_squared_frobenius_weight: float
    normalized_omitted_squared_frobenius_weight: float
    omitted_frobenius_l2_norm: float
    normalized_omitted_frobenius_l2_norm: float
    omitted_block_l1_norm: float
    normalized_omitted_block_l1_norm: float
    construction_parseval_relative_defect: float
    construction_parseval_pass: bool
    truncation: Periodic1DRankNMatrixComparisonResult
    total: Periodic1DRankNMatrixComparisonResult
    error_decomposition_defect: float
    normalized_error_decomposition_defect: float
    error_decomposition_pass: bool

    def __post_init__(self) -> None:
        if (
            type(self.maximum_range) is not int
            or self.maximum_range
            not in Periodic1DRankNAlignmentCalculationControls.SUPPORT_RADII
        ):
            raise ValueError("maximum_range must be a frozen built-in support radius")
        if (
            type(self.rank) is not int
            or self.rank not in Periodic1DRankNAlignmentConfiguration.RETAINED_RANKS
        ):
            raise ValueError("rank must be in the frozen retained-rank inventory")
        if self.energy_reference != (
            Periodic1DRankNAlignmentCalculationControls.ENERGY_REFERENCE
        ):
            raise ValueError("energy_reference must equal the frozen normalization")
        if type(self.retained_translations) is not tuple or any(
            type(value) is not int for value in self.retained_translations
        ):
            raise TypeError("retained_translations must be an exact integer tuple")
        if self.retained_translations != tuple(
            range(-self.maximum_range, self.maximum_range + 1)
        ):
            raise ValueError(
                "retained_translations must equal the declared symmetric support"
            )
        for value, name in (
            (
                self.omitted_squared_frobenius_weight,
                "omitted_squared_frobenius_weight",
            ),
            (
                self.normalized_omitted_squared_frobenius_weight,
                "normalized_omitted_squared_frobenius_weight",
            ),
            (self.omitted_frobenius_l2_norm, "omitted_frobenius_l2_norm"),
            (
                self.normalized_omitted_frobenius_l2_norm,
                "normalized_omitted_frobenius_l2_norm",
            ),
            (self.omitted_block_l1_norm, "omitted_block_l1_norm"),
            (
                self.normalized_omitted_block_l1_norm,
                "normalized_omitted_block_l1_norm",
            ),
            (
                self.construction_parseval_relative_defect,
                "construction_parseval_relative_defect",
            ),
            (self.error_decomposition_defect, "error_decomposition_defect"),
            (
                self.normalized_error_decomposition_defect,
                "normalized_error_decomposition_defect",
            ),
        ):
            _finite_nonnegative(value, name)
        if self.omitted_frobenius_l2_norm != math.sqrt(
            self.omitted_squared_frobenius_weight
        ):
            raise ValueError("omitted l2 norm must be the square root of the weight")
        squared_scale = self.rank * self.energy_reference**2
        linear_scale = math.sqrt(self.rank) * self.energy_reference
        normalized = (
            self.normalized_omitted_squared_frobenius_weight,
            self.normalized_omitted_frobenius_l2_norm,
            self.normalized_omitted_block_l1_norm,
        )
        expected_normalized = (
            self.omitted_squared_frobenius_weight / squared_scale,
            self.omitted_frobenius_l2_norm / linear_scale,
            self.omitted_block_l1_norm / linear_scale,
        )
        if normalized != expected_normalized:
            raise ValueError("normalized tail fields are inconsistent")
        if type(self.construction_parseval_pass) is not bool:
            raise TypeError("construction_parseval_pass must be a built-in bool")
        controls = Periodic1DRankNAlignmentCalculationControls
        fourier_tolerance = controls.FOURIER_CONSISTENCY_TOLERANCE
        if self.construction_parseval_pass is not (
            self.construction_parseval_relative_defect <= fourier_tolerance
        ):
            raise ValueError("construction Parseval disposition is inconsistent")
        if type(self.error_decomposition_pass) is not bool:
            raise TypeError("error_decomposition_pass must be a built-in bool")
        decomposition_tolerance = controls.ERROR_DECOMPOSITION_TOLERANCE
        if self.error_decomposition_pass is not (
            self.normalized_error_decomposition_defect <= decomposition_tolerance
        ):
            raise ValueError("error-decomposition disposition is inconsistent")
        if (
            type(self.truncation) is not Periodic1DRankNMatrixComparisonResult
            or type(self.total) is not Periodic1DRankNMatrixComparisonResult
        ):
            raise TypeError("truncation and total must be exact comparison records")

    @property
    def support_policy(self) -> ConjugateClosedSupport:
        """Return the typed explicit symmetric support policy."""
        return ConjugateClosedSupport(
            tuple(
                LatticeDisplacement(LatticeDimension.ONE, (translation,))
                for translation in self.retained_translations
            )
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "maximum_range": self.maximum_range,
            "rank": self.rank,
            "energy_reference": self.energy_reference,
            "retained_translations": self.retained_translations,
            "omitted_squared_frobenius_weight": (self.omitted_squared_frobenius_weight),
            "normalized_omitted_squared_frobenius_weight": (
                self.normalized_omitted_squared_frobenius_weight
            ),
            "omitted_frobenius_l2_norm": self.omitted_frobenius_l2_norm,
            "normalized_omitted_frobenius_l2_norm": (
                self.normalized_omitted_frobenius_l2_norm
            ),
            "omitted_block_l1_norm": self.omitted_block_l1_norm,
            "normalized_omitted_block_l1_norm": (self.normalized_omitted_block_l1_norm),
            "construction_parseval_relative_defect": (
                self.construction_parseval_relative_defect
            ),
            "construction_parseval_pass": self.construction_parseval_pass,
            "truncation": self.truncation,
            "total": self.total,
            "error_decomposition_defect": self.error_decomposition_defect,
            "normalized_error_decomposition_defect": (
                self.normalized_error_decomposition_defect
            ),
            "error_decomposition_pass": self.error_decomposition_pass,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "maximum_range",
            "rank",
            "energy_reference",
            "retained_translations",
            "omitted_squared_frobenius_weight",
            "normalized_omitted_squared_frobenius_weight",
            "omitted_frobenius_l2_norm",
            "normalized_omitted_frobenius_l2_norm",
            "omitted_block_l1_norm",
            "normalized_omitted_block_l1_norm",
            "construction_parseval_relative_defect",
            "construction_parseval_pass",
            "truncation",
            "total",
            "error_decomposition_defect",
            "normalized_error_decomposition_defect",
            "error_decomposition_pass",
        }:
            raise ValueError("support result fields do not match")
        maximum_range = values["maximum_range"]
        rank = values["rank"]
        translations = values["retained_translations"]
        if type(maximum_range) is not int or type(rank) is not int:
            raise TypeError("maximum_range and rank must decode to integers")
        if not isinstance(translations, tuple) or any(
            type(value) is not int for value in translations
        ):
            raise TypeError("retained_translations must decode to built-in integers")
        return cls(
            maximum_range=maximum_range,
            rank=rank,
            energy_reference=_decoded_float(
                values["energy_reference"], "energy_reference"
            ),
            retained_translations=translations,
            omitted_squared_frobenius_weight=_decoded_float(
                values["omitted_squared_frobenius_weight"],
                "omitted_squared_frobenius_weight",
            ),
            normalized_omitted_squared_frobenius_weight=_decoded_float(
                values["normalized_omitted_squared_frobenius_weight"],
                "normalized_omitted_squared_frobenius_weight",
            ),
            omitted_frobenius_l2_norm=_decoded_float(
                values["omitted_frobenius_l2_norm"], "omitted_frobenius_l2_norm"
            ),
            normalized_omitted_frobenius_l2_norm=_decoded_float(
                values["normalized_omitted_frobenius_l2_norm"],
                "normalized_omitted_frobenius_l2_norm",
            ),
            omitted_block_l1_norm=_decoded_float(
                values["omitted_block_l1_norm"], "omitted_block_l1_norm"
            ),
            normalized_omitted_block_l1_norm=_decoded_float(
                values["normalized_omitted_block_l1_norm"],
                "normalized_omitted_block_l1_norm",
            ),
            construction_parseval_relative_defect=_decoded_float(
                values["construction_parseval_relative_defect"],
                "construction_parseval_relative_defect",
            ),
            construction_parseval_pass=_decoded_bool(
                values["construction_parseval_pass"],
                "construction_parseval_pass",
            ),
            truncation=Periodic1DRankNMatrixComparisonResult.from_dict(
                _mapping_value(values["truncation"], "truncation")
            ),
            total=Periodic1DRankNMatrixComparisonResult.from_dict(
                _mapping_value(values["total"], "total")
            ),
            error_decomposition_defect=_decoded_float(
                values["error_decomposition_defect"],
                "error_decomposition_defect",
            ),
            normalized_error_decomposition_defect=_decoded_float(
                values["normalized_error_decomposition_defect"],
                "normalized_error_decomposition_defect",
            ),
            error_decomposition_pass=_decoded_bool(
                values["error_decomposition_pass"],
                "error_decomposition_pass",
            ),
        )


__all__ = ["Periodic1DRankNSupportResult"]
