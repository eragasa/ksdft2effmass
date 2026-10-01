r"""Calculation Workflow for reconstructable Appendix G isolated-band channels.

The Workflow extracts the demonstrated numerical campaign behavior from the frozen
historical runner without performing filesystem access or external execution.  It
calculates parent-representation studies, scalar-band reciprocal samples, complete
hoppings, finite-range diagnostics, and parent observables.  Gauge transport and
Wannier localization remain separate capabilities and are not implied by this result.

The plane-wave matrix is a finite Galerkin representation of the Bloch fiber, while
the real-space route uses a centered second-order periodic finite-difference stencil
with conjugate Bloch-seam phases.  Their low-mode comparison is performed only after
the finite-difference operator is transported into the common discrete Fourier basis.
The cosine model is also compared with Mathieu characteristic values using
``q = 2 V_0 / E_G`` and ``E / E_G = A / 4``.  Complete scalar hoppings use the finite
Fourier pair

.. math::

   t_R = N_k^{-1}\sum_j e^{-i k_j R} E(k_j), \qquad
   E(k_j) = \sum_R e^{i k_j R} t_R.

Finite-range diagnostics retain training and withheld errors, omitted-coefficient
norms, the finite-transform Parseval residual, unconstrained complex least-squares
route defects, bandwidth error, and analytical hopping curvature as distinct values.
The parent curvature instead uses the explicitly requested three-point momentum step.
All public campaign quantities are unitless under the Appendix G convention
``a = 2 pi``, ``G = 1``, and ``E_G = 1``.

References
----------
Payne, M. C. et al. (1992), *Reviews of Modern Physics* 64, 1045--1097.
https://doi.org/10.1103/RevModPhys.64.1045

Chelikowsky, J. R., Troullier, N., and Saad, Y. (1994), *Physical Review
Letters* 72, 1240--1243. https://doi.org/10.1103/PhysRevLett.72.1240

McLachlan, N. W. (1947), *Theory and Application of Mathieu Functions*.

Trefethen, L. N. (2000), *Spectral Methods in MATLAB*.
https://doi.org/10.1137/1.9780898719598

Golub, G. H. and Van Loan, C. F. (2013), *Matrix Computations*, fourth edition.

Marzari, N. et al. (2012), *Reviews of Modern Physics* 84, 1419--1475.
https://doi.org/10.1103/RevModPhys.84.1419
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
from scipy.linalg import eigh  # type: ignore[import-untyped]
from scipy.special import mathieu_a, mathieu_b  # type: ignore[import-untyped]

from ksdft2effmass.operators import (
    ComplexMatrixQuantity,
    ScalarQuantity,
    Unitless,
    VectorQuantity,
)
from ksdft2effmass.solid_state import BlockHoppingModel1D, ReciprocalOperatorSamples1D

from .isolated import Periodic1DIsolatedBandCampaignDefinition
from .isolated_results import (
    Periodic1DFiniteDifferenceGridObservation,
    Periodic1DHoppingRangeDiagnostic,
    Periodic1DLowModeOperatorObservation,
    Periodic1DParentBandObservables,
    Periodic1DParentRepresentationVerificationResult,
    Periodic1DPlaneWaveCutoffObservation,
    Periodic1DWeakPotentialGapObservation,
)

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type IntegerVector = npt.NDArray[np.int64]


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCalculationRequest:
    """Declare one execution-local isolated-band diagnostic calculation.

    Parameters
    ----------
    definition
        Versioned Appendix G isolated-band controls.  All quantities use the retained
        dimensionless convention in which energies are normalized by :math:`E_G`.
    zone_center_curvature_step
        Positive reduced-momentum step used only for the parent central-difference
        curvature diagnostic.  The finite-range hopping curvature is analytical.
    """

    definition: Periodic1DIsolatedBandCampaignDefinition
    zone_center_curvature_step: ScalarQuantity

    def __post_init__(self) -> None:
        """Validate exact definition ownership and a positive unitless step."""
        if type(self.definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError(
                "definition must be Periodic1DIsolatedBandCampaignDefinition"
            )
        if type(self.zone_center_curvature_step) is not ScalarQuantity:
            raise TypeError("zone_center_curvature_step must be ScalarQuantity")
        if not isinstance(self.zone_center_curvature_step.unit, Unitless):
            raise ValueError("zone_center_curvature_step must use Unitless")
        if self.zone_center_curvature_step.magnitude <= 0.0:
            raise ValueError("zone_center_curvature_step must be positive")


@dataclass(frozen=True, slots=True)
class Periodic1DIsolatedBandCalculationResult:
    """Retain all requested calculated isolated-band diagnostic channels.

    Parameters
    ----------
    request
        Exact calculation controls, including the curvature differencing step.
    parent_verification
        Plane-wave cutoff, finite-difference, low-mode, Mathieu, weak-gap, and
        symmetry diagnostics.
    reciprocal_samples
        Lowest-band energies on the complete centered reciprocal mesh.
    hopping_model
        Complete centered finite Fourier coefficients for the sampled scalar band.
    hopping_range_study
        Separate training, withheld, Parseval, route, bandwidth, and curvature
        diagnostics for every requested finite range.
    parent_observables
        Independently sampled parent bandwidth, boundary gap, and center curvature.
    full_mesh_reconstruction_maximum_absolute_error
        Maximum real-part reconstruction error on the training mesh.
    full_mesh_reconstruction_maximum_imaginary
        Maximum imaginary reconstruction residual on the training mesh.
    hopping_maximum_imaginary
        Maximum imaginary part among complete scalar hopping coefficients.
    """

    request: Periodic1DIsolatedBandCalculationRequest
    parent_verification: Periodic1DParentRepresentationVerificationResult
    reciprocal_samples: ReciprocalOperatorSamples1D
    hopping_model: BlockHoppingModel1D
    hopping_range_study: tuple[Periodic1DHoppingRangeDiagnostic, ...]
    parent_observables: Periodic1DParentBandObservables
    full_mesh_reconstruction_maximum_absolute_error: float
    full_mesh_reconstruction_maximum_imaginary: float
    hopping_maximum_imaginary: float

    def __post_init__(self) -> None:
        """Validate typed channels and finite nonnegative reconstruction residuals."""
        if type(self.request) is not Periodic1DIsolatedBandCalculationRequest:
            raise TypeError("request uses the wrong calculation request type")
        if (
            type(self.parent_verification)
            is not Periodic1DParentRepresentationVerificationResult
        ):
            raise TypeError("parent_verification uses the wrong ResultObject")
        if type(self.reciprocal_samples) is not ReciprocalOperatorSamples1D:
            raise TypeError("reciprocal_samples must be ReciprocalOperatorSamples1D")
        if self.reciprocal_samples.matrix_dimension != 1:
            raise ValueError("reciprocal_samples must represent one scalar band")
        if type(self.hopping_model) is not BlockHoppingModel1D:
            raise TypeError("hopping_model must be BlockHoppingModel1D")
        if self.hopping_model.matrix_dimension != 1:
            raise ValueError("hopping_model must contain scalar blocks")
        if (
            not isinstance(self.hopping_range_study, tuple)
            or not self.hopping_range_study
            or any(
                type(item) is not Periodic1DHoppingRangeDiagnostic
                for item in self.hopping_range_study
            )
        ):
            raise TypeError("hopping_range_study must be a nonempty typed tuple")
        if type(self.parent_observables) is not Periodic1DParentBandObservables:
            raise TypeError("parent_observables uses the wrong ResultObject")
        residuals = (
            self.full_mesh_reconstruction_maximum_absolute_error,
            self.full_mesh_reconstruction_maximum_imaginary,
            self.hopping_maximum_imaginary,
        )
        if any(
            type(value) is not float or not np.isfinite(value) or value < 0.0
            for value in residuals
        ):
            raise ValueError("reconstruction residuals must be finite and nonnegative")


class Periodic1DIsolatedBandCalculationWorkflow:
    """Calculate reusable nonlocalization channels of the isolated Appendix G study.

    The Workflow performs deterministic in-process NumPy/SciPy calculations only.  It
    does not read retained results, invoke a historical runner, execute Wannier90,
    establish material validation, or perform uncertainty quantification.

    Notes
    -----
    ``execute`` returns operationally immutable project ResultObjects.  Plane-wave
    diagonalization uses dense Hermitian eigensolves; finite-difference calculations
    request only the lowest declared eigenvalues from a dense Hermitian matrix.  The
    complete Fourier transform is evaluated as a direct finite sum so its phase and
    centered-representative convention remain explicit.  Rank-deficient or
    ill-conditioned fitting is not reclassified as a passing scientific result.

    See Also
    --------
    Periodic1DIsolatedResultVerifier
        Independent retained-result reconstruction that does not import this Workflow.
    """

    __slots__ = ()

    def execute(
        self, request: Periodic1DIsolatedBandCalculationRequest
    ) -> Periodic1DIsolatedBandCalculationResult:
        """Calculate parent studies, scalar Fourier reduction, and observables.

        Parameters
        ----------
        request
            Versioned controls and explicit parent-curvature step.

        Returns
        -------
        Periodic1DIsolatedBandCalculationResult
            Separate calculated parent, transform, finite-range, and observable
            channels.
        """
        if type(request) is not Periodic1DIsolatedBandCalculationRequest:
            raise TypeError("request must be Periodic1DIsolatedBandCalculationRequest")
        definition = request.definition
        parent = self.calculate_parent_verification(definition)
        coordinates = -0.5 + np.arange(
            definition.reciprocal_mesh_size, dtype=np.float64
        ) / float(definition.reciprocal_mesh_size)
        cutoff = definition.plane_wave_cutoffs[-1]
        energies = np.asarray(
            [
                self.plane_wave_eigensystem(
                    float(momentum), definition.potential_strength.magnitude, cutoff
                )[0][0]
                for momentum in coordinates
            ],
            dtype=np.float64,
        )
        representatives = np.arange(
            -definition.reciprocal_mesh_size // 2,
            definition.reciprocal_mesh_size // 2,
            dtype=np.int64,
        )
        hoppings = self.direct_hoppings(
            energies,
            coordinates,
            representatives,
            definition.lattice_period.magnitude,
        )
        reconstruction = self.reconstruct(
            hoppings,
            coordinates,
            representatives,
            definition.lattice_period.magnitude,
        )
        reciprocal_samples = ReciprocalOperatorSamples1D(
            VectorQuantity(coordinates, Unitless()),
            definition.reciprocal_vector,
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[energy]], dtype=np.complex128), Unitless()
                )
                for energy in energies
            ),
        )
        hopping_model = BlockHoppingModel1D(
            definition.reciprocal_vector,
            tuple(int(value) for value in representatives),
            tuple(
                ComplexMatrixQuantity(
                    np.asarray([[coefficient]], dtype=np.complex128), Unitless()
                )
                for coefficient in hoppings
            ),
        )
        range_study = self.calculate_hopping_range_study(
            definition, energies, coordinates, representatives, hoppings
        )
        parent_observables = self.calculate_parent_observables(
            definition, request.zone_center_curvature_step.magnitude
        )
        return Periodic1DIsolatedBandCalculationResult(
            request,
            parent,
            reciprocal_samples,
            hopping_model,
            range_study,
            parent_observables,
            float(np.max(np.abs(reconstruction.real - energies))),
            float(np.max(np.abs(reconstruction.imag))),
            float(np.max(np.abs(hoppings.imag))),
        )

    def calculate_parent_verification(
        self, definition: Periodic1DIsolatedBandCampaignDefinition
    ) -> Periodic1DParentRepresentationVerificationResult:
        """Calculate discretization, reference, and symmetry channels.

        Parameters
        ----------
        definition
            Versioned model and parent-study controls.

        Returns
        -------
        Periodic1DParentRepresentationVerificationResult
            Separate plane-wave, finite-difference, low-mode, weak-gap, Mathieu, and
            symmetry outcomes.
        """
        if type(definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition uses the wrong campaign definition type")
        momenta = definition.parent_sample_momenta.magnitude
        potential = definition.potential_strength.magnitude
        band_count = definition.compared_band_count
        reference = np.asarray(
            [
                self.plane_wave_eigensystem(
                    float(momentum), potential, definition.plane_wave_reference_cutoff
                )[0][:band_count]
                for momentum in momenta
            ],
            dtype=np.float64,
        )
        plane_wave = tuple(
            Periodic1DPlaneWaveCutoffObservation(
                cutoff,
                float(
                    np.max(
                        np.abs(
                            np.asarray(
                                [
                                    self.plane_wave_eigensystem(
                                        float(momentum), potential, cutoff
                                    )[0][:band_count]
                                    for momentum in momenta
                                ],
                                dtype=np.float64,
                            )
                            - reference
                        )
                    )
                ),
            )
            for cutoff in definition.plane_wave_cutoffs
        )
        finite_difference: list[Periodic1DFiniteDifferenceGridObservation] = []
        low_mode: list[Periodic1DLowModeOperatorObservation] = []
        for points in definition.finite_difference_points:
            values = np.asarray(
                [
                    self.finite_difference_energies(
                        float(momentum),
                        potential,
                        points,
                        band_count,
                        definition.lattice_period.magnitude,
                    )
                    for momentum in momenta
                ],
                dtype=np.float64,
            )
            finite_difference.append(
                Periodic1DFiniteDifferenceGridObservation(
                    points,
                    1.0 / float(points),
                    float(np.max(np.abs(values - reference))),
                )
            )
            low_mode.append(
                Periodic1DLowModeOperatorObservation(
                    points,
                    definition.common_low_mode_cutoff,
                    max(
                        self.low_mode_operator_error(
                            float(momentum),
                            potential,
                            points,
                            definition.common_low_mode_cutoff,
                            definition.lattice_period.magnitude,
                        )
                        for momentum in momenta
                    ),
                )
            )
        weak = tuple(
            self.calculate_weak_gap(
                float(strength), definition.plane_wave_reference_cutoff
            )
            for strength in definition.weak_potential_strengths.magnitude
        )
        q = 2.0 * potential
        center = float(mathieu_a(0, q) / 4.0)
        boundary_values = np.sort(
            np.asarray([mathieu_a(1, q), mathieu_b(1, q)], dtype=np.float64) / 4.0
        )
        center_plane_wave = self.plane_wave_eigensystem(
            0.0, potential, definition.plane_wave_reference_cutoff
        )[0][0]
        boundary_plane_wave = self.plane_wave_eigensystem(
            0.5, potential, definition.plane_wave_reference_cutoff
        )[0][:2]
        inversion, sign = self.calculate_symmetry_residuals(definition)
        return Periodic1DParentRepresentationVerificationResult(
            plane_wave,
            tuple(finite_difference),
            tuple(low_mode),
            weak,
            center,
            (float(boundary_values[0]), float(boundary_values[1])),
            abs(float(center_plane_wave) - center),
            float(np.max(np.abs(boundary_plane_wave - boundary_values))),
            "q=2*V0/E_G and E/E_G=A/4",
            inversion,
            sign,
        )

    def plane_wave_eigensystem(
        self, momentum: float, potential_strength: float, cutoff: int
    ) -> tuple[RealVector, ComplexMatrix]:
        """Diagonalize one normalized cosine-potential plane-wave fiber.

        Parameters
        ----------
        momentum
            Reduced reciprocal coordinate in the first Brillouin zone.
        potential_strength
            Nonnegative cosine amplitude in normalized :math:`E_G` units.
        cutoff
            Positive symmetric reciprocal-index cutoff.

        Returns
        -------
        tuple
            Increasing eigenvalues and column-major normalized eigenvectors.
        """
        if type(momentum) is not float:
            raise TypeError("momentum must be a built-in float")
        if not np.isfinite(momentum):
            raise ValueError("momentum must be finite")
        if type(potential_strength) is not float:
            raise TypeError("potential_strength must be a built-in float")
        if not np.isfinite(potential_strength):
            raise ValueError("potential_strength must be finite")
        if type(cutoff) is not int or cutoff <= 0:
            raise ValueError("cutoff must be a positive built-in int")
        indices = np.arange(-cutoff, cutoff + 1, dtype=np.float64)
        matrix = np.diag(np.square(momentum + indices)).astype(np.complex128)
        coupling = 0.5 * potential_strength
        matrix += np.diag(np.full(2 * cutoff, coupling), 1)
        matrix += np.diag(np.full(2 * cutoff, coupling), -1)
        values, vectors = np.linalg.eigh(matrix)
        return (
            np.asarray(values, dtype=np.float64),
            np.asarray(vectors, dtype=np.complex128),
        )

    def finite_difference_energies(
        self,
        momentum: float,
        potential_strength: float,
        points: int,
        band_count: int,
        lattice_period: float,
    ) -> RealVector:
        """Calculate lowest periodic second-difference fiber eigenvalues.

        Parameters
        ----------
        momentum, potential_strength
            Reduced reciprocal coordinate and normalized cosine amplitude.
        points, band_count
            Periodic grid size and number of increasing eigenvalues returned.
        lattice_period
            Positive direct-lattice period.

        Returns
        -------
        numpy.ndarray
            Lowest ``band_count`` binary64 eigenvalues.
        """
        self.validate_fiber_scalars(
            momentum, potential_strength, points, lattice_period
        )
        if type(band_count) is not int:
            raise TypeError("band_count must be a built-in int")
        if not 1 <= band_count <= points:
            raise ValueError("band_count must lie between one and points")
        spacing = lattice_period / float(points)
        kinetic = 1.0 / spacing**2
        coordinates = spacing * np.arange(points, dtype=np.float64)
        matrix = np.diag(
            2.0 * kinetic + potential_strength * np.cos(coordinates)
        ).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * lattice_period)
        matrix[-1, 0] = matrix[0, -1].conjugate()
        return np.asarray(
            eigh(
                matrix,
                subset_by_index=(0, band_count - 1),
                eigvals_only=True,
                check_finite=False,
            ),
            dtype=np.float64,
        )

    def low_mode_operator_error(
        self,
        momentum: float,
        potential_strength: float,
        points: int,
        low_mode_cutoff: int,
        lattice_period: float,
    ) -> float:
        """Compare finite-difference and plane-wave operators on common modes.

        Parameters
        ----------
        momentum, potential_strength
            Reduced reciprocal coordinate and normalized cosine amplitude.
        points, low_mode_cutoff
            Periodic grid size and symmetric common Fourier cutoff.
        lattice_period
            Positive direct-lattice period.

        Returns
        -------
        float
            Frobenius defect in normalized :math:`E_G` units.
        """
        self.validate_fiber_scalars(
            momentum, potential_strength, points, lattice_period
        )
        if type(low_mode_cutoff) is not int:
            raise TypeError("low_mode_cutoff must be a built-in int")
        if low_mode_cutoff < 0:
            raise ValueError("low_mode_cutoff must be nonnegative")
        if 2 * low_mode_cutoff + 1 > points:
            raise ValueError("common low-mode dimension must not exceed points")
        spacing = lattice_period / float(points)
        kinetic = 1.0 / spacing**2
        coordinates = spacing * np.arange(points, dtype=np.float64)
        matrix = np.diag(
            2.0 * kinetic + potential_strength * np.cos(coordinates)
        ).astype(np.complex128)
        off_diagonal = np.full(points - 1, -kinetic)
        matrix += np.diag(off_diagonal, 1) + np.diag(off_diagonal, -1)
        matrix[0, -1] = -kinetic * np.exp(-1j * momentum * lattice_period)
        matrix[-1, 0] = matrix[0, -1].conjugate()
        indices = np.arange(-low_mode_cutoff, low_mode_cutoff + 1)
        transform = np.exp(
            1j * np.outer(coordinates, momentum + indices.astype(np.float64))
        ) / np.sqrt(points)
        transported = transform.conj().T @ matrix @ transform
        plane_wave = np.diag(np.square(momentum + indices)).astype(np.complex128)
        coupling = 0.5 * potential_strength
        plane_wave += np.diag(np.full(2 * low_mode_cutoff, coupling), 1)
        plane_wave += np.diag(np.full(2 * low_mode_cutoff, coupling), -1)
        return float(np.linalg.norm(transported - plane_wave))

    def validate_fiber_scalars(
        self,
        momentum: float,
        potential_strength: float,
        points: int,
        lattice_period: float,
    ) -> None:
        """Validate scalar inputs shared by finite-difference fiber operations.

        Parameters
        ----------
        momentum, potential_strength
            Finite built-in floating-point model values.
        points
            Periodic grid size of at least three.
        lattice_period
            Positive finite built-in floating-point period.
        """
        for name, value in (
            ("momentum", momentum),
            ("potential_strength", potential_strength),
            ("lattice_period", lattice_period),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
        if lattice_period <= 0.0:
            raise ValueError("lattice_period must be positive")
        if type(points) is not int:
            raise TypeError("points must be a built-in int")
        if points < 3:
            raise ValueError("points must be at least three")

    def calculate_symmetry_residuals(
        self, definition: Periodic1DIsolatedBandCampaignDefinition
    ) -> tuple[float, float]:
        """Calculate inversion and potential-sign translation spectral residuals.

        Parameters
        ----------
        definition
            Versioned potential, band-count, and cutoff controls.

        Returns
        -------
        tuple
            Inversion defect followed by cosine-sign translation defect.
        """
        if type(definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition uses the wrong campaign definition type")
        mesh = np.linspace(-0.5, 0.5, 41)
        cutoff = definition.plane_wave_cutoffs[-1]
        count = definition.compared_band_count
        strength = definition.potential_strength.magnitude
        positive = np.asarray(
            [
                self.plane_wave_eigensystem(float(k), strength, cutoff)[0][:count]
                for k in mesh
            ]
        )
        reflected = np.asarray(
            [
                self.plane_wave_eigensystem(float(-k), strength, cutoff)[0][:count]
                for k in mesh
            ]
        )
        negative = np.asarray(
            [
                self.plane_wave_eigensystem(float(k), -strength, cutoff)[0][:count]
                for k in mesh
            ]
        )
        return (
            float(np.max(np.abs(positive - reflected))),
            float(np.max(np.abs(positive - negative))),
        )

    def calculate_weak_gap(
        self, potential_strength: float, reference_cutoff: int
    ) -> Periodic1DWeakPotentialGapObservation:
        """Calculate one boundary gap against its leading weak-cosine value.

        Parameters
        ----------
        potential_strength
            Positive normalized cosine amplitude.
        reference_cutoff
            Symmetric plane-wave reference cutoff.

        Returns
        -------
        Periodic1DWeakPotentialGapObservation
            Numerical gap, leading value, and relative deviation.
        """
        if type(potential_strength) is not float:
            raise TypeError("potential_strength must be a built-in float")
        if not np.isfinite(potential_strength) or potential_strength <= 0.0:
            raise ValueError("potential_strength must be finite and positive")
        if type(reference_cutoff) is not int:
            raise TypeError("reference_cutoff must be a built-in int")
        if reference_cutoff <= 0:
            raise ValueError("reference_cutoff must be positive")
        values = self.plane_wave_eigensystem(0.5, potential_strength, reference_cutoff)[
            0
        ]
        gap = float(values[1] - values[0])
        return Periodic1DWeakPotentialGapObservation(
            potential_strength,
            gap,
            potential_strength,
            abs(gap - potential_strength) / potential_strength,
        )

    def direct_hoppings(
        self,
        energies: RealVector,
        coordinates: RealVector,
        representatives: IntegerVector,
        lattice_period: float,
    ) -> ComplexVector:
        """Calculate complete scalar hopping coefficients by a direct finite sum.

        Parameters
        ----------
        energies, coordinates
            Ordered scalar band values and reciprocal coordinates.
        representatives
            Ordered centered integer cell representatives.
        lattice_period
            Direct-lattice period in the Fourier phase convention.

        Returns
        -------
        numpy.ndarray
            Complete complex hopping coefficients.
        """
        self.validate_fourier_inputs(
            energies, coordinates, representatives, lattice_period
        )
        phase = np.exp(-1j * np.outer(representatives * lattice_period, coordinates))
        return np.asarray(phase @ energies / coordinates.size, dtype=np.complex128)

    def reconstruct(
        self,
        hoppings: ComplexVector,
        coordinates: RealVector,
        representatives: IntegerVector,
        lattice_period: float,
    ) -> ComplexVector:
        """Reconstruct scalar reciprocal samples by the inverse finite sum.

        Parameters
        ----------
        hoppings, representatives
            Complex coefficients and corresponding integer cell representatives.
        coordinates
            Reciprocal coordinates to evaluate.
        lattice_period
            Direct-lattice period in the Fourier phase convention.

        Returns
        -------
        numpy.ndarray
            Complex reconstructed scalar-band samples.
        """
        if type(hoppings) is not np.ndarray or hoppings.dtype != np.complex128:
            raise TypeError("hoppings must be a complex128 NumPy array")
        if hoppings.ndim != 1 or not np.all(np.isfinite(hoppings)):
            raise ValueError("hoppings must be a finite vector")
        self.validate_fourier_inputs(
            np.zeros(coordinates.shape, dtype=np.float64),
            coordinates,
            representatives,
            lattice_period,
        )
        if hoppings.shape != representatives.shape:
            raise ValueError("one hopping is required per representative")
        design = np.exp(1j * np.outer(coordinates, representatives * lattice_period))
        return np.asarray(design @ hoppings, dtype=np.complex128)

    def validate_fourier_inputs(
        self,
        energies: RealVector,
        coordinates: RealVector,
        representatives: IntegerVector,
        lattice_period: float,
    ) -> None:
        """Validate direct finite Fourier-pair inputs without changing them.

        Parameters
        ----------
        energies, coordinates
            Binary64 vectors with equal nonzero length.
        representatives
            Nonempty int64 vector of unique cell representatives.
        lattice_period
            Positive finite built-in float.
        """
        for name, value, dtype in (
            ("energies", energies, np.dtype(np.float64)),
            ("coordinates", coordinates, np.dtype(np.float64)),
            ("representatives", representatives, np.dtype(np.int64)),
        ):
            if type(value) is not np.ndarray or value.dtype != dtype:
                raise TypeError(f"{name} must be a {dtype.name} NumPy array")
            if value.ndim != 1 or value.size == 0:
                raise ValueError(f"{name} must be a nonempty vector")
            if not np.all(np.isfinite(value)):
                raise ValueError(f"{name} must contain finite values")
        if energies.shape != coordinates.shape:
            raise ValueError("energies and coordinates must have equal shapes")
        if np.unique(representatives).size != representatives.size:
            raise ValueError("representatives must be unique")
        if type(lattice_period) is not float:
            raise TypeError("lattice_period must be a built-in float")
        if not np.isfinite(lattice_period) or lattice_period <= 0.0:
            raise ValueError("lattice_period must be finite and positive")

    def calculate_hopping_range_study(
        self,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        energies: RealVector,
        coordinates: RealVector,
        representatives: IntegerVector,
        hoppings: ComplexVector,
    ) -> tuple[Periodic1DHoppingRangeDiagnostic, ...]:
        """Calculate every requested finite-range diagnostic independently.

        Parameters
        ----------
        definition
            Versioned range and withheld-mesh controls.
        energies, coordinates
            Complete-mesh scalar target samples.
        representatives, hoppings
            Complete Fourier coefficient representation.

        Returns
        -------
        tuple
            One separate diagnostic record per requested hopping range.
        """
        if type(definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition uses the wrong campaign definition type")
        self.validate_fourier_inputs(
            energies, coordinates, representatives, definition.lattice_period.magnitude
        )
        if type(hoppings) is not np.ndarray or hoppings.dtype != np.complex128:
            raise TypeError("hoppings must be a complex128 NumPy array")
        if hoppings.shape != representatives.shape or not np.all(np.isfinite(hoppings)):
            raise ValueError("hoppings must be finite and match representatives")
        withheld_coordinates = np.linspace(-0.5, 0.5, definition.withheld_mesh_size)
        cutoff = definition.plane_wave_cutoffs[-1]
        strength = definition.potential_strength.magnitude
        withheld_parent = np.asarray(
            [
                self.plane_wave_eigensystem(float(k), strength, cutoff)[0][0]
                for k in withheld_coordinates
            ],
            dtype=np.float64,
        )
        return tuple(
            self.calculate_one_hopping_range(
                hopping_range,
                energies,
                coordinates,
                withheld_coordinates,
                withheld_parent,
                representatives,
                hoppings,
                definition.lattice_period.magnitude,
            )
            for hopping_range in definition.hopping_ranges
        )

    def calculate_one_hopping_range(
        self,
        hopping_range: int,
        energies: RealVector,
        coordinates: RealVector,
        withheld_coordinates: RealVector,
        withheld_parent: RealVector,
        representatives: IntegerVector,
        hoppings: ComplexVector,
        lattice_period: float,
    ) -> Periodic1DHoppingRangeDiagnostic:
        """Calculate all metrics for one symmetric scalar hopping truncation.

        Parameters
        ----------
        hopping_range
            Maximum absolute integer cell displacement retained.
        energies, coordinates
            Complete training target and reciprocal mesh.
        withheld_coordinates, withheld_parent
            Independent comparison mesh and parent lowest-band target.
        representatives, hoppings
            Complete centered coefficient representation.
        lattice_period
            Direct-lattice period in the Fourier phase convention.

        Returns
        -------
        Periodic1DHoppingRangeDiagnostic
            Separate truncation, training, withheld, route, Parseval, and observable
            metrics.
        """
        if type(hopping_range) is not int:
            raise TypeError("hopping_range must be a built-in int")
        if hopping_range < 0:
            raise ValueError("hopping_range must be nonnegative")
        self.validate_fourier_inputs(
            energies, coordinates, representatives, lattice_period
        )
        if (
            type(withheld_coordinates) is not np.ndarray
            or withheld_coordinates.dtype != np.float64
            or withheld_coordinates.ndim != 1
            or withheld_coordinates.size == 0
            or not np.all(np.isfinite(withheld_coordinates))
        ):
            raise ValueError("withheld_coordinates must be a finite float64 vector")
        if (
            type(withheld_parent) is not np.ndarray
            or withheld_parent.dtype != np.float64
            or withheld_parent.shape != withheld_coordinates.shape
            or not np.all(np.isfinite(withheld_parent))
        ):
            raise ValueError("withheld_parent must match withheld_coordinates")
        if (
            type(hoppings) is not np.ndarray
            or hoppings.dtype != np.complex128
            or hoppings.shape != representatives.shape
            or not np.all(np.isfinite(hoppings))
        ):
            raise ValueError("hoppings must be a finite matching complex128 vector")
        mask = np.abs(representatives) <= hopping_range
        retained_representatives = representatives[mask]
        retained_hoppings = hoppings[mask]
        training = self.reconstruct(
            retained_hoppings,
            coordinates,
            retained_representatives,
            lattice_period,
        )
        withheld = self.reconstruct(
            retained_hoppings,
            withheld_coordinates,
            retained_representatives,
            lattice_period,
        )
        training_residual = energies - training.real
        withheld_residual = withheld_parent - withheld.real
        omitted_norm = float(np.linalg.norm(hoppings[~mask]))
        design = np.exp(
            1j * np.outer(coordinates, retained_representatives * lattice_period)
        )
        direct = np.linalg.lstsq(design, energies, rcond=None)[0]
        direct_training = design @ direct
        curvature = float(
            -np.sum(
                np.square(retained_representatives * lattice_period) * retained_hoppings
            ).real
        )
        parseval = abs(
            float(np.sum(np.square(training_residual)))
            - coordinates.size * omitted_norm**2
        )
        return Periodic1DHoppingRangeDiagnostic(
            hopping_range,
            int(np.count_nonzero(mask)),
            omitted_norm,
            float(np.max(np.abs(training_residual))),
            float(np.sqrt(np.mean(np.square(training_residual)))),
            float(np.max(np.abs(withheld_residual))),
            float(np.sqrt(np.mean(np.square(withheld_residual)))),
            abs(float(np.ptp(withheld.real)) - float(np.ptp(withheld_parent))),
            curvature,
            float(np.linalg.norm(direct - retained_hoppings)),
            float(np.linalg.norm(direct_training - training)),
            parseval,
        )

    def calculate_parent_observables(
        self,
        definition: Periodic1DIsolatedBandCampaignDefinition,
        curvature_step: float,
    ) -> Periodic1DParentBandObservables:
        """Calculate parent bandwidth, boundary gap, and center curvature.

        Parameters
        ----------
        definition
            Versioned parent model and withheld-mesh controls.
        curvature_step
            Positive reduced-momentum central-difference step.

        Returns
        -------
        Periodic1DParentBandObservables
            Three separate parent scalar observables.
        """
        if type(definition) is not Periodic1DIsolatedBandCampaignDefinition:
            raise TypeError("definition uses the wrong campaign definition type")
        if type(curvature_step) is not float:
            raise TypeError("curvature_step must be a built-in float")
        if not np.isfinite(curvature_step) or curvature_step <= 0.0:
            raise ValueError("curvature_step must be finite and positive")
        cutoff = definition.plane_wave_cutoffs[-1]
        strength = definition.potential_strength.magnitude
        mesh = np.linspace(-0.5, 0.5, definition.withheld_mesh_size)
        parent = np.asarray(
            [
                self.plane_wave_eigensystem(float(k), strength, cutoff)[0][0]
                for k in mesh
            ]
        )
        center = np.asarray(
            [
                self.plane_wave_eigensystem(float(k), strength, cutoff)[0][0]
                for k in (-curvature_step, 0.0, curvature_step)
            ]
        )
        boundary = self.plane_wave_eigensystem(0.5, strength, cutoff)[0]
        curvature = float((center[0] - 2.0 * center[1] + center[2]) / curvature_step**2)
        return Periodic1DParentBandObservables(
            float(np.ptp(parent)),
            float(boundary[1] - boundary[0]),
            curvature,
        )
