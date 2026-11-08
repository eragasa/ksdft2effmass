"""Nominal root for periodic KSD scientific models."""

from abc import ABC, abstractmethod
from typing import Literal

from ksdft2effmass.models.base import Model
from ksdft2effmass.serialization import StrWireEnum

type SpatialDimension = Literal[1, 2, 3]


class PeriodicModelRole(StrWireEnum):
    """Classify the evidentiary role of a periodic scientific model.

    ``CONTROL_MODEL`` identifies a controlled model used to isolate mathematical,
    numerical, or software behavior. ``MATERIAL_REFERENCE`` identifies an explicitly
    specified material model without implying scientific validation or physical
    completeness. ``REDUCED_MODEL`` identifies a parameterized effective model intended
    to be fitted or compared with an identified reference; the role does not imply that
    fitting, verification, or scientific validation has completed.
    """

    CONTROL_MODEL = "control_model"
    MATERIAL_REFERENCE = "material_reference"
    REDUCED_MODEL = "reduced_model"


class PeriodicModel(Model, ABC):
    """Identify a periodic scientific model without choosing dimension or rank.

    Dimension-specific owners supply the exact spatial dimension. Rank-specific owners
    independently supply a retained band-subspace rank. This base owns no provider
    model, represented operator, campaign, serializer, tolerance, or acceptance policy.
    """

    __slots__ = ()

    @property
    @abstractmethod
    def model_role(self) -> PeriodicModelRole:
        """Return the exact scientific-model role.

        Returns
        -------
        PeriodicModelRole
            Closed evidentiary role without an acceptance implication.

        """

    @property
    @abstractmethod
    def spatial_dimension(self) -> SpatialDimension:
        """Return the exact built-in periodic spatial dimension.

        Returns
        -------
        SpatialDimension
            Built-in integer one, two, or three.

        """


__all__ = ["PeriodicModel", "PeriodicModelRole", "SpatialDimension"]
