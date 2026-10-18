# Band Equivalence versus Hopping Locality experiment

## Maintained identity and location

The publication-independent family is

```text
ksdft2effmass.campaign.model-adequacy.periodic1d.band-equivalence-versus-hopping-locality
```

Its maintained source is under
`experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/`. Historical `M3`,
conference, paper, and appendix labels remain searchable aliases only. Existing source
and retained calculation evidence under `calculations/` is not rewritten.

No maintained version, retained run, or evidence-package identity has been assigned.
The former draft `v0` freeze was retired before commitment and is not an experiment
version.

## Active smooth-continuum boundary

The active experiment contains two realizations under the same smooth rotation family.
The analytic benchmark uses the normalized flat rank-two parent under

```math
U_a(q)=R(a\sin 2\pi q), \qquad 0\leq a\leq \pi/4.
```

Here `q=k/G=k a_0/(2\pi)` is the reduced dimensionless reciprocal coordinate. KSD owns
this physical meaning, reciprocal meshes, amplitudes, harmonic coefficients, finite
Fourier convention, thresholds, convergence controls, evidence correlation, and
interpretation.

The exact live owner dependencies are
`projectkoios-optimization@2c6dd7f717722f6b0495feb8cfe1287a104268a6` and
`projectkoios-physkit@7120b735c7e3e450aa8924780a71deb59d812632`.
`PeriodicHarmonicMaximizer` owns exact continuous harmonic maximization, and
`ComplexUnitaryProcrustesSolver` owns each full-rank source-to-target pairwise frame
alignment without null-space completion for deficient overlaps. The Numerics
finite-Fourier evaluator constructs shifted-mesh discrete blocks and checks nodal
reconstruction. PhysKit's block-hopping records and power analyzer own raw matrix-block
Frobenius powers, while its band evaluators compose Bloch reconstruction with the
canonical Numerics multi-series Fourier and batched Hermitian-spectrum solvers and
restore energy units. KSD
calls these owners directly, retains finite-cyclic Nyquist Hermiticity semantics, and
applies its own normalizations and scientific thresholds. The
independent non-flat verifier reconstructs $b_0+\sqrt{c^2+d^2}$, frame transport, and
block powers without calling the corresponding producer actions. No thin pass-through
adapter is introduced.

No finite-angle inventory occurs in active definitions, results, calculations,
verification, serialization, or schemas. The active result keeps separate:

- finite-mesh correlation `mu_N,max`;
- analytic comparator `J_0(2a)`;
- their quadrature defect;
- conventional ordered-eigenvalue band defect;
- continuously aligned minimum and exact-spectrum joint operator thresholds;
- complete finite-mesh Fourier-block powers and non-onsite hopping weight; and
- Parseval and residual-decomposition defects.

The analytic comparator is never substituted into finite-mesh evidence. Finite Fourier
blocks remain aliased discrete coefficients until convergence is demonstrated.

## Convergence and verification

`SmoothBlochContinuumConvergenceDefinition` accepts explicit nested doubling meshes,
amplitudes, caller-selected tolerances, and a required number of stable final
refinements. No mesh ladder or tolerance is frozen by the source contract.

Adjacent refinements compare finite-mesh correlation, operator thresholds, non-onsite
hopping weight, shared Fourier-block powers, and the canonical maximizing angle. The
fine mesh must also satisfy declared bounds for quadrature, band, identity, and Parseval
defects. The verification absolute tolerance is added to every metric as a conservative
margin before comparison; cases without that complete margin are `unresolved`. The only
dispositions are `converged` and `unresolved`. Convergence establishes
stability for this analytic family only; it is not material or physical validation.

`SmoothBlochContinuumVerifier` reconstructs each mesh without calling the producer or
the Optimization maximizer. `SmoothBlochContinuumConvergenceVerifier` independently
reconstructs refinement metrics and the final disposition. Canonical serializers bind
input, result, and verification documents by SHA-256, and strict schemas reject unknown
fields and altered method identities.

## Current exploratory analysis

The local analysis under
`experiments/model-adequacy/periodic1d/band-equivalence-versus-hopping-locality/analysis/`
finds roundoff-level momentum-refinement changes throughout the proposed
$N=32,64,128,256,512$ ladder for the analytic flat-parent family. It also tests
between-node amplitude resolution rather than comparing only nested shared nodes. The
proposed amplitude ladder through $N_a=64$ has maximum piecewise-linear midpoint defects
of approximately $3.08\times10^{-5}$ and $1.41\times10^{-5}$ for the two threshold
curves, so it does not meet the manuscript's draft $1.01\times10^{-8}$ unit-scale
criterion. This blocks freezing the amplitude protocol. The analysis is exploratory and
creates no retained run or evidence-package identity.

## Initial non-flat realization

