"""Software verification for the stable ``sp3s*`` parameter map."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import numpy as np
import pytest
from projectkoios.physkit.units import PhysicalUnit, ScalarQuantity

from ksdft2effmass.model_systems.slater_koster import DiamondSp3sStarParameters

pytestmark = pytest.mark.software_verification


class TestDiamondSp3sStarParameters:
    """Own unit, ordering, immutability, and public numeric-boundary checks."""

    def test_from_vector_ev__valid_values__round_trips_stable_order(self) -> None:
        values = np.linspace(-7.0, 7.0, 15, dtype=np.float64)

        parameters = DiamondSp3sStarParameters.from_vector_ev(values)

        assert parameters.parameter_names == (
            "E_s",
            "E_p",
            "E_s_star",
            "V1_ss_sigma",
            "V1_sp_sigma",
            "V1_pp_sigma",
            "V1_pp_pi",
            "V1_s_star_p_sigma",
            "V2_ss_sigma",
            "V2_sp_sigma",
            "V2_pp_sigma",
            "V2_pp_pi",
            "V2_s_star_p_sigma",
            "V2_s_s_star_sigma",
            "V2_s_star_s_star_sigma",
        )
        np.testing.assert_array_equal(parameters.as_vector_ev(), values)
        assert parameters.as_vector_ev().flags.writeable is False
        assert all(
            value.unit == PhysicalUnit("electron_volt")
            for value in parameters.ordered_quantities()
        )

    def test_from_vector_ev__boolean_or_numeric_string__rejects(self) -> None:
        with pytest.raises(TypeError, match="real numbers excluding booleans"):
            DiamondSp3sStarParameters.from_vector_ev(np.ones(15, dtype=np.bool_))
        with pytest.raises(TypeError, match="real numbers excluding booleans"):
            DiamondSp3sStarParameters.from_vector_ev(np.full(15, "1.0", dtype=np.str_))

    def test_from_vector_ev__wrong_shape_or_nonfinite__rejects(self) -> None:
        with pytest.raises(ValueError, match=r"shape \(15,\)"):
            DiamondSp3sStarParameters.from_vector_ev(np.ones(14))
        invalid = np.ones(15)
        invalid[7] = np.inf
        with pytest.raises(ValueError, match="finite"):
            DiamondSp3sStarParameters.from_vector_ev(invalid)

    def test_energy_fields__wrong_unit__reject(self) -> None:
        parameters = DiamondSp3sStarParameters.from_vector_ev(np.zeros(15))

        with pytest.raises(ValueError, match="electron_volt"):
            type(parameters.onsite)(
                ScalarQuantity(0.0, PhysicalUnit("joule")),
                parameters.onsite.p,
                parameters.onsite.s_star,
            )

    def test_parameter_record__mutation__is_forbidden(self) -> None:
        parameters = DiamondSp3sStarParameters.from_vector_ev(np.zeros(15))

        with pytest.raises(FrozenInstanceError):
            parameters.onsite = parameters.onsite  # type: ignore[misc]
