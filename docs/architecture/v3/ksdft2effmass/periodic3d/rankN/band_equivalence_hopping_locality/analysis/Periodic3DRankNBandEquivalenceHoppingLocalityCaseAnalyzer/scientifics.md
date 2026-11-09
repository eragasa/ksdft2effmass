# `Periodic3DRankNBandEquivalenceHoppingLocalityCaseAnalyzer` scientific interpretation

The class evaluates a finite synthetic periodic-3D rank-N baseline and reports attained
matrix, spectrum, transport, Fourier, locality, and support diagnostics. These are
software-development results, not material validation or retained scientific evidence.

The parent and gauge transformation are distinct scientific objects.
`Periodic3DRankNParentModel` requires the parent to own its exact structured basis,
ambient embedding, spectra, support, reference frames, represented Hamiltonians,
isolation-gap lower bound, energy convention, and stable model identity. A concrete
analytic calculation may represent that parent with PhysKit block-hopping objects, but
neither the formulas nor the provider construction belong to reusable source.
`parent_scale` is a parent-family parameter, not a generic analysis parameter. The
`Periodic3DRankNGivensGaugeTransformation` supplies a right-acting unitary field, its
application to any admitted frame or represented operator of matching rank, and the
construction inverse. Circuit depth, normalization, harmonic bonds, and transformation
coefficient therefore identify the transformation rather than the parent Hamiltonian.

The generic field analyzer receives immutable reference and comparison frames and
represented operators through `Periodic3DRankNBandEquivalenceFieldSamples`. Prescribed
inverse actions are optional and are required only when policy selects the
known-inverse-oracle route. The separate
`Periodic3DRankNBandEquivalenceHoppingLocalityPolicy` contains the regular
construction-transform size, per-axis centered-mesh offsets, explicit error-normalization
scale, alignment routes, optional support-decision tolerances, numerical-rank
selections, and the explicit ordered reciprocal-endpoint sewing inventory without
parent or transformation parameters. The sewing matrices act in the ambient frame
space and therefore have the frame ambient dimension, not merely the retained rank. An
empty tolerance inventory retains complete support curves without manufacturing
first-passing decisions.
Evaluation coordinates belong to the
sampled fields: a tensor-product inventory retains the established tensor evaluator,
while an arbitrary ordered point inventory uses the shared-grid finite-series evaluator.
The resulting field analysis likewise carries operator, energy, basis, rank, and
alignment evidence without claiming a synthetic model identity or external gap.

Those operands may come from the parent/gauge case sampler or the in-memory Wannier-field
producer. The sampler preserves the parent-owned basis display identity at the legacy
represented-field boundary. The Wannier adapter validates array shape, frame isometry,
represented-operator Hermiticity, units and representation labels, then optionally
applies the independent Givens transformation. It does not establish DFT or Wannier90
convergence, source-file identity, subspace acceptance, or material validation. The case
analyzer samples its supplied correlated case, invokes the generic field analyzer, and
then adds the study-specific metadata envelope.

The non-onsite summary is a diagnostic projection, not the support-selection owner.
Because its current subtraction can suppress roundoff-scale power, a stored zero must
not be interpreted as a categorical strictly-onsite statement. Physical-metric shell
powers and truncation decisions retain their separately calculated meanings.

The limitation is deferred under
[`TD-BEL-003`](../../../../../../../../tasks/tech_debt/band-equivalence-locality/index.md#td-bel-003-rank-n-non-onsite-summary-subtraction)
until scale expansion, retained production, or a strictly-onsite claim requires its
replacement.
