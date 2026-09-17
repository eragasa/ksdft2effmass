# Matched one-dimensional pristine–defect extraction

This directory retains the bounded synthetic numerical-verification exercise used
in Appendix I of the research monograph. It constructs exactly matched pristine
and defect supercells from the accepted periodic-1D represented parents, applies
known coordinate and energy-reference perturbations, recovers planted impurity
operators, and keeps representation, finite-size, model-class, spectral, and
wavefunction diagnostics separate.

The retained evidence is **synthetic test data**. It is not a silicon or dopant
calculation, scientific validation, transferability study, or uncertainty
quantification.

## Contents

- `input.json` — frozen version-1 controls and exact parent-artifact identities.
- `run_experiment.py` — deterministic calculation runner.
- `result.json` — canonical retained numerical result.
- `verify_result.py` — independent reconstruction and verification.
- `plot_result.py` — deterministic summary-figure renderer.
- `summary.png` — six-panel diagnostic summary.
- `protocol.md` — mathematical definitions, stopping rules, and reproduction.
- `report.md` — self-contained mini-paper.
- `SHA256SUMS` — identities of retained calculation artifacts.

## Reproduction

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d/result.json
uv run python ../calculations/research-monograph/impurity-defect-1d/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d/result.json
uv run python ../calculations/research-monograph/impurity-defect-1d/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d/summary.png
```

Verify retained identities from this directory:

```bash
shasum -a 256 -c SHA256SUMS
```
