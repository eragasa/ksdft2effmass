Solid-state lattice models API
==============================

The supported public import path is ``ksdft2effmass.solid_state``.  This initial
surface owns finite integer lattice geometry, boundary twists, dimension-specific
reciprocal meshes, one-dimensional reciprocal paths and band frames, scalar and block
hopping models, localized scalar perturbations, and explicit integral lattice
operations in one, two, and three spatial
dimensions.

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
