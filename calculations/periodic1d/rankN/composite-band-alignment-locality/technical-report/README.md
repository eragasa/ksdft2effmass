# Technical report

[`technical_report.tex`](technical_report.tex) is the calculation-facing development
report. Its nine numerical figures are replaceable producer-only snapshots and are
visibly labeled development/unverified; they are not retained scientific evidence.
Calculate once, admit exact cache integrity once, and then regenerate figures repeatedly
from the calculation root with:

```bash
python run_01_calculation.py
python run_02_verification.py
python run_03_render.py
```

Only the first command performs the scientific calculation. Cache admission establishes
canonical-byte and inventory integrity, not independent scientific verification.

Build outside the source tree with:

```bash
mkdir -p /tmp/ksd-higher-rank-d1-report
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/ksd-higher-rank-d1-report technical_report.tex
```

The selected compiled `technical_report.pdf` is retained as a review snapshot. It is
not retained numerical evidence, scientific validation, or a publication; LaTeX
auxiliary products remain untracked.
