"""Typed diagnostic packaging over maintained development CSV projections.

Scientific quantities are produced by the installed-owner development entrypoints.  This
module validates their historical CSV projection and derives labelled catalog and
sampled-cutoff records without recomputing scientific analyses.
Canonical bytes use the repository's :class:`BaseTypedRecord` serialization boundary;
no dataframe API or extracted JSON schema is maintained.
"""

from __future__ import annotations

import csv
import math
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Self

from ksdft2effmass.serialization import BaseTypedRecord, SerializableValue


class DiagnosticTable(StrEnum):
    """Name one maintained development table."""

    AMPLITUDE_RESOLUTION = "amplitude-resolution"
    HOPPING_POWER_MAP = "hopping-power-map"
    MOMENTUM_REFINEMENT = "momentum-refinement"
    NONFLAT_AMPLITUDE_RESOLUTION = "nonflat-amplitude-resolution"
    NONFLAT_CONTINUUM = "nonflat-continuum"
    NONFLAT_HOPPING_POWER_MAP = "nonflat-hopping-power-map"
    NONFLAT_MOMENTUM_REFINEMENT = "nonflat-momentum-refinement"
    NONFLAT_SELECTED_HOPPING_TAILS = "nonflat-selected-hopping-tails"
    PARENT_FAMILY_CONTINUUM = "parent-family-continuum"
    PARENT_FAMILY_SUMMARY = "parent-family-summary"
    SELECTED_HOPPING_TAILS = "selected-hopping-tails"
    TRUNCATION_CONSEQUENCES = "truncation-consequences"
    TRUNCATION_REFINEMENT = "truncation-refinement"
    TRUNCATION_SUMMARY = "truncation-summary"


@dataclass(frozen=True, slots=True)
class DiagnosticTableContract:
    """Bind one historical CSV projection to its ordered identity columns."""

    name: DiagnosticTable
    filename: str
    keys: tuple[str, ...]
    expected_rows: int


_CONTRACTS = (
    DiagnosticTableContract(
        DiagnosticTable.AMPLITUDE_RESOLUTION,
        "amplitude-resolution.csv",
        ("amplitude_intervals",),
        10,
    ),
    DiagnosticTableContract(
        DiagnosticTable.HOPPING_POWER_MAP,
        "hopping-power-map.csv",
        ("amplitude", "absolute_displacement"),
        845,
    ),
    DiagnosticTableContract(
        DiagnosticTable.MOMENTUM_REFINEMENT,
        "momentum-refinement.csv",
        ("coarse_mesh_size", "fine_mesh_size"),
        4,
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_AMPLITUDE_RESOLUTION,
        "nonflat-amplitude-resolution.csv",
        ("amplitude_intervals",),
        4,
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_CONTINUUM,
        "nonflat-continuum.csv",
        ("amplitude",),
        65,
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_HOPPING_POWER_MAP,
        "nonflat-hopping-power-map.csv",
        ("amplitude", "absolute_displacement"),
        845,
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_MOMENTUM_REFINEMENT,
        "nonflat-momentum-refinement.csv",
        ("coarse_mesh_size", "fine_mesh_size"),
        4,
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_SELECTED_HOPPING_TAILS,
        "nonflat-selected-hopping-tails.csv",
        ("amplitude", "maximum_range"),
        21,
    ),
    DiagnosticTableContract(
        DiagnosticTable.PARENT_FAMILY_CONTINUUM,
        "parent-family-continuum.csv",
        ("parent_hopping_scale", "amplitude"),
        165,
    ),
    DiagnosticTableContract(
        DiagnosticTable.PARENT_FAMILY_SUMMARY,
        "parent-family-summary.csv",
        ("parent_hopping_scale",),
        5,
    ),
    DiagnosticTableContract(
        DiagnosticTable.SELECTED_HOPPING_TAILS,
        "selected-hopping-tails.csv",
        ("amplitude", "maximum_range"),
        21,
    ),
    DiagnosticTableContract(
        DiagnosticTable.TRUNCATION_CONSEQUENCES,
        "truncation-consequences.csv",
        ("parent_hopping_scale", "amplitude", "maximum_range"),
        2805,
    ),
    DiagnosticTableContract(
        DiagnosticTable.TRUNCATION_REFINEMENT,
        "truncation-refinement.csv",
        ("parent_hopping_scale", "construction_mesh_size", "amplitude"),
        495,
    ),
    DiagnosticTableContract(
        DiagnosticTable.TRUNCATION_SUMMARY,
        "truncation-summary.csv",
        ("parent_hopping_scale",),
        5,
    ),
)

_REQUIRED_COLUMNS: Mapping[DiagnosticTable, tuple[str, ...]] = {
    DiagnosticTable.PARENT_FAMILY_SUMMARY: (
        "minimum_sampled_external_gap",
        "minimum_sampled_transport_singular_value",
        "maximum_transport_procrustes_residual",
        "maximum_transport_unitarity_defect",
        "closure_holonomy_phase_0",
        "closure_holonomy_phase_1",
        "periodic_closure_defect",
    ),
    DiagnosticTable.TRUNCATION_CONSEQUENCES: (
        "reference_ordinary_omitted_power",
        "comparison_ordinary_omitted_power",
        "reference_maximum_truncation_hamiltonian_error",
        "reference_rms_truncation_hamiltonian_error",
        "reference_maximum_band_error",
        "comparison_maximum_truncation_hamiltonian_error",
        "comparison_rms_truncation_hamiltonian_error",
        "comparison_maximum_truncation_band_error",
        "comparison_maximum_total_hamiltonian_error",
        "comparison_maximum_total_band_error",
    ),
    DiagnosticTable.TRUNCATION_REFINEMENT: (
        "reference_band_first_passing_range",
        "comparison_band_first_passing_range",
        "reference_hamiltonian_first_passing_range",
        "comparison_hamiltonian_first_passing_range",
    ),
}


def _contract(name: DiagnosticTable) -> DiagnosticTableContract:
    return next(item for item in _CONTRACTS if item.name is name)


def _category(quantity: str) -> str:
    if "external_gap" in quantity or "projector" in quantity:
        return "subspace"
    if (
        any(
            token in quantity
            for token in ("transport", "procrustes", "frame", "closure_holonomy")
        )
        or quantity == "periodic_closure_defect"
    ):
        return "frame-and-sewing"
    if "hamiltonian" in quantity or "operator" in quantity:
        return "operator"
    if "band" in quantity or "eigenvalue" in quantity:
        return "spectrum"
    if any(
        token in quantity
        for token in ("hopping", "omitted_power", "nyquist_power", "tail_weight")
    ):
        return "locality"
    if "correlation" in quantity or "angle" in quantity:
        return "alignment"
    if any(
        token in quantity
        for token in (
            "hermiticity",
            "parseval",
            "reconstruction",
            "verification",
            "quadrature",
            "identity_defect",
            "discrepancy",
        )
    ):
        return "numerical-consistency"
    if any(
        token in quantity
        for token in ("mesh", "refinement", "amplitude_intervals", "amplitude_nodes")
    ):
        return "resolution"
    return "control-or-derived"


def _aggregation(quantity: str) -> str:
    if "maximum" in quantity:
        return "maximum"
    if "minimum" in quantity:
        return "minimum"
    if "rms" in quantity:
        return "root-mean-square"
    if "phase" in quantity:
        return "phase-set-member"
    if "power" in quantity or "weight" in quantity:
        return "power"
    if "disposition" in quantity or quantity.startswith("passes_"):
        return "disposition"
    return "pointwise-or-control"


def _unit(quantity: str) -> str:
    if "phase" in quantity:
        return "radian"
    if any(
        token in quantity
        for token in (
            "mesh_size",
            "intervals",
            "nodes",
            "maximum_range",
            "displacement",
        )
    ):
        return "count"
    if "external_gap" in quantity or (
        "threshold" in quantity and "over_sqrt_kappa" not in quantity
    ):
        return "E_ref"
    return "unitless"


def _normalization(quantity: str) -> str:
    if "hamiltonian_error" in quantity:
        return "Frobenius/(sqrt(2)*E_ref)"
    if "band_error" in quantity or "band_defect" in quantity:
        return "energy/E_ref"
    if "omitted_power" in quantity or "nyquist_power" in quantity:
        return "Frobenius-power/(2*E_ref^2)"
    if "hopping_weight" in quantity or "tail_weight" in quantity:
        return "rank-two normalized Frobenius power"
    if "over_sqrt_kappa" in quantity:
        return "value/sqrt(kappa)"
    if "normalized_squared_operator_residual" in quantity:
        return "operator-residual^2/kappa"
    return "as-declared-by-source-table"


