r"""Software verification of ``OperatorRecordComparisonResult``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the invariants facet. System under test and evidence
class
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

from dataclasses import dataclass
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import OperatorRecordComparisonResult

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordComparisonResult


def comparison_result(**overrides: object) -> OperatorRecordComparisonResult:
    r"""Evidence ID: Owns no identifier; supports evidence in this module.

    Requirement: Comparison-result cases require a valid baseline whose public fields
    can be
    overridden one partition at a time.

    Method: Construct or inspect only the named synthetic fixture operation (comparison
    result);
    the helper owns no assertion result and introduces no hidden oracle.

    Oracle: Literal constructor values, the declared public-field inventory where
    completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.

    Acceptance: The helper returns exactly the requested fixture value or applies only
    the
    documented comparison; all pass/fail assertions remain in the owning test.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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
            id="reference_empty",
        ),
        pytest.param(
            "reference_identifier",
            1,
            TypeError,
            "reference identifier must be a string",
            id="reference_python_int",
        ),
        pytest.param(
            "reference_identifier",
            object(),
            TypeError,
            "reference identifier must be a string",
            id="reference_object",
        ),
        pytest.param(
            "candidate_identifier",
            "",
            ValueError,
            "candidate identifier must not be empty",
            id="candidate_empty",
        ),
        pytest.param(
            "candidate_identifier",
            1,
            TypeError,
            "candidate identifier must be a string",
            id="candidate_python_int",
        ),
        pytest.param(
            "candidate_identifier",
            object(),
            TypeError,
            "candidate identifier must be a string",
            id="candidate_object",
        ),
    ],
)
def test_constructor__enforce_identifier_invariants__is_enforced(
    field_name: str,
    bad_value: object,
    expected_error: type[Exception],
    expected_message: str,
) -> None:
    r"""Evidence ID: SV-ORCR-005

    Requirement: Reference and candidate identifiers are independently nonempty strings.
    method and
    acceptance Supply one invalid role per collected case and require the exact
    ``TypeError``/``ValueError`` class and field-specific diagnostic. interpretation and
    limitations Passing verifies identifier state only; no trimming or string-subclass
    policy beyond the documented constructor behavior is asserted.

    Method: Exercise the named public surface with the synthetic inputs and semantic
    partition
    encoded unchanged in the test body; warnings are not accepted unless explicitly
    controlled.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: A pass supports only this requirement; a failure may identify an
    implementation,
    fixture, oracle, environment, or accepted-contract defect and requires diagnosis
    rather than weakened expectations.

    Limitations: This synthetic software evidence does not establish numerical
    verification, physical
    correctness, scientific validation, UQ, portability, or cross-language agreement.
    """

    with pytest.raises(expected_error, match=expected_message):
        comparison_result(**{field_name: bad_value})


