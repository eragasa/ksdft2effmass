"""Same-frame kinetic decomposition of finite Wannier operator meshes.

The records in this module consume already identified plane-wave coefficients,
canonical kinetic energies, parent eigenvalues, disentanglement matrices, and
Wannier gauge matrices. Native-file decoding and simulation provenance remain with
their integration owners. The construction neither executes electronic-structure
software nor identifies a continuous scalar potential.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from itertools import product

import numpy as np
import numpy.typing as npt

from ksdft2effmass.operators import (
    MODEL_SYSTEM_UNIT_CONVERTER,
    ComplexMatrixQuantity,
    MatrixQuantity,
    PhysicalUnit,
    Unitless,
    VectorQuantity,
)

type CellRepresentative3D = tuple[int, int, int]
type ComplexArray = npt.NDArray[np.complex128]


class WannierOperatorRole(StrEnum):
    """Distinguish the three represented operators in one decomposition."""

    HAMILTONIAN = "hamiltonian"
    KINETIC = "kinetic"
    NONKINETIC_REMAINDER = "nonkinetic-remainder"


@dataclass(frozen=True, slots=True, eq=False)
class PlaneWaveBandSample:
    """Retain parent-band coefficients and diagonal kinetic energies at one k point.

    Parameters
    ----------
    coefficients
        Unitless matrix with plane-wave/spinor coordinates in rows and ordered
        parent-band coordinates in columns.
    kinetic_energies
        Canonical kinetic energy for every coefficient row. Spinor coordinates, when
        present, repeat the corresponding spatial kinetic energy.

    Notes
    -----
    This record does not decode an FFT grid or establish coefficient normalization.
    Those conventions must be fixed before construction.
    """

    coefficients: ComplexMatrixQuantity
    kinetic_energies: VectorQuantity

    def __post_init__(self) -> None:
        """Validate coefficient, kinetic-energy, and parent-band dimensions."""
        self._check_args_coefficients()
        self._check_args_kinetic_energies()

    def _check_args_coefficients(self) -> None:
        """Validate one nonempty unitless coefficient matrix."""
        if type(self.coefficients) is not ComplexMatrixQuantity:
            raise TypeError("coefficients must be ComplexMatrixQuantity")
        if not isinstance(self.coefficients.unit, Unitless):
            raise ValueError("coefficients must be unitless")
        rows, columns = self.coefficients.magnitude.shape
        if rows == 0 or columns == 0:
            raise ValueError("coefficients must have nonzero dimensions")

    def _check_args_kinetic_energies(self) -> None:
        """Validate one physical energy per coefficient row."""
        if type(self.kinetic_energies) is not VectorQuantity:
            raise TypeError("kinetic_energies must be VectorQuantity")
        if not isinstance(self.kinetic_energies.unit, PhysicalUnit):
            raise ValueError("kinetic_energies must have a physical unit")
        _require_energy_unit(self.kinetic_energies.unit, "kinetic_energies")
        if self.kinetic_energies.magnitude.size != self.coefficient_count:
            raise ValueError(
                "kinetic-energy count must equal plane-wave coefficient rows"
            )

    @property
    def coefficient_count(self) -> int:
        """Return the flattened plane-wave/spinor coordinate count."""
        return int(self.coefficients.magnitude.shape[0])

    @property
    def band_count(self) -> int:
        """Return the ordered parent-band count."""
        return int(self.coefficients.magnitude.shape[1])


@dataclass(frozen=True, slots=True, eq=False)
class WannierFrameSample:
    """Retain the parent spectrum and same-k Wannier frame factors.

    ``disentanglement`` has logical shape ``(parent band, retained state)`` and
    ``gauge`` has shape ``(retained state, Wannier coordinate)``. Their product is
    the represented frame from Wannier coordinates into parent-band coordinates.
    """

    parent_eigenvalues: VectorQuantity
    disentanglement: ComplexMatrixQuantity
    gauge: ComplexMatrixQuantity

    def __post_init__(self) -> None:
        """Validate energy, unitless frame factors, and matrix dimensions."""
        self._check_args_parent_eigenvalues()
        self._check_args_frame_factors()

    def _check_args_parent_eigenvalues(self) -> None:
        """Validate a nonempty physical parent spectrum."""
        if type(self.parent_eigenvalues) is not VectorQuantity:
            raise TypeError("parent_eigenvalues must be VectorQuantity")
        if not isinstance(self.parent_eigenvalues.unit, PhysicalUnit):
            raise ValueError("parent_eigenvalues must have a physical unit")
        _require_energy_unit(self.parent_eigenvalues.unit, "parent_eigenvalues")
        if self.parent_eigenvalues.magnitude.size == 0:
            raise ValueError("parent_eigenvalues must be nonempty")

    def _check_args_frame_factors(self) -> None:
        """Validate unitless disentanglement and square gauge factors."""
        for name, matrix in (
            ("disentanglement", self.disentanglement),
            ("gauge", self.gauge),
        ):
            if type(matrix) is not ComplexMatrixQuantity:
                raise TypeError(f"{name} must be ComplexMatrixQuantity")
            if not isinstance(matrix.unit, Unitless):
                raise ValueError(f"{name} must be unitless")
        band_count, retained_count = self.disentanglement.magnitude.shape
        if band_count != self.parent_eigenvalues.magnitude.size:
            raise ValueError("disentanglement rows must equal parent eigenvalue count")
        if retained_count == 0:
            raise ValueError("disentanglement must retain at least one state")
        if self.gauge.magnitude.shape != (retained_count, retained_count):
            raise ValueError("gauge must be square on the retained coordinates")

    @property
    def band_count(self) -> int:
        """Return the parent-band count."""
        return int(self.disentanglement.magnitude.shape[0])

    @property
    def wannier_count(self) -> int:
        """Return the retained Wannier-coordinate count."""
        return int(self.disentanglement.magnitude.shape[1])


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDecompositionRequest:
    """Declare one ordered uniform-mesh same-frame decomposition.

    The reciprocal mesh is the unshifted half-open tensor product
    ``(i/N1, j/N2, k/N3)`` in C order. The request supplies explicit scientific and
    representation identities; none are inferred from matrix dimensions or spectra.
    """

    source_binding_identifier: str
    frame_identifier: str
    energy_reference: str
    hamiltonian_identifier: str
    kinetic_identifier: str
    nonkinetic_remainder_identifier: str
    fractional_kpoints: MatrixQuantity
    mesh_shape: tuple[int, int, int]
    plane_wave_samples: tuple[PlaneWaveBandSample, ...]
    frame_samples: tuple[WannierFrameSample, ...]
    output_energy_unit: PhysicalUnit
    coordinate_absolute_tolerance: float
    frame_absolute_tolerance: float
    diagnostic_absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate identities, ordered mesh, correlated samples, and tolerances."""
        self._check_args_identifiers()
        self._check_args_tolerances()
        self._check_args_mesh()
        self._check_args_samples()
        self._check_args_frames()

    def _check_args_identifiers(self) -> None:
        """Validate explicit nonempty identities and their distinct operator roles."""
        identifiers = {
            "source_binding_identifier": self.source_binding_identifier,
            "frame_identifier": self.frame_identifier,
            "energy_reference": self.energy_reference,
            "hamiltonian_identifier": self.hamiltonian_identifier,
            "kinetic_identifier": self.kinetic_identifier,
            "nonkinetic_remainder_identifier": (self.nonkinetic_remainder_identifier),
        }
        for name, value in identifiers.items():
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        operator_identifiers = (
            self.hamiltonian_identifier,
            self.kinetic_identifier,
            self.nonkinetic_remainder_identifier,
        )
        if len(set(operator_identifiers)) != 3:
            raise ValueError("represented operator identifiers must be distinct")
        if type(self.output_energy_unit) is not PhysicalUnit:
            raise TypeError("output_energy_unit must be PhysicalUnit")
        _require_energy_unit(self.output_energy_unit, "output_energy_unit")

    def _check_args_tolerances(self) -> None:
        """Validate finite nonnegative built-in floating-point tolerances."""
        for name, value in (
            ("coordinate_absolute_tolerance", self.coordinate_absolute_tolerance),
            ("frame_absolute_tolerance", self.frame_absolute_tolerance),
            ("diagnostic_absolute_tolerance", self.diagnostic_absolute_tolerance),
        ):
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    def _check_args_mesh(self) -> None:
        """Validate the declared mesh and exact unshifted sample order."""
        if type(self.fractional_kpoints) is not MatrixQuantity:
            raise TypeError("fractional_kpoints must be MatrixQuantity")
        if not isinstance(self.fractional_kpoints.unit, Unitless):
            raise ValueError("fractional_kpoints must be unitless")
        if type(self.mesh_shape) is not tuple or len(self.mesh_shape) != 3:
            raise TypeError("mesh_shape must contain three built-in integers")
        if any(type(value) is not int for value in self.mesh_shape):
            raise TypeError("mesh_shape must contain three built-in integers")
        if any(value <= 0 for value in self.mesh_shape):
            raise ValueError("mesh_shape entries must be positive")
        expected = _fractional_mesh(self.mesh_shape)
        if self.fractional_kpoints.magnitude.shape != expected.shape:
            raise ValueError("fractional_kpoints shape disagrees with mesh_shape")
        defect = float(np.max(np.abs(self.fractional_kpoints.magnitude - expected)))
        if defect > self.coordinate_absolute_tolerance:
            raise ValueError(
                "fractional_kpoints do not follow the declared half-open mesh order"
            )

    def _check_args_samples(self) -> None:
        """Validate sample counts, exact classes, dimensions, and energy units."""
        sample_count = self.fractional_kpoints.magnitude.shape[0]
        for name, samples, expected_type in (
            ("plane_wave_samples", self.plane_wave_samples, PlaneWaveBandSample),
            ("frame_samples", self.frame_samples, WannierFrameSample),
        ):
            if type(samples) is not tuple:
                raise TypeError(f"{name} must be a tuple")
            if len(samples) != sample_count:
                raise ValueError(f"{name} count must equal reciprocal-point count")
            if any(type(sample) is not expected_type for sample in samples):
                raise TypeError(f"{name} contains an invalid sample type")
        first_plane_wave = self.plane_wave_samples[0]
        first_frame = self.frame_samples[0]
        if first_plane_wave.band_count != first_frame.band_count:
            raise ValueError("plane-wave and frame parent-band counts must agree")
        for plane_wave, frame in zip(
            self.plane_wave_samples, self.frame_samples, strict=True
        ):
            if plane_wave.band_count != first_plane_wave.band_count:
                raise ValueError("parent-band count must be constant across the mesh")
            if frame.band_count != first_frame.band_count:
                raise ValueError("frame parent-band count must be constant")
            if frame.wannier_count != first_frame.wannier_count:
                raise ValueError("Wannier count must be constant across the mesh")
            MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
                plane_wave.kinetic_energies.unit, self.output_energy_unit
            )
            MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(
                frame.parent_eigenvalues.unit, self.output_energy_unit
            )

    def _check_args_frames(self) -> None:
        """Require isometric disentanglement and unitary gauge factors."""
        identity = np.eye(self.wannier_count, dtype=np.complex128)
        for sample in self.frame_samples:
            disentanglement = sample.disentanglement.magnitude
            gauge = sample.gauge.magnitude
            disentanglement_defect = float(
                np.linalg.norm(disentanglement.conj().T @ disentanglement - identity)
            )
            gauge_defect = float(np.linalg.norm(gauge.conj().T @ gauge - identity))
            if (
                max(disentanglement_defect, gauge_defect)
                > self.frame_absolute_tolerance
            ):
                raise ValueError(
                    "disentanglement and gauge factors must define an isometric frame"
                )

    @property
    def sample_count(self) -> int:
        """Return the reciprocal-point count."""
        return len(self.frame_samples)

    @property
    def band_count(self) -> int:
        """Return the parent-band count."""
        return self.frame_samples[0].band_count

    @property
    def wannier_count(self) -> int:
        """Return the retained Wannier-coordinate count."""
        return self.frame_samples[0].wannier_count


