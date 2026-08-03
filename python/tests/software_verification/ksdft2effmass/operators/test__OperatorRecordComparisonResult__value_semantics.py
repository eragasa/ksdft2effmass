"""Value-semantics evidence for ``OperatorRecordComparisonResult``.

System under test and evidence class
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
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.operators import OperatorRecordComparisonResult

pytestmark = pytest.mark.software_verification


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
    """Construct valid synthetic comparison state without test-side coercion.

    Every argument maps directly to the same-named public field. Defaults satisfy
    ``0 <= maximum <= spectral <= Frobenius`` and use deterministic synthetic
    ``eV`` metadata. The helper performs no canonicalization and establishes no
    physical meaning or scientific validity.
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
            id="SV-ORCR-012-identifying-field",
        ),
        pytest.param(
            "maximum_absolute_residual",
            0.5,
            id="SV-ORCR-012-metric-field",
        ),
        pytest.param(
            "undeclared_attribute",
            "dynamic-state",
            id="SV-ORCR-012-dynamic-attribute",
        ),
    ],
)
def test_enforce_immutable_slotted_state(field_name: str, new_value: object) -> None:
    """SV-ORCR-012: prevent field reassignment and dynamic state.

    Requirement
        Public identifying and metric fields are immutable, and slotted state
        excludes undeclared dynamic attributes.
    Method and acceptance
        Use normal public ``setattr`` syntax and require
        ``FrozenInstanceError`` for each independently collected assignment.
    Interpretation and limitations
        Passing verifies ordinary public mutation resistance without inspecting
        private dataclass machinery or asserting hash behavior.
    """

    result = comparison_result()

    with pytest.raises(FrozenInstanceError):
        setattr(result, field_name, new_value)


@pytest.mark.parametrize(
    ("field_name", "changed_value"),
    [
        pytest.param(
            "reference_identifier",
            "other-reference",
            id="SV-ORCR-013-reference-unequal",
        ),
        pytest.param(
            "candidate_identifier",
            "other-candidate",
            id="SV-ORCR-013-candidate-unequal",
        ),
        pytest.param("matrix_dimension", 3, id="SV-ORCR-013-dimension-unequal"),
        pytest.param("energy_unit", "Ry", id="SV-ORCR-013-unit-unequal"),
        pytest.param(
            "maximum_absolute_residual",
            2.0,
            id="SV-ORCR-013-maximum-unequal-valid-order",
        ),
        pytest.param(
            "spectral_residual",
            3.5,
            id="SV-ORCR-013-spectral-unequal-valid-order",
        ),
        pytest.param(
            "frobenius_residual",
            5.0,
            id="SV-ORCR-013-frobenius-unequal-valid-order",
        ),
    ],
)
def test_provide_exact_structural_equality(
    field_name: str, changed_value: object
) -> None:
    """SV-ORCR-013: compare every public field by exact stored value.

    Requirement
        Independently constructed equal state compares equal; a valid change to
        any one public field compares unequal; unrelated objects compare unequal
        through normal equality syntax.
    Method and acceptance
        Compare two independent default objects, then one valid single-field
        variant selected by the collected case. Metric variants preserve
        ``maximum <= spectral <= Frobenius``.
    Interpretation and limitations
        Equality is exact structural equality, not approximate residual
        comparison or physical operator equivalence. Hash behavior remains
        intentionally unspecified.
    """

    first = comparison_result()
    second = comparison_result()
    changed = comparison_result(**{field_name: changed_value})  # type: ignore[arg-type]

    assert first == second
    assert first != changed
    assert first != object()