The typed non-flat realization constructs a dispersive four-state Hermitian parent,
selects the isolated lower two-state spectral subspace, closes a deterministic
parallel-transport frame, and applies the same smooth
$U_a(q)=R(a\sin 2\pi q)$ family. It reports external gap, transport-rank,
orthonormality, closure, Hermiticity, band, harmonic, threshold, complete finite-Fourier,
non-onsite-weight, Parseval, and reconstruction channels. It does not assume the
flat-parent residual--tail identity or a $J_0(2a)$ comparator.

The producer calls the exact continuous harmonic owner; `SmoothFourStateVerifier`
independently rebuilds the parent, retained frame, Fourier evidence, and harmonic maximum.
Nested momentum refinement has only `converged` and `unresolved` dispositions and adds
the verification absolute tolerance before every threshold comparison. Neighboring-frame
transport singular values are qualification gates, while shared parent eigenvalues and
retained spectral projectors provide frame-invariant cross-mesh controls. The current
exploratory $N\leq512$ momentum study is `converged`; the $N_a\leq64$ amplitude ladder
still fails its midpoint tests. The deterministic adaptive action caches direct samples,
evaluates every interval midpoint, refines only failing intervals, and requires a
separate quarter-point inventory after midpoint acceptance. It adds the verification
margin to every selection and validation test and remains `unresolved` at its explicit
level or unique-sample cap. Its
production cap and thresholds are not frozen. Admissible-set/witness controls, strict
serialization, and schemas remain prospective. Disjoint post-decision evaluation is now
implemented only for the exploratory finite-range consequence action described below.

## Finite-range consequence action

`SmoothFourStateTruncationExperiment` separates the complete even-mesh cyclic Fourier
inventory from an ordinary-lattice hopping model. KSD removes and reports the centered
Nyquist block as a distinct conversion-power channel. The remaining conjugate-closed
ordinary inventory is passed directly to PhysKit for Hermiticity diagnostics and one
canonical ordered range-family evaluation. PhysKit retains each exact symmetric
truncation and raw omitted power, shares the reciprocal-grid phase matrix across source
and retained models, and performs one concatenated complete-spectrum solve. KSD chooses
the cutoffs, applies retained-rank and $E_G$ normalization, constructs the disjoint
shifted evaluation mesh, and reports interpolation, deliberate truncation, and total
sorted-band errors separately.

The action does not infer cyclic equivalence inside PhysKit and requires every cutoff to
satisfy $R_c<N/2$. Direct comparison matrices remain unitarily related to the ordinary
reference before truncation. The comparison finite interpolant is measured separately
against that direct field, so its aliasing/interpolation defect cannot be reported as a
range-truncation consequence.

This layer is exploratory. Cutoffs and error targets are not frozen, independent result
verification and strict serialization are not implemented, and no retained result or
range-to-accuracy claim is issued. Velocity, curvature, and physical effective mass are
outside the current action pending internal-band qualification, derivative conventions,
and physical length/energy units.

## Parent-hopping homotopy

`SmoothFourStateParentFamilyDefinition` scales every non-onsite parent block by
$0\leq\rho\leq1$ while preserving the onsite matrices, retained rank, frame protocol,
and representation-rotation family. This separates parent dispersion and pre-existing
locality from the representation amplitude $a$. The exploratory study samples five
$\rho$ values, 33 amplitudes, and momentum meshes through $N=256$; all five momentum
studies return `converged`. The analysis compares the normalized residual
$x=\epsilon_{\min}^2/\kappa$ with normalized excess locality
$y=(P_{>0}^{A}-P_{>0}^{H})/\kappa$. The flat endpoint satisfies $y=x$; away from that
endpoint, $y-x$ is reported as a diagnostic departure rather than assuming the flat
identity. The study does not infer a continuous-$\rho$ certificate from its finite
samples. The homotopy remains part of the same experiment realization rather
than defining a new publication-derived experiment family.

## Historical regression isolation

The prior four-state, nine-angle, 64/257 calculation is retained only through the
explicit `band_equivalence_hopping_locality.regression` namespace and
`regression/historical-64-257/`. Its binding records the historical revision, tree, and
file digests. It has no maintained version identity, source freeze, evidence policy,
run identity, or evidence-package identity.

That fixture detects unintended changes to historically matched software channels. It
does not select scientific meshes, thresholds, alignment, convergence, dispositions, or
publication conclusions. The separate threshold-sensitivity calculation remains
excluded from its baseline.

## Remaining work before versioning

Before assigning a maintained version, the experiment still requires a reviewed
momentum ladder, a direct or adaptive amplitude rule, frozen disjoint-evaluation and
cutoff inventories, numerical tolerances, uncertainty propagation near thresholds,
independent truncation-result verification, strict non-flat schemas, and qualification
of the smooth non-flat four-state realization. Retained execution and evidence packaging
require separate operator authorization.