@dataclass(frozen=True, slots=True, eq=False)
class WannierRepresentedOperatorMesh3D:
    """Retain one represented operator in reciprocal and canonical lattice space."""

    identifier: str
    role: WannierOperatorRole
    source_binding_identifier: str
    frame_identifier: str
    energy_reference: str
    fractional_kpoints: MatrixQuantity
    mesh_shape: tuple[int, int, int]
    coordinate_absolute_tolerance: float
    reciprocal_matrices: tuple[ComplexMatrixQuantity, ...]
    representatives: tuple[CellRepresentative3D, ...]
    lattice_blocks: tuple[ComplexMatrixQuantity, ...]

    def __post_init__(self) -> None:
        """Validate identity, shared frame metadata, matrix dimensions, and ordering."""
        self._check_args_metadata()
        self._check_args_mesh()
        self._check_args_matrices()

    def _check_args_metadata(self) -> None:
        """Validate nonempty identities and explicit operator role."""
        for name, value in (
            ("identifier", self.identifier),
            ("source_binding_identifier", self.source_binding_identifier),
            ("frame_identifier", self.frame_identifier),
            ("energy_reference", self.energy_reference),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a string")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        if type(self.role) is not WannierOperatorRole:
            raise TypeError("role must be WannierOperatorRole")

    def _check_args_mesh(self) -> None:
        """Validate reciprocal and centered canonical lattice inventories."""
        if type(self.fractional_kpoints) is not MatrixQuantity:
            raise TypeError("fractional_kpoints must be MatrixQuantity")
        if not isinstance(self.fractional_kpoints.unit, Unitless):
            raise ValueError("fractional_kpoints must be unitless")
        if (
            type(self.mesh_shape) is not tuple
            or len(self.mesh_shape) != 3
            or any(type(value) is not int for value in self.mesh_shape)
        ):
            raise TypeError("mesh_shape must contain three built-in integers")
        expected_count = int(np.prod(self.mesh_shape))
        if expected_count <= 0:
            raise ValueError("mesh_shape entries must be positive")
        if type(self.coordinate_absolute_tolerance) is not float:
            raise TypeError("coordinate_absolute_tolerance must be a built-in float")
        if (
            not np.isfinite(self.coordinate_absolute_tolerance)
            or self.coordinate_absolute_tolerance < 0.0
        ):
            raise ValueError(
                "coordinate_absolute_tolerance must be finite and nonnegative"
            )
        expected_kpoints = _fractional_mesh(self.mesh_shape)
        if self.fractional_kpoints.magnitude.shape != expected_kpoints.shape:
            raise ValueError("fractional_kpoints shape disagrees with mesh_shape")
        coordinate_defect = float(
            np.max(np.abs(self.fractional_kpoints.magnitude - expected_kpoints))
        )
        if coordinate_defect > self.coordinate_absolute_tolerance:
            raise ValueError(
                "fractional_kpoints do not follow the declared half-open mesh order"
            )
        expected_representatives = _centered_representatives(self.mesh_shape)
        if self.representatives != expected_representatives:
            raise ValueError("representatives must use canonical centered FFT order")

    def _check_args_matrices(self) -> None:
        """Validate matching homogeneous reciprocal and lattice matrix families."""
        expected_count = int(np.prod(self.mesh_shape))
        for name, matrices in (
            ("reciprocal_matrices", self.reciprocal_matrices),
            ("lattice_blocks", self.lattice_blocks),
        ):
            if type(matrices) is not tuple or len(matrices) != expected_count:
                raise ValueError(f"{name} must contain one matrix per mesh point")
            if any(type(matrix) is not ComplexMatrixQuantity for matrix in matrices):
                raise TypeError(f"{name} must contain ComplexMatrixQuantity values")
        first = self.reciprocal_matrices[0]
        dimension = first.magnitude.shape[0]
        if dimension == 0 or first.magnitude.shape != (dimension, dimension):
            raise ValueError(
                "represented operator matrices must be nonempty and square"
            )
        if not isinstance(first.unit, PhysicalUnit):
            raise ValueError("represented operator matrices must have a physical unit")
        _require_energy_unit(first.unit, "represented operator matrices")
        for matrix in (*self.reciprocal_matrices, *self.lattice_blocks):
            if matrix.magnitude.shape != (dimension, dimension):
                raise ValueError(
                    "all represented operator matrices must have one shape"
                )
            if matrix.unit != first.unit:
                raise ValueError("all represented operator matrices must share a unit")
        expected_blocks, _ = _fourier_transform(
            [matrix.magnitude for matrix in self.reciprocal_matrices],
            self.mesh_shape,
        )
        if any(
            not np.array_equal(expected, actual.magnitude)
            for expected, actual in zip(
                expected_blocks, self.lattice_blocks, strict=True
            )
        ):
            raise ValueError(
                "lattice blocks must be the canonical Fourier transform of "
                "reciprocal matrices"
            )

    @property
    def wannier_count(self) -> int:
        """Return the represented Wannier-coordinate count."""
        return int(self.reciprocal_matrices[0].magnitude.shape[0])


@dataclass(frozen=True, slots=True)
class WannierKineticDecompositionDiagnostics:
    """Retain numerical defects for one same-frame finite-mesh construction."""

    gauge_unitarity_maximum_frobenius: float
    disentanglement_isometry_maximum_frobenius: float
    combined_frame_isometry_maximum_frobenius: float
    hamiltonian_hermiticity_maximum_frobenius: float
    kinetic_hermiticity_maximum_frobenius: float
    nonkinetic_remainder_hermiticity_maximum_frobenius: float
    reciprocal_decomposition_maximum_frobenius: float
    hamiltonian_roundtrip_maximum_frobenius: float
    kinetic_roundtrip_maximum_frobenius: float
    nonkinetic_remainder_roundtrip_maximum_frobenius: float
    lattice_decomposition_maximum_frobenius: float
    absolute_tolerance: float

    def __post_init__(self) -> None:
        """Validate finite nonnegative defects and tolerance."""
        values = (
            (
                "gauge_unitarity_maximum_frobenius",
                self.gauge_unitarity_maximum_frobenius,
            ),
            (
                "disentanglement_isometry_maximum_frobenius",
                self.disentanglement_isometry_maximum_frobenius,
            ),
            (
                "combined_frame_isometry_maximum_frobenius",
                self.combined_frame_isometry_maximum_frobenius,
            ),
            (
                "hamiltonian_hermiticity_maximum_frobenius",
                self.hamiltonian_hermiticity_maximum_frobenius,
            ),
            (
                "kinetic_hermiticity_maximum_frobenius",
                self.kinetic_hermiticity_maximum_frobenius,
            ),
            (
                "nonkinetic_remainder_hermiticity_maximum_frobenius",
                self.nonkinetic_remainder_hermiticity_maximum_frobenius,
            ),
            (
                "reciprocal_decomposition_maximum_frobenius",
                self.reciprocal_decomposition_maximum_frobenius,
            ),
            (
                "hamiltonian_roundtrip_maximum_frobenius",
                self.hamiltonian_roundtrip_maximum_frobenius,
            ),
            (
                "kinetic_roundtrip_maximum_frobenius",
                self.kinetic_roundtrip_maximum_frobenius,
            ),
            (
                "nonkinetic_remainder_roundtrip_maximum_frobenius",
                self.nonkinetic_remainder_roundtrip_maximum_frobenius,
            ),
            (
                "lattice_decomposition_maximum_frobenius",
                self.lattice_decomposition_maximum_frobenius,
            ),
            ("absolute_tolerance", self.absolute_tolerance),
        )
        for name, value in values:
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value) or value < 0.0:
                raise ValueError(f"{name} must be finite and nonnegative")

    @property
    def passes(self) -> bool:
        """Return whether decomposition, Hermiticity, and round trips pass."""
        assessed = (
            self.hamiltonian_hermiticity_maximum_frobenius,
            self.kinetic_hermiticity_maximum_frobenius,
            self.nonkinetic_remainder_hermiticity_maximum_frobenius,
            self.reciprocal_decomposition_maximum_frobenius,
            self.hamiltonian_roundtrip_maximum_frobenius,
            self.kinetic_roundtrip_maximum_frobenius,
            self.nonkinetic_remainder_roundtrip_maximum_frobenius,
            self.lattice_decomposition_maximum_frobenius,
        )
        return max(assessed) <= self.absolute_tolerance


