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

Concrete records implement `_mapping` and `_from_mapping`. Each maintained case is
serialized as four typed semantic sections: `representation`, `alignment`,
`hamiltonian_comparison`, and `residual`. QHO1D has no custom JSON array transport and
no `.tolist()` serialization logic. The earlier flat-case execution remains byte-exact
and is decoded through its explicitly retained layout.

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
  `direct-spatial-truncation-3x3x3-physkit-norms` is the maintained execution;
  `direct-spatial-truncation-3x3x3-sections` and
  `direct-spatial-truncation-3x3x3` remain prior byte-exact records.

## Mathematical comparison

For each declared box half-width, requested grid spacing, and retained dimension, the
calculation forms

\[
J^{\mathsf T}H_{b,h}J-D_K,
\]

where `J` is the sampled-Hermite Gram-orthonormalized injection, `H_{b,h}` is the finite
Dirichlet-grid Hamiltonian, and `D_K` is the direct diagonal number-state reference.
The direct reference avoids the highest-state defect introduced by products of already
truncated ladder matrices. Production Frobenius diagnostics use
`projectkoios.physkit.linalg.matrix.norm.FrobeniusMatrixNorm`; the independent verifier
retains a direct NumPy route.

For an exactly isometric `J`,

\[
J^{\mathsf T}H_{b,h}J-D_K
=J^{\mathsf T}(H_{b,h}J-JD_K).
\]

This is a computable finite-dimensional a-posteriori relation, not a continuum
finite-box bound. The aggregate discrepancy currently combines finite-box closure,
boundary-adjacent rows, interior discretization, finite sampled-state Gram correction,
projection, and binary64 reconstruction.

The reusable `Qho1dCrossGridAnalyzer` additionally compares adjacent coarse/fine
pulled-back Hamiltonians at fixed box and retained dimension. Because both pullbacks
act in the same ordered number-state coordinates, their difference is well-defined.
Its Frobenius norm is an adjacent-representation change diagnostic, not a continuum
error estimate or convergence rate.

## Removed predecessor

The JSON-authored development input, `dev_*` scripts, replaceable development-output
path, predecessor report, `model_systems.qho1d.study` package, and compatibility aliases
were removed after the direct migration was completed. They are recoverable from Git
commit `7e3331eb3addd8034cdf97cc2a65e64c4f74ac67`; their disposition and content
identities are recorded in
`docs/architecture/v3/ksdft2effmass/model_systems/qho1d/legacy-disposition.md`.

The absent historical locator
`calculations/research-monograph/harmonic-oscillator/` was not restored. New and
maintained work uses only the direct typed lifecycle documented above.
