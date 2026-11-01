"""Immutable rank-one alignment-applicability result."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import ClassVar, Self

from projectkoios.physkit.periodic.lattice import DirectLattice1D
from projectkoios.physkit.units import PhysicalUnit

from ksdft2effmass.gauge_alignment import GaugeAlignmentGroupIdentity
from ksdft2effmass.periodic1d.fourier_locality import (
    Periodic1DFourierLocalityConfiguration,
)
from ksdft2effmass.periodic1d.gauge_alignment import Periodic1DGaugeAlignment
from ksdft2effmass.periodic1d.geometry import Periodic1DLatticeGeometry
from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue

from .definition import Periodic1DRank1AlignmentApplicability


@dataclass(frozen=True, slots=True)
class Periodic1DRank1AlignmentApplicabilityResult(
    BaseTypedRecord,
    Periodic1DGaugeAlignment,
):
    """Retain the exact scalar boundary without duplicate alignment channels."""

    configuration: Periodic1DFourierLocalityConfiguration
    lattice_geometry: Periodic1DLatticeGeometry
    gauge_group_identity: GaugeAlignmentGroupIdentity
    applicability: Periodic1DRank1AlignmentApplicability
    inapplicable_alignment_controls: tuple[str, ...]

    GAUGE_GROUP_IDENTITY: ClassVar[GaugeAlignmentGroupIdentity] = (
        GaugeAlignmentGroupIdentity.unitary(represented_dimension=1)
    )
    INAPPLICABLE_ALIGNMENT_CONTROLS: ClassVar[tuple[str, ...]] = (
        "global-unitary",
        "pointwise-unitary",
        "known-inverse-oracle",
        "restricted-internal-rotation",
    )

    def __post_init__(self) -> None:
        """Reject alternate ranks, gauge groups, or duplicate-channel inventories."""
        if type(self.configuration) is not Periodic1DFourierLocalityConfiguration:
            raise TypeError(
                "configuration must be Periodic1DFourierLocalityConfiguration"
            )
        if type(self.lattice_geometry) is not Periodic1DLatticeGeometry:
            raise TypeError("lattice_geometry must be Periodic1DLatticeGeometry")
        if type(self.gauge_group_identity) is not GaugeAlignmentGroupIdentity:
            raise TypeError(
                "gauge_group_identity must be GaugeAlignmentGroupIdentity"
            )
        if self.gauge_group_identity != self.GAUGE_GROUP_IDENTITY:
            raise ValueError("rank-one alignment must use the unitary group U(1)")
        if type(self.applicability) is not Periodic1DRank1AlignmentApplicability:
            raise TypeError("applicability must be the exact rank-one enum")
        if (
            self.applicability
            is not Periodic1DRank1AlignmentApplicability.OPERATOR_TRIVIAL
        ):
            raise ValueError("rank-one internal alignment must be operator-trivial")
        if type(self.inapplicable_alignment_controls) is not tuple or any(
            type(value) is not str for value in self.inapplicable_alignment_controls
        ):
            raise TypeError(
                "inapplicable_alignment_controls must be a tuple of built-in strings"
            )
        if (
            self.inapplicable_alignment_controls
            != self.INAPPLICABLE_ALIGNMENT_CONTROLS
        ):
            raise ValueError(
                "inapplicable alignment controls must match the scalar boundary"
            )

    @property
    def retained_rank(self) -> int:
        """Return the represented scalar retained-space dimension."""
        return self.gauge_group_identity.represented_dimension

    @property
    def gauge_group(self) -> str:
        """Return the conventional rank-one unitary-group label."""
        return self.gauge_group_identity.mathematical_label

    @property
    def direct_lattice(self) -> DirectLattice1D:
        """Return the PhysKit direct lattice for the declared reduced convention."""
        return self.lattice_geometry.direct_lattice

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "configuration": self.configuration,
            "lattice_period": self.lattice_geometry.lattice_period,
            "lattice_unit": self.lattice_geometry.lattice_unit,
            "retained_rank": self.retained_rank,
            "gauge_group": self.gauge_group,
            "applicability": self.applicability.to_wire(),
            "inapplicable_alignment_controls": self.inapplicable_alignment_controls,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        if set(values) != {
            "configuration",
            "lattice_period",
            "lattice_unit",
            "retained_rank",
            "gauge_group",
            "applicability",
            "inapplicable_alignment_controls",
        }:
            raise ValueError("rank-one alignment-applicability fields do not match")
        configuration = values["configuration"]
        lattice_period = values["lattice_period"]
        lattice_unit = values["lattice_unit"]
        retained_rank = values["retained_rank"]
        gauge_group = values["gauge_group"]
        applicability = values["applicability"]
        controls = values["inapplicable_alignment_controls"]
        if not isinstance(configuration, Mapping):
            raise TypeError("configuration must decode to a mapping")
        if type(lattice_period) is not float:
            raise TypeError("lattice_period must decode to a built-in float")
        if type(lattice_unit) is not PhysicalUnit:
            raise TypeError("lattice_unit must decode to PhysicalUnit")
        if type(gauge_group) is not str:
            raise TypeError("gauge_group must decode to a built-in string")
        if type(retained_rank) is not int:
            raise TypeError("retained_rank must decode to a built-in integer")
        if type(applicability) is not str:
            raise TypeError("applicability must decode to a built-in string")
        if not isinstance(controls, tuple) or any(
            type(value) is not str for value in controls
        ):
            raise TypeError("alignment controls must decode to a tuple of strings")
        if retained_rank != 1:
            raise ValueError("retained_rank must equal one")
        if gauge_group != "U(1)":
            raise ValueError("rank-one alignment must use U(1)")
        return cls(
            configuration=Periodic1DFourierLocalityConfiguration.from_dict(
                configuration
            ),
            lattice_geometry=Periodic1DLatticeGeometry(
                lattice_period,
                lattice_unit,
            ),
            gauge_group_identity=cls.GAUGE_GROUP_IDENTITY,
            applicability=Periodic1DRank1AlignmentApplicability.from_wire(applicability),
            inapplicable_alignment_controls=tuple(controls),
        )


__all__ = ["Periodic1DRank1AlignmentApplicabilityResult"]
