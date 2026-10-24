"""Software verification of the KSD-to-PhysKit linear-algebra boundary."""

from projectkoios.physkit import linalg as physkit_linalg
from projectkoios.physkit import units as physkit_units

from ksdft2effmass import linalg


class TestPhysKitLinearAlgebraOwnership:
    """Require KSD compatibility names to retain exact PhysKit identities."""

    def test_quantity_names__are_exact_physkit_objects(self) -> None:
        """KSD quantity names must not introduce wrappers or conversion copies."""
        assert linalg.PhysicalUnit is physkit_units.PhysicalUnit
        assert linalg.Unitless is physkit_units.Unitless
        assert linalg.ModelSystemUnit is physkit_units.ModelSystemUnit
        assert linalg.ScalarQuantity is physkit_units.ScalarQuantity
        assert linalg.VectorQuantity is physkit_units.VectorQuantity
        assert linalg.RealMatrixQuantity is physkit_units.MatrixQuantity
        assert linalg.ComplexMatrixQuantity is physkit_units.ComplexMatrixQuantity
        assert linalg.CsrRealMatrixQuantity is physkit_units.SparseMatrixQuantity
        assert (
            linalg.CsrComplexMatrixQuantity is physkit_units.ComplexSparseMatrixQuantity
        )
        assert linalg.PintUnitConverter is physkit_units.PintUnitConverter
        assert not hasattr(linalg, "MODEL_SYSTEM_UNIT_CONVERTER")
        assert not hasattr(linalg, "ModelSystemUnitConverter")

    def test_matrix_verification_names__are_exact_physkit_objects(self) -> None:
        """KSD matrix verification must expose the canonical PhysKit behavior."""
        assert linalg.MatrixVerifier is physkit_linalg.MatrixVerifier
        assert linalg.VerifiedMatrixUtils is physkit_linalg.VerifiedMatrixUtils
        assert linalg.VerifiedMatrix is physkit_linalg.VerifiedMatrix
        assert linalg.CsrSparseMatrix is physkit_linalg.CsrSparseMatrix
