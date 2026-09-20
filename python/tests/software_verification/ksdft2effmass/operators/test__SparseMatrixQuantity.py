r"""Software verification of ``SparseMatrixQuantity``.

Evidence profile: routine

Bounded artifact scope: immutable canonical CSR quantity storage and explicit
conversion boundaries.

Facet and represented meaning

The DataObject retains finite binary64 matrix values, shape, CSR structure, and one
explicit physical or dimensionless unit.

Intrinsic and cross-object scope

Canonicalization, structural correlation, immutability, and fresh CSR conversion are
included.

VVUQ and scientific exclusions

This verifies storage behavior, not a numerical method, scientific validation,
uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import SparseMatrixQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = SparseMatrixQuantity


class TestSparseMatrixQuantity:
    """Own software evidence for ``SparseMatrixQuantity``."""

    def test_constructor__canonical_csr_storage__is_compact_and_immutable(self) -> None:
        """Evidence ID: SV-OPERATORS-SPARSE-001

        Requirement: SparseMatrixQuantity owns canonical finite CSR data without
        exposing mutable maintained storage.

        Acceptance: A three-by-three tridiagonal matrix stores seven nonzeros in
        immutable arrays, reconstructs exactly, and returned CSR mutation cannot alter
        the maintained value.
        """
        source = sparse.diags(
            ([-1.0, -1.0], [2.0, 2.0, 2.0], [-1.0, -1.0]),
            offsets=(-1, 0, 1),
            format="csr",
        )
        quantity = SparseMatrixQuantity.from_csr(source, Unitless())

        assert quantity.shape == (3, 3)
        assert quantity.nonzero_count == 7
        assert not quantity.data.flags.writeable
        assert not quantity.column_indices.flags.writeable
        assert not quantity.row_offsets.flags.writeable
        np.testing.assert_array_equal(quantity.to_csr().toarray(), source.toarray())
        returned = quantity.to_csr()
        returned[0, 0] = 99.0
        assert quantity.to_csr()[0, 0] == 2.0

    def test_constructor__canonical_csr_invariants__reject_invalid_storage(
        self,
    ) -> None:
        """Evidence ID: SV-OPERATORS-SPARSE-002

        Requirement: Direct construction enforces canonical CSR structure and the
        public real-numeric contract rather than relying on SciPy normalization.

        Acceptance: Explicit stored zeros and Boolean sparse values are rejected.
        """
        with pytest.raises(ValueError, match="explicit zeros"):
            SparseMatrixQuantity(
                data=np.array([0.0]),
                column_indices=np.array([0], dtype=np.int64),
                row_offsets=np.array([0, 1], dtype=np.int64),
                shape=(1, 1),
                unit=Unitless(),
            )
        with pytest.raises(TypeError, match="excluding booleans"):
            SparseMatrixQuantity.from_csr(
                sparse.csr_array([[True]], dtype=np.bool_), Unitless()
            )
