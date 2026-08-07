r"""Software verification of ``HermiticityResult``.

Facet and represented meaning
-----------------------------
This class-owned module owns the invariants facet. Facet and contract
------------------
This module owns direct constructor rejection for residual
:math:`\varepsilon_{\mathrm H}`, tolerance :math:`\tau`, and their common
``energy_unit``. Residual and tolerance admit documented Python and NumPy real
scalar families, canonicalize to finite non-negative binary64 values, and reject
wrong semantic types with ``TypeError``. Correctly typed nonfinite or negative
values raise ``ValueError``. The energy unit must be a nonempty Python string.

Ownership and scope
-------------------
These are ResultObject state invariants. No matrix, ``OperatorRecord``, Analyzer,
unit conversion, registry, normalization, or physical provenance is involved.
The approved architecture and Sphinx contracts are the oracle. Passing
establishes strict constructor taxonomy; failure may indicate a ResultObject
regression, contract/documentation mismatch, or evidence defect.

VVUQ boundaries
---------------
This module provides software-verification evidence ``SV-HR-006`` through
``SV-HR-013``. It does not verify Analyzer residual accuracy, tolerance policy,
physical Hermiticity, DFT or Wannier validity, scientific validation,
uncertainty quantification, or Rust conformance.

Intrinsic and cross-object scope
--------------------------------
The primary owner is ``HermiticityResult``; collaborators only construct inputs or
expose public outcomes. Accepted public contracts, literal expected values, Python
language semantics, and assigned schema or fixture artifacts provide the oracles. No
runtime warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions
------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import warnings
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import HermiticityResult

pytestmark = pytest.mark.software_verification

SUT = HermiticityResult


@pytest.mark.parametrize(
    "invalid_residual",
    [
        pytest.param(True, id="sv_hr_006_boolean_true"),
        pytest.param(False, id="sv_hr_006_boolean_false"),
        pytest.param(np.bool_(True), id="sv_hr_006_numpy_boolean"),
        pytest.param(None, id="none"),
        pytest.param("0.0", id="sv_hr_006_raw_string"),
        pytest.param(b"0.0", id="bytes"),
        pytest.param(0.0 + 0.0j, id="complex"),
        pytest.param(np.complex128(0.0 + 0.0j), id="complex"),
        pytest.param(object(), id="sv_hr_006_arbitrary_object"),
    ],
)
def test_constructor__residual_wrong_types_are_rejected__is_enforced(
    invalid_residual: object,
) -> None:
    r"""Evidence ID
    SV-HR-006
    Requirement
    Booleans, ``None``, numeric strings, bytes, complex values, and arbitrary objects
    are not residual real numbers and are not coerced.
    Method
    Call the public constructor directly, using ``Any`` and ``cast`` only at this
    deliberate invalid residual boundary.
    Oracle
    The approved ResultObject and Sphinx contracts require an admitted real scalar and
    the residual-specific diagnostic.
    Acceptance
    Every case raises exactly ``TypeError`` with residual-specific wording that
    identifies the real-number requirement.
    Interpretation
    Passing establishes residual semantic typing and Boolean/string/complex exclusion.
    Limitations
    Finiteness and sign have separate evidence. No Analyzer, numerical verification,
    scientific validation, UQ, or Rust conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        HermiticityResult(
            residual=cast(Any, invalid_residual),
            tolerance=1.0e-12,
            energy_unit="eV",
        )

    message = str(exc_info.value)
    assert "Hermiticity residual" in message
    assert "real number" in message


