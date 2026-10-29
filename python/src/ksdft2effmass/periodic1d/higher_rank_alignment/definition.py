"""Closed protocol identities and dispositions for higher-rank alignment."""

from __future__ import annotations

from enum import StrEnum


class Periodic1DHigherRankAlignmentChannel(StrEnum):
    """Identify one frozen higher-rank alignment family."""

    IDENTITY = "A0"
    GLOBAL_UNITARY = "A1"
    POINTWISE_UNITARY = "A2"
    KNOWN_INVERSE_ORACLE = "A3"


class Periodic1DHigherRankAlignmentStatus(StrEnum):
    """Retain the exact disposition of one alignment channel."""

    QUALIFIED = "qualified"
    AGGREGATE_RANK_DEFICIENT = "aggregate-rank-deficient"
    POINTWISE_RANK_DEFICIENT = "pointwise-rank-deficient"
    NUMERICALLY_UNRESOLVED = "alignment-numerically-unresolved"
    INTEGRITY_FAILED = "alignment-integrity-failed"
    ORACLE_INTEGRITY_FAILED = "oracle-integrity-failed"


class Periodic1DHigherRankGlobalUnitaryDownstreamApplicability(StrEnum):
    """State whether the global-unitary channel has downstream values."""

    APPLICABLE = "applicable"
    INAPPLICABLE_AGGREGATE_RANK_DEFICIENT = "inapplicable-aggregate-rank-deficient"


class Periodic1DHigherRankAlignmentBackendExceptionCode(StrEnum):
    """Classify an alignment backend failure without retaining exception text."""

    ARITHMETIC_NONFINITE = "backend-arithmetic-nonfinite"
    NONCONVERGENCE = "backend-nonconvergence"
    VALIDATION_FAILED = "backend-validation-failed"


__all__ = [
    "Periodic1DHigherRankGlobalUnitaryDownstreamApplicability",
    "Periodic1DHigherRankAlignmentBackendExceptionCode",
    "Periodic1DHigherRankAlignmentChannel",
    "Periodic1DHigherRankAlignmentStatus",
]
