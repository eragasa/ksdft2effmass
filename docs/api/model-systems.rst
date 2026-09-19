Quantum model systems
=====================

``ksdft2effmass.analysis.model_systems`` contains public analyses for controlled
quantum model systems.  A model system is an idealized physical and mathematical
system used to expose representation, discretization, and reduction behavior under
explicit assumptions.  The term does not imply a toy calculation, and numerical
verification of a model system does not establish scientific validation for a
semiconductor application.

Reusable represented-model components
--------------------------------------

Uniform Cartesian grids retain explicit coordinate units, include both boundary
points, and distinguish complete from interior shapes.  Multidimensional grids are
Cartesian products with fixed ``ij`` indexing and row-major flattening.  A
:class:`DirichletBoundaryCondition` owns the prescribed boundary value independently
of grid geometry. :class:`DirichletInterval` composes those independent spatial and
boundary records without selecting a Hamiltonian or physical model.
:class:`~ksdft2effmass.operators.LadderOperator1D` owns the generic
finite occupation-number basis and exposes its highest-state commutator defect.

.. currentmodule:: ksdft2effmass.analysis.model_systems

.. autoclass:: UniformCartesianGrid1D
   :members:

.. autoclass:: UniformCartesianGrid2D
   :members:

.. autoclass:: UniformCartesianGrid3D
   :members:

.. autoclass:: DirichletBoundaryCondition
   :members:

.. autoclass:: DirichletInterval
   :members:

The reusable ladder and finite-difference operator constructors consumed by these
model systems belong to :doc:`operators`.

Finite harmonic oscillator
--------------------------

The harmonic-oscillator analysis uses three public mathematical software models of
the same physical oscillator:

* :class:`HarmonicOscillatorAnalytical` owns exact energies and coordinate-space
  Hermite number states;
* :class:`HarmonicOscillatorFiniteDifference` applies oscillator physics to a
  reusable :class:`~ksdft2effmass.analysis.model_systems.DirichletInterval` and
  composes the centered second-order finite-difference Hamiltonian; and
* :class:`HarmonicOscillatorLadderOperators` composes
  :class:`~ksdft2effmass.operators.LadderOperator1D` and applies the
  oscillator energy scale.

The comparator samples analytical states on the Dirichlet grid, constructs an
explicit injection by symmetric Gram orthonormalization, pulls the finite-grid
Hamiltonian into retained coordinates, and reports the signed difference from the
ladder Hamiltonian.  The truncated ladder commutator differs from the
infinite-dimensional canonical commutator at the highest retained state.

The finite grid matrix is a canonical CSR numerical representation, not the continuum
differential operator. The comparator materializes it only at the explicit historical
comparison boundary so version-one retained arithmetic remains unchanged. The
comparison therefore keeps finite-boundary, spatial-discretization,
map-conditioning, and retained-space effects conceptually distinct.  Its diagnostics
are not uncertainty estimates or scientific acceptance criteria.

The supported model-system implementation uses public package, module, class, and
method names.  It contains no underscore-prefixed implementation classes or methods;
Python-required special methods retain their language-defined names.

Use the public imports below.

Unit-aware quantities
---------------------

Public model-system values carry immutable typed scalar, vector, dense-matrix, or CSR
sparse-matrix quantities owned by :doc:`operators`.
:class:`~ksdft2effmass.operators.Unitless` is a first-class
unit type, not absent unit metadata. Pint owns unit parsing, dimensional compatibility,
and conversion through :class:`~ksdft2effmass.operators.PintUnitConverter`; project
records own strict value types and immutable array storage. Physical oscillator
parameters retain action, mass, inverse-time, length, wavefunction, and energy
dimensions. The historical normalized study enters through
:class:`HarmonicOscillatorNondimensionalizer`, which explicitly attaches
:class:`~ksdft2effmass.operators.Unitless` without asserting that the corresponding
physical quantities are intrinsically dimensionless.

.. currentmodule:: ksdft2effmass.analysis.model_systems.harmonic_oscillator

.. autoclass:: HarmonicOscillatorNondimensionalizer
   :members:

.. autoclass:: HarmonicOscillatorParameters
   :members:

.. autoclass:: HarmonicOscillatorAnalytical
   :members:

.. autoclass:: HarmonicOscillatorFiniteDifference
   :members:

.. autoclass:: HarmonicOscillatorLadderOperators
   :members:

.. autoclass:: HarmonicOscillatorComparisonRequest
   :members:

.. autoclass:: HarmonicOscillatorComparisonResult
   :members:

.. autoclass:: HarmonicOscillatorComparator
   :members:

One-dimensional particle in a box
---------------------------------

The public particle-in-a-box surface separates continuum spectrum, reusable spatial
interval, and finite-difference representation. Its initial campaign remains the
historical one-dimensional normalized Appendix D experiment.

.. currentmodule:: ksdft2effmass.analysis.model_systems

.. autoclass:: ParticleInBoxParameters
   :members:

.. autoclass:: ParticleInBoxAnalytical
   :members:

.. autoclass:: ParticleInBoxFiniteDifference
   :members:

.. autoclass:: ParticleInBoxGridEvaluation
   :members:

.. autoclass:: ParticleInBoxGridEvaluator
   :members:
