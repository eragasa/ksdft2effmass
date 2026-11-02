# Periodic 3-D nonorthogonal rank-two band equivalence and locality

## Report status and reading rule

This report describes a bounded synthetic three-dimensional comparison across a matched
simple-cubic control, an FCC Bravais control, and a diamond-basis connectivity control.
The calculation owner provides one nominal calculation action with independent typed
verification, two bounded refinement actions, and one replaceable analysis-rendering
action. **No execution is retained**.

The available numerical summary is a replaceable development record. It is not retained
execution evidence, silicon validation, a convergence result, or sealed evidence.

The action set was inspected at KSD revision
`a5fc0e99b8e4a91dfd3006692255b1acb522a03d` (tree
`f5c9479ee7fc9d14f185ced0ad2df31029e7da76`). This is an immutable source identity,
not a validity or publication claim.

## Scientific question

The study asks how gauge-induced Fourier nonlocality should be compared in three
dimensions when shell support is defined by a nonorthogonal metric and when basis
offsets are present. It separates three named synthetic cases:

1. `matched-simple-cubic-bravais-control`;
2. `fcc-bravais-control`; and
3. `silicon-inspired-diamond`.

The third case uses synthetic diamond connectivity and a two-site basis offset. It is not
an `sp3s*` model, a valley model, an effective-mass model, a density-functional result,
or a silicon material calculation.

## Frozen nominal request

If executed, the nominal calculation action fixes:

| Item | Nominal value |
|---|---|
| Dimension / retained rank | 3 / 2 |
| Simple-cubic positive bonds | three primitive coordinate bonds |
| FCC positive bonds | six stored primitive-coordinate bonds |
| Diamond basis offsets | `(0,0,0)` and `(1/4,1/4,1/4)` |
| Gauge normalization | bond RMS |
| Shell metric scale | `2` |
| Construction mesh | `8 x 8 x 8` tensor Monkhorst--Pack mesh |
| Evaluation mesh | disjoint shifted `17 x 17 x 17` mesh, shift `1/3` |
| Parent scales | `0`, `1` |
| Amplitudes | `0`, half maximum, maximum; maximum `pi/(4 sqrt(12))` |
| Band tolerances | `1e-3`, `1e-5` |
| Shell cap | complete FCC metric shells through index `7` |
| Model | synthetic four-state locality development model v1 |

These values define a nominal request. They do not imply that a calculation ran or that
a retained verification or render record exists.

## Metric-complete and resource-bounded method

The calculation works in reduced reciprocal coordinates but orders translation support
by the physical direct-lattice metric. Every shell must include all integer translations
at the same metric radius. This prevents an orthogonal-coordinate box or a selected set
of visually convenient FCC vectors from masquerading as a complete locality cutoff.

The producer is designed to avoid a dense global Hamiltonian. For each case it records
parent and retained-subspace qualification, graph-frame closure, covariant and restricted
alignment, mesh-origin-aware three-dimensional Fourier conversion, twisted-Nyquist and
ordinary Hermiticity checks, interpolation and complete-shell truncation errors, total
matrix and spectral errors, Parseval, basis-distance and metric-covariance diagnostics,
resource checks, and sampled first-passing decisions.

All mandatory channels must refer to the same stored case, parent scale, amplitude,
tolerance, alignment, sign convention, and shell inventory. Interpolation, truncation,
and total errors are kept separate. An unresolved row remains unresolved at the frozen
cap.

## Analytic flat-parent controls

At parent scale `rho = 0`, the protocol uses two distinct continuum controls.

- For the matched simple-cubic case,
  `c_sc(g) = J_0(2g sqrt(2/3))^3`. This is the orthogonal
  `J_0(2a/3)^3` law after the protocol substitution `a = g sqrt(6)`.
- For FCC, the comparator is a constrained triple sum of six Bessel factors with
  argument `2g/sqrt(3)`.

