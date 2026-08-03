"""Intrinsic-invariant evidence for ``OperatorRecordComparisonResult``.

System under test and evidence class
------------------------------------
This software-verification module provides ``SV-ORCR-005`` through
``SV-ORCR-011`` for the ResultObject's identifiers, energy unit, structural
dimension, admitted residual scalars, exact mathematical ordering, strict raw
roundoff-order rejection, and conversion-overflow taxonomy.

Requirements, strategy, and acceptance
--------------------------------------
Every invalid field is supplied through normal public construction. Independently
collected parameter cases require ``TypeError`` for wrong semantic types and
``ValueError`` for admitted values that violate nonemptiness, positivity,
finiteness, non-negativity, representability, or metric ordering. Diagnostics
must identify the affected field.

Ownership, interpretation, and limitations
------------------------------------------
Scalar finiteness and exact stored ordering are intrinsic software invariants.
The producing ``OperatorRecordResidualAnalyzer`` computes raw metrics, evaluates
its roundoff allowance, canonicalizes permitted discrepancies, and only then
constructs this ResultObject. Direct construction neither calculates allowance
nor repairs values. Passing establishes the tested intrinsic constructor
invariants. Failure may indicate a ResultObject implementation regression,
contract/documentation mismatch, or evidence defect requiring investigation; it
does not by itself establish analyzer numerical failure, physical-model error,
scientific invalidity, or quantified uncertainty. These tests do not execute a
norm algorithm, so numerical verification is not applicable. The ResultObject
has no physical acceptance threshold; valid state does not establish physical
equivalence. Scientific validation and uncertainty quantification have not been
performed.
"""

from dataclasses import dataclass
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import OperatorRecordComparisonResult

pytestmark = pytest.mark.software_verification


def comparison_result(**overrides: object) -> OperatorRecordComparisonResult:
    """Construct the public ResultObject from valid defaults plus overrides.

    The canonical defaults are identifiers ``reference`` and ``candidate``,
    dimension ``2``, unit ``eV``, and metrics ``maximum=1``, ``spectral=3``,
    ``Frobenius=4``. The helper performs no coercion or validation itself; each
    override reaches the public constructor unchanged, where documented scalar
    canonicalization and intrinsic validation occur. The state is synthetic and
    has no physical interpretation.
    """

    values: dict[str, object] = {
        "reference_identifier": "reference",
        "candidate_identifier": "candidate",
        "matrix_dimension": 2,
        "energy_unit": "eV",
        "maximum_absolute_residual": 1.0,
        "frobenius_residual": 4.0,
        "spectral_residual": 3.0,
    }
    values.update(overrides)
    return OperatorRecordComparisonResult(**cast(Any, values))


@pytest.mark.parametrize(
    ("field_name", "bad_value", "expected_error", "expected_message"),
    [
        pytest.param(
            "reference_identifier",
            "",
            ValueError,
            "reference identifier must not be empty",
            id="SV-ORCR-005-reference-empty",
        ),
        pytest.param(
            "reference_identifier",
            1,
            TypeError,
            "reference identifier must be a string",
            id="SV-ORCR-005-reference-python-int",
        ),
        pytest.param(
            "reference_identifier",
            object(),
            TypeError,
            "reference identifier must be a string",
            id="SV-ORCR-005-reference-object",
        ),
        pytest.param(
            "candidate_identifier",
            "",
            ValueError,
            "candidate identifier must not be empty",
            id="SV-ORCR-005-candidate-empty",
        ),
        pytest.param(
            "candidate_identifier",
            1,
            TypeError,
            "candidate identifier must be a string",
            id="SV-ORCR-005-candidate-python-int",
        ),
        pytest.param(
            "candidate_identifier",
            object(),
            TypeError,
            "candidate identifier must be a string",
            id="SV-ORCR-005-candidate-object",
        ),
    ],
)
def test_enforce_identifier_invariants(
    field_name: str,
    bad_value: object,
    expected_error: type[Exception],
    expected_message: str,
) -> None:
    """SV-ORCR-005: enforce each identifier role independently.

    Requirement
        Reference and candidate identifiers are independently nonempty strings.
    Method and acceptance
        Supply one invalid role per collected case and require the exact
        ``TypeError``/``ValueError`` class and field-specific diagnostic.
    Interpretation and limitations
        Passing verifies identifier state only; no trimming or string-subclass
        policy beyond the documented constructor behavior is asserted.
    """

    with pytest.raises(expected_error, match=expected_message):
        comparison_result(**{field_name: bad_value})