@pytest.mark.parametrize(
    ("bad_value", "expected_error", "expected_message"),
    [
        pytest.param("", ValueError, "energy unit must not be empty", id="empty"),
        pytest.param(
            1, TypeError, "energy unit must be a string", id="sv_orcr_006_python_int"
        ),
        pytest.param(
            object(), TypeError, "energy unit must be a string", id="sv_orcr_006_object"
        ),
    ],
)
def test_constructor__enforce_energy_unit_invariants__is_enforced(
    bad_value: object,
    expected_error: type[Exception],
    expected_message: str,
) -> None:
    r"""Evidence ID: SV-ORCR-006

    Requirement: OperatorRecordComparisonResult enforces this structural-result
    partition: enforce
    energy unit invariants: is enforced.

    Method: Construct valid baseline instances, change only the named enforce energy
    unit
    invariants: is enforced partition, and observe constructor, field, equality, hash,
    or public-API behavior as applicable.

    Oracle: Literal constructor values, the declared public-field inventory where
    completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.

    Acceptance: The named partition raises exactly expected_error with the asserted
    public message,
    code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    with pytest.raises(expected_error, match=expected_message):
        comparison_result(energy_unit=bad_value)


@pytest.mark.parametrize(
    ("bad_value", "expected_error", "expected_message"),
    [
        pytest.param(0, ValueError, "matrix_dimension must be positive", id="zero"),
        pytest.param(
            -1,
            ValueError,
            "matrix_dimension must be positive",
            id="negative_python_int",
        ),
        pytest.param(
            np.int64(-1),
            ValueError,
            "matrix_dimension must be positive",
            id="negative_numpy_int",
        ),
        pytest.param(
            True,
            TypeError,
            "matrix_dimension must be a positive integer",
            id="sv_orcr_007_python_bool",
        ),
        pytest.param(
            np.bool_(True),
            TypeError,
            "matrix_dimension must be a positive integer",
            id="sv_orcr_007_numpy_bool",
        ),
        pytest.param(
            2.0,
            TypeError,
            "matrix_dimension must be a positive integer",
            id="sv_orcr_007_python_float",
        ),
        pytest.param(
            "2",
            TypeError,
            "matrix_dimension must be a positive integer",
            id="sv_orcr_007_numeric_string",
        ),
        pytest.param(
            object(),
            TypeError,
            "matrix_dimension must be a positive integer",
            id="sv_orcr_007_object",
        ),
    ],
)
def test_constructor__enforce_matrix_dimension_invariants__is_enforced(
    bad_value: object,
    expected_error: type[Exception],
    expected_message: str,
) -> None:
    r"""Evidence ID: SV-ORCR-007

    Requirement: Python and NumPy integer scalars are admitted, then required to be
    positive;
    Boolean, floating, string, and arbitrary-object inputs are not integer semantics.
    method and acceptance Collect each invalid category independently and require exact
    exception taxonomy with a dimension-specific diagnostic. interpretation and
    limitations Positive NumPy canonicalization is covered by ``the owning evidence``.
    No upper dimension policy or allocation feasibility is tested here.

    Method: Exercise the named public surface with the synthetic inputs and semantic
    partition
    encoded unchanged in the test body; warnings are not accepted unless explicitly
    controlled.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: A pass supports only this requirement; a failure may identify an
    implementation,
    fixture, oracle, environment, or accepted-contract defect and requires diagnosis
    rather than weakened expectations.

    Limitations: This synthetic software evidence does not establish numerical
    verification, physical
    correctness, scientific validation, UQ, portability, or cross-language agreement.
    """

    with pytest.raises(expected_error, match=expected_message):
        comparison_result(matrix_dimension=bad_value)


@dataclass(frozen=True, slots=True)
class ResidualInvariantCase:
    r"""One invalid residual-scalar admission case.

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
RESIDUAL_INVARIANT_CASES = (
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            -1.0,
            "negative",
            ValueError,
            "maximum_absolute_residual must be non-negative",
        ),
        id="maximum_negative",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            np.nan,
            "nan",
            ValueError,
            "maximum_absolute_residual must be finite",
        ),
        id="maximum_nan",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            np.inf,
            "positive_infinity",
            ValueError,
            "maximum_absolute_residual must be finite",
        ),
        id="maximum_positive_infinity",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            -np.inf,
            "negative_infinity",
            ValueError,
            "maximum_absolute_residual must be finite",
        ),
        id="maximum_negative_infinity",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            True,
            "python_bool",
            TypeError,
            "maximum_absolute_residual must be a real number",
        ),
        id="maximum_python_bool",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            np.bool_(True),
            "numpy_bool",
            TypeError,
            "maximum_absolute_residual must be a real number",
        ),
        id="maximum_numpy_bool",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            "1.0",
            "numeric_string",
            TypeError,
            "maximum_absolute_residual must be a real number",
        ),
        id="maximum_numeric_string",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            b"1.0",
            "bytes",
            TypeError,
            "maximum_absolute_residual must be a real number",
        ),
        id="maximum_bytes",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            1.0 + 0.0j,
            "python_complex",
            TypeError,
            "maximum_absolute_residual must be a real number",
        ),
        id="maximum_python_complex",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            np.complex128(1.0 + 0.0j),
            "numpy_complex",
            TypeError,
            "maximum_absolute_residual must be a real number",
        ),
        id="maximum_numpy_complex",
    ),
    pytest.param(
        ResidualInvariantCase(
            "maximum_absolute_residual",
            "maximum",
            object(),
            "object",
            TypeError,
            "maximum_absolute_residual must be a real number",
        ),
        id="maximum_object",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            -1.0,
            "negative",
            ValueError,
            "frobenius_residual must be non-negative",
        ),
        id="frobenius_negative",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            np.nan,
            "nan",
            ValueError,
            "frobenius_residual must be finite",
        ),
        id="frobenius_nan",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            np.inf,
            "positive_infinity",
            ValueError,
            "frobenius_residual must be finite",
        ),
        id="frobenius_positive_infinity",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            -np.inf,
            "negative_infinity",
            ValueError,
            "frobenius_residual must be finite",
        ),
        id="frobenius_negative_infinity",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            True,
            "python_bool",
            TypeError,
            "frobenius_residual must be a real number",
        ),
        id="frobenius_python_bool",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            np.bool_(True),
            "numpy_bool",
            TypeError,
            "frobenius_residual must be a real number",
        ),
        id="frobenius_numpy_bool",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            "1.0",
            "numeric_string",
            TypeError,
            "frobenius_residual must be a real number",
        ),
        id="frobenius_numeric_string",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            b"1.0",
            "bytes",
            TypeError,
            "frobenius_residual must be a real number",
        ),
        id="frobenius_bytes",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            1.0 + 0.0j,
            "python_complex",
            TypeError,
            "frobenius_residual must be a real number",
        ),
        id="frobenius_python_complex",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            np.complex128(1.0 + 0.0j),
            "numpy_complex",
            TypeError,
            "frobenius_residual must be a real number",
        ),
        id="frobenius_numpy_complex",
    ),
    pytest.param(
        ResidualInvariantCase(
            "frobenius_residual",
            "frobenius",
            object(),
            "object",
            TypeError,
            "frobenius_residual must be a real number",
        ),
        id="frobenius_object",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            -1.0,
            "negative",
            ValueError,
            "spectral_residual must be non-negative",
        ),
        id="spectral_negative",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            np.nan,
            "nan",
            ValueError,
            "spectral_residual must be finite",
        ),
        id="spectral_nan",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            np.inf,
            "positive_infinity",
            ValueError,
            "spectral_residual must be finite",
        ),
        id="spectral_positive_infinity",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            -np.inf,
            "negative_infinity",
            ValueError,
            "spectral_residual must be finite",
        ),
        id="spectral_negative_infinity",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            True,
            "python_bool",
            TypeError,
            "spectral_residual must be a real number",
        ),
        id="spectral_python_bool",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            np.bool_(True),
            "numpy_bool",
            TypeError,
            "spectral_residual must be a real number",
        ),
        id="spectral_numpy_bool",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            "1.0",
            "numeric_string",
            TypeError,
            "spectral_residual must be a real number",
        ),
        id="spectral_numeric_string",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            b"1.0",
            "bytes",
            TypeError,
            "spectral_residual must be a real number",
        ),
        id="spectral_bytes",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            1.0 + 0.0j,
            "python_complex",
            TypeError,
            "spectral_residual must be a real number",
        ),
        id="spectral_python_complex",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            np.complex128(1.0 + 0.0j),
            "numpy_complex",
            TypeError,
            "spectral_residual must be a real number",
        ),
        id="spectral_numpy_complex",
    ),
    pytest.param(
        ResidualInvariantCase(
            "spectral_residual",
            "spectral",
            object(),
            "object",
            TypeError,
            "spectral_residual must be a real number",
        ),
        id="spectral_object",
    ),
)


