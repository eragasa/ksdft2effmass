# Periodic 2-D rank-two band equivalence and hopping locality

## Report status and reading rule

This report describes the calculation-owned orthogonal two-dimensional square-lattice
study. The repository currently retains one direct execution,
`direct-square-rank2-n16`, with the explicit status:

> **CALCULATED RESULT — UNSEALED**

The retained bytes are finite sampled synthetic output. They are not sealed production
evidence, a convergence result, a material calculation, publication acceptance, or a
Lean-checked runtime certificate.

The direct lifecycle and retained execution were inspected at KSD revision
`a5fc0e99b8e4a91dfd3006692255b1acb522a03d` (tree
`f5c9479ee7fc9d14f185ced0ad2df31029e7da76`). This immutable source anchor identifies
the implementation read by this report; hashes identify bytes, not scientific validity.

## Scientific question

The study isolates a representation question: two rank-two Bloch operator fields can
have the same pointwise bands while a momentum-dependent unitary changes the locality of
their Fourier representation. On a bounded square-lattice control, the calculation asks
how much finite shell support is required to satisfy declared operator and band-error
tolerances after that gauge change.

This question is narrower than material adequacy. The model is a synthetic four-state
parent with a retained rank-two subspace. No graphene, silicon, density-functional,
effective-mass, experimental, or first-principles claim is made.

## Frozen nominal request

The retained request fixes the following finite design.

| Item | Retained value |
|---|---|
| Case | `square-directed-parent` |
| Dimension / retained rank | 2 / 2 |
| Direct primitive basis | unit square, primitive vectors stored by columns |
| Parent / gauge normalization | directed-axis / axis-maximum |
| Construction mesh | `16 x 16` tensor Monkhorst--Pack mesh |
| Evaluation mesh | disjoint shifted `33 x 33` mesh, shift `1/3` |
| Parent scales | `0`, `1` |
| Gauge amplitudes | `0`, `pi/8`, `pi/4` |
| Band tolerances | `1e-3`, `1e-5` |
| Shell cap | every attainable square shell through squared radius `25` |
| Energy reference and units | synthetic dimensionless zero reference |

The request, model identity, basis, gauge family, support inventory, mesh origins,
tolerances, and shell cap are operands of the result. Changing any of them defines a new
calculation rather than a reinterpretation of this execution.

## Method

The direct producer executes the calculation-owned typed request and records:

1. parent-spectrum and retained-subspace qualification;
2. graph-frame construction and closure diagnostics;
3. covariant and restricted alignment channels;
4. mesh-origin-aware multidimensional Fourier conversion;
5. complete square metric-shell inventories, including the even-mesh Nyquist classes;
6. interpolation, truncation, and total matrix and spectral errors;
7. Parseval, Hermiticity, twisted-Nyquist, reconstruction, and identity diagnostics; and
8. sampled first-passing shell decisions at the declared band tolerances.

Construction-mesh interpolation, support truncation, and total evaluation error remain
separate channels. A small total error does not erase a large interpolation or
truncation contribution. Likewise, equality of the pointwise bands under unitary
conjugation does not imply equality of Fourier support after a momentum-dependent gauge.

A first-passing decision exists only when a stored shell satisfies every required finite
criterion. A row that does not pass by the frozen cap remains unresolved; neither the
cap nor the tolerance may be changed after seeing the result.

## Direct execution and verification record

The retained ownership chain is:

`configuration -> calculation result -> independent finite verifier -> authenticated render`

The execution manifest records `sealed: false`. Its principal byte identities are:

| Artifact | SHA-256 |
|---|---|
| `inputs/configuration.json` | `01a13192e096be5c310550ea6d34ffbf619589cedcca5f8e275f3c8ce7f3b5ab` |
| `results/result.json` | `4159c5e8dc60da2db81d7160fad27d98abc9c2564cafea6877530db0b6cffa1a` |
| retained calculation-producer snapshot | `ed7efc16dc32100fbf3de413feaddbe20857d8adedf11f763590548022fba29b` |
| retained verification-producer snapshot | `997c89707333861c3172dff4f469b0762f2da1fd67942f424471d2a838a62ef6` |
| `verification/verification.json` | `fccb0bfbb46777b4ac24110bdb01ff32aca804a90535f630e5ecca59c79616b0` |

