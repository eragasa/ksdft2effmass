Periodic-1D route-reconciliation campaign
=========================================

``ksdft2effmass.periodic1d.campaign.reconciliation.route`` is the canonical
owner of the retained synthetic independent-route campaign.  Its leaf and
``reconciliation`` parent facades expose only the encoded documents, exact result
document, and campaign entry point.  Lower-level contracts and route Actions
remain in their defining modules.

The site-space route assembles the finite twisted parent before subtraction.  The
folded-fiber route independently evaluates primitive Bloch fibers and constructs
the discrete folding map.  Both receive the same authenticated hopping blocks,
raw candidate, explicit candidate-to-reference unitary, and scalar energy-reference
shift.  Agreement therefore establishes a bounded algebraic commutativity result,
not independent physical evidence.

Mismatched parent truncation, domains, coordinate weights, and alignment maps are
kept distinct.  Unsupported comparisons stop before subtraction; paired
reconciliation records proceed only after a common parent/domain, explicit dual
and metric, or relative unitary is supplied.

Exact documents and facade
--------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.reconciliation.route.encoded_documents
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.reconciliation.route.result_documents
   :members:
   :show-inheritance:
   :no-index:

.. automodule:: ksdft2effmass.periodic1d.campaign.reconciliation.route.campaign
   :members:
   :show-inheritance:
   :no-index:

Typed controls, alignment, and numerical routes
-----------------------------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.reconciliation.route.workflow
   :members:
   :show-inheritance:
   :no-index:

Independent verification
------------------------

.. automodule:: ksdft2effmass.periodic1d.campaign.reconciliation.route.verification
   :members:
   :show-inheritance:
   :no-index:

Scientific and computational limits
-----------------------------------

The retained inputs and results are synthetic.  Passing tests do not establish
material adequacy, continuum or infinite-volume convergence, transferability,
uncertainty quantification, or acceptance.  Dense matrix products, eigensolves,
and singular-value computations have cubic time and quadratic storage scaling in
represented dimension.  No arbitrary size cap is imposed, so allocation can
raise ``MemoryError``.  SHA-256 establishes exact content identity only.  This
campaign performs no Quantum ESPRESSO or Wannier90 execution.
