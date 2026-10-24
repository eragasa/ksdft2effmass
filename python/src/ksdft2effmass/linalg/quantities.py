"""Compatibility names for canonical PhysKit numerical quantities.

PhysKit owns the immutable unit-bearing quantity implementations. This module retains
KSD's established import names as exact aliases; it defines no wrapper or conversion
record.
"""

from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    MatrixQuantity,
    ModelSystemUnit,
    PhysicalUnit,
    PintUnitConverter,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

RealMatrixQuantity = MatrixQuantity
"""Compatibility alias for PhysKit's real dense matrix quantity."""

CsrRealMatrixQuantity = SparseMatrixQuantity
"""Compatibility alias for PhysKit's real canonical-CSR matrix quantity."""

CsrComplexMatrixQuantity = ComplexSparseMatrixQuantity
"""Compatibility alias for PhysKit's complex canonical-CSR matrix quantity."""

__all__ = [
    "ComplexMatrixQuantity",
    "CsrComplexMatrixQuantity",
    "CsrRealMatrixQuantity",
    "ModelSystemUnit",
    "PhysicalUnit",
    "PintUnitConverter",
    "RealMatrixQuantity",
    "ScalarQuantity",
    "Unitless",
    "VectorQuantity",
]
