# Controlled spin-space embedding exercise

## Status and scope

This directory contains a **calculated synthetic numerical-verification exercise** for Appendix I of the research monograph. It verifies explicit mappings among spinless, spin-degenerate, collinear, and spinor finite state spaces before later pristine--defect operator extraction.

The result is human-accepted within this bounded synthetic scope. It is not a Kohn--Sham calculation, an explicit spin--orbit model, a silicon impurity operator, scientific validation, uncertainty quantification, or evidence of transferability to phosphorus or boron. The retained result preserves its pre-extraction runner identity; newly authored results also bind the extracted implementation module.

## Retained artifacts

- `input.json`: authored finite matrices, represented conventions, rotations, and tolerance;
- `protocol.md`: state spaces, exact identities, comparison rules, and acceptance criteria;
- `run_experiment.py`: minimal typed CLI adapter;
- `spin_spaces_calculation/run_experiment.py`: immutable records, represented
  operators, compatibility and difference actions, serialization, and Workflow;
- `result.json`: represented operators, checks, structured stops, error separation, and provenance;
- `verify_result.py`: minimal typed CLI adapter;
- `spin_spaces_calculation/verify_result.py`: independent reconstruction and
  analytical verification ActionObject;
- `plot_result.py`: deterministic journal-style visualization;
- `summary.png`: operator, model-class, and covariance summary;
- `report.md`: self-contained methods-and-results mini-paper; and
- `SHA256SUMS`: SHA-256 identities for maintained artifacts.

## Reproduction

From `python/` using the resolved project environment:

```bash
uv run python \
  ../calculations/research-monograph/impurity-spin-spaces/run_experiment.py \
  --input ../calculations/research-monograph/impurity-spin-spaces/input.json \
  --output ../calculations/research-monograph/impurity-spin-spaces/result.json

uv run python \
  ../calculations/research-monograph/impurity-spin-spaces/verify_result.py \
  ../calculations/research-monograph/impurity-spin-spaces/result.json

uv run --extra notebooks python \
  ../calculations/research-monograph/impurity-spin-spaces/plot_result.py \
  ../calculations/research-monograph/impurity-spin-spaces/result.json \
  --output ../calculations/research-monograph/impurity-spin-spaces/summary.png
```

The largest represented matrix is $8\times8$. Runtime is expected to be seconds on a laptop, with one JSON result and one PNG figure as generated outputs.

## Calculated summary

The exact spin lift satisfies its two pullbacks and cross-spin zero condition. Its Frobenius norm agrees with $\sqrt{2}\|\Delta H_0\|_F$ to $1.11\times10^{-16}$. A raw block-order comparison has defect $5.60\times10^{-1}$, while the declared permutation removes it exactly. Five spin-frame rotations have unaligned defects between $4.01\times10^{-2}$ and $1.28\times10^{-1}$ but aligned defects below $1.77\times10^{-16}$.

The optimal spin-independent model exactly recovers the degenerate lift and leaves relative residuals of $0.408$ and $0.261$ for the planted collinear and spin-mixing terms. Incompatible spin dimension, block order, spin frame, or energy reference stops comparison instead of producing a nominal norm.

Exact values and bounded interpretation are in `report.md`.