@pytest.mark.parametrize(
    "invalid_residual",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive_infinity"),
        pytest.param(float("-inf"), id="negative_infinity"),
        pytest.param(10**10000, id="positive_integer"),
        pytest.param(-(10**10000), id="negative_integer"),
    ],
)
def test_constructor__residual_must_be_finite__is_enforced(
    invalid_residual: float | int,
) -> None:
    r"""Evidence ID
    SV-HR-007
    Requirement
    Residual storage is finite binary64; accepted Python integer conversion overflow
    maps to ``ValueError`` rather than leaking ``OverflowError``.
    Method
    Construct directly under a local RuntimeWarning-as-error boundary with each
    correctly typed invalid value.
    Oracle
    The approved finite-scalar contract defines the residual-specific public
    ``ValueError`` diagnostic.
    Acceptance
    Every case raises exactly ``ValueError`` with residual-specific finite- number
    wording and emits no RuntimeWarning.
    Interpretation
    Passing establishes finite-number taxonomy including conversion overflow.
    Limitations
    This is constructor software verification, not extreme-scale residual numerical
    verification, scientific validation, UQ, or Rust conformance.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError) as exc_info:
            HermiticityResult(
                residual=invalid_residual,
                tolerance=1.0e-12,
                energy_unit="eV",
            )

    message = str(exc_info.value)
    assert "Hermiticity residual" in message
    assert "finite" in message


@pytest.mark.parametrize(
    "negative_residual",
    [
        pytest.param(-1.0, id="negative_unit_scale"),
        pytest.param(-1.0e-300, id="negative_small_scale"),
    ],
)
def test_constructor__residual_must_be_nonnegative__is_enforced(
    negative_residual: float,
) -> None:
    r"""Evidence ID
    SV-HR-008
    Requirement
    A residual is non-negative; finite negative values cannot be stored.
    Method
    Construct directly with two synthetic negative scales and valid other fields.
    Oracle
    The approved intrinsic invariant defines the residual-specific non-negativity
    diagnostic.
    Acceptance
    Every case raises exactly ``ValueError`` with residual-specific non-negativity
    wording.
    Interpretation
    Passing establishes sign enforcement; exact zero admission is owned by ``the owning
    evidence``.
    Limitations
    Multiple scales do not constitute numerical verification. Analyzer behavior,
    scientific validation, UQ, and Rust conformance are untested.
    """

    with pytest.raises(ValueError) as exc_info:
        HermiticityResult(
            residual=negative_residual,
            tolerance=1.0e-12,
            energy_unit="eV",
        )

    message = str(exc_info.value)
    assert "Hermiticity residual" in message
    assert "non-negative" in message


@pytest.mark.parametrize(
    "invalid_tolerance",
    [
        pytest.param(True, id="sv_hr_009_boolean_true"),
        pytest.param(False, id="sv_hr_009_boolean_false"),
        pytest.param(np.bool_(False), id="sv_hr_009_numpy_boolean"),
        pytest.param(None, id="none"),
        pytest.param("1e-12", id="sv_hr_009_raw_string"),
        pytest.param(b"1e-12", id="bytes"),
        pytest.param(0.0 + 0.0j, id="complex"),
        pytest.param(np.complex128(0.0 + 0.0j), id="complex"),
        pytest.param(object(), id="sv_hr_009_arbitrary_object"),
    ],
)
def test_constructor__tolerance_wrong_types_are_rejected__is_enforced(
    invalid_tolerance: object,
) -> None:
    r"""Evidence ID
    SV-HR-009
    Requirement
    Booleans, ``None``, numeric strings, bytes, complex values, and arbitrary objects
    are not tolerance real numbers and are not coerced.
    Method
    Call the public constructor directly, using ``Any`` and ``cast`` only at this
    deliberate invalid tolerance boundary.
    Oracle
    The approved ResultObject and Sphinx contracts require an admitted real scalar and
    the tolerance-specific diagnostic.
    Acceptance
    Every case raises exactly ``TypeError`` with tolerance-specific wording that
    identifies the real-number requirement.
    Interpretation
    Passing establishes the tolerance boundary independently of residual evidence.
    Limitations
    Finiteness and sign have separate evidence. No Analyzer, numerical verification,
    scientific validation, UQ, or Rust conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        HermiticityResult(
            residual=0.0,
            tolerance=cast(Any, invalid_tolerance),
            energy_unit="eV",
        )

    message = str(exc_info.value)
    assert "Hermiticity tolerance" in message
    assert "real number" in message


@pytest.mark.parametrize(
    "invalid_tolerance",
    [
        pytest.param(float("nan"), id="nan"),
        pytest.param(float("inf"), id="positive_infinity"),
        pytest.param(float("-inf"), id="negative_infinity"),
        pytest.param(10**10000, id="positive_integer"),
        pytest.param(-(10**10000), id="negative_integer"),
    ],
)
def test_constructor__tolerance_must_be_finite__is_enforced(
    invalid_tolerance: float | int,
) -> None:
    r"""Evidence ID
    SV-HR-010
    Requirement
    Tolerance storage is finite binary64; integer conversion overflow maps to
    ``ValueError`` rather than leaking ``OverflowError``.
    Method
    Construct directly under a RuntimeWarning-as-error boundary with each correctly
    typed invalid tolerance.
    Oracle
    The approved finite-scalar contract defines the tolerance-specific public
    ``ValueError`` diagnostic.
    Acceptance
    Every case raises exactly ``ValueError`` with tolerance-specific finite- number
    wording and emits no RuntimeWarning.
    Interpretation
    Passing establishes tolerance finite-number taxonomy independently.
    Limitations
    This does not verify tolerance suitability, Analyzer numerics, scientific
    validation, UQ, or Rust conformance.
    """

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        with pytest.raises(ValueError) as exc_info:
            HermiticityResult(
                residual=0.0,
                tolerance=invalid_tolerance,
                energy_unit="eV",
            )

    message = str(exc_info.value)
    assert "Hermiticity tolerance" in message
    assert "finite" in message


@pytest.mark.parametrize(
    "negative_tolerance",
    [
        pytest.param(-1.0, id="negative_unit_scale"),
        pytest.param(-1.0e-300, id="negative_small_scale"),
    ],
)
def test_constructor__tolerance_must_be_nonnegative__is_enforced(
    negative_tolerance: float,
) -> None:
    r"""Evidence ID
    SV-HR-011
    Requirement
    No negative-tolerance convention is supported; values are not converted to absolute
    magnitude.
    Method
    Construct directly with two finite negative tolerances and valid other fields.
    Oracle
    The approved intrinsic invariant defines the tolerance-specific non-negativity
    diagnostic.
    Acceptance
    Every case raises exactly ``ValueError`` with tolerance-specific non-negativity
    wording.
    Interpretation
    Passing establishes exact sign enforcement for stored tolerance policy.
    Limitations
    This does not assess scientific appropriateness of any non-negative tolerance,
    numerical verification, scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        HermiticityResult(
            residual=0.0,
            tolerance=negative_tolerance,
            energy_unit="eV",
        )

    message = str(exc_info.value)
    assert "Hermiticity tolerance" in message
    assert "non-negative" in message


@pytest.mark.parametrize(
    "invalid_energy_unit",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_hr_012_boolean_true"),
        pytest.param(False, id="sv_hr_012_boolean_false"),
        pytest.param(1, id="sv_hr_012_integer"),
        pytest.param(b"eV", id="bytes"),
        pytest.param(object(), id="sv_hr_012_arbitrary_object"),
    ],
)
def test_constructor__energy_unit_wrong_types_are_rejected__is_enforced(
    invalid_energy_unit: object,
) -> None:
    r"""Evidence ID
    SV-HR-012
    Requirement
    The energy unit must satisfy the approved Python string policy; other values are not
    converted or interpreted as unit names.
    Method
    Call the public constructor directly, using ``Any`` and ``cast`` only at the
    deliberate invalid unit boundary.
    Oracle
    The approved ResultObject contract uses ``isinstance(value, str)`` semantics and the
    field-specific string diagnostic; it does not impose an exact-built-in-string
    boundary or unit registry.
    Acceptance
    Every non-string raises exactly ``TypeError`` with field-specific wording that
    identifies the string requirement.
    Interpretation
    Passing establishes field-specific semantic typing without introducing physical-unit
    validation.
    Limitations
    Python string subclasses remain permitted by existing policy; NumPy string scalars
    are not Python ``str`` instances. No normalization, unit conversion, scientific
    validation, UQ, or Rust conformance is tested.
    """

    with pytest.raises(TypeError) as exc_info:
        HermiticityResult(
            residual=0.0,
            tolerance=1.0e-12,
            energy_unit=cast(Any, invalid_energy_unit),
        )

    message = str(exc_info.value)
    assert "Hermiticity energy unit" in message
    assert "string" in message


def test_constructor__empty_energy_unit_is_rejected_without__is_enforced() -> None:
    r"""Evidence ID
    SV-HR-013
    Requirement
    An empty energy-unit string is invalid; this task introduces no trimming,
    normalization, case folding, unit registry, or conversion.
    Method
    Construct directly with ``""`` and separately confirm that the existing
    nonempty-string policy leaves a whitespace-only string unchanged.
    Oracle
    The approved contract requires a nonempty Python string and deliberately specifies
    no syntax or physical-name validation.
    Acceptance
    The empty string raises exactly ``ValueError`` with field-specific empty-value
    wording, while ``" "`` remains accepted and retained exactly.
    Interpretation
    Passing establishes the existing lexical boundary without silently broadening unit
    semantics.
    Limitations
    acceptance of a nonempty string does not establish a recognized or physically
    suitable unit. No unit conversion, scientific validation, UQ, or Rust conformance is
    established.
    """

    with pytest.raises(ValueError) as exc_info:
        HermiticityResult(
            residual=0.0,
            tolerance=1.0e-12,
            energy_unit="",
        )

    message = str(exc_info.value)
    assert "Hermiticity energy unit" in message
    assert "empty" in message
    whitespace_result = HermiticityResult(0.0, 1.0e-12, " ")
    assert whitespace_result.energy_unit == " "
