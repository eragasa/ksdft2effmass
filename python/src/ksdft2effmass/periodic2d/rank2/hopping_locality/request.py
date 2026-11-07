"""Periodic-2D rank-two hopping-locality request values."""

from __future__ import annotations

from dataclasses import dataclass

from ksdft2effmass.periodic.periodic2d.rank2.models import (
    Periodic2DRank2BlockHoppingModel,
)

from .base import Periodic2DRank2HoppingLocalityAnalysisRequestRole


@dataclass(frozen=True, slots=True)
class Periodic2DRank2HoppingLocalityAnalysisRequest(
    Periodic2DRank2HoppingLocalityAnalysisRequestRole
):
    """Bind one exact periodic-2D model to its metric-shell inventory.

    Parameters
    ----------
    model
        Complete exact periodic-2D rank-two block-hopping scientific model.
    shell_indices
        Nonnegative metric-shell label for each provider term in provider order.

    Raises
    ------
    TypeError
        If any value lacks its exact nominal owner.
    ValueError
        If shell labels do not match the provider term inventory or are negative.

    Notes
    -----
    The request describes one model only. Reference or comparison roles belong to an
    explicit higher-level study composition and are not locality inputs.

    """

    model: Periodic2DRank2BlockHoppingModel
    shell_indices: tuple[int, ...]

    def __post_init__(self) -> None:
        """Validate exact model ownership and term-to-shell correlation.

        Raises
        ------
        TypeError
            If model or shell labels lack their exact runtime types.
        ValueError
            If shell labels do not cover every hopping term exactly once by order or
            contain a negative value.

        """
        if type(self.model) is not Periodic2DRank2BlockHoppingModel:
            raise TypeError("model must be Periodic2DRank2BlockHoppingModel")
        if type(self.shell_indices) is not tuple or any(
            type(shell_index) is not int for shell_index in self.shell_indices
        ):
            raise TypeError("shell_indices must contain built-in integers")
        # Shell labels are positional metadata over immutable provider term order;
        # accepting a different length would silently misattribute hopping power.
        if len(self.shell_indices) != len(self.model.block_hopping_model.terms):
            raise ValueError("shell_indices must match the hopping term count")
        if any(shell_index < 0 for shell_index in self.shell_indices):
            raise ValueError("shell_indices must be nonnegative")

    @property
    def identifier(self) -> str:
        """Return the stable scientific-model identity.

        Returns
        -------
        str
            Exact model identity used to correlate the locality result.

        """
        return self.model.model_id


__all__ = ["Periodic2DRank2HoppingLocalityAnalysisRequest"]
