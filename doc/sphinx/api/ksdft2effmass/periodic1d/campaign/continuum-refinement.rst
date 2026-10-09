Periodic-1D continuum-refinement campaign
==========================================

``ksdft2effmass.periodic1d.campaign.refinement.continuum`` is the canonical
owner of the retained synthetic separated-refinement campaign.  Its leaf and
``refinement`` parent facades expose only the encoded documents, exact result
document, and campaign entry point.  Lower-level contracts and Actions remain in
their defining modules and are documented below without flattening the facade.

The campaign keeps continuum mesh, finite domain, lattice supercell, lattice
scale, and defect-profile family as separate axes.  It also keeps
low-momentum compression, high-momentum coupling, spectra, projectors, and
boundary probabilities as separate diagnostics.  Passing retained comparisons
establishes bounded software and numerical consistency only; it does not prove an
asymptotic continuum limit, material adequacy, transferability, uncertainty
quantification, or scientific acceptance.

Exact documents and facade
--------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.refinement.continuum.encoded_documents
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.refinement.continuum.result_documents
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.refinement.continuum.campaign
   :members:
   :show-inheritance:
   :no-index:

Typed controls and numerical Actions
------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.refinement.continuum.workflow
   :members:
   :show-inheritance:
   :no-index:

Independent verification
------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.refinement.continuum.verification
   :members:
   :show-inheritance:
   :no-index:

Computational boundary
----------------------

Dense eigensolves, matrix products, and singular-value computations have cubic
time and quadratic storage scaling in represented dimension.  No arbitrary size
cap is imposed, so allocation can raise ``MemoryError``.  SHA-256 establishes
exact content identity only.  This campaign performs no Quantum ESPRESSO or
Wannier90 execution.
