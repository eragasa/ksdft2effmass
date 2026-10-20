# Numerical contract

The interface inherits square source/target dimensions and domain correlation. It adds no
norm, eigensolve, residual, tolerance, dtype, or precision rule.

A non-Hermitian finite square matrix is a valid implementation value until a separate
Hermiticity requirement is declared and evaluated.
