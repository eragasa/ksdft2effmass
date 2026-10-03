"""One-dimensional parent-qualified scientific-retention definitions.

This module connects reusable band-index selection data to the general periodic
scientific-retention contract. It does not select bands, inspect eigenvalues,
construct a projector or frame, choose a gauge, or execute a campaign.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.operators import OrthogonalSpectralSubspace
from ksdft2effmass.periodic import (
    PeriodicRetainedSubspace,
    PeriodicRetentionDefinition,
    PeriodicRetentionKind,
)


@dataclass(frozen=True, slots=True)
class Periodic1DSelectedBandRetentionDefinition:
    """Bind one contiguous band selection to a one-dimensional parent.

    Parameters
    ----------
    retention
        Parent-qualified general retention definition. Its parent must have
        spatial dimension one, its kind must be
        :attr:`~ksdft2effmass.periodic.PeriodicRetentionKind.SELECTED_BANDS`,
        and its rank must equal the number of selected bands.
    selection
        Inclusive contiguous zero-based parent-band interval. The ascending band
        indices correspond elementwise to ``retention.ordered_state_labels``.

    Raises
    ------
    TypeError
        If either field is not the exact supported public DataObject type.
    ValueError
        If the parent is not one-dimensional, retention kind is not selected
        bands, or retained rank differs from the selected band count.

    Attributes
    ----------
    retention
        General parent-qualified scientific-retention definition.
    selection
        Reusable inclusive contiguous band selection.

    Notes
    -----
    The aggregate supplies parent operator, ambient state space, reciprocal
    domain, construction-record, assumption, and provenance identities that a
    band-index interval alone lacks. It remains a retention definition rather
    than a retained subspace: no projector, frame, gauge, or numerical operator
    is stored.

    Construction is software verification of exact identity and dimension
    relations. It does not establish band isolation, projector accuracy,
    physical adequacy, numerical verification, scientific validation, or
    uncertainty quantification.
    """

    retention: PeriodicRetentionDefinition
    selection: ContiguousBandSelection

    def __post_init__(self) -> None:
        """Validate one-dimensional parentage, kind, and selected rank."""
        if type(self.retention) is not PeriodicRetentionDefinition:
            raise TypeError("retention must be PeriodicRetentionDefinition")
        if type(self.selection) is not ContiguousBandSelection:
            raise TypeError("selection must be ContiguousBandSelection")
        if self.retention.parent_operator.spatial_dimension != 1:
            raise ValueError("retention parent must be one-dimensional")
        if self.retention.kind is not PeriodicRetentionKind.SELECTED_BANDS:
            raise ValueError("retention kind must be selected bands")
        if self.retention.rank != self.selection.band_count:
            raise ValueError("retention rank must equal selected band count")

    @property
    def band_indices(self) -> tuple[int, ...]:
        """Return selected parent-band indices in retained-state order.

        Returns
        -------
        tuple[int, ...]
            Inclusive ascending zero-based indices from ``lower_index`` through
            ``upper_index``. Position ``i`` corresponds to
            ``retention.ordered_state_labels[i]``.
        """
        return tuple(range(self.selection.lower_index, self.selection.upper_index + 1))


@dataclass(frozen=True, slots=True)
class Periodic1DRetainedBandGroupDefinition:
    """Identify one named parent-qualified retained band group.

    Parameters
    ----------
    identifier
        Stable nonempty group identity within its owning campaign definition.
    retained_bands
        Parent-qualified selected-band retention definition.

    Raises
    ------
    TypeError
        If either field has the wrong exact semantic type.
    ValueError
        If ``identifier`` is empty.

    Notes
    -----
    The group adds a campaign-facing name without weakening or duplicating parent,
    operator, state-space, reciprocal-domain, construction, assumption, or provenance
    identities owned by ``retained_bands``. It is a retention definition, not a
    projector, frame, represented matrix, or effective model.
    """

    identifier: str
    retained_bands: Periodic1DSelectedBandRetentionDefinition

    def __post_init__(self) -> None:
        """Validate exact group identity and selected-band definition type."""
        if type(self.identifier) is not str:
            raise TypeError("identifier must be a built-in str")
        if self.identifier == "":
            raise ValueError("identifier must be nonempty")
        if type(self.retained_bands) is not Periodic1DSelectedBandRetentionDefinition:
            raise TypeError(
                "retained_bands must be Periodic1DSelectedBandRetentionDefinition"
            )

    @property
    def selection(self) -> ContiguousBandSelection:
        """Return the reusable contiguous parent-band selection."""
        return self.retained_bands.selection

    @property
    def lower_index(self) -> int:
        """Return the first selected zero-based parent-band index."""
        return self.selection.lower_index

    @property
    def upper_index(self) -> int:
        """Return the last selected zero-based parent-band index."""
        return self.selection.upper_index

    @property
    def band_count(self) -> int:
        """Return the retained group rank."""
        return self.retained_bands.retention.rank


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DOrthogonalSpectralRetainedSubspace:
    """Bind numerical eigenspace coordinates to one scientific retained space.

    Parameters
    ----------
    retained_subspace
        Parent-qualified one-dimensional retained mathematical space, including its
        ambient state-space, reciprocal-domain, construction, and provenance identity.
    represented_subspace
        Immutable numerical eigenvalues and orthonormal column embedding.

    Raises
    ------
    TypeError
        If either field has the wrong exact public type.
    ValueError
        If the scientific space is not one-dimensional or its retained and ambient
        dimensions disagree with the numerical eigenspace representation.

    Notes
    -----
    The numerical embedding represents, but does not define, the scientific retained
    space. Construction does not establish parent alignment, numerical convergence,
    physical adequacy, scientific validation, or uncertainty quantification.
    """

    retained_subspace: PeriodicRetainedSubspace
    represented_subspace: OrthogonalSpectralSubspace

    def __post_init__(self) -> None:
        """Validate exact types, one-dimensional parentage, and dimensions."""
        if type(self.retained_subspace) is not PeriodicRetainedSubspace:
            raise TypeError("retained_subspace must be PeriodicRetainedSubspace")
        if type(self.represented_subspace) is not OrthogonalSpectralSubspace:
            raise TypeError("represented_subspace must be OrthogonalSpectralSubspace")
        if self.retained_subspace.spatial_dimension != 1:
            raise ValueError("retained_subspace parent must be one-dimensional")
        if self.retained_subspace.rank != self.represented_subspace.retained_dimension:
            raise ValueError("retained dimensions must agree")
        if (
            self.retained_subspace.ambient_dimension
            != self.represented_subspace.full_dimension
        ):
            raise ValueError("ambient dimensions must agree")


__all__ = [
    "Periodic1DOrthogonalSpectralRetainedSubspace",
    "Periodic1DRetainedBandGroupDefinition",
    "Periodic1DSelectedBandRetentionDefinition",
]
