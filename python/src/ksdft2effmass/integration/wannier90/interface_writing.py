"""Deterministic, execution-independent Wannier90 interface-file preparation.

The module writes caller-supplied ``.win``, ``.eig``, ``.amn``, and ``.mmn``
representations. It correlates dimensions and ordered ``.mmn`` neighbor headers with
a parsed ``.nnkp`` record. It performs no filesystem discovery, external execution,
projection generation, overlap construction, unit conversion, localization, or
scientific validation.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from ksdft2effmass.operators import PhysicalUnit, ScalarQuantity, Unitless

from .interface_data import (
    Wannier90EigenvalueData,
    Wannier90NeighborOverlapData,
    Wannier90ProjectionData,
)
from .neighbor_lists import Wannier90NeighborListData

type FloatTriple = tuple[float, float, float]
type IntegerTriple = tuple[int, int, int]
type FractionalAtom = tuple[str, float, float, float]


@dataclass(frozen=True, slots=True)
class Wannier90InputData:
    """Represent the demonstrated deterministic subset of a Wannier90 ``.win`` file.

    Parameters
    ----------
    num_bands
        Positive number of supplied outer-window bands.
    num_wann
        Positive number of requested Wannier functions, not exceeding ``num_bands``.
    num_iter
        Positive maximum localization-iteration count.
    convergence_tolerance
        Positive finite spread-convergence tolerance, serialized with a Fortran
        ``d`` exponent.
    convergence_window
        Positive convergence-window length.
    precondition
        Whether Wannier90 preconditioning is requested.
    search_shells
        Positive neighbor-shell search limit.
    write_hr
        Whether the real-space Hamiltonian is requested.
    write_u_matrices
        Whether unitary matrices are requested.
    translate_home_cell
        Whether Wannier centers are translated into the home cell.
    unit_cell_cart_angstrom
        Three ordered Cartesian lattice vectors in ångström. Components are finite
        built-in floats.
    atoms_fractional
        Nonempty ordered ``(symbol, x, y, z)`` tuples in fractional coordinates.
    projections
        Nonempty ordered Wannier90 projection lines.
    mp_grid
        Three positive Monkhorst--Pack counts. The demonstrated subset is an
        x-directed one-dimensional embedding, so the second and third counts are one.
    kpoints_fractional
        Ordered x-directed reciprocal points in fractional reciprocal-lattice
        coordinates. The second and third coordinates are exactly zero, and the count
        must equal the product of ``mp_grid``.

    Notes
    -----
    This record owns representation validity only. It does not select scientific
    defaults, prove lattice adequacy, or generate projections.
    """

    num_bands: int
    num_wann: int
    num_iter: int
    convergence_tolerance: float
    convergence_window: int
    precondition: bool
    search_shells: int
    write_hr: bool
    write_u_matrices: bool
    translate_home_cell: bool
    unit_cell_cart_angstrom: tuple[FloatTriple, FloatTriple, FloatTriple]
    atoms_fractional: tuple[FractionalAtom, ...]
    projections: tuple[str, ...]
    mp_grid: IntegerTriple
    kpoints_fractional: tuple[FloatTriple, ...]

    def __post_init__(self) -> None:
        """Validate the closed demonstrated input subset."""

        for name, value in (
            ("num_bands", self.num_bands),
            ("num_wann", self.num_wann),
            ("num_iter", self.num_iter),
            ("convergence_window", self.convergence_window),
            ("search_shells", self.search_shells),
        ):
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
            if value <= 0:
                raise ValueError(f"{name} must be positive")
        if self.num_wann > self.num_bands:
            raise ValueError("num_wann must not exceed num_bands")
        if type(self.convergence_tolerance) is not float:
            raise TypeError("convergence_tolerance must be a built-in float")
        if not math.isfinite(self.convergence_tolerance):
            raise ValueError("convergence_tolerance must be finite")
        if self.convergence_tolerance <= 0.0:
            raise ValueError("convergence_tolerance must be positive")
        for name, value in (
            ("precondition", self.precondition),
            ("write_hr", self.write_hr),
            ("write_u_matrices", self.write_u_matrices),
            ("translate_home_cell", self.translate_home_cell),
        ):
            if type(value) is not bool:
                raise TypeError(f"{name} must be a built-in bool")
        self.require_float_triples(
            self.unit_cell_cart_angstrom, "unit_cell_cart_angstrom", 3
        )
        if type(self.atoms_fractional) is not tuple:
            raise TypeError("atoms_fractional must be a built-in tuple")
        if not self.atoms_fractional:
            raise ValueError("atoms_fractional must be nonempty")
        for atom in self.atoms_fractional:
            if type(atom) is not tuple:
                raise TypeError("each atom must be a built-in tuple")
            if len(atom) != 4:
                raise ValueError("each atom must contain exactly four values")
            symbol, x_coordinate, y_coordinate, z_coordinate = atom
            if type(symbol) is not str:
                raise TypeError("atom symbols must be built-in strings")
            if not symbol or symbol != symbol.strip():
                raise ValueError("atom symbols must be nonempty and stripped")
            for coordinate in (x_coordinate, y_coordinate, z_coordinate):
                if type(coordinate) is not float:
                    raise TypeError("fractional coordinates must be built-in floats")
                if not math.isfinite(coordinate):
                    raise ValueError("fractional coordinates must be finite")
        if type(self.projections) is not tuple:
            raise TypeError("projections must be a built-in tuple")
        if not self.projections:
            raise ValueError("projections must be nonempty")
        for projection in self.projections:
            if type(projection) is not str:
                raise TypeError("projection lines must be built-in strings")
            if not projection or projection != projection.strip():
                raise ValueError("projection lines must be nonempty and stripped")
            if "\n" in projection or "\r" in projection:
                raise ValueError("projection lines must not contain line terminators")
        if type(self.mp_grid) is not tuple:
            raise TypeError("mp_grid must be a built-in tuple")
        if len(self.mp_grid) != 3:
            raise ValueError("mp_grid must contain exactly three values")
        if any(type(value) is not int for value in self.mp_grid):
            raise TypeError("mp_grid values must be built-in integers")
        if any(value <= 0 for value in self.mp_grid):
            raise ValueError("mp_grid counts must be positive")
        if self.mp_grid[1:] != (1, 1):
            raise ValueError("the demonstrated input subset requires a 1D mp_grid")
        kpoint_count = self.mp_grid[0] * self.mp_grid[1] * self.mp_grid[2]
        self.require_float_triples(
            self.kpoints_fractional, "kpoints_fractional", kpoint_count
        )
        if any(
            kpoint[1] != 0.0 or kpoint[2] != 0.0 for kpoint in self.kpoints_fractional
        ):
            raise ValueError(
                "the demonstrated input subset requires x-directed kpoints"
            )

    @staticmethod
    def require_float_triples(
        values: tuple[FloatTriple, ...],
        name: str,
        expected_count: int,
    ) -> None:
        """Require an exact tuple of finite built-in-float triples."""

        if type(values) is not tuple:
            raise TypeError(f"{name} must be a built-in tuple")
        if len(values) != expected_count:
            raise ValueError(f"{name} must contain exactly {expected_count} triples")
        for triple in values:
            if type(triple) is not tuple:
                raise TypeError(f"{name} entries must be built-in tuples")
            if len(triple) != 3:
                raise ValueError(f"{name} entries must contain exactly three values")
            if any(type(value) is not float for value in triple):
                raise TypeError(f"{name} entries must contain built-in floats")
            if any(not math.isfinite(value) for value in triple):
                raise ValueError(f"{name} must contain finite values")

    @property
    def kpoint_count(self) -> int:
        """Return the complete reciprocal-point count."""

        return len(self.kpoints_fractional)


class Wannier90InputFileWriter:
    """Write the demonstrated :class:`Wannier90InputData` subset deterministically."""

    __slots__ = ()

    def execute(self, input_data: Wannier90InputData) -> str:
        """Return one newline-terminated Wannier90 ``.win`` representation.

        Parameters
        ----------
        input_data
            Explicit settings, cell, atoms, projections, mesh, and reciprocal points.

        Returns
        -------
        str
            Deterministic UTF-8-compatible text.

        Raises
        ------
        TypeError
            If ``input_data`` is not exactly :class:`Wannier90InputData`.
        """

        if type(input_data) is not Wannier90InputData:
            raise TypeError("input_data must be Wannier90InputData")
        tolerance = repr(input_data.convergence_tolerance)
        if "e" in tolerance:
            mantissa, exponent = tolerance.split("e")
            if "." not in mantissa:
                mantissa += ".0"
            tolerance = f"{mantissa}d{exponent}"
        precondition = "true" if input_data.precondition else "false"
        write_hr = "true" if input_data.write_hr else "false"
        write_u_matrices = "true" if input_data.write_u_matrices else "false"
        translate_home_cell = "true" if input_data.translate_home_cell else "false"
        lines = [
            f"num_bands = {input_data.num_bands}",
            f"num_wann = {input_data.num_wann}",
            f"num_iter = {input_data.num_iter}",
            f"conv_tol = {tolerance}",
            f"conv_window = {input_data.convergence_window}",
            f"precond = {precondition}",
            f"search_shells = {input_data.search_shells}",
            f"write_hr = {write_hr}",
            f"write_u_matrices = {write_u_matrices}",
            f"translate_home_cell = {translate_home_cell}",
            "",
            "begin unit_cell_cart",
            "ang",
        ]
        lines.extend(
            " ".join(repr(component) for component in vector)
            for vector in input_data.unit_cell_cart_angstrom
        )
        lines.extend(["end unit_cell_cart", "", "begin atoms_frac"])
        lines.extend(
            f"{symbol} {repr(x_coordinate)} {repr(y_coordinate)} {repr(z_coordinate)}"
            for symbol, x_coordinate, y_coordinate, z_coordinate in (
                input_data.atoms_fractional
            )
        )
        lines.extend(["end atoms_frac", "", "begin projections"])
        lines.extend(input_data.projections)
        lines.extend(
            [
                "end projections",
                "",
                "mp_grid = " + " ".join(str(value) for value in input_data.mp_grid),
                "",
                "begin kpoints",
            ]
        )
        lines.extend(
            f"{kpoint[0]:.16f} 0.0 0.0" for kpoint in input_data.kpoints_fractional
        )
        lines.extend(["end kpoints", ""])
        return "\n".join(lines)


class Wannier90EigenvalueFileWriter:
    """Write complete k-point-by-band energy tables as Wannier90 ``.eig`` text."""

    __slots__ = ()

    def execute(self, data: Wannier90EigenvalueData) -> str:
        """Return indexed ``.eig`` text without converting energy magnitudes.

        The represented energy unit remains in ``data`` because ``.eig`` text does
        not encode a unit. The caller must select the unit expected by the consuming
        Wannier90 workflow.
        """

        if type(data) is not Wannier90EigenvalueData:
            raise TypeError("data must be Wannier90EigenvalueData")
        if not isinstance(data.eigenvalues.unit, PhysicalUnit):
            raise ValueError("eigenvalues must carry a physical energy unit")
        lines: list[str] = []
        for kpoint_index in range(data.kpoint_count):
            for band_index in range(data.band_count):
                value = data.eigenvalues.magnitude[kpoint_index, band_index]
                lines.append(f"{band_index + 1:5d} {kpoint_index + 1:5d} {value:.16e}")
        return "\n".join(lines) + "\n"


class Wannier90ProjectionFileWriter:
    """Write complete projection matrices as deterministic Wannier90 ``.amn`` text."""

    __slots__ = ()

    def execute(self, data: Wannier90ProjectionData, comment: str) -> str:
        """Return headered, indexed, newline-terminated ``.amn`` text."""

        if type(data) is not Wannier90ProjectionData:
            raise TypeError("data must be Wannier90ProjectionData")
        if type(comment) is not str:
            raise TypeError("comment must be a built-in str")
        if not comment or comment != comment.strip():
            raise ValueError("comment must be nonempty and stripped")
        if "\n" in comment or "\r" in comment:
            raise ValueError("comment must not contain line terminators")
        lines = [
            comment,
            f"{data.band_count:12d}{data.kpoint_count:12d}{data.wannier_count:12d}",
        ]
        for kpoint_index, matrix in enumerate(data.matrices, start=1):
            for projection_index in range(data.wannier_count):
                for band_index in range(data.band_count):
                    value = matrix.magnitude[band_index, projection_index]
                    lines.append(
                        f"{band_index + 1:5d}{projection_index + 1:5d}"
                        f"{kpoint_index:5d} {value.real:22.14e} "
                        f"{value.imag:22.14e}"
                    )
        return "\n".join(lines) + "\n"


class Wannier90NeighborOverlapFileWriter:
    """Write ``.mmn`` text after exact ordered correlation with parsed ``.nnkp``."""

    __slots__ = ()

    def execute(
        self,
        data: Wannier90NeighborOverlapData,
        neighbor_list: Wannier90NeighborListData,
        comment: str,
    ) -> str:
        """Return deterministic column-major ``.mmn`` text.

        Raises
        ------
        TypeError
            If an input has the wrong semantic type.
        ValueError
            If dimensions or any ordered neighbor header disagree with ``.nnkp``.
        """

        if type(data) is not Wannier90NeighborOverlapData:
            raise TypeError("data must be Wannier90NeighborOverlapData")
        if type(neighbor_list) is not Wannier90NeighborListData:
            raise TypeError("neighbor_list must be Wannier90NeighborListData")
        if type(comment) is not str:
            raise TypeError("comment must be a built-in str")
        if not comment or comment != comment.strip():
            raise ValueError("comment must be nonempty and stripped")
        if "\n" in comment or "\r" in comment:
            raise ValueError("comment must not contain line terminators")
        if data.kpoint_count != neighbor_list.kpoint_count:
            raise ValueError("overlap and nnkp k-point counts differ")
        if data.neighbor_count != neighbor_list.neighbor_count:
            raise ValueError("overlap and nnkp neighbor counts differ")
        for index, record in enumerate(neighbor_list.records):
            retained = (
                data.first_kpoint_indices[index] + 1,
                data.second_kpoint_indices[index] + 1,
                *data.reciprocal_shifts[index],
            )
            if retained != record:
                raise ValueError("overlap neighbor header differs from ordered nnkp")
        lines = [
            comment,
            f"{data.band_count:12d}{data.kpoint_count:12d}{data.neighbor_count:12d}",
        ]
        for index, matrix in enumerate(data.matrices):
            first, second, gx, gy, gz = neighbor_list.records[index]
            lines.append(f"{first:5d}{second:5d}{gx:5d}{gy:5d}{gz:5d}")
            for column_index in range(data.band_count):
                for row_index in range(data.band_count):
                    value = matrix.magnitude[row_index, column_index]
                    lines.append(f"{value.real:22.14e} {value.imag:22.14e}")
        return "\n".join(lines) + "\n"


@dataclass(frozen=True, slots=True)
class Wannier90InterfacePreparationRequest:
    """Collect one complete caller-supplied interface-preparation request.

    Parameters
    ----------
    input_data
        Explicit demonstrated ``.win`` subset.
    eigenvalues
        Complete energy table whose physical unit is retained but not converted.
    projections
        Complete dimensionless band-by-projection matrices.
    neighbor_list
        Parsed ``.nnkp`` points and ordered neighbor records.
    neighbor_overlaps
        Complete dimensionless overlap matrices and corresponding headers.
    projection_comment
        Nonempty single-line ``.amn`` comment.
    neighbor_overlap_comment
        Nonempty single-line ``.mmn`` comment.
    nnkp_kpoint_tolerance
        Nonnegative finite absolute tolerance for each dimensionless fractional
        reciprocal coordinate, represented by :class:`ScalarQuantity` with
        :class:`Unitless`. The tolerance addresses decimal precision in parsed
        ``.nnkp`` text; it is not a scientific-acceptance tolerance.
    """

    input_data: Wannier90InputData
    eigenvalues: Wannier90EigenvalueData
    projections: Wannier90ProjectionData
    neighbor_list: Wannier90NeighborListData
    neighbor_overlaps: Wannier90NeighborOverlapData
    projection_comment: str
    neighbor_overlap_comment: str
    nnkp_kpoint_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Require exact typed components and valid single-line comments."""

        expected = (
            (self.input_data, Wannier90InputData, "input_data"),
            (self.eigenvalues, Wannier90EigenvalueData, "eigenvalues"),
            (self.projections, Wannier90ProjectionData, "projections"),
            (self.neighbor_list, Wannier90NeighborListData, "neighbor_list"),
            (
                self.neighbor_overlaps,
                Wannier90NeighborOverlapData,
                "neighbor_overlaps",
            ),
        )
        for value, expected_type, name in expected:
            if type(value) is not expected_type:
                raise TypeError(f"{name} has the wrong semantic type")
        for comment in (self.projection_comment, self.neighbor_overlap_comment):
            if type(comment) is not str:
                raise TypeError("comments must be built-in strings")
            if not comment or comment != comment.strip():
                raise ValueError("comments must be nonempty and stripped")
            if "\n" in comment or "\r" in comment:
                raise ValueError("comments must not contain line terminators")
        if type(self.nnkp_kpoint_tolerance) is not ScalarQuantity:
            raise TypeError("nnkp_kpoint_tolerance must be ScalarQuantity")
        if not isinstance(self.nnkp_kpoint_tolerance.unit, Unitless):
            raise ValueError("nnkp_kpoint_tolerance must be unitless")
        if self.nnkp_kpoint_tolerance.magnitude < 0.0:
            raise ValueError("nnkp_kpoint_tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Wannier90InterfacePreparationResult:
    """Retain deterministic interface texts and compatibility diagnostics.

    ``maximum_nnkp_kpoint_defect`` is the maximum absolute dimensionless fractional
    coordinate difference between the explicit ``.win`` mesh and parsed ``.nnkp``
    points. It and ``nnkp_kpoint_tolerance`` are :class:`ScalarQuantity` values with
    :class:`Unitless`. The physical ``eigenvalue_unit`` accompanies ``.eig`` text
    because that native format does not encode a unit.
    """

    input_text: str
    eigenvalue_text: str
    projection_text: str
    neighbor_overlap_text: str
    eigenvalue_unit: PhysicalUnit
    maximum_nnkp_kpoint_defect: ScalarQuantity
    nnkp_kpoint_tolerance: ScalarQuantity

    def __post_init__(self) -> None:
        """Require four newline-terminated texts and a physical energy unit."""

        for text_name, text_value in (
            ("input_text", self.input_text),
            ("eigenvalue_text", self.eigenvalue_text),
            ("projection_text", self.projection_text),
            ("neighbor_overlap_text", self.neighbor_overlap_text),
        ):
            if type(text_value) is not str:
                raise TypeError(f"{text_name} must be a built-in str")
            if not text_value.endswith("\n"):
                raise ValueError(f"{text_name} must be newline-terminated")
        if not isinstance(self.eigenvalue_unit, PhysicalUnit):
            raise TypeError("eigenvalue_unit must be a physical unit")
        for quantity_name, quantity in (
            ("maximum_nnkp_kpoint_defect", self.maximum_nnkp_kpoint_defect),
            ("nnkp_kpoint_tolerance", self.nnkp_kpoint_tolerance),
        ):
            if type(quantity) is not ScalarQuantity:
                raise TypeError(f"{quantity_name} must be ScalarQuantity")
            if not isinstance(quantity.unit, Unitless):
                raise ValueError(f"{quantity_name} must be unitless")
            if quantity.magnitude < 0.0:
                raise ValueError(f"{quantity_name} must be nonnegative")
        if (
            self.maximum_nnkp_kpoint_defect.magnitude
            > self.nnkp_kpoint_tolerance.magnitude
        ):
            raise ValueError("nnkp k-point defect must not exceed its tolerance")


class Wannier90InterfacePreparationWorkflow:
    """Correlate and serialize a complete execution-independent interface set."""

    __slots__ = ()

    def execute(
        self, request: Wannier90InterfacePreparationRequest
    ) -> Wannier90InterfacePreparationResult:
        """Validate dimensions and return deterministic interface-file text.

        This Workflow performs no path discovery, file writing, external execution,
        unit conversion, overlap construction, scientific validation, or UQ.
        """

        if type(request) is not Wannier90InterfacePreparationRequest:
            raise TypeError("request must be Wannier90InterfacePreparationRequest")
        counts = (
            request.input_data.kpoint_count,
            request.eigenvalues.kpoint_count,
            request.projections.kpoint_count,
            request.neighbor_list.kpoint_count,
            request.neighbor_overlaps.kpoint_count,
        )
        if len(set(counts)) != 1:
            raise ValueError("interface k-point counts differ")
        nnkp_kpoints = request.neighbor_list.kpoints_fractional
        if nnkp_kpoints is None:
            raise ValueError("interface preparation requires parsed nnkp k points")
        maximum_nnkp_kpoint_defect = max(
            abs(input_value - nnkp_value)
            for input_kpoint, nnkp_kpoint in zip(
                request.input_data.kpoints_fractional, nnkp_kpoints, strict=True
            )
            for input_value, nnkp_value in zip(input_kpoint, nnkp_kpoint, strict=True)
        )
        if maximum_nnkp_kpoint_defect > request.nnkp_kpoint_tolerance.magnitude:
            raise ValueError("input and nnkp reciprocal points differ beyond tolerance")
        if request.input_data.num_bands != request.eigenvalues.band_count:
            raise ValueError("input and eigenvalue band counts differ")
        if request.input_data.num_bands != request.projections.band_count:
            raise ValueError("input and projection band counts differ")
        if request.input_data.num_bands != request.neighbor_overlaps.band_count:
            raise ValueError("input and overlap band counts differ")
        if request.input_data.num_wann != request.projections.wannier_count:
            raise ValueError("input and projection Wannier counts differ")
        eigenvalue_unit = request.eigenvalues.eigenvalues.unit
        if not isinstance(eigenvalue_unit, PhysicalUnit):
            raise ValueError("eigenvalues must carry a physical energy unit")
        input_text = Wannier90InputFileWriter().execute(request.input_data)
        eigenvalue_text = Wannier90EigenvalueFileWriter().execute(request.eigenvalues)
        projection_text = Wannier90ProjectionFileWriter().execute(
            request.projections, request.projection_comment
        )
        neighbor_overlap_text = Wannier90NeighborOverlapFileWriter().execute(
            request.neighbor_overlaps,
            request.neighbor_list,
            request.neighbor_overlap_comment,
        )
        return Wannier90InterfacePreparationResult(
            input_text=input_text,
            eigenvalue_text=eigenvalue_text,
            projection_text=projection_text,
            neighbor_overlap_text=neighbor_overlap_text,
            eigenvalue_unit=eigenvalue_unit,
            maximum_nnkp_kpoint_defect=ScalarQuantity(
                float(maximum_nnkp_kpoint_defect), Unitless()
            ),
            nnkp_kpoint_tolerance=request.nnkp_kpoint_tolerance,
        )