@pytest.mark.parametrize(
    "case",
    RESIDUAL_INVARIANT_CASES,
)
def test_constructor__enforce_residual_scalar_invariants__is_enforced(
    case: ResidualInvariantCase,
) -> None:
    r"""Evidence ID: SV-ORCR-008

    Requirement: OperatorRecordComparisonResult enforces this structural-result
    partition: enforce
    residual scalar invariants: is enforced.

    Method: Construct valid baseline instances, change only the named enforce residual
    scalar
    invariants: is enforced partition, and observe constructor, field, equality, hash,
    or public-API behavior as applicable.

    Oracle: Literal constructor values, the declared public-field inventory where
    completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.

    Acceptance: The named partition raises exactly case.expected_error with the asserted
    public
    message, code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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
            id="maximum_exceeds_spectral",
        ),
        pytest.param(
            1.0,
            3.0,
            2.0,
            "spectral_residual must not exceed frobenius_residual",
            id="sv_orcr_009_spectral_exceeds_frobenius",
        ),
    ],
)
def test_constructor__enforce_mathematical_metric_ordering__is_enforced(
    maximum: float,
    spectral: float,
    frobenius: float,
    expected_message: str,
) -> None:
    r"""Evidence ID: SV-ORCR-009

    Requirement: OperatorRecordComparisonResult enforces this structural-result
    partition: enforce
    mathematical metric ordering: is enforced.

    Method: Construct valid baseline instances, change only the named enforce
    mathematical
    metric ordering: is enforced partition, and observe constructor, field, equality,
    hash, or public-API behavior as applicable.

    Oracle: Literal constructor values, the declared public-field inventory where
    completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.

    Acceptance: The named partition raises exactly ValueError with the asserted public
    message,
    code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
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
            id="sv_orcr_010_known_binary64_regression_a",
        ),
        pytest.param(
            2.23606797749979e100,
            2.2360679774997897e100,
            2.23606797749979e100,
            id="sv_orcr_010_known_binary64_regression_b",
        ),
    ],
)
def test_constructor__reject_uncanonicalized_roundoff_order__is_enforced(
    maximum: float, spectral: float, frobenius: float
) -> None:
    r"""Evidence ID: SV-ORCR-010

    Requirement: The ResultObject strictly rejects supplied ``maximum > spectral`` even
    when the
    inversion resembles binary64 roundoff. method and acceptance Supply two known raw
    regression triples and require the exact ordering ``ValueError``. interpretation and
    limitations The analyzer owns raw computation, allowance evaluation, permitted
    upward canonicalization, and subsequent construction. This test does not execute or
    numerically verify that analyzer policy.

    Method: Exercise the named public surface with the synthetic inputs and semantic
    partition
    encoded unchanged in the test body; warnings are not accepted unless explicitly
    controlled.

    Oracle: The accepted public contract, fixed literal expectations, public artifacts,
    and
    Python language semantics determine the result independently of production private
    helpers.

    Acceptance: Every existing assertion, exact value, exception taxonomy, ordering
    rule, fixture
    identity, and explicit tolerance or ULP criterion passes unchanged.

    Interpretation: A pass supports only this requirement; a failure may identify an
    implementation,
    fixture, oracle, environment, or accepted-contract defect and requires diagnosis
    rather than weakened expectations.

    Limitations: This synthetic software evidence does not establish numerical
    verification, physical
    correctness, scientific validation, UQ, portability, or cross-language agreement.
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
        pytest.param(
            "maximum_absolute_residual",
            "maximum",
            10**10000,
            "huge_positive",
            id="maximum_huge_positive",
        ),
        pytest.param(
            "maximum_absolute_residual",
            "maximum",
            -(10**10000),
            "huge_negative",
            id="maximum_huge_negative",
        ),
        pytest.param(
            "frobenius_residual",
            "frobenius",
            10**10000,
            "huge_positive",
            id="frobenius_huge_positive",
        ),
        pytest.param(
            "frobenius_residual",
            "frobenius",
            -(10**10000),
            "huge_negative",
            id="frobenius_huge_negative",
        ),
        pytest.param(
            "spectral_residual",
            "spectral",
            10**10000,
            "huge_positive",
            id="spectral_huge_positive",
        ),
        pytest.param(
            "spectral_residual",
            "spectral",
            -(10**10000),
            "huge_negative",
            id="spectral_huge_negative",
        ),
    ],
)
def test_constructor__input_boundary__translate_huge_integer_metric_conversion(
    field_name: str, field_label: str, value: int, value_label: str
) -> None:
    r"""Evidence ID: SV-ORCR-011

    Requirement: OperatorRecordComparisonResult enforces this structural-result
    partition: input
    boundary: translate huge integer metric conversion.

    Method: Construct valid baseline instances, change only the named input boundary:
    translate
    huge integer metric conversion partition, and observe constructor, field, equality,
    hash, or public-API behavior as applicable.

    Oracle: Literal constructor values, the declared public-field inventory where
    completeness
    is claimed, frozen dataclass semantics, and Python equality/hash rules determine the
    result independently.

    Acceptance: The named partition raises exactly ValueError with the asserted public
    message,
    code, or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """

    with pytest.raises(ValueError, match=f"{field_name} must be finite"):
        comparison_result(**{field_name: value})
