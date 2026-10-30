# Periodic 2-D nonorthogonal rank-two band equivalence and locality

## Report status and reading rule

This report describes a bounded synthetic two-dimensional comparison across square and
triangular Bravais metrics and a honeycomb-basis control. The nominal direct
`calculate -> independently verify -> authenticated render` lifecycle is installed, but
**no direct execution is retained** in this calculation owner.

The only numerical summary currently available is a replaceable development record. It
is not admitted direct-lifecycle evidence, graphene validation, sealed evidence, or
publication support.

The lifecycle was inspected at KSD revision
`a5fc0e99b8e4a91dfd3006692255b1acb522a03d` (tree
`f5c9479ee7fc9d14f185ced0ad2df31029e7da76`). This revision is a source identity, not a
scientific endorsement.

## Scientific question

The study asks whether gauge-induced Fourier nonlocality and finite support requirements
can be compared consistently when the direct-lattice basis is nonorthogonal and when a
basis offset is present. It separates three named synthetic cases:

1. `matched-square-bravais-control`;
2. `triangular-bravais-control`; and
3. `graphene-inspired-honeycomb`.

The third case is a connectivity and basis-offset control. It is not a carbon or
graphene Hamiltonian and carries no graphene material claim.

## Frozen nominal request

If the direct producer is run, its checked-in request fixes:

| Item | Nominal value |
|---|---|
| Dimension / retained rank | 2 / 2 |
| Square bonds | `(1,0)`, `(0,1)` |
| Triangular bonds | `(1,0)`, `(0,1)`, `(1,-1)` |
| Honeycomb basis offsets | `(0,0)` and `(1/3,1/3)` in reduced coordinates |
| Gauge normalization | bond RMS |
| Construction mesh | `16 x 16` tensor Monkhorst--Pack mesh |
| Evaluation mesh | disjoint shifted `33 x 33` mesh, shift `1/3` |
| Parent scales | `0`, `1` |
| Amplitudes | `0`, half maximum, maximum; maximum `pi/(4 sqrt(6))` |
| Band tolerances | `1e-3`, `1e-5` |
| Shell cap | complete metric shells through index `21` |
| Model | synthetic four-state locality development model v1 |

These values define a prospective direct request, not a completed execution. No result
or verification hash may be inferred from the checked-in script.

## Metric-complete method

The calculation uses reduced reciprocal coordinates but orders Fourier support through
the physical direct-lattice metric. A complete shell is the full set of integer
translations at a common metric radius; it must not be replaced by a coordinate box or
by selectively chosen vectors. The basis-distance and metric-covariance diagnostics are
kept explicit so that square and triangular cases are not compared under an accidental
orthogonal-coordinate norm.

For each case the method records parent and retained-subspace qualification, graph-frame
closure, covariant and restricted alignment, exact mesh-origin-aware Fourier conversion,
twisted-Nyquist and ordinary Hermiticity checks, interpolation error, complete-shell
truncation error, total matrix and spectral error, Parseval checks, and sampled
first-passing decisions.

Interpolation, truncation, and total errors are separate channels. A first-passing shell
exists only when every mandatory finite criterion passes at the same stored case,
parent scale, amplitude, tolerance, and support inventory. Unresolved rows remain
unresolved at the frozen cap.

## Analytic flat-parent controls

At parent scale `rho = 0`, the protocol fixes the constant lower-two-eigenvector frame
and defines two distinct continuum comparators.

- The matched square control factorizes as `c_square(g) = J_0(2g)^2`.
- The triangular control is the zero-mode constrained series
  `sum_l (-1)^l J_l(x)^3`, with `x = 2g sqrt(2/3)`.

The triangular series requires a declared symmetric truncation, a reviewed tail bound,
and independent high-accuracy torus quadrature. None of those obligations is satisfied
merely by having a finite sampled calculation. The analytic comparators never replace
the finite-mesh correlation stored by a future direct execution.

## Current numerical status

The historical bounded development run used the nominal `16/33` meshes, parent scales
`0` and `1`, the three nominal amplitudes, and complete metric shells through index
`21`. Its development summary reported `passes: true` and a maximum stored identity
defect of about `3.5e-15`. Some strict sampled decisions remained unresolved at the
shell cap, and no threshold, cap, or model was changed in response.

Those outputs were produced by a former custom aggregation workflow. The workflow and
duplicate schemas have been removed, and the canonical JSON outputs are intentionally
excluded. Historical summaries or SHA-256 references do not establish admission by the
current typed lifecycle.

Because no `executions/direct-triangular-honeycomb-rank2-n16/` directory is retained,
this report presents no direct result table, no direct verification outcome, no render
authentication, and no evidence seal.

## Formal theorem crosswalk

Project Koios Formal was inspected at merge commit
`9f27941db0472683fd3971c462301ab6e0a3d046` (tree
`cc5030f6227b0c2acfa7cfd48dd9a2d1fe038d5e`). The source-neutral proved declarations
`BG-FOURIER-THM-129`, `BG-FOURIER-THM-130`, and `BG-FOURIER-THM-131` establish the
normalized one-circle `J_0` identity, its finite-product power law, and the exact `Fin 2`
square. After the protocol's algebraic amplitude substitution, this is the proposition
shape needed by the matched square control.

That crosswalk does not prove KSD's external phase, coordinate, measure, quadrature, or
runtime binding. Formal currently has no nonzero-order Jacobi--Anger or triangular
triple-Bessel theorem covering the triangular comparator, and it does not certify a
series truncation or tail bound here. The checked runtime-certificate count is zero.

The exact Formal propositions use the period-one coordinate `sin(2 pi x)`, positive
phase, standard Haar probability measure, and a carrier of the form
`Fin 2 -> UnitAddCircle`. Their reported foundational dependencies are `propext`,
`Classical.choice`, and `Quot.sound`; this should not be paraphrased as axiom-free.

## Evidence lifecycle

A future direct execution would have to preserve the entire owner-controlled chain:

`typed configuration -> typed result -> independent finite verification -> authenticated render`

The producer refuses to overwrite an existing execution. The verifier must bind the
exact configuration and result hashes and independently reproduce its declared finite
comparisons. Rendering may begin only from a passing verification record. Even then the
execution remains **CALCULATED RESULT — UNSEALED** unless a separate owner-controlled
sealing contract and authorization are completed.

## Limitations and nonclaims

This report does **not** establish:

- a retained direct result or passing direct verification record;
- graphene physics, carbon parameters, material validation, or experimental agreement;
- mesh, shell, series-tail, quadrature, or finite-to-continuum convergence;
- a certified triangular Jacobi--Anger evaluation;
- correctness of floating-point, eigensolver, serialization, or plotting machinery;
- a Lean-checked KSD runtime proposition;
- sealed evidence, publication acceptance, or novelty.

## Ownership and reproduction

The calculation owner is
`calculations/periodic2d/rank2/nonorthogonal/band-equivalence-locality/`. The governing
protocol remains
`experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/experimental-protocol.tex`.
The direct entry points are `run_01_calculation.py`, `run_02_verification.py`, and
`run_03_render.py`.

Development and refinement runners remain replaceable diagnostic surfaces outside the
nominal direct lifecycle. Running any of them would create a new provenance event; it
would not convert the historical development summary into retained or sealed evidence.
