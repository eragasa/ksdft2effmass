"""Run independently separated continuum-refinement axes for the synthetic 1D defect."""

from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import dataclass
from pathlib import Path
from typing import cast

import numpy as np
import numpy.typing as npt

from ksdft2effmass.periodic1d.campaign.serialization import (
    Periodic1DCampaignJsonDecoder,
)
from ksdft2effmass.serialization.json import JsonValue

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealVector = npt.NDArray[np.float64]
type IntegerVector = npt.NDArray[np.int64]
type ProfileFamily = str


@dataclass(frozen=True, slots=True)
class ContinuumRefinementSourceIdentity:
    """Identify one immutable source artifact.

    Parameters
    ----------
    path
        Nonempty repository-relative path of an authenticated compact source.
    sha256
        Lowercase 64-character SHA-256 content identity.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    path: str
    sha256: str

    def __post_init__(self) -> None:
        if not self.path or len(self.sha256) != 64:
            raise ValueError("source identity is invalid")


@dataclass(frozen=True, slots=True)
class ContinuumRepresentedContract:
    """Define units, basis, reference, and profile normalizations.

    Parameters
    ----------
    reference_lattice_period
        Positive reference primitive-cell period in the declared length unit.
    length_unit
        Exact unit label for every campaign length quantity.
    energy_unit
        Exact unit label for every campaign energy quantity.
    basis
        Exact label for the represented basis and its ordering convention.
    energy_reference
        Exact label for the zero and alignment convention of represented energies.
    fixed_integrated_magnitude
        Positive integrated defect strength held fixed on the scale axis.
    fixed_peak_magnitude
        Positive peak defect strength held fixed on the profile axis.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    reference_lattice_period: float
    length_unit: str
    energy_unit: str
    basis: str
    energy_reference: str
    fixed_integrated_magnitude: float
    fixed_peak_magnitude: float

    def __post_init__(self) -> None:
        if (
            self.reference_lattice_period <= 0.0
            or not self.length_unit
            or not self.energy_unit
            or not self.basis
            or not self.energy_reference
            or self.fixed_integrated_magnitude <= 0.0
            or self.fixed_peak_magnitude <= 0.0
        ):
            raise ValueError("represented contract is invalid")


@dataclass(frozen=True, slots=True)
class ContinuumComparisonContract:
    """Own frozen numerical and crossover criteria.

    Parameters
    ----------
    physical_low_momentum_cutoff
        Positive reciprocal cutoff defining the low-momentum diagnostic region.
    brillouin_edge_fraction
        Fractional reciprocal cutoff defining the Brillouin-edge diagnostic region.
    bound_state_edge_margin
        Positive energy margin required between a bound state and the parent-band
        edge.
    continuum_mesh_binding_tolerance
        Maximum accepted binding-energy change under continuum mesh refinement.
    continuum_mesh_projector_tolerance
        Maximum accepted projector change under continuum mesh refinement.
    finite_domain_binding_tolerance
        Maximum accepted binding-energy change under domain enlargement.
    finite_domain_boundary_probability_tolerance
        Maximum accepted boundary probability on the finite-domain axis.
    lattice_supercell_binding_tolerance
        Maximum accepted binding-energy change under lattice-supercell enlargement.
    lattice_supercell_boundary_probability_tolerance
        Maximum accepted boundary probability on the lattice-supercell axis.
    relative_binding_tolerance
        Maximum accepted relative discrepancy in binding energy.
    projector_frobenius_tolerance
        Maximum accepted Frobenius discrepancy between bound-state projectors.
    compressed_operator_tolerance
        Maximum Frobenius discrepancy between compressed represented operators.
    cross_coupling_tolerance
        Maximum accepted coupling between retained and complementary subspaces.
    brillouin_edge_weight_tolerance
        Maximum accepted state weight in the Brillouin-edge diagnostic region.
    require_equal_bound_state_count
        Whether compared refinement levels must have equal bound-state counts.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    physical_low_momentum_cutoff: float
    brillouin_edge_fraction: float
    bound_state_edge_margin: float
    continuum_mesh_binding_tolerance: float
    continuum_mesh_projector_tolerance: float
    finite_domain_binding_tolerance: float
    finite_domain_boundary_probability_tolerance: float
    lattice_supercell_binding_tolerance: float
    lattice_supercell_boundary_probability_tolerance: float
    relative_binding_tolerance: float
    projector_frobenius_tolerance: float
    compressed_operator_tolerance: float
    cross_coupling_tolerance: float
    brillouin_edge_weight_tolerance: float
    require_equal_bound_state_count: bool

    def __post_init__(self) -> None:
        numeric = (
            self.physical_low_momentum_cutoff,
            self.brillouin_edge_fraction,
            self.bound_state_edge_margin,
            self.continuum_mesh_binding_tolerance,
            self.continuum_mesh_projector_tolerance,
            self.finite_domain_binding_tolerance,
            self.finite_domain_boundary_probability_tolerance,
            self.lattice_supercell_binding_tolerance,
            self.lattice_supercell_boundary_probability_tolerance,
            self.relative_binding_tolerance,
            self.projector_frobenius_tolerance,
            self.compressed_operator_tolerance,
            self.cross_coupling_tolerance,
            self.brillouin_edge_weight_tolerance,
        )
        if any(value <= 0.0 or not np.isfinite(value) for value in numeric):
            raise ValueError("comparison tolerances must be finite and positive")
        if self.brillouin_edge_fraction >= 0.5:
            raise ValueError("Brillouin edge fraction must be below one half")


@dataclass(frozen=True, slots=True)
class ContinuumRefinementCampaignInput:
    """Represent every frozen refinement axis.

    Parameters
    ----------
    experiment_id
        Exact stable identity of the retained synthetic campaign.
    sources
        Ordered authenticated source identities required by the campaign.
    represented
        Explicit units, basis, energy reference, and normalization conventions.
    mesh_domain
        Positive represented-domain length held fixed on the mesh-refinement axis.
    mesh_width
        Positive defect width held fixed on the mesh-refinement axis.
    mesh_family
        Defect-profile family used by the mesh-refinement axis.
    mesh_counts
        Strictly increasing centered Fourier basis sizes for mesh refinement.
    domain_width
        Fixed positive defect width used along the domain-refinement axis.
    domain_family
        Defect-profile family used by the finite-domain refinement axis.
    domain_spacing
        Fixed positive real-space spacing used along the domain-refinement axis.
    domain_lengths
        Strictly increasing represented-domain lengths for finite-domain refinement.
    supercell_spacing
        Positive lattice spacing held fixed on the supercell-refinement axis.
    supercell_width
        Positive defect width held fixed on the supercell-refinement axis.
    supercell_family
        Defect-profile family used by the lattice-supercell axis.
    supercell_counts
        Strictly increasing lattice-supercell sizes used by the refinement axis.
    scale_domain
        Positive represented-domain length held fixed on the scaling axis.
    scale_width
        Positive defect width held fixed on the scaling axis.
    scale_family
        Defect-profile family used by the scaling axis.
    scale_spacings
        Strictly decreasing positive real-space spacings for continuum scaling.
    profile_domain
        Positive represented-domain length held fixed on the profile-family axis.
    profile_spacing
        Positive real-space spacing held fixed on the profile-family axis.
    profile_widths
        Strictly increasing defect widths used by the profile-family comparison.
    profile_families
        Ordered supported defect families compared at fixed peak magnitude.
    comparison
        Frozen tolerances and crossover criteria for continuum–lattice comparisons.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    experiment_id: str
    sources: tuple[ContinuumRefinementSourceIdentity, ...]
    represented: ContinuumRepresentedContract
    mesh_domain: float
    mesh_width: float
    mesh_family: ProfileFamily
    mesh_counts: tuple[int, ...]
    domain_width: float
    domain_family: ProfileFamily
    domain_spacing: float
    domain_lengths: tuple[float, ...]
    supercell_spacing: float
    supercell_width: float
    supercell_family: ProfileFamily
    supercell_counts: tuple[int, ...]
    scale_domain: float
    scale_width: float
    scale_family: ProfileFamily
    scale_spacings: tuple[float, ...]
    profile_domain: float
    profile_spacing: float
    profile_widths: tuple[float, ...]
    profile_families: tuple[ProfileFamily, ...]
    comparison: ContinuumComparisonContract

    def __post_init__(self) -> None:
        if not self.experiment_id or len(self.sources) != 3:
            raise ValueError("experiment identity or sources are invalid")
        for values in (self.mesh_counts, self.supercell_counts):
            if not values or any(value < 8 or value % 2 for value in values):
                raise ValueError("mode and cell counts must be positive even values")
        if tuple(sorted(self.mesh_counts)) != self.mesh_counts:
            raise ValueError("mesh counts must be strictly ordered")
        if tuple(sorted(self.supercell_counts)) != self.supercell_counts:
            raise ValueError("supercell counts must be strictly ordered")
        if tuple(sorted(self.domain_lengths)) != self.domain_lengths:
            raise ValueError("domain lengths must be strictly ordered")
        if tuple(sorted(self.profile_widths)) != self.profile_widths:
            raise ValueError("profile widths must be strictly ordered")
        if tuple(sorted(self.scale_spacings, reverse=True)) != self.scale_spacings:
            raise ValueError("lattice spacings must be ordered coarse to fine")
        if self.profile_families != ("fixed-integrated", "fixed-peak"):
            raise ValueError("profile families are not the frozen pair")
        positive = (
            self.mesh_domain,
            self.mesh_width,
            self.domain_width,
            self.domain_spacing,
            self.supercell_spacing,
            self.supercell_width,
            self.scale_domain,
            self.scale_width,
            self.profile_domain,
            self.profile_spacing,
            *self.domain_lengths,
            *self.scale_spacings,
            *self.profile_widths,
        )
        if any(value <= 0.0 or not np.isfinite(value) for value in positive):
            raise ValueError("refinement values must be finite and positive")


