# Periodic 3-D rank-two band equivalence and hopping locality

## Report status and reading rule

This report describes the orthogonal three-dimensional simple-cubic calculation owner.
The nominal direct `calculate -> independently verify -> authenticated render` lifecycle
is installed, but **no periodic-3D direct execution is retained**.

The available numerical summary belongs to a replaceable bounded development run. It is
not admitted direct-lifecycle evidence, a convergence ladder, a production calculation,
or sealed scientific evidence.

The lifecycle was inspected at KSD revision
`a5fc0e99b8e4a91dfd3006692255b1acb522a03d` (tree
`f5c9479ee7fc9d14f185ced0ad2df31029e7da76`). The revision fixes source identity only.

## Scientific question

The study extends the finite rank-two gauge/locality comparison to a three-dimensional
simple-cubic synthetic parent. It asks how a momentum-dependent rank-two unitary can
preserve pointwise bands while redistributing Fourier weight among complete cubic
translation shells.

The study is intentionally synthetic. It is not a silicon calculation, a
density-functional calculation, an effective-mass extraction, or a material-validation
exercise.

## Frozen nominal request

If executed, the direct producer fixes:

| Item | Nominal value |
|---|---|
| Case | `simple-cubic-directed-parent` |
| Dimension / retained rank | 3 / 2 |
| Positive bonds | `(1,0,0)`, `(0,1,0)`, `(0,0,1)` |
| Direct metric | cubic primitive lattice |
| Parent / gauge normalization | directed-axis / axis-maximum |
| Construction mesh | `8 x 8 x 8` tensor Monkhorst--Pack mesh |
| Evaluation mesh | disjoint shifted `17 x 17 x 17` mesh, shift `1/3` |
| Parent scales | `0`, `1` |
| Gauge amplitudes | `0`, `pi/8`, `pi/4` |
| Band tolerances | `1e-3`, `1e-5` |
| Shell cap | every attainable cubic shell through squared radius `9` |
| Model | synthetic four-state locality development model v1 |

No direct result, verification status, or provenance hash may be inferred from this
checked-in request alone.

## Resource-bounded method

The producer uses tensor-product finite meshes and does not materialize a dense global
Hamiltonian. It records parent-spectrum and retained-subspace qualification, graph-frame
closure, covariant and restricted alignment, exact mesh-origin-aware three-dimensional
Fourier conversion, complete cubic shell inventories, twisted-Nyquist and ordinary
Hermiticity checks, interpolation and truncation errors, total matrix and spectral
errors, Parseval checks, resource diagnostics, and sampled first-passing shell decisions.

Construction-mesh interpolation, support truncation, and total evaluation error remain
distinct. The complete-shell policy includes every translation at a given metric radius;
a coordinate box or selected axial subset is not an admissible replacement.

A sampled decision remains unresolved when no stored shell through the frozen cap
satisfies all mandatory channels. That fail-closed result must not be rewritten as a
continuum impossibility or repaired by changing the cap after inspection.

## Analytic flat-parent control

For parent scale `rho = 0`, the protocol fixes a constant retained frame and uses

`theta_a(q) = (a/3) sum_{alpha=1}^3 sin(2 pi q_alpha)`.

The normalized continuum phase average factorizes with proposition shape

`<exp(2 i theta_a)> = J_0(2a/3)^3`.

This yields the protocol's flat-parent correlation and operator-loss comparators. They
are analytic controls, not finite-mesh substitutes. They do not authenticate runtime
quadrature, certify Fourier coefficients, or establish finite-to-continuum convergence.

## Current numerical status

The bounded development run used the nominal `8^3` construction and `17^3` evaluation
meshes, parent scales `0` and `1`, amplitudes `0`, `pi/8`, and `pi/4`, and all attainable
cubic shells through squared radius `9`. Its development verifier reported `passes:
true`, with a maximum stored identity defect of about `6.0e-15`.

The rotated endpoint remained unresolved at the sampled shell cap. This is the required
failure-safe disposition, not a negative scientific result.

The historical input, result, and verification documents were produced by a former
custom aggregation workflow. That workflow and its duplicate schemas have been removed.
The development records do not establish admission by the current typed lifecycle.
Because no `executions/direct-simple-cubic-rank2-n8/` directory is retained, there is no
direct result table, direct verification hash, authenticated direct figure, or seal to
report.

The protocol discusses a possible `16/32/64` refinement ladder, but this development run
does not authorize or complete that ladder.

## Formal theorem crosswalk

Project Koios Formal was inspected at merge commit
`9f27941db0472683fd3971c462301ab6e0a3d046` (tree
`cc5030f6227b0c2acfa7cfd48dd9a2d1fe038d5e`). Relevant source-neutral proved
declarations are:

- `BG-FOURIER-THM-129`, the normalized one-circle sine-phase `J_0` identity;
- `BG-FOURIER-THM-130`, the arbitrary finite product power law;
- `BG-FOURIER-THM-132`, the exact `Fin 3` cube;
- `BG-FOURIER-THM-133`, the exact scaled result `J_0(2a/3)^3`;
- `BG-SPECIAL-THM-014`, the full-angle zeroth-order Bessel integral.

The scaled `Fin 3` proposition has the mathematical form required by the flat-parent
comparator. It fixes `Fin 3 -> UnitAddCircle`, standard Haar probability measure,
period-one coordinates `sin(2 pi x)`, positive phase, and no hidden `2 pi` factor in the
real amplitude.

This does not bind the KSD serialization or runtime to those Lean objects. No frozen
proposition-specific certificate proves KSD's phase convention, coordinate map, measure,
quadrature, binary64 values, Fourier conversion, or comparator implementation. Formal
does not establish mesh convergence or scientific adequacy. The checked
runtime-certificate count is zero.

The cited declarations are proved without repository admissions and report the standard
Lean/Mathlib foundational dependencies `propext`, `Classical.choice`, and `Quot.sound`.
They should not be described as axiom-free.

## Evidence lifecycle

A future direct run must retain the complete owner-controlled chain:

`typed configuration -> typed result -> independent finite verification -> authenticated render`

The scripts refuse to overwrite an existing execution. Verification must bind the exact
configuration and result bytes and reproduce the declared finite comparisons. Rendering
is presentation only and may start only from passing verification. A passing chain would
still be **CALCULATED RESULT — UNSEALED** until a separate sealing contract and
authorization are satisfied.

## Limitations and nonclaims

This report does **not** establish:

- a retained direct result or passing direct verification record;
- completion of the proposed `16/32/64` refinement ladder;
- mesh, shell, amplitude, or finite-to-continuum convergence;
- a material, silicon, effective-mass, or first-principles conclusion;
- correctness of floating-point, eigensolver, serialization, or plotting machinery;
- a Lean-authenticated runtime comparator or Fourier transform;
- sealed evidence, production readiness, publication acceptance, or novelty.

## Ownership and reproduction

The calculation owner is
`calculations/periodic3d/rank2/orthogonal/band-equivalence-locality/`. The governing
protocol remains
`experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/experimental-protocol.tex`.
The direct entry points are `run_01_calculation.py`, `run_02_verification.py`, and
`run_03_render.py`.

Development and refinement surfaces remain replaceable diagnostics outside the direct
lifecycle. Running them creates new bytes and provenance; it does not promote the
historical summary or create a seal.
