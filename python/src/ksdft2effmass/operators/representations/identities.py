"""Immutable identities for representation nodes.

Bloch-operator and cell-hopping representations use different role enums because they
are fields on different carrier domains. Derivation history belongs to transformation
identities under ``ksdft2effmass.operators.transformations``. Enum members carry no
domain-facing string value; serializers must own explicit wire mappings.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import final

from .domains import FiniteMomentumMeshDomain, FiniteTranslationDomain
from .spaces import RepresentationSpaceIdentity


class BlochSpaceRole(Enum):
    r"""Enumerate represented-space roles for a Bloch-operator field.

    A Bloch operator field has carrier
    :math:`H:K\rightarrow\operatorname{End}(V)` on a momentum domain.

    Attributes
    ----------
    ambient
        Parent represented Bloch space.
    retained
        Declared retained Bloch space.

    Notes
    -----
    Gauge transformation, alignment, and Fourier reconstruction are not members
    because they describe derivation history. Enum membership does not prove the
    node's domain, space, basis, or rank. The integer ``.value`` is an internal
    discriminant, not a serialization token.
    """

    ambient = 1
    retained = 2


class CellHoppingRepresentationRole(Enum):
    r"""Enumerate finite-inventory roles for a cell-hopping field.

    A cell-hopping field has carrier
    :math:`\widehat H:\Gamma\rightarrow\operatorname{End}(V)` on a finite
    translation domain.

    Attributes
    ----------
    complete_declared_inventory
        Coefficients on every member of the declared finite inventory.
    support_truncated
        Coefficients restricted to one declared support.

    Notes
    -----
    ``complete_declared_inventory`` means complete only for the declared finite
    inventory, never continuum-complete. Fourier conversion and support truncation
    are transformation kinds, not members of this enum. The integer ``.value`` is
    an internal discriminant, not a serialization token.
    """

    complete_declared_inventory = 1
    support_truncated = 2


def _require_nonempty_exact_string(value: str, name: str, /) -> str:
    """Validate one exact nonempty built-in string without normalization."""
    if type(value) is not str:
        raise TypeError(f"{name} must be an exact built-in string")
    if value == "":
        raise ValueError(f"{name} must not be empty")
    return value


@final
@dataclass(frozen=True, slots=True)
class RepresentationIdentity:
    """Identify one representation node and its interpreted finite space.

    Parameters
    ----------
    representation_id
        Exact nonempty identity of this graph node.
    domain
        Exact momentum or translation domain object. Its nominal type must agree
        with ``role``.
    space
        Exact represented-space identity containing state space, ordered basis,
        geometry, energy reference, scalar field, and coordinate convention.
    role
        :class:`BlochSpaceRole` for a momentum domain or
        :class:`CellHoppingRepresentationRole` for a translation domain.
    source_artifact_id
        Exact nonempty identity of the source formula, calculation, or artifact.

    Raises
    ------
    TypeError
        If a field violates its exact nominal type or the role does not belong to
        the supplied carrier-domain family.
    ValueError
        If a textual identity is empty.

    Notes
    -----
    ``domain_id`` and ``rank`` are derived. Derivation history belongs to typed
    transformation edges rather than mutually exclusive node-role members.
    """

    representation_id: str
    domain: FiniteMomentumMeshDomain | FiniteTranslationDomain
    space: RepresentationSpaceIdentity
    role: BlochSpaceRole | CellHoppingRepresentationRole
    source_artifact_id: str

    def __post_init__(self) -> None:
        """Validate exact identity, domain/role family, space, and source.

        Raises
        ------
        TypeError
            If a field violates its exact nominal type or domain/role family.
        ValueError
            If a textual identity is empty.
        """
        _require_nonempty_exact_string(
            self.representation_id,
            "representation identity",
        )
        if type(self.space) is not RepresentationSpaceIdentity:
            raise TypeError("space must be an exact RepresentationSpaceIdentity")
        if type(self.domain) is FiniteMomentumMeshDomain:
            if type(self.role) is not BlochSpaceRole:
                raise TypeError("a momentum domain requires a BlochSpaceRole")
        elif type(self.domain) is FiniteTranslationDomain:
            if type(self.role) is not CellHoppingRepresentationRole:
                raise TypeError(
                    "a translation domain requires a CellHoppingRepresentationRole"
                )
        else:
            raise TypeError(
                "domain must be an exact FiniteMomentumMeshDomain or "
                "FiniteTranslationDomain"
            )
        _require_nonempty_exact_string(
            self.source_artifact_id,
            "source artifact identity",
        )

    @property
    def domain_id(self) -> str:
        """Return the exact composed carrier-domain identity.

        Returns
        -------
        str
            Exact ``domain.identity`` value.
        """
        return self.domain.identity

    @property
    def rank(self) -> int:
        """Return the composed represented-space dimension.

        Returns
        -------
        int
            Positive exact ``space.dimension`` value.
        """
        return self.space.dimension

    @property
    def space_id(self) -> str:
        """Return the composed represented-space identity.

        Returns
        -------
        str
            Exact ``space.identifier`` value.
        """
        return self.space.identifier

    @property
    def basis_id(self) -> str:
        """Return the exact composed basis identity.

        Returns
        -------
        str
            Exact ``space.basis.identifier`` value.
        """
        return self.space.basis.identifier


@final
class RepresentationIdentityFactory:
    """Construct representation identities from complete domain objects.

    The carrier-specific methods keep enum choices visible and derive domain identity
    and rank from their complete owners rather than accepting parallel values.
    """

    __slots__ = ()

    def create_bloch(
        self,
        *,
        representation_id: str,
        domain: FiniteMomentumMeshDomain,
        space: RepresentationSpaceIdentity,
        role: BlochSpaceRole,
        source_artifact_id: str,
    ) -> RepresentationIdentity:
        """Construct one momentum-domain Bloch representation identity.

        Parameters
        ----------
        representation_id
            Exact nonempty graph-node identity.
        domain
            Exact finite momentum domain.
        space
            Exact represented-space identity.
        role
            Explicit Bloch-space enum member.
        source_artifact_id
            Exact nonempty source identity.

        Returns
        -------
        RepresentationIdentity
            Validated immutable Bloch-node identity.
        """
        if type(domain) is not FiniteMomentumMeshDomain:
            raise TypeError("domain must be an exact FiniteMomentumMeshDomain")
        if type(role) is not BlochSpaceRole:
            raise TypeError("role must be an exact BlochSpaceRole")
        return RepresentationIdentity(
            representation_id=representation_id,
            domain=domain,
            space=space,
            role=role,
            source_artifact_id=source_artifact_id,
        )

    def create_cell_hopping(
        self,
        *,
        representation_id: str,
        domain: FiniteTranslationDomain,
        space: RepresentationSpaceIdentity,
        role: CellHoppingRepresentationRole,
        source_artifact_id: str,
    ) -> RepresentationIdentity:
        """Construct one translation-domain cell-hopping identity.

        Parameters
        ----------
        representation_id
            Exact nonempty graph-node identity.
        domain
            Exact finite translation domain.
        space
            Exact represented-space identity.
        role
            Explicit cell-hopping inventory-role enum member.
        source_artifact_id
            Exact nonempty source identity.

        Returns
        -------
        RepresentationIdentity
            Validated immutable cell-hopping node identity.
        """
        if type(domain) is not FiniteTranslationDomain:
            raise TypeError("domain must be an exact FiniteTranslationDomain")
        if type(role) is not CellHoppingRepresentationRole:
            raise TypeError("role must be an exact CellHoppingRepresentationRole")
        return RepresentationIdentity(
            representation_id=representation_id,
            domain=domain,
            space=space,
            role=role,
            source_artifact_id=source_artifact_id,
        )


__all__ = [
    "BlochSpaceRole",
    "CellHoppingRepresentationRole",
    "RepresentationIdentity",
    "RepresentationIdentityFactory",
]
