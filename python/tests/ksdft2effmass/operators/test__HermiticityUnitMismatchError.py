"""Object tests for structured Hermiticity unit-mismatch errors."""

from ksdft2effmass.operators import HermiticityUnitMismatchError


def test_error_retains_analyzer_and_record_units() -> None:
    error = HermiticityUnitMismatchError("eV", "hartree")

    assert error.analyzer_energy_unit == "eV"
    assert error.record_energy_unit == "hartree"
    assert "energy unit" in str(error)


def test_error_has_no_json_serialization_api() -> None:
    error = HermiticityUnitMismatchError("eV", "hartree")

    assert not hasattr(error, "serialize")
    assert not hasattr(error, "to_dict")
