# Analytical finite-rank oracle for the 1D defect benchmark

This directory retains a deterministic synthetic comparison between a finite-rank Bloch-resolvent oracle and an independently assembled site-space eigensolve.

## Evidence status

**Synthetic test data / software and numerical verification.** This package does not establish silicon behavior, an infinite-system or continuum limit, material validity, transferability, scientific validation, uncertainty quantification, or a public API. The retained result preserves its pre-extraction runner identity; newly authored results also bind the extracted implementation module.

## Contents

- `input.json` — frozen source identities, parent, rank-one parameters, special controls, and tolerances.
- `run_experiment.py` — minimal typed CLI adapter.
- `analytical_oracle_calculation/run_experiment.py` — direct Bloch-resolvent
  oracle, independent site-space comparison, serializers, and Workflow.
- `result.json` — retained rank-one sweep, threshold, no-state, degeneracy, and unequal-rank records.
- `verify_result.py` — minimal typed CLI adapter.
- `analytical_oracle_calculation/verify_result.py` — independent reconstruction
  ActionObject that imports no runner implementation.
- `plot_result.py` — deterministic summary renderer.
- `summary.png` — energy, binding, projector, and special-control diagnostics.
- `protocol.md` — finite-rank identity, root rule, comparison contract, and reproduction procedure.
- `report.md` — compact methods-and-results mini-paper.
- `SHA256SUMS` — package content identities.

## Core result

For the rank-one defect $V_g=-g|v\rangle\langle v|$, the oracle solves

$$
1-g\langle v|(H_0-EI)^{-1}|v\rangle=0
$$

using direct $2\times2$ Bloch-fiber resolvents rather than a full defect-Hamiltonian eigensolve. Across 20 attractive controls, the maximum energy discrepancy is $6.11\times10^{-16}E_G$ and the maximum projector defect is $6.14\times10^{-13}$.

## Reproduce

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-analytical-oracle/summary.png
```

Then run `sha256sum -c SHA256SUMS` from this directory.
