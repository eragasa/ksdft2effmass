# Technical report

[`technical_report.tex`](technical_report.tex) is the calculation-facing technical
report. Its nine numerical figures are calculated, integrity-admitted report snapshots
visibly labeled **CALCULATED RESULT — UNSEALED**. They are scientifically reviewable,
but remain unsealed and do not automatically confer publication acceptance. Calculate
once, admit exact cache integrity once, and then regenerate figures repeatedly from the
calculation root with:

```bash
python run_01_calculation.py
python run_02_verification.py
python run_03_render.py
```

Only the first command performs the scientific calculation. Cache admission establishes
canonical-byte and inventory integrity, not scientific validity or independent
scientific verification.

Build outside the source tree with:

```bash
mkdir -p /tmp/ksd-higher-rank-d1-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-higher-rank-d1-report technical_report.tex
```

The selected compiled `technical_report.pdf` is retained as an unsealed review snapshot.
It does not itself establish scientific validation, publication acceptance, or release;
LaTeX auxiliary products remain untracked.
