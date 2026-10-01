Two-dimensional reciprocal meshes and sewing
==============================================

Purpose and public contract
---------------------------

``ksdft2effmass.analysis.model_systems.periodic2d`` provides explicit reduced
reciprocal meshes, positive-neighbor wrapping, and finite plane-wave coefficient
sewing.  The records are reusable model-system infrastructure pending later PhysKit
migration.  They contain no retained-campaign paths, acceptance policy, or material
interpretation.

The mesh is a finite sampling of a reciprocal primitive cell.  The neighbor result is
a topological relation on that periodic mesh.  The sewing map is a finite matrix acting
on plane-wave coefficient vectors.  These are distinct mathematical objects: mesh
neighbors wrap periodically, while finite plane-wave coefficients shifted beyond the
basis cutoff are discarded rather than wrapped.

Mesh mathematics
----------------

For point counts :math:`N_1,N_2\geq2`, mesh indices
:math:`0\leq i<N_1` and :math:`0\leq j<N_2` identify reduced coordinates

.. math::
   :label: periodic2d-centered-reciprocal-mesh

   \boldsymbol\kappa_{ij}
   = \left(-\frac12+\frac{i}{N_1},
            -\frac12+\frac{j}{N_2}\right).

Points occupy the half-open primitive reciprocal cell
:math:`[-1/2,1/2)\times[-1/2,1/2)` and use first-index-outer,
second-index-inner order.  A positive first-direction neighbor is

.. math::
   :label: periodic2d-first-reciprocal-neighbor

   (i,j)\longmapsto((i+1)\bmod N_1,j),

with reciprocal translation :math:`(1,0)` exactly when :math:`i=N_1-1` and
:math:`(0,0)` otherwise.  The second-direction rule is analogous with translation
:math:`(0,1)`.  The translation :math:`\mathbf t` satisfies

.. math::
   :label: periodic2d-neighbor-translation

   \boldsymbol\kappa_{\mathrm{unwrapped}}
   = \boldsymbol\kappa_{\mathrm{wrapped}} + \mathbf t.

Plane-wave sewing
-----------------

Let :math:`\mathbf e_1=(1,0)` and :math:`\mathbf e_2=(0,1)`.  For the finite square
basis :math:`-M\leq n_1,n_2\leq M`, the coefficient map representing
:math:`\boldsymbol\kappa\mapsto\boldsymbol\kappa+\mathbf e_\alpha` is

.. math::
   :label: periodic2d-plane-wave-sewing-map

   (S_\alpha c)_{\mathbf n}
   = \begin{cases}
       c_{\mathbf n+\mathbf e_\alpha},
       & \mathbf n+\mathbf e_\alpha\text{ lies in the retained basis},\\
       0, & \text{otherwise}.
     \end{cases}

Thus :math:`S_\alpha` is a partial shift, not a unitary permutation.  For a basis side
length :math:`L=2M+1`, each map has rank :math:`L(L-1)`.  The missing boundary sector
records finite-cutoff truncation and must not be repaired by periodic coefficient
wrapping.

Symbols and conventions
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 22 22 18 38

   * - Field or symbol
     - Domain or shape
     - Unit
     - Meaning
   * - ``point_counts``
     - two built-in integers, each at least two
     - unitless
     - Mesh counts along the first and second reciprocal primitive vectors.
   * - :math:`\boldsymbol\kappa_{ij}`
     - two built-in floats
     - reduced reciprocal coordinate
     - Coefficients applied to the PhysKit reciprocal basis matrix :math:`B`.
   * - ``reciprocal_translation``
     - integer pair
     - reciprocal-lattice index
     - Translation restoring the unwrapped positive neighbor.
   * - :math:`S_\alpha`
     - complex ``((2M+1)^2, (2M+1)^2)`` matrix
     - unitless
     - Finite plane-wave coefficient sewing map.

Assumptions, invariants, and exclusions
---------------------------------------

* The positive half-boundary is excluded. Zero is sampled along a direction exactly
  when that direction's point count is even.
* Only positive unit steps along the two primitive reciprocal directions are modeled.
* Reduced coordinates are not Cartesian wave vectors; Cartesian values require
  multiplication by the PhysKit reciprocal primitive-basis matrix.
* The sewing request retains the complete
  :class:`PlaneWaveBlochHamiltonian2DModel`, including basis order and state-space
  identities.
* Neighbor translations are exact integer records.  No floating tolerance is used.
* Sewing matrices are immutable, unitless, and validated element by element.
* This surface does not transport eigenvectors, choose phases, construct Wilson loops,
  compare occupied subspaces, or claim topological convergence.

Algorithm and failure policy
----------------------------

``ReciprocalMeshNeighbor2DConstructor`` advances one integer mesh index, applies
modular wrapping in only the requested direction, and records the corresponding
integer reciprocal translation.  ``PlaneWaveReciprocalSewing2DConstructor`` looks up
each shifted reciprocal index in the model's ordered finite basis and writes one only
when that source coefficient remains represented.

Wrong semantic types raise ``TypeError``.  Out-of-range source indices, odd or trivial
mesh counts, forged translations, incompatible result shapes, nonunitless maps, and
incorrect coefficient shifts raise ``ValueError``.  Strings, booleans, and NumPy
scalar substitutes are not coerced into documented built-in or enum types.

Implementation and evidence mapping
-----------------------------------

* Source:
  ``python/src/ksdft2effmass/analysis/model_systems/periodic2d/reciprocal_mesh.py``
* Software verification:
  ``python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/``
* Plane-wave model contract:
  :doc:`plane_waves`

The tests independently check half-open ordering, ordinary and wrapped neighbors,
integer translations, exact Kronecker-product sewing maps, map rank, nonunitarity,
strict runtime types, result correlation, and rejection of periodic coefficient
wrapping.  These establish software behavior only; they do not establish physical or
scientific validation.

Reference and provenance
------------------------

* Bloch, F., “Über die Quantenmechanik der Elektronen in Kristallgittern,”
  *Z. Phys.* **52**, 555–600 (1929). DOI: ``10.1007/BF01339455``.
* The centered half-open mesh, positive-neighbor translation convention, finite-basis
  ordering, and explicit truncating sewing map are repository-derived contracts.

Limitations
-----------

Only rectangular index meshes in reciprocal primitive coordinates and positive unit
neighbors are represented.  Nonuniform meshes, symmetry reduction, negative or
multi-step navigation, adaptive sampling, transported band frames, and common-space
plane-wave/finite-difference comparison remain outside this slice. Python integers do
not overflow when the total point count is formed, but materializing coordinates or
sewing matrices for very large counts can exhaust available memory; no hidden size cap
or sparse fallback is applied.

Public API
----------

.. currentmodule:: ksdft2effmass.analysis.model_systems

.. autoclass:: PositiveReciprocalDirection2D
   :members:

.. autoclass:: CenteredUniformReciprocalMesh2D
   :members:

.. autoclass:: ReciprocalMeshNeighbor2DRequest
   :members:

.. autoclass:: ReciprocalMeshNeighbor2DResult
   :members:

.. autoclass:: ReciprocalMeshNeighbor2DConstructor
   :members:

.. autoclass:: PlaneWaveReciprocalSewing2DRequest
   :members:

.. autoclass:: PlaneWaveReciprocalSewing2DResult
   :members:

.. autoclass:: PlaneWaveReciprocalSewing2DConstructor
   :members:
