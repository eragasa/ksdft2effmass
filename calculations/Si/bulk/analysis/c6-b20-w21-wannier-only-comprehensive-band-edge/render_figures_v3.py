from __future__ import annotations

import json
from pathlib import Path

import render_multiband as multiband
import render_results as results

ROOT = Path(__file__).resolve().parent
FIGURES = ROOT / "figures-v3"


def main() -> None:
    if FIGURES.exists():
        raise FileExistsError(f"refusing to overwrite {FIGURES}")
    FIGURES.mkdir()

    results.FIGURES = FIGURES
    result = results.mapping(
        json.loads((ROOT / "result.json").read_text(encoding="utf-8")), "result"
    )
    plot_data = results.mapping(
        json.loads((ROOT / "plot-data.json").read_text(encoding="utf-8")),
        "plot data",
    )
    results.render_gamma(result)
    results.render_dispersions(plot_data)
    results.render_valence_sensitivity(result)
    results.render_electron(result)
    results.render_high_symmetry(result)

    multiband.FIGURES = FIGURES
    multiband.main()


if __name__ == "__main__":
    main()
