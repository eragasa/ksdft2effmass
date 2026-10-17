# Conference paper 2: multidimensional spectral-to-tight-binding representation

## Working title

> *From spectral Hamiltonians to tight binding in two and three dimensions: isotropic
> locality on orthogonal and non-orthogonal lattices*

## Scope

Paper 2 is the prospective multidimensional continuation of Paper 1. The inherited
spatial/lattice promises, deliberate exclusions, and remaining qualification work are
tracked in [`paper-1v3-successor-crosswalk.md`](paper-1v3-successor-crosswalk.md). The
stronger quantity-by-quantity requirement is tracked against all 110 predecessor rows in
[`paper-1v3-calculation-parity-audit.md`](paper-1v3-calculation-parity-audit.md). It is
organized around the publication-independent experiment families:

- [`../../../../experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/`](../../../../experiments/model-adequacy/periodic2d/band-equivalence-versus-hopping-locality/)
- [`../../../../experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/`](../../../../experiments/model-adequacy/periodic2d_nonorthog/band-equivalence-versus-hopping-locality/)
- [`../../../../experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/`](../../../../experiments/model-adequacy/periodic3d/band-equivalence-versus-hopping-locality/)
- [`../../../../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/`](../../../../experiments/model-adequacy/periodic3d_nonorthog/band-equivalence-versus-hopping-locality/)

A prospective geometry-stress extension is owned separately by:

- [`../../../../experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/`](../../../../experiments/model-adequacy/periodic2d/gauge-locality-under-synthetic-strain/)
- [`../../../../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/`](../../../../experiments/model-adequacy/periodic3d/gauge-locality-under-synthetic-strain/)

The paper will compare complete cell--orbital, Bloch, spectral-eigensystem, retained-frame,
and Wannier/tight-binding representations. It will permit Hamiltonian subtraction only
after the relevant spaces, frames, gauges, energy references, units, and normalizations
have been explicitly aligned.

The phrase **non-orthogonal, non-anisotropic** is taken literally here to mean
non-orthogonal primitive-cell geometry with a physically isotropic model. Isotropy is
therefore defined using the direct-lattice metric and complete lattice-point-group bond
orbits, not equality of coefficients attached to arbitrary coordinate axes. Anisotropic
hopping amplitudes or direction-dependent physical laws remain outside Paper 2 unless
its scope is changed explicitly.

## Scientific stages

1. Square-lattice and simple-cubic orthogonal isotropic baselines.
2. A graphene-inspired triangular/honeycomb 2-D target with separate matched Bravais
   controls, followed by a silicon-inspired FCC/diamond 3-D target with separate matched
   Bravais controls.
3. Cross-dimensional comparison only after each experiment has its own convergence,
   verification, and evidence qualification, while satisfying the shared
   [`test and diagnostic parity contract`](../../../../experiments/model-adequacy/band-equivalence-test-and-diagnostic-parity.md).

The separate non-orthogonal families now select the primitive metrics,
two-site honeycomb/diamond bases, inspired bipartite parents, matched Bravais-control
parents, RMS gauge-amplitude convention, analytic comparators, metric shells,
basis-aware distance diagnostics, and primitive-basis covariance controls. Mesh and
shell caps, control-parent gap qualification, comparator-tail certification, final
tolerances and schemas, frozen revisions, and qualified convergence/verifier contracts
remain open. Bounded three-level actions with independent development verifiers now
exercise all four families without conferring evidence status. One pointwise
graphene-family shell decision changes between the first two levels; every decision is
unchanged on the final refinement. All 110 Paper 1 catalog rows now have an explicit
mapping, while row-level independent parity verification and the multidimensional
closure-phase aggregation remain open.
``Graphene-inspired'' and
``silicon-inspired'' identify
structural synthetic controls only; neither is a material parametrization or validation.
Orthogonal directed-hopping outcomes must not be copied into the matched Hermitian-parent
controls.

## Working-color convention

In the rendered `manuscript.pdf`, red text marks prospective work, unexecuted
calculations, open controls, conditional conclusions, or content that must be replaced
by qualified evidence. Established definitions and currently selected mathematical
contracts remain black.

## Analytic proof status

The manuscript now contains an initial self-contained proof layer:

1. a Laurent-polynomial counterexample proving that spectral projection does not, as an
   operation, preserve finite hopping support; and
2. the orthogonal $d\in\{2,3\}$ flat-parent residual--locality theorem, including the
   $J_0(a)^2$ and $J_0(2a/3)^3$ correlations, the best constant restricted-alignment
   residual, the non-onsite Parseval identity, and the exact-spectrum threshold;
3. the monotonicity and small-amplitude dimension law, whose leading threshold slope is
   $\sqrt{2\kappa/d}$;
4. an exact shell-resolved Bessel-product formula and rigorous factorial Fourier-tail
   certificate for the orthogonal flat-parent family; and
5. a bond-orbit theorem expressing a selected non-orthogonal flat-parent comparator as
   the zero Fourier mode and as a Bessel sum constrained by integer relations among the
   orbit's reduced-coordinate bond vectors; and
6. a constrained-series complete-shell certificate with explicit one-index triangular
   and three-index FCC remainder bounds.

These are analytic manuscript proofs, not numerical evidence, formal-prover results, or
independently reviewed acceptance records. The orthogonal factorial tail must not be
transferred to dependent bond orbits. The separate constrained certificates have bounded
binary64 development evaluations with declared numerical margins, but not formal
interval evaluation or qualified convergence status.

## References and literature boundary

The maintained BibTeX source is [`references.bib`](references.bib). It records the
foundational Wannier-localization literature, Wannier90 and maximally localized Wannier
review, compact-Wannier distinction, graphene Wannier model, strained hexagonal
Hamiltonians, environment-dependent Hamiltonian mappings, and the historical Bain
path. The manuscript cites these works where their roles are discussed and states that
none of gauge localization, strained Hamiltonians, environment response, or the Bain
path is individually claimed as new. The candidate contribution is the controlled
combination of fixed gauge, physical-metric complete supports, restricted alignment,
and first-passing physical hopping range.

## Status

The strain extension currently has bounded M0 diagnostics, separately labeled frozen
four-state M1 and fixed radial-response M2 smoke actions, and a software-verified
unimodular FCC-to-Bain common-cell map. Strict schemas, independent artifact verification,
and convergence remain open; it contributes no material-strain result.

This remains a pre-results manuscript package. Replaceable bounded three-level records
are available but do not constitute the paper's qualified numerical results or complete
the diagnostic-parity and convergence requirements. Proximity-only correlation endpoint
canonicalization remains deferred technical debt under
[`TD-BEL-001`](../../../../tasks/tech_debt/band-equivalence-locality/index.md). No protocol freeze,
qualified convergence result, retained run, evidence package, material claim, conference
submission, or publication is asserted or authorized. The previous
first-principles silicon Paper 2 has moved intact to
[`../conference-paper-4/`](../conference-paper-4/).
