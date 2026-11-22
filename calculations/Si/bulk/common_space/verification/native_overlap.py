"""Independent exact overlap reconstruction after shared native parsing."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import ClassVar

from .gram_rank import (
    CommonSpaceGramRankEnclosure,
    _ExactComplex,
    _ExactGramRankEncloser,
    _ExactMatrix,
)
from .native_inputs import CommonSpaceParsedNativeInputs


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceReconstructedOverlap:
    """An exact dimensionless B in the explicitly declared atomic coordinate order.

    This in-process record is not an authenticated scientific result or a completed
    CSD1-V verification. Exact entries and subsequent Gram arithmetic refer to parsed
    binary64 values and the declared trial convention, not unknown native exact data.
    """

    parsed_inputs: CommonSpaceParsedNativeInputs
    ordered_index: int
    _matrix: _ExactMatrix

    def __post_init__(self) -> None:
        if type(self.parsed_inputs) is not CommonSpaceParsedNativeInputs:
            raise TypeError("parsed_inputs must be CommonSpaceParsedNativeInputs")
        self.parsed_inputs.contract.require_ordered_index(self.ordered_index)
        if type(self._matrix) is not _ExactMatrix or (
            len(self._matrix.rows),
            len(self._matrix.rows[0]),
        ) != (10, 10):
            raise ValueError("reconstructed overlap must be an exact ten-by-ten matrix")

    @property
    def fractional_kpoint(self) -> tuple[float, float, float]:
        return self.parsed_inputs.contract.ordered_fractional_kpoints[
            self.ordered_index
        ]

    @property
    def atomic_basis_order(self) -> tuple[str, ...]:
        return self.parsed_inputs.contract.atomic_basis_order

    def entry(self, *, row: int, column: int) -> tuple[Fraction, Fraction]:
        """Return exact real/imaginary components; indices are built-in integers."""
        if any(
            type(index) is not int or not 0 <= index < 10 for index in (row, column)
        ):
            raise ValueError(
                "overlap entry indices must be built-in integers in [0, 10)"
            )
        value = self._matrix.rows[row][column]
        return value.real, value.imaginary

    def enclose_rank(self, *, rank_threshold: Fraction) -> CommonSpaceGramRankEnclosure:
        """Certify this exact reconstructed matrix without rounding B to binary64.

        Threshold must be an exact nonnegative built-in Fraction. This method neither
        derives native-decimal uncertainty nor selects a scientific threshold. Candidate
        overflow yields numerical inconclusiveness; resource errors propagate.
        """
        return _ExactGramRankEncloser(
            independent_overlap=self._matrix, rank_threshold=rank_threshold
        ).execute()


@dataclass(frozen=True, slots=True, kw_only=True)
class CommonSpaceNativeOverlapReconstruction:
    """Construct W=U_dis U, C=A T†, B=W† C using independent exact arithmetic.

    Native shapes are logical (band, trial), (wannier, wannier), and (band, wannier).
    T has atomic rows and native-projection columns: four hybrids at each center,
    then the two radial s channels. All products are exact for parsed binary64 entries;
    no floating reconstructed B, producer matrix, pseudoinverse, or completion is used.
    Rational products have no fixed-width numeric overflow; resource errors propagate.
    """

    HYBRID_DIRECTIONS: ClassVar[tuple[tuple[int, int, int], ...]] = (
        (1, 1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
    )

    parsed_inputs: CommonSpaceParsedNativeInputs
    ordered_index: int

    def __post_init__(self) -> None:
        if type(self.parsed_inputs) is not CommonSpaceParsedNativeInputs:
            raise TypeError("parsed_inputs must be CommonSpaceParsedNativeInputs")
        self.parsed_inputs.contract.require_ordered_index(self.ordered_index)

    def execute(self) -> CommonSpaceReconstructedOverlap:
        """Reconstruct only the selected declared point; do not advance a gate."""
        index = self.ordered_index
        amn = _ExactMatrix.from_binary64(
            tuple(
                tuple(complex(value) for value in row)
                for row in self.parsed_inputs.trial_overlaps.matrices[index].magnitude
            )
        )
        gauge = _ExactMatrix.from_binary64(
            tuple(
                tuple(complex(value) for value in row)
                for row in self.parsed_inputs.gauge.matrices[index].magnitude
            )
        )
        disentanglement = _ExactMatrix.from_binary64(
            tuple(
                tuple(complex(value) for value in row)
                for row in self.parsed_inputs.disentanglement.matrices[index].magnitude
            )
        )
        transform = self._atomic_transform()
        retained_frame = disentanglement.multiply(gauge)
        atomic_trials = amn.multiply(transform.adjoint())
        return CommonSpaceReconstructedOverlap(
            parsed_inputs=self.parsed_inputs,
            ordered_index=index,
            _matrix=retained_frame.adjoint().multiply(atomic_trials),
        )

    @classmethod
    def _atomic_transform(cls) -> _ExactMatrix:
        """Derive coefficients from hybrid directions, not producer matrix code."""

        def coefficient(atomic: int, native: int) -> Fraction:
            center, orbital = divmod(atomic, 5)
            if orbital == 4:
                # s* is the additional radial s channel, not a principal quantum number.
                return Fraction(int(native == 8 + center))
            if not 4 * center <= native < 4 * center + 4:
                return Fraction(0)
            if orbital == 0:
                return Fraction(1, 2)
            return Fraction(cls.HYBRID_DIRECTIONS[native - 4 * center][orbital - 1], 2)

        transform = _ExactMatrix(
            rows=tuple(
                tuple(
                    _ExactComplex(real=coefficient(row, column)) for column in range(10)
                )
                for row in range(10)
            )
        )
        identity = _ExactMatrix.diagonal((Fraction(1),) * 10)
        if transform.multiply(transform.adjoint()) != identity:
            raise RuntimeError("declared atomic transformation is not exactly unitary")
        return transform
