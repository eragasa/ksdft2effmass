"""Immutable contracts for the synthetic finite-rank-oracle campaign."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from ksdft2effmass.periodic1d import Periodic1DFiniteHoppingToyModel

type ComplexMatrix = npt.NDArray[np.complex128]
type ComplexVector = npt.NDArray[np.complex128]
type RealArray = npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class FiniteRankOracleSourceIdentity:
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
        """Validate the immutable FiniteRankOracleSourceIdentity invariants."""
        if not self.path or len(self.sha256) != 64:
            raise ValueError("source identity is invalid")


@dataclass(frozen=True, slots=True)
class FiniteRankParentContract:
    """Represent the finite parent convention used by every control.

    Parameters
    ----------
    group_id
        Exact retained parent-band-group identity.
    hopping_range
        Nonnegative maximum primitive-cell hopping displacement.
    momentum
        Finite dimensionless reduced primitive-cell crystal momentum.
    energy_unit
        Exact unit label for every campaign energy quantity.
    ordering
        Exact label for the parent basis and hopping ordering convention.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    group_id: str
    hopping_range: int
    momentum: float
    energy_unit: str
    ordering: str

    def __post_init__(self) -> None:
        """Validate the immutable FiniteRankParentContract invariants."""
        if (
            not self.group_id
            or self.hopping_range < 0
            or not np.isfinite(self.momentum)
            or not self.energy_unit
            or not self.ordering
        ):
            raise ValueError("parent contract is invalid")


@dataclass(frozen=True, slots=True)
class RankOneOracleContract:
    """Represent the rank-one oracle parameter sequence.

    Parameters
    ----------
    cell_counts
        Strictly increasing finite-supercell sizes used by the rank-one study.
    attractive_magnitudes
        Strictly increasing positive defect magnitudes in the declared energy unit.
    orbital_angle
        Finite mixing angle defining the two-component defect orbital.
    orbital_phase
        Finite relative phase defining the two-component defect orbital.
    defect_site
        Zero-based defect-cell index in finite supercell order.
    equation
        Exact authored form of the finite rank-one secular equation.
    root_domain
        Exact authored energy domain of the scalar secular root.
    root_selection
        Exact authored rule selecting the physical scalar root.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    cell_counts: tuple[int, ...]
    attractive_magnitudes: tuple[float, ...]
    orbital_angle: float
    orbital_phase: float
    defect_site: int
    equation: str
    root_domain: str
    root_selection: str

    def __post_init__(self) -> None:
        """Validate the immutable RankOneOracleContract invariants."""
        if (
            not self.cell_counts
            or any(value < 2 for value in self.cell_counts)
            or tuple(sorted(set(self.cell_counts))) != self.cell_counts
            or not self.attractive_magnitudes
            or any(value <= 0.0 for value in self.attractive_magnitudes)
            or tuple(sorted(set(self.attractive_magnitudes)))
            != self.attractive_magnitudes
            or self.defect_site < 0
            or not self.equation
            or not self.root_domain
            or not self.root_selection
        ):
            raise ValueError("rank-one contract is invalid")

    @property
    def orbital_vector(self) -> ComplexVector:
        """Return the normalized authored two-orbital defect vector.

        Returns
        -------
        ComplexVector
            Normalized complex orbital vector in parent basis order.
        """
        return np.asarray(
            [
                np.cos(self.orbital_angle),
                np.exp(1j * self.orbital_phase) * np.sin(self.orbital_angle),
            ],
            dtype=np.complex128,
        )


@dataclass(frozen=True, slots=True)
class FiniteRankSpecialControls:
    """Represent threshold, no-bound-state, and degeneracy controls.

    Parameters
    ----------
    cell_count
        Exact number of cells in the finite periodic supercell.
    attractive_magnitude
        Positive attractive rank-one defect magnitude in the declared energy unit.
    repulsive_magnitude
        Positive repulsive defect magnitude in the declared energy unit.
    threshold_magnitude
        Positive near-threshold defect magnitude in the declared energy unit.
    spin_degeneracy
        Exact positive multiplicity used by the degeneracy control.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    cell_count: int
    attractive_magnitude: float
    repulsive_magnitude: float
    threshold_magnitude: float
    spin_degeneracy: int

    def __post_init__(self) -> None:
        """Validate the immutable FiniteRankSpecialControls invariants."""
        if (
            self.cell_count < 2
            or self.attractive_magnitude <= 0.0
            or self.repulsive_magnitude <= 0.0
            or self.threshold_magnitude != 0.0
            or self.spin_degeneracy != 2
        ):
            raise ValueError("special controls are invalid")


