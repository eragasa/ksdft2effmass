"""Calculation-owned retained-basis inventory for the rank-N analytic study."""

from __future__ import annotations

import numpy as np
from analytic_parent import ControlPeriodic1DRankNAnalyticParentModel

from ksdft2effmass.periodic.operators import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisInventory,
    PeriodicBasisInventoryEntry,
)
from ksdft2effmass.periodic.periodic1d.operators import Periodic1DBasisIdentity


def _entry(
    *,
    retained_rank: int,
    display_identifier: str,
    labels: tuple[str, ...],
) -> PeriodicBasisInventoryEntry[Periodic1DBasisIdentity]:
    return PeriodicBasisInventoryEntry(
        retained_rank=retained_rank,
        basis_identity=Periodic1DBasisIdentity(
            display_identifier=display_identifier,
            coordinates=tuple(
                LabeledComponentBasisCoordinate(label=label) for label in labels
            ),
        ),
    )


CONTROL_BASIS_INVENTORY: PeriodicBasisInventory[Periodic1DBasisIdentity] = (
    PeriodicBasisInventory(
        entries=(
            _entry(
                retained_rank=3,
                display_identifier="periodic1d-rankN-control-retained-basis-r03",
                labels=(
                    "retained-orbital-00",
                    "retained-orbital-01",
                    "retained-orbital-02",
                ),
            ),
            _entry(
                retained_rank=4,
                display_identifier="periodic1d-rankN-control-retained-basis-r04",
                labels=(
                    "retained-orbital-00",
                    "retained-orbital-01",
                    "retained-orbital-02",
                    "retained-orbital-03",
                ),
            ),
            _entry(
                retained_rank=8,
                display_identifier="periodic1d-rankN-control-retained-basis-r08",
                labels=(
                    "retained-orbital-00",
                    "retained-orbital-01",
                    "retained-orbital-02",
                    "retained-orbital-03",
                    "retained-orbital-04",
                    "retained-orbital-05",
                    "retained-orbital-06",
                    "retained-orbital-07",
                ),
            ),
            _entry(
                retained_rank=16,
                display_identifier="periodic1d-rankN-control-retained-basis-r16",
                labels=(
                    "retained-orbital-00",
                    "retained-orbital-01",
                    "retained-orbital-02",
                    "retained-orbital-03",
                    "retained-orbital-04",
                    "retained-orbital-05",
                    "retained-orbital-06",
                    "retained-orbital-07",
                    "retained-orbital-08",
                    "retained-orbital-09",
                    "retained-orbital-10",
                    "retained-orbital-11",
                    "retained-orbital-12",
                    "retained-orbital-13",
                    "retained-orbital-14",
                    "retained-orbital-15",
                ),
            ),
        )
    )
)


def control_parent_model(
    retained_rank: int,
) -> ControlPeriodic1DRankNAnalyticParentModel:
    """Construct the calculation-owned analytic parent for one retained rank."""
    ambient_dimension = 2 * retained_rank
    frame = np.zeros((ambient_dimension, retained_rank), dtype=np.complex128)
    frame[:retained_rank] = np.eye(retained_rank, dtype=np.complex128)
    return ControlPeriodic1DRankNAnalyticParentModel(
        retained_rank=retained_rank,
        basis=CONTROL_BASIS_INVENTORY.basis_identity_for_rank(retained_rank),
        reference_frame=frame,
        sewing_map=np.eye(ambient_dimension, dtype=np.complex128),
    )


__all__ = ["CONTROL_BASIS_INVENTORY", "control_parent_model"]
