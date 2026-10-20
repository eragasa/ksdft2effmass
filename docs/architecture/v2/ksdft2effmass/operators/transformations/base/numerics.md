# Numerical contract

Phase 1 performs no transformation arithmetic. Each concrete Action implements the
abstract public `transform` method and must enforce exact request/Action/result enum
agreement. The base supplies final protected validation methods for this purpose.

A kind mismatch raises `ValueError`; invalid nominal membership or raw-string kind raises
`TypeError`. Concrete operations own dimensions, dtype, precision, algorithms, residuals,
tolerances, overflow behavior, and failure dispositions.
