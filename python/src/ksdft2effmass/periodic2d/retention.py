"""Two-dimensional parent-qualified scientific-retention definitions.

This module connects reusable contiguous band-index selection data to the general
periodic scientific-retention contract. It does not inspect eigenvalues, establish
band isolation, construct a projector or frame, choose a gauge, create a retained
operator, or execute a campaign.
"""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.analysis.periodic_bands import ContiguousBandSelection
from ksdft2effmass.periodic import PeriodicRetentionDefinition, PeriodicRetentionKind


@dataclass(frozen=True, slots=True)
class Periodic2DSelectedBandRetentionDefinition:
    """Bind one contiguous band selection to a two-dimensional parent.

    Parameters
    ----------
    retention
        Parent-qualified general retention definition. Its parent must have exactly
        two periodic spatial dimensions, its construction kind must be
        :attr:`~ksdft2effmass.periodic.PeriodicRetentionKind.SELECTED_BANDS`, and its
        retained rank must equal the number of selected bands.
    selection
        Inclusive contiguous zero-based parent-band interval. Ascending band indices
        correspond elementwise to ``retention.ordered_state_labels``.

    Raises
    ------
    TypeError
        If either field is not the exact supported public DataObject type.
    ValueError
        If the parent is not two-dimensional, the construction kind is not selected
        bands, or retained rank differs from the selected band count.

    Attributes
    ----------
    retention
        General parent-qualified scientific-retention definition.
    selection
        Reusable inclusive contiguous parent-band selection.

    Notes
    -----
    This aggregate supplies the parent model, mathematical operator, ambient state
    space, reciprocal domain, construction-record, assumption, and provenance
    identities that a band-index interval alone lacks. It remains a retention
    definition rather than a retained mathematical subspace: it stores no projector,
    frame, gauge, represented operator, or finite matrix.

    Projection, disentanglement, basis transformation, and hopping truncation remain
    distinct operations. Construction verifies only the declared software identities,
    dimensions, ordering, and rank. It does not establish band isolation, numerical
    convergence, physical adequacy, scientific validation, uncertainty quantification,
    or any relationship among parent-model, discretization, and model-reduction error.
    """

    retention: PeriodicRetentionDefinition
    selection: ContiguousBandSelection

    def __post_init__(self) -> None:
        """Validate exact field types and two-dimensional retention semantics."""
        self._check_args_types()
        self._check_args_retention_semantics()

    def _check_args_types(self) -> None:
        """Require exact general-retention and contiguous-selection records."""
        if type(self.retention) is not PeriodicRetentionDefinition:
            raise TypeError("retention must be PeriodicRetentionDefinition")
        if type(self.selection) is not ContiguousBandSelection:
            raise TypeError("selection must be ContiguousBandSelection")

    def _check_args_retention_semantics(self) -> None:
        """Require a two-dimensional selected-band definition of matching rank."""
        # The reusable index interval cannot supply parent dimensionality or a
        # scientific construction kind; those meanings remain with the parent-qualified
        # retention definition.
        if self.retention.parent_operator.spatial_dimension != 2:
            raise ValueError("retention parent must be two-dimensional")
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
            Inclusive ascending zero-based indices. Position ``i`` corresponds to
            ``retention.ordered_state_labels[i]``.
        """
        return tuple(range(self.selection.lower_index, self.selection.upper_index + 1))


__all__ = ["Periodic2DSelectedBandRetentionDefinition"]
