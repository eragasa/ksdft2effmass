Periodic-1D defect extraction
=============================

The periodic-1D defect campaign is a chain of controlled synthetic capabilities.
The maintained software distinguishes five scientific operations:

#. matched extraction with a declared comparison map;
#. blind inference of an admissible alignment;
#. reconciliation of independent real-space and Bloch-fiber routes;
#. a finite-rank resolvent oracle; and
#. separated continuum refinement.

The historical phase letters A through E identify retained provenance only.  They are
not public software names.  All five families have canonical owners beneath
``ksdft2effmass.periodic1d.campaign``: matched extraction under ``extraction.matched``,
blind alignment under ``alignment.blind``, route reconciliation under
``reconciliation.route``, the finite-rank oracle under ``oracle.finite_rank``, and
continuum refinement under ``refinement.continuum``.  The former underscored defect
routes are removed without aliases.  Reusable controlled systems remain separate from
campaign provenance and acceptance policy.

Comparison boundary
-------------------

A defect perturbation is formed only after the represented parent and candidate are
identified on the same finite state space.  Compatibility includes the matrix
dimension, cell, orbital and spin factors, reduced momentum, site and internal ordering,
coordinate frame, energy unit, energy reference, geometry, and represented subspace.
The extraction code performs no implicit alignment, gauge conversion, basis mapping,
geometry transformation, or energy-zero inference.

The matched capability accepts an authored unitary comparison map.  It records the
parent :math:`H_0`, the aligned candidate :math:`H_{\mathrm{def}}`, and the extracted
operator perturbation

.. math::

   \Delta H = H_{\mathrm{def}} - H_0

as distinct represented operators.  A perturbation may contain onsite, bond,
orbital-mixing, and spin-mixing blocks; therefore the general object is an operator
perturbation and is not necessarily a scalar potential.

Blind-alignment boundary
------------------------

Blind alignment receives the reference and candidate represented Hamiltonians, an
anchor cross-covariance from candidate to reference coordinates, retained-subspace
overlap information, an exterior energy anchor, and explicit numerical policy.  It
does not receive the authored coordinate map, scalar energy shift, planted
perturbation, or post hoc oracle errors.

For anchor cross-covariance :math:`C=L\Sigma R^\dagger`, singular values above the
explicit rank tolerance define an identified sector and the inferred partial isometry
is

.. math::

   \widehat U = L_r R_r^\dagger.

With reference-sector projector :math:`P=\widehat U\widehat U^\dagger`, aligned
candidate :math:`\widehat H_d=\widehat U H_d\widehat U^\dagger`, and an exterior
estimate :math:`\widehat\delta` of the scalar energy shift, extraction returns

.. math::

   \widehat V
   = \widehat H_d - \widehat\delta P - P H_0 P.

A rank-deficient result identifies only this compressed sector.  No completion on the
anchor-null complement is inferred.  Unequal represented dimensions stop on the
ordinary route and require the separate explicitly declared rectangular reconciliation
route.  Rank, spin, retained-subspace angle, anchor conditioning, and exterior
energy-anchor failures produce structured stops rather than implicit coercions.

Independent-route boundary
--------------------------

Independent-route reconciliation starts only after a candidate-to-reference map and
scalar energy correction have been declared. Route A assembles and subtracts the
finite twisted supercell directly in site space. Route B independently evaluates the
primitive Bloch fibers and folds them into the finite supercell representation. For
folding map :math:`F`, the commutativity comparison is

.. math::

   F^\dagger V^{(A)}F \stackrel{?}{=} V^{(B)}.

Both routes share authenticated mathematical inputs, so implementation separation is
not independent physical evidence. Changed hopping truncation, fiber domain,
quadrature weights, or alignment map is never absorbed into a nominal residual.
Comparisons either stop, report explicit noncommutativity, or use a separately declared
common-parent, common-domain, dual-map/induced-metric, or relative-unitary
reconciliation. A small spectral discrepancy does not erase an operator-level route
discrepancy.

Retained evidence
-----------------

