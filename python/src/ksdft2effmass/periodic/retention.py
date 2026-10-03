r"""Scientific retained spaces, exact operators, and finite representations.

This module separates four meanings that must not be inferred from one another:
a :class:`~ksdft2effmass.periodic.PeriodicModel` identifies a modeled periodic
system, :class:`PeriodicRetainedSubspace` identifies selected mathematical state
space, :class:`PeriodicRetainedOperator` identifies an exact operator on that
space, and :class:`PeriodicRepresentedRetainedOperator` binds the exact operator
to one finite :class:`~ksdft2effmass.operators.OperatorRecord`.

For an orthogonal projector :math:`P` on a parent space :math:`\mathcal H`, the
retained space and exact retained operator are

.. math::

   \mathcal H^{(P)} = \operatorname{im}P,
   \qquad
   H^{(P)} = \left.PHP\right|_{\mathcal H^{(P)}}.

For an ordered orthonormal retained basis :math:`(|b_i\rangle)_{i=0}^{r-1}`,
the represented matrix is

.. math::

   H^{(P)}_{ij}=\langle b_i|H^{(P)}|b_j\rangle.

These equations define distinct mathematical objects. In particular,
``PeriodicRetainedOperator`` is not a matrix container, and
``PeriodicRepresentedRetainedOperator`` does not turn an ``OperatorRecord`` into
a physical model.

Phase-four records use stable parent identities. They do not embed a concrete
model, resolve an identity, open a filesystem path, execute a calculation,
select eigenvectors, compute a projector, choose a gauge, align spaces, convert
units, shift energy zeros, truncate couplings, fit an effective model, or
serialize state. Successful construction is software-contract verification
only; it does not establish numerical verification, scientific validation,
uncertainty quantification, or suitability of the retained space.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ksdft2effmass.operators import EnergyReference, OperatorRecord

from .model import SpatialDimension


class PeriodicRetentionKind(Enum):
    """Classify the declared construction of a periodic retained subspace.

    Attributes
    ----------
    SPECTRAL_RESTRICTION
        Retain an identified invariant spectral sector of the parent operator.
    SELECTED_BANDS
        Retain an ordered band family over an identified reciprocal domain.
    DISENTANGLED_SUBSPACE
        Retain a fixed-rank subspace selected from a larger candidate manifold by
        a separately identified disentanglement construction.

    Notes
    -----
    This enum classifies a construction; it does not contain selected indices,
    a projector, a frame, an energy window, or numerical evidence. Those data
    require their own typed records and identities.
    """

    SPECTRAL_RESTRICTION = "spectral_restriction"
    SELECTED_BANDS = "selected_bands"
    DISENTANGLED_SUBSPACE = "disentangled_subspace"


class PeriodicRetainedOperatorConstructionKind(Enum):
    """Classify how an exact operator on a retained space is obtained.

    Attributes
    ----------
    INVARIANT_RESTRICTION
        Restrict a parent operator to a retained invariant subspace.
    ORTHOGONAL_COMPRESSION
        Apply an orthogonal compression and declare the resulting operator's
        domain and codomain to be the retained space.

    Notes
    -----
    Both values describe operators whose declared domain and codomain are the
    retained space. An ambient operator ``P H P`` acting on the full parent
    space is not represented by :class:`PeriodicRetainedOperator`.
    """

    INVARIANT_RESTRICTION = "invariant_restriction"
    ORTHOGONAL_COMPRESSION = "orthogonal_compression"


class PeriodicHermiticityStatus(Enum):
    """Record the declaration status of exact retained-operator Hermiticity.

    Attributes
    ----------
    DECLARED_HERMITIAN
        The owning scientific contract declares the exact operator Hermitian.
    DECLARED_NON_HERMITIAN
        The owning scientific contract declares the exact operator
        non-Hermitian.
    NOT_ASSESSED
        This record makes no Hermiticity declaration.

    Notes
    -----
    This metadata is not the output of a tolerance-based matrix analysis. A
    represented Hermiticity residual and its tolerance belong to a separate
    analyzer ActionObject.
    """

    DECLARED_HERMITIAN = "declared_hermitian"
    DECLARED_NON_HERMITIAN = "declared_non_hermitian"
    NOT_ASSESSED = "not_assessed"


@dataclass(frozen=True, slots=True)
class PeriodicOperatorReference:
    """Stable identity of one parent operator and its state space.

    Parameters
    ----------
    model_id
        Stable nonempty identity of the parent periodic model.
    operator_id
        Stable nonempty identity of the parent mathematical operator.
    state_space_id
        Stable nonempty identity of the operator's ambient state space.
    spatial_dimension
        Exact built-in integer ``1``, ``2``, or ``3`` identifying the number of
        periodic spatial directions. Booleans, numeric strings, and NumPy scalar
        substitutes are rejected.

    Raises
    ------
    TypeError
        If an identity is not a string or ``spatial_dimension`` is not exactly a
        built-in ``int``.
    ValueError
        If an identity is empty or the dimension is outside ``{1, 2, 3}``.

    Notes
    -----
    A reference is not an embedded model, path, repository root, URL, registry
    entry, or proof that a parent object exists. Identity resolution is outside
    this DataObject.
    """

    model_id: str
    operator_id: str
    state_space_id: str
    spatial_dimension: SpatialDimension

    def __post_init__(self) -> None:
        """Validate exact identity and dimension fields."""
        for value, name in (
            (self.model_id, "model_id"),
            (self.operator_id, "operator_id"),
            (self.state_space_id, "state_space_id"),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if value == "":
                raise ValueError(f"{name} must not be empty")
        if type(self.spatial_dimension) is not int:
            raise TypeError("spatial_dimension must be a built-in int")
        if self.spatial_dimension not in (1, 2, 3):
            raise ValueError("spatial_dimension must be one, two, or three")


@dataclass(frozen=True, slots=True)
class PeriodicRetentionDefinition:
    """Define one parent-qualified periodic retention construction.

    Parameters
    ----------
    retention_id
        Stable nonempty identity of this retention definition.
    parent_operator
        Exact stable reference to the parent operator and ambient state space.
    retained_space_id
        Stable nonempty identity assigned to the resulting retained space.
    kind
        Exact construction classification.
    rank
        Positive retained dimension as an exact built-in integer.
    ordered_state_labels
        Tuple of exactly ``rank`` unique nonempty labels. The order is semantic
        and later fixes represented basis ordering.
    reciprocal_domain_id
        Nonempty identity of the sampled mesh, path, Brillouin-zone domain, or
        other reciprocal-domain convention applicable to the construction.
    construction_record_id
        Nonempty identity of the closed typed record that supplies the selection,
        projector, frame, window, or other method-specific construction data.
    assumption_ids
        Ordered tuple of unique nonempty identities for applicable scientific or
        mathematical assumptions. An empty tuple is valid.
    provenance_id
        Nonempty identity of the provenance record for this definition.

    Raises
    ------
    TypeError
        If a field has the wrong exact semantic type. Lists are not accepted for
        tuple fields, and booleans are not accepted as ranks.
    ValueError
        If an identity or label is empty, rank is not positive, ordered-label
        count differs from rank, or labels or assumption identities repeat.

    Notes
    -----
    The ``construction_record_id`` names method-specific typed state; it is not
    a generic parameter mapping. This record does not resolve that identity or
    assess the adequacy of the selected space.
    """

    retention_id: str
    parent_operator: PeriodicOperatorReference
    retained_space_id: str
    kind: PeriodicRetentionKind
    rank: int
    ordered_state_labels: tuple[str, ...]
    reciprocal_domain_id: str
    construction_record_id: str
    assumption_ids: tuple[str, ...]
    provenance_id: str

    def __post_init__(self) -> None:
        """Validate intrinsic retention-definition invariants."""
        for value, name in (
            (self.retention_id, "retention_id"),
            (self.retained_space_id, "retained_space_id"),
            (self.reciprocal_domain_id, "reciprocal_domain_id"),
            (self.construction_record_id, "construction_record_id"),
            (self.provenance_id, "provenance_id"),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if value == "":
                raise ValueError(f"{name} must not be empty")
        if type(self.parent_operator) is not PeriodicOperatorReference:
            raise TypeError("parent_operator must be PeriodicOperatorReference")
        if type(self.kind) is not PeriodicRetentionKind:
            raise TypeError("kind must be PeriodicRetentionKind")
        if type(self.rank) is not int:
            raise TypeError("rank must be a built-in int")
        if self.rank <= 0:
            raise ValueError("rank must be positive")
        if type(self.ordered_state_labels) is not tuple:
            raise TypeError("ordered_state_labels must be a tuple")
        if len(self.ordered_state_labels) != self.rank:
            raise ValueError("ordered_state_labels length must equal rank")
        for label in self.ordered_state_labels:
            if not isinstance(label, str):
                raise TypeError("ordered_state_labels must contain strings")
            if label == "":
                raise ValueError("ordered_state_labels must not contain empty labels")
        if len(set(self.ordered_state_labels)) != len(self.ordered_state_labels):
            raise ValueError("ordered_state_labels must be unique")
        if type(self.assumption_ids) is not tuple:
            raise TypeError("assumption_ids must be a tuple")
        for assumption_id in self.assumption_ids:
            if not isinstance(assumption_id, str):
                raise TypeError("assumption_ids must contain strings")
            if assumption_id == "":
                raise ValueError("assumption_ids must not contain empty identities")
        if len(set(self.assumption_ids)) != len(self.assumption_ids):
            raise ValueError("assumption_ids must be unique")


@dataclass(frozen=True, slots=True)
class PeriodicRetainedSubspace:
    """Identify a retained periodic state space and its construction metadata.

    Parameters
    ----------
    definition
        Parent-qualified retention definition whose ``retained_space_id`` names
        this space and whose ``rank`` is its finite retained dimension.
    ambient_state_space_id
        Exact ambient identity. It must equal
        ``definition.parent_operator.state_space_id``.
    ambient_dimension
        Positive exact built-in integer dimension of the represented ambient
        space. It must not be smaller than retained rank.
    projector_or_frame_record_id
        Nonempty identity of the numerical projector, orthonormal frame, or
        frame-family record representing this subspace.
    spin_convention
        Nonempty identity or exact textual convention for represented spin.
    internal_degree_convention
        Nonempty identity or exact textual convention for orbital, sublattice,
        channel, or other internal degrees of freedom.
    reciprocal_boundary_convention
        Nonempty identity or exact textual convention for reciprocal-boundary
        sewing or periodic closure.
    provenance_id
        Nonempty identity of the retained-space construction provenance.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type or ``ambient_dimension`` is not
        exactly a built-in integer.
    ValueError
        If an identity is empty, ambient dimension is not positive, retained
        rank exceeds ambient dimension, or the ambient identity differs from the
        parent reference.

    Notes
    -----
    This DataObject identifies the mathematical retained space. The referenced
    projector or frame is representation data; a unitary frame change can leave
    this retained-space identity unchanged. Construction does not numerically
    verify orthogonality, smoothness, isolation, or topology.
    """

    definition: PeriodicRetentionDefinition
    ambient_state_space_id: str
    ambient_dimension: int
    projector_or_frame_record_id: str
    spin_convention: str
    internal_degree_convention: str
    reciprocal_boundary_convention: str
    provenance_id: str

    def __post_init__(self) -> None:
        """Validate retained-space fields and parent-space agreement."""
        if type(self.definition) is not PeriodicRetentionDefinition:
            raise TypeError("definition must be PeriodicRetentionDefinition")
        for value, name in (
            (self.ambient_state_space_id, "ambient_state_space_id"),
            (self.projector_or_frame_record_id, "projector_or_frame_record_id"),
            (self.spin_convention, "spin_convention"),
            (self.internal_degree_convention, "internal_degree_convention"),
            (
                self.reciprocal_boundary_convention,
                "reciprocal_boundary_convention",
            ),
            (self.provenance_id, "provenance_id"),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if value == "":
                raise ValueError(f"{name} must not be empty")
        if type(self.ambient_dimension) is not int:
            raise TypeError("ambient_dimension must be a built-in int")
        if self.ambient_dimension <= 0:
            raise ValueError("ambient_dimension must be positive")
        if (
            self.ambient_state_space_id
            != self.definition.parent_operator.state_space_id
        ):
            raise ValueError("ambient state-space identity must match parent operator")
        if self.definition.rank > self.ambient_dimension:
            raise ValueError("retained rank must not exceed ambient dimension")

    @property
    def retained_space_id(self) -> str:
        """Return the stable retained state-space identity."""
        return self.definition.retained_space_id

    @property
    def rank(self) -> int:
        """Return the exact finite retained dimension."""
        return self.definition.rank

    @property
    def spatial_dimension(self) -> SpatialDimension:
        """Return the parent model's exact periodic spatial dimension."""
        return self.definition.parent_operator.spatial_dimension


