# `Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer` scientific interpretation

The class evaluates a finite synthetic periodic-3D rank-N baseline and reports attained
matrix, spectrum, transport, Fourier, locality, and support diagnostics. These are
software-development results, not material validation or retained scientific evidence.

The finite-range block-hopping parent and the synthetic attack are distinct scientific
objects. `Periodic3DRankNBlockHoppingParentBuilder` constructs the parent as a PhysKit
`DenseBlockHoppingModel` with an onsite block and selected first- and second-harmonic hopping
blocks. The v1 `parent_scale` field is therefore a hopping/dispersion scale owned by
this parent construction, not a generic analysis parameter. The retained v1 field
sampler evaluates the equivalent closed-form Bloch law so that this internal ownership
correction does not change established binary64 result bytes. The parent supplies the
reference frame and represented Hamiltonian. The
`Periodic3DRankNGivensGaugeAttack` supplies a right-acting unitary field, its application
to any admitted frame or represented operator of matching rank, and the construction
inverse. Circuit depth, normalization, harmonic bonds, and attack coefficient therefore
identify the attack rather than the parent Hamiltonian.

The generic field analyzer receives immutable reference and comparison frames and
represented operators through `Periodic3DRankNBandEquivalenceFieldSamples`. Prescribed
inverse actions are optional and are required only when policy selects the
known-inverse-oracle route. The separate
`Periodic3DRankNBandEquivalenceHoppingLocalityPolicy` contains the regular
construction-transform size, per-axis centered-mesh offsets, explicit error-normalization
scale, alignment routes, optional support-decision tolerances, and numerical-rank
selections without synthetic parent or attack parameters. An empty tolerance inventory
retains complete support curves without manufacturing first-passing decisions.
Evaluation coordinates belong to the
sampled fields: a tensor-product inventory retains the established tensor evaluator,
while an arbitrary ordered point inventory uses the shared-grid finite-series evaluator.
The resulting field analysis likewise carries operator, energy, basis, rank, and
alignment evidence without claiming a synthetic model identity or external gap.

Those operands may come from the synthetic-case sampler or the in-memory Wannier-field
producer. The Wannier adapter validates array shape, frame isometry, represented-operator
Hermiticity, units and representation labels, then optionally applies the independent
Givens attack. It does not establish DFT or Wannier90 convergence, source-file identity,
subspace acceptance, or material validation. The v1 synthetic case analyzer samples its
case, invokes the generic field analyzer, and then adds the existing synthetic metadata
envelope without changing serialized results.

The non-onsite summary is a diagnostic projection, not the support-selection owner.
Because its current subtraction can suppress roundoff-scale power, a stored zero must
not be interpreted as a categorical strictly-onsite statement. Physical-metric shell
powers and truncation decisions retain their separately calculated meanings.

The limitation is deferred under
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction)
until scale expansion, retained production, or a strictly-onsite claim requires its
replacement.
