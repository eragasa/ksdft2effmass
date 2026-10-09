Solid-state lattice models API
==============================

The root ``ksdft2effmass.solid_state`` facade exposes its reviewed composite lattice
surface. Finite Wigner--Seitz interpolation is owned by
``ksdft2effmass.solid_state.wignerseitz.interpolation``; Löwdin quadratic effective
Hamiltonians are owned by the explicit modules under
``ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic``. Requests,
Results, and Actions from those implementation families are deliberately not flattened
into the root facade.

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
coordinate transformation before construction.  A ``BravaisLattice*D`` record is a
declared classification, not by itself evidence that basis vectors satisfy its metric
invariants.  ``BravaisMetricCompatibilityAnalyzer`` performs that caller-toleranced
check without claiming a unique maximal-symmetry classification.

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

.. autoclass:: BravaisMetricCompatibilityResult
   :members:

.. autoclass:: BravaisMetricCompatibilityAnalyzer
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

Composed ``Lattice1D``, ``Lattice2D``, and ``Lattice3D`` records require correlated
passing duality and Bravais-metric results.  They therefore represent verified
software composition under their retained caller tolerances; they do not establish
scientific validation or a unique Bravais classification.

.. autoclass:: LatticeDualityResult
   :members:

.. autoclass:: LatticeDualityAnalyzer
   :members:

Reciprocal meshes, one-dimensional paths, and band frames
----------------------------------------------------------

The one-dimensional centered reciprocal mesh carries its reciprocal-coordinate unit
and is even and half-open.  The two-dimensional centered mesh uses reduced coordinates
on a half-open primitive reciprocal cell with first-index-outer, second-index-inner
ordering.  Neither mesh supplies electronic-structure integration weights.  The 2D
neighbor and finite-basis sewing Actions remain under
``ksdft2effmass.analysis.model_systems`` and consume the solid-state mesh DataObject.

For ordered one-dimensional plane-wave indices
:math:`n,m\in\{-P,\ldots,P\}`, positive-reciprocal-vector sewing uses
:math:`c_n(k+G)=c_{n+1}(k)` and therefore
:math:`S_{nm}=\delta_{m,n+1}`.  The out-of-cutoff boundary coefficient is discarded,
not wrapped, so the represented matrix has a first superdiagonal of ones and a zero
final row.  This explicit finite-cutoff map is nonunitary and must not be identified
with the exact reciprocal sewing operator on the untruncated parent space.

Reciprocal frame paths retain orthonormality tolerance and endpoint sewing separately.
Polar transport supports scalar and composite frames and reports the minimum overlap
singular value and closure eigenphases.

.. autoclass:: CenteredUniformReciprocalMesh1D
   :members:

.. autoclass:: CenteredUniformReciprocalMesh2D
   :members:

.. autoclass:: PlaneWaveBasis1D
   :members:

.. autoclass:: ReciprocalSewingDirection1D
   :members:

.. autoclass:: PlaneWaveReciprocalSewingResult
   :members:

.. autoclass:: PlaneWaveReciprocalSewingConstructor
   :members:

.. autoclass:: ReciprocalBandFramePath1D
   :members:

.. autoclass:: PolarBandFrameTransportResult1D
   :members:

.. autoclass:: PolarBandFrameTransporter1D
   :members:

.. autoclass:: BandProjectorPathResult1D
   :members:

.. autoclass:: BandProjectorPathConstructor1D
   :members:

.. autoclass:: BandFrameAlignmentResult1D
   :members:

.. autoclass:: BandFrameAligner1D
   :members:

Projectors remove scalar or composite right-unitary gauge choices. Pointwise alignment
uses unitary Procrustes rotations and retains frame and projector defects separately;
it refuses to bridge different reciprocal sewing maps implicitly.

Wilson-loop phase spectra
--------------------------

Wilson eigenphases are stored as unordered, canonical principal-branch multisets.
Their increasing storage order is deterministic but does not identify bands across
spectra. Circular comparison uses an optimal assignment and reports signed residuals,
maximum defect, Euclidean defect, and an explicit tolerance. The center mapping is a
stated phase convention and does not by itself establish polarization or topology.
The phase/center relation follows the geometric-phase framework of `King-Smith and
Vanderbilt (1993) <https://doi.org/10.1103/PhysRevB.47.1651>`_; the broader Wannier
context is reviewed by `Marzari et al. (2012)
<https://doi.org/10.1103/RevModPhys.84.1419>`_.