The version-one inputs and results beneath ``calculations/research-monograph`` are
immutable evidence records.  Maintained deserializers enforce their exact schema,
units, ordering, source identities, and finite-value requirements.  Maintained
workflows may calculate a new result at a new path, while retained-result verifiers
independently reconstruct the bounded synthetic diagnostics.  Correlation with a
retained artifact establishes identity and consistency, not numerical verification by
itself.

The matched known-map capability is the first complete maintained package integration.
The canonical blind-alignment package provides strict version-one input and result
adaptation, authenticated matched-baseline loading, its typed observation-only
inference core, canonical result encoding, identity-only retained correlation, and
complete typed campaign composition.  Its supported package route is deliberately
limited to an immutable encoded-document owner and an encapsulating campaign façade;
lower-level records and Actionizers remain in defining modules rather than being
re-exported.  The former underscored route is removed without an alias; see
:doc:`../api/ksdft2effmass/periodic1d/campaign/alignment-blind` for the full API.  Its
independent verifier authenticates all direct and transitive sources and reconstructs
all retained exact, sensitivity, gauge, stop, and boundary-diagnostic records without
importing the maintained calculation algorithms.  This completes the maintained
software and numerical-verification slice for blind alignment while leaving all
material-validation and uncertainty claims explicitly excluded.

The route-reconciliation package now provides strict version-one input adaptation,
authenticated matched and periodic-parent loading, separate site-space and Bloch-fiber
Actionizers, explicit mismatch and reconciliation records, canonical retained-byte
correlation, and an independent verifier for all 15 records. Its supported facade
exports the campaign, the exact byte-only encoded-document pair owner, and the exact
single-result document owner. The latter derives SHA-256 directly from retained bytes
without decoding or assigning route meaning. Calculation, retained correlation, and
verification own repository location in three distinct typed
requests; location is neither encoded state nor inferred provenance. Calculation and
verification correlate exact encapsulated input bytes with the authenticated repository
input identity before using route metadata. The former aggregate campaign-model route
is retired. Row-044 software evidence establishes this
ownership and the retained input/result content identities only; the retained campaign
numerics remain separately bounded synthetic numerical-verification evidence.

The finite-rank-oracle package separates exact encoded documents from repository
location. Its leaf facade also exposes the exact single-result document owner, which
derives SHA-256 directly from retained bytes without qualifying an oracle. Calculation
and retained correlation receive explicit absolute roots, while independent verification
owns its root in a typed request whose construction performs no filesystem access.
Executing operations bind encapsulated and repository input bytes
to declared provenance before using the input-owned energy unit, authenticate the
periodic parent plus the matched and route-reconciliation results, then compare a
Bloch-fiber resolvent root
with an independent site-space eigensolve. Twenty attractive controls and four boundary
controls preserve root, residual, energy, projector, degeneracy, and unequal-rank
channels. Canonical correlation and independent reconstruction remain distinct. The
name denotes this bounded analytical comparison route, not a generic oracle engine,
production qualification mechanism, infinite-system theorem, or material result.

The continuum-refinement package keeps five operations separate; see
:doc:`periodic1d-continuum-refinement` for the represented operators, scale convention,
profile normalizations, numerical diagnostics, frozen decisions, and scientific
reasoning. The operations are continuum-mesh
refinement at fixed domain and profile, continuum-domain refinement at fixed spectral
spacing and profile, lattice-supercell refinement at fixed lattice spacing and
profile, lattice-scale refinement at fixed physical domain and profile, and comparison
of fixed-integrated and fixed-peak profile-width families. Its leaf facade exposes the
exact single-result document owner, which derives content identity without decoding or
assigning continuum meaning. Its 31 records retain binding energy, bound-state count,
projector, compressed-operator, cross-coupling,
Brillouin-edge, and boundary-probability channels without combining the distinct error
axes. The independent verifier reconstructs those records without importing the
maintained Workflow. The bounded lattice-scale criteria pass over the tested sequence,
but neither profile family establishes a profile-defined continuum crossover over the
tested width domain. No integration step reruns or rewrites a retained artifact.

Evidence limitation
-------------------

These capabilities use controlled represented parents and planted perturbations.  A
passing workflow or verifier establishes only its stated software or numerical
contract.  It does not establish silicon behavior, dopant physics, DFT convergence,
production Wannier behavior, transferability, scientific validation, or uncertainty
quantification.
