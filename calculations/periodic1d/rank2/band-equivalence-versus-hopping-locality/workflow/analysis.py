"""Validated pandas bundle for experiment-owned diagnostic tables.

Scientific calculations remain in the experiment actions and analysis producers. This
module only loads, validates, reshapes, and labels their CSV outputs for inspection and
plotting.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]


class DiagnosticTable(StrEnum):
    """Name one maintained analysis table."""

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
    """Bind one CSV source to its ordered identity columns."""

    name: DiagnosticTable
    filename: str
    keys: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DiagnosticMetricMetadata:
    """Describe one diagnostic without assigning it an acceptance threshold."""

    category: str
    aggregation: str
    unit: str
    normalization: str
    role: str


_CONTRACTS = (
    DiagnosticTableContract(
        DiagnosticTable.AMPLITUDE_RESOLUTION,
        "amplitude-resolution.csv",
        ("amplitude_intervals",),
    ),
    DiagnosticTableContract(
        DiagnosticTable.HOPPING_POWER_MAP,
        "hopping-power-map.csv",
        ("amplitude", "absolute_displacement"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.MOMENTUM_REFINEMENT,
        "momentum-refinement.csv",
        ("coarse_mesh_size", "fine_mesh_size"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_AMPLITUDE_RESOLUTION,
        "nonflat-amplitude-resolution.csv",
        ("amplitude_intervals",),
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_CONTINUUM,
        "nonflat-continuum.csv",
        ("amplitude",),
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_HOPPING_POWER_MAP,
        "nonflat-hopping-power-map.csv",
        ("amplitude", "absolute_displacement"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_MOMENTUM_REFINEMENT,
        "nonflat-momentum-refinement.csv",
        ("coarse_mesh_size", "fine_mesh_size"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.NONFLAT_SELECTED_HOPPING_TAILS,
        "nonflat-selected-hopping-tails.csv",
        ("amplitude", "maximum_range"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.PARENT_FAMILY_CONTINUUM,
        "parent-family-continuum.csv",
        ("parent_hopping_scale", "amplitude"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.PARENT_FAMILY_SUMMARY,
        "parent-family-summary.csv",
        ("parent_hopping_scale",),
    ),
    DiagnosticTableContract(
        DiagnosticTable.SELECTED_HOPPING_TAILS,
        "selected-hopping-tails.csv",
        ("amplitude", "maximum_range"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.TRUNCATION_CONSEQUENCES,
        "truncation-consequences.csv",
        ("parent_hopping_scale", "amplitude", "maximum_range"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.TRUNCATION_REFINEMENT,
        "truncation-refinement.csv",
        ("parent_hopping_scale", "construction_mesh_size", "amplitude"),
    ),
    DiagnosticTableContract(
        DiagnosticTable.TRUNCATION_SUMMARY,
        "truncation-summary.csv",
        ("parent_hopping_scale",),
    ),
)


_EXPECTED_ROWS: dict[DiagnosticTable, int] = {
    DiagnosticTable.AMPLITUDE_RESOLUTION: 10,
    DiagnosticTable.HOPPING_POWER_MAP: 845,
    DiagnosticTable.MOMENTUM_REFINEMENT: 4,
    DiagnosticTable.NONFLAT_AMPLITUDE_RESOLUTION: 4,
    DiagnosticTable.NONFLAT_CONTINUUM: 65,
    DiagnosticTable.NONFLAT_HOPPING_POWER_MAP: 845,
    DiagnosticTable.NONFLAT_MOMENTUM_REFINEMENT: 4,
    DiagnosticTable.NONFLAT_SELECTED_HOPPING_TAILS: 21,
    DiagnosticTable.PARENT_FAMILY_CONTINUUM: 165,
    DiagnosticTable.PARENT_FAMILY_SUMMARY: 5,
    DiagnosticTable.SELECTED_HOPPING_TAILS: 21,
    DiagnosticTable.TRUNCATION_CONSEQUENCES: 2805,
    DiagnosticTable.TRUNCATION_REFINEMENT: 495,
    DiagnosticTable.TRUNCATION_SUMMARY: 5,
}

_EXPECTED_COLUMNS: dict[DiagnosticTable, tuple[str, ...]] = {
    DiagnosticTable.AMPLITUDE_RESOLUTION: (
        "amplitude_intervals",
        "amplitude_nodes",
        "maximum_operator_threshold_midpoint_interpolation_defect",
        "maximum_joint_threshold_midpoint_interpolation_defect",
        "passes_unit_scale_draft_tolerance",
    ),
    DiagnosticTable.HOPPING_POWER_MAP: (
        "amplitude",
        "absolute_displacement",
        "normalized_hopping_weight",
    ),
    DiagnosticTable.MOMENTUM_REFINEMENT: (
        "coarse_mesh_size",
        "fine_mesh_size",
        "maximum_correlation_change",
        "maximum_threshold_change",
        "maximum_hopping_weight_change",
        "maximum_hopping_block_power_change",
        "maximum_angle_change",
        "maximum_fine_quadrature_defect",
        "maximum_band_defect",
        "maximum_identity_defect",
        "maximum_parseval_defect",
        "within_draft_tolerances",
    ),
    DiagnosticTable.NONFLAT_AMPLITUDE_RESOLUTION: (
        "amplitude_intervals",
        "maximum_correlation_midpoint_defect",
        "maximum_operator_threshold_midpoint_defect",
        "maximum_joint_threshold_midpoint_defect",
        "maximum_nonzero_hopping_weight_midpoint_defect",
        "maximum_hopping_block_power_midpoint_defect",
        "passes_draft_tolerance",
    ),
    DiagnosticTable.NONFLAT_CONTINUUM: (
        "amplitude",
        "maximum_band_defect",
        "maximum_correlation",
        "minimum_operator_threshold",
        "exact_spectrum_joint_operator_threshold",
        "reference_nonzero_hopping_weight",
        "comparison_nonzero_hopping_weight",
    ),
    DiagnosticTable.NONFLAT_HOPPING_POWER_MAP: (
        "amplitude",
        "absolute_displacement",
        "reference_normalized_hopping_weight",
        "comparison_normalized_hopping_weight",
    ),
    DiagnosticTable.NONFLAT_MOMENTUM_REFINEMENT: (
        "coarse_mesh_size",
        "fine_mesh_size",
        "maximum_parent_diagnostic_change",
        "maximum_shared_parent_eigenvalue_defect",
        "maximum_shared_projector_defect",
        "maximum_correlation_change",
        "maximum_threshold_change",
        "maximum_hopping_weight_change",
        "maximum_hopping_block_power_change",
        "maximum_angle_change",
        "maximum_band_defect",
        "maximum_reconstruction_defect",
        "maximum_parseval_defect",
        "fine_mesh_verification_defect",
        "within_draft_tolerances",
    ),
    DiagnosticTable.NONFLAT_SELECTED_HOPPING_TAILS: (
        "amplitude",
        "maximum_range",
        "reference_normalized_tail_weight",
        "comparison_normalized_tail_weight",
        "maximum_correlation",
        "minimum_operator_threshold",
        "exact_spectrum_joint_operator_threshold",
    ),
    DiagnosticTable.PARENT_FAMILY_CONTINUUM: (
        "parent_hopping_scale",
        "amplitude",
        "maximum_correlation",
        "splitting_scale",
        "minimum_operator_threshold_over_sqrt_kappa",
        "joint_threshold_over_sqrt_kappa",
        "reference_nonzero_hopping_weight",
        "comparison_nonzero_hopping_weight",
        "excess_nonzero_hopping_weight",
        "normalized_squared_operator_residual",
        "normalized_excess_nonzero_hopping_weight",
        "flat_identity_departure",
        "maximum_band_defect",
    ),
    DiagnosticTable.PARENT_FAMILY_SUMMARY: (
        "parent_hopping_scale",
        "momentum_disposition",
        "minimum_sampled_external_gap",
        "minimum_sampled_transport_singular_value",
        "maximum_transport_procrustes_residual",
        "maximum_transport_unitarity_defect",
        "maximum_transport_rank_cutoff",
        "closure_holonomy_phase_0",
        "closure_holonomy_phase_1",
        "closure_holonomy_unitarity_defect",
        "maximum_frame_orthonormality_defect",
        "periodic_closure_defect",
        "maximum_reference_hermiticity_defect",
        "maximum_final_parent_invariant_change",
        "maximum_final_outcome_change",
        "verification_defect",
        "endpoint_minimum_threshold_over_sqrt_kappa",
        "endpoint_excess_nonzero_hopping_weight",
    ),
    DiagnosticTable.SELECTED_HOPPING_TAILS: (
        "amplitude",
        "maximum_range",
        "normalized_tail_weight",
        "finite_mesh_maximum_correlation",
        "minimum_operator_threshold",
        "exact_spectrum_joint_operator_threshold",
        "nonzero_hopping_weight",
    ),
    DiagnosticTable.TRUNCATION_CONSEQUENCES: (
        "parent_hopping_scale",
        "amplitude",
        "maximum_range",
        "reference_nyquist_power",
        "comparison_nyquist_power",
        "maximum_direct_band_defect",
        "comparison_maximum_interpolation_hamiltonian_error",
        "comparison_rms_interpolation_hamiltonian_error",
        "comparison_maximum_interpolation_band_error",
        "comparison_rms_interpolation_band_error",
        "reference_ordinary_omitted_power",
        "comparison_ordinary_omitted_power",
        "reference_total_omitted_power",
        "comparison_total_omitted_power",
        "reference_maximum_truncation_hamiltonian_error",
        "reference_rms_truncation_hamiltonian_error",
        "reference_maximum_band_error",
        "reference_rms_band_error",
        "comparison_maximum_truncation_hamiltonian_error",
        "comparison_rms_truncation_hamiltonian_error",
        "comparison_maximum_truncation_band_error",
        "comparison_rms_truncation_band_error",
        "comparison_maximum_total_hamiltonian_error",
        "comparison_rms_total_hamiltonian_error",
        "comparison_maximum_total_band_error",
        "comparison_rms_total_band_error",
    ),
    DiagnosticTable.TRUNCATION_REFINEMENT: (
        "parent_hopping_scale",
        "amplitude",
        "construction_mesh_size",
        "evaluation_mesh_size",
        "decision_tolerance",
        "verification_discrepancy",
        "reference_band_first_passing_range",
        "reference_band_passing_error",
        "reference_band_preceding_error",
        "comparison_band_first_passing_range",
        "comparison_band_passing_error",
        "comparison_band_preceding_error",
        "reference_hamiltonian_first_passing_range",
        "reference_hamiltonian_passing_error",
        "reference_hamiltonian_preceding_error",
        "comparison_hamiltonian_first_passing_range",
        "comparison_hamiltonian_passing_error",
        "comparison_hamiltonian_preceding_error",
    ),
    DiagnosticTable.TRUNCATION_SUMMARY: (
        "parent_hopping_scale",
        "construction_mesh_size",
        "evaluation_mesh_size",
        "minimum_mesh_separation",
        "maximum_direct_band_defect",
        "maximum_interpolation_hamiltonian_error",
        "maximum_interpolation_band_error",
        "endpoint_range_0_total_hamiltonian_error",
        "endpoint_range_0_total_band_error",
        "endpoint_range_8_total_hamiltonian_error",
        "endpoint_range_8_total_band_error",
        "endpoint_range_16_total_hamiltonian_error",
        "endpoint_range_16_total_band_error",
    ),
}


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


def diagnostic_metric_metadata(quantity: str) -> DiagnosticMetricMetadata:
    """Return display metadata without changing the source value."""
    if type(quantity) is not str or not quantity:
        raise TypeError("quantity must be a nonempty built-in string")
    return DiagnosticMetricMetadata(
        category=_category(quantity),
        aggregation=_aggregation(quantity),
        unit=_unit(quantity),
        normalization=_normalization(quantity),
        role=_role(quantity),
    )


class DiagnosticBundle:
    """Hold validated analysis tables and return defensive pandas copies."""

    __slots__ = ("_directory", "_tables")

    def __init__(
        self,
        directory: Path,
        tables: tuple[tuple[DiagnosticTable, pd.DataFrame], ...],
    ) -> None:
        self._directory = directory
        self._tables = tables

    @classmethod
    def load(cls, directory: Path) -> DiagnosticBundle:
        """Load every maintained diagnostic CSV and validate table relationships."""
        if not isinstance(directory, Path):
            raise TypeError("directory must be a pathlib.Path")
        resolved = directory.resolve()
        tables: list[tuple[DiagnosticTable, pd.DataFrame]] = []
        for contract in _CONTRACTS:
            path = resolved / contract.filename
            if not path.is_file():
                raise FileNotFoundError(path)
            frame = pd.read_csv(path)
            cls._validate_table(frame, contract)
            tables.append((contract.name, frame))
        bundle = cls(resolved, tuple(tables))
        bundle._validate_relationships()
        return bundle

    @property
    def directory(self) -> Path:
        """Return the source directory."""
        return self._directory

    @property
    def names(self) -> tuple[DiagnosticTable, ...]:
        """Return table names in canonical source order."""
        return tuple(name for name, _ in self._tables)

    def table(self, name: DiagnosticTable) -> pd.DataFrame:
        """Return a deep copy of one canonical table."""
        if type(name) is not DiagnosticTable:
            raise TypeError("name must be a DiagnosticTable")
        for candidate, frame in self._tables:
            if candidate is name:
                return frame.copy(deep=True)
        raise KeyError(name)

    def sampled_range_decisions(
        self,
        tolerances: tuple[float, ...],
    ) -> pd.DataFrame:
        """Return first passing sampled cutoffs for matrix and spectral criteria."""
        if type(tolerances) is not tuple or not tolerances:
            raise TypeError("tolerances must be a nonempty tuple")
        if any(type(value) is not float or value <= 0.0 for value in tolerances):
            raise ValueError("tolerances must contain positive built-in floats")
        if tolerances != tuple(sorted(set(tolerances), reverse=True)):
            raise ValueError("tolerances must be unique and strictly decreasing")

        source = self.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
        rows: list[dict[str, float | int | str]] = []
        for parent_scale in source["parent_hopping_scale"].drop_duplicates():
            parent = source.loc[source["parent_hopping_scale"] == parent_scale]
            for amplitude in parent["amplitude"].drop_duplicates():
                point = parent.loc[parent["amplitude"] == amplitude]
                for tolerance in tolerances:
                    selections: dict[str, int | None] = {}
                    for name, column in (
                        ("reference_band", "reference_maximum_band_error"),
                        (
                            "comparison_band",
                            "comparison_maximum_total_band_error",
                        ),
                        (
                            "reference_hamiltonian",
                            "reference_maximum_truncation_hamiltonian_error",
                        ),
                        (
                            "comparison_hamiltonian",
                            "comparison_maximum_total_hamiltonian_error",
                        ),
                    ):
                        passing = point.loc[point[column] <= tolerance, "maximum_range"]
                        selections[name] = (
                            None if passing.empty else int(passing.iloc[0])
                        )
                    row: dict[str, float | int | str] = {
                        "parent_hopping_scale": float(parent_scale),
                        "amplitude": float(amplitude),
                        "tolerance": tolerance,
                    }
                    for name, selection in selections.items():
                        row[f"{name}_first_passing_range"] = (
                            "unresolved" if selection is None else selection
                        )
                    for channel in ("band", "hamiltonian"):
                        reference = selections[f"reference_{channel}"]
                        comparison = selections[f"comparison_{channel}"]
                        row[f"{channel}_sampled_range_inflation"] = (
                            "unresolved"
                            if reference is None or comparison is None
                            else comparison - reference
                        )
                    rows.append(row)
        return pd.DataFrame.from_records(rows)

    def long_form(self, *, numeric_only: bool = False) -> pd.DataFrame:
        """Return all diagnostic values in one metadata-labelled tidy table."""
        if type(numeric_only) is not bool:
            raise TypeError("numeric_only must be a built-in bool")
        parts: list[pd.DataFrame] = []
        contracts = {contract.name: contract for contract in _CONTRACTS}
        for name, source in self._tables:
            contract = contracts[name]
            value_columns = tuple(
                column for column in source.columns if column not in contract.keys
            )
            melted = source.melt(
                id_vars=list(contract.keys),
                value_vars=list(value_columns),
                var_name="quantity",
                value_name="value",
            )
            melted.insert(0, "source_table", name.value)
            metadata = tuple(
                diagnostic_metric_metadata(str(quantity))
                for quantity in melted["quantity"]
            )
            melted["category"] = tuple(item.category for item in metadata)
            melted["aggregation"] = tuple(item.aggregation for item in metadata)
            melted["unit"] = tuple(item.unit for item in metadata)
            melted["normalization"] = tuple(item.normalization for item in metadata)
            melted["role"] = tuple(item.role for item in metadata)
            if numeric_only:
                melted["value"] = pd.to_numeric(melted["value"], errors="coerce")
                melted = melted.dropna(subset=["value"])
            parts.append(melted)
        return pd.concat(parts, ignore_index=True, sort=False)

    @staticmethod
    def _validate_table(
        frame: pd.DataFrame,
        contract: DiagnosticTableContract,
    ) -> None:
        if frame.empty:
            raise ValueError(f"{contract.filename} must not be empty")
        actual_columns = tuple(str(column) for column in frame.columns)
        expected_columns = _EXPECTED_COLUMNS[contract.name]
        if actual_columns != expected_columns:
            raise ValueError(
                f"{contract.filename} columns do not match the declared schema"
            )
        missing = tuple(key for key in contract.keys if key not in frame.columns)
        if missing:
            raise ValueError(
                f"{contract.filename} is missing identity columns {missing}"
            )
        if bool(frame.isna().any(axis=None)):
            raise ValueError(f"{contract.filename} contains missing values")
        if bool(frame.duplicated(subset=list(contract.keys)).any()):
            raise ValueError(f"{contract.filename} contains duplicate identities")
        ordered = frame.sort_values(
            list(contract.keys), kind="mergesort", ignore_index=True
        )
        actual_keys = frame.loc[:, list(contract.keys)].reset_index(drop=True)
        expected_keys = ordered.loc[:, list(contract.keys)]
        if not actual_keys.equals(expected_keys):
            raise ValueError(f"{contract.filename} violates canonical key order")
        expected_rows = _EXPECTED_ROWS[contract.name]
        if len(frame) != expected_rows:
            raise ValueError(
                f"{contract.filename} has {len(frame)} rows; expected {expected_rows}"
            )

    def _validate_relationships(self) -> None:
        continuum = self.table(DiagnosticTable.PARENT_FAMILY_CONTINUUM)
        summary = self.table(DiagnosticTable.PARENT_FAMILY_SUMMARY)
        truncation = self.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
        truncation_refinement = self.table(DiagnosticTable.TRUNCATION_REFINEMENT)
        truncation_summary = self.table(DiagnosticTable.TRUNCATION_SUMMARY)

        parent_scales = tuple(summary["parent_hopping_scale"])
        if tuple(truncation_summary["parent_hopping_scale"]) != parent_scales:
            raise ValueError("parent and truncation summaries must use the same scales")
        if tuple(continuum["parent_hopping_scale"].drop_duplicates()) != parent_scales:
            raise ValueError("parent continuum must preserve summary scale order")
        if tuple(truncation["parent_hopping_scale"].drop_duplicates()) != parent_scales:
            raise ValueError("truncation table must preserve summary scale order")
        if (
            tuple(truncation_refinement["parent_hopping_scale"].drop_duplicates())
            != parent_scales
        ):
            raise ValueError("truncation refinement must preserve summary scale order")

        amplitudes = tuple(continuum["amplitude"].drop_duplicates())
        if tuple(truncation["amplitude"].drop_duplicates()) != amplitudes:
            raise ValueError(
                "parent and truncation tables must use the same amplitudes"
            )
        if tuple(truncation_refinement["amplitude"].drop_duplicates()) != amplitudes:
            raise ValueError(
                "parent and truncation refinement tables must use the same amplitudes"
            )
        ranges = tuple(truncation["maximum_range"].drop_duplicates())
        expected_continuum_index = pd.MultiIndex.from_product(
            (parent_scales, amplitudes),
            names=("parent_hopping_scale", "amplitude"),
        )
        actual_continuum_index = pd.MultiIndex.from_frame(
            continuum.loc[:, ["parent_hopping_scale", "amplitude"]]
        )
        if not actual_continuum_index.equals(expected_continuum_index):
            raise ValueError(
                "parent continuum does not contain the complete product grid"
            )
        expected_truncation_index = pd.MultiIndex.from_product(
            (parent_scales, amplitudes, ranges),
            names=("parent_hopping_scale", "amplitude", "maximum_range"),
        )
        actual_truncation_index = pd.MultiIndex.from_frame(
            truncation.loc[:, ["parent_hopping_scale", "amplitude", "maximum_range"]]
        )
        if not actual_truncation_index.equals(expected_truncation_index):
            raise ValueError(
                "truncation table does not contain the complete product grid"
            )
        refinement_meshes = tuple(
            truncation_refinement["construction_mesh_size"].drop_duplicates()
        )
        expected_refinement_index = pd.MultiIndex.from_product(
            (parent_scales, refinement_meshes, amplitudes),
            names=(
                "parent_hopping_scale",
                "construction_mesh_size",
                "amplitude",
            ),
        )
        actual_refinement_index = pd.MultiIndex.from_frame(
            truncation_refinement.loc[
                :, ["parent_hopping_scale", "construction_mesh_size", "amplitude"]
            ]
        )
        if not actual_refinement_index.equals(expected_refinement_index):
            raise ValueError(
                "truncation refinement does not contain the complete product grid"
            )


__all__ = [
    "DiagnosticBundle",
    "DiagnosticMetricMetadata",
    "DiagnosticTable",
    "DiagnosticTableContract",
    "diagnostic_metric_metadata",
]