@dataclass(frozen=True, slots=True, eq=False)
class WannierKineticDecompositionResult:
    """Retain three distinct same-frame operators and their numerical diagnostics."""

    request: WannierKineticDecompositionRequest
    hamiltonian: WannierRepresentedOperatorMesh3D
    kinetic: WannierRepresentedOperatorMesh3D
    nonkinetic_remainder: WannierRepresentedOperatorMesh3D
    diagnostics: WannierKineticDecompositionDiagnostics

    def __post_init__(self) -> None:
        """Validate roles, request identities, shared frames, and decomposition."""
        self._check_args_types_and_roles()
        self._check_args_correlations()
        self._check_args_construction_and_diagnostics()

    def _check_args_types_and_roles(self) -> None:
        """Validate exact aggregate component classes and operator roles."""
        if type(self.request) is not WannierKineticDecompositionRequest:
            raise TypeError("request must be WannierKineticDecompositionRequest")
        for name, operator, role in (
            ("hamiltonian", self.hamiltonian, WannierOperatorRole.HAMILTONIAN),
            ("kinetic", self.kinetic, WannierOperatorRole.KINETIC),
            (
                "nonkinetic_remainder",
                self.nonkinetic_remainder,
                WannierOperatorRole.NONKINETIC_REMAINDER,
            ),
        ):
            if type(operator) is not WannierRepresentedOperatorMesh3D:
                raise TypeError(f"{name} must be WannierRepresentedOperatorMesh3D")
            if operator.role is not role:
                raise ValueError(f"{name} has the wrong operator role")
        if type(self.diagnostics) is not WannierKineticDecompositionDiagnostics:
            raise TypeError(
                "diagnostics must be WannierKineticDecompositionDiagnostics"
            )

    def _check_args_correlations(self) -> None:
        """Require every represented operator to retain the request metadata."""
        expected_identifiers = (
            self.request.hamiltonian_identifier,
            self.request.kinetic_identifier,
            self.request.nonkinetic_remainder_identifier,
        )
        for operator, identifier in zip(
            (self.hamiltonian, self.kinetic, self.nonkinetic_remainder),
            expected_identifiers,
            strict=True,
        ):
            if operator.identifier != identifier:
                raise ValueError("operator identifier disagrees with request")
            if (
                operator.source_binding_identifier
                != self.request.source_binding_identifier
            ):
                raise ValueError("operator source binding disagrees with request")
            if operator.frame_identifier != self.request.frame_identifier:
                raise ValueError("operator frame disagrees with request")
            if operator.energy_reference != self.request.energy_reference:
                raise ValueError("operator energy reference disagrees with request")
            if operator.mesh_shape != self.request.mesh_shape:
                raise ValueError("operator mesh shape disagrees with request")
            if operator.coordinate_absolute_tolerance != (
                self.request.coordinate_absolute_tolerance
            ):
                raise ValueError("operator coordinate tolerance disagrees with request")
            if operator.wannier_count != self.request.wannier_count:
                raise ValueError("operator Wannier count disagrees with request")
            if any(
                matrix.unit != self.request.output_energy_unit
                for matrix in (
                    *operator.reciprocal_matrices,
                    *operator.lattice_blocks,
                )
            ):
                raise ValueError("operator energy unit disagrees with request")
            if operator.fractional_kpoints is not self.request.fractional_kpoints:
                raise ValueError(
                    "operator must retain the exact request k-point record"
                )

    def _check_args_construction_and_diagnostics(self) -> None:
        """Require represented values and diagnostics to match the request."""
        construction = _construct_reciprocal_values(self.request)
        operators_and_expected = (
            (self.hamiltonian, construction.hamiltonian),
            (self.kinetic, construction.kinetic),
            (self.nonkinetic_remainder, construction.remainder),
        )
        for operator, expected_values in operators_and_expected:
            if any(
                not np.array_equal(actual.magnitude, expected)
                for actual, expected in zip(
                    operator.reciprocal_matrices, expected_values, strict=True
                )
            ):
                raise ValueError(
                    "reciprocal matrices do not match the declared request construction"
                )

        hamiltonian_blocks, hamiltonian_reconstructed = _fourier_transform(
            construction.hamiltonian, self.request.mesh_shape
        )
        kinetic_blocks, kinetic_reconstructed = _fourier_transform(
            construction.kinetic, self.request.mesh_shape
        )
        remainder_blocks, remainder_reconstructed = _fourier_transform(
            construction.remainder, self.request.mesh_shape
        )
        expected_diagnostics = {
            "gauge_unitarity_maximum_frobenius": construction.gauge_defect,
            "disentanglement_isometry_maximum_frobenius": (
                construction.disentanglement_defect
            ),
            "combined_frame_isometry_maximum_frobenius": construction.frame_defect,
            "hamiltonian_hermiticity_maximum_frobenius": _hermiticity_defect(
                construction.hamiltonian
            ),
            "kinetic_hermiticity_maximum_frobenius": _hermiticity_defect(
                construction.kinetic
            ),
            "nonkinetic_remainder_hermiticity_maximum_frobenius": (
                _hermiticity_defect(construction.remainder)
            ),
            "reciprocal_decomposition_maximum_frobenius": (
                _array_decomposition_defect(
                    construction.hamiltonian,
                    construction.kinetic,
                    construction.remainder,
                )
            ),
            "hamiltonian_roundtrip_maximum_frobenius": _roundtrip_defect(
                construction.hamiltonian, hamiltonian_reconstructed
            ),
            "kinetic_roundtrip_maximum_frobenius": _roundtrip_defect(
                construction.kinetic, kinetic_reconstructed
            ),
            "nonkinetic_remainder_roundtrip_maximum_frobenius": (
                _roundtrip_defect(construction.remainder, remainder_reconstructed)
            ),
            "lattice_decomposition_maximum_frobenius": (
                _array_decomposition_defect(
                    hamiltonian_blocks, kinetic_blocks, remainder_blocks
                )
            ),
        }
        epsilon = np.finfo(np.float64).eps
        for name, expected in expected_diagnostics.items():
            actual = getattr(self.diagnostics, name)
            if not np.isclose(actual, expected, rtol=0.0, atol=epsilon):
                raise ValueError(f"{name} diagnostic is inconsistent")
        if self.diagnostics.absolute_tolerance != (
            self.request.diagnostic_absolute_tolerance
        ):
            raise ValueError("diagnostic tolerance disagrees with request")


