"""Package maintained diagnostics through typed records and render overview figures."""

from __future__ import annotations

import csv
from collections.abc import Iterable, Mapping
from pathlib import Path

import matplotlib.pyplot as plt
from development_diagnostic_plots import (
    plot_frame_and_sewing_diagnostics,
    plot_hamiltonian_and_spectral_errors,
    plot_sampled_range_decisions,
    save_figure,
)
from development_diagnostics import (
    DiagnosticBundle,
    DiagnosticCatalog,
    SampledRangeDecisions,
)

CALCULATION = Path(__file__).resolve().parent
RESULTS = CALCULATION / "simulations" / "development" / "results"
FIGURES = CALCULATION / "analysis" / "development" / "figures"


def _write_csv(
    path: Path,
    fieldnames: tuple[str, ...],
    rows: Iterable[Mapping[str, str]],
) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def main() -> None:
    """Validate all sources, write typed diagnostics, and render overview figures."""
    bundle = DiagnosticBundle.load(RESULTS)
    catalog = bundle.catalog()
    catalog = DiagnosticCatalog.from_json(catalog.to_json())
    _write_csv(
        RESULTS / "diagnostic-catalog.csv",
        ("quantity", "category", "aggregation", "unit", "normalization", "role"),
        (entry.csv_row() for entry in catalog.entries),
    )

    decisions = bundle.sampled_range_decisions((1.0e-6, 1.0e-8, 1.0e-10, 1.0e-12))
    decisions = SampledRangeDecisions.from_json(decisions.to_json())
    _write_csv(
        RESULTS / "sampled-range-decisions.csv",
        (
            "parent_hopping_scale",
            "amplitude",
            "tolerance",
            "reference_band_first_passing_range",
            "comparison_band_first_passing_range",
            "reference_hamiltonian_first_passing_range",
            "comparison_hamiltonian_first_passing_range",
            "band_sampled_range_inflation",
            "hamiltonian_sampled_range_inflation",
        ),
        (decision.csv_row() for decision in decisions.decisions),
    )

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
    print(f"long_rows={bundle.long_form_row_count}")
    print(f"catalog_rows={len(catalog.entries)}")
    print(f"decision_rows={len(decisions.decisions)}")


if __name__ == "__main__":
    main()
