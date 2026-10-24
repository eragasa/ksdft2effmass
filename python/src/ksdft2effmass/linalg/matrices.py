"""Compatibility names for canonical PhysKit matrix verification.

PhysKit owns raw/quantity matrix admission, immutable canonicalization, dense
conversion, and sparse-safe Hermiticity decisions. This module re-exports the exact
PhysKit objects without wrappers.
"""

from projectkoios.physkit.linalg import (
    CsrSparseMatrix,
    MatrixVerifier,
    VerifiedMatrix,
    VerifiedMatrixUtils,
)

__all__ = [
    "CsrSparseMatrix",
    "MatrixVerifier",
    "VerifiedMatrix",
    "VerifiedMatrixUtils",
]