The FCC producer obligation is stronger than evaluating an ordinary finite sum: it
requires a declared symmetric summation domain, a reviewed tail bound, and independent
high-accuracy torus quadrature. Neither comparator may silently replace the finite-mesh
correlation in a future direct result.

## Current numerical status

The bounded development run used the nominal `8^3` construction and `17^3` evaluation
meshes, parent scales `0` and `1`, three RMS gauge amplitudes through
`pi/(4 sqrt(12))`, and complete FCC metric shells through index `7`. Its development
summary reported `passes: true` and a maximum stored identity defect of about `4.5e-15`.
Several sampled first-passing decisions remained unresolved at the declared shell cap;
no tolerance, cap, or model was changed in response.

The historical outputs were produced by a former custom aggregation workflow. That
workflow and its duplicate schemas have been removed, and historical hashes do not
establish admission by the current typed action surface. Because no retained execution
directory exists, this report presents no retained result table, verification outcome,
authenticated figure, or seal.

The bounded `8/16/32` action ladder is a replaceable numerical check, not a convergence
disposition.

## Formal theorem crosswalk

Project Koios Formal was inspected at merge commit
`9f27941db0472683fd3971c462301ab6e0a3d046` (tree
`cc5030f6227b0c2acfa7cfd48dd9a2d1fe038d5e`). The proved declarations
`BG-FOURIER-THM-129`, `BG-FOURIER-THM-130`, `BG-FOURIER-THM-132`, and
`BG-FOURIER-THM-133` establish the normalized one-circle identity, the finite-product
power law, the exact `Fin 3` cube, and the scaled `J_0(2a/3)^3` result. After the
protocol substitution `a = g sqrt(6)`, this has the proposition shape of the matched
simple-cubic comparator.

This is not a KSD runtime certificate. KSD has no frozen checked bridge binding its
serialized phase, coordinate map, measure normalization, quadrature, binary64 values,
Fourier conversion, or comparator code to the Lean objects. Formal also has no retained
FCC six-factor triple-sum theorem, reviewed tail certificate, or runtime quadrature
certificate for this calculation. The checked runtime-certificate count is zero.

The exact product-torus theorems fix `Fin 3 -> UnitAddCircle`, standard Haar probability
measure, period-one coordinates `sin(2 pi x)`, positive phase, and no extra `2 pi` in
the real amplitude. Their reported foundational dependencies are `propext`,
`Classical.choice`, and `Quot.sound`; they are not described as axiom-free.

## Evidence lifecycle

A future retained execution must preserve:

`typed configuration -> typed result -> independent finite verification -> authenticated render`

The producer refuses to overwrite existing execution bytes. Verification must bind the
exact configuration and result hashes and independently reproduce its declared finite
comparisons. Rendering is presentation only and requires a passing verification record.
A passing chain remains **CALCULATED RESULT — UNSEALED** until a separate
owner-controlled sealing contract and authorization are completed.

## Limitations and nonclaims

This report does **not** establish:

- a retained result or passing retained verification record;
- silicon physics, `sp3s*` bands, valleys, effective masses, or experimental agreement;
- mesh, shell, Bessel-series-tail, quadrature, or finite-to-continuum convergence;
- convergence of the bounded `8/16/32` refinement ladder;
- correctness of floating-point, eigensolver, serialization, or plotting machinery;
- a Lean-checked FCC comparator or KSD runtime proposition;
- sealed evidence, production readiness, publication acceptance, or novelty.

## Ownership and reproduction

The calculation owner is
`calculations/periodic3d_rank2_fcc_diamond/band_equivalence_hopping_locality/`. The
governing protocol is
`calculations/periodic3d_rank2_fcc_diamond/band_equivalence_hopping_locality/protocol/experimental-protocol.tex`.
The maintained actions are `run_nominal_calculation.py`, `run_refinement_01.py`,
`run_refinement_02.py`, and `render_nominal_analysis.py`.

All outputs remain replaceable diagnostics. Running an action creates new bytes and
provenance; it does not promote the historical summary, complete a convergence study,
or create an evidence seal.