def _role(quantity: str) -> str:
    if "disposition" in quantity or quantity.startswith(("passes_", "within_")):
        return "disposition"
    if (
        "external_gap" in quantity
        or "minimum_sampled_transport_singular_value" in quantity
    ):
        return "qualification-gate"
    if any(
        token in quantity
        for token in (
            "defect",
            "hermiticity",
            "parseval",
            "unitarity",
            "rank_cutoff",
            "verification",
            "discrepancy",
        )
    ):
        return "numerical-check"
    if any(token in quantity for token in ("mesh_size", "intervals", "nodes")):
        return "control"
    return "reported-diagnostic"


def _require_fields(
    values: Mapping[str, SerializableValue], expected: tuple[str, ...]
) -> None:
    if set(values) != set(expected):
        raise ValueError("record fields do not match the declared inventory")


def _string(values: Mapping[str, SerializableValue], name: str) -> str:
    value = values[name]
    if type(value) is not str or not value:
        raise TypeError(f"{name} must be a nonempty built-in string")
    return value


def _float(values: Mapping[str, SerializableValue], name: str) -> float:
    value = values[name]
    if type(value) is not float or not math.isfinite(value):
        raise TypeError(f"{name} must be a finite built-in float")
    return value


def _optional_int(values: Mapping[str, SerializableValue], name: str) -> int | None:
    value = values[name]
    if value is not None and type(value) is not int:
        raise TypeError(f"{name} must be a built-in int or None")
    return value


@dataclass(frozen=True, slots=True)
class DiagnosticCatalogEntry(BaseTypedRecord):
    """Describe one diagnostic quantity without assigning an acceptance threshold."""

    quantity: str
    category: str
    aggregation: str
    unit: str
    normalization: str
    role: str

    @classmethod
    def from_quantity(cls, quantity: str) -> Self:
        """Construct metadata for one source-column quantity."""
        if type(quantity) is not str or not quantity:
            raise TypeError("quantity must be a nonempty built-in string")
        return cls(
            quantity=quantity,
            category=_category(quantity),
            aggregation=_aggregation(quantity),
            unit=_unit(quantity),
            normalization=_normalization(quantity),
            role=_role(quantity),
        )

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "quantity": self.quantity,
            "category": self.category,
            "aggregation": self.aggregation,
            "unit": self.unit,
            "normalization": self.normalization,
            "role": self.role,
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = (
            "quantity",
            "category",
            "aggregation",
            "unit",
            "normalization",
            "role",
        )
        _require_fields(values, fields)
        return cls(*(_string(values, name) for name in fields))

    def csv_row(self) -> Mapping[str, str]:
        """Return the historical catalog projection."""
        return {
            "quantity": self.quantity,
            "category": self.category,
            "aggregation": self.aggregation,
            "unit": self.unit,
            "normalization": self.normalization,
            "role": self.role,
        }


@dataclass(frozen=True, slots=True)
class DiagnosticCatalog(BaseTypedRecord):
    """Own the canonical ordered diagnostic catalog."""

    entries: tuple[DiagnosticCatalogEntry, ...]

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"entries": self.entries}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _require_fields(values, ("entries",))
        entries = values["entries"]
        if type(entries) is not tuple:
            raise TypeError("entries must be a tuple")
        decoded: list[DiagnosticCatalogEntry] = []
        for entry in entries:
            if not isinstance(entry, Mapping):
                raise TypeError("catalog entries must decode as mappings")
            decoded.append(DiagnosticCatalogEntry.from_dict(entry))
        return cls(tuple(decoded))


