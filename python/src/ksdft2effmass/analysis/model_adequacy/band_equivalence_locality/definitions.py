"""Immutable family-owned controls for locality development calculations."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Self

import numpy as np
from projectkoios.physkit.periodic.lattice import (
    DirectLattice2D,
    DirectLattice3D,
    DirectLatticeMetric,
)
from projectkoios.physkit.units import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
)

from ksdft2effmass.real_space_support_truncation import BasisResolvedMetricGeometry
from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StringWireEnum,
)

TRANSPORT_RANK_DEFICIENT_REASON = (
    "rank-deficient neighbor overlap does not identify unique transport"
)


class BandEquivalenceLocalityFamilyEnum(StringWireEnum):
    """Name one independently interpreted development replication."""

    SQUARE = (
        "ksdft2effmass.campaign.model-adequacy.periodic2d."
        "band-equivalence-versus-hopping-locality"
    )
    GRAPHENE_INSPIRED = (
        "ksdft2effmass.campaign.model-adequacy.periodic2d-nonorthogonal."
        "band-equivalence-versus-hopping-locality"
    )
    SIMPLE_CUBIC = (
        "ksdft2effmass.campaign.model-adequacy.periodic3d."
        "band-equivalence-versus-hopping-locality"
    )
    SILICON_INSPIRED = (
        "ksdft2effmass.campaign.model-adequacy.periodic3d-nonorthogonal."
        "band-equivalence-versus-hopping-locality"
    )


class ParentEnum(StringWireEnum):
    """Select one exact four-state synthetic parent law."""

    DIRECTED_AXIS = "directed-axis"
    HERMITIAN_BRAVAIS = "hermitian-bravais"
    BIPARTITE_INSPIRED = "bipartite-inspired"


class GaugeNormalizationEnum(StringWireEnum):
    """Select the declared interpretation of the gauge amplitude."""

    AXIS_MAXIMUM = "axis-maximum"
    BOND_RMS = "bond-rms"


@dataclass(frozen=True, slots=True, eq=False)
class BandEquivalenceLocalitySyntheticModelDefinition(BaseTypedRecord):
    """Declare every coefficient and identity of the synthetic four-state model."""

    identifier: str
    parent_basis_identifier: str
    retained_basis_identifier: str
    energy_reference: str
    onsite: ComplexMatrixQuantity
    directed_hopping: ComplexMatrixQuantity
    bipartite_lower_onsite: ScalarQuantity
    bipartite_upper_onsite: ScalarQuantity
    bipartite_lower_bond_scale: ScalarQuantity
    bipartite_upper_bond_scale: ScalarQuantity
    bipartite_intersector_coupling: ScalarQuantity
    retained_seed: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate explicit identities, units, shapes, and retained-seed rank."""
        for text_value, text_name in (
            (self.identifier, "identifier"),
            (self.parent_basis_identifier, "parent_basis_identifier"),
            (self.retained_basis_identifier, "retained_basis_identifier"),
            (self.energy_reference, "energy_reference"),
        ):
            if type(text_value) is not str:
                raise TypeError(f"{text_name} must be a built-in string")
            if not text_value:
                raise ValueError(f"{text_name} must be nonempty")
        for matrix_value, matrix_name in (
            (self.onsite, "onsite"),
            (self.directed_hopping, "directed_hopping"),
            (self.retained_seed, "retained_seed"),
        ):
            if type(matrix_value) is not ComplexMatrixQuantity:
                raise TypeError(f"{matrix_name} must be ComplexMatrixQuantity")
            if type(matrix_value.unit) is not Unitless:
                raise ValueError(f"{matrix_name} must be explicitly unitless")
        if self.onsite.magnitude.shape != (4, 4):
            raise ValueError("onsite must have shape (4, 4)")
        if not np.array_equal(
            self.onsite.magnitude, self.onsite.magnitude.conjugate().T
        ):
            raise ValueError("onsite must be Hermitian")
        if self.directed_hopping.magnitude.shape != (4, 4):
            raise ValueError("directed_hopping must have shape (4, 4)")
        if self.retained_seed.magnitude.shape != (4, 2):
            raise ValueError("retained_seed must have shape (4, 2)")
        if int(np.linalg.matrix_rank(self.retained_seed.magnitude)) != 2:
            raise ValueError("retained_seed must have column rank two")
        for scalar_value, scalar_name in (
            (self.bipartite_lower_onsite, "bipartite_lower_onsite"),
            (self.bipartite_upper_onsite, "bipartite_upper_onsite"),
            (self.bipartite_lower_bond_scale, "bipartite_lower_bond_scale"),
            (self.bipartite_upper_bond_scale, "bipartite_upper_bond_scale"),
            (
                self.bipartite_intersector_coupling,
                "bipartite_intersector_coupling",
            ),
        ):
            if type(scalar_value) is not ScalarQuantity:
                raise TypeError(f"{scalar_name} must be ScalarQuantity")
            if type(scalar_value.unit) is not Unitless:
                raise ValueError(f"{scalar_name} must be explicitly unitless")

    @property
    def retained_rank(self) -> int:
        """Return the explicitly declared retained-seed column count."""
        return int(self.retained_seed.magnitude.shape[1])

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "identifier": self.identifier,
            "parent_basis_identifier": self.parent_basis_identifier,
            "retained_basis_identifier": self.retained_basis_identifier,
            "energy_reference": self.energy_reference,
            "onsite": self.onsite,
            "directed_hopping": self.directed_hopping,
            "bipartite_lower_onsite": self.bipartite_lower_onsite,
            "bipartite_upper_onsite": self.bipartite_upper_onsite,
            "bipartite_lower_bond_scale": self.bipartite_lower_bond_scale,
            "bipartite_upper_bond_scale": self.bipartite_upper_bond_scale,
            "bipartite_intersector_coupling": (self.bipartite_intersector_coupling),
            "retained_seed": self.retained_seed,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "identifier",
            "parent_basis_identifier",
            "retained_basis_identifier",
            "energy_reference",
            "onsite",
            "directed_hopping",
            "bipartite_lower_onsite",
            "bipartite_upper_onsite",
            "bipartite_lower_bond_scale",
            "bipartite_upper_bond_scale",
            "bipartite_intersector_coupling",
            "retained_seed",
        }
        if set(values) != required:
            raise ValueError("synthetic-model definition fields do not match")
        strings: dict[str, str] = {}
        for name in (
            "identifier",
            "parent_basis_identifier",
            "retained_basis_identifier",
            "energy_reference",
        ):
            value = values[name]
            if type(value) is not str:
                raise TypeError(f"{name} must decode to a built-in string")
            strings[name] = value
        matrices: dict[str, ComplexMatrixQuantity] = {}
        for name in ("onsite", "directed_hopping", "retained_seed"):
            value = values[name]
            if type(value) is not ComplexMatrixQuantity:
                raise TypeError(f"{name} must decode to ComplexMatrixQuantity")
            matrices[name] = value
        scalars: dict[str, ScalarQuantity] = {}
        for name in (
            "bipartite_lower_onsite",
            "bipartite_upper_onsite",
            "bipartite_lower_bond_scale",
            "bipartite_upper_bond_scale",
            "bipartite_intersector_coupling",
        ):
            value = values[name]
            if type(value) is not ScalarQuantity:
                raise TypeError(f"{name} must decode to ScalarQuantity")
            scalars[name] = value
        return cls(
            identifier=strings["identifier"],
            parent_basis_identifier=strings["parent_basis_identifier"],
            retained_basis_identifier=strings["retained_basis_identifier"],
            energy_reference=strings["energy_reference"],
            onsite=matrices["onsite"],
            directed_hopping=matrices["directed_hopping"],
            bipartite_lower_onsite=scalars["bipartite_lower_onsite"],
            bipartite_upper_onsite=scalars["bipartite_upper_onsite"],
            bipartite_lower_bond_scale=scalars["bipartite_lower_bond_scale"],
            bipartite_upper_bond_scale=scalars["bipartite_upper_bond_scale"],
            bipartite_intersector_coupling=scalars["bipartite_intersector_coupling"],
            retained_seed=matrices["retained_seed"],
        )


FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1 = (
    BandEquivalenceLocalitySyntheticModelDefinition(
        identifier="four-state-locality-development-model-v1",
        parent_basis_identifier="synthetic-four-state-parent-basis-v1",
        retained_basis_identifier="projected-seed-rank-two-basis-v1",
        energy_reference="synthetic-dimensionless-zero-v1",
        onsite=ComplexMatrixQuantity(
            np.array(
                (
                    (-1.20, 0.06, 0.0, 0.0),
                    (0.06, -0.35, 0.0, 0.0),
                    (0.0, 0.0, 1.00, 0.04),
                    (0.0, 0.0, 0.04, 1.75),
                ),
                dtype=np.complex128,
            ),
            Unitless(),
        ),
        directed_hopping=ComplexMatrixQuantity(
            np.array(
                (
                    (0.15, 0.0, 0.12, 0.0),
                    (0.0, -0.10, 0.0, 0.10),
                    (0.0, 0.0, 0.05, 0.0),
                    (0.0, 0.0, 0.0, -0.04),
                ),
                dtype=np.complex128,
            ),
            Unitless(),
        ),
        bipartite_lower_onsite=ScalarQuantity(-1.20, Unitless()),
        bipartite_upper_onsite=ScalarQuantity(1.20, Unitless()),
        bipartite_lower_bond_scale=ScalarQuantity(0.30, Unitless()),
        bipartite_upper_bond_scale=ScalarQuantity(0.10, Unitless()),
        bipartite_intersector_coupling=ScalarQuantity(0.08, Unitless()),
        retained_seed=ComplexMatrixQuantity(
            np.eye(4, 2, dtype=np.complex128),
            Unitless(),
        ),
    )
)


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityCase(BaseTypedRecord, BasisResolvedMetricGeometry):
    """Define one parent and geometry inside an experiment family."""

    name: str
    dimension: int
    parent_kind: ParentEnum
    gauge_normalization: GaugeNormalizationEnum
    positive_bonds: tuple[tuple[int, ...], ...]
    direct_metric: DirectLatticeMetric
    shell_metric_scale: float
    basis_offsets: tuple[tuple[float, ...], ...] = ()

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name:
            raise TypeError("name must be a nonempty built-in str")
        if type(self.dimension) is not int or self.dimension not in (2, 3):
            raise ValueError("dimension must be the built-in integer 2 or 3")
        if type(self.parent_kind) is not ParentEnum:
            raise TypeError("parent_kind must be ParentEnum")
        if type(self.gauge_normalization) is not GaugeNormalizationEnum:
            raise TypeError("gauge_normalization must be GaugeNormalizationEnum")
        if type(self.positive_bonds) is not tuple or not self.positive_bonds:
            raise TypeError("positive_bonds must be a nonempty tuple")
        if any(
            type(bond) is not tuple
            or len(bond) != self.dimension
            or any(type(component) is not int for component in bond)
            for bond in self.positive_bonds
        ):
            raise TypeError(
                "positive_bonds must contain built-in integer tuples matching dimension"
            )
        self.validate_basis_resolved_metric_geometry()

    def _mapping(self) -> Mapping[str, SerializableValue]:
        primitive_basis = self.direct_metric.primitive_basis
        return {
            "name": self.name,
            "dimension": self.dimension,
            "parent_kind": self.parent_kind.to_wire(),
            "gauge_normalization": self.gauge_normalization.to_wire(),
            "positive_bonds": self.positive_bonds,
            "direct_lattice_primitive_basis_rows": tuple(
                tuple(float(component) for component in row) for row in primitive_basis
            ),
            "direct_lattice_primitive_vector_axis": "columns",
            "shell_metric_scale": self.shell_metric_scale,
            "basis_offsets": self.basis_offsets,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "name",
            "dimension",
            "parent_kind",
            "gauge_normalization",
            "positive_bonds",
            "direct_lattice_primitive_basis_rows",
            "direct_lattice_primitive_vector_axis",
            "shell_metric_scale",
            "basis_offsets",
        }
        if set(values) != required:
            raise ValueError("band-equivalence case fields do not match")
        name = values["name"]
        dimension = values["dimension"]
        parent_kind = values["parent_kind"]
        gauge_normalization = values["gauge_normalization"]
        positive_bonds = values["positive_bonds"]
        primitive_basis_rows = values["direct_lattice_primitive_basis_rows"]
        primitive_vector_axis = values["direct_lattice_primitive_vector_axis"]
        shell_metric_scale = values["shell_metric_scale"]
        basis_offsets = values["basis_offsets"]
        if type(name) is not str or type(dimension) is not int:
            raise TypeError("case name and dimension must decode to built-in values")
        if type(parent_kind) is not str or type(gauge_normalization) is not str:
            raise TypeError("case enum values must decode to built-in strings")
        if type(positive_bonds) is not tuple or any(
            type(bond) is not tuple
            or any(type(component) is not int for component in bond)
            for bond in positive_bonds
        ):
            raise TypeError("positive_bonds must decode to integer tuples")
        if type(primitive_basis_rows) is not tuple or any(
            type(row) is not tuple
            or any(type(component) is not float for component in row)
            for row in primitive_basis_rows
        ):
            raise TypeError("primitive basis rows must decode to float tuples")
        if primitive_vector_axis != "columns":
            raise ValueError("direct lattice primitive vectors must be columns")
        if type(shell_metric_scale) is not float:
            raise TypeError("shell_metric_scale must decode to a built-in float")
        if type(basis_offsets) is not tuple or any(
            type(offset) is not tuple
            or any(type(component) is not float for component in offset)
            for offset in basis_offsets
        ):
            raise TypeError("basis_offsets must decode to float tuples")
        basis = np.asarray(primitive_basis_rows, dtype=np.float64)
        direct_lattice: DirectLattice2D | DirectLattice3D
        if dimension == 2:
            direct_lattice = DirectLattice2D(a1=basis[:, 0], a2=basis[:, 1])
        elif dimension == 3:
            direct_lattice = DirectLattice3D(
                a1=basis[:, 0],
                a2=basis[:, 1],
                a3=basis[:, 2],
            )
        else:
            raise ValueError("case dimension must be two or three")
        return cls(
            name=name,
            dimension=dimension,
            parent_kind=ParentEnum.from_wire(parent_kind),
            gauge_normalization=GaugeNormalizationEnum.from_wire(gauge_normalization),
            positive_bonds=positive_bonds,
            direct_metric=DirectLatticeMetric(direct_lattice),
            shell_metric_scale=shell_metric_scale,
            basis_offsets=basis_offsets,
        )


