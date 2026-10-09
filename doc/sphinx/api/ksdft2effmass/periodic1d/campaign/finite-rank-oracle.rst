Periodic-1D finite-rank-oracle campaign
=======================================

``ksdft2effmass.periodic1d.campaign.oracle.finite_rank`` is the canonical
owner of one retained synthetic finite-rank comparison.  Its leaf and ``oracle``
parent facades expose only the encoded documents, exact result document, and
campaign entry point.  Lower-level contracts, numerical Actions, and independent
reconstruction remain in their defining modules.

“Oracle” names a qualified analytical route for this finite evidence class and
validity domain.  The route compares a rank-one Bloch-resolvent secular solution
with a separately assembled finite site-space eigensolve.  It is not a generic
oracle engine, an infinite-system theorem, a continuum-limit result, a material
model, uncertainty quantification, or an acceptance mechanism.

Exact documents and facade
--------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.encoded_documents
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.result_documents
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.campaign
   :members:
   :show-inheritance:
   :no-index:

Contracts and strict input adaptation
-------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.contracts
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.input_decoding
   :members:
   :show-inheritance:
   :no-index:

Authenticated parent and maintained numerical routes
----------------------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.parent_data
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.numerical_actions
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.comparison
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.workflow
   :members:
   :show-inheritance:
   :no-index:

Independent reconstruction and verification
-------------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.independent_reconstruction
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.oracle.finite_rank.verification
   :members:
   :show-inheritance:
   :no-index:

Computational boundary
----------------------

Finite dense eigensolves and matrix products have cubic time and quadratic
storage scaling in represented dimension.  No arbitrary size cap is imposed, so
allocation can raise ``MemoryError``.  SHA-256 establishes exact content identity
only.  The campaign consumes retained compact sources and performs no Quantum
ESPRESSO or Wannier90 execution.