@dataclass(frozen=True, slots=True)
class SampledRangeDecision(BaseTypedRecord):
    """Retain distinct first-passing spectral and Hamiltonian cutoffs."""

    parent_hopping_scale: float
    amplitude: float
    tolerance: float
    reference_band_first_passing_range: int | None
    comparison_band_first_passing_range: int | None
    reference_hamiltonian_first_passing_range: int | None
    comparison_hamiltonian_first_passing_range: int | None

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {
            "parent_hopping_scale": self.parent_hopping_scale,
            "amplitude": self.amplitude,
            "tolerance": self.tolerance,
            "reference_band_first_passing_range": (
                self.reference_band_first_passing_range
            ),
            "comparison_band_first_passing_range": (
                self.comparison_band_first_passing_range
            ),
            "reference_hamiltonian_first_passing_range": (
                self.reference_hamiltonian_first_passing_range
            ),
            "comparison_hamiltonian_first_passing_range": (
                self.comparison_hamiltonian_first_passing_range
            ),
        }

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        fields = (
            "parent_hopping_scale",
            "amplitude",
            "tolerance",
            "reference_band_first_passing_range",
            "comparison_band_first_passing_range",
            "reference_hamiltonian_first_passing_range",
            "comparison_hamiltonian_first_passing_range",
        )
        _require_fields(values, fields)
        return cls(
            parent_hopping_scale=_float(values, fields[0]),
            amplitude=_float(values, fields[1]),
            tolerance=_float(values, fields[2]),
            reference_band_first_passing_range=_optional_int(values, fields[3]),
            comparison_band_first_passing_range=_optional_int(values, fields[4]),
            reference_hamiltonian_first_passing_range=_optional_int(values, fields[5]),
            comparison_hamiltonian_first_passing_range=_optional_int(values, fields[6]),
        )

    @property
    def band_sampled_range_inflation(self) -> int | None:
        """Return comparison minus reference spectral cutoff when both resolve."""
        if (
            self.reference_band_first_passing_range is None
            or self.comparison_band_first_passing_range is None
        ):
            return None
        return (
            self.comparison_band_first_passing_range
            - self.reference_band_first_passing_range
        )

    @property
    def hamiltonian_sampled_range_inflation(self) -> int | None:
        """Return comparison minus reference Hamiltonian cutoff when both resolve."""
        if (
            self.reference_hamiltonian_first_passing_range is None
            or self.comparison_hamiltonian_first_passing_range is None
        ):
            return None
        return (
            self.comparison_hamiltonian_first_passing_range
            - self.reference_hamiltonian_first_passing_range
        )

    def csv_row(self) -> Mapping[str, str]:
        """Return the historical sampled-decision CSV projection."""

        def rendered(value: int | None) -> str:
            return "unresolved" if value is None else str(value)

        return {
            "parent_hopping_scale": str(self.parent_hopping_scale),
            "amplitude": str(self.amplitude),
            "tolerance": str(self.tolerance),
            "reference_band_first_passing_range": rendered(
                self.reference_band_first_passing_range
            ),
            "comparison_band_first_passing_range": rendered(
                self.comparison_band_first_passing_range
            ),
            "reference_hamiltonian_first_passing_range": rendered(
                self.reference_hamiltonian_first_passing_range
            ),
            "comparison_hamiltonian_first_passing_range": rendered(
                self.comparison_hamiltonian_first_passing_range
            ),
            "band_sampled_range_inflation": rendered(self.band_sampled_range_inflation),
            "hamiltonian_sampled_range_inflation": rendered(
                self.hamiltonian_sampled_range_inflation
            ),
        }


@dataclass(frozen=True, slots=True)
class SampledRangeDecisions(BaseTypedRecord):
    """Own canonical ordered sampled range decisions."""

    decisions: tuple[SampledRangeDecision, ...]

    def _mapping(self) -> Mapping[str, SerializableValue]:
        return {"decisions": self.decisions}

    @classmethod
    def _from_mapping(cls, values: Mapping[str, SerializableValue]) -> Self:
        _require_fields(values, ("decisions",))
        decisions = values["decisions"]
        if type(decisions) is not tuple:
            raise TypeError("decisions must be a tuple")
        decoded: list[SampledRangeDecision] = []
        for decision in decisions:
            if not isinstance(decision, Mapping):
                raise TypeError("decisions must decode as mappings")
            decoded.append(SampledRangeDecision.from_dict(decision))
        return cls(tuple(decoded))