class WannierKineticDecompositionConstructor:
    r"""Construct ``H^W``, ``T^W``, and their same-frame non-kinetic remainder.

    For parent-band coefficients ``C(k)``, diagonal plane-wave kinetic energies
    ``t(k)``, parent eigenvalues ``epsilon(k)``, disentanglement ``D(k)``, and gauge
    ``U(k)``, the represented retained frame is ``W(k) = D(k) U(k)`` and

    .. math::

       T^W = W^\dagger C^\dagger\operatorname{diag}(t)CW,
       \qquad
       H^W = W^\dagger\operatorname{diag}(\epsilon)W.

    The remainder is defined only after both operands occupy this identical frame.
    Its canonical finite-mesh lattice blocks use a negative-exponent forward discrete
    Fourier transform. The result is not identified as a continuous scalar potential.
    """

    __slots__ = ()

    def execute(
        self, request: WannierKineticDecompositionRequest
    ) -> WannierKineticDecompositionResult:
        """Return the three represented operators and numerical diagnostics."""
        if type(request) is not WannierKineticDecompositionRequest:
            raise TypeError("request must be WannierKineticDecompositionRequest")
        construction = _construct_reciprocal_values(request)
        hamiltonian_values = construction.hamiltonian
        kinetic_values = construction.kinetic
        remainder_values = construction.remainder
        hamiltonian_blocks, hamiltonian_reconstructed = _fourier_transform(
            hamiltonian_values, request.mesh_shape
        )
        kinetic_blocks, kinetic_reconstructed = _fourier_transform(
            kinetic_values, request.mesh_shape
        )
        remainder_blocks, remainder_reconstructed = _fourier_transform(
            remainder_values, request.mesh_shape
        )
        unit = request.output_energy_unit
        representatives = _centered_representatives(request.mesh_shape)
        hamiltonian_operator = _operator_mesh(
            request,
            request.hamiltonian_identifier,
            WannierOperatorRole.HAMILTONIAN,
            hamiltonian_values,
            hamiltonian_blocks,
            representatives,
            unit,
        )
        kinetic_operator = _operator_mesh(
            request,
            request.kinetic_identifier,
            WannierOperatorRole.KINETIC,
            kinetic_values,
            kinetic_blocks,
            representatives,
            unit,
        )
        remainder_operator = _operator_mesh(
            request,
            request.nonkinetic_remainder_identifier,
            WannierOperatorRole.NONKINETIC_REMAINDER,
            remainder_values,
            remainder_blocks,
            representatives,
            unit,
        )
        diagnostics = WannierKineticDecompositionDiagnostics(
            gauge_unitarity_maximum_frobenius=construction.gauge_defect,
            disentanglement_isometry_maximum_frobenius=(
                construction.disentanglement_defect
            ),
            combined_frame_isometry_maximum_frobenius=construction.frame_defect,
            hamiltonian_hermiticity_maximum_frobenius=_hermiticity_defect(
                hamiltonian_values
            ),
            kinetic_hermiticity_maximum_frobenius=_hermiticity_defect(kinetic_values),
            nonkinetic_remainder_hermiticity_maximum_frobenius=(
                _hermiticity_defect(remainder_values)
            ),
            reciprocal_decomposition_maximum_frobenius=_array_decomposition_defect(
                hamiltonian_values, kinetic_values, remainder_values
            ),
            hamiltonian_roundtrip_maximum_frobenius=_roundtrip_defect(
                hamiltonian_values, hamiltonian_reconstructed
            ),
            kinetic_roundtrip_maximum_frobenius=_roundtrip_defect(
                kinetic_values, kinetic_reconstructed
            ),
            nonkinetic_remainder_roundtrip_maximum_frobenius=_roundtrip_defect(
                remainder_values, remainder_reconstructed
            ),
            lattice_decomposition_maximum_frobenius=_array_decomposition_defect(
                hamiltonian_blocks, kinetic_blocks, remainder_blocks
            ),
            absolute_tolerance=request.diagnostic_absolute_tolerance,
        )
        return WannierKineticDecompositionResult(
            request,
            hamiltonian_operator,
            kinetic_operator,
            remainder_operator,
            diagnostics,
        )


