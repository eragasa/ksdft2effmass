"""Compatibility imports for PhysKit-owned immutable numerical quantities.

PhysKit owns model-system units, immutable dense and sparse quantities, and Pint-backed
conversion behavior. This module preserves the supported
``ksdft2effmass.operators.quantities`` import route while ensuring that ksdft2effmass
and PhysKit use the same nominal runtime types.
"""

from physkit.units.quantities import (
    MODEL_SYSTEM_PINT_REGISTRY,
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrix,
    ComplexMatrixQuantity,
    ComplexSparseMatrixQuantity,
    ComplexVector,
    IntegerVector,
    MatrixQuantity,
    ModelSystemQuantity,
    ModelSystemUnit,
    PhysicalUnit,
    PintUnitConverter,
    RealMatrix,
    RealVector,
    ScalarQuantity,
    SparseMatrixQuantity,
    Unitless,
    VectorQuantity,
)

__all__ = [
    "MODEL_SYSTEM_PINT_REGISTRY",
    "MODEL_SYSTEM_UNIT_CONVERTER",
    "ComplexMatrix",
    "ComplexMatrixQuantity",
    "ComplexSparseMatrixQuantity",
    "ComplexVector",
    "IntegerVector",
    "MatrixQuantity",
    "ModelSystemQuantity",
    "ModelSystemUnit",
    "PhysicalUnit",
    "PintUnitConverter",
    "RealMatrix",
    "RealVector",
    "ScalarQuantity",
    "SparseMatrixQuantity",
    "Unitless",
    "VectorQuantity",
]