@dataclass(frozen=True, slots=True)
class DiagnosticTableData:
    """Hold one immutable historical CSV projection."""

    name: DiagnosticTable
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

    def _column_index(self, column: str) -> int:
        if type(column) is not str:
            raise TypeError("column must be a built-in string")
        try:
            return self.columns.index(column)
        except ValueError as error:
            raise KeyError(column) from error

    def text(self, row: tuple[str, ...], column: str) -> str:
        """Return one exact CSV field."""
        if type(row) is not tuple or len(row) != len(self.columns):
            raise TypeError("row must be one table row")
        return row[self._column_index(column)]

    def number(self, row: tuple[str, ...], column: str) -> float:
        """Return one finite numeric field."""
        value = float(self.text(row, column))
        if not math.isfinite(value):
            raise ValueError(f"{self.name.value}.{column} must be finite")
        return value

    def integer(self, row: tuple[str, ...], column: str) -> int:
        """Return one integer field."""
        return int(self.text(row, column))

    def unique_numbers(self, column: str) -> tuple[float, ...]:
        """Return first-occurrence numeric values in source order."""
        values: list[float] = []
        for row in self.rows:
            value = self.number(row, column)
            if value not in values:
                values.append(value)
        return tuple(values)

    def selected(
        self,
        *,
        parent_hopping_scale: float | None = None,
        amplitude: float | None = None,
        tolerance: float | None = None,
    ) -> tuple[tuple[str, ...], ...]:
        """Select rows using exact stored values and close float matching."""
        selected: list[tuple[str, ...]] = []
        for row in self.rows:
            if parent_hopping_scale is not None and not math.isclose(
                self.number(row, "parent_hopping_scale"),
                parent_hopping_scale,
                rel_tol=1.0e-12,
                abs_tol=1.0e-15,
            ):
                continue
            if amplitude is not None and not math.isclose(
                self.number(row, "amplitude"),
                amplitude,
                rel_tol=1.0e-12,
                abs_tol=1.0e-15,
            ):
                continue
            if tolerance is not None and not math.isclose(
                self.number(row, "tolerance"),
                tolerance,
                rel_tol=1.0e-12,
                abs_tol=1.0e-18,
            ):
                continue
            selected.append(row)
        return tuple(selected)


def _first_passing(
    table: DiagnosticTableData,
    rows: tuple[tuple[str, ...], ...],
    column: str,
    tolerance: float,
) -> int | None:
    return next(
        (
            table.integer(row, "maximum_range")
            for row in rows
            if table.number(row, column) <= tolerance
        ),
        None,
    )