@dataclass(frozen=True, slots=True)
class ContinuumParentRecord:
    """Retain the accepted scalar parent as an immutable represented dispersion.

    Parameters
    ----------
    displacements
        Ordered signed hopping displacements paired with the supplied coefficients.
    hoppings
        Ordered finite hopping coefficients or blocks in their declared displacement
        order.
    lower_edge
        Lower edge of the finite parent spectrum in the declared energy unit.
    parabolic_coefficient
        Finite coefficient of the continuum parabolic dispersion.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    displacements: IntegerVector
    hoppings: ComplexVector
    lower_edge: float
    parabolic_coefficient: float

    def __post_init__(self) -> None:
        displacements = np.asarray(self.displacements, dtype=np.int64)
        hoppings = np.asarray(self.hoppings, dtype=np.complex128)
        if (
            displacements.ndim != 1
            or hoppings.shape != displacements.shape
            or displacements.size < 3
            or not np.all(np.isfinite(hoppings))
            or not np.isfinite(self.lower_edge)
            or self.parabolic_coefficient <= 0.0
        ):
            raise ValueError("parent record is invalid")
        immutable_r = np.frombuffer(displacements.tobytes(), dtype=np.int64)
        immutable_t = np.frombuffer(hoppings.tobytes(), dtype=np.complex128)
        object.__setattr__(self, "displacements", immutable_r)
        object.__setattr__(self, "hoppings", immutable_t)


@dataclass(frozen=True, slots=True)
class ContinuumSpectrumResult:
    """Record the lowest state and all below-edge eigenvalues.

    Parameters
    ----------
    energy
        Candidate bound-state energy in the declared campaign energy unit.
    binding
        Positive binding energy measured below the declared lower band edge.
    bound_count
        Number of eigenvalues below the declared parent-band edge.
    state
        Normalized complex state in the declared finite basis order.
    boundary_probability
        Probability mass in the campaign-defined boundary region.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    energy: float
    binding: float
    bound_count: int
    state: ComplexVector
    boundary_probability: float

    def __post_init__(self) -> None:
        state = np.asarray(self.state, dtype=np.complex128)
        if (
            state.ndim != 1
            or not np.all(np.isfinite(state))
            or not np.isfinite(self.energy)
            or self.binding < 0.0
            or self.bound_count < 0
            or not 0.0 <= self.boundary_probability <= 1.0
        ):
            raise ValueError("spectrum result is invalid")
        immutable = np.frombuffer(state.tobytes(), dtype=np.complex128)
        object.__setattr__(self, "state", immutable)


