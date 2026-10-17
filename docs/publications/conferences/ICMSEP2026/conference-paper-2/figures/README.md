# Paper 2 figures

Publication-local rendered figures belong in this directory. Generated PDF and PNG
files are ignored and must not be committed as development evidence.

Each rendered figure has a same-stem Python entry point under [`src/`](src/). For
example:

```text
figures/rhombic-2d-strain-scan.pdf
figures/src/rhombic-2d-strain-scan.py
```

Run a script from the repository Python environment to regenerate its owning experiment
diagnostic and stage the publication copy:

```bash
python/.venv/bin/python \
  docs/publications/conferences/ICMSEP2026/conference-paper-2/figures/src/rhombic-2d-strain-scan.py
```

Pass `--reuse-existing` only to restage an already generated experiment diagnostic
without recalculating it. The shell--scale entry points stage one four-case principal
comparison and eight independently rendered case plots generated from the same typed
calculator and supplied-axis renderer; they do not crop a composite figure. The scripts
do not transfer scientific ownership to the publication tree: family definitions,
calculations, tolerances, and evidence remain with their publication-independent
experiment roots.