.. autoclass:: WilsonCenterConvention1D
   :members:

.. autoclass:: WilsonLoopSpectrum1D
   :members:

.. autoclass:: WilsonLoopSpectrumCanonicalizer1D
   :members:

.. autoclass:: WilsonLoopPhaseSetComparisonResult1D
   :members:

.. autoclass:: WilsonLoopPhaseSetComparator1D
   :members:

Projected operators and hopping transforms
------------------------------------------

Reciprocal operator samples carry explicit coordinates, reciprocal period, matrix
unit, and ordering. They are reusable numerical data and do not by themselves state
whether the matrices represent a parent, projected, retained, or reconstructed
operator. That role belongs to the construction result or scientific aggregate that
adds operator identity, basis, gauge, energy reference, and provenance; matrix shape
alone is insufficient. Projection requires an exactly compatible frame path. The
complete Fourier transform uses centered Born--von Karman representatives and retains
its inverse-reconstruction result; interpolation and finite-range truncation remain
separate actions. Scalar bands use one-by-one blocks rather than a separate implicit
scalar convention.

.. autoclass:: ReciprocalOperatorSamples1D
   :members:

.. autoclass:: BandProjectedOperatorPathConstructor1D
   :members:

.. autoclass:: BlockHoppingModel1D
   :members:

.. autoclass:: ReciprocalOperatorFourierTransformResult1D
   :members:

.. autoclass:: ReciprocalOperatorFourierTransformer1D
   :members:

.. autoclass:: BlockHoppingInterpolator1D
   :members:

.. autoclass:: BlockHoppingTruncationResult1D
   :members:

.. autoclass:: BlockHoppingTruncator1D
   :members:

Nearest-neighbor silicon Slater--Koster model
---------------------------------------------

The initial effective-model class is a spinless, orthogonal, ten-orbital
:math:`sp^3s^*` model for diamond silicon.  Its eight-dimensional linear operator
span contains three onsite coefficients and the nearest-neighbor
:math:`ss\sigma`, :math:`sp\sigma`, :math:`s^*p\sigma`, :math:`pp\sigma`, and
:math:`pp\pi` channels.  Other channels are exact exclusions from this model class,
not claims that the corresponding physical contributions vanish.

The real-space representation retains explicit cell displacements and obeys
:math:`H(-R)=H(R)^\dagger`.  Bloch construction accepts primitive reduced coordinates
and applies the declared positive cell Fourier phase.  It does not fit parameters,
infer a Wannier alignment, or establish physical adequacy.

.. autoclass:: SiliconSp3sStarParameter
   :members:

.. autoclass:: SiliconSp3sStarNearestNeighborParameters
   :members:

.. autoclass:: SiliconDiamondSp3sStarNearestNeighborModel
   :members:

.. autoclass:: SiliconSp3sStarOperatorComponent
   :members:

.. autoclass:: SiliconDiamondSp3sStarNearestNeighborOperator
   :members:

.. autoclass:: SiliconDiamondSp3sStarNearestNeighborConstructor
   :members:

.. autoclass:: SiliconSp3sStarBlochHamiltonianSamples
   :members:

.. autoclass:: SiliconSp3sStarBlochHamiltonianConstructor
   :members:

Same-frame Wannier kinetic decomposition
----------------------------------------

The three-dimensional decomposition consumes already identified plane-wave
coefficients, diagonal canonical kinetic energies, parent eigenvalues,
disentanglement matrices, and Wannier gauge matrices.  It constructs the total and
kinetic operators in the identical retained frame before subtraction and retains both
reciprocal-space matrices and canonical finite-mesh lattice blocks.  Native QE and
Wannier90 decoding, artifact authentication, FFT/G-vector conventions, and simulation
provenance remain outside this solid-state action. Inputs and outputs must use physical
energy units. The canonical lattice representation uses the specified normalized
negative-phase forward transform and positive-phase reconstruction. Public result
records recheck the request construction, Fourier correlation, and every retained
diagnostic rather than trusting caller-supplied values.

The difference is explicitly a represented non-kinetic remainder.  It is not thereby
a continuous scalar potential and can contain local, nonlocal pseudopotential,
Hartree, exchange-correlation, and other represented contributions.

.. autoclass:: PlaneWaveBandSample
   :members:

.. autoclass:: WannierFrameSample
   :members:

.. autoclass:: WannierOperatorRole
   :members:

