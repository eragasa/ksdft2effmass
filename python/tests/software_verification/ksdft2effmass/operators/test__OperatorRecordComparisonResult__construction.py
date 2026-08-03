"""Construction evidence for ``OperatorRecordComparisonResult``.

System under test and evidence class
------------------------------------
The system under test is the immutable structural comparison ResultObject. This
module provides software-verification evidence ``SV-ORCR-001`` through
``SV-ORCR-004`` for valid construction, documented scalar canonicalization,
positive structural dimensions, and the deliberate absence of ResultObject-owned
serialization APIs.

Requirements, strategy, and acceptance
--------------------------------------
Tests construct the public object directly and inspect public fields and built-in
Python scalar types. Valid metrics must satisfy
``0 <= maximum_absolute_residual <= spectral_residual <= frobenius_residual``.
The ResultObject validates and stores already-computed state; it does not execute
residual norms, allocate a represented matrix, repair roundoff, or impose
producer-owned numerical dimension policy.

Ownership, interpretation, and limitations
------------------------------------------
Residual computation and permitted roundoff canonicalization belong to
``OperatorRecordResidualAnalyzer``. Serialization requires a separately approved
serializer ActionObject and wire-format specification. Passing establishes the
documented construction boundary only. Failure may indicate a ResultObject
implementation regression, contract/documentation mismatch, or evidence defect
requiring investigation; it does not by itself establish analyzer numerical
failure, physical-model error, scientific invalidity, or quantified uncertainty.
Numerical verification is not applicable to direct ResultObject construction. A
valid result does not establish physical Hamiltonian equivalence or scientific
residual acceptability. Scientific validation and uncertainty quantification
have not been performed.
"""

from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import OperatorRecordComparisonResult

pytestmark = pytest.mark.software_verification


def test_construct_valid_comparison_result() -> None:
    r"""SV-ORCR-001: construct and expose every valid public field.

    Requirement
        Construction accepts a complete valid state satisfying
        :math:`0\leq\varepsilon_{\max}\leq\varepsilon_2\leq\varepsilon_{\mathrm F}`.
    Method and acceptance
        Construct with keyword arguments and require exact equality for every
        public field.
    Interpretation and limitations
        Passing verifies stored state, not calculation of the metric values or
        physical equivalence of represented operators.
    """

    result = OperatorRecordComparisonResult(
        reference_identifier="reference",
        candidate_identifier="candidate",
        matrix_dimension=2,
        energy_unit="eV",
        maximum_absolute_residual=1.0,
        frobenius_residual=4.0,
        spectral_residual=3.0,
    )

    assert result.reference_identifier == "reference"
    assert result.candidate_identifier == "candidate"
    assert result.matrix_dimension == 2
    assert result.energy_unit == "eV"
    assert result.maximum_absolute_residual == 1.0
    assert result.frobenius_residual == 4.0
    assert result.spectral_residual == 3.0


@pytest.mark.parametrize(
    ("matrix_dimension", "maximum", "spectral", "frobenius"),
    [
        pytest.param(
            2,
            1,
            3,
            4,
            id="SV-ORCR-002-python-integer-metrics",
        ),
        pytest.param(
            np.int64(2),
            np.int64(1),
            np.int64(3),
            np.int64(4),
            id="SV-ORCR-002-numpy-integer-dimension-and-metrics",
        ),
        pytest.param(
            2,
            1.0,
            3.0,
            4.0,
            id="SV-ORCR-002-python-floating-metrics",
        ),
        pytest.param(
            np.int32(2),
            np.float32(1.0),
            np.float64(3.0),
            np.float32(4.0),
            id="SV-ORCR-002-numpy-floating-metrics",
        ),
    ],
)
def test_canonicalize_documented_numeric_scalars(
    matrix_dimension: object,
    maximum: object,
    spectral: object,
    frobenius: object,
) -> None:
    """SV-ORCR-002: canonicalize accepted integer and floating scalars.

    Requirement
        Documented Python and NumPy integer dimensions become built-in ``int``;
        documented Python and NumPy integer or floating metrics become built-in
        ``float``.
    Method and acceptance
        Collect representative admitted families, preserve valid metric order,
        and require exact values and exact built-in stored types for every field.
    Interpretation and limitations
        Passing covers only the represented Python/NumPy integer and floating
        families and widths; it does not claim Boolean or complex admission.
    """

    result = OperatorRecordComparisonResult(
        reference_identifier="reference",
        candidate_identifier="candidate",
        matrix_dimension=cast(Any, matrix_dimension),
        energy_unit="eV",
        maximum_absolute_residual=cast(Any, maximum),
        frobenius_residual=cast(Any, frobenius),
        spectral_residual=cast(Any, spectral),
    )

    assert result.matrix_dimension == 2
    assert type(result.matrix_dimension) is int
    assert result.maximum_absolute_residual == 1.0
    assert type(result.maximum_absolute_residual) is float
    assert result.frobenius_residual == 4.0
    assert type(result.frobenius_residual) is float
    assert result.spectral_residual == 3.0
    assert type(result.spectral_residual) is float


def test_accept_documented_large_positive_structural_dimension() -> None:
    """SV-ORCR-003: accept positive structural Python-integer dimensions.

    Requirement
        The documented ResultObject contract accepts any positive Python integer
        and imposes no analyzer/comparator maximum-dimension policy.
    Method and acceptance
        Store a very large positive integer exactly without allocating a matrix.
    Interpretation and limitations
        This is structural Python metadata. It does not claim that the
        corresponding matrix fits available memory, define a serialized Rust
        boundary, or move numerical dimension policy from the producing
        ActionObject into the ResultObject.
    """

    matrix_dimension = 10**10000

    result = OperatorRecordComparisonResult(
        "reference", "candidate", matrix_dimension, "eV", 1.0, 4.0, 3.0
    )

    assert result.matrix_dimension == matrix_dimension
    assert type(result.matrix_dimension) is int


def test_exclude_unapproved_result_serialization_apis() -> None:
    """SV-ORCR-004: exclude ResultObject-owned serialization APIs.

    Requirement
        No ``to_json``, ``from_json``, ``to_dict``, ``from_dict``, ``serialize``,
        or ``deserialize`` contract exists for this ResultObject.
    Method and acceptance
        Require all six names to be absent from both the public instance and
        class as applicable.
    Interpretation and limitations
        Passing preserves the serializer ActionObject ownership boundary. A
        future wire format requires separate human approval and specification.
    """

    result = OperatorRecordComparisonResult(
        "reference", "candidate", 2, "eV", 1.0, 4.0, 3.0
    )

    for name in (
        "to_json",
        "from_json",
        "to_dict",
        "from_dict",
        "serialize",
        "deserialize",
    ):
        assert not hasattr(result, name)
        assert not hasattr(OperatorRecordComparisonResult, name)
