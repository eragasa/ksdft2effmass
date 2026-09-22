# Independent-route one-dimensional defect extraction

This directory retains a deterministic synthetic comparison between direct real-space and independently implemented Bloch-fiber defect-extraction routes.

## Evidence status

**Synthetic test data / software and numerical verification.** This package does not establish silicon behavior, material validity, continuum convergence, transferability, scientific validation, uncertainty quantification, or a public API. The retained result preserves its pre-extraction runner identity; newly authored results also bind the extracted implementation module.

## Contents

- `input.json` — frozen source identities, represented-space contract, controls, adversarial changes, and tolerances.
- `run_experiment.py` — minimal typed CLI adapter.
- `independent_route_calculation/run_experiment.py` — separate real-space and
  Bloch-fiber implementations, comparison actions, serializers, and Workflow.
- `result.json` — retained nominal and adversarial numerical records.
- `verify_result.py` — minimal typed CLI adapter.
- `independent_route_calculation/verify_result.py` — independent reconstruction
  ActionObject that imports no runner implementation.
- `plot_result.py` — deterministic summary renderer.
- `summary.png` — operator, observable, error-ledger, and adversarial summary.
- `protocol.md` — mathematical routes, commutativity rule, stopping policy, and reproduction procedure.
- `report.md` — compact methods-and-results mini-paper.
- `SHA256SUMS` — package content identities.

## Core result

For all seven accepted null, local, nonlocal, collinear, and spin-mixing controls,

$$
F^\dagger V^{(A)}F=V^{(B)}
$$

within the frozen $10^{-11}$ tolerance. Changed parent truncation is retained as explicit noncommutativity, while changed fiber domain, quadrature weights, and alignment map stop before nominal extraction. All four are paired with declared common-parent, common-domain, dual-map/induced-metric, and relative-unitary reconciliation controls. The reconciled route defects remain below $6.83\times10^{-15}E_G$; the original noncommutativity and stops remain guards against silent coercion.

## Reproduce

From `python/`:

```bash
uv run python ../calculations/research-monograph/impurity-defect-1d-independent-route/run_experiment.py \
  --input ../calculations/research-monograph/impurity-defect-1d-independent-route/input.json \
  --output ../calculations/research-monograph/impurity-defect-1d-independent-route/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-independent-route/verify_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-independent-route/result.json

uv run python ../calculations/research-monograph/impurity-defect-1d-independent-route/plot_result.py \
  --result ../calculations/research-monograph/impurity-defect-1d-independent-route/result.json \
  --output ../calculations/research-monograph/impurity-defect-1d-independent-route/summary.png
```

Then run `sha256sum -c SHA256SUMS` from this directory.