class ContinuumRefinementInputDeserializer:
    """Parse the closed version-1 refinement input."""

    __slots__ = ("_decoder",)

    def __init__(self) -> None:
        """Bind the maintained strict campaign JSON decoder."""
        self._decoder = Periodic1DCampaignJsonDecoder()

    def execute(self, payload: bytes) -> ContinuumRefinementCampaignInput:
        """Decode strict UTF-8 JSON into the closed version-one input.

        Parameters
        ----------
        payload
            Exact immutable encoded JSON bytes.

        Returns
        -------
        ContinuumRefinementCampaignInput
            Closed immutable version-one continuum-refinement input.

        Raises
        ------
        TypeError
            An argument does not have the required exact public type.
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        if type(payload) is not bytes:
            raise TypeError("payload must be exact bytes")
        root = self._decoder.document(payload)
        if set(root) != {
            "schema_version",
            "experiment_id",
            "evidence_status",
            "source_identities",
            "represented_contract",
            "continuum_mesh_axis",
            "continuum_domain_axis",
            "lattice_supercell_axis",
            "lattice_scale_axis",
            "profile_width_axis",
            "comparison_contract",
        }:
            raise ValueError("input fields must match the version-one contract")
        if self._integer(root["schema_version"], "schema version") != 1:
            raise ValueError("unsupported schema version")
        if root["evidence_status"] != "synthetic test data":
            raise ValueError("evidence status mismatch")
        sources = tuple(
            ContinuumRefinementSourceIdentity(
                self._string(item["path"], "source path"),
                self._string(item["sha256"], "source sha256"),
            )
            for item in self._records(root["source_identities"], "sources")
        )
        represented = self._mapping(root["represented_contract"], "represented")
        mesh = self._mapping(root["continuum_mesh_axis"], "mesh")
        domain = self._mapping(root["continuum_domain_axis"], "domain")
        supercell = self._mapping(root["lattice_supercell_axis"], "supercell")
        scale = self._mapping(root["lattice_scale_axis"], "scale")
        profile = self._mapping(root["profile_width_axis"], "profile")
        comparison = self._mapping(root["comparison_contract"], "comparison")
        return ContinuumRefinementCampaignInput(
            self._string(root["experiment_id"], "experiment id"),
            sources,
            ContinuumRepresentedContract(
                self._real(represented["reference_lattice_period"], "period"),
                self._string(represented["length_unit"], "length unit"),
                self._string(represented["energy_unit"], "energy unit"),
                self._string(represented["basis"], "basis"),
                self._string(represented["energy_reference"], "energy reference"),
                self._real(
                    represented["fixed_integrated_magnitude"], "integrated magnitude"
                ),
                self._real(represented["fixed_peak_magnitude"], "peak magnitude"),
            ),
            self._real(mesh["domain_length"], "mesh domain"),
            self._real(mesh["profile_width"], "mesh width"),
            self._string(mesh["profile_family"], "mesh family"),
            self._integers(mesh["mode_counts"], "mesh counts"),
            self._real(domain["profile_width"], "domain width"),
            self._string(domain["profile_family"], "domain family"),
            self._real(domain["spectral_spacing"], "domain spacing"),
            self._reals(domain["domain_lengths"], "domain lengths"),
            self._real(supercell["lattice_spacing"], "supercell spacing"),
            self._real(supercell["profile_width"], "supercell width"),
            self._string(supercell["profile_family"], "supercell family"),
            self._integers(supercell["cell_counts"], "supercell counts"),
            self._real(scale["domain_length"], "scale domain"),
            self._real(scale["profile_width"], "scale width"),
            self._string(scale["profile_family"], "scale family"),
            self._reals(scale["lattice_spacings"], "scale spacings"),
            self._real(profile["domain_length"], "profile domain"),
            self._real(profile["lattice_spacing"], "profile spacing"),
            self._reals(profile["widths"], "profile widths"),
            self._strings(profile["families"], "profile families"),
            ContinuumComparisonContract(
                self._real(comparison["physical_low_momentum_cutoff"], "cutoff"),
                self._real(comparison["brillouin_edge_fraction"], "edge fraction"),
                self._real(comparison["bound_state_edge_margin"], "edge margin"),
                self._real(
                    comparison["continuum_mesh_binding_tolerance"],
                    "mesh binding tolerance",
                ),
                self._real(
                    comparison["continuum_mesh_projector_tolerance"],
                    "mesh projector tolerance",
                ),
                self._real(
                    comparison["finite_domain_binding_tolerance"],
                    "domain binding tolerance",
                ),
                self._real(
                    comparison["finite_domain_boundary_probability_tolerance"],
                    "domain boundary tolerance",
                ),
                self._real(
                    comparison["lattice_supercell_binding_tolerance"],
                    "supercell binding tolerance",
                ),
                self._real(
                    comparison["lattice_supercell_boundary_probability_tolerance"],
                    "supercell boundary tolerance",
                ),
                self._real(
                    comparison["relative_binding_tolerance"],
                    "relative binding tolerance",
                ),
                self._real(
                    comparison["projector_frobenius_tolerance"],
                    "projector tolerance",
                ),
                self._real(
                    comparison["compressed_operator_tolerance"],
                    "operator tolerance",
                ),
                self._real(comparison["cross_coupling_tolerance"], "cross tolerance"),
                self._real(
                    comparison["brillouin_edge_weight_tolerance"],
                    "edge weight tolerance",
                ),
                self._boolean(
                    comparison["require_equal_bound_state_count"],
                    "count requirement",
                ),
            ),
        )

    @staticmethod
    def _mapping(value: JsonValue, field: str) -> dict[str, JsonValue]:
        if type(value) is not dict:
            raise TypeError(f"{field} must be an object")
        return value

    @classmethod
    def _records(cls, value: JsonValue, field: str) -> tuple[dict[str, JsonValue], ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._mapping(item, field) for item in value)

    @staticmethod
    def _string(value: JsonValue, field: str) -> str:
        if type(value) is not str or not value:
            raise TypeError(f"{field} must be a nonempty string")
        return value

    @classmethod
    def _strings(cls, value: JsonValue, field: str) -> tuple[str, ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._string(item, field) for item in value)

    @staticmethod
    def _integer(value: JsonValue, field: str) -> int:
        if type(value) is not int:
            raise TypeError(f"{field} must be an int excluding bool")
        return value

    @classmethod
    def _integers(cls, value: JsonValue, field: str) -> tuple[int, ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._integer(item, field) for item in value)

    @staticmethod
    def _real(value: JsonValue, field: str) -> float:
        if type(value) is int:
            result = float(value)
        elif type(value) is float:
            result = value
        else:
            raise TypeError(f"{field} must be a real number excluding bool")
        if not np.isfinite(result):
            raise ValueError(f"{field} must be finite")
        return result

    @classmethod
    def _reals(cls, value: JsonValue, field: str) -> tuple[float, ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        return tuple(cls._real(item, field) for item in value)

    @staticmethod
    def _boolean(value: JsonValue, field: str) -> bool:
        if type(value) is not bool:
            raise TypeError(f"{field} must be bool")
        return value


class ContinuumParentLoader:
    """Verify source identities and load the accepted scalar parent."""

    __slots__ = ("_decoder",)

    def __init__(self) -> None:
        """Bind the maintained strict campaign JSON decoder."""
        self._decoder = Periodic1DCampaignJsonDecoder()

    def execute(
        self, repository_root: Path, config: ContinuumRefinementCampaignInput
    ) -> ContinuumParentRecord:
        """Authenticate configured sources and decode the periodic parent.

        Parameters
        ----------
        repository_root
            Explicit absolute root confining authenticated repository-relative access.
        config
            Closed continuum-refinement campaign input.

        Returns
        -------
        ContinuumParentRecord
            Authenticated parent dispersion and hopping data in explicit displacement
            order.

        Raises
        ------
        TypeError
            An argument does not have the required exact public type.
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        values: dict[str, JsonValue] | None = None
        for source in config.sources:
            path = repository_root / source.path
            payload = path.read_bytes()
            if hashlib.sha256(payload).hexdigest() != source.sha256:
                raise ValueError(f"source identity mismatch: {source.path}")
            if source.path.endswith("periodic-1d/result.json"):
                values = self._mapping(
                    self._decoder.document(payload), "periodic result"
                )
        if values is None:
            raise ValueError("periodic parent source is missing")
        reduction = self._mapping(
            values["isolated_band_reduction"], "isolated reduction"
        )
        representatives = self._integers(
            reduction["hopping_representatives_cells"], "displacements"
        )
        encoded = reduction["hopping_coefficients"]
        if type(encoded) is not list:
            raise TypeError("hopping coefficients must be an array")
        coefficients: list[complex] = []
        for item in encoded:
            if type(item) is not list or len(item) != 2:
                raise TypeError("hopping coefficient must be a real-imaginary pair")
            coefficients.append(
                complex(
                    self._real(item[0], "hopping real"),
                    self._real(item[1], "hopping imaginary"),
                )
            )
        displacements = np.asarray(representatives, dtype=np.int64)
        hoppings = np.asarray(coefficients, dtype=np.complex128)
        lower_edge = float(np.real(np.sum(hoppings)))
        coefficient = float(
            np.real(-0.5 * np.sum((2.0 * np.pi * displacements) ** 2 * hoppings))
        )
        return ContinuumParentRecord(displacements, hoppings, lower_edge, coefficient)

    @staticmethod
    def _mapping(value: JsonValue, field: str) -> dict[str, JsonValue]:
        if type(value) is not dict:
            raise TypeError(f"{field} must be an object")
        return value

    @classmethod
    def _integers(cls, value: JsonValue, field: str) -> tuple[int, ...]:
        if type(value) is not list:
            raise TypeError(f"{field} must be an array")
        result: list[int] = []
        for item in value:
            if type(item) is not int:
                raise TypeError(f"{field} entries must be integers excluding booleans")
            result.append(item)
        return tuple(result)

    @staticmethod
    def _real(value: JsonValue, field: str) -> float:
        if type(value) is int:
            result = float(value)
        elif type(value) is float:
            result = value
        else:
            raise TypeError(f"{field} must be a real scalar excluding booleans")
        if not np.isfinite(result):
            raise ValueError(f"{field} must be finite")
        return result


