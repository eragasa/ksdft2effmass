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
not public software names.  The maintained package groups each capability beneath
``ksdft2effmass.campaigns.research_monograph.periodic_1d.defects``.  Reusable
controlled systems extracted from those capabilities live separately beneath
``periodic_1d.model.toy_defects`` so campaign provenance and acceptance policy do not
become properties of a toy Hamiltonian.

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
The blind-alignment package currently provides strict version-one input and result
adaptation, authenticated matched-baseline loading, its typed observation-only
inference core, canonical result encoding, identity-only retained correlation, and
complete typed campaign composition.  Its supported package route is deliberately
limited to an immutable campaign model and an encapsulating campaign façade; lower-level
records and Actionizers remain in defining modules rather than being re-exported.  Its
independent verifier authenticates all direct and transitive sources and reconstructs
all retained exact, sensitivity, gauge, stop, and boundary-diagnostic records without
importing the maintained calculation algorithms.  This completes the maintained
software and numerical-verification slice for blind alignment while leaving all
material-validation and uncertainty claims explicitly excluded.
The remaining three capabilities likewise stay authoritative in their calculation
packages until their corresponding maintained package slices meet the same typed,
independently verified contract.  No integration step reruns or rewrites a retained
artifact.

Evidence limitation
-------------------

These capabilities use controlled represented parents and planted perturbations.  A
passing workflow or verifier establishes only its stated software or numerical
contract.  It does not establish silicon behavior, dopant physics, DFT convergence,
production Wannier behavior, transferability, scientific validation, or uncertainty
quantification.