@dataclass(frozen=True, slots=True)
class PeriodicRetainedOperator:
    r"""Identify an exact operator whose domain and codomain are one retained space.

    Parameters
    ----------
    operator_id
        Stable nonempty identity of the exact retained operator.
    parent_operator
        Exact reference to the parent operator from which it is retained.
    retained_subspace
        Retained mathematical domain and codomain.
    construction_kind
        Exact restriction or orthogonal-compression classification.
    energy_reference
        Exact scalar energy-zero and energy-unit metadata. It declares the
        convention of the exact retained operator without performing conversion
        or alignment.
    hermiticity_status
        Declaration status of exact-operator Hermiticity, not a represented
        residual result.
    provenance_id
        Nonempty identity of the restriction or compression provenance.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If an identity is empty or the supplied parent differs from the retained
        subspace's parent reference.

    Notes
    -----
    Mathematically, this record identifies
    :math:`\left.PHP\right|_{\operatorname{im}P}`. It does not store ``P``, the
    parent operator implementation, an ambient ``PHP`` matrix, or finite matrix
    coordinates.
    """

    operator_id: str
    parent_operator: PeriodicOperatorReference
    retained_subspace: PeriodicRetainedSubspace
    construction_kind: PeriodicRetainedOperatorConstructionKind
    energy_reference: EnergyReference
    hermiticity_status: PeriodicHermiticityStatus
    provenance_id: str

    def __post_init__(self) -> None:
        """Validate exact-operator identity and retained-space agreement."""
        for value, name in (
            (self.operator_id, "operator_id"),
            (self.provenance_id, "provenance_id"),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if value == "":
                raise ValueError(f"{name} must not be empty")
        if type(self.parent_operator) is not PeriodicOperatorReference:
            raise TypeError("parent_operator must be PeriodicOperatorReference")
        if type(self.retained_subspace) is not PeriodicRetainedSubspace:
            raise TypeError("retained_subspace must be PeriodicRetainedSubspace")
        if type(self.construction_kind) is not PeriodicRetainedOperatorConstructionKind:
            raise TypeError(
                "construction_kind must be PeriodicRetainedOperatorConstructionKind"
            )
        if type(self.energy_reference) is not EnergyReference:
            raise TypeError("energy_reference must be EnergyReference")
        if type(self.hermiticity_status) is not PeriodicHermiticityStatus:
            raise TypeError("hermiticity_status must be PeriodicHermiticityStatus")
        if self.parent_operator != self.retained_subspace.definition.parent_operator:
            raise ValueError("parent operator must match retained-subspace parent")

    @property
    def domain_id(self) -> str:
        """Return the retained domain identity."""
        return self.retained_subspace.retained_space_id

    @property
    def codomain_id(self) -> str:
        """Return the retained codomain identity."""
        return self.retained_subspace.retained_space_id


@dataclass(frozen=True, slots=True)
class PeriodicRepresentedRetainedOperator:
    """Bind an exact retained operator to one finite represented operator.

    Parameters
    ----------
    representation_id
        Stable nonempty identity of this exact representation binding.
    retained_operator
        Exact retained mathematical operator being represented.
    operator_record
        Finite matrix, state-space, ordered orthonormal basis, geometry, energy
        reference, and represented provenance.
    representation_map_id
        Nonempty identity of the map from retained states to matrix coordinates.
    gauge_id
        Nonempty identity of the represented gauge or frame convention.
    provenance_id
        Nonempty identity of the binding provenance.

    Raises
    ------
    TypeError
        If a field has the wrong semantic type.
    ValueError
        If an identity is empty or state-space identity, rank, basis ordering,
        energy unit, or energy-zero metadata disagree.

    Notes
    -----
    The exact binding checks representation metadata; it does not infer a basis
    transformation or gauge alignment. Equal dimensions alone are insufficient.
    The geometry remains owned by ``operator_record`` and is not duplicated.
    """

    representation_id: str
    retained_operator: PeriodicRetainedOperator
    operator_record: OperatorRecord
    representation_map_id: str
    gauge_id: str
    provenance_id: str

    def __post_init__(self) -> None:
        """Validate intrinsic exact-representation binding invariants."""
        for value, name in (
            (self.representation_id, "representation_id"),
            (self.representation_map_id, "representation_map_id"),
            (self.gauge_id, "gauge_id"),
            (self.provenance_id, "provenance_id"),
        ):
            if not isinstance(value, str):
                raise TypeError(f"{name} must be a string")
            if value == "":
                raise ValueError(f"{name} must not be empty")
        if type(self.retained_operator) is not PeriodicRetainedOperator:
            raise TypeError("retained_operator must be PeriodicRetainedOperator")
        if type(self.operator_record) is not OperatorRecord:
            raise TypeError("operator_record must be OperatorRecord")
        subspace = self.retained_operator.retained_subspace
        if self.operator_record.state_space.identifier != subspace.retained_space_id:
            raise ValueError(
                "operator-record state-space identity must match retained space"
            )
        if self.operator_record.state_space.dimension != subspace.rank:
            raise ValueError("operator-record dimension must match retained rank")
        if (
            self.operator_record.basis.ordering
            != subspace.definition.ordered_state_labels
        ):
            raise ValueError(
                "operator-record basis ordering must match retained labels"
            )
        if (
            self.operator_record.energy_reference
            != self.retained_operator.energy_reference
        ):
            raise ValueError(
                "operator-record energy reference must match retained operator"
            )


class PeriodicRetainedSubspaceConstructor:
    """Construct one parent-qualified retained-space record.

    The ActionObject makes retention construction explicit without selecting
    eigenvectors or computing a projector. It binds already identified scientific
    and represented metadata and returns an immutable
    :class:`PeriodicRetainedSubspace`.
    """

    __slots__ = ()

    def execute(
        self,
        *,
        definition: PeriodicRetentionDefinition,
        ambient_state_space_id: str,
        ambient_dimension: int,
        projector_or_frame_record_id: str,
        spin_convention: str,
        internal_degree_convention: str,
        reciprocal_boundary_convention: str,
        provenance_id: str,
    ) -> PeriodicRetainedSubspace:
        """Bind a retention definition to retained-space construction metadata.

        Returns
        -------
        PeriodicRetainedSubspace
            Immutable retained-space construction result.

        Raises
        ------
        TypeError
            If an input violates the exact semantic type contract.
        ValueError
            If identity, dimension, or parent-space invariants fail.
        """
        return PeriodicRetainedSubspace(
            definition=definition,
            ambient_state_space_id=ambient_state_space_id,
            ambient_dimension=ambient_dimension,
            projector_or_frame_record_id=projector_or_frame_record_id,
            spin_convention=spin_convention,
            internal_degree_convention=internal_degree_convention,
            reciprocal_boundary_convention=reciprocal_boundary_convention,
            provenance_id=provenance_id,
        )


class PeriodicRetainedOperatorConstructor:
    """Construct one exact operator on an identified retained space.

    The ActionObject records an exact restriction or orthogonal compression. It
    performs no numerical compression and stores no matrix coordinates.
    """

    __slots__ = ()

    def execute(
        self,
        *,
        operator_id: str,
        parent_operator: PeriodicOperatorReference,
        retained_subspace: PeriodicRetainedSubspace,
        construction_kind: PeriodicRetainedOperatorConstructionKind,
        energy_reference: EnergyReference,
        hermiticity_status: PeriodicHermiticityStatus,
        provenance_id: str,
    ) -> PeriodicRetainedOperator:
        """Bind an exact parent and retained domain/codomain.

        Returns
        -------
        PeriodicRetainedOperator
            Immutable exact retained-operator construction result.

        Raises
        ------
        TypeError
            If an input violates the exact semantic type contract.
        ValueError
            If an identity is empty or parent references disagree.
        """
        return PeriodicRetainedOperator(
            operator_id=operator_id,
            parent_operator=parent_operator,
            retained_subspace=retained_subspace,
            construction_kind=construction_kind,
            energy_reference=energy_reference,
            hermiticity_status=hermiticity_status,
            provenance_id=provenance_id,
        )


class PeriodicRepresentedRetainedOperatorConstructor:
    """Construct one exact binding to a finite ``OperatorRecord``.

    This ActionObject validates represented state-space, dimension, ordering, and
    energy-reference agreement. It does not align, transform, convert, or alter
    the supplied finite matrix.
    """

    __slots__ = ()

    def execute(
        self,
        *,
        representation_id: str,
        retained_operator: PeriodicRetainedOperator,
        operator_record: OperatorRecord,
        representation_map_id: str,
        gauge_id: str,
        provenance_id: str,
    ) -> PeriodicRepresentedRetainedOperator:
        """Bind a compatible finite record to an exact retained operator.

        Returns
        -------
        PeriodicRepresentedRetainedOperator
            Immutable represented retained-operator construction result.

        Raises
        ------
        TypeError
            If an input violates the exact semantic type contract.
        ValueError
            If an identity is empty or represented metadata are incompatible.
        """
        return PeriodicRepresentedRetainedOperator(
            representation_id=representation_id,
            retained_operator=retained_operator,
            operator_record=operator_record,
            representation_map_id=representation_map_id,
            gauge_id=gauge_id,
            provenance_id=provenance_id,
        )


__all__ = [
    "PeriodicHermiticityStatus",
    "PeriodicOperatorReference",
    "PeriodicRepresentedRetainedOperator",
    "PeriodicRepresentedRetainedOperatorConstructor",
    "PeriodicRetainedOperator",
    "PeriodicRetainedOperatorConstructionKind",
    "PeriodicRetainedOperatorConstructor",
    "PeriodicRetainedSubspace",
    "PeriodicRetainedSubspaceConstructor",
    "PeriodicRetentionDefinition",
    "PeriodicRetentionKind",
]
