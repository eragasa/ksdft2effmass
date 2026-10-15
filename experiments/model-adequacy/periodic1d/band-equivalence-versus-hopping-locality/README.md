# Band Equivalence versus Hopping Locality

## Status

This is the publication-independent experiment home for

```text
ksdft2effmass.campaign.model-adequacy.periodic1d.band-equivalence-versus-hopping-locality
```

The earlier `v0` draft has been retired without assigning a maintained version. Its
64-point construction and 257-point staggered evaluation route is isolated under
[`regression/historical-64-257/`](regression/historical-64-257/) as a non-decisive
regression fixture. It does not define the scientific mesh, thresholds,
continuous-alignment method, or evidence contract for the redesigned experiment.

Initial source implementation now covers the smooth flat-parent band-equivalent
continuum

```math
U_a(q)=R(a\sin 2\pi q), \qquad 0\leq a\leq \pi/4.
```

It retains the conventional Bloch-band defect beside separate finite-mesh and analytic
correlation channels, exact continuous global real-rotation selection, operator
thresholds, a complete finite Fourier-block power inventory, non-onsite hopping weight,
Parseval and residual-decomposition defects, and independent reconstruction. In
particular, finite-mesh $\mu_{N,\max}$ and analytic $J_0(2a)$ are separate result fields;
the analytic comparator is never substituted into finite-$N$ evidence.

The current flat-parent data analysis is reported in
[`analysis/README.md`](analysis/README.md). It finds roundoff-level momentum refinement
changes but shows that the proposed amplitude ladder through $N_a=64$ is too coarse for
a $10^{-8}$ uniform piecewise-linear threshold curve. This is exploratory development
analysis, not retained evidence.

An initial typed non-flat four-state realization now uses the same smooth
$U_a(q)=R(a\sin 2\pi q)$ family with a dispersive parent and deterministic periodic
retained frame. It includes exact continuous harmonic selection, finite Fourier blocks,
Parseval evidence, nested momentum refinement, cached adaptive midpoint amplitude
refinement with disjoint quarter-point validation and an explicit unique-sample cap,
conservative `converged`/`unresolved` dispositions, and
independent reconstruction. Neighbor-overlap singular values are qualification gates,
not convergence observables; shared parent eigenvalues and spectral projectors provide
the frame-invariant refinement channels. The corrected $N=32$--512 momentum study is
`converged`. Primary numerical claims are pointwise at the prospectively declared
amplitudes; plotted connections are guides to the eye. The separate capped
amplitude-interpolation supplement remains `unresolved`.

A bounded parent homotopy scales every non-onsite parent block by
$0\leq\rho\leq1$, separating parent dispersion and pre-existing locality from the
rotation amplitude $a$. The exploratory five-scale, 33-amplitude study is reported in
[`analysis/README.md`](analysis/README.md). It is a finite sampling of a continuous
model family, not retained evidence. The resulting scientific-story figure compares the
normalized residual with comparison-minus-reference hopping weight: the exact flat
identity holds at $\rho=0$ and deforms systematically as parent hopping increases. The
non-flat realization has no $J_0(2a)$ comparator and does not assume the flat-parent
residual--tail identity.

The existing finite-angle four-state implementation remains available only through the
explicit `band_equivalence_hopping_locality.regression` namespace. Active definitions,
results, calculations, and verification contain no finite-angle inventory. Strict
non-flat serialization and schemas have not been defined because its numerical contract
is not frozen. No maintained version, retained run, evidence package, or publication
evidence has been created.

Historical `M3` and conference labels are searchable aliases only; they are not the
maintained experiment identity. Existing evidence under `calculations/` remains
unchanged.

## Numerical ownership

The exact dependency

```text
projectkoios-optimization@cf551409872a621b4e47d2236ac4ffdc12c187c0
projectkoios-physkit@07b2a1ee3ccd07926e90f43b4d1046efccc5ad8c
```

provide the active owner capabilities. Optimization owns exact maximization of a
unit-free periodic harmonic and the full-rank complex-unitary pairwise Procrustes solve;
rank-deficient results expose no invented null-space completion. PhysKit owns immutable
matrix-valued hopping records and raw unit-aware block Frobenius powers. Its ordinary
lattice Hermiticity and truncation semantics do not replace KSD's finite-cyclic Nyquist
checks. Optimization's affine-residual, rectangle, support, and finite-selection
capabilities remain consumed only by the isolated historical regression implementation.

The smooth-continuum calculations construct their physics-semantic second-harmonic
coefficients locally and call the generic Optimization harmonic owner directly. The
non-flat producer uses the Numerics finite-Fourier evaluator both to construct its
discrete blocks under the shifted-mesh convention and to check nodal reconstruction. It
calls Optimization directly for each unique neighbor-frame alignment and PhysKit
directly for block powers. The independent verifier reconstructs the harmonic maximum as
$b_0+\sqrt{c^2+d^2}$ and independently repeats the SVD/frame and raw-power calculations.
No finite angle inventory enters either active definition or result. Neither owner
repository provides a thin KSD-specific pass-through adapter. No immutable experiment
version or retained execution provenance is attached to these live-development pins.

`SmoothBlochContinuumVerifier` independently reconstructs each finite-mesh harmonic,
continuous maximizing angle, threshold, Fourier-block power, and analytic comparator.
`SmoothBlochContinuumConvergenceVerifier` additionally reconstructs every adjacent mesh
comparison and the final `converged` or `unresolved` disposition without calling the
producer. Every metric must remain below its threshold after adding the declared
verification absolute tolerance as a conservative numerical margin. Passing establishes
bounded analytic-family software and mesh-convergence behavior only, not material
validation or general uncertainty quantification. `SmoothFourStateVerifier` provides
independent reconstruction for the non-flat realization; its current exploratory
convergence result is `unresolved`, so no non-flat scientific acceptance claim follows.

## Development checks

```console
cd experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality
uv lock --check
../../../../python/.venv/bin/pytest -q
../../../../python/.venv/bin/ruff check .
../../../../python/.venv/bin/ruff format --check .
../../../../python/.venv/bin/mypy analysis src tests
```
