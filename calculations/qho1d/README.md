# QHO1D spatial-truncation calculation

This package composes the dimension-specific one-dimensional quantum harmonic
oscillator implementation in `ksdft2effmass.model_systems.qho1d`. It studies the
finite represented effect of replacing the real-line oscillator by a finite
homogeneous-Dirichlet interval and centered finite-difference grid.

No dimension-neutral `QHO` implementation, continuum proof, physical uncertainty
statement, semiconductor result, or scientific validation is claimed.

## Direct lifecycle

The maintained successor uses three explicit module-scope scripts:

```text
run_01_calculation.py → run_02_verification.py → run_03_render.py
```

From `python/`, execute them in order with the repository source selected explicitly:

```console
PYTHONPATH=$PWD/src uv run python ../calculations/qho1d/run_01_calculation.py
PYTHONPATH=$PWD/src uv run python ../calculations/qho1d/run_02_verification.py
PYTHONPATH=$PWD/src uv run python ../calculations/qho1d/run_03_render.py
```

The scripts contain no Workflow, `main()` function, argument parser, or JSON-authored
scientific input. They refuse to overwrite stage-owned artifacts. Reusable calculation,
verification, serialization, and visualization behavior belongs to the Python package.

The successor JSON boundary is the same shared boundary used by PIAB1D:

```text
to_json → to_dict → TypedJsonMappingSerializer.serialize
from_json → TypedJsonMappingDeserializer.deserialize → from_dict
```

Concrete records implement `_mapping` and `_from_mapping`. QHO1D has no custom JSON
array transport and no `.tolist()` serialization logic.

## Package structure

- `protocol.md` declares the finite scientific question, sweep, independent route, and
  claim boundary.
- `evidence-policy.md` distinguishes development output from sealed evidence.
- `inputs/README.md` explains the Python-authored configuration boundary.
- `run_01_calculation.py` writes one typed result and exact serialized configuration.
- `run_02_verification.py` reconstructs the result through independent formulas.
- `run_03_render.py` consumes only authenticated verification and publishes figures.
- `technical_report/` owns the maintained self-contained calculation report.
- `executions/` contains concrete unsealed or separately sealed execution directories.

## Mathematical comparison

For each declared box half-width, requested grid spacing, and retained dimension, the
calculation forms

\[
J^{\mathsf T}H_{b,h}J-D_K,
\]

where `J` is the sampled-Hermite Gram-orthonormalized injection, `H_{b,h}` is the finite
Dirichlet-grid Hamiltonian, and `D_K` is the direct diagonal number-state reference.
The direct reference avoids the highest-state defect introduced by products of already
truncated ladder matrices.

For an exactly isometric `J`,

\[
J^{\mathsf T}H_{b,h}J-D_K
=J^{\mathsf T}(H_{b,h}J-JD_K).
\]

This is a computable finite-dimensional a-posteriori relation, not a continuum
finite-box bound. The aggregate discrepancy currently combines finite-box closure,
boundary-adjacent rows, interior discretization, finite sampled-state Gram correction,
projection, and binary64 reconstruction.

## Historical development boundary

The predecessor files `input.json`, `dev_analysis.py`, `dev_verification.py`,
`dev_plots.py`, `analysis/development/`, and `development_report/` remain available for
their existing development and report provenance. They are not used by the direct
successor lifecycle. Removing them is a separate destructive action and is not part of
this additive migration.

The separately retained historical package under
`calculations/research-monograph/harmonic-oscillator/` remains an independent
historical locator; the direct successor does not rewrite its identities.
