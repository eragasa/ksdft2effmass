Two-dimensional plane-wave Bloch operators
==========================================

Purpose and public contract
---------------------------

``ksdft2effmass.analysis.model_systems.periodic2d`` provides a reusable finite
plane-wave representation of a spinless scalar two-dimensional periodic operator.
PhysKit owns the primitive direct and reciprocal lattices.  The local model-system
surface owns the finite reciprocal cutoff, Fourier coefficient inventory, momentum
fiber, energy scale, represented matrix, and direct--reciprocal compatibility check.
It is intentionally independent of retained periodic2d campaign bytes and acceptance
policy so the capability can later migrate to PhysKit.

The modeled subject is a scalar particle in a periodic potential.  The mathematical
object is one Bloch fiber of a continuum periodic operator.  The numerical
representation is a finite complex matrix in an ordered reciprocal basis.  The
software owner is :class:`PlaneWaveBlochHamiltonian2DConstructor`.

Mathematics
-----------

Let the columns of :math:`A` be direct primitive vectors and the columns of
:math:`B` be reciprocal primitive vectors.  The two-pi dual convention is

.. math::
   :label: periodic2d-plane-wave-duality

   A^{\mathsf T} B = 2\pi I.

For reduced reciprocal coordinates :math:`\boldsymbol\kappa`, reciprocal integer
indices :math:`\mathbf n,\mathbf n'\in\mathbb Z^2`, kinetic scale
:math:`E_{\mathrm K}`, and Fourier coefficients :math:`V_{\mathbf m}`, the
represented matrix is

