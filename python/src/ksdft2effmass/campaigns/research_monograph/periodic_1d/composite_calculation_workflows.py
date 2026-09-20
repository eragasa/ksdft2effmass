r"""Execution-local calculation Workflow for the Appendix G composite-band study.

The Workflow calculates the demonstrated two-band composite channels from explicit
in-memory controls. It constructs finite plane-wave parent fibers, sampled gaps,
polar-transported frames, controlled and rough gauge transformations, projectors,
Wilson spectra, represented reciprocal operators, complete block hoppings, finite-range
errors, and direct-fit route comparisons. It composes the reusable public model,
solid-state, and analysis owners rather than reading retained result bytes.

All quantities use the Appendix G dimensionless convention ``a = 2 pi``, ``G = 1``,
and ``E_G = 1``. Parent-representation error, reciprocal sampling, external isolation,
gauge covariance, transform reconstruction, truncation, withheld error, and route
comparison remain separate represented channels. Wilson spectra are unordered phase
multisets and do not establish polarization or topology.

The Workflow performs no filesystem discovery, retained-result access, external
execution, Wannier90 localization, material validation, or uncertainty quantification.

The numerical route follows the cited literature only at the level stated here:
plane-wave discretization supplies finite Hermitian parent matrices [1]_, SVD-based
unitary polar factors define neighboring-frame transport [2]_, Wilson phases retain
the closed-loop spectral information without a polarization claim [3]_ [4]_, a
normalized FFT evaluates the complete uniform-mesh Fourier transform [5]_, and dense
SVD/least-squares algorithms support alignment and the direct fitting route [6]_.
SHA-256 artifact identities follow the byte-level hash standard [7]_ and establish
representation identity only.

References
----------
.. [1] Payne, M. C. et al. (1992), "Iterative minimization techniques for
   *ab initio* total-energy calculations: molecular dynamics and conjugate
   gradients," *Reviews of Modern Physics* 64, 1045--1097.
   https://doi.org/10.1103/RevModPhys.64.1045
.. [2] Higham, N. J. (1986), "Computing the Polar Decomposition---with
   Applications," *SIAM Journal on Scientific and Statistical Computing* 7,
   1160--1174. https://doi.org/10.1137/0907079
.. [3] King-Smith, R. D. and Vanderbilt, D. (1993), "Theory of polarization of
   crystalline solids," *Physical Review B* 47, 1651--1654.
   https://doi.org/10.1103/PhysRevB.47.1651
.. [4] Marzari, N. et al. (2012), "Maximally localized Wannier functions: Theory
   and applications," *Reviews of Modern Physics* 84, 1419--1475.
   https://doi.org/10.1103/RevModPhys.84.1419
.. [5] Cooley, J. W. and Tukey, J. W. (1965), "An algorithm for the machine
   calculation of complex Fourier series," *Mathematics of Computation* 19,
   297--301. https://doi.org/10.1090/S0025-5718-1965-0178586-1
.. [6] Golub, G. H. and Van Loan, C. F. (2013), *Matrix Computations*, fourth
   edition, Johns Hopkins University Press.
.. [7] National Institute of Standards and Technology (2015), *Secure Hash
   Standard (SHS)*, FIPS PUB 180-4. https://doi.org/10.6028/NIST.FIPS.180-4
"""

from __future__ import annotations

import hashlib

import numpy as np
import numpy.typing as npt

from ksdft2effmass.analysis.hopping_diagnostics import (
    BlockHoppingHermiticityAnalyzer1D,
)
from ksdft2effmass.analysis.hopping_fits import (
    BlockHoppingLeastSquaresFitter1D,
    BlockHoppingModelComparator1D,
)
from ksdft2effmass.analysis.model_systems.periodic_1d import (
    PeriodicFourierPotential1D,
    PlaneWaveFiberHamiltonian1DConstructor,
)
from ksdft2effmass.analysis.periodic_bands import (
    BandApproximationErrorAnalyzer1D,
    BandGapAnalyzer1D,
    BandSpectrumSamples1D,
)
from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    MatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import (
    BandFrameAligner1D,
    BandProjectedOperatorPathConstructor1D,
    BandProjectorPathConstructor1D,
    BandProjectorPathResult1D,
    BlockHoppingInterpolator1D,
    BlockHoppingModel1D,
    BlockHoppingTruncator1D,
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
    PlaneWaveReciprocalSewingConstructor,
    PolarBandFrameTransporter1D,
    ReciprocalBandFramePath1D,
    ReciprocalOperatorFourierTransformer1D,
    ReciprocalOperatorSamples1D,
    WilsonLoopPhaseSetComparator1D,
    WilsonLoopSpectrumCanonicalizer1D,
)

from .composite import (
    Periodic1DRetainedBandGroup,
)
from .composite_calculation import (
    Periodic1DCompositeBandCalculationGroupResult,
    Periodic1DCompositeBandCalculationRequest,
    Periodic1DCompositeBandCalculationResult,
    Periodic1DCompositeParentCalculationResult,
)
from .composite_results import (
    Periodic1DCompositeArtifactIdentities,
    Periodic1DCompositeBandGroupResult,
    Periodic1DCompositeBandIsolationResult,
    Periodic1DCompositeDirectRouteComparisonResult,
    Periodic1DCompositeExternalIsolationStatus,
    Periodic1DCompositeGaugeComparisonResult,
    Periodic1DCompositeHoppingRangeResult,
    Periodic1DCompositeHoppingRepresentationResult,
    Periodic1DCompositeWilsonGroupResult,
)

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexArray3 = npt.NDArray[np.complex128]
type RealMatrix = npt.NDArray[np.float64]
type RealVector = npt.NDArray[np.float64]


