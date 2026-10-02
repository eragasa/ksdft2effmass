"""One-dimensional parent-qualified scientific-retention definitions.

This module connects reusable band-index selection data to the general periodic
scientific-retention contract. It does not select bands, inspect eigenvalues,
construct a projector or frame, choose a gauge, or execute a campaign.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.periodic import PeriodicRetentionDefinition, PeriodicRetentionKind


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


__all__ = ["Periodic1DSelectedBandRetentionDefinition"]
