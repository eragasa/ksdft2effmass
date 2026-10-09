"""Typed JSON decoding mechanics for periodic-1D campaign serializers."""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import ScalarQuantity, Unitless, VectorQuantity
from ksdft2effmass.serialization.json import JsonValue, StrictJsonDecoder

type ComplexMatrix = npt.NDArray[np.complex128]


class Periodic1DCampaignJsonDecoder(StrictJsonDecoder):
    """Adapt strict JSON primitives for periodic-1D campaign schemas.

    This stateless wire owner adds unitless scalar/vector and dense complex-pair
    matrix adaptation to :class:`StrictJsonDecoder`. Schema-specific serializers
    remain responsible for field inventories, physical units, scientific identity,
    provenance, and cross-field meaning. No method infers those properties from names,
    dimensions, ranks, or values.
    """

    __slots__ = ()

    def scalar(self, value: JsonValue, name: str) -> ScalarQuantity:
        """Return one explicitly unitless scalar quantity.

        Parameters
        ----------
        value
            Exact JSON integer or finite float. Booleans and numeric strings are not
            numeric inputs.
        name
            Field name used in diagnostics.

        Returns
        -------
        ScalarQuantity
            A binary64 scalar bound to :class:`Unitless`.

        Raises
        ------
        TypeError
            If ``value`` is not an exact supported JSON numeric type.
        ValueError
            If a floating value is nonfinite.
        OverflowError
            If an integer cannot be represented as finite binary64.
        """
        return ScalarQuantity(self.real(value, name), Unitless())

    def vector(self, value: JsonValue, name: str) -> VectorQuantity:
        """Return one explicitly unitless binary64 vector quantity.

        Parameters
        ----------
        value
            JSON array whose members are exact integers or finite floats.
        name
            Field name used in diagnostics.

        Returns
        -------
        VectorQuantity
            A defensive binary64 vector bound to :class:`Unitless`.

        Raises
        ------
        TypeError
            If ``value`` is not an array or a member has an unsupported exact type.
        ValueError
            If a floating member is nonfinite or the quantity invariant is violated.
        OverflowError
            If an integer member cannot be represented as finite binary64.
        MemoryError
            If storage for the dense binary64 vector cannot be allocated.
        """
        return VectorQuantity(
            np.asarray(
                [self.real(item, name) for item in self.array(value, name)],
                dtype=np.float64,
            ),
            Unitless(),
        )

    def complex_matrix(self, value: JsonValue, name: str) -> ComplexMatrix:
        """Decode a nonempty rectangular complex-pair matrix wire.

        Each matrix entry must be a two-element JSON array ``[real, imaginary]``.
        The returned ``complex128`` array is a non-writeable defensive copy. This
        method adapts numeric wire representation only: it assigns no basis, unit,
        state-space, operator, provenance, or scientific meaning.

        Raises
        ------
        TypeError
            If an array or numeric component has the wrong exact JSON type.
        ValueError
            If the matrix is empty, ragged, contains empty rows, or contains a
            complex entry whose wire length is not two.
        OverflowError
            If an integer component cannot be represented as binary64.
        MemoryError
            If storage for the dense ``complex128`` matrix cannot be allocated.
        """
        row_values = self.array(value, name)
        if not row_values:
            raise ValueError(f"{name} must be nonempty")
        rows: list[list[complex]] = []
        expected_width: int | None = None
        for row_index, row_value in enumerate(row_values):
            encoded_row = self.array(row_value, f"{name}[{row_index}]")
            if not encoded_row:
                raise ValueError(f"{name} rows must be nonempty")
            if expected_width is None:
                expected_width = len(encoded_row)
            elif len(encoded_row) != expected_width:
                raise ValueError(f"{name} must be rectangular")
            row: list[complex] = []
            for column_index, entry_value in enumerate(encoded_row):
                entry_name = f"{name}[{row_index}][{column_index}]"
                pair = self.array(entry_value, entry_name)
                if len(pair) != 2:
                    raise ValueError(f"{entry_name} must contain real and imaginary")
                row.append(
                    complex(
                        self.real(pair[0], f"{entry_name}[0]"),
                        self.real(pair[1], f"{entry_name}[1]"),
                    )
                )
            rows.append(row)
        matrix = np.asarray(rows, dtype=np.complex128)
        return np.frombuffer(matrix.tobytes(order="C"), dtype=np.complex128).reshape(
            matrix.shape
        )