.. autoclass:: WannierKineticDecompositionRequest
   :members:

.. autoclass:: WannierRepresentedOperatorMesh3D
   :members:

.. autoclass:: WannierKineticDecompositionDiagnostics
   :members:

.. autoclass:: WannierKineticDecompositionResult
   :members:

.. autoclass:: WannierKineticDecompositionConstructor
   :members:

Finite Wigner--Seitz interpolation and Cartesian derivatives
-------------------------------------------------------------

An explicit Wigner--Seitz inventory supplies an identified source mesh, direct-lattice
basis, integer representatives, and native degeneracies.  The name refers to Wigner
and Seitz's cell construction
(`doi:10.1103/PhysRev.43.804 <https://doi.org/10.1103/PhysRev.43.804>`_); the
authoritative specification records the complete citation provenance and claim
boundary.  Every modulo-mesh residue
must be represented, and each degeneracy must equal its residue-class multiplicity.
A logarithmic determinant preserves nonsingularity classification across raw
determinant underflow and overflow, while representative components that cannot be
converted exactly to binary64 are rejected before distinct translations can collapse
in phase evaluation.
The same-frame interpolation action lifts the canonical blocks of one
``WannierKineticDecompositionResult`` by residue and evaluates all three operators
with the positive Wannier phase and degeneracy division.  It retains Hermiticity and
``H = T + R`` defects without treating those checks as interpolation convergence or
scientific validation.

The Cartesian derivative action evaluates one represented operator's value, gradient,
and Hessian analytically.  Their units are energy, energy times length, and energy
times length squared.  Public interpolation and derivative Result constructors accept
no precomputed evaluation witness.  Actions own request-to-value derivation and execute
it once; Results validate intrinsic retained relations and diagnostics without replaying
the Action.  Manual Result construction does not establish Action execution or
provenance.  This action does not choose a degenerate subspace, perform a Löwdin
reduction, convert curvature to mass, or infer native-file provenance.

.. currentmodule:: ksdft2effmass.solid_state.wignerseitz.interpolation

.. autoclass:: WignerSeitzInterpolationInventory3D
   :members:

.. autoclass:: WignerSeitzRepresentedOperator3D
   :members:

.. autoclass:: WannierRepresentedOperatorWignerSeitzConstructor3D
   :members:

.. autoclass:: WignerSeitzOperatorInterpolationRequest3D
   :members:

.. autoclass:: WignerSeitzOperatorInterpolationResult3D
   :members:

.. autoclass:: WignerSeitzOperatorInterpolator3D
   :members:

.. autoclass:: WannierKineticWignerSeitzInterpolationRequest3D
   :members:

.. autoclass:: WannierKineticWignerSeitzInterpolationDiagnostics
   :members:

.. autoclass:: WannierKineticWignerSeitzInterpolationResult3D
   :members:

.. autoclass:: WannierKineticWignerSeitzInterpolator3D
   :members:

.. autoclass:: WannierRepresentedOperatorCartesianDerivativeRequest3D
   :members:

.. autoclass:: WannierRepresentedOperatorCartesianDerivativeDiagnostics3D
   :members:

.. autoclass:: WannierRepresentedOperatorCartesianDerivativeResult3D
   :members:

.. autoclass:: WannierRepresentedOperatorCartesianDerivativeConstructor3D
   :members:

Löwdin quadratic effective Hamiltonian
--------------------------------------

The Löwdin quadratic effective-Hamiltonian reduction consumes same-frame Hamiltonian,
kinetic, and represented non-kinetic-remainder derivative results.  The name refers to
Löwdin's class-partition perturbation construction
(`doi:10.1063/1.1748067 <https://doi.org/10.1063/1.1748067>`_); the authoritative
specification records the complete citation provenance and its claim boundary.  The
request explicitly states
an ordered Hamiltonian eigenspace selection, reference energy, degeneracy tolerance,
Hamiltonian-Hermiticity tolerance, and selected-space covariance probe.  A Hamiltonian
outside that tolerance is rejected because it does not define the declared Hermitian
eigenspace and Löwdin complement resolvent.  Within tolerance, the explicitly
Hermitian-projected value supplies the eigenspace and projected base value, and the
result retains the projection correction.  Both gauges in the base-covariance
comparison use that same projected value, so accepted anti-Hermitian content is not
misreported as a covariance defect.  Public reduction and downstream Result
constructors accept no evaluation witness.  Each Action performs request-to-value
derivation once, while Results validate intrinsic retained relations and diagnostics
without replaying the Action.  The result also retains selected and complementary
frames, the
complementary resolvent, direct projected tensors, the total
remote Löwdin term, its kinetic--kinetic, remainder--remainder, and cross-term
partition, and unit-carrying closure and basis-covariance diagnostics.  The retained
covariance-probe base, gradient, and effective-quadratic tensors allow the Result to
validate those diagnostics without a second eigensolve or request-to-reduction pass.
Separate typed actions
evaluate the finite quadratic polynomial at explicit Cartesian reciprocal offsets and
contract its quadratic tensor along explicit normalized Cartesian directions.  They
return unit-carrying matrix families and anti-Hermiticity diagnostics without
performing eigenspectrum interpretation.

