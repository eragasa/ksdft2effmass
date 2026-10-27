"""Software verification for packaged pandas diagnostics and plotting access."""

from __future__ import annotations

import math
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore[import-untyped]
import pytest
from workflow.analysis import (
    DiagnosticBundle,
    DiagnosticTable,
)
from workflow.analysis_plot import (
    plot_frame_and_sewing_diagnostics,
    plot_hamiltonian_and_spectral_errors,
    plot_sampled_range_decisions,
)

pytestmark = pytest.mark.software_verification

RESULTS = (
    Path(__file__).resolve().parents[1] / "simulations" / "development" / "results"
)


class TestDiagnosticBundle:
    """Establish complete loading, immutable access, metadata, and plot consumption."""

    def test_load__validates_complete_experiment_tables(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)

        assert len(bundle.names) == 14
        truncation = bundle.table(DiagnosticTable.TRUNCATION_CONSEQUENCES)
        refinement = bundle.table(DiagnosticTable.TRUNCATION_REFINEMENT)
        assert len(truncation) == 2805
        assert len(refinement) == 495
        assert tuple(truncation.columns[:3]) == (
            "parent_hopping_scale",
            "amplitude",
            "maximum_range",
        )
        assert "comparison_maximum_total_hamiltonian_error" in truncation
        assert "comparison_maximum_total_band_error" in truncation

    def test_load__rejects_a_missing_diagnostic_column(self, tmp_path: Path) -> None:
        copied = tmp_path / "analysis"
        copied.mkdir()
        for source in RESULTS.glob("*.csv"):
            shutil.copy2(source, copied / source.name)
        path = copied / "parent-family-summary.csv"
        frame = pd.read_csv(path).drop(columns=["closure_holonomy_phase_1"])
        frame.to_csv(path, index=False)

        with pytest.raises(ValueError, match="declared schema"):
            DiagnosticBundle.load(copied)

    def test_load__rejects_duplicate_and_noncanonical_identities(
        self, tmp_path: Path
    ) -> None:
        copied = tmp_path / "analysis"
        copied.mkdir()
        for source in RESULTS.glob("*.csv"):
            shutil.copy2(source, copied / source.name)
        path = copied / "truncation-consequences.csv"
        frame = pd.read_csv(path)
        frame = pd.concat((frame, frame.iloc[[0]]), ignore_index=True)
        frame.to_csv(path, index=False)

        with pytest.raises(ValueError, match="duplicate identities"):
            DiagnosticBundle.load(copied)

        frame = frame.iloc[:-1].iloc[::-1]
        frame.to_csv(path, index=False)
        with pytest.raises(ValueError, match="canonical key order"):
            DiagnosticBundle.load(copied)

    def test_table__returns_a_defensive_copy(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)
        first = bundle.table(DiagnosticTable.PARENT_FAMILY_SUMMARY)
        original = float(first.loc[0, "minimum_sampled_external_gap"])
        first.loc[0, "minimum_sampled_external_gap"] = -1.0

        second = bundle.table(DiagnosticTable.PARENT_FAMILY_SUMMARY)
        assert float(second.loc[0, "minimum_sampled_external_gap"]) == original

    def test_long_form__labels_every_numeric_diagnostic(self) -> None:
        bundle = DiagnosticBundle.load(RESULTS)
        long_form = bundle.long_form(numeric_only=True)

        required = {
            "source_table",
            "quantity",
            "value",
            "category",
            "aggregation",
            "unit",
            "normalization",
            "role",
        }
        assert required <= set(long_form.columns)
        hamiltonian = long_form.loc[
            long_form["quantity"] == "comparison_maximum_total_hamiltonian_error"
        ]
        assert not hamiltonian.empty
        assert set(hamiltonian["category"]) == {"operator"}
        assert set(hamiltonian["normalization"]) == {"Frobenius/(sqrt(2)*E_ref)"}

    def test_sampled_range_decisions__keeps_matrix_and_band_rules_separate(
        self,
    ) -> None:
        bundle = DiagnosticBundle.load(RESULTS)
        decisions = bundle.sampled_range_decisions((1.0e-6, 1.0e-8))

        assert len(decisions) == 5 * 33 * 2
        assert "band_sampled_range_inflation" in decisions
        assert "hamiltonian_sampled_range_inflation" in decisions
        endpoint = decisions.loc[
            (decisions["parent_hopping_scale"] == 1.0)
            & np.isclose(decisions["amplitude"], math.pi / 4.0)
            & (decisions["tolerance"] == 1.0e-8)
        ]
        assert len(endpoint) == 1
        assert int(endpoint.iloc[0]["reference_band_first_passing_range"]) == 4
        assert int(endpoint.iloc[0]["comparison_band_first_passing_range"]) == 10

    def test_truncation_refinement__keeps_final_dense_decisions_unchanged(
        self,
    ) -> None:
        bundle = DiagnosticBundle.load(RESULTS)
        refinement = bundle.table(DiagnosticTable.TRUNCATION_REFINEMENT)
        channels = (
            "reference_band_first_passing_range",
            "comparison_band_first_passing_range",
            "reference_hamiltonian_first_passing_range",
            "comparison_hamiltonian_first_passing_range",
        )
        coarse = refinement.loc[
            refinement["construction_mesh_size"] == 256
        ].reset_index(drop=True)
        fine = refinement.loc[refinement["construction_mesh_size"] == 512].reset_index(
            drop=True
        )

        assert len(coarse) == len(fine) == 5 * 33
        assert np.array_equal(
            coarse.loc[:, channels].to_numpy(),
            fine.loc[:, channels].to_numpy(),
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
