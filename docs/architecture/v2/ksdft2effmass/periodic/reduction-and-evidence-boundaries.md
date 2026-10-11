# Reduction and evidence boundaries

## Manuscript sources

The periodic software architecture must preserve the scientific boundaries established
throughout the monograph, especially:

- [Comparing Operators Responsibly](../../../../publications/research-monograph/chapters/operator-comparison.tex);
- [Evidence for Model Adequacy](../../../../publications/research-monograph/chapters/evidence-for-model-adequacy.tex);
- [Retained and Localized Bulk Representations](../../../../publications/research-monograph/chapters/bulk-representations.tex);
- [Bulk Reduced-Model Classes](../../../../publications/research-monograph/chapters/bulk-reduced-models.tex);
- [Extraction of the Impurity Operator](../../../../publications/research-monograph/chapters/impurity-operator-extraction.tex);
- [Lattice Impurity Model Classes](../../../../publications/research-monograph/chapters/lattice-impurity-models.tex);
- [Continuum Effective-Mass Reduction](../../../../publications/research-monograph/chapters/continuum-effective-mass.tex);
- [Current Evidence Boundary](../../../../publications/research-monograph/chapters/current-evidence-boundary.tex); and
- [Mathematical Structure of Reduction and Continuum Claims](../../../../publications/research-monograph/chapters/mathematics-of-reduction.tex).

This page extracts software-ownership consequences. It does not replace the scientific
or mathematical definitions in those chapters or an applicable specification.

## Operations must remain distinct

The following operations have different domains, codomains, invariants, and error
sources and therefore require distinct typed requests and results:

- selecting or projecting a target subspace;
- disentangling a retained subspace from a larger candidate space;
- changing gauge or basis within one fixed subspace;
- optimizing localization within that subspace;
- transforming between reciprocal- and real-space representations;
- truncating represented blocks or couplings;
- aligning independently constructed spaces;
- aligning scalar energy references;
- fitting or projecting into a restricted model class; and
- embedding a continuum model into an atomistic comparison space.

A generic transformation result must not erase which operation occurred. In
particular, Wannierization is not synonymous with rank reduction, localization does not
perform hopping truncation, and equal spectra do not supply an alignment map.

## Model class, model instance, operator, and fit result

A model class defines an admissible family and its constraints. A model instance fixes
one member of that family. Its operator is a mathematical object acting on a stated
space. A finite matrix is a representation of that operator. A fitted parameter vector
is an output of a declared fitting operation, not a complete model unless the class,
conventions, and construction are also identified.

A reduction definition therefore records, as applicable:

- the exact parent model, operator, and retained representation;
- the candidate model class and parameter domain;
- symmetry, orbital, spin, range, Fourier, sign, and energy-zero conventions;
- the reduction, projection, or fitting map;
- frozen training inputs and a disjoint withheld evaluation set;
- quantities, metrics, normalizations, tolerances, and intended use; and
- provenance for the resulting model instance and represented operator.

The selected model is the least complex member only relative to a frozen ordered
family and a complete prespecified acceptance rule. A failed criterion is not removed,
and the family is not expanded after inspecting outcomes merely to force acceptance.

## Compatibility and alignment are prerequisites

Equal array shape, matrix dtype, nominal dimension, orbital labels, or similar spectra
do not establish common represented meaning. A comparison gate checks the applicable
state-space, retained-rank, geometry, site mapping, basis and ordering, units, Fourier
convention, spin, scalar energy reference, and gauge prerequisites.

Subspace diagnostics and an alignment map are separate results. Principal angles or
overlap singular values diagnose compatibility; they do not themselves transport an
operator. The chosen identification records its direction, conditioning,
non-uniqueness, and residuals. Scalar energy alignment is another operation and cannot
be hidden inside a unitary basis map.

When compatibility or alignment is unavailable, direct subtraction stops. A declared
invariant comparison may still be possible, but it must state the invariant and the
claim it supports.

## Impurity extraction is a signed aligned operation

An impurity operator is not the raw doped Hamiltonian and not every perturbation is a
scalar potential. It is a signed pristine--doped operator difference after physical
branches, retained spaces, geometry, spin, units, energy references, and coordinates
have been made compatible.

The extraction request and result identify:

- pristine and doped parent identities;
- retained spaces and represented operators;
- alignment and energy-reference results;
- transport direction and operand order;
- full-unitary or partial-isometry status; and
- the common space in which the signed difference acts.

Onsite scalar, orbital-dependent onsite, bond or hopping, spin-mixing, and
finite-extent interpretations are subsequent typed analyses. Finite matrix dimension
does not establish finite spatial extent.

## Reduction routes have identities

Direct spectral fitting, operator-mediated fitting, truncation, extract-then-reduce,
and reduce-then-extract are distinct routes. Their outputs can be compared only when
they share compatible parentage, spaces, gauges, objectives, weights, domains, and
normalizations.

Exact route commutativity follows only under the applicable common linear map in common
coordinates. Nonlinear fitting, independently selected gauges, separately chosen
alignments, and gauge-dependent truncation can produce legitimate nonzero route
defects. A route defect is a result with a declared domain and norm, not automatically
an implementation failure.

## Continuum models require an embedding

A continuum effective-mass model has its own state space. Its matrix cannot be
subtracted directly from a lattice or retained atomistic operator. Comparison requires
an explicit embedding or identification with stated normalization, channel ordering,
discretization, boundary conditions, and domain of validity.

Continuum discretization, discrete-to-continuum scaling, band-edge homogenization, and
infinite-volume limits are separate processes. Varying several simultaneously does not
identify which approximation caused agreement. A finite crossover radius is not
assumed; an unavailable or infinite result over the tested domain is valid.

## Evidence and negative outcomes

Every result states a bounded claim before its evidence class, oracle, metric,
tolerance, and disposition. Mathematical proof, software verification, numerical
verification, scientific validation, and uncertainty quantification remain separate.
Reproduction and process completion do not promote evidence between these classes.

The architecture must represent negative and unavailable outcomes directly, including:

- incompatible or unaligned spaces;
- an unidentified model parameter or unstable fit;
- no accepted class in the tested frozen hierarchy;
- a nonconverged numerical sequence;
- a nonzero route defect under declared controls; and
- no finite crossover over the tested domain.

These outcomes retain the tested domain, rejected candidates, metrics, tolerances, and
limitations. They are not generalized beyond that domain, converted to zeros, or
silently removed from a catalog or report.
