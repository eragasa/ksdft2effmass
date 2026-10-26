Quantum model systems
=====================

``ksdft2effmass.model_systems`` contains public analyses for controlled
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

.. currentmodule:: ksdft2effmass.model_systems

``BaseModelSystemAnalyzer`` remains a nominal action type.
``BaseVerification`` enforces final ``to_dict``/``from_dict`` and
``to_json``/``from_json`` representation boundaries for every concrete verification.
``BaseModelAnalysisVerification`` adds the authenticated visualization-data binding.
``BaseModelAnalysisVerifier`` owns the final derive--digest--verify composition so
callers cannot supply projection digests.
``BaseModelAnalysisVisualizationPlotter`` defines the operation that produces one
immutable visualization, while ``BaseModelAnalysisVisualizer`` defines aggregate
visualization over a unique set. ``BaseModelAnalysisVisualization`` is the nominal
value base. Generic PNG values require a cross-platform-safe basename ending exactly
in ``.png`` and decode the supplied bytes before admission.
``BaseModelAnalysisVisualizationData`` and ``BaseModelAnalysisVerification``
separately fix the dictionary and JSON boundaries for immutable verification values;
concrete values implement only their typed mapping.

.. autoclass:: BaseModelSystemAnalyzer
   :members:

.. autoclass:: BaseModelAnalysisVerifier
   :members:

.. autoclass:: BaseModelAnalysisVisualizer
   :members:

.. autoclass:: BaseModelAnalysisVisualizationPlotter
   :members:

.. autoclass:: BaseModelAnalysisVisualization
   :members:

.. autoclass:: BaseModelAnalysisVisualizationData
   :members:

.. autoclass:: ModelAnalysisPngVisualization
   :members:

.. autoclass:: BaseVerification
   :members:

.. autoclass:: BaseModelAnalysisVerification
   :members:

.. autoclass:: ModelAnalysisVerificationResult
   :members:

.. autoclass:: QuadratureVerification
   :members:

.. autoclass:: VisualizationProjectionVerification
   :members:

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
model systems belong to :doc:`operators`. The complete code-to-calculation flow and
represented equations are documented in
:doc:`../concepts/controlled-model-calculations`.

QHO1D
-----

``QHO1D`` is the dimension-specific one-dimensional quantum harmonic oscillator
owner. No dimension-neutral ``QHO`` API or 2D/3D implementation is claimed. The
analysis uses three public mathematical software models of
the same physical oscillator:

* :class:`Qho1dAnalytical` owns exact energies and coordinate-space
  Hermite number states;
* :class:`Qho1dFiniteDifference` applies oscillator physics to a
  reusable :class:`~ksdft2effmass.model_systems.DirichletInterval` and
  composes the centered second-order finite-difference Hamiltonian; and
* :class:`Qho1dLadderOperators` composes
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
:class:`Qho1dNondimensionalizer`, which explicitly attaches
:class:`~ksdft2effmass.operators.Unitless` without asserting that the corresponding
physical quantities are intrinsically dimensionless.

.. currentmodule:: ksdft2effmass.model_systems.qho1d

.. autoclass:: Qho1dNondimensionalizer
   :members:

.. autoclass:: Qho1dParameters
   :members:

.. autoclass:: Qho1dAnalytical
   :members:

.. autoclass:: Qho1dFiniteDifference
   :members:

.. autoclass:: Qho1dLadderOperators
   :members:

.. autoclass:: Qho1dComparisonRequest
   :members:

.. autoclass:: Qho1dComparisonResult
   :members:

.. autoclass:: Qho1dComparator
   :members:

The direct successor surface owns one Python-authored typed configuration, immutable
calculation records, an independent reference route, operation-partitioned
verification, and authenticated visualization. It uses the same shared typed JSON
boundary as PIAB1D; historical ``study`` serialization is not involved.

.. autoclass:: Qho1dConfiguration
   :members:

.. autoclass:: Qho1dSpatialRepresentationResult
   :members:

.. autoclass:: Qho1dSampledStateAlignmentResult
   :members:

.. autoclass:: Qho1dHamiltonianComparisonResult
   :members:

.. autoclass:: Qho1dResidualResult
   :members:

.. autoclass:: Qho1dCaseResult
   :members:

.. autoclass:: Qho1dStateComparisonResult
   :members:

.. autoclass:: Qho1dCalculationResult
   :members:

.. autoclass:: Qho1dAnalyzer
   :members:

The adjacent-grid analyzer compares successive coarse/fine pulled-back Hamiltonians
only after both act in the same retained number-state coordinates. Its Frobenius norm
is a finite-representation change diagnostic, not a continuum error estimate.

.. autoclass:: Qho1dCrossGridComparisonResult
   :members:

.. autoclass:: Qho1dCrossGridAnalysisResult
   :members:

.. autoclass:: Qho1dCrossGridAnalyzer
   :members:

.. autoclass:: Qho1dCrossGridVerification
   :members:

.. autoclass:: Qho1dCrossGridVerifier
   :members:

.. autoclass:: Qho1dIndependentReferenceAnalyzer
   :members:

.. autoclass:: Qho1dSpatialRepresentationVerification
   :members:

.. autoclass:: Qho1dSampledStateAlignmentVerification
   :members:

.. autoclass:: Qho1dHamiltonianComparisonVerification
   :members:

.. autoclass:: Qho1dResidualVerification
   :members:

.. autoclass:: Qho1dStateComparisonVerification
   :members:

``Qho1dSweepVerification`` remains available only to decode the earlier retained
three-component direct verification record.

.. autoclass:: Qho1dSweepVerification
   :members:

.. autoclass:: Qho1dVerification
   :members:

.. autoclass:: Qho1dVerifier
   :members:

.. autoclass:: Qho1dVisualizationPlotEnum
   :members:

.. autoclass:: Qho1dVisualizationData
   :members:

.. autoclass:: Qho1dVisualizer
   :members:

The following classes retain the historical JSON-authored study contract. They do not
participate in direct calculate--verify--render executions. They are maintained for
historical reproduction and compatibility only; new callers must use the direct typed
surface. The non-destructive maintenance and removal gates are recorded in
``docs/architecture/v3/ksdft2effmass/model_systems/qho1d/legacy-disposition.md``.

.. autoclass:: Qho1dStudyDefinition
   :members:

.. autoclass:: Qho1dStudyResult
   :members:

.. autoclass:: Qho1dStudyInputDeserializer
   :members:

.. autoclass:: Qho1dStudyEvaluator
   :members:

.. autoclass:: Qho1dStudyResultSerializer
   :members:

.. autoclass:: Qho1dResultVerifier
   :members:

One-dimensional particle in a box
---------------------------------

PhysKit owns the ``Piab1D`` continuum model, analytical solution, homogeneous-
Dirichlet grid, finite-difference Hamiltonian, and eigensolution. KSD owns only the
calculation-specific spectral reduction, residual diagnostics, retained evidence, and
verification composed around that pinned implementation.

.. currentmodule:: ksdft2effmass.model_systems.piab1d

.. autoclass:: Piab1dAnalysis
   :members:

.. autoclass:: Piab1dAnalyzer
   :members:

.. autoclass:: Piab1dDiagnostics
   :members:

.. autoclass:: Piab1dVerification
   :members:

.. autoclass:: Piab1dVerifier
   :members:

.. autoclass:: Piab1dVisualizationPlotEnum
   :members:

.. autoclass:: Piab1dVisualizationData
   :members:

.. autoclass:: Piab1dVisualization
   :members:

.. autoclass:: Piab1dVisualizer
   :members:

``Piab1dAnalyzer`` constructs a set of cohesive diagnostic analyzers and iterates over
that set to produce the complete immutable ``Piab1dDiagnostics`` inventory. There is
no diagnostic facade or factory in this tranche.

Historical retained-result wire objects remain documented with their owning research
monograph campaign API. They are not part of the direct successor calculation surface.

Two-dimensional plane-wave Bloch operators
-------------------------------------------

The reusable periodic2d plane-wave owner uses PhysKit direct and reciprocal lattices,
an explicit finite Fourier inventory, reduced primitive-basis momentum coordinates,
and a caller-toleranced two-pi duality check. The reciprocal-mesh surface adds
centered half-open sampling, explicit positive-neighbor translations, and truncating
finite-basis sewing maps. See
:doc:`ksdft2effmass/model_systems/periodic2d/plane_waves` and
:doc:`ksdft2effmass/model_systems/periodic2d/reciprocal_mesh` for the complete
mathematics, units, ordering, implementation, evidence, and limitation contracts.

.. toctree::
   :hidden:

   ksdft2effmass/model_systems/periodic2d/plane_waves
   ksdft2effmass/model_systems/periodic2d/reciprocal_mesh

One-dimensional periodic Fourier models
---------------------------------------

The periodic-1D model surface retains a finite real Fourier potential, an ordered
plane-wave basis, and two finite representations of a Bloch fiber.  Reduced momentum
is dimensionless in ``[-1/2, 1/2]``.  The plane-wave representation uses the recoil
energy associated with the declared reciprocal vector.  The periodic finite-
difference representation uses a half-open cell grid and a conjugate Bloch seam.
Neither finite matrix is identified with the continuum operator.

The constructors require explicit period or reciprocal-duality tolerances and
compatible energy units.  They do not select bands, construct gauges, run Wannier90,
or apply Appendix G acceptance criteria. Reciprocal frame and hopping operations
belong to :doc:`solid-state`.

.. currentmodule:: ksdft2effmass.model_systems.periodic_1d

.. autoclass:: PeriodicFourierPotential1D
   :members:

.. autoclass:: PeriodicUniformGrid1D
   :members:

.. autoclass:: PlaneWaveFiberHamiltonian1DResult
   :members:

.. autoclass:: PlaneWaveFiberHamiltonian1DConstructor
   :members:

.. autoclass:: PeriodicFiniteDifferenceFiberHamiltonian1DResult
   :members:

.. autoclass:: PeriodicFiniteDifferenceFiberHamiltonian1DConstructor
   :members:
