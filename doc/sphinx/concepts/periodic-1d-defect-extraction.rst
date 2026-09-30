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

Retained evidence
-----------------

The version-one inputs and results beneath ``calculations/research-monograph`` are
immutable evidence records.  Maintained deserializers enforce their exact schema,
units, ordering, source identities, and finite-value requirements.  Maintained
workflows may calculate a new result at a new path, while retained-result verifiers
independently reconstruct the bounded synthetic diagnostics.  Correlation with a
retained artifact establishes identity and consistency, not numerical verification by
itself.

The matched known-map capability is the first maintained package integration.  The
remaining four retained capabilities stay authoritative in their calculation
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
