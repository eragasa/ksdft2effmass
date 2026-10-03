"""Complete one-dimensional periodic Fourier scientific toy models."""

from __future__ import annotations

from dataclasses import dataclass, field

from ksdft2effmass.analysis.model_systems import PeriodicFourierPotential1D
from ksdft2effmass.operators import MODEL_SYSTEM_UNIT_CONVERTER, ScalarQuantity
from ksdft2effmass.periodic import (
    Periodic1DModel,
    PeriodicModelRole,
    PeriodicOperatorReference,
)
from ksdft2effmass.solid_state import (
    CenteredUniformReciprocalMesh1D,
    PlaneWaveBasis1D,
)


@dataclass(frozen=True, slots=True, init=False)
class Periodic1DFourierHamiltonianToyModel(Periodic1DModel):
    r"""Represent a complete quadratic-kinetic periodic Fourier toy parent.

    The modeled one-dimensional parent has Bloch-fiber matrix elements

    .. math::

       H_{nm}(k) = E_G (k+n)^2\delta_{nm} + V_{n-m},

    where ``potential`` defines the period, Fourier coefficients, and coefficient
    energy unit; ``recoil_energy`` is the positive scalar :math:`E_G`; and ``k`` is
    reduced momentum in the closed primitive interval ``[-0.5, 0.5]``. This record
    identifies the untruncated parent law, not a finite plane-wave representation.

    Parameters
    ----------
    model_id
        Stable nonempty configured-parent identity.
    state_space_id
        Stable nonempty identity of the parent Bloch state-space family.
    reciprocal_domain_id
        Stable nonempty identity of the primitive reduced reciprocal domain.
    potential
        Real finite Fourier potential, including its period and energy convention.
    recoil_energy
        Positive kinetic energy scale compatible with the potential coefficients.

    Raises
    ------
    TypeError
        If an identity or composed scientific value has the wrong exact type.
    ValueError
        If an identity is empty, recoil energy is not positive, or potential and
        recoil-energy units are incompatible.

    Notes
    -----
    Nominal membership and the exact ``TOY`` role classify scientific ownership and
    evidentiary purpose. They do not establish material realism, completeness of a
    parent electronic-structure calculation, scientific validation, or uncertainty
    quantification.
    """

    _model_id: str = field(repr=False)
    state_space_id: str
    reciprocal_domain_id: str
    potential: PeriodicFourierPotential1D
    recoil_energy: ScalarQuantity

    def __init__(
        self,
        model_id: str,
        state_space_id: str,
        reciprocal_domain_id: str,
        potential: PeriodicFourierPotential1D,
        recoil_energy: ScalarQuantity,
    ) -> None:
        """Store and validate the complete parent definition."""
        object.__setattr__(self, "_model_id", model_id)
        object.__setattr__(self, "state_space_id", state_space_id)
        object.__setattr__(self, "reciprocal_domain_id", reciprocal_domain_id)
        object.__setattr__(self, "potential", potential)
        object.__setattr__(self, "recoil_energy", recoil_energy)
        self.__post_init__()

    def __post_init__(self) -> None:
        """Validate identities, exact component types, scale, and units."""
        for name, value in (
            ("model_id", self.model_id),
            ("state_space_id", self.state_space_id),
            ("reciprocal_domain_id", self.reciprocal_domain_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")
        if type(self.potential) is not PeriodicFourierPotential1D:
            raise TypeError("potential must be PeriodicFourierPotential1D")
        if type(self.recoil_energy) is not ScalarQuantity:
            raise TypeError("recoil_energy must be ScalarQuantity")
        if self.recoil_energy.magnitude <= 0.0:
            raise ValueError("recoil_energy must be positive")
        if not MODEL_SYSTEM_UNIT_CONVERTER.compatible(
            self.potential.constant_coefficient.unit, self.recoil_energy.unit
        ):
            raise ValueError("potential and recoil-energy units must be compatible")

    @property
    def model_id(self) -> str:
        """Return the stable configured-parent identity."""
        return self._model_id

    @property
    def model_role(self) -> PeriodicModelRole:
        """Return the exact toy-model evidentiary role."""
        return PeriodicModelRole.TOY


@dataclass(frozen=True, slots=True, eq=False)
class Periodic1DPlaneWaveParentRepresentation:
    r"""Identify one finite plane-wave representation of an untruncated parent.

    Parameters
    ----------
    representation_id
        Stable nonempty identity of the finite Galerkin representation.
    parent_model
        Untruncated one-dimensional Fourier Hamiltonian being approximated.
    basis
        Ordered finite plane-wave basis, including the symmetric cutoff.
    reciprocal_mesh
        Finite reciprocal mesh on which the represented parent fibers are sampled.
    represented_operator
        Stable reference to the finite Galerkin operator family. Its state-space
        identity must be distinct from the untruncated parent's state-space identity.
    representation_map_id
        Stable nonempty identity of the Galerkin representation map.
    provenance_id
        Stable nonempty identity of the representation provenance.

    Notes
    -----
    This DataObject does not turn the finite Galerkin operator into the untruncated
    parent operator. Once the basis and mesh are fixed, ``represented_operator``
    identifies the resulting finite mathematical operator family; approximation of the
    untruncated parent remains numerical/discretization error recorded separately.
    Construction performs no eigensolve and makes no convergence, validation, or
    uncertainty-quantification claim.
    """

    representation_id: str
    parent_model: Periodic1DFourierHamiltonianToyModel
    basis: PlaneWaveBasis1D
    reciprocal_mesh: CenteredUniformReciprocalMesh1D
    represented_operator: PeriodicOperatorReference
    representation_map_id: str
    provenance_id: str

    def __post_init__(self) -> None:
        """Check identities, component types, and finite-parent correlation."""
        self._check_args_identities()
        self._check_args_components()
        self._check_args_parent_binding()

    def _check_args_identities(self) -> None:
        """Require nonempty exact string identities."""
        for name, value in (
            ("representation_id", self.representation_id),
            ("representation_map_id", self.representation_map_id),
            ("provenance_id", self.provenance_id),
        ):
            if type(value) is not str:
                raise TypeError(f"{name} must be a built-in str")
            if value == "":
                raise ValueError(f"{name} must be nonempty")

    def _check_args_components(self) -> None:
        """Require exact domain-object types at the representation boundary."""
        if type(self.parent_model) is not Periodic1DFourierHamiltonianToyModel:
            raise TypeError("parent_model must be Periodic1DFourierHamiltonianToyModel")
        if type(self.basis) is not PlaneWaveBasis1D:
            raise TypeError("basis must be PlaneWaveBasis1D")
        if type(self.reciprocal_mesh) is not CenteredUniformReciprocalMesh1D:
            raise TypeError("reciprocal_mesh must be CenteredUniformReciprocalMesh1D")
        if type(self.represented_operator) is not PeriodicOperatorReference:
            raise TypeError("represented_operator must be PeriodicOperatorReference")

    def _check_args_parent_binding(self) -> None:
        """Keep untruncated and finite parent identities distinct and correlated."""
        if self.represented_operator.model_id != self.parent_model.model_id:
            raise ValueError("represented operator must identify the parent model")
        if self.represented_operator.spatial_dimension != 1:
            raise ValueError("represented operator must be one-dimensional")
        if self.represented_operator.state_space_id == self.parent_model.state_space_id:
            raise ValueError(
                "finite and untruncated parent state spaces must remain distinct"
            )
        mesh_period = MODEL_SYSTEM_UNIT_CONVERTER.convert_scalar(
            self.reciprocal_mesh.reciprocal_period,
            self.basis.reciprocal_vector.unit,
        )
        if mesh_period.magnitude != self.basis.reciprocal_vector.magnitude:
            raise ValueError("plane-wave basis and reciprocal mesh must agree")
        expected_reciprocal = self.parent_model.potential.reciprocal_period_in(
            self.basis.reciprocal_vector
        )
        if expected_reciprocal != self.basis.reciprocal_vector.magnitude:
            raise ValueError("plane-wave basis must represent the parent period")

    @property
    def cutoff(self) -> int:
        """Return the symmetric reciprocal-index cutoff."""
        return self.basis.cutoff

    @property
    def ambient_dimension(self) -> int:
        """Return the finite represented Bloch-fiber dimension."""
        return self.basis.dimension


class Periodic1DPlaneWaveParentRepresentationConstructor:
    """Construct one validated finite representation of an untruncated parent."""

    __slots__ = ()

    def execute(
        self,
        *,
        representation_id: str,
        parent_model: Periodic1DFourierHamiltonianToyModel,
        basis: PlaneWaveBasis1D,
        reciprocal_mesh: CenteredUniformReciprocalMesh1D,
        represented_operator: PeriodicOperatorReference,
        representation_map_id: str,
        provenance_id: str,
    ) -> Periodic1DPlaneWaveParentRepresentation:
        """Validate and return one immutable finite parent representation."""
        return Periodic1DPlaneWaveParentRepresentation(
            representation_id=representation_id,
            parent_model=parent_model,
            basis=basis,
            reciprocal_mesh=reciprocal_mesh,
            represented_operator=represented_operator,
            representation_map_id=representation_map_id,
            provenance_id=provenance_id,
        )


__all__ = [
    "Periodic1DFourierHamiltonianToyModel",
    "Periodic1DPlaneWaveParentRepresentation",
    "Periodic1DPlaneWaveParentRepresentationConstructor",
]
