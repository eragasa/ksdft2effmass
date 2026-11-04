"""Typed periodic-2D arbitrary-rank aggregate study definitions."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import ClassVar, Self, cast

import numpy as np
from projectkoios.numerics.numpy.typing import Float64Array
from projectkoios.optimization.alignment.procrustes import (
    ComplexUnitaryProcrustesRankCutoffRule,
    ComplexUnitaryProcrustesTolerance,
)
from projectkoios.physkit.periodic.lattice import DirectLattice2D, DirectLatticeMetric

from ksdft2effmass.periodic2d.rankN.band_equivalence_hopping_locality.base import (
    Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
)
from ksdft2effmass.periodic2d.rankN.gauge_alignment.definition import (
    Periodic2DRankNGaugeAlignment,
)
from ksdft2effmass.real_space_support_truncation import BasisResolvedMetricGeometry
from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StrWireEnum,
)

from .model import Periodic2DRankNGaugeNormalizationEnum


class Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum(StrWireEnum):
    """Identify one independently interpreted periodic-2D rank-N family."""

    ORTHOGONAL = (
        "ksdft2effmass.periodic2d-rankN-orthogonal-band-equivalence-hopping-locality.v1"
    )
    NONORTHOGONAL = (
        "ksdft2effmass.periodic2d-rankN-nonorthogonal-"
        "band-equivalence-hopping-locality.v1"
    )


@dataclass(frozen=True, slots=True)
class Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition(
    BaseTypedRecord,
    BasisResolvedMetricGeometry,
):
    """Bind one reviewed lattice geometry and gauge-normalization convention."""

    identifier: str
    positive_bonds: tuple[tuple[int, int], ...]
    gauge_normalization: Periodic2DRankNGaugeNormalizationEnum
    direct_metric: DirectLatticeMetric
    shell_metric_scale: float
    basis_offsets: tuple[tuple[float, float], ...] = ()
    dimension: int = field(init=False, default=2, repr=False)

    def __post_init__(self) -> None:
        if type(self.identifier) is not str or not self.identifier:
            raise TypeError("identifier must be a nonempty built-in string")
        if type(self.positive_bonds) is not tuple or not self.positive_bonds:
            raise TypeError("positive_bonds must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != 2
            or any(type(component) is not int for component in bond)
            or bond == (0, 0)
            for bond in self.positive_bonds
        ):
            raise TypeError("positive_bonds must contain nonzero integer pairs")
        if len(set(self.positive_bonds)) != len(self.positive_bonds):
            raise ValueError("positive_bonds must be unique")
        if type(self.gauge_normalization) is not Periodic2DRankNGaugeNormalizationEnum:
            raise TypeError("gauge_normalization must be the exact periodic-2D enum")
        if type(self.direct_metric) is not DirectLatticeMetric:
            raise TypeError("direct_metric must be DirectLatticeMetric")
        if type(self.direct_metric.direct_lattice) is not DirectLattice2D:
            raise TypeError("direct_metric must use the exact PhysKit DirectLattice2D")
        self.validate_basis_resolved_metric_geometry()

    def _mapping(self) -> Mapping[str, SerializableValue]:
        basis = self.direct_metric.primitive_basis
        return {
            "identifier": self.identifier,
            "positive_bonds": self.positive_bonds,
            "gauge_normalization": self.gauge_normalization.to_wire(),
            "direct_lattice_primitive_basis_rows": tuple(
                tuple(float(component) for component in row) for row in basis
            ),
            "direct_lattice_primitive_vector_axis": "columns",
            "shell_metric_scale": self.shell_metric_scale,
            "basis_offsets": self.basis_offsets,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "identifier",
            "positive_bonds",
            "gauge_normalization",
            "direct_lattice_primitive_basis_rows",
            "direct_lattice_primitive_vector_axis",
            "shell_metric_scale",
            "basis_offsets",
        }
        if set(values) != required:
            raise ValueError("periodic-2D rank-N case fields do not match")
        identifier = values["identifier"]
        bonds = values["positive_bonds"]
        normalization = values["gauge_normalization"]
        basis_rows = values["direct_lattice_primitive_basis_rows"]
        vector_axis = values["direct_lattice_primitive_vector_axis"]
        shell_scale = values["shell_metric_scale"]
        basis_offsets = values["basis_offsets"]
        if type(identifier) is not str or type(normalization) is not str:
            raise TypeError("case identifiers must decode to built-in strings")
        if type(bonds) is not tuple or any(
            type(bond) is not tuple
            or any(type(component) is not int for component in bond)
            for bond in bonds
        ):
            raise TypeError("positive_bonds must decode to integer tuples")
        if type(basis_rows) is not tuple or any(
            type(row) is not tuple
            or any(type(component) is not float for component in row)
            for row in basis_rows
        ):
            raise TypeError("primitive basis must decode to float tuples")
        if vector_axis != "columns":
            raise ValueError("direct lattice primitive vectors must be columns")
        if type(shell_scale) is not float:
            raise TypeError("shell_metric_scale must decode to a built-in float")
        if type(basis_offsets) is not tuple or any(
            type(offset) is not tuple
            or any(type(component) is not float for component in offset)
            for offset in basis_offsets
        ):
            raise TypeError("basis_offsets must decode to float tuples")
        basis = cast(
            Float64Array,
            np.asarray(basis_rows, dtype=np.float64),
        )
        if basis.shape != (2, 2):
            raise ValueError("periodic-2D primitive basis must have shape (2, 2)")
        return cls(
            identifier=identifier,
            positive_bonds=bonds,
            gauge_normalization=(
                Periodic2DRankNGaugeNormalizationEnum.from_wire(normalization)
            ),
            direct_metric=DirectLatticeMetric(
                DirectLattice2D(a1=basis[:, 0], a2=basis[:, 1])
            ),
            shell_metric_scale=shell_scale,
            basis_offsets=basis_offsets,
        )


@dataclass(frozen=True, slots=True)
class Periodic2DRankNBandEquivalenceHoppingLocalityRequest(
    BaseTypedRecord,
    Periodic2DRankNBandEquivalenceHoppingLocalityRequestRole,
):
    """Freeze one exact periodic-2D rank-N software study definition."""

    RETAINED_RANKS: ClassVar[tuple[int, ...]] = (3, 4, 8)
    CIRCUIT_DEPTHS: ClassVar[tuple[int, ...]] = (1, 2, 4)
    PARENT_SCALES: ClassVar[tuple[float, ...]] = (0.0, 1.0)
    BAND_TOLERANCES: ClassVar[tuple[float, ...]] = (1.0e-3, 1.0e-5)
    GAUGE_ALIGNMENTS: ClassVar[tuple[Periodic2DRankNGaugeAlignment, ...]] = (
        Periodic2DRankNGaugeAlignment.IDENTITY,
        Periodic2DRankNGaugeAlignment.GLOBAL_UNITARY,
        Periodic2DRankNGaugeAlignment.POINTWISE_UNITARY,
        Periodic2DRankNGaugeAlignment.KNOWN_INVERSE_ORACLE,
    )
    PROCRUSTES_RANK_CUTOFF_RULE: ClassVar[ComplexUnitaryProcrustesRankCutoffRule] = (
        ComplexUnitaryProcrustesRankCutoffRule.MAXIMUM
    )
    PROCRUSTES_RANK_ABSOLUTE: ClassVar[float] = 1.0e-12
    PROCRUSTES_RANK_RELATIVE: ClassVar[float] = 1.0e-10
    PROCRUSTES_VALIDATION_ABSOLUTE: ClassVar[float] = 1.0e-12
    PROCRUSTES_VALIDATION_RELATIVE: ClassVar[float] = 1.0e-10
    TRANSPORT_RANK_ABSOLUTE: ClassVar[float] = 1.0e-10
    TRANSPORT_RANK_RELATIVE: ClassVar[float] = 1.0e-12
    NORM_ENERGY_SCALE: ClassVar[float] = 1.0

    family: Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum
    cases: tuple[Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition, ...]
    retained_ranks: tuple[int, ...]
    circuit_depths: tuple[int, ...]
    construction_size: int
    evaluation_size: int
    evaluation_shift: float
    parent_scales: tuple[float, ...]
    attack_coefficients: tuple[float, ...]
    band_tolerances: tuple[float, ...]
    gauge_alignments: tuple[Periodic2DRankNGaugeAlignment, ...]
    shell_cap: int
    procrustes_rank_cutoff_rule: ComplexUnitaryProcrustesRankCutoffRule
    procrustes_rank_absolute: float
    procrustes_rank_relative: float
    procrustes_validation_absolute: float
    procrustes_validation_relative: float
    transport_rank_absolute: float
    transport_rank_relative: float
    norm_energy_scale: float

    @property
    def band_subspace_ranks(self) -> tuple[int, ...]:
        """Return the requested band-subspace rank inventory."""
        return self.retained_ranks

    def __post_init__(self) -> None:
        if (
            type(self.family)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum
        ):
            raise TypeError("family must be the exact periodic-2D rank-N enum")
        if type(self.cases) is not tuple or not self.cases:
            raise TypeError("cases must be a nonempty tuple")
        if any(
            type(case)
            is not Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition
            for case in self.cases
        ):
            raise TypeError("cases must contain exact periodic-2D definitions")
        if self.retained_ranks != self.RETAINED_RANKS:
            raise ValueError("retained_ranks must match the selected inventory")
        if self.circuit_depths != self.CIRCUIT_DEPTHS:
            raise ValueError("circuit_depths must match the selected inventory")
        if self.parent_scales != self.PARENT_SCALES:
            raise ValueError("parent_scales must match the selected inventory")
        if self.band_tolerances != self.BAND_TOLERANCES:
            raise ValueError("band_tolerances must match the selected inventory")
        if self.gauge_alignments != self.GAUGE_ALIGNMENTS:
            raise ValueError("gauge_alignments must match the selected inventory")
        if any(
            type(alignment) is not Periodic2DRankNGaugeAlignment
            for alignment in self.gauge_alignments
        ):
            raise TypeError("gauge_alignments must contain exact periodic-2D enums")
        if type(self.procrustes_rank_cutoff_rule) is not (
            ComplexUnitaryProcrustesRankCutoffRule
        ):
            raise TypeError(
                "procrustes_rank_cutoff_rule must be the exact Project Koios enum"
            )
        if self.procrustes_rank_cutoff_rule is not self.PROCRUSTES_RANK_CUTOFF_RULE:
            raise ValueError(
                "procrustes_rank_cutoff_rule must match the selected control"
            )
        for value, expected, name in (
            (
                self.procrustes_rank_absolute,
                self.PROCRUSTES_RANK_ABSOLUTE,
                "procrustes_rank_absolute",
            ),
            (
                self.procrustes_rank_relative,
                self.PROCRUSTES_RANK_RELATIVE,
                "procrustes_rank_relative",
            ),
            (
                self.procrustes_validation_absolute,
                self.PROCRUSTES_VALIDATION_ABSOLUTE,
                "procrustes_validation_absolute",
            ),
            (
                self.procrustes_validation_relative,
                self.PROCRUSTES_VALIDATION_RELATIVE,
                "procrustes_validation_relative",
            ),
        ):
            if value != expected:
                raise ValueError(f"{name} must match the selected control")
        if self.transport_rank_absolute != self.TRANSPORT_RANK_ABSOLUTE:
            raise ValueError("transport_rank_absolute must match the selected control")
        if self.transport_rank_relative != self.TRANSPORT_RANK_RELATIVE:
            raise ValueError("transport_rank_relative must match the selected control")
        if self.norm_energy_scale != self.NORM_ENERGY_SCALE:
            raise ValueError("norm_energy_scale must match the selected control")
        if self.construction_size != 16 or self.evaluation_size != 33:
            raise ValueError("periodic-2D meshes must be the selected 16/33 pair")
        if self.evaluation_shift != 1.0 / 3.0:
            raise ValueError("evaluation_shift must be the selected one-third shift")
        expected_attacks: tuple[float, ...]
        expected_shell_cap: int
        if (
            self.family
            is Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.ORTHOGONAL
        ):
            expected_attacks = (0.0, math.pi / 8.0, math.pi / 4.0)
            expected_shell_cap = 25
            expected_case_signatures = _orthogonal_case_signatures()
        else:
            expected_attacks = (
                0.0,
                math.pi / (8.0 * math.sqrt(6.0)),
                math.pi / (4.0 * math.sqrt(6.0)),
            )
            expected_shell_cap = 21
            expected_case_signatures = _nonorthogonal_case_signatures()
        if self.attack_coefficients != expected_attacks:
            raise ValueError("attack_coefficients must match the selected family")
        if self.shell_cap != expected_shell_cap:
            raise ValueError("shell_cap must match the selected family")
        if tuple(_case_signature(case) for case in self.cases) != (
            expected_case_signatures
        ):
            raise ValueError("cases must match the selected family geometry inventory")

    @property
    def procrustes_tolerance(self) -> ComplexUnitaryProcrustesTolerance:
        """Return the selected global and pointwise Procrustes software policy."""
        return ComplexUnitaryProcrustesTolerance(
            rank_absolute=self.procrustes_rank_absolute,
            rank_relative=self.procrustes_rank_relative,
            validation_absolute=self.procrustes_validation_absolute,
            validation_relative=self.procrustes_validation_relative,
            rank_cutoff_rule=self.procrustes_rank_cutoff_rule,
        )

    @property
    def case_count(self) -> int:
        """Return the complete analytic rank/depth/scale/attack case count."""
        return (
            len(self.cases)
            * len(self.retained_ranks)
            * len(self.circuit_depths)
            * len(self.parent_scales)
            * len(self.attack_coefficients)
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "family": self.family.to_wire(),
            "cases": self.cases,
            "retained_ranks": self.retained_ranks,
            "circuit_depths": self.circuit_depths,
            "construction_size": self.construction_size,
            "evaluation_size": self.evaluation_size,
            "evaluation_shift": self.evaluation_shift,
            "parent_scales": self.parent_scales,
            "attack_coefficients": self.attack_coefficients,
            "band_tolerances": self.band_tolerances,
            "gauge_alignments": tuple(
                alignment.to_wire() for alignment in self.gauge_alignments
            ),
            "shell_cap": self.shell_cap,
            "procrustes_rank_cutoff_rule": self.procrustes_rank_cutoff_rule.value,
            "procrustes_rank_absolute": self.procrustes_rank_absolute,
            "procrustes_rank_relative": self.procrustes_rank_relative,
            "procrustes_validation_absolute": self.procrustes_validation_absolute,
            "procrustes_validation_relative": self.procrustes_validation_relative,
            "transport_rank_absolute": self.transport_rank_absolute,
            "transport_rank_relative": self.transport_rank_relative,
            "norm_energy_scale": self.norm_energy_scale,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "family",
            "cases",
            "retained_ranks",
            "circuit_depths",
            "construction_size",
            "evaluation_size",
            "evaluation_shift",
            "parent_scales",
            "attack_coefficients",
            "band_tolerances",
            "gauge_alignments",
            "shell_cap",
            "procrustes_rank_cutoff_rule",
            "procrustes_rank_absolute",
            "procrustes_rank_relative",
            "procrustes_validation_absolute",
            "procrustes_validation_relative",
            "transport_rank_absolute",
            "transport_rank_relative",
            "norm_energy_scale",
        }
        if set(values) != required:
            raise ValueError("periodic-2D rank-N request fields do not match")
        family = values["family"]
        cases = values["cases"]
        gauge_alignments = values["gauge_alignments"]
        procrustes_rank_cutoff_rule = values["procrustes_rank_cutoff_rule"]
        if type(family) is not str:
            raise TypeError("family must decode to a built-in string")
        if type(procrustes_rank_cutoff_rule) is not str:
            raise TypeError(
                "procrustes_rank_cutoff_rule must decode to a built-in string"
            )
        if type(cases) is not tuple or any(
            not isinstance(case, Mapping) for case in cases
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        if type(gauge_alignments) is not tuple or any(
            type(alignment) is not str for alignment in gauge_alignments
        ):
            raise TypeError("gauge_alignments must decode to built-in strings")
        integer_names = ("construction_size", "evaluation_size", "shell_cap")
        integers: dict[str, int] = {}
        for name in integer_names:
            value = values[name]
            if type(value) is not int:
                raise TypeError(f"{name} must decode to a built-in integer")
            integers[name] = value
        float_names = (
            "evaluation_shift",
            "procrustes_rank_absolute",
            "procrustes_rank_relative",
            "procrustes_validation_absolute",
            "procrustes_validation_relative",
            "transport_rank_absolute",
            "transport_rank_relative",
            "norm_energy_scale",
        )
        floats: dict[str, float] = {}
        for name in float_names:
            value = values[name]
            if type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float")
            floats[name] = value
        integer_tuple_names = ("retained_ranks", "circuit_depths")
        integer_tuples: dict[str, tuple[int, ...]] = {}
        for name in integer_tuple_names:
            value = values[name]
            if type(value) is not tuple or any(type(item) is not int for item in value):
                raise TypeError(f"{name} must decode to built-in integers")
            integer_tuples[name] = value
        float_tuple_names = (
            "parent_scales",
            "attack_coefficients",
            "band_tolerances",
        )
        float_tuples: dict[str, tuple[float, ...]] = {}
        for name in float_tuple_names:
            value = values[name]
            if type(value) is not tuple or any(
                type(item) is not float for item in value
            ):
                raise TypeError(f"{name} must decode to built-in floats")
            float_tuples[name] = value
        return cls(
            family=Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum.from_wire(
                family
            ),
            cases=tuple(
                Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition.from_dict(
                    case
                )
                for case in cases
            ),
            retained_ranks=integer_tuples["retained_ranks"],
            circuit_depths=integer_tuples["circuit_depths"],
            construction_size=integers["construction_size"],
            evaluation_size=integers["evaluation_size"],
            evaluation_shift=floats["evaluation_shift"],
            parent_scales=float_tuples["parent_scales"],
            attack_coefficients=float_tuples["attack_coefficients"],
            band_tolerances=float_tuples["band_tolerances"],
            gauge_alignments=tuple(
                Periodic2DRankNGaugeAlignment.from_wire(alignment)
                for alignment in gauge_alignments
            ),
            shell_cap=integers["shell_cap"],
            procrustes_rank_cutoff_rule=(
                ComplexUnitaryProcrustesRankCutoffRule(procrustes_rank_cutoff_rule)
            ),
            procrustes_rank_absolute=floats["procrustes_rank_absolute"],
            procrustes_rank_relative=floats["procrustes_rank_relative"],
            procrustes_validation_absolute=floats["procrustes_validation_absolute"],
            procrustes_validation_relative=floats["procrustes_validation_relative"],
            transport_rank_absolute=floats["transport_rank_absolute"],
            transport_rank_relative=floats["transport_rank_relative"],
            norm_energy_scale=floats["norm_energy_scale"],
        )


_CaseSignature = tuple[
    str,
    tuple[tuple[int, int], ...],
    Periodic2DRankNGaugeNormalizationEnum,
    tuple[tuple[float, ...], ...],
    float,
    tuple[tuple[float, ...], ...],
]


def _case_signature(
    case: Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition,
) -> _CaseSignature:
    basis = case.direct_metric.primitive_basis
    return (
        case.identifier,
        case.positive_bonds,
        case.gauge_normalization,
        tuple(tuple(float(component) for component in row) for row in basis),
        case.shell_metric_scale,
        case.basis_offsets,
    )


def _orthogonal_case_signatures() -> tuple[_CaseSignature, ...]:
    return (
        (
            "square-axis-control",
            ((1, 0), (0, 1)),
            Periodic2DRankNGaugeNormalizationEnum.AXIS_MAXIMUM,
            ((1.0, 0.0), (0.0, 1.0)),
            1.0,
            (),
        ),
    )


def _nonorthogonal_case_signatures() -> tuple[_CaseSignature, ...]:
    triangular_basis = ((1.0, 0.5), (0.0, math.sqrt(3.0) / 2.0))
    triangular_bonds = ((1, 0), (0, 1), (1, -1))
    return (
        (
            "matched-square-bravais-control",
            ((1, 0), (0, 1)),
            Periodic2DRankNGaugeNormalizationEnum.BOND_RMS,
            ((1.0, 0.0), (0.0, 1.0)),
            1.0,
            (),
        ),
        (
            "triangular-bravais-control",
            triangular_bonds,
            Periodic2DRankNGaugeNormalizationEnum.BOND_RMS,
            triangular_basis,
            1.0,
            (),
        ),
        (
            "triangular-two-basis-metric-control",
            triangular_bonds,
            Periodic2DRankNGaugeNormalizationEnum.BOND_RMS,
            triangular_basis,
            1.0,
            ((0.0, 0.0), (1.0 / 3.0, 1.0 / 3.0)),
        ),
    )


__all__ = [
    "Periodic2DRankNBandEquivalenceHoppingLocalityCaseDefinition",
    "Periodic2DRankNBandEquivalenceHoppingLocalityFamilyEnum",
    "Periodic2DRankNBandEquivalenceHoppingLocalityRequest",
]