@pytest.mark.parametrize(
    ("bad_value", "expected_error", "expected_message"),
    [
        pytest.param(
            "", ValueError, "energy unit must not be empty", id="SV-ORCR-006-empty"
        ),
        pytest.param(
            1, TypeError, "energy unit must be a string", id="SV-ORCR-006-python-int"
        ),
        pytest.param(
            object(),
            TypeError,
            "energy unit must be a string",
            id="SV-ORCR-006-object",
        ),
    ],
)
def test_enforce_energy_unit_invariants(
    bad_value: object,
    expected_error: type[Exception],
    expected_message: str,
) -> None:
    """SV-ORCR-006: require a nonempty energy-unit string.

    Requirement and method
        Supply empty or wrong-semantic-type unit state through public
        construction.
    Acceptance
        The exact documented exception class and unit-specific message match.
    Interpretation and limitations
        Passing verifies stored unit metadata; no conversion or dimensional
        consistency with an external object is performed.
    """

    with pytest.raises(expected_error, match=expected_message):
        comparison_result(energy_unit=bad_value)


@pytest.mark.parametrize(
    ("bad_value", "expected_error", "expected_message"),
    [
        pytest.param(
            0, ValueError, "matrix_dimension must be positive", id="SV-ORCR-007-zero"
        ),
        pytest.param(
            -1,
            ValueError,
            "matrix_dimension must be positive",
            id="SV-ORCR-007-negative-python-int",
        ),
        pytest.param(
            np.int64(-1),
            ValueError,
            "matrix_dimension must be positive",
            id="SV-ORCR-007-negative-numpy-int",
        ),
        pytest.param(
            True,
            TypeError,
            "matrix_dimension must be a positive integer",
            id="SV-ORCR-007-python-bool",
        ),
        pytest.param(
            np.bool_(True),
            TypeError,
            "matrix_dimension must be a positive integer",
            id="SV-ORCR-007-numpy-bool",
        ),
        pytest.param(
            2.0,
            TypeError,
            "matrix_dimension must be a positive integer",
            id="SV-ORCR-007-python-float",
        ),
        pytest.param(
            "2",
            TypeError,
            "matrix_dimension must be a positive integer",
            id="SV-ORCR-007-numeric-string",
        ),
        pytest.param(
            object(),
            TypeError,
            "matrix_dimension must be a positive integer",
            id="SV-ORCR-007-object",
        ),
    ],
)
def test_enforce_matrix_dimension_invariants(
    bad_value: object,
    expected_error: type[Exception],
    expected_message: str,
) -> None:
    """SV-ORCR-007: enforce integer type and positive dimension.

    Requirement
        Python and NumPy integer scalars are admitted, then required to be
        positive; Boolean, floating, string, and arbitrary-object inputs are not
        integer semantics.
    Method and acceptance
        Collect each invalid category independently and require exact exception
        taxonomy with a dimension-specific diagnostic.
    Interpretation and limitations
        Positive NumPy canonicalization is covered by ``SV-ORCR-002``. No upper
        dimension policy or allocation feasibility is tested here.
    """

    with pytest.raises(expected_error, match=expected_message):
        comparison_result(matrix_dimension=bad_value)


@dataclass(frozen=True, slots=True)
class ResidualInvariantCase:
    """One invalid residual-scalar admission case.

    ``field_name`` selects the public metric without renaming it; ``field_label``
    is the readable pytest-ID component; ``bad_value`` reaches the constructor
    without test-side coercion; ``value_label`` names its semantic category;
    ``expected_error`` and ``expected_message`` define the public taxonomy and
    field-specific oracle. This table is synthetic software evidence and does
    not contain expected numerical-analysis output.
    """

    field_name: str
    field_label: str
    bad_value: object
    value_label: str
    expected_error: type[Exception]
    expected_message: str


_METRIC_FIELDS = (
    ("maximum_absolute_residual", "maximum"),
    ("frobenius_residual", "frobenius"),
    ("spectral_residual", "spectral"),
)
_INVALID_METRIC_VALUES = (
    ("negative", -1.0, ValueError, "must be non-negative"),
    ("nan", np.nan, ValueError, "must be finite"),
    ("positive-infinity", np.inf, ValueError, "must be finite"),
    ("negative-infinity", -np.inf, ValueError, "must be finite"),
    ("python-bool", True, TypeError, "must be a real number"),
    ("numpy-bool", np.bool_(True), TypeError, "must be a real number"),
    ("numeric-string", "1.0", TypeError, "must be a real number"),
    ("bytes", b"1.0", TypeError, "must be a real number"),
    ("python-complex", 1.0 + 0.0j, TypeError, "must be a real number"),
    ("numpy-complex", np.complex128(1.0 + 0.0j), TypeError, "must be a real number"),
    ("object", object(), TypeError, "must be a real number"),
)
RESIDUAL_INVARIANT_CASES = tuple(
    ResidualInvariantCase(
        field_name,
        field_label,
        bad_value,
        value_label,
        expected_error,
        f"{field_name} {message_suffix}",
    )
    for field_name, field_label in _METRIC_FIELDS
    for value_label, bad_value, expected_error, message_suffix in _INVALID_METRIC_VALUES
)


