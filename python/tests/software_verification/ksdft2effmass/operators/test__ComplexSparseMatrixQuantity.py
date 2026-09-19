r"""Software verification of ``ComplexSparseMatrixQuantity``.

Evidence profile: routine

Bounded artifact scope: immutable canonical complex128 CSR quantities and explicit
sparse/dense conversion boundaries.

Facet and represented meaning

The DataObject owns finite complex CSR values, canonical structure, shape, and one
explicit unit without implicit densification.

Intrinsic and cross-object scope

Duplicate summation, zero elimination, sorted indices, immutable storage, fresh-copy
conversion, and adverse input families are included.

VVUQ and scientific exclusions

This verifies represented storage, not Hermiticity, a finite-lattice constructor,
scientific validation, uncertainty quantification, or human acceptance.
"""

import numpy as np
import pytest
from scipy import sparse  # type: ignore[import-untyped]

from ksdft2effmass.operators import ComplexSparseMatrixQuantity, Unitless

pytestmark = pytest.mark.software_verification
SUT = ComplexSparseMatrixQuantity


class TestComplexSparseMatrixQuantity:
    """Own software evidence for ``ComplexSparseMatrixQuantity``."""

    def test_method__from_csr__canonicalizes_and_owns_complex_storage(self) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-SPARSE-001

        Requirement: The factory canonicalizes complex sparse input into immutable CSR.

        Acceptance: Duplicate entries sum, an explicit zero disappears, stored arrays
        are immutable, and mutation of a returned CSR array cannot alter the quantity.
        """
        source = sparse.coo_array(
            (
                np.array([1.0 + 2.0j, 2.0 - 1.0j, 0.0 + 0.0j, 4.0j]),
                (np.array([0, 0, 0, 1]), np.array([1, 1, 0, 0])),
            ),
            shape=(2, 2),
        )
        quantity = ComplexSparseMatrixQuantity.from_csr(source, Unitless())

        assert quantity.shape == (2, 2)
        assert quantity.nonzero_count == 2
        assert not quantity.data.flags.writeable
        assert not quantity.column_indices.flags.writeable
        assert not quantity.row_offsets.flags.writeable
        np.testing.assert_array_equal(
            quantity.to_csr().toarray(),
            np.array([[0.0 + 0.0j, 3.0 + 1.0j], [0.0 + 4.0j, 0.0 + 0.0j]]),
        )
        returned = quantity.to_csr()
        returned[0, 1] = 99.0
        assert quantity.to_csr()[0, 1] == 3.0 + 1.0j
        np.testing.assert_array_equal(
            quantity.to_dense().magnitude, quantity.to_csr().toarray()
        )

    def test_constructor__canonical_csr_invariants__rejects_invalid_storage(
        self,
    ) -> None:
        """Evidence ID: SV-OPERATORS-COMPLEX-SPARSE-002

        Requirement: Direct construction enforces canonical CSR and numeric types.

        Acceptance: An explicit complex zero and Boolean sparse matrix are rejected.
        """
        with pytest.raises(ValueError, match="explicit zeros"):
            ComplexSparseMatrixQuantity(
                data=np.array([0.0 + 0.0j]),
                column_indices=np.array([0], dtype=np.int64),
                row_offsets=np.array([0, 1], dtype=np.int64),
                shape=(1, 1),
                unit=Unitless(),
            )
        with pytest.raises(TypeError, match="excluding booleans"):
            ComplexSparseMatrixQuantity.from_csr(
                sparse.csr_array([[True]], dtype=np.bool_), Unitless()
            )
