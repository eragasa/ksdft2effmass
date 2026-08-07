r"""Software verification of ``OperatorRecordComparisonResult``.

Facet and represented meaning
-----------------------------
This class-owned module owns the value semantics facet. System under test and
evidence class
------------------------------------
This software-verification module provides ``SV-ORCR-012`` and ``SV-ORCR-013``
for operationally immutable slotted state and exact structural equality.

Requirements, strategy, and acceptance
--------------------------------------
Normal public assignment syntax must not reassign declared fields or add dynamic
attributes. Independently constructed objects with identical public state must
compare equal; valid objects differing in any one public field must compare
unequal. Every altered metric tuple remains mathematically ordered.

Ownership, interpretation, and limitations
------------------------------------------
Equality compares exact stored ResultObject state. It is not approximate
numerical comparison and does not establish physical operator equivalence.
Approximate numerical behavior belongs to analyzer numerical-verification tests.
Passing establishes the tested immutable and exact-equality behavior. Failure
may indicate a ResultObject implementation regression, contract/documentation
mismatch, or evidence defect requiring investigation; it does not by itself
establish analyzer numerical failure, physical-model error, scientific
invalidity, or quantified uncertainty. Hashability is not documented as a
public contract, so this module deliberately adds no hash assertion and does not
freeze incidental dataclass behavior into the API. Numerical verification is
not applicable to direct ResultObject value semantics. Scientific validation and
uncertainty quantification have not been performed.

Intrinsic and cross-object scope
--------------------------------
The primary owner is ``OperatorRecordComparisonResult``; collaborators only
construct inputs or expose public outcomes. Accepted public contracts, literal
expected values, Python language semantics, and assigned schema or fixture artifacts
provide the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.operators import OperatorRecordComparisonResult

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordComparisonResult

EQUALITY_FIELDS = (
    "reference_identifier",
    "candidate_identifier",
    "matrix_dimension",
    "energy_unit",
    "maximum_absolute_residual",
    "frobenius_residual",
    "spectral_residual",
)


def comparison_result(
    *,
    reference_identifier: str = "reference",
    candidate_identifier: str = "candidate",
    matrix_dimension: int = 2,
    energy_unit: str = "eV",
    maximum_absolute_residual: float = 1.0,
    frobenius_residual: float = 4.0,
    spectral_residual: float = 3.0,
) -> OperatorRecordComparisonResult:
    r"""Evidence ID
    Owns no identifier; supports evidence in this module.
    Requirement
    Comparison-result cases require a valid baseline whose public fields can be
    overridden one partition at a time.
    Method
    Construct or inspect only the named synthetic fixture operation (comparison result);
    the helper owns no assertion result and introduces no hidden oracle.
    Oracle
    Literal constructor values, the declared public-field inventory where completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.
    Acceptance
    The helper returns exactly the requested fixture value or applies only the
    documented comparison; all pass/fail assertions remain in the owning test.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    return OperatorRecordComparisonResult(
        reference_identifier=reference_identifier,
        candidate_identifier=candidate_identifier,
        matrix_dimension=matrix_dimension,
        energy_unit=energy_unit,
        maximum_absolute_residual=maximum_absolute_residual,
        frobenius_residual=frobenius_residual,
        spectral_residual=spectral_residual,
    )


@pytest.mark.parametrize(
    ("field_name", "new_value"),
    [
        pytest.param(
            "reference_identifier",
            "changed-reference",
            id="sv_orcr_012_identifying_field",
        ),
        pytest.param("maximum_absolute_residual", 0.5, id="sv_orcr_012_metric_field"),
        pytest.param(
            "undeclared_attribute", "dynamic-state", id="sv_orcr_012_dynamic_attribute"
        ),
    ],
)
def test_constructor__enforce_immutable_slotted_state__is_enforced(
    field_name: str, new_value: object
) -> None:
    r"""Evidence ID
    SV-ORCR-012
    Requirement
    Frozen slotted state rejects representative identity-field and metric-field
    assignment as well as creation of an undeclared attribute.
    Method
    Construct valid baseline instances, change only the named enforce immutable slotted
    state: is enforced partition, and observe constructor, field, equality, hash, or
    public-API behavior as applicable.
    Oracle
    Literal constructor values, the declared public-field inventory where completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.
    Acceptance
    The named partition raises exactly FrozenInstanceError with the asserted public
    message, code, or attached result; no alternate exception is accepted.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    result = comparison_result()

    with pytest.raises(FrozenInstanceError):
        setattr(result, field_name, new_value)


@pytest.mark.parametrize(
    ("field_name", "changed_value"),
    [
        pytest.param("reference_identifier", "other-reference", id="reference_unequal"),
        pytest.param("candidate_identifier", "other-candidate", id="candidate_unequal"),
        pytest.param("matrix_dimension", 3, id="dimension_unequal"),
        pytest.param("energy_unit", "Ry", id="unit_unequal"),
        pytest.param(
            "maximum_absolute_residual", 2.0, id="maximum_unequal_valid_order"
        ),
        pytest.param("spectral_residual", 3.5, id="valid_order"),
        pytest.param("frobenius_residual", 5.0, id="valid_order"),
    ],
)
def test_method__eq__provide_exact_structural_equality(
    field_name: str, changed_value: object
) -> None:
    r"""Evidence ID
    SV-ORCR-013
    Requirement
    OperatorRecordComparisonResult equality is exact over every declared public field
    and distinguishes each field independently.
    Method
    Construct valid baseline instances, change only the named eq: provide exact
    structural equality partition, and observe constructor, field, equality, hash, or
    public-API behavior as applicable.
    Oracle
    Literal constructor values, the declared public-field inventory where completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.
    Acceptance
    The equal baseline compares equal, every independently varied inventoried field
    compares unequal, and comparison with an unrelated object is false.
    Interpretation
    A pass supports only this named public-contract partition; failure identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.
    Limitations
    The synthetic software cases do not establish numerical verification, physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    assert EQUALITY_FIELDS == (
        "reference_identifier",
        "candidate_identifier",
        "matrix_dimension",
        "energy_unit",
        "maximum_absolute_residual",
        "frobenius_residual",
        "spectral_residual",
    )
    first = comparison_result()
    second = comparison_result()
    changed = comparison_result(**{field_name: changed_value})  # type: ignore[arg-type]

    assert first == second
    assert first != changed
    assert first != object()
