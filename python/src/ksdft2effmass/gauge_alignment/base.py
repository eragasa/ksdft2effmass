"""Scientific ownership and analysis-role bases for gauge alignment."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import final

from ksdft2effmass.serialization import StringWireEnum


class GaugeAlignment(ABC):  # noqa: B024 - intentionally nominal marker
    """Identify a gauge-alignment capability or its exact applicability boundary.

    Concrete subclasses must state the represented state space, gauge group, action
    convention, and whether a nontrivial alignment exists. Membership does not imply
    representation equivalence, frame transport, coefficient locality, support
    truncation, or successful numerical recovery. This base owns no solver, tolerance,
    acceptance policy, or wire format.
    """

    __slots__ = ()


class GaugeAlignmentActionConvention(StringWireEnum):
    """Identify which side of a represented frame receives the gauge action."""

    LEFT = "left"
    RIGHT = "right"


class GaugeAlignmentInnerProductConvention(StringWireEnum):
    """Identify the inner-product convention used by the alignment objective."""

    EUCLIDEAN_ORTHONORMAL = "euclidean-orthonormal"


class GaugeAlignmentGroupFamily(StringWireEnum):
    """Classify the transformation constraint defining a gauge group.

    Group family does not encode the represented inner product. For example,
    metric-unitary and Euclidean-unitary actions share the unitary family but require
    different inner-product conventions and numerical objectives.
    """

    UNITARY = "unitary"


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GaugeAlignmentGroupIdentity:
    """Bind one gauge-group family to its finite represented dimension."""

    family: GaugeAlignmentGroupFamily
    represented_dimension: int

    def __post_init__(self) -> None:
        if type(self.family) is not GaugeAlignmentGroupFamily:
            raise TypeError("family must be GaugeAlignmentGroupFamily")
        if type(self.represented_dimension) is not int:
            raise TypeError("represented_dimension must be a built-in integer")
        if self.represented_dimension <= 0:
            raise ValueError("represented_dimension must be positive")

    @classmethod
    def unitary(cls, *, represented_dimension: int) -> GaugeAlignmentGroupIdentity:
        """Return the unitary family in one finite represented dimension."""
        return cls(
            family=GaugeAlignmentGroupFamily.UNITARY,
            represented_dimension=represented_dimension,
        )

    @property
    def mathematical_label(self) -> str:
        """Return the conventional finite-dimensional group label."""
        if self.family is GaugeAlignmentGroupFamily.UNITARY:
            return f"U({self.represented_dimension})"
        raise RuntimeError("unsupported gauge-alignment group family")


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GaugeAlignmentAnalysisIdentity:
    """Retain the common finite scientific identity of one alignment analysis."""

    gauge_group_identity: GaugeAlignmentGroupIdentity
    alignment_sample_count: int
    action_convention: GaugeAlignmentActionConvention
    inner_product_convention: GaugeAlignmentInnerProductConvention

    def __post_init__(self) -> None:
        if type(self.gauge_group_identity) is not GaugeAlignmentGroupIdentity:
            raise TypeError(
                "gauge_group_identity must be GaugeAlignmentGroupIdentity"
            )
        if type(self.alignment_sample_count) is not int:
            raise TypeError("alignment_sample_count must be a built-in integer")
        if self.alignment_sample_count <= 0:
            raise ValueError("alignment_sample_count must be positive")
        if type(self.action_convention) is not GaugeAlignmentActionConvention:
            raise TypeError(
                "action_convention must be GaugeAlignmentActionConvention"
            )
        if (
            type(self.inner_product_convention)
            is not GaugeAlignmentInnerProductConvention
        ):
            raise TypeError(
                "inner_product_convention must be "
                "GaugeAlignmentInnerProductConvention"
            )

    @property
    def retained_rank(self) -> int:
        """Return the dimension on which the retained gauge group acts."""
        return self.gauge_group_identity.represented_dimension

    @property
    def gauge_group(self) -> str:
        """Return the conventional finite-dimensional gauge-group label."""
        return self.gauge_group_identity.mathematical_label


class _GaugeAlignmentAnalysisIdentityOwner(GaugeAlignment, ABC):
    """Provide validated common accessors from one explicit analysis identity."""

    __slots__ = ()

    @property
    @abstractmethod
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the immutable finite scientific identity of this analysis role."""

    @property
    @final
    def retained_rank(self) -> int:
        """Return the dimension of the represented retained state space."""
        return self.analysis_identity.retained_rank

    @property
    @final
    def gauge_group(self) -> str:
        """Return the explicitly declared retained-space gauge-group label."""
        return self.analysis_identity.gauge_group

    @property
    @final
    def gauge_group_identity(self) -> GaugeAlignmentGroupIdentity:
        """Return the typed family and represented dimension of the gauge group."""
        return self.analysis_identity.gauge_group_identity

    @property
    @final
    def alignment_sample_count(self) -> int:
        """Return the number of ordered samples covered by the analysis."""
        return self.analysis_identity.alignment_sample_count

    @property
    @final
    def action_convention(self) -> GaugeAlignmentActionConvention:
        """Return the side on which the represented gauge transformation acts."""
        return self.analysis_identity.action_convention

    @property
    @final
    def inner_product_convention(self) -> GaugeAlignmentInnerProductConvention:
        """Return the inner-product convention used by the alignment objective."""
        return self.analysis_identity.inner_product_convention


class GaugeAlignmentAnalysisRequest(_GaugeAlignmentAnalysisIdentityOwner, ABC):
    """Bind the common scientific identity of one finite alignment analysis."""

    __slots__ = ()


class GaugeAlignmentAnalysis(_GaugeAlignmentAnalysisIdentityOwner, ABC):
    """Expose the common scientific identity retained by an alignment analysis."""

    __slots__ = ()


class GaugeAlignmentAnalyzer[
    GaugeAlignmentAnalysisRequestT: GaugeAlignmentAnalysisRequest,
    GaugeAlignmentAnalysisT: GaugeAlignmentAnalysis,
](_GaugeAlignmentAnalysisIdentityOwner, ABC):
    """Execute one exact request and return one gauge-alignment analysis."""

    __slots__ = ()

    @property
    @abstractmethod
    def request(self) -> GaugeAlignmentAnalysisRequestT:
        """Return the complete immutable request bound to this action."""

    @property
    @final
    def analysis_identity(self) -> GaugeAlignmentAnalysisIdentity:
        """Return the scientific identity delegated by the bound request."""
        return self.request.analysis_identity

    @abstractmethod
    def execute(self) -> GaugeAlignmentAnalysisT:
        """Execute the bound gauge-alignment analysis without external effects."""


__all__ = [
    "GaugeAlignment",
    "GaugeAlignmentActionConvention",
    "GaugeAlignmentAnalysis",
    "GaugeAlignmentAnalysisIdentity",
    "GaugeAlignmentAnalysisRequest",
    "GaugeAlignmentAnalyzer",
    "GaugeAlignmentGroupFamily",
    "GaugeAlignmentGroupIdentity",
    "GaugeAlignmentInnerProductConvention",
]
