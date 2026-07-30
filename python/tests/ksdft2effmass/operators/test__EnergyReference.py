from typing import Any

import pytest

from ksdft2effmass.operators import EnergyReference


def test_public_import_constructs_energy_reference() -> None:
    reference = EnergyReference("valence-band maximum", "eV")

    assert reference.zero == "valence-band maximum"
    assert reference.unit == "eV"


@pytest.mark.parametrize(
    "field, value",
    [("zero", ""), ("unit", "")],
)
def test_string_fields_must_be_nonempty(field: str, value: str) -> None:
    kwargs: dict[str, Any] = {"zero": "explicit zero", "unit": "eV"}
    kwargs[field] = value

    with pytest.raises(ValueError, match="must not be empty"):
        EnergyReference(**kwargs)


@pytest.mark.parametrize(
    "field, value",
    [("zero", None), ("unit", 1)],
)
def test_string_fields_must_be_strings(field: str, value: Any) -> None:
    kwargs: dict[str, Any] = {"zero": "explicit zero", "unit": "eV"}
    kwargs[field] = value

    with pytest.raises(TypeError, match="must be a string"):
        EnergyReference(**kwargs)


def test_energy_reference_has_no_unapplied_numeric_offset_field() -> None:
    reference = EnergyReference("explicit zero", "eV")

    assert not hasattr(reference, "value")