This finite matrix construction does not identify a physical band manifold, track
scalar bands through a degeneracy, convert curvature to effective mass, or establish
mesh, interpolation, parent-model, or scientific convergence.

.. currentmodule:: ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.reduction

.. autoclass:: WannierKineticLowdinQuadraticReductionRequest3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticReductionDiagnostics3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticReductionResult3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticReductionConstructor3D
   :members:

.. currentmodule:: ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.evaluation

.. autoclass:: WannierKineticLowdinQuadraticModelEvaluationRequest3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticModelEvaluationDiagnostics3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticModelEvaluationResult3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticModelEvaluator3D
   :members:

.. currentmodule:: ksdft2effmass.solid_state.hamiltonians.effective.lowdin_quadratic.contraction

.. autoclass:: WannierKineticLowdinQuadraticDirectionalContractionRequest3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticDirectionalContractionDiagnostics3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticDirectionalContractionResult3D
   :members:

.. autoclass:: WannierKineticLowdinQuadraticDirectionalContractionConstructor3D
   :members:

Finite lattice geometry
-----------------------

.. currentmodule:: ksdft2effmass.solid_state

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

.. autoclass:: TwistFiber
   :members:

.. autoclass:: TwistGaugeBridgeConvention
   :members:

.. autoclass:: TwistGaugeBridgeResult
   :members:

.. autoclass:: TwistGaugeBridgeConstructor
   :members:

.. autoclass:: TwistGaugeEquivalenceIssueCode
   :members:

.. autoclass:: TwistGaugeEquivalenceResult
   :members:

.. autoclass:: TwistGaugeEquivalenceAnalyzer
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

Represented finite-lattice operators
------------------------------------

.. autoclass:: ScalarFiniteLatticeOperator
   :members:

.. autoclass:: ScalarFiniteLatticeOperatorCompatibilityIssueCode
   :members:

.. autoclass:: ScalarFiniteLatticeOperatorCompatibilityResult
   :members:

.. autoclass:: ScalarFiniteLatticeOperatorCompatibilityAnalyzer
   :members:

.. autoclass:: ScalarFiniteLatticeOperatorAdder
   :members:

.. autoclass:: ScalarFiniteLatticeRouteReconciliationResult
   :members:

.. autoclass:: ScalarFiniteLatticeRouteReconciliationWorkflow
   :members:

.. autoclass:: TwistedSupercellOperatorConstructor
   :members:

.. autoclass:: LocalizedPerturbationOperatorConstructor
   :members:

.. autoclass:: QuotientSeamOperatorConstructor
   :members:

``ScalarFiniteLatticeOperator`` correlates canonical complex CSR values with scalar
one-state-per-cell geometry, ordering, boundary twist, gauge, basis, unit,
energy-reference, and provenance metadata. Compatibility analysis and sparse addition
require exact shape, twist-fiber, basis, unit, and energy-reference agreement before
arithmetic. Multi-orbital and spin representations remain outside this contract.

This specialized sparse record is not replaced by the general dense
:class:`~ksdft2effmass.operators.OperatorRecord`. Higher-level scientific parent or
retained-operator aggregates may compose it, but those ksdft identities remain outside
PhysKit-owned finite-periodic mechanics. Matrix shape alone does not create that
scientific binding.

Integral lattice operations
---------------------------

Coordinate and displacement transformers accept every represented unimodular integral
operation.  Boundary twists are covectors: a general coordinate transform would
require the contragredient matrix ``M^{-T}``.  The bounded
``BoundaryTwistTransformer`` therefore accepts only signed axis permutations, for
which the represented operation is orthogonal and ``M^{-T} = M``.

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
