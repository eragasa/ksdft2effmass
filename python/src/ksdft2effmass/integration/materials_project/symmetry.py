"""Pymatgen symmetry adaptation for canonical structure snapshots."""

from __future__ import annotations

import json
import math
import warnings
from dataclasses import dataclass
from importlib.metadata import version

from pymatgen.core import Lattice, Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

from ksdft2effmass.structures.catalog import StructureSymmetry

type JsonValue = (
    None | bool | int | float | str | list[JsonValue] | dict[str, JsonValue]
)
type JsonObject = dict[str, JsonValue]

__all__ = ["PymatgenStructureSymmetryAnalyzer"]


@dataclass(frozen=True, slots=True)
class PymatgenStructureSymmetryAnalyzer:
    """Derive tolerance-qualified symmetry from one canonical snapshot.

    Notes
    -----
    This integration adapter owns canonical JSON and unit adaptation. Pymatgen and
    spglib own the crystallographic algorithm. No network request is performed.
    """

    def execute(
        self,
        snapshot: bytes,
        *,
        symprec_angstrom: float,
        angle_tolerance_degree: float,
    ) -> StructureSymmetry:
        """Return symmetry while retaining analyzer version and tolerances.

        Parameters
        ----------
        snapshot
            Exact canonical project structure JSON bytes in LAMMPS ``metal`` units.
        symprec_angstrom
            Positive finite positional tolerance in angstrom.
        angle_tolerance_degree
            Positive finite angular tolerance in degrees.

        Returns
        -------
        StructureSymmetry
            Immutable derived symmetry, analyzer identity and version, exact
            tolerances, and site-ordered Wyckoff and equivalence assignments.

        Raises
        ------
        TypeError
            An input or decoded snapshot field has the wrong semantic type.
        ValueError
            A tolerance, JSON document, canonical unit, shape, numeric value, or
            pymatgen symmetry result is invalid.
        """
        if type(snapshot) is not bytes:
            raise TypeError("snapshot must be bytes")
        for name, value in (
            ("symprec_angstrom", symprec_angstrom),
            ("angle_tolerance_degree", angle_tolerance_degree),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be built-in float")
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        try:
            decoded = json.loads(snapshot)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("malformed canonical structure snapshot") from error
        root = self._mapping(decoded, "structure snapshot")
        if root.get("unit_system") != "metal":
            raise ValueError("structure snapshot must use canonical metal units")
        direct = self._mapping(root.get("direct_lattice"), "direct_lattice")
        if direct.get("unit") != "angstrom":
            raise ValueError("direct lattice must use angstrom")
        vectors = self._matrix(direct.get("vectors"))
        sites = self._list(root.get("sites"), "sites")
        species: list[str] = []
        coordinates: list[tuple[float, float, float]] = []
        for item in sites:
            site = self._mapping(item, "site")
            if site.get("coordinate_unit") != "angstrom":
                raise ValueError("site coordinates must use angstrom")
            species.append(self._string(site.get("species_name"), "species_name"))
            coordinates.append(self._vector(site.get("coordinates"), "coordinates"))
        structure = Structure(
            Lattice(vectors),
            species,
            coordinates,
            coords_are_cartesian=True,
            to_unit_cell=True,
        )
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message=(
                    "Set OLD_ERROR_HANDLING to false and catch the errors directly."
                ),
                category=DeprecationWarning,
                module="spglib.spg",
            )
            analyzer = SpacegroupAnalyzer(
                structure,
                symprec=symprec_angstrom,
                angle_tolerance=angle_tolerance_degree,
            )
            dataset = analyzer.get_symmetry_dataset()
        if dataset is None:
            raise ValueError("pymatgen did not produce a symmetry dataset")
        return StructureSymmetry(
            analyzer_identity="pymatgen.symmetry.analyzer.SpacegroupAnalyzer",
            analyzer_version=version("pymatgen"),
            symprec_angstrom=symprec_angstrom,
            angle_tolerance_degree=angle_tolerance_degree,
            space_group_symbol=analyzer.get_space_group_symbol(),
            space_group_number=analyzer.get_space_group_number(),
            hall_symbol=analyzer.get_hall(),
            crystal_system=analyzer.get_crystal_system(),
            point_group_symbol=analyzer.get_point_group_symbol(),
            wyckoff_symbols=tuple(dataset.wyckoffs),
            equivalent_atoms=tuple(int(value) for value in dataset.equivalent_atoms),
        )

    @staticmethod
    def _mapping(value: JsonValue, name: str) -> JsonObject:
        if type(value) is not dict:
            raise TypeError(f"{name} must be an object")
        return value

    @staticmethod
    def _list(value: JsonValue, name: str) -> list[JsonValue]:
        if type(value) is not list:
            raise TypeError(f"{name} must be a list")
        return value

    @staticmethod
    def _string(value: JsonValue, name: str) -> str:
        if type(value) is not str:
            raise TypeError(f"{name} must be str")
        if not value:
            raise ValueError(f"{name} must be nonempty")
        return value

    @classmethod
    def _vector(cls, value: JsonValue, name: str) -> tuple[float, float, float]:
        values = cls._list(value, name)
        if len(values) != 3:
            raise ValueError(f"{name} must contain three values")
        return (
            cls._number(values[0], name),
            cls._number(values[1], name),
            cls._number(values[2], name),
        )

    @classmethod
    def _matrix(
        cls, value: JsonValue
    ) -> tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float],
    ]:
        values = cls._list(value, "vectors")
        if len(values) != 3:
            raise ValueError("vectors must contain three rows")
        return (
            cls._vector(values[0], "vectors"),
            cls._vector(values[1], "vectors"),
            cls._vector(values[2], "vectors"),
        )

    @staticmethod
    def _number(value: JsonValue, name: str) -> float:
        if type(value) is int:
            result = float(value)
        elif type(value) is float:
            result = value
        else:
            raise TypeError(f"{name} values must be numeric")
        if not math.isfinite(result):
            raise ValueError(f"{name} values must be finite")
        return result
