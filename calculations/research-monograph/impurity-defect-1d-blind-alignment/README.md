# Impurity defect-1D blind alignment

This directory retains the deterministic synthetic calculation package for the blind-alignment follow-on to the accepted known-map one-dimensional defect benchmark.

## Evidence status

**Human-accepted synthetic test data / software and numerical verification within this bounded exercise.** The package does not report a silicon calculation, scientific validation, transferability, uncertainty quantification, production Wannierization, or a public API. The retained result preserves its pre-extraction runner identity; newly authored results also bind the extracted implementation module.

## Contents

- `input.json` — frozen source identities, inference policy, nominal cases, noise sweep, gauge-equivalent case, and stopping controls.
- `run_experiment.py` — minimal typed CLI adapter.
- `blind_alignment_calculation/run_experiment.py` — typed construction,
  inference, post hoc oracle evaluation, serialization, and Workflow.
- `result.json` — retained numerical results and provenance.
- `verify_result.py` — minimal typed CLI adapter.
- `blind_alignment_calculation/verify_result.py` — independent reconstruction
  ActionObject that imports no runner implementation.
- `plot_result.py` — summary-figure renderer.
- `summary.png` — map, extraction, gauge-equivalence, and stopping summary.
- `diagnostics.png` — conditioning, principal-angle, energy-anchor, rank, and spin debugging summary.
- `protocol.md` — complete observation contract, inference rule, equivalence rule, stopping policy, metrics, and reproduction commands.
- `report.md` — compact mini-paper.
- `SHA256SUMS` — content-identity catalog for the package.

## Core information boundary

The inference action receives the two represented Hamiltonians, an anchor cross-covariance, retained-subspace overlap information, an exterior energy anchor, spin labels, and a partial-alignment permission flag. It does not receive the authored hidden map, scalar energy shift, planted defect, or oracle errors. Those values are used only after inference to evaluate recovery.

## Reproduce

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-blind-alignment/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-blind-alignment/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-blind-alignment/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-blind-alignment/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-blind-alignment/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-blind-alignment/summary.png \
  --diagnostics-output ../calculations/research-monograph/impurity-defect-1d-blind-alignment/diagnostics.png
```

Then, from this directory:

```bash
sha256sum -c SHA256SUMS
```

See `protocol.md` before interpreting any metric.