@dataclass(slots=True)
class _WannierReciprocalConstruction:
    """Hold one ephemeral same-frame reciprocal construction."""

    hamiltonian: list[ComplexArray]
    kinetic: list[ComplexArray]
    remainder: list[ComplexArray]
    gauge_defect: float
    disentanglement_defect: float
    frame_defect: float


def _construct_reciprocal_values(
    request: WannierKineticDecompositionRequest,
) -> _WannierReciprocalConstruction:
    """Construct reciprocal operators and frame defects from one request."""
    hamiltonian: list[ComplexArray] = []
    kinetic: list[ComplexArray] = []
    remainder: list[ComplexArray] = []
    gauge_defects: list[float] = []
    disentanglement_defects: list[float] = []
    frame_defects: list[float] = []
    identity = np.eye(request.wannier_count, dtype=np.complex128)
    for plane_wave, frame_sample in zip(
        request.plane_wave_samples, request.frame_samples, strict=True
    ):
        coefficients = plane_wave.coefficients.magnitude
        kinetic_energies = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            plane_wave.kinetic_energies, request.output_energy_unit
        ).magnitude
        eigenvalues = MODEL_SYSTEM_UNIT_CONVERTER.convert_vector(
            frame_sample.parent_eigenvalues, request.output_energy_unit
        ).magnitude
        disentanglement = frame_sample.disentanglement.magnitude
        gauge = frame_sample.gauge.magnitude
        frame = disentanglement @ gauge
        parent_kinetic = coefficients.conj().T @ (
            kinetic_energies[:, np.newaxis] * coefficients
        )
        hamiltonian_matrix = frame.conj().T @ (eigenvalues[:, np.newaxis] * frame)
        kinetic_matrix = frame.conj().T @ parent_kinetic @ frame
        remainder_matrix = hamiltonian_matrix - kinetic_matrix
        hamiltonian.append(hamiltonian_matrix)
        kinetic.append(kinetic_matrix)
        remainder.append(remainder_matrix)
        gauge_defects.append(float(np.linalg.norm(gauge.conj().T @ gauge - identity)))
        disentanglement_defects.append(
            float(np.linalg.norm(disentanglement.conj().T @ disentanglement - identity))
        )
        frame_defects.append(float(np.linalg.norm(frame.conj().T @ frame - identity)))
    return _WannierReciprocalConstruction(
        hamiltonian,
        kinetic,
        remainder,
        max(gauge_defects),
        max(disentanglement_defects),
        max(frame_defects),
    )