.. math::
   :label: periodic2d-plane-wave-matrix

   H_{\mathbf n'\mathbf n}(\boldsymbol\kappa)
   = E_{\mathrm K}
     \left\lVert B(\boldsymbol\kappa+\mathbf n)\right\rVert^2
     \delta_{\mathbf n'\mathbf n}
     + V_{\mathbf n'-\mathbf n}.

Reduced coordinates are coefficients in the reciprocal primitive basis; they are not
Cartesian wave-vector components.  The finite square cutoff
:math:`-M\leq n_1,n_2\leq M` uses ``p``-outer, ``q``-inner order.  A real represented
potential requires

.. math::
   :label: periodic2d-plane-wave-reality

   V_{-\mathbf m}=V_{\mathbf m}^{*}.

Symbols, units, domains, and ordering
-------------------------------------

.. list-table::
   :header-rows: 1
   :widths: 18 24 18 40

   * - Symbol or field
     - Domain or shape
     - Unit
     - Meaning
   * - :math:`A`
     - real ``(2, 2)`` matrix
     - PhysKit lattice coordinate unit
     - Direct primitive vectors stored as columns.
   * - :math:`B`
     - real ``(2, 2)`` matrix
     - reciprocal coordinate unit
     - Reciprocal primitive vectors stored as columns.
   * - :math:`\boldsymbol\kappa`
     - two built-in floats
     - reduced reciprocal coordinate
     - Bloch momentum coefficients in basis :math:`B`.
   * - :math:`\mathbf n=(p,q)`
     - integer pair
     - unitless
     - Reciprocal basis index, ordered with ``p`` outer and ``q`` inner.
   * - :math:`M`
     - nonnegative built-in integer
     - unitless
     - Symmetric reciprocal cutoff.
   * - :math:`E_{\mathrm K}`
     - positive finite scalar
     - declared energy unit
     - Scale multiplying squared reciprocal-vector magnitude.
   * - :math:`V_{\mathbf m}`
     - finite built-in complex
     - same energy unit as :math:`E_{\mathrm K}`
     - Potential Fourier coefficient at integer transfer :math:`\mathbf m`.
   * - :math:`H`
     - complex ``((2M+1)^2, (2M+1)^2)`` matrix
     - declared energy unit
     - Finite represented Bloch operator.

Assumptions, invariants, and exclusions
---------------------------------------

* ``DirectLattice2D`` and ``ReciprocalLattice2D`` come from
  ``projectkoios.physkit.periodic.lattice``.
* The model is spinless and scalar.  It has one explicit state-space identifier, basis
  identifier, and energy-reference identifier.
* Fourier transfers are sorted, unique, and exactly conjugate symmetric.  Missing
  transfers represent exact zero.
* The lattice arrays are finite and linearly independent under their PhysKit
  contracts.  Their mutual duality is checked separately by the constructor.
* The kinetic scale converts the numerical squared reciprocal norm to the declared
  energy unit.  The pinned PhysKit lattice records do not themselves carry physical
  units.
* No eigensolver, band selection, basis sewing, gauge alignment, hopping transform,
  truncation comparison, Wannierization, DFT execution, scientific validation, or
  uncertainty quantification is included.

Algorithm and data flow
-----------------------

#. Validate the immutable model and request records.
#. Compute :math:`A^{\mathsf T}B-2\pi I` and its maximum absolute component.
#. Reject a lattice pair whose residual exceeds the caller's absolute tolerance.
#. Fill each matrix element with :math:`V_{\mathbf n'-\mathbf n}` in declared basis
   order.
#. Map every reduced vector :math:`\boldsymbol\kappa+\mathbf n` through :math:`B` and
   add its kinetic contribution to the corresponding diagonal.
#. Copy the finite matrix into immutable ``complex128`` storage carrying the model's
   energy unit.

Tolerance and numerical-failure policy
--------------------------------------

The caller owns ``duality_absolute_tolerance``.  It is finite, nonnegative, and
applied inclusively to the maximum absolute component of the dimensionless duality
residual.  No tolerance is used to repair lattice data, symmetrize Fourier
coefficients, or alter matrix entries.  Nonfinite public scalars and coefficients are
rejected.  The implementation uses binary64 real and complex arithmetic; very large
lattice or kinetic values can overflow and are not silently interpreted as valid
operators.

Serialization and compatibility
--------------------------------

This slice defines no serialized wire format.  Equal matrix dimensions do not imply
compatibility.  A complete comparison must also establish matching state-space,
basis-order, lattice, momentum, energy-unit, energy-reference, spin, and gauge
conventions.

Implementation and evidence mapping
-----------------------------------

* Source: ``python/src/ksdft2effmass/analysis/model_systems/periodic2d/plane_waves.py``
* Software verification:
  ``python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/``
* Numerical verification:
  ``python/tests/numerical_verification/ksdft2effmass/analysis/model_systems/periodic2d/test__PlaneWaveBlochHamiltonian2DConstructor.py``
* Campaign adapter:
  ``python/src/ksdft2effmass/campaigns/periodic2d/model/toy_models/cosine.py``

Software-verification tests cover strict runtime types, deterministic ordering,
Fourier conjugate symmetry, result correlation, dimensions, units, and immutability.
The numerical tests use rectangular and skew lattices with analytically known
reciprocal maps, a constant potential, and a complex conjugate Fourier pair.  They
check column-vector geometry, kinetic scaling, transfer orientation, and Hermiticity.
These checks establish only their documented software and numerical claims.  They do not validate a material model or retained
scientific result.

Reference and provenance
------------------------

* Bloch, F., “Über die Quantenmechanik der Elektronen in Kristallgittern,”
  *Z. Phys.* **52**, 555–600 (1929). DOI: ``10.1007/BF01339455``.
* The finite matrix convention, ordering, strict runtime boundary, and migration-ready
  ownership decomposition are repository-derived contracts documented on this page.

Limitations and unresolved risks
--------------------------------

The current model supports only a square reciprocal-index cutoff, one scalar kinetic
scale, and finite Fourier inventories.  PhysKit lattice objects at the pinned revision
do not attach units to primitive vectors, so callers must keep their coordinate and
kinetic-scale convention consistent.  No condition estimator is reported for nearly
singular primitive bases beyond PhysKit's lattice construction checks.  Reciprocal
sewing and transported finite-difference comparison remain separate parity work.

Public API
----------

.. currentmodule:: ksdft2effmass.analysis.model_systems

.. autoclass:: PlaneWaveFourierCoefficient2D
   :members:

.. autoclass:: PlaneWaveBlochHamiltonian2DModel
   :members:

.. autoclass:: PlaneWaveBlochHamiltonian2DRequest
   :members:

.. autoclass:: PlaneWaveBlochHamiltonian2DResult
   :members:

.. autoclass:: PlaneWaveBlochHamiltonian2DConstructor
   :members:
