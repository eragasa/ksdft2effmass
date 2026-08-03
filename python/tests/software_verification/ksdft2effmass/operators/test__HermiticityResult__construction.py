r"""Software verification of ``HermiticityResult`` construction.

Facet and contract
------------------
This module owns public construction, stored-field mapping, accepted scalar-
family canonicalization, the derived ``is_hermitian`` boundary, exclusion of the
derived property from constructor state, and serialization exclusion.
``HermiticityResult`` stores residual :math:`\varepsilon_{\mathrm H}`, tolerance
:math:`\tau`, and their common ``energy_unit``. The predicate is exactly
``residual <= tolerance`` over the stored binary64 values.

Ownership and scope
-------------------
The ResultObject stores no matrix, ``OperatorRecord``, physical provenance, unit
conversion, or Analyzer policy beyond the recorded tolerance. It does not
compute

.. math::

   \varepsilon_{\mathrm H}=\max_{i,j}|H_{ij}-H_{ji}^{*}|.

These direct tests invoke no ``HermiticityAnalyzer``. The approved architecture
and Sphinx contracts are the oracle. Passing establishes construction,
canonical stored state, and the software predicate only. Failure may indicate a
ResultObject regression, contract/documentation mismatch, or evidence defect.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-HR-001`` through
``SV-HR-005``. It does not establish Analyzer residual accuracy, scientific
appropriateness of :math:`\tau`, physical Hermiticity, DFT or Wannier validity,
scientific validation, uncertainty quantification, or Rust conformance. No
``HermiticityResult`` wire format is approved.
"""

from typing import Any, assert_type, cast

import numpy as np
import pytest

from ksdft2effmass.operators import HermiticityResult

pytestmark = pytest.mark.software_verification


def make_result(
    *,
    residual: float = 0.0,
    tolerance: float = 1.0e-12,
    energy_unit: str = "eV",
) -> HermiticityResult:
    """Construct a valid synthetic ResultObject for ``SV-HR-003`` to ``005``.

    Evidence ID
        Supporting helper for ``SV-HR-003`` through ``SV-HR-005``; it owns no
        separate evidence identifier.
    Requirement
        Ordinary fixtures use only values already intended to satisfy public
        semantic types rather than disguising invalid construction behind
        ``Any``.
    Method
        Pass typed residual, tolerance, and energy-unit values unchanged to the
        public constructor.
    Oracle
        The approved ResultObject contract defines these three constructor
        fields and performs any documented scalar canonicalization itself.
    Acceptance
        The constructor returns a public synthetic ``HermiticityResult``.
    Interpretation
        The helper provides concise valid fixtures without performing analysis
        or coercion outside the object.
    Limitations
        It performs no matrix analysis or unit conversion and establishes no
        numerical accuracy, physical Hermiticity, scientific validity,
        scientific validation, uncertainty quantification, or Rust conformance.
    """

    return HermiticityResult(
        residual=residual,
        tolerance=tolerance,
        energy_unit=energy_unit,
    )


def test_public_construction_and_stored_field_mapping() -> None:
    """SV-HR-001: verify distinct inputs map to canonical public fields.

    Evidence ID
        ``SV-HR-001``.
    Requirement
        The ResultObject stores residual, tolerance, and common energy unit in
        their declared roles and canonical built-in boundary types.
    Method
        Construct directly with distinct synthetic values and inspect the three
        public fields without invoking the Analyzer.
    Oracle
        The approved ResultObject and Sphinx contracts define the field mapping
        and built-in scalar storage.
    Acceptance
        Values equal their inputs and have exact types ``float``, ``float``, and
        ``str`` respectively.
    Interpretation
        Passing establishes public construction and stored-field mapping.
    Limitations
        No residual computation, tolerance suitability, physical Hermiticity,
        scientific validation, uncertainty quantification, or Rust conformance
        is established.
    """

    result = HermiticityResult(
        residual=2.0e-13,
        tolerance=1.0e-12,
        energy_unit="eV",
    )

    assert result.residual == 2.0e-13
    assert result.tolerance == 1.0e-12
    assert result.energy_unit == "eV"
    assert type(result.residual) is float
    assert type(result.tolerance) is float
    assert type(result.energy_unit) is str
    assert_type(result.residual, float)
    assert_type(result.tolerance, float)
    assert_type(result.energy_unit, str)


@pytest.mark.parametrize(
    "scalar",
    [
        pytest.param(0, id="SV-HR-002-python-integer"),
        pytest.param(1.0, id="SV-HR-002-python-float"),
        pytest.param(np.int64(0), id="SV-HR-002-numpy-integer"),
        pytest.param(np.float64(1.0e-12), id="SV-HR-002-numpy-floating"),
    ],
)
def test_accepted_scalar_families_canonicalize_in_both_positions(
    scalar: int | float | np.integer | np.floating,
) -> None:
    """SV-HR-002: canonicalize each approved scalar family to ``float``.

    Evidence ID
        ``SV-HR-002``; stable parameter IDs name the four supported scalar
        families without assigning additional evidence identifiers.
    Requirement
        Representative Python integer, Python float, NumPy integer scalar, and
        NumPy floating scalar inputs are accepted independently as residual and
        tolerance and stored as built-in floats.
    Method
        Construct one result with the scalar in the residual position and a
        second with it in the tolerance position.
    Oracle
        The approved public scalar contract admits exactly these representative
        families and canonicalizes them at the ResultObject boundary.
    Acceptance
        Both independently exercised positions store exact built-in ``float``
        values for every family.
    Interpretation
        Passing establishes documented family admission and canonical storage in
        both fields.
    Limitations
        This does not claim arbitrary numeric-protocol, Decimal, Fraction, array,
        complex, or every NumPy-width admission. It establishes no numerical
        verification, scientific validation, UQ, or Rust conformance.
    """

    residual_result = HermiticityResult(
        residual=scalar,
        tolerance=1.0,
        energy_unit="eV",
    )
    tolerance_result = HermiticityResult(
        residual=0.0,
        tolerance=scalar,
        energy_unit="eV",
    )

    assert residual_result.residual == float(scalar)
    assert type(residual_result.residual) is float
    assert type(residual_result.tolerance) is float
    assert tolerance_result.tolerance == float(scalar)
    assert type(tolerance_result.residual) is float
    assert type(tolerance_result.tolerance) is float


@pytest.mark.parametrize(
    ("residual", "tolerance", "expected"),
    [
        pytest.param(5.0e-13, 1.0e-12, True, id="SV-HR-003-below-tolerance"),
        pytest.param(0.0, 0.0, True, id="SV-HR-003-equal-tolerance"),
        pytest.param(2.0e-12, 1.0e-12, False, id="SV-HR-003-above-tolerance"),
    ],
)
def test_derived_hermiticity_predicate_has_inclusive_boundary(
    residual: float,
    tolerance: float,
    expected: bool,
) -> None:
    """SV-HR-003: verify the exact inclusive stored-scalar predicate.

    Evidence ID
        ``SV-HR-003``; parameter IDs distinguish below, equal including exact
        zero, and above-tolerance states.
    Requirement
        ``is_hermitian`` is true exactly when
        :math:`\\varepsilon_{\\mathrm H}\\leq\\tau`; equality, including zero equals
        zero, is accepted.
    Method
        Construct synthetic results on each side of the boundary and inspect the
        derived Boolean without approximate comparison.
    Oracle
        The approved mathematical and Sphinx contracts define direct binary64
        comparison with an inclusive boundary.
    Acceptance
        Each predicate is the exact expected Boolean singleton.
    Interpretation
        Passing establishes the software predicate derived from stored values.
    Limitations
        It does not establish that the residual was computed correctly or that
        the selected tolerance is scientifically appropriate; physical
        Hermiticity, scientific validation, UQ, and Rust conformance are absent.
    """

    result = make_result(residual=residual, tolerance=tolerance)

    assert result.is_hermitian is expected


def test_derived_field_cannot_be_supplied_as_constructor_state() -> None:
    """SV-HR-004: reject derived-field overrides in both argument forms.

    Evidence ID
        ``SV-HR-004``.
    Requirement
        ``is_hermitian`` is derived rather than stored and cannot be supplied as
        keyword or extra positional constructor state; changing stored scalars
        changes the predicate naturally.
    Method
        Invoke an ``Any``-typed constructor only at deliberate invalid-signature
        boundaries, then compare valid accepted and rejected scalar states.
    Oracle
        The approved three-field constructor and derived-property contract admit
        no fourth state field.
    Acceptance
        Both override attempts raise exactly ``TypeError``; valid scalar states
        independently produce true and false predicates.
    Interpretation
        Passing prevents contradictory stored and derived acceptance states.
    Limitations
        Signature-generated error wording is not frozen. Analyzer behavior,
        tolerance suitability, numerical verification, scientific validation,
        UQ, and Rust conformance are untested.
    """

    invalid_constructor = cast(Any, HermiticityResult)

    with pytest.raises(TypeError):
        invalid_constructor(
            residual=0.0,
            tolerance=1.0e-12,
            energy_unit="eV",
            is_hermitian=False,
        )
    with pytest.raises(TypeError):
        invalid_constructor(0.0, 1.0e-12, "eV", False)

    assert make_result(residual=0.0, tolerance=0.0).is_hermitian is True
    assert make_result(residual=1.0, tolerance=0.0).is_hermitian is False


def test_result_has_no_independent_serialization_api() -> None:
    """SV-HR-005: verify ResultObject serialization exclusion.

    Evidence ID
        ``SV-HR-005``.
    Requirement
        Neither instance nor class exposes the six unapproved JSON, dictionary,
        serializer, or deserializer method names.
    Method
        Inspect a valid instance and the public class for each excluded name.
    Oracle
        The approved wire-format contract assigns ``OperatorRecordJsonSerializer``
        only to ``OperatorRecord`` and approves no ``HermiticityResult`` schema.
    Acceptance
        Every excluded method is absent from both instance and class.
    Interpretation
        Passing establishes absence of an independent ResultObject wire API.
    Limitations
        Exception and Result serialization remain outside this contract;
        pickling and future schemas are unspecified. No numerical verification,
        scientific validation, UQ, or Rust conformance is established.
    """

    result = make_result()

    for method_name in (
        "to_json",
        "to_dict",
        "serialize",
        "from_json",
        "from_dict",
        "deserialize",
    ):
        assert not hasattr(result, method_name)
        assert not hasattr(HermiticityResult, method_name)
