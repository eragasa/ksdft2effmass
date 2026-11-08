"""Calculation-owned retained-basis inventory for the periodic-2D rank-N baseline.

This module composes immutable source-domain values only. Importing it performs no
scientific calculation and creates no retained evidence.
"""

from ksdft2effmass.periodic.operators import (
    LabeledComponentBasisCoordinate,
    PeriodicBasisInventory,
    PeriodicBasisInventoryEntry,
)
from ksdft2effmass.periodic.periodic2d.operators import Periodic2DBasisIdentity

PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY: PeriodicBasisInventory[
    Periodic2DBasisIdentity
] = PeriodicBasisInventory(
    entries=(
        PeriodicBasisInventoryEntry(
            retained_rank=3,
            basis_identity=Periodic2DBasisIdentity(
                display_identifier="periodic2d-rankN-control-retained-basis-r3",
                coordinates=(
                    LabeledComponentBasisCoordinate(label="retained-orbital-00"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-01"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-02"),
                ),
            ),
        ),
        PeriodicBasisInventoryEntry(
            retained_rank=4,
            basis_identity=Periodic2DBasisIdentity(
                display_identifier="periodic2d-rankN-control-retained-basis-r4",
                coordinates=(
                    LabeledComponentBasisCoordinate(label="retained-orbital-00"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-01"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-02"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-03"),
                ),
            ),
        ),
        PeriodicBasisInventoryEntry(
            retained_rank=8,
            basis_identity=Periodic2DBasisIdentity(
                display_identifier="periodic2d-rankN-control-retained-basis-r8",
                coordinates=(
                    LabeledComponentBasisCoordinate(label="retained-orbital-00"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-01"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-02"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-03"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-04"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-05"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-06"),
                    LabeledComponentBasisCoordinate(label="retained-orbital-07"),
                ),
            ),
        ),
    )
)


__all__ = ["PERIODIC2D_RANK_N_CONTROL_BASIS_INVENTORY"]
