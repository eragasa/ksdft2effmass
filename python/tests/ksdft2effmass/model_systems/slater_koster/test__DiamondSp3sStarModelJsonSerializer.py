"""Software verification for deterministic ``sp3s*`` model serialization."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

import numpy as np
import pytest
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity

from ksdft2effmass.model_systems.slater_koster import (
    DiamondSp3sStarGeometry,
    DiamondSp3sStarModel,
    DiamondSp3sStarModelJsonSerializer,
    DiamondSp3sStarParameters,
)
from ksdft2effmass.periodic.periodic3d.operators.basis import Periodic3DBasisIdentity
from ksdft2effmass.serialization import TypedJsonMappingDeserializer

pytestmark = pytest.mark.software_verification


class TestDiamondSp3sStarModelJsonSerializer:
    """Own stable convention-rich typed JSON without scientific result claims."""

    def test_serialize__same_model_twice__returns_identical_canonical_bytes(
        self,
    ) -> None:
        serializer = DiamondSp3sStarModelJsonSerializer()
        model = self._model()

        first = serializer.serialize(model)
        second = serializer.serialize(model)
        document = TypedJsonMappingDeserializer().deserialize(first)
        basis_mapping = document["basis"]
        geometry = document["geometry"]
        parameters = document["parameters"]
        assert isinstance(basis_mapping, Mapping)
        assert isinstance(geometry, Mapping)
        assert isinstance(parameters, Mapping)
        first_neighbor = parameters["first_neighbor"]
        assert isinstance(first_neighbor, Mapping)

        assert first == second
        assert first.endswith(b"\n")
        assert document["schema_version"] == 2
        assert document["model"] == "homopolar-diamond-spinless-sp3s-star"
        assert Periodic3DBasisIdentity.from_dict(basis_mapping) == model.basis_identity
        assert document["parameter_order"] == model.parameters.parameter_names
        assert first_neighbor["fixed_V1_s_s_star_sigma"] == ScalarQuantity(
            0.0,
            PhysicalUnit("electron_volt"),
        )
        first_cells = geometry["first_neighbor_A_to_B_target_cells"]
        phase_convention = document["phase_convention"]
        assert isinstance(first_cells, tuple)
        assert isinstance(phase_convention, str)
        assert len(first_cells) == 4
        assert "R+tau" in phase_convention
        assert "fit" not in document
        assert "oracle" not in document

    def test_serialize__wrong_type__rejects(self) -> None:
        serializer = DiamondSp3sStarModelJsonSerializer()
        wrong = cast(DiamondSp3sStarModel, self._model().parameters)

        with pytest.raises(TypeError, match="must be DiamondSp3sStarModel"):
            serializer.serialize(wrong)

    @staticmethod
    def _model() -> DiamondSp3sStarModel:
        return DiamondSp3sStarModel(
            geometry=DiamondSp3sStarGeometry(
                ScalarQuantity(5.4, PhysicalUnit("angstrom"))
            ),
            parameters=DiamondSp3sStarParameters.from_vector_ev(
                np.linspace(-1.0, 1.0, 15)
            ),
        )