@pytest.mark.parametrize(
    "case",
    RESIDUAL_INVARIANT_CASES,
    ids=[
        f"SV-ORCR-008-{case.field_label}-{case.value_label}"
        for case in RESIDUAL_INVARIANT_CASES
    ],
)
def test_enforce_residual_scalar_invariants(case: ResidualInvariantCase) -> None:
    """SV-ORCR-008: enforce each residual scalar's admission contract.

    Requirement
        Metrics reject wrong semantic types with ``TypeError`` and admitted real
        values that are negative or nonfinite with ``ValueError``.
    Method and acceptance
        Independently collect every field/category pair and require exact public
        exception taxonomy plus the full affected field name.
    Interpretation and limitations
        Passing verifies scalar state admission, not numerical agreement or a
        physical residual threshold.
    """

    with pytest.raises(case.expected_error, match=case.expected_message):
        comparison_result(**{case.field_name: case.bad_value})


@pytest.mark.parametrize(
    ("maximum", "spectral", "frobenius", "expected_message"),
    [
        pytest.param(
            4.0,
            3.0,
            5.0,
            "maximum_absolute_residual must not exceed spectral_residual",
            id="SV-ORCR-009-maximum-exceeds-spectral",
        ),
        pytest.param(
            1.0,
            3.0,
            2.0,
            "spectral_residual must not exceed frobenius_residual",
            id="SV-ORCR-009-spectral-exceeds-frobenius",
        ),
    ],
)
def test_enforce_mathematical_metric_ordering(
    maximum: float,
    spectral: float,
    frobenius: float,
    expected_message: str,
) -> None:
    r"""SV-ORCR-009: enforce the intrinsic stored norm ordering.

    Requirement
        Direct state must satisfy
        :math:`\varepsilon_{\max}\leq\varepsilon_2\leq\varepsilon_{\mathrm F}`.
    Method and acceptance
        Violate each inequality independently and require its field-specific
        ``ValueError``.
    Interpretation and limitations
        This is structural software verification, not analyzer accuracy or
        physical acceptance evidence.
    """

    with pytest.raises(ValueError, match=expected_message):
        comparison_result(
            maximum_absolute_residual=maximum,
            spectral_residual=spectral,
            frobenius_residual=frobenius,
        )


@pytest.mark.parametrize(
    ("maximum", "spectral", "frobenius"),
    [
        pytest.param(
            1.4142135623730952e100,
            1.4142135623730948e100,
            1.4142135623730952e100,
            id="SV-ORCR-010-known-binary64-regression-a",
        ),
        pytest.param(
            2.23606797749979e100,
            2.2360679774997896e100,
            2.23606797749979e100,
            id="SV-ORCR-010-known-binary64-regression-b",
        ),
    ],
)
def test_reject_uncanonicalized_roundoff_order_violations(
    maximum: float, spectral: float, frobenius: float
) -> None:
    """SV-ORCR-010: reject raw roundoff-inconsistent metric state.

    Requirement
        The ResultObject strictly rejects supplied ``maximum > spectral`` even
        when the inversion resembles binary64 roundoff.
    Method and acceptance
        Supply two known raw regression triples and require the exact ordering
        ``ValueError``.
    Interpretation and limitations
        The analyzer owns raw computation, allowance evaluation, permitted
        upward canonicalization, and subsequent construction. This test does not
        execute or numerically verify that analyzer policy.
    """

    with pytest.raises(
        ValueError,
        match="maximum_absolute_residual must not exceed spectral_residual",
    ):
        comparison_result(
            maximum_absolute_residual=maximum,
            spectral_residual=spectral,
            frobenius_residual=frobenius,
        )


@pytest.mark.parametrize(
    ("field_name", "field_label", "value", "value_label"),
    [
        pytest.param(field_name, field_label, value, value_label)
        for field_name, field_label in _METRIC_FIELDS
        for value, value_label in (
            (10**10000, "huge-positive"),
            (-(10**10000), "huge-negative"),
        )
    ],
    ids=[
        f"SV-ORCR-011-{field_label}-{value_label}"
        for _, field_label in _METRIC_FIELDS
        for value_label in ("huge-positive", "huge-negative")
    ],
)
def test_translate_huge_integer_metric_conversion(
    field_name: str, field_label: str, value: int, value_label: str
) -> None:
    """SV-ORCR-011: translate huge-integer conversion overflow consistently.

    Requirement
        Accepted Python-integer scalar conversion that overflows binary64 maps to
        the field-specific finite-real ``ValueError`` taxonomy.
    Method and acceptance
        Supply huge positive and negative integers to every metric field and
        require ``<field> must be finite``.
    Interpretation and limitations
        Passing verifies exception translation only; ``field_label`` and
        ``value_label`` provide stable readable collection IDs and do not affect
        construction.
    """

    with pytest.raises(ValueError, match=f"{field_name} must be finite"):
        comparison_result(**{field_name: value})
