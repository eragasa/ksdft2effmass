# QHO1D development report

This directory retains the TeX source, bibliography, report-local figure inputs,
and a compiled PDF snapshot. The report and figures are development outputs, not
sealed evidence, scientific validation, or a publication release.

From the repository root, regenerate and independently verify the development
result, render the report inputs, and build the PDF with:

```console
cd python
PYTHONPATH=$PWD/src uv run python ../calculations/qho1d/dev_analysis.py
PYTHONPATH=$PWD/src uv run python ../calculations/qho1d/dev_verification.py
PYTHONPATH=$PWD/src uv run python ../calculations/qho1d/dev_plots.py
cd ../calculations/qho1d
cp analysis/development/qho1d-*.png development_report/
cd development_report
latexmk -pdf -interaction=nonstopmode -halt-on-error development_report.tex
```

The retained report-local figures were rendered from the verified development
result with SHA-256
`1bc17c2911ede0d679af080442a7331a18972213f9ad464a4f6fb6937d2f961a`:

| Figure | SHA-256 |
|---|---|
| `qho1d-eigenstates.png` | `d016e16a6ecc2eea216a8e329347f1c878febb7839c096384e2009c5cb328ca7` |
| `qho1d-eigenstate-distortion.png` | `792b8a6b80806f62efd1b6f18562d7fa21d9b76792b15c97725e744076508a66` |
| `qho1d-diagnostics.png` | `5476634b34c30a67244a7f541484465d11bc748dbfafc311cf2c28a2346ed58a` |

The result JSON remains a replaceable development output beneath
`analysis/development/`; the committed input, calculation, verification, plotting,
report, and reusable source files are the reproducible source chain.