@dataclass(frozen=True, slots=True)
class FiniteRankOracleTolerances:
    """Represent frozen numerical-verification tolerances.

    Parameters
    ----------
    root_interval
        Width of the final scalar secular-root bracket.
    secular_residual
        Absolute residual of the independently evaluated secular equation.
    energy_agreement
        Absolute energy discrepancy between independently compared routes.
    eigen_residual
        Norm of the finite represented eigenpair residual.
    projector_agreement
        Frobenius discrepancy between compared bound-state projectors.
    edge_margin
        Positive energy margin used to classify a finite eigenvalue as bound.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    root_interval: float
    secular_residual: float
    energy_agreement: float
    eigen_residual: float
    projector_agreement: float
    edge_margin: float

    def __post_init__(self) -> None:
        """Validate the immutable FiniteRankOracleTolerances invariants."""
        if any(
            value <= 0.0
            for value in (
                self.root_interval,
                self.secular_residual,
                self.energy_agreement,
                self.eigen_residual,
                self.projector_agreement,
                self.edge_margin,
            )
        ):
            raise ValueError("tolerances must be positive")


@dataclass(frozen=True, slots=True)
class FiniteRankOracleCampaignInput:
    """Represent the closed analytical-oracle input.

    Parameters
    ----------
    experiment_id
        Exact stable identity of the retained synthetic campaign.
    sources
        Ordered authenticated source identities required by the campaign.
    parent
        Explicit parent contract or authenticated parent data used by the operation.
    rank_one
        Closed rank-one defect-oracle parameter contract.
    special
        Closed threshold, repulsive, and degeneracy controls.
    tolerances
        Closed numerical comparison tolerances for the finite-rank campaign.
    """

    experiment_id: str
    sources: tuple[FiniteRankOracleSourceIdentity, ...]
    parent: FiniteRankParentContract
    rank_one: RankOneOracleContract
    special: FiniteRankSpecialControls
    tolerances: FiniteRankOracleTolerances


@dataclass(frozen=True, slots=True)
class FiniteRankOracleParentData:
    """Retain the explicitly adapted parent and verified source identities.

    Parameters
    ----------
    model
        Explicit finite-hopping parent toy model supplying the represented fibers.
    sources
        Ordered authenticated source identities required by the campaign.

    Raises
    ------
    TypeError
        An argument does not have the required exact public type.
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    model: Periodic1DFiniteHoppingToyModel
    sources: tuple[FiniteRankOracleSourceIdentity, ...]

    def __post_init__(self) -> None:
        """Require the exact two-orbital toy model and authenticated sources."""
        if type(self.model) is not Periodic1DFiniteHoppingToyModel:
            raise TypeError("model must be Periodic1DFiniteHoppingToyModel")
        if self.model.orbital_count != 2:
            raise ValueError("finite-rank parent must contain exactly two orbitals")
        if type(self.sources) is not tuple or not self.sources:
            raise TypeError("sources must be a nonempty exact tuple")
        if any(
            type(item) is not FiniteRankOracleSourceIdentity for item in self.sources
        ):
            raise TypeError("every source must be FiniteRankOracleSourceIdentity")


@dataclass(frozen=True, slots=True)
class RankOneRootResult:
    """Record one independently resolved rank-one secular root.

    Parameters
    ----------
    energy
        Candidate bound-state energy in the declared campaign energy unit.
    lower_bracket
        Lower endpoint of the final scalar secular-root bracket.
    upper_bracket
        Upper endpoint of the final scalar secular-root bracket.
    secular_residual
        Absolute residual of the independently evaluated secular equation.
    iteration_count
        Number of iterations used by the bounded scalar root solve.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    energy: float
    lower_bracket: float
    upper_bracket: float
    secular_residual: float
    iteration_count: int

    def __post_init__(self) -> None:
        """Validate the immutable RankOneRootResult invariants."""
        if (
            not np.isfinite(self.energy)
            or self.lower_bracket > self.energy
            or self.energy > self.upper_bracket
            or self.secular_residual < 0.0
            or self.iteration_count < 1
        ):
            raise ValueError("root result is invalid")


@dataclass(frozen=True, slots=True)
class FiniteRankOracleProvenance:
    """Represent explicit execution-adapter provenance.

    Parameters
    ----------
    input_path
        Explicit path of the retained input within the operation-owned root.
    input_sha256
        Lowercase SHA-256 identity of the exact retained input bytes.
    script_path
        Explicit repository-relative path of the retained campaign script.
    script_sha256
        Lowercase SHA-256 identity of the exact retained script bytes.
    python_version
        Explicit nonempty Python version retained as software provenance.
    numpy_version
        Explicit nonempty NumPy version retained as software provenance.

    Raises
    ------
    ValueError
        An argument violates a schema, domain, identity, or correlation invariant.
    """

    input_path: str
    input_sha256: str
    script_path: str
    script_sha256: str
    python_version: str
    numpy_version: str

    def __post_init__(self) -> None:
        """Validate paths, versions, and lowercase SHA-256 identities."""
        if any(
            type(value) is not str or not value
            for value in (
                self.input_path,
                self.script_path,
                self.python_version,
                self.numpy_version,
            )
        ):
            raise ValueError("provenance paths and versions must be nonempty")
        for digest in (self.input_sha256, self.script_sha256):
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError("provenance digests must be lowercase SHA-256")
