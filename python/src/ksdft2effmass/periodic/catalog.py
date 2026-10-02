"""Explicit immutable catalogs for periodic scientific models."""

from dataclasses import dataclass

from .model import (
    Periodic1DModel,
    Periodic2DModel,
    Periodic3DModel,
    PeriodicModel,
    PeriodicModelRole,
    SpatialDimension,
)


@dataclass(frozen=True, slots=True)
class PeriodicToyModelCatalog:
    """Store an ordered, explicitly registered inventory of toy models.

    Parameters
    ----------
    models
        A nonempty exact tuple of nominal periodic models. Every model must declare
        the exact ``TOY`` role, a nonempty unique identifier, and membership in the
        dimension-specific nominal branch matching its reported dimension.

    Notes
    -----
    Tuple order is catalog order and is preserved. The catalog performs no module
    scanning, subclass discovery, model evaluation, comparison, or acceptance.
    """

    models: tuple[PeriodicModel, ...]

    def __post_init__(self) -> None:
        """Validate explicit membership, roles, dimensions, and identities."""
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
            if model.model_role is not PeriodicModelRole.TOY:
                raise ValueError("every catalog member must have the TOY role")
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
        """Return model identities in deterministic catalog order."""
        return tuple(model.model_id for model in self.models)

    @property
    def spatial_dimensions(self) -> tuple[SpatialDimension, ...]:
        """Return exact dimensions in deterministic catalog order."""
        return tuple(model.spatial_dimension for model in self.models)


__all__ = ["PeriodicToyModelCatalog"]