@dataclass(frozen=True, slots=True)
class DiagnosticBundle:
    """Load immutable diagnostic projections and derive typed presentation records."""

    _directory: Path
    _tables: tuple[DiagnosticTableData, ...]

    @classmethod
    def load(cls, directory: Path) -> Self:
        """Load all maintained CSV projections and validate identities and grids."""
        if not isinstance(directory, Path):
            raise TypeError("directory must be a pathlib.Path")
        resolved = directory.resolve()
        tables = tuple(cls._load_table(resolved, contract) for contract in _CONTRACTS)
        bundle = cls(resolved, tables)
        bundle._validate_relationships()
        return bundle

    @staticmethod
    def _load_table(
        directory: Path, contract: DiagnosticTableContract
    ) -> DiagnosticTableData:
        path = directory / contract.filename
        if not path.is_file():
            raise FileNotFoundError(path)
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            try:
                columns = tuple(next(reader))
            except StopIteration as error:
                raise ValueError(f"{contract.filename} must not be empty") from error
            rows = tuple(tuple(row) for row in reader)
        if not columns or len(set(columns)) != len(columns):
            raise ValueError(f"{contract.filename} must have unique columns")
        if any(
            len(row) != len(columns) or any(value == "" for value in row)
            for row in rows
        ):
            raise ValueError(f"{contract.filename} contains missing values")
        required = (*contract.keys, *_REQUIRED_COLUMNS.get(contract.name, ()))
        if any(column not in columns for column in required):
            raise ValueError(
                f"{contract.filename} columns do not match required fields"
            )
        if len(rows) != contract.expected_rows:
            raise ValueError(
                f"{contract.filename} has {len(rows)} rows; "
                f"expected {contract.expected_rows}"
            )
        indexes = tuple(columns.index(key) for key in contract.keys)
        identities = tuple(tuple(row[index] for index in indexes) for row in rows)
        if len(set(identities)) != len(identities):
            raise ValueError(f"{contract.filename} contains duplicate identities")
        numeric_identities = tuple(
            tuple(float(value) for value in identity) for identity in identities
        )
        if numeric_identities != tuple(sorted(numeric_identities)):
            raise ValueError(f"{contract.filename} violates canonical key order")
        return DiagnosticTableData(contract.name, columns, rows)

    @property
    def directory(self) -> Path:
        """Return the resolved source directory."""
        return self._directory

    @property
    def names(self) -> tuple[DiagnosticTable, ...]:
        """Return table names in canonical source order."""
        return tuple(table.name for table in self._tables)

    def table(self, name: DiagnosticTable) -> DiagnosticTableData:
        """Return one immutable table projection."""
        if type(name) is not DiagnosticTable:
            raise TypeError("name must be a DiagnosticTable")
        return next(table for table in self._tables if table.name is name)

    @property
    def long_form_row_count(self) -> int:
        """Return the number of identity-labelled source values."""
        return sum(
            len(table.rows) * (len(table.columns) - len(_contract(table.name).keys))
            for table in self._tables
        )

    def catalog(self) -> DiagnosticCatalog:
        """Return canonical metadata for every distinct non-identity quantity."""
        quantities = {
            column
            for table in self._tables
            for column in table.columns
            if column not in _contract(table.name).keys
        }
        entries = tuple(
            sorted(
                (DiagnosticCatalogEntry.from_quantity(value) for value in quantities),
                key=lambda item: (item.category, item.quantity),
            )
        )
        return DiagnosticCatalog(entries)

    def sampled_range_decisions(
        self, tolerances: tuple[float, ...]
    ) -> SampledRangeDecisions:
        """Return first passing sampled cutoffs for four separate error channels."""
        if type(tolerances) is not tuple or not tolerances:
            raise TypeError("tolerances must be a nonempty tuple")
        if any(
            type(value) is not float or not math.isfinite(value) or value <= 0.0
            for value in tolerances
        ):
            raise ValueError("tolerances must contain finite positive built-in floats")
        if tolerances != tuple(sorted(set(tolerances), reverse=True)):
            raise ValueError("tolerances must be unique and strictly decreasing")
        table = self.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
        decisions: list[SampledRangeDecision] = []
        for parent_scale in table.unique_numbers("parent_hopping_scale"):
            parent_rows = table.selected(parent_hopping_scale=parent_scale)
            amplitudes: list[float] = []
            for row in parent_rows:
                amplitude = table.number(row, "amplitude")
                if amplitude not in amplitudes:
                    amplitudes.append(amplitude)
            for amplitude in amplitudes:
                rows = table.selected(
                    parent_hopping_scale=parent_scale,
                    amplitude=amplitude,
                )
                for tolerance in tolerances:
                    decisions.append(
                        SampledRangeDecision(
                            parent_hopping_scale=parent_scale,
                            amplitude=amplitude,
                            tolerance=tolerance,
                            reference_band_first_passing_range=_first_passing(
                                table,
                                rows,
                                "reference_maximum_band_error",
                                tolerance,
                            ),
                            comparison_band_first_passing_range=_first_passing(
                                table,
                                rows,
                                "comparison_maximum_total_band_error",
                                tolerance,
                            ),
                            reference_hamiltonian_first_passing_range=_first_passing(
                                table,
                                rows,
                                "reference_maximum_truncation_hamiltonian_error",
                                tolerance,
                            ),
                            comparison_hamiltonian_first_passing_range=_first_passing(
                                table,
                                rows,
                                "comparison_maximum_total_hamiltonian_error",
                                tolerance,
                            ),
                        )
                    )
        return SampledRangeDecisions(tuple(decisions))

    def _validate_relationships(self) -> None:
        continuum = self.table(DiagnosticTable.PARENT_FAMILY_CONTINUUM)
        summary = self.table(DiagnosticTable.PARENT_FAMILY_SUMMARY)
        truncation = self.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
        refinement = self.table(DiagnosticTable.TRUNCATION_REFINEMENT)
        truncation_summary = self.table(DiagnosticTable.TRUNCATION_SUMMARY)
        scales = summary.unique_numbers("parent_hopping_scale")
        for table in (continuum, truncation, refinement, truncation_summary):
            if table.unique_numbers("parent_hopping_scale") != scales:
                raise ValueError("maintained tables must preserve parent-scale order")
        amplitudes = continuum.unique_numbers("amplitude")
        if truncation.unique_numbers("amplitude") != amplitudes:
            raise ValueError("parent and truncation tables must share amplitudes")
        if refinement.unique_numbers("amplitude") != amplitudes:
            raise ValueError("parent and refinement tables must share amplitudes")
        ranges = truncation.unique_numbers("maximum_range")
        if len(continuum.rows) != len(scales) * len(amplitudes):
            raise ValueError("parent continuum must contain the complete product grid")
        if len(truncation.rows) != len(scales) * len(amplitudes) * len(ranges):
            raise ValueError("truncation table must contain the complete product grid")
        meshes = refinement.unique_numbers("construction_mesh_size")
        if len(refinement.rows) != len(scales) * len(meshes) * len(amplitudes):
            raise ValueError("refinement table must contain the complete product grid")


__all__ = [
    "DiagnosticBundle",
    "DiagnosticCatalog",
    "DiagnosticCatalogEntry",
    "DiagnosticTable",
    "DiagnosticTableData",
    "SampledRangeDecision",
    "SampledRangeDecisions",
]
