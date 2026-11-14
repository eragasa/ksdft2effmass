"""Ordered coordinate identities for finite periodic bases.

The values in this module identify matrix coordinates only. They do not identify a
state space, frame, gauge, embedding, geometry, energy reference, sewing map, or
artifact provenance.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Self

from ksdft2effmass.serialization import (
    BaseTypedRecord,
    SerializableValue,
    StrWireEnum,
)


class PeriodicBasisFamily(StrWireEnum):
    """Closed vocabulary of coordinate families supported by the first wire."""

    LABELED_COMPONENT = "labeled_component"
    PLANE_WAVE = "plane_wave"
    WANNIER_ORBITAL = "wannier_orbital"
    SLATER_KOSTER_ORBITAL = "slater_koster_orbital"


class SlaterKosterOrbital(StrWireEnum):
    """Orbital labels supported by the spinless ``sp3s*`` model boundary."""

    S = "s"
    P_X = "p_x"
    P_Y = "p_y"
    P_Z = "p_z"
    S_STAR = "s_star"


@dataclass(frozen=True, slots=True)
class LabeledComponentBasisCoordinate(BaseTypedRecord):
    """Identify one ordered analytic or composite component by an exact label.

    Parameters
    ----------
    label
        Nonempty exact component label. Spelling and case are semantic and are not
        normalized.
    """

    label: str

    def __post_init__(self) -> None:
        _require_nonempty_string(self.label, "label")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "kind": PeriodicBasisFamily.LABELED_COMPONENT.to_wire(),
            "label": self.label,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _require_fields(values, ("kind", "label"))
        _require_kind(values["kind"], PeriodicBasisFamily.LABELED_COMPONENT)
        label = values["label"]
        if type(label) is not str:
            raise TypeError("label must be a built-in string")
        return cls(label=label)


@dataclass(frozen=True, slots=True)
class PlaneWaveBasisCoordinate(BaseTypedRecord):
    """Identify one plane-wave coefficient coordinate.

    Parameters
    ----------
    reciprocal_index
        Exact integer reciprocal-lattice index in ordered primitive reciprocal axes.
        One, two, and three dimensional indices are supported. Booleans are rejected.
    component_label
        Optional exact internal-component label. ``None`` denotes a scalar plane-wave
        coefficient rather than an unknown component.
    """

    reciprocal_index: tuple[int, ...]
    component_label: str | None = None

    def __post_init__(self) -> None:
        if type(self.reciprocal_index) is not tuple:
            raise TypeError("reciprocal_index must be a tuple of built-in ints")
        if len(self.reciprocal_index) not in (1, 2, 3):
            raise ValueError("reciprocal_index must have dimension 1, 2, or 3")
        if any(type(component) is not int for component in self.reciprocal_index):
            raise TypeError(
                "reciprocal_index must contain built-in ints excluding booleans"
            )
        if self.component_label is not None:
            _require_nonempty_string(self.component_label, "component_label")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "component_label": self.component_label,
            "kind": PeriodicBasisFamily.PLANE_WAVE.to_wire(),
            "reciprocal_index": self.reciprocal_index,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _require_fields(values, ("component_label", "kind", "reciprocal_index"))
        _require_kind(values["kind"], PeriodicBasisFamily.PLANE_WAVE)
        reciprocal_index = values["reciprocal_index"]
        component_label = values["component_label"]
        if type(reciprocal_index) is not tuple or any(
            type(component) is not int for component in reciprocal_index
        ):
            raise TypeError("reciprocal_index must be a tuple of built-in ints")
        if component_label is not None and type(component_label) is not str:
            raise TypeError("component_label must be a built-in string or None")
        return cls(
            reciprocal_index=reciprocal_index,
            component_label=component_label,
        )


@dataclass(frozen=True, slots=True)
class WannierOrbitalBasisCoordinate(BaseTypedRecord):
    """Identify one qualified native Wannier orbital coordinate.

    Parameters
    ----------
    native_ordinal
        Zero-based ordinal in the provider-native ordered Wannier inventory.
    qualified_orbital_label
        Nonempty exact orbital label whose scientific meaning has been established by
        an admission step. A generated ordinal-only label is not sufficient evidence.

    Notes
    -----
    Artifact identity and gauge remain separate. Provider adapters must fail closed
    when they cannot establish ``qualified_orbital_label`` semantics.
    """

    native_ordinal: int
    qualified_orbital_label: str

    def __post_init__(self) -> None:
        if type(self.native_ordinal) is not int:
            raise TypeError("native_ordinal must be a built-in int excluding booleans")
        if self.native_ordinal < 0:
            raise ValueError("native_ordinal must be nonnegative")
        _require_nonempty_string(
            self.qualified_orbital_label, "qualified_orbital_label"
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "kind": PeriodicBasisFamily.WANNIER_ORBITAL.to_wire(),
            "native_ordinal": self.native_ordinal,
            "qualified_orbital_label": self.qualified_orbital_label,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _require_fields(
            values,
            ("kind", "native_ordinal", "qualified_orbital_label"),
        )
        _require_kind(values["kind"], PeriodicBasisFamily.WANNIER_ORBITAL)
        native_ordinal = values["native_ordinal"]
        qualified_orbital_label = values["qualified_orbital_label"]
        if type(native_ordinal) is not int:
            raise TypeError("native_ordinal must be a built-in int")
        if type(qualified_orbital_label) is not str:
            raise TypeError("qualified_orbital_label must be a built-in string")
        return cls(
            native_ordinal=native_ordinal,
            qualified_orbital_label=qualified_orbital_label,
        )


@dataclass(frozen=True, slots=True)
class SlaterKosterOrbitalBasisCoordinate(BaseTypedRecord):
    """Identify one Slater--Koster site-orbital coordinate.

    Parameters
    ----------
    site_label
        Nonempty exact site or sublattice label within the primitive-cell inventory.
    orbital
        Exact Slater--Koster orbital label in conventional Cartesian axes.
    spin_component
        Optional exact explicit spin-component label. ``None`` denotes a spinless
        coordinate rather than an unknown spin component.
    """

    site_label: str
    orbital: SlaterKosterOrbital
    spin_component: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_string(self.site_label, "site_label")
        if type(self.orbital) is not SlaterKosterOrbital:
            raise TypeError("orbital must be SlaterKosterOrbital")
        if self.spin_component is not None:
            _require_nonempty_string(self.spin_component, "spin_component")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "kind": PeriodicBasisFamily.SLATER_KOSTER_ORBITAL.to_wire(),
            "orbital": self.orbital.to_wire(),
            "site_label": self.site_label,
            "spin_component": self.spin_component,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _require_fields(values, ("kind", "orbital", "site_label", "spin_component"))
        _require_kind(values["kind"], PeriodicBasisFamily.SLATER_KOSTER_ORBITAL)
        orbital = values["orbital"]
        site_label = values["site_label"]
        spin_component = values["spin_component"]
        if type(orbital) is not str:
            raise TypeError("orbital must be a built-in string")
        if type(site_label) is not str:
            raise TypeError("site_label must be a built-in string")
        if spin_component is not None and type(spin_component) is not str:
            raise TypeError("spin_component must be a built-in string or None")
        return cls(
            site_label=site_label,
            orbital=SlaterKosterOrbital.from_wire(orbital),
            spin_component=spin_component,
        )


type PeriodicBasisCoordinate = (
    LabeledComponentBasisCoordinate
    | PlaneWaveBasisCoordinate
    | WannierOrbitalBasisCoordinate
    | SlaterKosterOrbitalBasisCoordinate
)

_COORDINATE_TYPES: tuple[type[PeriodicBasisCoordinate], ...] = (
    LabeledComponentBasisCoordinate,
    PlaneWaveBasisCoordinate,
    WannierOrbitalBasisCoordinate,
    SlaterKosterOrbitalBasisCoordinate,
)


@dataclass(frozen=True, slots=True)
class PeriodicBasisIdentity(BaseTypedRecord, ABC):
    """Own the dimension-neutral invariants of an ordered periodic basis.

    Parameters
    ----------
    display_identifier
        Nonempty descriptive identifier for logs and human-readable records. It is
        deliberately excluded from equality and hashing.
    coordinates
        Nonempty tuple of unique coordinates from exactly one concrete family. Tuple
        position is the represented matrix row/column order.

    Notes
    -----
    Concrete one-, two-, and three-dimensional subclasses own spatial dimension.
    Compatibility is exact dataclass equality: dimensional concrete type, coordinate
    family, and ordered coordinate values must match. ``display_identifier`` does not
    participate. No normalization, permutation, alias, gauge bridge, or provider
    inference occurs.
    """

    display_identifier: str = field(compare=False)
    coordinates: tuple[PeriodicBasisCoordinate, ...]

    def __post_init__(self) -> None:
        _require_nonempty_string(self.display_identifier, "display_identifier")
        if type(self.coordinates) is not tuple:
            raise TypeError("coordinates must be a tuple")
        if not self.coordinates:
            raise ValueError("coordinates must not be empty")
        first_type = type(self.coordinates[0])
        if first_type not in _COORDINATE_TYPES:
            raise TypeError("coordinates contain an unsupported coordinate type")
        if any(type(coordinate) is not first_type for coordinate in self.coordinates):
            raise ValueError("coordinates must all belong to one basis family")
        if len(set(self.coordinates)) != len(self.coordinates):
            raise ValueError("coordinates must be unique")
        spatial_dimension = type(self)._required_spatial_dimension()
        if spatial_dimension not in (1, 2, 3):
            raise ValueError("spatial dimension must be 1, 2, or 3")
        if first_type is PlaneWaveBasisCoordinate and any(
            len(coordinate.reciprocal_index) != spatial_dimension
            for coordinate in self.coordinates
            if type(coordinate) is PlaneWaveBasisCoordinate
        ):
            raise ValueError(
                "plane-wave reciprocal-index dimension must match the periodic basis"
            )

    @classmethod
    @abstractmethod
    def _required_spatial_dimension(cls) -> int:
        """Return the concrete periodic spatial dimension."""

    @property
    def spatial_dimension(self) -> int:
        """Return the concrete periodic spatial dimension."""
        return type(self)._required_spatial_dimension()

    @property
    def dimension(self) -> int:
        """Return the number of represented coordinates."""
        return len(self.coordinates)

    @property
    def family(self) -> PeriodicBasisFamily:
        """Return the exact coordinate family represented by this identity."""
        coordinate = self.coordinates[0]
        if type(coordinate) is LabeledComponentBasisCoordinate:
            return PeriodicBasisFamily.LABELED_COMPONENT
        if type(coordinate) is PlaneWaveBasisCoordinate:
            return PeriodicBasisFamily.PLANE_WAVE
        if type(coordinate) is WannierOrbitalBasisCoordinate:
            return PeriodicBasisFamily.WANNIER_ORBITAL
        if type(coordinate) is SlaterKosterOrbitalBasisCoordinate:
            return PeriodicBasisFamily.SLATER_KOSTER_ORBITAL
        raise TypeError("coordinates contain an unsupported coordinate type")

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "coordinates": self.coordinates,
            "display_identifier": self.display_identifier,
            "family": self.family.to_wire(),
            "schema_version": 2,
            "spatial_dimension": self.spatial_dimension,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _require_fields(
            values,
            (
                "coordinates",
                "display_identifier",
                "family",
                "schema_version",
                "spatial_dimension",
            ),
        )
        schema_version = values["schema_version"]
        display_identifier = values["display_identifier"]
        family_wire = values["family"]
        coordinate_values = values["coordinates"]
        spatial_dimension = values["spatial_dimension"]
        if type(schema_version) is not int:
            raise TypeError("schema_version must be a built-in int")
        if schema_version != 2:
            raise ValueError("schema_version must be 2")
        if type(spatial_dimension) is not int:
            raise TypeError("spatial_dimension must be a built-in int")
        if spatial_dimension != cls._required_spatial_dimension():
            raise ValueError("spatial_dimension does not match the concrete basis type")
        if type(display_identifier) is not str:
            raise TypeError("display_identifier must be a built-in string")
        if type(family_wire) is not str:
            raise TypeError("family must be a built-in string")
        if type(coordinate_values) is not tuple:
            raise TypeError("coordinates must be a tuple")
        family = PeriodicBasisFamily.from_wire(family_wire)
        coordinate_type = _coordinate_type(family)
        coordinates: list[PeriodicBasisCoordinate] = []
        for coordinate_value in coordinate_values:
            if not isinstance(coordinate_value, Mapping):
                raise TypeError("each coordinate must be a mapping")
            coordinates.append(coordinate_type.from_dict(coordinate_value))
        return cls(
            display_identifier=display_identifier,
            coordinates=tuple(coordinates),
        )


def _coordinate_type(
    family: PeriodicBasisFamily,
) -> type[PeriodicBasisCoordinate]:
    if family is PeriodicBasisFamily.LABELED_COMPONENT:
        return LabeledComponentBasisCoordinate
    if family is PeriodicBasisFamily.PLANE_WAVE:
        return PlaneWaveBasisCoordinate
    if family is PeriodicBasisFamily.WANNIER_ORBITAL:
        return WannierOrbitalBasisCoordinate
    if family is PeriodicBasisFamily.SLATER_KOSTER_ORBITAL:
        return SlaterKosterOrbitalBasisCoordinate
    raise ValueError("unsupported periodic basis family")


def _require_nonempty_string(value: str, name: str) -> None:
    if type(value) is not str:
        raise TypeError(f"{name} must be a built-in string")
    if not value:
        raise ValueError(f"{name} must not be empty")


def _require_fields(
    values: Mapping[str, SerializableValue],
    expected: tuple[str, ...],
) -> None:
    if set(values) != set(expected):
        raise ValueError(f"fields must be exactly {expected!r}")


def _require_kind(value: SerializableValue, expected: PeriodicBasisFamily) -> None:
    if type(value) is not str:
        raise TypeError("kind must be a built-in string")
    if PeriodicBasisFamily.from_wire(value) is not expected:
        raise ValueError(f"kind must be {expected.to_wire()!r}")


__all__ = [
    "LabeledComponentBasisCoordinate",
    "PeriodicBasisCoordinate",
    "PeriodicBasisFamily",
    "PeriodicBasisIdentity",
    "PlaneWaveBasisCoordinate",
    "SlaterKosterOrbital",
    "SlaterKosterOrbitalBasisCoordinate",
    "WannierOrbitalBasisCoordinate",
]