@dataclass(frozen=True, slots=True)
class BandEquivalenceLocalityRequest(BaseTypedRecord):
    """Freeze one bounded, non-evidentiary experiment execution."""

    family: BandEquivalenceLocalityFamilyEnum
    cases: tuple[BandEquivalenceLocalityCase, ...]
    synthetic_model: BandEquivalenceLocalitySyntheticModelDefinition
    construction_size: int
    evaluation_size: int
    evaluation_shift: float
    parent_scales: tuple[float, ...]
    amplitudes: tuple[float, ...]
    band_tolerances: tuple[float, ...]
    shell_cap: int
    amplitude_resolution_intervals: tuple[int, ...] = (
        8,
        16,
        32,
        64,
        128,
        256,
        512,
        1024,
        2048,
        4096,
    )
    transport_rank_absolute: float = 1.0e-10
    transport_rank_relative: float = 1.0e-12

    def __post_init__(self) -> None:
        if type(self.family) is not BandEquivalenceLocalityFamilyEnum:
            raise TypeError("family must be BandEquivalenceLocalityFamilyEnum")
        if type(self.cases) is not tuple or not self.cases:
            raise TypeError("cases must be a nonempty tuple")
        if any(type(case) is not BandEquivalenceLocalityCase for case in self.cases):
            raise TypeError("cases must contain BandEquivalenceLocalityCase values")
        if (
            type(self.synthetic_model)
            is not BandEquivalenceLocalitySyntheticModelDefinition
        ):
            raise TypeError(
                "synthetic_model must be "
                "BandEquivalenceLocalitySyntheticModelDefinition"
            )
        dimensions = {case.dimension for case in self.cases}
        if len(dimensions) != 1:
            raise ValueError("all cases in one family must have one dimension")
        if type(self.construction_size) is not int or self.construction_size < 4:
            raise ValueError("construction_size must be an integer of at least four")
        if self.construction_size % 2:
            raise ValueError("construction_size must be even")
        if type(self.evaluation_size) is not int or self.evaluation_size < 3:
            raise ValueError("evaluation_size must be an integer of at least three")
        if type(self.evaluation_shift) is not float:
            raise TypeError("evaluation_shift must be a built-in float")
        if not math.isfinite(self.evaluation_shift):
            raise ValueError("evaluation_shift must be finite")
        if not 0.0 < self.evaluation_shift < 1.0:
            raise ValueError("evaluation_shift must lie strictly between zero and one")
        for name, values in (
            ("parent_scales", self.parent_scales),
            ("amplitudes", self.amplitudes),
        ):
            if type(values) is not tuple or not values:
                raise TypeError(f"{name} must be a nonempty tuple")
            if any(
                type(value) is not float or not math.isfinite(value) for value in values
            ):
                raise TypeError(f"{name} must contain finite built-in floats")
            if any(value < 0.0 for value in values):
                raise ValueError(f"{name} must be nonnegative")
            if values != tuple(sorted(set(values))):
                raise ValueError(f"{name} must be unique and increasing")
        if self.parent_scales[-1] > 1.0:
            raise ValueError("parent_scales must not exceed one")
        if type(self.band_tolerances) is not tuple or not self.band_tolerances:
            raise TypeError("band_tolerances must be a nonempty tuple")
        if any(
            type(value) is not float or value <= 0.0 for value in self.band_tolerances
        ):
            raise ValueError("band_tolerances must contain positive built-in floats")
        if self.band_tolerances != tuple(
            sorted(set(self.band_tolerances), reverse=True)
        ):
            raise ValueError("band_tolerances must be unique and decreasing")
        if type(self.shell_cap) is not int or self.shell_cap < 0:
            raise ValueError("shell_cap must be a nonnegative built-in int")
        if (
            type(self.amplitude_resolution_intervals) is not tuple
            or not self.amplitude_resolution_intervals
            or any(
                type(value) is not int or value < 1
                for value in self.amplitude_resolution_intervals
            )
        ):
            raise ValueError(
                "amplitude_resolution_intervals must contain positive built-in integers"
            )
        if any(
            fine != 2 * coarse
            for coarse, fine in zip(
                self.amplitude_resolution_intervals[:-1],
                self.amplitude_resolution_intervals[1:],
                strict=True,
            )
        ):
            raise ValueError(
                "amplitude resolution intervals must form a doubling ladder"
            )
        for name, value in (
            ("transport_rank_absolute", self.transport_rank_absolute),
            ("transport_rank_relative", self.transport_rank_relative),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
            if value <= 0.0:
                raise ValueError(f"{name} must be positive")

    @property
    def dimension(self) -> int:
        """Return the common dimension of this family."""
        return self.cases[0].dimension

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "family": self.family.to_wire(),
            "cases": self.cases,
            "synthetic_model": self.synthetic_model,
            "construction_size": self.construction_size,
            "evaluation_size": self.evaluation_size,
            "evaluation_shift": self.evaluation_shift,
            "parent_scales": self.parent_scales,
            "amplitudes": self.amplitudes,
            "band_tolerances": self.band_tolerances,
            "shell_cap": self.shell_cap,
            "amplitude_resolution_intervals": self.amplitude_resolution_intervals,
            "transport_rank_absolute": self.transport_rank_absolute,
            "transport_rank_relative": self.transport_rank_relative,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        required = {
            "family",
            "cases",
            "synthetic_model",
            "construction_size",
            "evaluation_size",
            "evaluation_shift",
            "parent_scales",
            "amplitudes",
            "band_tolerances",
            "shell_cap",
            "amplitude_resolution_intervals",
            "transport_rank_absolute",
            "transport_rank_relative",
        }
        if set(values) != required:
            raise ValueError("band-equivalence request fields do not match")
        family = values["family"]
        cases_value = values["cases"]
        synthetic_model_value = values["synthetic_model"]
        if type(family) is not str:
            raise TypeError("family must decode to a built-in string")
        if type(cases_value) is not tuple or any(
            not isinstance(case, Mapping) for case in cases_value
        ):
            raise TypeError("cases must decode to a tuple of mappings")
        if not isinstance(synthetic_model_value, Mapping):
            raise TypeError("synthetic_model must decode to a mapping")
        integers: dict[str, int] = {}
        for name in ("construction_size", "evaluation_size", "shell_cap"):
            value = values[name]
            if type(value) is not int:
                raise TypeError(f"{name} must decode to a built-in integer")
            integers[name] = value
        floats: dict[str, float] = {}
        for name in (
            "evaluation_shift",
            "transport_rank_absolute",
            "transport_rank_relative",
        ):
            value = values[name]
            if type(value) is not float:
                raise TypeError(f"{name} must decode to a built-in float")
            floats[name] = value
        float_tuples: dict[str, tuple[float, ...]] = {}
        for name in ("parent_scales", "amplitudes", "band_tolerances"):
            value = values[name]
            if type(value) is not tuple or any(
                type(item) is not float for item in value
            ):
                raise TypeError(f"{name} must decode to built-in float values")
            float_tuples[name] = value
        intervals = values["amplitude_resolution_intervals"]
        if type(intervals) is not tuple or any(
            type(item) is not int for item in intervals
        ):
            raise TypeError(
                "amplitude_resolution_intervals must decode to built-in integers"
            )
        return cls(
            family=BandEquivalenceLocalityFamilyEnum.from_wire(family),
            cases=tuple(
                BandEquivalenceLocalityCase.from_dict(case) for case in cases_value
            ),
            synthetic_model=BandEquivalenceLocalitySyntheticModelDefinition.from_dict(
                synthetic_model_value
            ),
            construction_size=integers["construction_size"],
            evaluation_size=integers["evaluation_size"],
            evaluation_shift=floats["evaluation_shift"],
            parent_scales=float_tuples["parent_scales"],
            amplitudes=float_tuples["amplitudes"],
            band_tolerances=float_tuples["band_tolerances"],
            shell_cap=integers["shell_cap"],
            amplitude_resolution_intervals=intervals,
            transport_rank_absolute=floats["transport_rank_absolute"],
            transport_rank_relative=floats["transport_rank_relative"],
        )


__all__ = [
    "BandEquivalenceLocalityCase",
    "BandEquivalenceLocalityRequest",
    "BandEquivalenceLocalitySyntheticModelDefinition",
    "BandEquivalenceLocalityFamilyEnum",
    "FOUR_STATE_LOCALITY_DEVELOPMENT_MODEL_V1",
    "GaugeNormalizationEnum",
    "ParentEnum",
    "TRANSPORT_RANK_DEFICIENT_REASON",
]
