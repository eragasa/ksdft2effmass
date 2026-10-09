"""Typed records for the periodic2d isolated-band campaign."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandCampaignDefinition:
    """Retain the closed dimensionless controls of the version-one campaign.

    Every real scalar is an exact built-in ``float`` in the documented dimensionless
    convention. Integer inventories contain exact built-in ``int`` values. Momentum
    pairs use reduced reciprocal coordinates in first-direction, second-direction
    order.

    Parameters
    ----------
    experiment_id
        Nonempty version-one experiment identity.
    lattice_period, reciprocal_vector, reciprocal_energy
        Positive dimensionless direct period, reciprocal primitive magnitude, and
        reciprocal energy scale, with ``lattice_period * reciprocal_vector = 2*pi``.
    lambda_x, lambda_y
        Positive isotropic cosine amplitudes.
    anisotropic_lambda_x, anisotropic_lambda_y, anisotropic_lambda_xy
        Anisotropic-control cosine amplitudes; the mixed amplitude may be zero.
    coupling_sequence
        Increasing nonnegative mixed-coupling values beginning at zero.
    plane_wave_cutoffs, plane_wave_reference_cutoff
        Increasing positive study cutoffs and a larger reference cutoff.
    finite_difference_points
        Increasing odd grid counts of at least five per direction.
    parent_sample_momenta
        Nonempty reduced-momentum pairs used for parent comparison.
    parent_coupling
        Nonnegative mixed coupling for parent comparison.
    compared_band_count, common_low_mode_cutoff
        Positive band count and square common-space cutoff.
    reciprocal_mesh_size, withheld_mesh_size
        Odd transform-mesh size and a strictly finer withheld mesh size.
    shell_squared_radii
        Increasing nonnegative point-group shell radii including the full mesh.
    effective_mass_step
        Positive dimensionless centered-difference step.
    minimum_neighbor_overlap, chern_integer_defect
        Positive topology controls; overlap lies strictly between zero and one.
    """

    experiment_id: str
    lattice_period: float
    reciprocal_vector: float
    reciprocal_energy: float
    lambda_x: float
    lambda_y: float
    anisotropic_lambda_x: float
    anisotropic_lambda_y: float
    anisotropic_lambda_xy: float
    coupling_sequence: tuple[float, ...]
    plane_wave_cutoffs: tuple[int, ...]
    plane_wave_reference_cutoff: int
    finite_difference_points: tuple[int, ...]
    parent_sample_momenta: tuple[tuple[float, float], ...]
    parent_coupling: float
    compared_band_count: int
    common_low_mode_cutoff: int
    reciprocal_mesh_size: int
    withheld_mesh_size: int
    shell_squared_radii: tuple[int, ...]
    effective_mass_step: float
    minimum_neighbor_overlap: float
    chern_integer_defect: float

    def __post_init__(self) -> None:
        """Validate exact types and all version-one control invariants."""
        if type(self.experiment_id) is not str:
            raise TypeError("experiment_id must be a built-in str")
        if not self.experiment_id:
            raise ValueError("experiment_id must be nonempty")
        real_fields = (
            ("lattice_period", self.lattice_period),
            ("reciprocal_vector", self.reciprocal_vector),
            ("reciprocal_energy", self.reciprocal_energy),
            ("lambda_x", self.lambda_x),
            ("lambda_y", self.lambda_y),
            ("anisotropic_lambda_x", self.anisotropic_lambda_x),
            ("anisotropic_lambda_y", self.anisotropic_lambda_y),
            ("anisotropic_lambda_xy", self.anisotropic_lambda_xy),
            ("parent_coupling", self.parent_coupling),
            ("effective_mass_step", self.effective_mass_step),
            ("minimum_neighbor_overlap", self.minimum_neighbor_overlap),
            ("chern_integer_defect", self.chern_integer_defect),
        )
        for name, value in real_fields:
            if type(value) is not float:
                raise TypeError(f"{name} must be a built-in float")
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
        positive = (
            self.lattice_period,
            self.reciprocal_vector,
            self.reciprocal_energy,
            self.lambda_x,
            self.lambda_y,
            self.anisotropic_lambda_x,
            self.anisotropic_lambda_y,
            self.effective_mass_step,
            self.minimum_neighbor_overlap,
            self.chern_integer_defect,
        )
        if not all(value > 0.0 for value in positive):
            raise ValueError("positive controls must be positive")
        if self.anisotropic_lambda_xy < 0.0 or self.parent_coupling < 0.0:
            raise ValueError("coupling controls must be nonnegative")
        if not np.isclose(
            self.lattice_period * self.reciprocal_vector,
            2.0 * np.pi,
            rtol=0.0,
            atol=2.0e-15,
        ):
            raise ValueError("lattice_period*reciprocal_vector must equal 2*pi")
        self._validate_real_inventory(self.coupling_sequence, "coupling_sequence")
        self._validate_integer_inventory(self.plane_wave_cutoffs, "plane_wave_cutoffs")
        self._validate_integer_inventory(
            self.finite_difference_points, "finite_difference_points"
        )
        self._validate_integer_inventory(
            self.shell_squared_radii, "shell_squared_radii"
        )
        if self.coupling_sequence[0] != 0.0:
            raise ValueError("coupling_sequence must begin at the separable limit")
        if any(value < 0.0 for value in self.coupling_sequence):
            raise ValueError("coupling_sequence must be nonnegative")
        integer_fields = (
            ("plane_wave_reference_cutoff", self.plane_wave_reference_cutoff),
            ("compared_band_count", self.compared_band_count),
            ("common_low_mode_cutoff", self.common_low_mode_cutoff),
            ("reciprocal_mesh_size", self.reciprocal_mesh_size),
            ("withheld_mesh_size", self.withheld_mesh_size),
        )
        for name, value in integer_fields:
            if type(value) is not int:
                raise TypeError(f"{name} must be a built-in int")
        if self.plane_wave_reference_cutoff <= self.plane_wave_cutoffs[-1]:
            raise ValueError("reference cutoff must exceed study cutoffs")
        if any(value < 1 for value in self.plane_wave_cutoffs):
            raise ValueError("plane-wave cutoffs must be positive")
        if any(value < 5 or value % 2 == 0 for value in self.finite_difference_points):
            raise ValueError("finite-difference sizes must be odd and at least five")
        if self.compared_band_count < 1:
            raise ValueError("compared_band_count must be positive")
        if self.common_low_mode_cutoff < 1:
            raise ValueError("common_low_mode_cutoff must be positive")
        if self.common_low_mode_cutoff > self.plane_wave_cutoffs[0]:
            raise ValueError("common_low_mode_cutoff must fit every plane-wave basis")
        if self.reciprocal_mesh_size < 5 or self.reciprocal_mesh_size % 2 == 0:
            raise ValueError("reciprocal mesh must be odd and at least five")
        if self.withheld_mesh_size <= self.reciprocal_mesh_size:
            raise ValueError("withheld mesh must be finer than the transform mesh")
        maximum_rep = self.reciprocal_mesh_size // 2
        if self.shell_squared_radii[-1] != 2 * maximum_rep * maximum_rep:
            raise ValueError("final shell must contain every mesh representative")
        if not 0.0 < self.minimum_neighbor_overlap < 1.0:
            raise ValueError("minimum_neighbor_overlap must lie in (0,1)")
        if (
            type(self.parent_sample_momenta) is not tuple
            or not self.parent_sample_momenta
        ):
            raise TypeError("parent_sample_momenta must be a nonempty tuple")
        for momentum in self.parent_sample_momenta:
            if type(momentum) is not tuple or len(momentum) != 2:
                raise TypeError("each parent momentum must be a pair tuple")
            if any(type(component) is not float for component in momentum):
                raise TypeError("parent momentum components must be built-in floats")
            if not all(np.isfinite(component) for component in momentum):
                raise ValueError("parent momentum components must be finite")

    @staticmethod
    def _validate_real_inventory(values: tuple[float, ...], name: str) -> None:
        if type(values) is not tuple or not values:
            raise TypeError(f"{name} must be a nonempty tuple")
        if any(type(value) is not float for value in values):
            raise TypeError(f"{name} must contain built-in floats")
        if not all(np.isfinite(value) for value in values):
            raise ValueError(f"{name} must contain finite values")
        if tuple(sorted(set(values))) != values:
            raise ValueError(f"{name} must be strictly increasing")

    @staticmethod
    def _validate_integer_inventory(values: tuple[int, ...], name: str) -> None:
        if type(values) is not tuple or not values:
            raise TypeError(f"{name} must be a nonempty tuple")
        if any(type(value) is not int for value in values):
            raise TypeError(f"{name} must contain built-in integers")
        if tuple(sorted(set(values))) != values:
            raise ValueError(f"{name} must be strictly increasing")


@dataclass(frozen=True, slots=True)
class Periodic2DIsolatedBandProvenance:
    """Represent explicit retained-compatible calculation provenance.

    Parameters
    ----------
    input_path, script_path
        Repository-relative identities retained by the version-one result.
    input_sha256, script_sha256
        Lowercase SHA-256 identities of the input and calculation script.
    python_version, numpy_version
        Retained runtime-version strings.
    scipy_algorithm
        Retained eigensolver algorithm identity.
    floating_point
        Retained floating-point convention.
    """

    input_path: str
    input_sha256: str
    script_path: str
    script_sha256: str
    python_version: str
    numpy_version: str
    scipy_algorithm: str
    floating_point: str

    def __post_init__(self) -> None:
        """Validate exact nonempty strings and lowercase SHA-256 identities."""
        for name, value in (
            ("input_path", self.input_path),
            ("script_path", self.script_path),
            ("python_version", self.python_version),
            ("numpy_version", self.numpy_version),
            ("scipy_algorithm", self.scipy_algorithm),
            ("floating_point", self.floating_point),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if not value:
                raise ValueError(f"{name} must be nonempty")
        for name, digest in (
            ("input_sha256", self.input_sha256),
            ("script_sha256", self.script_sha256),
        ):
            if type(digest) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError(f"{name} must be a lowercase SHA-256 digest")
