# M3 post-hoc threshold sensitivity

This package reconstructs the exact M3 admissible-set distance while varying the
operator threshold at fixed spectral threshold `0.03`.

The analysis is explicitly post hoc. It consumes the sealed M3 `result.json`; it does
not modify that package, refit a model, use withheld values, or execute an external
calculator.

Run locally from the repository root:

```console
python/.venv/bin/python calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/analyze.py
python/.venv/bin/python calculations/ICMSEP2026/conference/paper_1/constrained-admissible-sets-threshold-sensitivity/verify_result.py
```

Principal outputs are:

- `operator-threshold-sensitivity.png`;
- `figure-data.csv`;
- `result.json`;
- `verification.json`; and
- `report.md`.

`verification-amendment.json` records post-hoc hardening of the source-manifest
correlation and decisive quadratic-premise checks after adversarial review. The
scientific controls and numerical results did not change.

The diagram is an exploratory sensitivity characterization, not a prospective result,
physical threshold calibration, uncertainty analysis, or material validation.
