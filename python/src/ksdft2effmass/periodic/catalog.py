"""Explicit immutable catalogs for periodic scientific models."""

from dataclasses import dataclass

from ksdft2effmass.periodic.models import (
    PeriodicModel,
    PeriodicModelRole,
    SpatialDimension,
)
from ksdft2effmass.periodic.periodic1d.models import Periodic1DModel
from ksdft2effmass.periodic.periodic2d.models import Periodic2DModel
from ksdft2effmass.periodic.periodic3d.models import Periodic3DModel


@dataclass(frozen=True, slots=True)
class PeriodicControlModelCatalog:
    """Store an ordered, explicitly registered inventory of control models.

    Parameters
    ----------
    models
        A nonempty exact tuple of nominal periodic models. Every model must declare
        the exact ``CONTROL_MODEL`` role, a nonempty unique identifier, and
        membership in the dimension-specific nominal branch matching its reported
        dimension.

    Notes
    -----
    Tuple order is catalog order and is preserved. The catalog performs no module
    scanning, subclass discovery, model evaluation, comparison, or acceptance.

    """

    models: tuple[PeriodicModel, ...]

    def __post_init__(self) -> None:
        """Validate explicit membership, roles, dimensions, and identities.

        Raises
        ------
        TypeError
            If the inventory or a model attribute lacks its exact runtime owner.
        ValueError
            If the inventory is empty, identities repeat, a role is not a control
            role, or reported dimension disagrees with admitted dimensional ownership.

        """
        if type(self.models) is not tuple:
            raise TypeError("models must be an exact tuple")
        if not self.models:
            raise ValueError("models must be nonempty")

        observed_ids: set[str] = set()
        for model in self.models:
            if not isinstance(model, PeriodicModel):
                raise TypeError("every catalog member must be a PeriodicModel")
            if type(model.model_role) is not PeriodicModelRole:
                raise TypeError("model_role must be a PeriodicModelRole")
            if model.model_role is not PeriodicModelRole.CONTROL_MODEL:
                raise ValueError(
                    "every catalog member must have the CONTROL_MODEL role"
                )
            if type(model.model_id) is not str:
                raise TypeError("model_id must be an exact str")
            if not model.model_id:
                raise ValueError("model_id must be nonempty")
            if model.model_id in observed_ids:
                raise ValueError("model_id values must be unique")
            observed_ids.add(model.model_id)

            dimension = model.spatial_dimension
            if type(dimension) is not int:
                raise TypeError("spatial_dimension must be an exact int")
            # Every fixed-rank block-hopping model now refines its dimensional model
            # owner, so the catalog needs only the nominal dimensional membership.
            expected_membership = {
                1: Periodic1DModel,
                2: Periodic2DModel,
                3: Periodic3DModel,
            }.get(dimension)
            if expected_membership is None:
                raise ValueError("spatial_dimension must be 1, 2, or 3")
            if not isinstance(model, expected_membership):
                raise ValueError(
                    "spatial_dimension must agree with nominal dimension membership"
                )

    @property
    def model_ids(self) -> tuple[str, ...]:
        """Return model identities in deterministic catalog order.

        Returns
        -------
        tuple[str, ...]
            Stable model identities in exact caller registration order.

        """
        return tuple(model.model_id for model in self.models)

    @property
    def spatial_dimensions(self) -> tuple[SpatialDimension, ...]:
        """Return exact dimensions in deterministic catalog order.

        Returns
        -------
        tuple[SpatialDimension, ...]
            Built-in spatial dimensions in exact caller registration order.

        """
        return tuple(model.spatial_dimension for model in self.models)


__all__ = ["PeriodicControlModelCatalog"]
