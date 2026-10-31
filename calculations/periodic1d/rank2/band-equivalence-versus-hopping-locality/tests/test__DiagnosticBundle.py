"""Software verification for typed diagnostic packaging and plotting access."""

from __future__ import annotations

import csv
import io
import math
import shutil
from collections.abc import Mapping
from pathlib import Path

import matplotlib.pyplot as plt
import pytest
from development_diagnostic_plots import (
    plot_frame_and_sewing_diagnostics,
    plot_hamiltonian_and_spectral_errors,
    plot_sampled_range_decisions,
)
from development_diagnostics import (
    DiagnosticBundle,
    DiagnosticCatalog,
    DiagnosticTable,
    SampledRangeDecisions,
)

pytestmark = pytest.mark.software_verification

RESULTS = (
    Path(__file__).resolve().parents[1] / "simulations" / "development" / "results"
)


def _copy_tables(destination: Path) -> None:
    destination.mkdir()
    for source in RESULTS.glob("*.csv"):
        shutil.copy2(source, destination / source.name)


def _read_csv(path: Path) -> tuple[tuple[str, ...], tuple[tuple[str, ...], ...]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        return tuple(next(reader)), tuple(tuple(row) for row in reader)


def _write_csv(
    path: Path,
    columns: tuple[str, ...],
    rows: tuple[tuple[str, ...], ...],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)


def _csv_projection(
    columns: tuple[str, ...], rows: tuple[Mapping[str, str], ...]
) -> str:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


class TestDiagnosticBundle:
    """Establish immutable loading, typed metadata, decisions, and plot consumption."""

    def test_load__validates_complete_development_tables(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)

        assert len(bundle.names) == 14
        truncation = bundle.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
        refinement = bundle.table(DiagnosticTable.TRUNCATION_REFINEMENT)
        assert len(truncation.rows) == 2805
        assert len(refinement.rows) == 495
        assert truncation.columns[:3] == (
            "parent_hopping_scale",
            "amplitude",
            "maximum_range",
        )
        assert "comparison_maximum_total_hamiltonian_error" in truncation.columns
        assert "comparison_maximum_total_band_error" in truncation.columns

    def test_load__rejects_a_missing_required_diagnostic_column(
        self, tmp_path: Path
    ) -> None:
        copied = tmp_path / "analysis"
        _copy_tables(copied)
        path = copied / "parent-family-summary.csv"
        columns, rows = _read_csv(path)
        removed = columns.index("closure_holonomy_phase_1")
        _write_csv(
            path,
            tuple(value for index, value in enumerate(columns) if index != removed),
            tuple(
                tuple(value for index, value in enumerate(row) if index != removed)
                for row in rows
            ),
        )

        with pytest.raises(ValueError, match="required fields"):
            DiagnosticBundle.load(copied)

    def test_load__rejects_duplicate_and_noncanonical_identities(
        self, tmp_path: Path
    ) -> None:
        copied = tmp_path / "analysis"
        _copy_tables(copied)
        path = copied / "truncation-consequences.csv"
        columns, rows = _read_csv(path)
        _write_csv(path, columns, (*rows, rows[0]))

        with pytest.raises(ValueError, match="has 2806 rows|duplicate identities"):
            DiagnosticBundle.load(copied)

        _write_csv(path, columns, tuple(reversed(rows)))
        with pytest.raises(ValueError, match="canonical key order"):
            DiagnosticBundle.load(copied)

    def test_catalog__uses_canonical_typed_serialization(self) -> None:
        catalog = DiagnosticBundle.load(RESULTS).catalog()
        round_trip = DiagnosticCatalog.from_json(catalog.to_json())

        assert round_trip == catalog
        assert len(catalog.entries) == 110
        hamiltonian = next(
            item
            for item in catalog.entries
            if item.quantity == "comparison_maximum_total_hamiltonian_error"
        )
        assert hamiltonian.category == "operator"
        assert hamiltonian.normalization == "Frobenius/(sqrt(2)*E_ref)"

    def test_typed_records__preserve_historical_csv_contracts(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)
        catalog = bundle.catalog()
        catalog_columns = (
            "quantity",
            "category",
            "aggregation",
            "unit",
            "normalization",
            "role",
        )
        assert _csv_projection(
            catalog_columns,
            tuple(entry.csv_row() for entry in catalog.entries),
        ) == (RESULTS / "diagnostic-catalog.csv").read_text(encoding="utf-8")

        decisions = bundle.sampled_range_decisions((1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12))
        decision_columns = (
            "parent_hopping_scale",
            "amplitude",
            "tolerance",
            "reference_band_first_passing_range",
            "comparison_band_first_passing_range",
            "reference_hamiltonian_first_passing_range",
            "comparison_hamiltonian_first_passing_range",
            "band_sampled_range_inflation",
            "hamiltonian_sampled_range_inflation",
        )
        decision_projection = _csv_projection(
            decision_columns,
            tuple(decision.csv_row() for decision in decisions.decisions),
        )
        assert tuple(decision_projection.splitlines()[0].split(",")) == decision_columns
        assert len(decision_projection.splitlines()) == 5 * 33 * 4 + 1

    def test_sampled_range_decisions__keeps_matrix_and_band_rules_separate(
        self,
    ) -> None:
        decisions = DiagnosticBundle.load(RESULTS).sampled_range_decisions(
            (1.0e-6, 1.0e-8)
        )
        round_trip = SampledRangeDecisions.from_json(decisions.to_json())

        assert round_trip == decisions
        assert len(decisions.decisions) == 5 * 33 * 2
        endpoint = tuple(
            item
            for item in decisions.decisions
            if item.parent_hopping_scale == 1.0
            and math.isclose(item.amplitude, math.pi / 4.0)
            and item.tolerance == 1.0e-8
        )
        assert len(endpoint) == 1
        assert endpoint[0].reference_band_first_passing_range == 4
        assert endpoint[0].comparison_band_first_passing_range == 10

    def test_truncation_refinement__keeps_final_dense_decisions_unchanged(
        self,
    ) -> None:
        table = DiagnosticBundle.load(RESULTS).table(
            DiagnosticTable.TRUNCATION_REFINEMENT
        )
        channels = (
            "reference_band_first_passing_range",
            "comparison_band_first_passing_range",
            "reference_hamiltonian_first_passing_range",
            "comparison_hamiltonian_first_passing_range",
        )
        coarse = tuple(
            row
            for row in table.rows
            if table.integer(row, "construction_mesh_size") == 256
        )
        fine = tuple(
            row
            for row in table.rows
            if table.integer(row, "construction_mesh_size") == 512
        )

        assert len(coarse) == len(fine) == 5 * 33
        assert tuple(
            tuple(table.text(row, channel) for channel in channels) for row in coarse
        ) == tuple(
            tuple(table.text(row, channel) for channel in channels) for row in fine
        )

    def test_plotters__consume_the_bundle_without_recalculation(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)
        error_figure = plot_hamiltonian_and_spectral_errors(bundle)
        frame_figure = plot_frame_and_sewing_diagnostics(bundle)
        range_figure = plot_sampled_range_decisions(bundle)

        assert len(error_figure.axes) == 4
        assert len(frame_figure.axes) == 4
        assert len(range_figure.axes) == 8
        plt.close(error_figure)
        plt.close(frame_figure)
        plt.close(range_figure)