def _fractional_mesh(shape: tuple[int, int, int]) -> npt.NDArray[np.float64]:
    axes = tuple(np.arange(size, dtype=np.float64) / size for size in shape)
    return np.stack(np.meshgrid(*axes, indexing="ij"), axis=-1).reshape(-1, 3)


def _centered_representatives(
    shape: tuple[int, int, int],
) -> tuple[CellRepresentative3D, ...]:
    axes = tuple(range(-(size // 2), -(size // 2) + size) for size in shape)
    return tuple(
        (first, second, third)
        for first, second, third in product(axes[0], axes[1], axes[2])
    )


def _fourier_transform(
    values: list[ComplexArray], shape: tuple[int, int, int]
) -> tuple[list[ComplexArray], list[ComplexArray]]:
    dimension = values[0].shape[0]
    reciprocal = np.asarray(values, dtype=np.complex128).reshape(
        (*shape, dimension, dimension)
    )
    unshifted = np.fft.fftn(reciprocal, axes=(0, 1, 2), norm="forward")
    centered = np.fft.fftshift(unshifted, axes=(0, 1, 2))
    reconstructed = np.fft.ifftn(
        np.fft.ifftshift(centered, axes=(0, 1, 2)),
        axes=(0, 1, 2),
        norm="forward",
    )
    return (
        [matrix for matrix in centered.reshape(-1, dimension, dimension)],
        [matrix for matrix in reconstructed.reshape(-1, dimension, dimension)],
    )


def _operator_mesh(
    request: WannierKineticDecompositionRequest,
    identifier: str,
    role: WannierOperatorRole,
    reciprocal_values: list[ComplexArray],
    lattice_values: list[ComplexArray],
    representatives: tuple[CellRepresentative3D, ...],
    unit: PhysicalUnit,
) -> WannierRepresentedOperatorMesh3D:
    return WannierRepresentedOperatorMesh3D(
        identifier=identifier,
        role=role,
        source_binding_identifier=request.source_binding_identifier,
        frame_identifier=request.frame_identifier,
        energy_reference=request.energy_reference,
        fractional_kpoints=request.fractional_kpoints,
        mesh_shape=request.mesh_shape,
        coordinate_absolute_tolerance=request.coordinate_absolute_tolerance,
        reciprocal_matrices=tuple(
            ComplexMatrixQuantity(value, unit) for value in reciprocal_values
        ),
        representatives=representatives,
        lattice_blocks=tuple(
            ComplexMatrixQuantity(value, unit) for value in lattice_values
        ),
    )


def _hermiticity_defect(values: list[ComplexArray]) -> float:
    return float(max(np.linalg.norm(value - value.conj().T) for value in values))


def _roundtrip_defect(
    values: list[ComplexArray], reconstructed: list[ComplexArray]
) -> float:
    return float(
        max(
            np.linalg.norm(value - candidate)
            for value, candidate in zip(values, reconstructed, strict=True)
        )
    )


def _array_decomposition_defect(
    hamiltonian: list[ComplexArray],
    kinetic: list[ComplexArray],
    remainder: list[ComplexArray],
) -> float:
    return float(
        max(
            np.linalg.norm(h_value - (t_value + r_value))
            for h_value, t_value, r_value in zip(
                hamiltonian, kinetic, remainder, strict=True
            )
        )
    )


def _require_energy_unit(unit: PhysicalUnit, name: str) -> None:
    """Require a physical unit convertible to joules."""
    try:
        MODEL_SYSTEM_UNIT_CONVERTER.conversion_factor(unit, PhysicalUnit("joule"))
    except ValueError as error:
        raise ValueError(f"{name} must use a physical energy unit") from error


__all__ = [
    "PlaneWaveBandSample",
    "WannierFrameSample",
    "WannierKineticDecompositionConstructor",
    "WannierKineticDecompositionDiagnostics",
    "WannierKineticDecompositionRequest",
    "WannierKineticDecompositionResult",
    "WannierOperatorRole",
    "WannierRepresentedOperatorMesh3D",
]
