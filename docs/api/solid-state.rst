Solid-state lattice models API
==============================

The supported public import path is ``ksdft2effmass.solid_state``.  This initial
surface owns finite integer lattice geometry, boundary twists, scalar hopping models,
localized scalar perturbations, and explicit integral lattice operations in one, two,
and three spatial dimensions.

These records do not represent atomic Cartesian structures, weighted k-point sampling,
material validation, or a completed finite-domain calculation.  Atomic periodic
geometry remains in ``ksdft2effmass.structures.periodic``; weighted reciprocal sampling
remains in ``ksdft2effmass.electronic_structure``; generic matrix representations
remain in ``ksdft2effmass.operators``.

.. currentmodule:: ksdft2effmass.solid_state

.. automodule:: ksdft2effmass.solid_state

Bravais, direct, and reciprocal lattices
----------------------------------------

Bravais classification factors lattice system from conventional-cell centering.
``P``, ``C``, ``I``, ``F``, and ``R`` therefore remain explicit without introducing
one nominal class for every system--centering pair.  ``C`` is the canonical
base-centered setting; axis-specific ``A`` and ``B`` settings require an explicit
coordinate transformation before construction.

.. autoclass:: BravaisCentering
   :members:

.. autoclass:: LatticeSystem1D
   :members:

.. autoclass:: LatticeSystem2D
   :members:

.. autoclass:: LatticeSystem3D
   :members:

.. autoclass:: BravaisLattice1D
   :members:

.. autoclass:: BravaisLattice2D
   :members:

.. autoclass:: BravaisLattice3D
   :members:

.. autoclass:: DirectLattice1D
   :members:

.. autoclass:: DirectLattice2D
   :members:

.. autoclass:: DirectLattice3D
   :members:

.. autoclass:: ReciprocalLatticeConvention
   :members:

.. autoclass:: ReciprocalLattice1D
   :members:

.. autoclass:: ReciprocalLattice2D
   :members:

.. autoclass:: ReciprocalLattice3D
   :members:

.. autoclass:: Lattice1D
   :members:

.. autoclass:: Lattice2D
   :members:

.. autoclass:: Lattice3D
   :members:

.. autoclass:: LatticeDualityResult
   :members:

.. autoclass:: LatticeDualityAnalyzer
   :members:

Finite lattice geometry
-----------------------

.. autoclass:: LatticeDimension
   :members:

.. autoclass:: LatticeSiteOrdering
   :members:

.. autoclass:: LatticeCoordinate
   :members:

.. autoclass:: LatticeDisplacement
   :members:

.. autoclass:: FiniteLatticeShape
   :members:

.. autoclass:: FiniteLatticeIndexer
   :members:

.. autoclass:: FiniteLatticeCoordinateResolver
   :members:

.. autoclass:: PeriodicImageResult
   :members:

.. autoclass:: PeriodicImageResolver
   :members:

Boundary phases
---------------

.. autoclass:: TwistGaugeRepresentation
   :members:

.. autoclass:: BoundaryTwistLift
   :members:

.. autoclass:: BoundaryTwistRepresentative
   :members:

.. autoclass:: BoundaryTwistReductionResult
   :members:

.. autoclass:: BoundaryTwistReducer
   :members:

.. autoclass:: BoundaryTwistMesh
   :members:

.. autoclass:: BoundaryTwistMeshEnumerator
   :members:

Scalar lattice models
---------------------

.. autoclass:: ScalarHoppingTerm
   :members:

.. autoclass:: ScalarHoppingModel
   :members:

.. autoclass:: LocalizedOnsiteTerm
   :members:

.. autoclass:: LocalizedBondTerm
   :members:

.. autoclass:: LocalizedPerturbation
   :members:

Integral lattice operations
---------------------------

.. autoclass:: IntegralLatticeOperation
   :members:

.. autoclass:: LatticeCoordinateTransformer
   :members:

.. autoclass:: LatticeDisplacementTransformer
   :members:

.. autoclass:: BoundaryTwistTransformer
   :members:

.. autoclass:: LatticeOperationCompatibilityResult
   :members:

.. autoclass:: LatticeOperationCompatibilityAuditor
   :members:
