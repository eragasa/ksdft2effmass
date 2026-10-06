Two-dimensional finite-difference Bloch operators
=================================================

Purpose and ownership
---------------------

``ksdft2effmass.analysis.model_systems.periodic2d`` owns a reusable centered finite-
difference representation of a spinless scalar Bloch operator on a square
dimensionless periodic cell. The reusable owner fixes the finite coordinate basis,
normalization, grid ordering, energy unit, energy reference, source/operator/state-
space identities, and construction provenance. The cosine-model constructor is an
adapter over this Action rather than a second matrix-assembly implementation.

This is a finite represented operator. It is not the continuum operator, a nominal
scientific model, a retained operator, or a campaign conclusion.

Mathematics and conventions
---------------------------

For coordinate period :math:`L`, odd grid size :math:`N`, and spacing
:math:`h=L/N`, the half-open grid is

.. math::

   x_i=y_i=\frac{iL}{N},\qquad 0\leq i<N.

The finite state space is :math:`\mathbb C^{N^2}` with Euclidean-orthonormal site
vectors ordered ``x_outer_y_inner``. The Action represents

.. math::

   H_h(\boldsymbol\kappa)
   = -E_K(\Delta_{h,x}^{\kappa_x}+\Delta_{h,y}^{\kappa_y})+V_h.

Each one-dimensional negative-Laplacian block has diagonal :math:`2E_K/h^2`, nearest-
neighbor entry :math:`-E_K/h^2`, last-to-first positive-direction phase
:math:`\exp(+i\kappa_dL)`, and conjugate reverse seam. The two-dimensional kinetic
matrix is the Kronecker sum in the declared site order. ``potential_samples`` is an
immutable real ``(N, N)`` quantity in the same energy unit as ``kinetic_scale``.

Contract and failure policy
---------------------------

* ``coordinate_period`` is a positive finite built-in float.
* ``points_per_direction`` is an odd built-in integer of at least five.
* The basis identity, source identity, operator identity, state-space identity,
  energy reference, and provenance identity are nonempty strings supplied by the
  caller; none is inferred from array shape or names.
* Reduced-momentum components are finite built-in floats in the dimensionless
  reciprocal coordinates dual to the square period.
* Potential shape and unit must agree exactly with the basis and kinetic scale.
* Grid spacing and squared spacing, :math:`E_K/h^2`, :math:`4E_K/h^2+V_{ij}`, and
  each seam argument :math:`\kappa_dL` must remain representable as finite binary64
  values. Range failure raises ``OverflowError`` before an invalid matrix is returned.
* The result matrix must have the declared dimension and unit and be exactly
  Hermitian.
* Stored arrays are copied into immutable canonical binary64/complex128 storage.

The dense represented matrix has dimension :math:`N^2` and storage scaling
:math:`O(N^4)`. The Action imposes no arbitrary grid cap; an unsatisfied dense
allocation propagates as ``MemoryError``. The current contract is intentionally
bounded to a square dimensionless coordinate cell and a centered second-order
stencil. It does not claim a general curvilinear, nonorthogonal, finite-element, or
physical-length discretization.

Cosine adapter
--------------

``Periodic2DFiniteDifferenceHamiltonianConstructor`` samples the exact cosine parent on
the existing period-``2*pi`` half-open grid, binds ``Unitless`` kinetic and potential
quantities, declares the model energy zero and represented identities, and delegates
the only matrix assembly algorithm to
``FiniteDifferenceBlochHamiltonian2DConstructor``. It returns the original campaign
request with the represented matrix, preserving grid order and seam direction.

Evidence and claim boundary
---------------------------

Software tests are split by public evidence owner using
``test__ClassName__construction.py``. They cover strict scalar types, positive finite
periods, odd grid extent, explicit identity, spacing underflow, potential/grid shape,
energy-unit correlation, squared-spacing and stencil range failures, composed-diagonal
overflow, finite seam arguments, result dimension, exact Hermiticity, and immutable
storage. Numerical constructor evidence uses
``test__FiniteDifferenceBlochHamiltonian2DConstructor__execute.py`` and analytic
stencil entries to check kinetic scaling, ``x_outer_y_inner`` flattening, directed
Bloch seams, structural zeros, exact Hermiticity, request identity, and immutable
storage with complex absolute tolerance ``2e-15`` where roundoff applies. Existing
cosine adapter tests additionally check exact request retention, seam entries, and
bitwise equality to the established matrix formula.

The class architecture pages link ``tests.py`` to these single canonical pytest
sources by relative symlink; no assertions are duplicated under documentation. These
tests establish bounded software and numerical behavior only. They do not establish
finite-difference convergence, continuum accuracy, physical adequacy, scientific
validation, uncertainty quantification, or acceptance.

Implementation and evidence paths
---------------------------------

* Source: ``python/src/ksdft2effmass/analysis/model_systems/periodic2d/finite_differences.py``
* Adapter: ``python/src/ksdft2effmass/periodic2d/model/toy_models/cosine.py``
* Software tests: ``python/tests/software_verification/ksdft2effmass/analysis/model_systems/periodic2d/``
* Numerical tests: ``python/tests/numerical_verification/ksdft2effmass/analysis/model_systems/periodic2d/``
* Campaign adapter tests: ``python/tests/ksdft2effmass/periodic2d/model/toy_models/``

Public API
----------

.. currentmodule:: ksdft2effmass.analysis.model_systems

.. autoclass:: UniformPeriodicCoordinateBasis2D
   :members:

.. autoclass:: FiniteDifferenceBlochHamiltonian2DModel
   :members:

.. autoclass:: FiniteDifferenceBlochHamiltonian2DRequest
   :members:

.. autoclass:: FiniteDifferenceBlochHamiltonian2DResult
   :members:

.. autoclass:: FiniteDifferenceBlochHamiltonian2DConstructor
   :members:
