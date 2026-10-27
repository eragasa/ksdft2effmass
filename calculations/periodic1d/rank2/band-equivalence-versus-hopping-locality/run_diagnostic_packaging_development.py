"""Package every maintained diagnostic table and render overview figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from workflow.analysis import DiagnosticBundle
from workflow.analysis_plot import (
    plot_frame_and_sewing_diagnostics,
    plot_hamiltonian_and_spectral_errors,
    plot_sampled_range_decisions,
    save_figure,
)

CALCULATION = Path(__file__).resolve().parent
RESULTS = CALCULATION / "simulations" / "development" / "results"
FIGURES = CALCULATION / "analysis" / "development" / "figures"


def main() -> None:
    """Validate all sources, write tidy diagnostics, and render overview figures."""
    bundle = DiagnosticBundle.load(RESULTS)
    long_form = bundle.long_form()
    catalog = (
        long_form.loc[
            :,
            [
                "quantity",
                "category",
                "aggregation",
                "unit",
                "normalization",
                "role",
            ],
        ]
        .drop_duplicates()
        .sort_values(["category", "quantity"], kind="mergesort", ignore_index=True)
    )
    catalog.to_csv(RESULTS / "diagnostic-catalog.csv", index=False)
    decisions = bundle.sampled_range_decisions((1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12))
    decisions.to_csv(RESULTS / "sampled-range-decisions.csv", index=False)

    error_figure = plot_hamiltonian_and_spectral_errors(bundle)
    save_figure(error_figure, FIGURES / "hamiltonian-spectral-diagnostics")
    plt.close(error_figure)

    frame_figure = plot_frame_and_sewing_diagnostics(bundle)
    save_figure(frame_figure, FIGURES / "frame-sewing-diagnostics")
    plt.close(frame_figure)

    range_figure = plot_sampled_range_decisions(bundle)
    save_figure(range_figure, FIGURES / "sampled-range-decision-map")
    plt.close(range_figure)

    print(f"tables={len(bundle.names)}")
    print(f"long_rows={len(long_form)}")
    print(f"catalog_rows={len(catalog)}")
    print(f"decision_rows={len(decisions)}")


if __name__ == "__main__":
    main()