class Periodic1DCompositeBandCalculationWorkflow:
    """Calculate the demonstrated direct composite-band Appendix G channels.

    The Workflow orchestrates existing model, solid-state, and analysis owners. It
    first calculates one finite plane-wave parent representation, then evaluates
    every requested contiguous two-band group against that same parent. The result
    preserves source, transported, controlled-gauge, aligned, and rough-gauge paths
    so that gauge covariance, hopping locality, truncation, withheld interpolation,
    and direct-fit agreement remain independently inspectable.

    Notes
    -----
    All represented energies and reciprocal coordinates are dimensionless in the
    Appendix G convention ``E_G = G = 1`` and ``a = 2 pi``. The polar-transport
    route uses SVD unitary polar factors in the sense of Higham (1986,
    https://doi.org/10.1137/0907079). Wilson eigenphases are stored as unordered
    principal-branch multisets; no stored ordering denotes band correspondence.

    This Workflow performs a finite represented calculation. It does not estimate
    plane-wave cutoff error, validate a material model, localize Wannier functions,
    quantify uncertainty, or infer polarization or topology.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DCompositeBandCalculationRequest
    ) -> Periodic1DCompositeBandCalculationResult:
        """Calculate parent fibers, group gauges, hoppings, and diagnostics.

        Parameters
        ----------
        request
            Immutable calculation definition and operation-specific tolerances. The
            reciprocal training mesh must be even, the withheld mesh must contain at
            least as many points, and every retained group must contain two bands.

        Returns
        -------
        Periodic1DCompositeBandCalculationResult
            Parent calculation and one complete result for each requested group, in
            the request's deterministic group order.

        Raises
        ------
        TypeError
            If ``request`` is not the exact request type.
        ValueError
            If a mesh or retained-group invariant is violated, or if a composed
            numerical owner rejects inconsistent dimensions, units, or tolerances.

        Notes
        -----
        All groups share the same parent matrices and eigenspaces. This prevents a
        group-specific parent discretization from being mistaken for a difference
        caused by band selection or gauge treatment.
        """

        if type(request) is not Periodic1DCompositeBandCalculationRequest:
            raise TypeError("request must be Periodic1DCompositeBandCalculationRequest")
        if request.definition.reciprocal_mesh_size % 2 != 0:
            raise ValueError("reciprocal_mesh_size must be even")
        if (
            request.definition.withheld_mesh_size
            < request.definition.reciprocal_mesh_size
        ):
            raise ValueError("withheld mesh must not be smaller than training mesh")
        if any(
            group.band_count != 2 for group in request.definition.retained_band_groups
        ):
            raise ValueError("the demonstrated composite calculation requires pairs")
        # Construct the parent once so every retained group is compared on an
        # identical reciprocal mesh, basis cutoff, and eigenproblem realization.
        parent = self.calculate_parent(request)
        groups = tuple(
            self.calculate_group(request, parent, group)
            for group in request.definition.retained_band_groups
        )
        return Periodic1DCompositeBandCalculationResult(request, parent, groups)

    def calculate_parent(
        self, request: Periodic1DCompositeBandCalculationRequest
    ) -> Periodic1DCompositeParentCalculationResult:
        """Calculate training parent fibers, eigenspaces, and withheld eigenvalues.

        Parameters
        ----------
        request
            Composite calculation request. Its definition supplies the plane-wave
            cutoff, potential strength, training mesh, withheld mesh, and retained
            group indices.

        Returns
        -------
        Periodic1DCompositeParentCalculationResult
            Complete training matrices, lowest required eigensystem, reciprocal
            sewing map, and the separately sampled withheld eigenvalues.

        Raises
        ------
        TypeError
            If ``request`` is not the exact request type.
        ValueError
            If the finite basis cannot provide the retained bands plus the external
            upper-gap band, or if a composed owner rejects incompatible values.

        Notes
        -----
        The training mesh is half-open and centered, matching a complete discrete
        Fourier period. The endpoint-inclusive withheld mesh is deliberately not
        used to construct hopping coefficients; it tests interpolation away from the
        training nodes. Plane-wave discretization follows the finite-basis approach
        reviewed by Payne et al. (1992,
        https://doi.org/10.1103/RevModPhys.64.1045).
        """

        if type(request) is not Periodic1DCompositeBandCalculationRequest:
            raise TypeError("request must be Periodic1DCompositeBandCalculationRequest")
        definition = request.definition
        # Appendix G fixes G = E_G = 1; wrapping these scales as quantities keeps
        # unit compatibility explicit at the model-construction boundary.
        reciprocal_period = ScalarQuantity(1.0, Unitless())
        recoil_energy = ScalarQuantity(1.0, Unitless())
        mesh = CenteredUniformReciprocalMesh1D(
            reciprocal_period, definition.reciprocal_mesh_size
        )
        basis = PlaneWaveBasis1D(reciprocal_period, definition.plane_wave_cutoff)
        potential = PeriodicFourierPotential1D(
            definition.period,
            ScalarQuantity(0.0, Unitless()),
            VectorQuantity(
                np.asarray(
                    [definition.potential_strength_over_recoil.magnitude],
                    dtype=np.float64,
                ),
                Unitless(),
            ),
            VectorQuantity(np.asarray([0.0], dtype=np.float64), Unitless()),
        )
        # One band above the highest retained index is required to measure the
        # upper external gap; zero-based indexing therefore requires ``+ 2``.
        required_bands = (
            max(group.upper_index for group in definition.retained_band_groups) + 2
        )
        if required_bands > basis.dimension:
            raise ValueError("plane-wave basis does not cover required external bands")
        training_matrices, training_values, training_vectors = self.parent_samples(
            mesh.coordinates.magnitude,
            basis,
            potential,
            recoil_energy,
            required_bands,
            request.duality_absolute_tolerance.magnitude,
        )
        # Endpoint inclusion makes the withheld route independent of the half-open
        # FFT grid while retaining both Brillouin-zone boundary representatives.
        withheld_coordinates = np.linspace(
            -0.5,
            0.5,
            definition.withheld_mesh_size,
            dtype=np.float64,
        )
        _, withheld_values, _ = self.parent_samples(
            withheld_coordinates,
            basis,
            potential,
            recoil_energy,
            required_bands,
            request.duality_absolute_tolerance.magnitude,
        )
        parent_operators = ReciprocalOperatorSamples1D(
            mesh.coordinates,
            reciprocal_period,
            tuple(
                ComplexMatrixQuantity(matrix, Unitless())
                for matrix in training_matrices
            ),
        )
        training_spectrum = BandSpectrumSamples1D(
            mesh.coordinates,
            reciprocal_period,
            MatrixQuantity(training_values, Unitless()),
        )
        sewing = PlaneWaveReciprocalSewingConstructor().execute(basis).coefficient_map
        parent_eigenframes = ReciprocalBandFramePath1D(
            mesh,
            tuple(
                ComplexMatrixQuantity(frame, Unitless()) for frame in training_vectors
            ),
            sewing,
            request.frame_orthonormality_absolute_tolerance.magnitude,
        )
        withheld_spectrum = BandSpectrumSamples1D(
            VectorQuantity(withheld_coordinates, Unitless()),
            reciprocal_period,
            MatrixQuantity(withheld_values, Unitless()),
        )
        return Periodic1DCompositeParentCalculationResult(
            mesh,
            basis,
            parent_operators,
            training_spectrum,
            parent_eigenframes,
            withheld_spectrum,
        )

    def parent_samples(
        self,
        coordinates: RealVector,
        basis: PlaneWaveBasis1D,
        potential: PeriodicFourierPotential1D,
        recoil_energy: ScalarQuantity,
        required_bands: int,
        duality_absolute_tolerance: float,
    ) -> tuple[ComplexArray3, RealMatrix, ComplexArray3]:
        """Construct finite parent matrices and their lowest eigenpairs.

        Parameters
        ----------
        coordinates
            Finite rank-one floating array of dimensionless reciprocal coordinates,
            with shape ``(N_k,)``. Repeated or nonmonotone points are permitted
            because this method owns independent pointwise fiber calculations.
        basis
            Ordered finite plane-wave basis shared by every fiber.
        potential
            Periodic Fourier potential represented in the basis convention.
        recoil_energy
            Energy scale supplied to the plane-wave constructor. Its unit determines
            the represented matrix and eigenvalue unit.
        required_bands
            Positive built-in integer no larger than ``basis.dimension``.
        duality_absolute_tolerance
            Finite nonnegative built-in ``float`` used by the constructor's lattice
            duality check.

        Returns
        -------
        tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]
            Complex parent matrices with shape ``(N_k, M, M)``, real ascending
            eigenvalues with shape ``(N_k, required_bands)``, and complex
            eigenvectors with shape ``(N_k, M, required_bands)``. Here ``M`` is the
            finite plane-wave dimension.

        Raises
        ------
        TypeError
            If an input has the wrong semantic type or array dtype.
        ValueError
            If coordinates are not finite and rank one, if the requested band count
            does not fit the basis, or if the tolerance is negative or nonfinite.

        Notes
        -----
        ``numpy.linalg.eigh`` is appropriate because every represented fiber is
        Hermitian. Eigenvectors within an exactly or numerically degenerate subspace
        are not individually canonical; downstream comparisons therefore use
        projectors or explicit frame alignment. Dense allocation or eigensolver
        failures propagate from NumPy. The method performs no cutoff-convergence
        estimate.
        """

        if not isinstance(coordinates, np.ndarray):
            raise TypeError("coordinates must be a numpy.ndarray")
        if not np.issubdtype(coordinates.dtype, np.floating):
            raise TypeError("coordinates must have a floating dtype")
        if coordinates.ndim != 1 or not np.all(np.isfinite(coordinates)):
            raise ValueError("coordinates must be a finite rank-one array")
        if type(basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if type(required_bands) is not int:
            raise TypeError("required_bands must be a built-in int")
        if required_bands <= 0 or required_bands > basis.dimension:
            raise ValueError("required_bands must fit the plane-wave basis")
        if type(duality_absolute_tolerance) is not float:
            raise TypeError("duality_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(duality_absolute_tolerance)
            or duality_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "duality_absolute_tolerance must be finite and nonnegative"
            )
        constructor = PlaneWaveFiberHamiltonian1DConstructor()
        matrices: list[ComplexMatrix] = []
        values: list[RealVector] = []
        vectors: list[ComplexMatrix] = []
        for coordinate in coordinates:
            # Each k point is an independent Hermitian fiber. Keeping the full
            # represented matrix allows later projection to use exactly the matrix
            # whose lowest eigenspace was selected here.
            represented = constructor.execute(
                float(coordinate),
                basis,
                potential,
                recoil_energy,
                duality_absolute_tolerance,
            ).represented_matrix.magnitude
            # ``eigh`` returns ascending eigenvalues; retain one shared leading
            # eigensystem rather than diagonalizing separately for each band group.
            eigenvalues, eigenvectors = np.linalg.eigh(represented)
            matrices.append(np.asarray(represented, dtype=np.complex128))
            values.append(np.asarray(eigenvalues[:required_bands], dtype=np.float64))
            vectors.append(
                np.asarray(eigenvectors[:, :required_bands], dtype=np.complex128)
            )
        return (
            np.asarray(matrices, dtype=np.complex128),
            np.asarray(values, dtype=np.float64),
            np.asarray(vectors, dtype=np.complex128),
        )

    def calculate_group(
        self,
        request: Periodic1DCompositeBandCalculationRequest,
        parent: Periodic1DCompositeParentCalculationResult,
        group: Periodic1DRetainedBandGroup,
    ) -> Periodic1DCompositeBandCalculationGroupResult:
        """Calculate all demonstrated channels for one retained two-band group.

        Parameters
        ----------
        request
            Calculation request owning tolerances, gauge amplitudes, hopping ranges,
            and the shared campaign definition.
        parent
            Parent result produced from the same request by :meth:`calculate_parent`.
        group
            Contiguous two-band selection to reduce.

        Returns
        -------
        Periodic1DCompositeBandCalculationGroupResult
            Retained source and transformed frame paths together with gauge, Wilson,
            isolation, complete hopping, truncation, interpolation, direct-route,
            Hermiticity, and artifact-identity channels.

        Raises
        ------
        TypeError
            If an argument is not its exact declared domain type.
        ValueError
            If required internal or external gaps are unavailable, or if a composed
            owner rejects incompatible meshes, dimensions, units, or tolerances.

        Notes
        -----
        Neighboring frames are transported with SVD unitary polar factors. This is a
        finite-dimensional parallel-transport convention, not Wannier localization.
        The controlled gauge tests covariance after independent transport and
        alignment. The alternating rough gauge is applied after transport to preserve
        pointwise spectra while deliberately degrading coefficient-space locality.
        Wilson phases follow the closed-loop construction discussed by King-Smith and
        Vanderbilt (1993, https://doi.org/10.1103/PhysRevB.47.1651) and Marzari et al.
        (2012, https://doi.org/10.1103/RevModPhys.84.1419), but this result makes no
        polarization or topology claim.
        """

        if type(request) is not Periodic1DCompositeBandCalculationRequest:
            raise TypeError("request must be Periodic1DCompositeBandCalculationRequest")
        if type(parent) is not Periodic1DCompositeParentCalculationResult:
            raise TypeError("parent must be Periodic1DCompositeParentCalculationResult")
        if type(group) is not Periodic1DRetainedBandGroup:
            raise TypeError("group must be Periodic1DRetainedBandGroup")
        definition = request.definition
        # The source frame is the raw eigensolver basis for this contiguous spectral
        # subspace. Individual columns are gauge-dependent; their span is not.
        selected = slice(group.lower_index, group.upper_index + 1)
        source_frames = ReciprocalBandFramePath1D(
            parent.mesh,
            tuple(
                ComplexMatrixQuantity(frame.magnitude[:, selected], Unitless())
                for frame in parent.parent_eigenframes.frames
            ),
            parent.parent_eigenframes.sewing_map,
            request.frame_orthonormality_absolute_tolerance.magnitude,
        )
        # SVD polar transport chooses the nearest unitary neighbor alignment and
        # distributes the sewn closure without assigning persistent band labels.
        transporter = PolarBandFrameTransporter1D()
        smooth_transport = transporter.execute(
            source_frames,
            request.overlap_singular_value_threshold.magnitude,
        )
        # Transport the controlled attack independently. Aligning only afterward
        # prevents the covariance diagnostic from reusing the reference transport.
        controlled_source = self.apply_controlled_gauge(
            source_frames,
            definition.controlled_gauge_amplitude.magnitude,
        )
        controlled_transport = transporter.execute(
            controlled_source,
            request.overlap_singular_value_threshold.magnitude,
        )
        alignment = BandFrameAligner1D().execute(
            smooth_transport.transported,
            controlled_transport.transported,
        )
        # Source projectors test subspace invariance before any transport convention
        # can hide an error in the deterministic gauge attack.
        projector_constructor = BandProjectorPathConstructor1D()
        source_projectors = projector_constructor.execute(source_frames)
        controlled_source_projectors = projector_constructor.execute(controlled_source)
        projector_defect = self.maximum_projector_defect(
            source_projectors, controlled_source_projectors
        )
        # Apply the high-frequency alternating gauge after smooth transport: this
        # preserves pointwise eigenvalues but supplies an adverse locality control.
        rough_frames = self.apply_rough_gauge(
            smooth_transport.transported,
            definition.rough_gauge_amplitude.magnitude,
        )
        projector = BandProjectedOperatorPathConstructor1D()
        coordinate_tolerance = request.coordinate_absolute_tolerance.magnitude
        smooth_operators = projector.execute(
            parent.parent_operators,
            smooth_transport.transported,
            coordinate_tolerance,
        )
        controlled_operators = projector.execute(
            parent.parent_operators,
            controlled_transport.transported,
            coordinate_tolerance,
        )
        aligned_operators = projector.execute(
            parent.parent_operators,
            alignment.aligned,
            coordinate_tolerance,
        )
        rough_operators = projector.execute(
            parent.parent_operators,
            rough_frames,
            coordinate_tolerance,
        )
        # Training and withheld targets remain distinct so truncation error on the
        # transform grid cannot be reported as off-grid interpolation performance.
        training_target = self.selected_spectrum(parent.training_spectrum, group)
        withheld_target = self.selected_spectrum(parent.withheld_spectrum, group)
        isolation = BandGapAnalyzer1D().execute(
            parent.withheld_spectrum, group.selection
        )
        # Canonicalization provides deterministic storage only. The following
        # comparator performs optimal circular matching of unordered phase sets.
        smooth_wilson = WilsonLoopSpectrumCanonicalizer1D().execute(
            smooth_transport.closure_eigenphases
        )
        controlled_wilson = WilsonLoopSpectrumCanonicalizer1D().execute(
            controlled_transport.closure_eigenphases
        )
        wilson_comparison = WilsonLoopPhaseSetComparator1D().execute(
            smooth_wilson,
            controlled_wilson,
            request.wilson_phase_absolute_tolerance,
        )
        # Transform the complete uniform mesh before any range restriction. The
        # reusable owner implements the normalized FFT and verifies its inverse.
        transformer = ReciprocalOperatorFourierTransformer1D()
        smooth_transform = transformer.execute(
            smooth_operators,
            parent.mesh,
            coordinate_tolerance,
            request.transform_reconstruction_absolute_tolerance.magnitude,
        )
        rough_transform = transformer.execute(
            rough_operators,
            parent.mesh,
            coordinate_tolerance,
            request.transform_reconstruction_absolute_tolerance.magnitude,
        )
        hermiticity = BlockHoppingHermiticityAnalyzer1D().execute(
            smooth_transform.hopping_model,
            request.hopping_hermiticity_absolute_tolerance,
            parent.mesh.point_count,
        )
        range_study = tuple(
            self.calculate_range(
                hopping_range,
                smooth_transform.hopping_model,
                rough_transform.hopping_model,
                training_target,
                withheld_target,
                coordinate_tolerance,
            )
            for hopping_range in definition.hopping_ranges_cells
        )
        # The direct least-squares route is fitted independently at the requested
        # finite range and compared against transform-then-truncate.
        direct_route = self.calculate_direct_route(
            definition.direct_route_range_cells,
            smooth_operators,
            smooth_transform.hopping_model,
        )
        controlled_eigenvalue_error = BandApproximationErrorAnalyzer1D().execute(
            training_target,
            controlled_operators,
            coordinate_tolerance,
        )
        aligned_operator_defect = self.maximum_operator_defect(
            smooth_operators, aligned_operators
        )
        rough_vs_smooth_hopping_defect = self.hopping_l2_defect(
            smooth_transform.hopping_model,
            rough_transform.hopping_model,
        )
        external_gap = isolation.external_minimum_gap
        internal_gap = isolation.internal_minimum_gap
        if external_gap is None or internal_gap is None:
            raise ValueError("composite group requires internal and external gaps")
        outcome = Periodic1DCompositeBandGroupResult(
            wilson=Periodic1DCompositeWilsonGroupResult(
                group.identifier,
                tuple(range(group.lower_index, group.upper_index + 1)),
                smooth_wilson,
                wilson_comparison.maximum_absolute_phase_defect,
            ),
            isolation=Periodic1DCompositeBandIsolationResult(
                internal_gap.magnitude,
                external_gap.magnitude,
                (
                    Periodic1DCompositeExternalIsolationStatus.PASS
                    if external_gap.magnitude
                    > definition.external_gap_threshold.magnitude
                    else Periodic1DCompositeExternalIsolationStatus.FAILED
                ),
            ),
            gauge_comparison=Periodic1DCompositeGaugeComparisonResult(
                smooth_transport.minimum_overlap_singular_value,
                projector_defect,
                alignment.frame_maximum_frobenius_defect,
                aligned_operator_defect,
                controlled_eigenvalue_error.maximum_absolute_error.magnitude,
                rough_vs_smooth_hopping_defect,
            ),
            hopping_representation=Periodic1DCompositeHoppingRepresentationResult(
                smooth_operators,
                smooth_transform.hopping_model,
                rough_transform.hopping_model,
                tuple(
                    float(np.linalg.norm(block.magnitude))
                    for block in smooth_transform.hopping_model.hopping_blocks
                ),
                tuple(
                    float(np.linalg.norm(block.magnitude))
                    for block in rough_transform.hopping_model.hopping_blocks
                ),
                smooth_transform.reconstruction_maximum_frobenius_error,
                rough_transform.reconstruction_maximum_frobenius_error,
                hermiticity.maximum_frobenius_defect.magnitude,
            ),
            range_study=range_study,
            direct_route=direct_route,
            identities=self.calculate_identities(
                smooth_transport.transported,
                projector_constructor.execute(smooth_transport.transported),
                smooth_operators,
                smooth_transform.hopping_model,
                rough_transform.hopping_model,
            ),
        )
        return Periodic1DCompositeBandCalculationGroupResult(
            group,
            outcome,
            source_frames,
            smooth_transport,
            controlled_source,
            controlled_transport,
            alignment,
            source_projectors,
            controlled_source_projectors,
            rough_frames,
            wilson_comparison,
        )

    def selected_spectrum(
        self,
        spectrum: BandSpectrumSamples1D,
        group: Periodic1DRetainedBandGroup,
    ) -> BandSpectrumSamples1D:
        """Select one contiguous group from a wider parent spectrum.

        Parameters
        ----------
        spectrum
            Parent spectrum whose rows are reciprocal samples and whose columns are
            ascending band energies.
        group
            Inclusive zero-based lower and upper band indices.

        Returns
        -------
        BandSpectrumSamples1D
            A spectrum reusing the source coordinates, reciprocal period, and energy
            unit, with only the selected contiguous columns.

        Raises
        ------
        TypeError
            If either argument has the wrong semantic type.
        ValueError
            If the upper band index does not fit the supplied spectrum.

        Notes
        -----
        This operation selects energies only; it does not infer continuity or band
        correspondence through a crossing.
        """

        if type(spectrum) is not BandSpectrumSamples1D:
            raise TypeError("spectrum must be BandSpectrumSamples1D")
        if type(group) is not Periodic1DRetainedBandGroup:
            raise TypeError("group must be Periodic1DRetainedBandGroup")
        if group.upper_index >= spectrum.band_count:
            raise ValueError("group must fit the supplied spectrum")
        selected = spectrum.eigenvalues.magnitude[
            :, group.lower_index : group.upper_index + 1
        ]
        return BandSpectrumSamples1D(
            spectrum.coordinates,
            spectrum.reciprocal_period,
            MatrixQuantity(selected, spectrum.eigenvalues.unit),
        )

    def apply_controlled_gauge(
        self,
        source: ReciprocalBandFramePath1D,
        amplitude: float,
    ) -> ReciprocalBandFramePath1D:
        """Apply the smooth deterministic two-band gauge attack.

        Parameters
        ----------
        source
            Rank-two reciprocal frame path. Each frame has shape ``(M, 2)``.
        amplitude
            Finite built-in ``float`` setting the sinusoidal real-rotation amplitude
            in radians.

        Returns
        -------
        ReciprocalBandFramePath1D
            Frame path ``F_j G_j`` with the source mesh, sewing map, and
            orthonormality tolerance. The unitary attack combines a smooth real
            rotation with fixed-amplitude diagonal phases.

        Raises
        ------
        TypeError
            If ``source`` or ``amplitude`` has the wrong semantic type.
        ValueError
            If ``amplitude`` is nonfinite or ``source`` does not have rank two.

        Notes
        -----
        Right multiplication changes the represented frame basis but preserves each
        rank-two projector in exact arithmetic. The attack is deterministic evidence
        for gauge covariance; it is not a random perturbation or physical evolution.
        """

        if type(source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        if type(amplitude) is not float:
            raise TypeError("amplitude must be a built-in float")
        if not np.isfinite(amplitude):
            raise ValueError("amplitude must be finite")
        if source.rank != 2:
            raise ValueError("controlled gauge attack requires a two-band frame")
        frames: list[ComplexMatrixQuantity] = []
        count = source.mesh.point_count
        for index, frame in enumerate(source.frames):
            # Use the mesh index fraction rather than the stored centered coordinate
            # so the attack is exactly periodic over the half-open discrete cycle.
            coordinate = float(index) / float(count)
            angle = amplitude * np.sin(2.0 * np.pi * coordinate)
            first_phase = 0.31 * np.cos(2.0 * np.pi * coordinate)
            second_phase = -0.27 * np.sin(4.0 * np.pi * coordinate)
            rotation = np.asarray(
                [
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)],
                ],
                dtype=np.complex128,
            )
            phases = np.diag(np.exp(1j * np.asarray([first_phase, second_phase])))
            frames.append(
                ComplexMatrixQuantity(
                    frame.magnitude @ rotation @ phases,
                    Unitless(),
                )
            )
        return ReciprocalBandFramePath1D(
            source.mesh,
            tuple(frames),
            source.sewing_map,
            source.orthonormality_absolute_tolerance,
        )

    def apply_rough_gauge(
        self,
        source: ReciprocalBandFramePath1D,
        amplitude: float,
    ) -> ReciprocalBandFramePath1D:
        """Apply the alternating deterministic two-band gauge attack.

        Parameters
        ----------
        source
            Rank-two reciprocal frame path, normally the smoothly transported path.
        amplitude
            Finite built-in ``float`` setting the alternating real-rotation angle in
            radians.

        Returns
        -------
        ReciprocalBandFramePath1D
            Gauge-equivalent path with alternating rotation and diagonal phase signs.

        Raises
        ------
        TypeError
            If ``source`` or ``amplitude`` has the wrong semantic type.
        ValueError
            If ``amplitude`` is nonfinite or ``source`` does not have rank two.

        Notes
        -----
        The factor ``(-1)**j`` injects the highest alternating mesh frequency. It
        preserves pointwise projectors and spectra in exact arithmetic while
        deliberately moving weight toward long-range hopping coefficients. The
        resulting locality degradation is an adverse control, not model error.
        """

        if type(source) is not ReciprocalBandFramePath1D:
            raise TypeError("source must be ReciprocalBandFramePath1D")
        if type(amplitude) is not float:
            raise TypeError("amplitude must be a built-in float")
        if not np.isfinite(amplitude):
            raise ValueError("amplitude must be finite")
        if source.rank != 2:
            raise ValueError("rough gauge attack requires a two-band frame")
        frames: list[ComplexMatrixQuantity] = []
        for index, frame in enumerate(source.frames):
            # Alternating sign supplies a deterministic mesh-scale gauge oscillation
            # while keeping every right-side transformation unitary.
            sign = 1.0 if index % 2 == 0 else -1.0
            angle = amplitude * sign
            rotation = np.asarray(
                [
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)],
                ],
                dtype=np.complex128,
            )
            phases = np.diag(np.exp(1j * np.asarray([0.43 * sign, -0.37 * sign])))
            frames.append(
                ComplexMatrixQuantity(
                    frame.magnitude @ rotation @ phases,
                    Unitless(),
                )
            )
        return ReciprocalBandFramePath1D(
            source.mesh,
            tuple(frames),
            source.sewing_map,
            source.orthonormality_absolute_tolerance,
        )

    def maximum_projector_defect(
        self,
        reference: BandProjectorPathResult1D,
        candidate: BandProjectorPathResult1D,
    ) -> float:
        """Return the maximum pointwise projector Frobenius defect.

        Parameters
        ----------
        reference, candidate
            Projector paths on the same reciprocal mesh.

        Returns
        -------
        float
            Maximum of ``||P_ref(k_j) - P_cand(k_j)||_F`` over all mesh points.
            The value is dimensionless and finite when the inputs are finite.

        Raises
        ------
        TypeError
            If either input is not a projector-path result.
        ValueError
            If the paths use different meshes.

        Notes
        -----
        Projectors remove arbitrary internal frame rotations, so this is the primary
        source-subspace gauge-invariance diagnostic. It does not measure agreement
        between individual frame columns.
        """

        if type(reference) is not BandProjectorPathResult1D:
            raise TypeError("reference must be BandProjectorPathResult1D")
        if type(candidate) is not BandProjectorPathResult1D:
            raise TypeError("candidate must be BandProjectorPathResult1D")
        if reference.source.mesh != candidate.source.mesh:
            raise ValueError("projector paths must use the same mesh")
        return float(
            max(
                np.linalg.norm(first.magnitude - second.magnitude)
                for first, second in zip(
                    reference.projectors, candidate.projectors, strict=True
                )
            )
        )

    def maximum_operator_defect(
        self,
        reference: ReciprocalOperatorSamples1D,
        candidate: ReciprocalOperatorSamples1D,
    ) -> float:
        """Return the maximum pointwise represented-operator Frobenius defect.

        Parameters
        ----------
        reference, candidate
            Reciprocal operator samples whose matrices are compared in their current
            represented bases and deterministic point order.

        Returns
        -------
        float
            Maximum matrix Frobenius norm of the pointwise difference.

        Raises
        ------
        TypeError
            If either argument is not reciprocal operator samples.
        ValueError
            If the paths contain different numbers of samples.

        Notes
        -----
        The caller must align represented bases before invoking this method. Equal
        sample counts alone do not establish coordinate, unit, or gauge compatibility;
        those checks belong to the constructing and alignment owners used upstream.
        """

        if type(reference) is not ReciprocalOperatorSamples1D:
            raise TypeError("reference must be ReciprocalOperatorSamples1D")
        if type(candidate) is not ReciprocalOperatorSamples1D:
            raise TypeError("candidate must be ReciprocalOperatorSamples1D")
        if len(reference.matrices) != len(candidate.matrices):
            raise ValueError("operator sample counts must agree")
        return float(
            max(
                np.linalg.norm(first.magnitude - second.magnitude)
                for first, second in zip(
                    reference.matrices, candidate.matrices, strict=True
                )
            )
        )

    def hopping_l2_defect(
        self,
        reference: BlockHoppingModel1D,
        candidate: BlockHoppingModel1D,
    ) -> float:
        """Return the coefficient-space block Frobenius defect for two models.

        Parameters
        ----------
        reference, candidate
            Block-hopping models with exactly the same ordered cell representatives.

        Returns
        -------
        float
            ``sqrt(sum_R ||H_ref(R) - H_cand(R)||_F**2)`` in the models' represented
            energy unit. The method does not normalize by model size or coefficient
            norm.

        Raises
        ------
        TypeError
            If either argument is not a block-hopping model.
        ValueError
            If the ordered cell representatives differ.

        Notes
        -----
        This coefficient-space quantity is kept distinct from sampled reciprocal-
        operator and band-energy errors. Parseval equivalence requires a complete
        compatible mesh and normalization convention and is not assumed here.
        """

        if type(reference) is not BlockHoppingModel1D:
            raise TypeError("reference must be BlockHoppingModel1D")
        if type(candidate) is not BlockHoppingModel1D:
            raise TypeError("candidate must be BlockHoppingModel1D")
        if reference.representatives != candidate.representatives:
            raise ValueError("hopping representatives must agree")
        return float(
            np.sqrt(
                sum(
                    np.linalg.norm(first.magnitude - second.magnitude) ** 2
                    for first, second in zip(
                        reference.hopping_blocks,
                        candidate.hopping_blocks,
                        strict=True,
                    )
                )
            )
        )

    def calculate_range(
        self,
        maximum_range: int,
        smooth_model: BlockHoppingModel1D,
        rough_model: BlockHoppingModel1D,
        training_target: BandSpectrumSamples1D,
        withheld_target: BandSpectrumSamples1D,
        coordinate_absolute_tolerance: float,
    ) -> Periodic1DCompositeHoppingRangeResult:
        """Calculate smooth and rough finite-range approximation channels.

        Parameters
        ----------
        maximum_range
            Nonnegative built-in integer cutoff in lattice cells. Blocks with
            ``abs(R) > maximum_range`` are zeroed rather than refitted.
        smooth_model, rough_model
            Complete hopping models produced from the smooth and adverse-control
            reciprocal operators.
        training_target
            Selected parent-band energies on the transform mesh.
        withheld_target
            Independently sampled selected-band energies used only for off-grid
            interpolation evaluation.
        coordinate_absolute_tolerance
            Finite nonnegative built-in ``float`` used when correlating reciprocal
            coordinates.

        Returns
        -------
        Periodic1DCompositeHoppingRangeResult
            Omitted coefficient norms and maximum band-energy errors for both gauges
            on both training and withheld coordinates.

        Raises
        ------
        TypeError
            If an input has the wrong semantic type.
        ValueError
            If the range is negative, the tolerance is negative or nonfinite, or a
            composed truncation, interpolation, or comparison invariant fails.

        Notes
        -----
        Truncation, interpolation, and error analysis remain separate operations.
        Comparing smooth and rough paths at the same range isolates gauge-dependent
        locality without changing the complete pointwise spectrum.
        """

        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        if type(smooth_model) is not BlockHoppingModel1D:
            raise TypeError("smooth_model must be BlockHoppingModel1D")
        if type(rough_model) is not BlockHoppingModel1D:
            raise TypeError("rough_model must be BlockHoppingModel1D")
        if type(training_target) is not BandSpectrumSamples1D:
            raise TypeError("training_target must be BandSpectrumSamples1D")
        if type(withheld_target) is not BandSpectrumSamples1D:
            raise TypeError("withheld_target must be BandSpectrumSamples1D")
        if type(coordinate_absolute_tolerance) is not float:
            raise TypeError("coordinate_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(coordinate_absolute_tolerance)
            or coordinate_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "coordinate_absolute_tolerance must be finite and nonnegative"
            )
        # Truncation zeroes omitted coefficients; it never re-optimizes retained
        # blocks, so the omitted norm and interpolation error retain clear meanings.
        truncator = BlockHoppingTruncator1D()
        smooth = truncator.execute(smooth_model, maximum_range)
        rough = truncator.execute(rough_model, maximum_range)
        interpolator = BlockHoppingInterpolator1D()
        smooth_training = interpolator.execute(
            smooth.truncated, training_target.coordinates
        )
        rough_training = interpolator.execute(
            rough.truncated, training_target.coordinates
        )
        # Evaluate the same truncated model on a disjoint coordinate set rather than
        # deriving withheld values from the training spectrum.
        smooth_withheld = interpolator.execute(
            smooth.truncated, withheld_target.coordinates
        )
        rough_withheld = interpolator.execute(
            rough.truncated, withheld_target.coordinates
        )
        analyzer = BandApproximationErrorAnalyzer1D()
        return Periodic1DCompositeHoppingRangeResult(
            maximum_range,
            smooth.omitted_block_l2_norm,
            rough.omitted_block_l2_norm,
            analyzer.execute(
                training_target, smooth_training, coordinate_absolute_tolerance
            ).maximum_absolute_error.magnitude,
            analyzer.execute(
                training_target, rough_training, coordinate_absolute_tolerance
            ).maximum_absolute_error.magnitude,
            analyzer.execute(
                withheld_target, smooth_withheld, coordinate_absolute_tolerance
            ).maximum_absolute_error.magnitude,
            analyzer.execute(
                withheld_target, rough_withheld, coordinate_absolute_tolerance
            ).maximum_absolute_error.magnitude,
        )

    def calculate_direct_route(
        self,
        maximum_range: int,
        source: ReciprocalOperatorSamples1D,
        mediated_model: BlockHoppingModel1D,
    ) -> Periodic1DCompositeDirectRouteComparisonResult:
        """Compare equal-weight direct fitting with transform-and-truncate.

        Parameters
        ----------
        maximum_range
            Nonnegative built-in integer defining representatives
            ``-maximum_range, ..., maximum_range``.
        source
            Smooth reciprocal-operator samples fitted directly with equal sample
            weights.
        mediated_model
            Complete Fourier-transform hopping model subsequently truncated to the
            same representatives.

        Returns
        -------
        Periodic1DCompositeDirectRouteComparisonResult
            Coefficient-space and sampled reciprocal-operator defects between the two
            finite-range routes.

        Raises
        ------
        TypeError
            If an argument has the wrong semantic type.
        ValueError
            If the range is negative or a composed fitter, truncator, or comparator
            invariant fails.

        Notes
        -----
        The direct route solves an unconstrained complex least-squares problem using
        dense numerical linear algebra as described by Golub and Van Loan (2013).
        It is not constrained to satisfy block Hermiticity. Its residual and its
        disagreement with transform-and-truncate are therefore separate diagnostics.
        """

        if type(maximum_range) is not int:
            raise TypeError("maximum_range must be a built-in int")
        if maximum_range < 0:
            raise ValueError("maximum_range must be nonnegative")
        if type(source) is not ReciprocalOperatorSamples1D:
            raise TypeError("source must be ReciprocalOperatorSamples1D")
        if type(mediated_model) is not BlockHoppingModel1D:
            raise TypeError("mediated_model must be BlockHoppingModel1D")
        # Symmetric representatives make the direct and mediated routes comparable;
        # equal weights reproduce the demonstrated Appendix G fitting contract.
        representatives = tuple(range(-maximum_range, maximum_range + 1))
        weights = VectorQuantity(
            np.ones(source.coordinates.magnitude.shape, dtype=np.float64),
            Unitless(),
        )
        fitted = BlockHoppingLeastSquaresFitter1D().execute(
            source, representatives, weights
        )
        mediated = BlockHoppingTruncator1D().execute(mediated_model, maximum_range)
        comparison = BlockHoppingModelComparator1D().execute(
            mediated.truncated,
            fitted.fitted_model,
            source.coordinates,
        )
        return Periodic1DCompositeDirectRouteComparisonResult(
            maximum_range,
            comparison.coefficient_l2_frobenius_defect.magnitude,
            comparison.sampled_maximum_frobenius_defect.magnitude,
        )

    def calculate_identities(
        self,
        smooth_frames: ReciprocalBandFramePath1D,
        smooth_projectors: BandProjectorPathResult1D,
        smooth_operators: ReciprocalOperatorSamples1D,
        smooth_model: BlockHoppingModel1D,
        rough_model: BlockHoppingModel1D,
    ) -> Periodic1DCompositeArtifactIdentities:
        """Calculate canonical SHA-256 identities for represented artifacts.

        Parameters
        ----------
        smooth_frames
            Smooth transported frames in deterministic mesh order.
        smooth_projectors
            Projectors constructed from those smooth frames.
        smooth_operators
            Smooth projected reciprocal operators.
        smooth_model, rough_model
            Complete block-hopping models in deterministic representative order.

        Returns
        -------
        Periodic1DCompositeArtifactIdentities
            Lowercase SHA-256 hexadecimal digests for canonical C-order little-endian
            complex128 arrays.

        Raises
        ------
        TypeError
            If any argument has the wrong semantic type.
        ValueError
            If canonical array construction exposes nonfinite or non-rank-three data.

        Notes
        -----
        SHA-256 follows NIST FIPS 180-4
        (https://doi.org/10.6028/NIST.FIPS.180-4). These digests bind exact array
        bytes for compatibility and provenance. They do not establish numerical
        equivalence, scientific validity, or physical alignment.
        """

        if type(smooth_frames) is not ReciprocalBandFramePath1D:
            raise TypeError("smooth_frames must be ReciprocalBandFramePath1D")
        if type(smooth_projectors) is not BandProjectorPathResult1D:
            raise TypeError("smooth_projectors must be BandProjectorPathResult1D")
        if type(smooth_operators) is not ReciprocalOperatorSamples1D:
            raise TypeError("smooth_operators must be ReciprocalOperatorSamples1D")
        if type(smooth_model) is not BlockHoppingModel1D:
            raise TypeError("smooth_model must be BlockHoppingModel1D")
        if type(rough_model) is not BlockHoppingModel1D:
            raise TypeError("rough_model must be BlockHoppingModel1D")
        # Stack in the owning path/model order before canonical byte conversion;
        # changing mesh or representative order must change the identity.
        return Periodic1DCompositeArtifactIdentities(
            self.array_sha256(
                np.asarray(
                    [frame.magnitude for frame in smooth_frames.frames],
                    dtype=np.complex128,
                )
            ),
            self.array_sha256(
                np.asarray(
                    [projector.magnitude for projector in smooth_projectors.projectors],
                    dtype=np.complex128,
                )
            ),
            self.array_sha256(
                np.asarray(
                    [matrix.magnitude for matrix in smooth_operators.matrices],
                    dtype=np.complex128,
                )
            ),
            self.array_sha256(
                np.asarray(
                    [block.magnitude for block in smooth_model.hopping_blocks],
                    dtype=np.complex128,
                )
            ),
            self.array_sha256(
                np.asarray(
                    [block.magnitude for block in rough_model.hopping_blocks],
                    dtype=np.complex128,
                )
            ),
        )

    def array_sha256(self, values: ComplexArray3) -> str:
        """Return SHA-256 over canonical complex-array bytes.

        Parameters
        ----------
        values
            Finite rank-three complex floating array. Input byte order, precision,
            and contiguity may vary; semantic dimensions are owned by the caller.

        Returns
        -------
        str
            Lowercase 64-character SHA-256 hexadecimal digest of C-order
            little-endian complex128 bytes.

        Raises
        ------
        TypeError
            If ``values`` is not a NumPy complex floating array.
        ValueError
            If ``values`` is not finite and rank three.

        Notes
        -----
        Canonicalization intentionally erases source dtype width, byte order, and
        memory strides before hashing. The operation follows the SHA-256 standard in
        NIST FIPS 180-4 (https://doi.org/10.6028/NIST.FIPS.180-4). Allocation failure
        propagates from NumPy. A digest establishes byte identity only.
        """

        if not isinstance(values, np.ndarray):
            raise TypeError("values must be a numpy.ndarray")
        if not np.issubdtype(values.dtype, np.complexfloating):
            raise TypeError("values must have a complex floating dtype")
        if values.ndim != 3 or not np.all(np.isfinite(values)):
            raise ValueError("values must be a finite rank-three array")
        # Fixed endian, width, and traversal order make identities independent of
        # host architecture and NumPy view strides.
        canonical = np.ascontiguousarray(values, dtype="<c16")
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()
