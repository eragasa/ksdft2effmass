"""Software verification for deterministic ``sp3s*`` model serialization."""

from __future__ import annotations

import json
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
        document = json.loads(first)

        assert first == second
        assert first.endswith(b"\n")
        assert document["schema_version"] == 1
        assert document["model"] == "homopolar-diamond-spinless-sp3s-star"
        assert document["basis_order"]["__ksd_type__"] == "tuple"
        assert document["parameter_order"]["items"] == list(
            model.parameters.parameter_names
        )
        fixed_zero = document["parameters"]["first_neighbor"]["fixed_V1_s_s_star_sigma"]
        assert fixed_zero["magnitude"] == 0.0
        assert fixed_zero["unit"]["expression"] == "electron_volt"
        first_cells = document["geometry"]["first_neighbor_A_to_B_target_cells"]
        assert len(first_cells["items"]) == 4
        assert "R+tau" in document["phase_convention"]
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