class ContinuumHamiltonianConstructor:
    """Construct compatible continuum and scaled-lattice Fourier matrices.

    Parameters
    ----------
    parent
        Explicit parent contract or authenticated parent data used by the operation.
    contract
        Typed ``contract`` value in this owner's documented convention.
    """

    __slots__ = ("_contract", "_parent")

    def __init__(
        self, parent: ContinuumParentRecord, contract: ContinuumRepresentedContract
    ) -> None:
        self._parent = parent
        self._contract = contract

    @staticmethod
    def modes(count: int) -> IntegerVector:
        """Return centered integer Fourier-mode labels.

        Parameters
        ----------
        count
            Exact size of the finite represented basis.

        Returns
        -------
        IntegerVector
            Ordered centered integer Fourier labels used by the represented matrix.
        """
        return np.arange(-count // 2, count // 2, dtype=np.int64)

    def continuum(
        self, count: int, length: float, width: float, family: ProfileFamily
    ) -> ComplexMatrix:
        """Construct a spectral continuum representation with exact coefficients.

        Parameters
        ----------
        count
            Exact size of the finite represented basis.
        length
            Positive finite represented-domain length in the campaign length unit.
        width
            Positive defect-profile width in the campaign length unit.
        family
            Explicit supported defect-profile family.

        Returns
        -------
        ComplexMatrix
            Continuum Hamiltonian in centered Fourier-mode order.

        Raises
        ------
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        modes = self.modes(count)
        wave_numbers = modes.astype(np.float64) / length
        # The continuum parent is the explicit parabolic band-edge model, while the
        # defect matrix uses exact Fourier coefficients for the selected profile.
        kinetic = self._parent.lower_edge + self._parent.parabolic_coefficient * (
            wave_numbers**2
        )
        differences = modes[:, None] - modes[None, :]
        exponent = (
            -2.0 * np.pi**2 * width**2 * (differences.astype(np.float64) / length) ** 2
        )
        if family == "fixed-integrated":
            prefactor = -self._contract.fixed_integrated_magnitude / length
        elif family == "fixed-peak":
            prefactor = (
                -self._contract.fixed_peak_magnitude
                * np.sqrt(2.0 * np.pi)
                * width
                / length
            )
        else:
            raise ValueError(f"unsupported profile family {family}")
        matrix = np.diag(kinetic).astype(np.complex128)
        matrix += prefactor * np.exp(exponent)
        self._check_hermitian(matrix)
        return matrix

    def lattice(
        self, count: int, spacing: float, width: float, family: ProfileFamily
    ) -> ComplexMatrix:
        """Construct the scaled lattice representation in the same Fourier ordering.

        Parameters
        ----------
        count
            Exact size of the finite represented basis.
        spacing
            Positive real-space grid spacing in the campaign length unit.
        width
            Positive defect-profile width in the campaign length unit.
        family
            Explicit supported defect-profile family.

        Returns
        -------
        ComplexMatrix
            Scaled lattice Hamiltonian in the same centered Fourier-mode order.
        """
        length = count * spacing
        modes = self.modes(count)
        physical_wave_numbers = modes.astype(np.float64) / length
        reduced_momenta = spacing * physical_wave_numbers
        # Evaluate the accepted periodic parent at the scaled reduced momenta before
        # applying the 1/a^2 continuum scaling; do not substitute the parabola here.
        phases = np.exp(
            2j * np.pi * reduced_momenta[:, None] * self._parent.displacements[None, :]
        )
        base_dispersion = np.real(phases @ self._parent.hoppings)
        kinetic = (
            self._parent.lower_edge
            + (base_dispersion - self._parent.lower_edge) / spacing**2
        )
        potential = self._sampled_profile(count, spacing, width, family)
        coefficients = np.fft.fft(potential) / count
        # Modular differences implement periodic convolution in the same centered
        # Fourier label order used by the continuum matrix.
        differences = (modes[:, None] - modes[None, :]) % count
        matrix = np.diag(kinetic).astype(np.complex128)
        matrix += coefficients[differences]
        self._check_hermitian(matrix)
        return matrix

    def _sampled_profile(
        self, count: int, spacing: float, width: float, family: ProfileFamily
    ) -> RealVector:
        length = count * spacing
        positions = spacing * np.arange(count, dtype=np.float64)
        periodic = np.zeros(count, dtype=np.float64)
        for image in range(-4, 5):
            periodic += np.exp(-0.5 * ((positions + image * length) / width) ** 2)
        if family == "fixed-integrated":
            scale = -self._contract.fixed_integrated_magnitude / (
                np.sqrt(2.0 * np.pi) * width
            )
        elif family == "fixed-peak":
            scale = -self._contract.fixed_peak_magnitude
        else:
            raise ValueError(f"unsupported profile family {family}")
        return np.asarray(scale * periodic, dtype=np.float64)

    @staticmethod
    def _check_hermitian(matrix: ComplexMatrix) -> None:
        residual = float(np.max(np.abs(matrix - matrix.conj().T)))
        if residual > 1e-12 or not np.all(np.isfinite(matrix)):
            raise ValueError(f"represented Hamiltonian is not Hermitian: {residual}")


class BoundSpectrumResolver:
    """Resolve finite spectra and localization diagnostics.

    Parameters
    ----------
    edge
        Lower parent-band edge in the declared energy unit.
    margin
        Typed ``margin`` value in this owner's documented convention.
    """

    __slots__ = ("_edge", "_margin")

    def __init__(self, edge: float, margin: float) -> None:
        self._edge = edge
        self._margin = margin

    def execute(self, matrix: ComplexMatrix, length: float) -> ContinuumSpectrumResult:
        """Resolve the lowest state and finite-domain spectral diagnostics.

        Parameters
        ----------
        matrix
            Finite complex matrix in the explicitly declared basis order.
        length
            Positive finite represented-domain length in the campaign length unit.

        Returns
        -------
        ContinuumSpectrumResult
            Lowest-state energy, binding, count, state, and boundary diagnostic.
        """
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        state = np.asarray(eigenvectors[:, 0], dtype=np.complex128)
        energy = float(eigenvalues[0])
        binding = max(0.0, self._edge - energy)
        bound_count = int(np.count_nonzero(eigenvalues < self._edge - self._margin))
        boundary = self._boundary_probability(state, length)
        return ContinuumSpectrumResult(energy, binding, bound_count, state, boundary)

    @staticmethod
    def _boundary_probability(state: ComplexVector, length: float) -> float:
        count = state.size
        modes = ContinuumHamiltonianConstructor.modes(count)
        points = np.arange(count, dtype=np.float64)
        # The unitary centered-mode transform preserves probability exactly, so the
        # boundary diagnostic is independent of arbitrary eigenvector phase.
        transform = np.exp(2j * np.pi * np.outer(points, modes) / count) / np.sqrt(
            count
        )
        real_state = transform @ state
        distances = np.minimum(
            points * length / count, length - points * length / count
        )
        return float(np.sum(np.abs(real_state[distances >= length / 4.0]) ** 2))


class BoundStateComparator:
    """Compare one-dimensional projectors across compatible Fourier label sets."""

    __slots__ = ()

    def execute(
        self,
        left: ComplexVector,
        left_modes: IntegerVector,
        right: ComplexVector,
        right_modes: IntegerVector,
    ) -> float:
        """Return the Frobenius distance between compatible rank-one projectors.

        Parameters
        ----------
        left
            First normalized state in its explicitly supplied Fourier order.
        left_modes
            Ordered integer Fourier labels corresponding one-to-one with ``left``.
        right
            Second normalized state in its explicitly supplied Fourier order.
        right_modes
            Ordered integer Fourier labels corresponding one-to-one with ``right``.

        Returns
        -------
        float
            Frobenius distance between the compatible rank-one projectors.
        """
        right_by_mode = {
            int(mode): right[index] for index, mode in enumerate(right_modes)
        }
        overlap = sum(
            np.conj(left[index]) * right_by_mode.get(int(mode), 0.0j)
            for index, mode in enumerate(left_modes)
        )
        left_norm = float(np.vdot(left, left).real)
        right_norm = float(np.vdot(right, right).real)
        fidelity = min(
            1.0,
            max(0.0, float(abs(overlap) ** 2 / (left_norm * right_norm))),
        )
        return float(np.sqrt(2.0 * (1.0 - fidelity)))


class OperatorDifferenceAnalyzer:
    """Analyze compatible lattice-minus-continuum represented differences.

    Parameters
    ----------
    cutoff
        Typed ``cutoff`` value in this owner's documented convention.
    edge_fraction
        Typed ``edge_fraction`` value in this owner's documented convention.
    """

    __slots__ = ("_cutoff", "_edge_fraction")

    def __init__(self, cutoff: float, edge_fraction: float) -> None:
        self._cutoff = cutoff
        self._edge_fraction = edge_fraction

    def execute(
        self,
        lattice: ComplexMatrix,
        continuum: ComplexMatrix,
        state: ComplexVector,
        length: float,
        spacing: float,
    ) -> tuple[float, float, float]:
        """Return compressed, cross-block, and Brillouin-edge diagnostics.

        Parameters
        ----------
        lattice
            Finite lattice represented Hamiltonian in the declared common basis.
        continuum
            Continuum represented Hamiltonian in centered Fourier-mode order.
        state
            Normalized complex state in the declared finite basis order.
        length
            Positive finite represented-domain length in the campaign length unit.
        spacing
            Positive real-space grid spacing in the campaign length unit.

        Returns
        -------
        tuple[float, float, float]
            Compressed-block norm, cross-block norm, and Brillouin-edge state weight.

        Raises
        ------
        ValueError
            An argument violates a schema, domain, identity, or correlation invariant.
        """
        if lattice.shape != continuum.shape:
            raise ValueError(
                "operator comparison requires equal represented dimensions"
            )
        modes = ContinuumHamiltonianConstructor.modes(lattice.shape[0])
        wave_numbers = modes.astype(np.float64) / length
        low = np.abs(wave_numbers) <= self._cutoff
        high = ~low
        difference = lattice - continuum
        # Keep low-sector model error distinct from coupling into the discarded
        # high-momentum sector; neither norm is a proxy for the other.
        compressed = difference[np.ix_(low, low)]
        compressed_norm = float(np.max(np.abs(np.linalg.eigvalsh(compressed))))
        cross = difference[np.ix_(low, high)]
        cross_norm = (
            float(np.linalg.svd(cross, compute_uv=False)[0]) if cross.size else 0.0
        )
        edge = np.abs(spacing * wave_numbers) >= self._edge_fraction
        edge_weight = float(np.sum(np.abs(state[edge]) ** 2))
        return compressed_norm, cross_norm, edge_weight


@dataclass(frozen=True, slots=True)
class ContinuumRefinementProvenance:
    """Represent explicit retained-compatible execution provenance.

    Parameters
    ----------
    input_sha256
        Lowercase SHA-256 identity of the exact retained input bytes.
    implementation_path
        Optional explicit repository-relative path of the executing implementation.
    implementation_sha256
        Optional lowercase SHA-256 identity of the executing implementation bytes.
    python_version
        Explicit nonempty Python version retained as software provenance.
    numpy_version
        Explicit nonempty NumPy version retained as software provenance.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    input_sha256: str
    implementation_path: str | None
    implementation_sha256: str | None
    python_version: str
    numpy_version: str

    def __post_init__(self) -> None:
        """Validate paths, versions, and lowercase SHA-256 identities."""
        if not self.python_version or not self.numpy_version:
            raise ValueError("provenance versions must be nonempty")
        if (self.implementation_path is None) != (self.implementation_sha256 is None):
            raise ValueError("implementation path and identity must appear together")
        if self.implementation_path is not None and not self.implementation_path:
            raise ValueError("implementation path must be nonempty when supplied")
        digests = (
            (self.input_sha256,)
            if self.implementation_sha256 is None
            else (self.input_sha256, self.implementation_sha256)
        )
        for digest in digests:
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("provenance digests must be lowercase SHA-256")


class ContinuumRefinementCampaignCalculator:
    """Execute the separated refinement axes and frozen crossover decisions.

    Parameters
    ----------
    config
        Closed continuum-refinement campaign input.
    parent
        Explicit parent contract or authenticated parent data used by the operation.
    """

    __slots__ = ("_builder", "_config", "_operators", "_parent", "_spectrum", "_states")

    def __init__(
        self, config: ContinuumRefinementCampaignInput, parent: ContinuumParentRecord
    ) -> None:
        self._config = config
        self._parent = parent
        self._builder = ContinuumHamiltonianConstructor(parent, config.represented)
        self._spectrum = BoundSpectrumResolver(
            parent.lower_edge, config.comparison.bound_state_edge_margin
        )
        self._states = BoundStateComparator()
        self._operators = OperatorDifferenceAnalyzer(
            config.comparison.physical_low_momentum_cutoff,
            config.comparison.brillouin_edge_fraction,
        )

    def execute(
        self, provenance: ContinuumRefinementProvenance
    ) -> dict[str, JsonValue]:
        """Calculate every separated axis and the bounded crossover assessment.

        Parameters
        ----------
        provenance
            Structured identities of authenticated inputs, implementation, and software
            versions.

        Returns
        -------
        dict[str, JsonValue]
            Closed result mapping containing separated axes and bounded crossover
            decisions.
        """
        mesh_records, mesh_pass = self._mesh_axis()
        domain_records, domain_pass = self._domain_axis()
        supercell_records, supercell_pass = self._supercell_axis()
        scale_records, scale_boundary = self._scale_axis()
        profile_families = self._profile_axis()
        support_pass = mesh_pass and domain_pass and supercell_pass
        family_boundaries: dict[str, JsonValue] = {}
        for family_value in profile_families:
            family = cast(dict[str, JsonValue], family_value)
            family_boundaries[cast(str, family["family"])] = family["crossover_width"]
        fixed_integrated = family_boundaries["fixed-integrated"]
        stable_comparison = support_pass and scale_boundary is not None
        profile_crossover = fixed_integrated is not None
        return {
            "schema_version": 1,
            "experiment_id": self._config.experiment_id,
            "calculation_status": "calculated synthetic numerical-verification result",
            "evidence_status": "synthetic test data",
            "represented_contract": {
                "basis": self._config.represented.basis,
                "length_unit": self._config.represented.length_unit,
                "energy_unit": self._config.represented.energy_unit,
                "energy_reference": self._config.represented.energy_reference,
                "operator_difference_order": "scaled lattice minus parabolic continuum",
                "parent_lower_edge": self._parent.lower_edge,
                "parabolic_coefficient": self._parent.parabolic_coefficient,
            },
            "continuum_mesh_axis": {
                "records": mesh_records,
                "latest_step_pass": mesh_pass,
            },
            "continuum_domain_axis": {
                "records": domain_records,
                "latest_step_pass": domain_pass,
            },
            "lattice_supercell_axis": {
                "records": supercell_records,
                "latest_step_pass": supercell_pass,
            },
            "lattice_scale_axis": {
                "records": scale_records,
                "largest_spacing_with_persistent_pass": scale_boundary,
            },
            "profile_width_axis": {"families": profile_families},
            "crossover_assessment": {
                "supporting_axes_pass": support_pass,
                "fixed_integrated_crossover_width": fixed_integrated,
                "fixed_peak_crossover_width": family_boundaries["fixed-peak"],
                "lattice_scale_persistent_pass_spacing": scale_boundary,
                "stable_lattice_scale_comparison": stable_comparison,
                "profile_defined_crossover_established": profile_crossover,
                "interpretation": (
                    "The lattice-scale sequence has a persistent bounded pass under "
                    "the frozen criteria, while neither profile-width family defines "
                    "a crossover because at least one separate criterion continues "
                    "to fail. This is not an infinite-volume theorem, material "
                    "validation, or uncertainty quantification."
                    if stable_comparison and not profile_crossover
                    else (
                        "A bounded synthetic comparison and profile-defined crossover "
                        "are established only for the frozen represented problem."
                        if stable_comparison
                        else (
                            "No bounded continuum comparison satisfies every frozen "
                            "criterion."
                        )
                    )
                ),
            },
            "error_accounting": {
                "continuum_discretization": (
                    "isolated by mode-count refinement at fixed domain and profile"
                ),
                "finite_domain": (
                    "isolated by continuum-domain refinement at fixed spectral "
                    "spacing and profile"
                ),
                "periodic_image": (
                    "isolated by lattice-supercell refinement at fixed lattice "
                    "spacing and profile"
                ),
                "lattice_scale": (
                    "isolated by scaling the accepted dispersion at fixed physical "
                    "domain and profile"
                ),
                "profile_model": (
                    "fixed-integrated and fixed-peak width families remain separate"
                ),
                "operator_model": (
                    "compressed and cross-block lattice-minus-continuum residuals "
                    "remain separate"
                ),
                "spectral_and_state": (
                    "binding, bound-state count, projector defect, and "
                    "Brillouin-edge weight remain separate"
                ),
                "scientific_validation": "not performed",
                "uncertainty_quantification": "not performed",
            },
            "literature_map": [
                {
                    "limit": "finite-rank impurity resolvent",
                    "references": ["Koster and Slater (1954)"],
                    "applicability": "method precedent, not a continuum result",
                },
                {
                    "limit": "weak slowly varying band-edge homogenization",
                    "references": [
                        "Hoefer and Weinstein (2011)",
                        "Duchene, Vukicevic, and Weinstein (2015)",
                    ],
                    "applicability": (
                        "motivates the scale-separated envelope comparison; theorem "
                        "hypotheses are not claimed for this finite synthetic parent"
                    ),
                },
                {
                    "limit": "discrete-to-continuum norm-resolvent convergence",
                    "references": ["Nakamura and Tadano (2021)"],
                    "applicability": (
                        "motivates explicit changing-space and lattice-scale control; "
                        "no theorem is reproduced"
                    ),
                },
                {
                    "limit": "finite-volume bound-state effects",
                    "references": ["Koenig, Lee, and Hammer (2011)"],
                    "applicability": (
                        "general precedent only; the represented one-dimensional "
                        "image law is measured directly"
                    ),
                },
                {
                    "limit": "semiconductor effective-mass and central-cell boundary",
                    "references": [
                        "Kohn and Luttinger (1955)",
                        "Gamble et al. (2015)",
                    ],
                    "applicability": (
                        "scope boundary only; no silicon or multivalley calculation "
                        "is performed"
                    ),
                },
            ],
            "limitations": [
                (
                    "The accepted isolated-band parent is a finite represented "
                    "synthetic model."
                ),
                (
                    "A profile-width crossover changes the defect family and is not "
                    "itself a continuum limit."
                ),
                (
                    "The lattice-scale sequence is finite and does not prove "
                    "asymptotic convergence."
                ),
                "Only the lowest nondegenerate bound-state projector is compared.",
                (
                    "No silicon, dopant, DFT, production Wannier, scientific "
                    "validation, transferability, or UQ claim is made."
                ),
            ],
            "provenance": {
                "input_sha256": provenance.input_sha256,
                **(
                    {
                        "implementation_identities": [
                            {
                                "path": provenance.implementation_path,
                                "sha256": provenance.implementation_sha256,
                            }
                        ]
                    }
                    if provenance.implementation_path is not None
                    else {}
                ),
                "source_identities": [
                    {"path": source.path, "sha256": source.sha256}
                    for source in self._config.sources
                ],
                "python": provenance.python_version,
                "numpy": provenance.numpy_version,
            },
        }

    def _mesh_axis(self) -> tuple[list[JsonValue], bool]:
        spectra: list[ContinuumSpectrumResult] = []
        matrices: list[ComplexMatrix] = []
        for count in self._config.mesh_counts:
            matrix = self._builder.continuum(
                count,
                self._config.mesh_domain,
                self._config.mesh_width,
                self._config.mesh_family,
            )
            matrices.append(matrix)
            spectra.append(self._spectrum.execute(matrix, self._config.mesh_domain))
        reference = spectra[-1]
        reference_modes = self._builder.modes(self._config.mesh_counts[-1])
        records: list[JsonValue] = []
        for count, matrix, spectrum in zip(
            self._config.mesh_counts, matrices, spectra, strict=True
        ):
            defect = self._states.execute(
                spectrum.state,
                self._builder.modes(count),
                reference.state,
                reference_modes,
            )
            records.append(
                {
                    "mode_count": count,
                    "spectral_spacing": self._config.mesh_domain / count,
                    "binding_energy": spectrum.binding,
                    "bound_state_count": spectrum.bound_count,
                    "boundary_probability": spectrum.boundary_probability,
                    "binding_defect_from_finest": abs(
                        spectrum.binding - reference.binding
                    ),
                    "projector_defect_from_finest": defect,
                    "operator_sha256": self._matrix_sha256(matrix),
                }
            )
        previous = spectra[-2]
        latest_defect = self._states.execute(
            previous.state,
            self._builder.modes(self._config.mesh_counts[-2]),
            reference.state,
            reference_modes,
        )
        passed = (
            abs(previous.binding - reference.binding)
            <= self._config.comparison.continuum_mesh_binding_tolerance
            and latest_defect
            <= self._config.comparison.continuum_mesh_projector_tolerance
        )
        return records, passed

    def _domain_axis(self) -> tuple[list[JsonValue], bool]:
        spectra: list[ContinuumSpectrumResult] = []
        records: list[JsonValue] = []
        for length in self._config.domain_lengths:
            count = round(length / self._config.domain_spacing)
            matrix = self._builder.continuum(
                count, length, self._config.domain_width, self._config.domain_family
            )
            spectrum = self._spectrum.execute(matrix, length)
            spectra.append(spectrum)
            records.append(
                {
                    "domain_length": length,
                    "mode_count": count,
                    "binding_energy": spectrum.binding,
                    "bound_state_count": spectrum.bound_count,
                    "boundary_probability": spectrum.boundary_probability,
                    "operator_sha256": self._matrix_sha256(matrix),
                }
            )
        reference = spectra[-1]
        for record, spectrum in zip(records, spectra, strict=True):
            cast(dict[str, JsonValue], record)["binding_defect_from_largest_domain"] = (
                abs(spectrum.binding - reference.binding)
            )
        passed = (
            abs(spectra[-2].binding - spectra[-1].binding)
            <= self._config.comparison.finite_domain_binding_tolerance
            and spectra[-1].boundary_probability
            <= self._config.comparison.finite_domain_boundary_probability_tolerance
        )
        return records, passed

    def _supercell_axis(self) -> tuple[list[JsonValue], bool]:
        spectra: list[ContinuumSpectrumResult] = []
        records: list[JsonValue] = []
        for count in self._config.supercell_counts:
            length = count * self._config.supercell_spacing
            matrix = self._builder.lattice(
                count,
                self._config.supercell_spacing,
                self._config.supercell_width,
                self._config.supercell_family,
            )
            spectrum = self._spectrum.execute(matrix, length)
            spectra.append(spectrum)
            records.append(
                {
                    "cell_count": count,
                    "domain_length": length,
                    "binding_energy": spectrum.binding,
                    "bound_state_count": spectrum.bound_count,
                    "boundary_probability": spectrum.boundary_probability,
                    "operator_sha256": self._matrix_sha256(matrix),
                }
            )
        reference = spectra[-1]
        for record, spectrum in zip(records, spectra, strict=True):
            cast(dict[str, JsonValue], record)[
                "binding_defect_from_largest_supercell"
            ] = abs(spectrum.binding - reference.binding)
        passed = (
            abs(spectra[-2].binding - spectra[-1].binding)
            <= self._config.comparison.lattice_supercell_binding_tolerance
            and spectra[-1].boundary_probability
            <= self._config.comparison.lattice_supercell_boundary_probability_tolerance
        )
        return records, passed

    def _scale_axis(self) -> tuple[list[JsonValue], JsonValue]:
        records: list[JsonValue] = []
        for spacing in self._config.scale_spacings:
            count = round(self._config.scale_domain / spacing)
            lattice = self._builder.lattice(
                count, spacing, self._config.scale_width, self._config.scale_family
            )
            continuum = self._builder.continuum(
                count,
                self._config.scale_domain,
                self._config.scale_width,
                self._config.scale_family,
            )
            lattice_spectrum = self._spectrum.execute(
                lattice, self._config.scale_domain
            )
            continuum_spectrum = self._spectrum.execute(
                continuum, self._config.scale_domain
            )
            records.append(
                self._comparison_record(
                    lattice,
                    continuum,
                    lattice_spectrum,
                    continuum_spectrum,
                    self._config.scale_domain,
                    spacing,
                    {"lattice_spacing": spacing, "site_count": count},
                )
            )
        boundary: JsonValue = None
        for index, record in enumerate(records):
            if all(
                bool(cast(dict[str, JsonValue], later)["all_criteria_pass"])
                for later in records[index:]
            ):
                boundary = cast(dict[str, JsonValue], record)["lattice_spacing"]
                break
        return records, boundary

    def _profile_axis(self) -> list[JsonValue]:
        count = round(self._config.profile_domain / self._config.profile_spacing)
        families: list[JsonValue] = []
        for family in self._config.profile_families:
            records: list[JsonValue] = []
            for width in self._config.profile_widths:
                lattice = self._builder.lattice(
                    count, self._config.profile_spacing, width, family
                )
                continuum = self._builder.continuum(
                    count, self._config.profile_domain, width, family
                )
                lattice_spectrum = self._spectrum.execute(
                    lattice, self._config.profile_domain
                )
                continuum_spectrum = self._spectrum.execute(
                    continuum, self._config.profile_domain
                )
                records.append(
                    self._comparison_record(
                        lattice,
                        continuum,
                        lattice_spectrum,
                        continuum_spectrum,
                        self._config.profile_domain,
                        self._config.profile_spacing,
                        {"width": width},
                    )
                )
            crossover: JsonValue = None
            for index, record in enumerate(records):
                if all(
                    bool(cast(dict[str, JsonValue], later)["all_criteria_pass"])
                    for later in records[index:]
                ):
                    crossover = cast(dict[str, JsonValue], record)["width"]
                    break
            families.append(
                {"family": family, "records": records, "crossover_width": crossover}
            )
        return families

    def _comparison_record(
        self,
        lattice: ComplexMatrix,
        continuum: ComplexMatrix,
        lattice_spectrum: ContinuumSpectrumResult,
        continuum_spectrum: ContinuumSpectrumResult,
        length: float,
        spacing: float,
        identity: dict[str, JsonValue],
    ) -> dict[str, JsonValue]:
        projector = self._states.execute(
            lattice_spectrum.state,
            self._builder.modes(lattice.shape[0]),
            continuum_spectrum.state,
            self._builder.modes(continuum.shape[0]),
        )
        compressed, cross, edge_weight = self._operators.execute(
            lattice, continuum, lattice_spectrum.state, length, spacing
        )
        binding_error = abs(lattice_spectrum.binding - continuum_spectrum.binding)
        relative = binding_error / max(continuum_spectrum.binding, np.finfo(float).tiny)
        count_equal = lattice_spectrum.bound_count == continuum_spectrum.bound_count
        criteria_bool = {
            "relative_binding": relative
            <= self._config.comparison.relative_binding_tolerance,
            "projector": projector
            <= self._config.comparison.projector_frobenius_tolerance,
            "compressed_operator": compressed
            <= self._config.comparison.compressed_operator_tolerance,
            "cross_coupling": cross <= self._config.comparison.cross_coupling_tolerance,
            "brillouin_edge_weight": edge_weight
            <= self._config.comparison.brillouin_edge_weight_tolerance,
            "bound_state_count": count_equal
            or not self._config.comparison.require_equal_bound_state_count,
        }
        criteria: dict[str, JsonValue] = dict(criteria_bool)
        return {
            **identity,
            "lattice_binding_energy": lattice_spectrum.binding,
            "continuum_binding_energy": continuum_spectrum.binding,
            "absolute_binding_error": binding_error,
            "relative_binding_error": relative,
            "lattice_bound_state_count": lattice_spectrum.bound_count,
            "continuum_bound_state_count": continuum_spectrum.bound_count,
            "projector_frobenius_defect": projector,
            "compressed_operator_spectral_norm": compressed,
            "cross_coupling_spectral_norm": cross,
            "brillouin_edge_weight": edge_weight,
            "criteria": criteria,
            "all_criteria_pass": all(criteria_bool.values()),
            "lattice_operator_sha256": self._matrix_sha256(lattice),
            "continuum_operator_sha256": self._matrix_sha256(continuum),
        }

    @staticmethod
    def _matrix_sha256(matrix: ComplexMatrix) -> str:
        canonical = np.asarray(matrix, dtype=np.complex128).copy()
        canonical.real = np.round(canonical.real, decimals=9)
        canonical.imag = np.round(canonical.imag, decimals=9)
        canonical.real[canonical.real == 0.0] = 0.0
        canonical.imag[canonical.imag == 0.0] = 0.0
        return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


class ContinuumResultSerializer:
    """Serialize a finite JSON result deterministically."""

    __slots__ = ()

    def execute(self, value: dict[str, JsonValue]) -> bytes:
        """Return canonical sorted finite UTF-8 JSON bytes.

        Parameters
        ----------
        value
            Strictly decoded JSON value consumed by the closed-schema adapter.

        Returns
        -------
        bytes
            Canonical sorted UTF-8 JSON with one trailing newline.
        """
        return (
            json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"
        ).encode("utf-8")


class ContinuumRefinementFileWorkflow:
    """Load, execute, and serialize one continuum-refinement operation."""

    __slots__ = ()

    def execute(self, input_path: Path, output_path: Path) -> None:
        """Calculate a new file result with current implementation provenance.

        Parameters
        ----------
        input_path
            Explicit path of the retained input within the operation-owned root.
        output_path
            Explicit destination for the newly serialized result document.
        """
        payload = input_path.read_bytes()
        config = ContinuumRefinementInputDeserializer().execute(payload)
        repository_root = input_path.parents[3]
        parent = ContinuumParentLoader().execute(repository_root, config)
        implementation = Path(__file__).resolve()
        result = ContinuumRefinementCampaignCalculator(config, parent).execute(
            ContinuumRefinementProvenance(
                input_sha256=hashlib.sha256(payload).hexdigest(),
                implementation_path=implementation.relative_to(
                    repository_root
                ).as_posix(),
                implementation_sha256=hashlib.sha256(
                    implementation.read_bytes()
                ).hexdigest(),
                python_version=platform.python_version(),
                numpy_version=np.__version__,
            )
        )
        output_path.write_bytes(ContinuumResultSerializer().execute(result))
