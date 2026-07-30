"""Object tests for public compatibility mismatch-code reachability order."""

from ksdft2effmass.operators import OperatorRecordCompatibilityMismatchCode

EXPECTED_CODES = (
    ("MATRIX_DIMENSION_MISMATCH", "matrix_dimension_mismatch"),
    ("STATE_SPACE_KIND_MISMATCH", "state_space_kind_mismatch"),
    ("OPERATOR_KIND_MISMATCH", "operator_kind_mismatch"),
    ("ORDERED_BASIS_LABELS_MISMATCH", "ordered_basis_labels_mismatch"),
    ("BASIS_KIND_MISMATCH", "basis_kind_mismatch"),
    ("LATTICE_VECTORS_MISMATCH", "lattice_vectors_mismatch"),
    ("BOUNDARY_CONDITIONS_MISMATCH", "boundary_conditions_mismatch"),
    ("COORDINATE_CONVENTION_MISMATCH", "coordinate_convention_mismatch"),
    ("GEOMETRY_LENGTH_UNIT_MISMATCH", "geometry_length_unit_mismatch"),
    ("ENERGY_UNIT_MISMATCH", "energy_unit_mismatch"),
    ("ENERGY_ZERO_CONVENTION_MISMATCH", "energy_zero_convention_mismatch"),
)


def test_public_import_exposes_all_stable_mismatch_codes_in_rule_order() -> None:
    assert (
        tuple(
            (code.name, code.value) for code in OperatorRecordCompatibilityMismatchCode
        )
        == EXPECTED_CODES
    )


def test_mismatch_code_values_are_machine_readable_strings() -> None:
    for code in OperatorRecordCompatibilityMismatchCode:
        assert isinstance(code.value, str)
        assert code.value == code.value.lower()
        assert " " not in code.value


def test_removed_orthonormality_mismatch_is_not_public() -> None:
    assert not hasattr(
        OperatorRecordCompatibilityMismatchCode, "ORTHONORMALITY_CONVENTION_MISMATCH"
    )