The script identities bind the immutable copies retained under the execution's
`producers/` directory; they are not assertions about a later checkout of the root entry
points.

The verifier records five passing comparisons: independently recomputed band values,
parent values, shell powers, stored identity defects, and projection-inventory
defects. The largest listed comparison defect is about `7.55e-15`, below its declared
`5e-11` tolerance. This is finite numerical verification of the stored result contract;
it is not an independent scientific replication, a continuum bound, or an evidence
seal.

The authenticated figure
`executions/direct-square-rank2-n16/figures/band-equivalence-locality-requirements.png`
is presentation derived from that verified finite result. Its rendering record binds the
verification JSON and labels the figure as presentation rather than new evidence.

## Current result boundary

Within the retained finite request, the calculation and verifier report a completed,
passing typed lifecycle. Some strict sampled first-passing decisions remain unresolved
at the declared shell cap. That is a valid fail-closed outcome, not a negative continuum
or material conclusion.

The historical development surface reports the same bounded `16/33` design, `passes:
true`, and a maximum stored identity defect of about `4.1e-15`. Those development
artifacts are replaceable and are not admitted into the direct lifecycle. Their former
custom aggregation workflow and duplicate schemas have been removed.

## Analytic flat-parent control

For parent scale `rho = 0`, the protocol fixes the retained frame to the constant two
lowest eigenvectors of the parent and forbids an additional momentum-dependent frame
gauge. With

`theta_a(q) = (a/2) [sin(2 pi q_x) + sin(2 pi q_y)]`,

the normalized continuum comparator has the proposition shape

`<exp(2 i theta_a)> = J_0(a)^2`.

The protocol consequently derives its flat-parent correlation and operator-loss
comparators from that average and a continuum Parseval identity. These analytic values
remain comparators only; they do not replace the stored finite-mesh correlation, verify
the quadrature, or prove finite-to-continuum convergence.

## Formal theorem crosswalk

The exact source-neutral mathematics was inspected in Project Koios Formal at merge
commit `9f27941db0472683fd3971c462301ab6e0a3d046` (tree
`cc5030f6227b0c2acfa7cfd48dd9a2d1fe038d5e`). Relevant proved declarations are:

- `BG-FOURIER-THM-129`: the normalized positive sine-phase circle average is `J_0(b)`;
- `BG-FOURIER-THM-130`: equal sine phases on a finite normalized product torus give a
  cardinality power of `J_0`;
- `BG-FOURIER-THM-131`: the exact `Fin 2` product-torus specialization is `J_0(b)^2`;
- `BG-SPECIAL-THM-014`: the corresponding full-angle exponential kernel equals
  `2 pi J_0`.

Those Lean propositions fix the carrier `Fin 2 -> UnitAddCircle`, standard Haar
probability measure, period-one coordinate `sin(2 pi x)`, positive phase, and no extra
`2 pi` in the real amplitude. They use only Lean/Mathlib's standard classical
foundations reported as `propext`, `Classical.choice`, and `Quot.sound`.

This is a conditional mathematical crosswalk, not a runtime certificate. KSD has not
frozen or checked a proposition-specific bridge proving that the serialized phase,
coordinate map, measure normalization, binary64 values, quadrature, Fourier transform,
or comparator implementation are the exact objects in the Lean theorem. The checked
runtime-certificate count for this calculation is therefore zero.

## Limitations and nonclaims

This report does **not** establish:

- mesh, shell, or amplitude convergence;
- a continuum locality threshold or a continuous-amplitude result;
- correctness of NumPy, SciPy, eigensolvers, floating-point arithmetic, serialization,
  or plotting beyond the stated finite verification comparisons;
- authentication of the runtime analytic comparator by Lean;
- uncertainty quantification, model adequacy for a material, or experimental agreement;
- sealed evidence, production readiness, publication acceptance, or novelty.

## Reproduction and ownership

The calculation owner is
`calculations/periodic2d/rank2/orthogonal/band-equivalence-locality/`. The governing
scientific protocol remains
`experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/experimental-protocol.tex`.
The nominal lifecycle is exposed by `run_01_calculation.py`,
`run_02_verification.py`, and `run_03_render.py`.

The direct scripts refuse to overwrite an existing execution. Development and
refinement surfaces remain outside the nominal lifecycle. Reproduction creates new
bytes and a new provenance event; it does not retroactively seal this execution or
promote its claim status.
