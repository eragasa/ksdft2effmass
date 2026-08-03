"""Software-verification evidence for ``HermiticityAnalyzer`` configuration.

Evidence IDs
------------
``SV-HA-001`` through ``SV-HA-010``.

Requirement
-----------
The public ActionObject requires explicit finite non-negative tolerance and
nonempty energy-unit configuration, canonicalizes approved real scalar families
to ``float``, is frozen and slotted, and owns no serialization API.

Method
------
``SV-HA-001`` through ``SV-HA-010`` exercise only public construction and
publicly observable dataclass state.

Oracle
------
The approved Analyzer contract in the operator-record architecture and Sphinx
Hermiticity documentation supplies the independent public oracle.

Acceptance
----------
Exact Python types, values, exception categories, semantic diagnostic fragments,
dataclass fields, and absent APIs must match the documented contract.

Interpretation
--------------
Passing establishes the Analyzer configuration boundary and error taxonomy;
failure indicates an implementation, contract-documentation, or evidence defect
that requires investigation.

Limitations
-----------
No matrix residual is computed. Scientific suitability of a tolerance,
scientific validation, uncertainty quantification, and Rust conformance are not
established.
"""

from dataclasses import FrozenInstanceError, fields
from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import HermiticityAnalyzer

pytestmark = pytest.mark.software_verification


def test_explicit_public_construction_stores_distinct_configuration() -> None:
    """SV-HA-001: verify explicit construction and stored configuration.

    Evidence ID
    -----------
    ``SV-HA-001``.
    Requirement
    -----------
    Both configuration values are explicit and stored as built-in Python types.
    Method
    ------
    Construct one Analyzer with distinct nonzero tolerance and ``"eV"`` unit.
    Oracle
    ------
    The approved public constructor and field contract defines expected state.
    Acceptance
    ----------
    Values and exact stored types must equal the declared expectations.
    Interpretation
    --------------
    Passing establishes explicit public configuration storage.
    Limitations
    -----------
    No default policy, tolerance suitability, scientific validation, UQ, or Rust
    conformance is established.
    """

    analyzer = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")

    assert analyzer.tolerance == 1.0e-12
    assert type(analyzer.tolerance) is float
    assert analyzer.energy_unit == "eV"
    assert type(analyzer.energy_unit) is str


@pytest.mark.parametrize(
    ("tolerance", "expected"),
    [
        pytest.param(2, 2.0, id="SV-HA-002-python-integer"),
        pytest.param(1.25, 1.25, id="SV-HA-002-python-float"),
        pytest.param(np.int64(3), 3.0, id="SV-HA-002-numpy-integer"),
        pytest.param(np.float32(0.5), 0.5, id="SV-HA-002-numpy-floating"),
    ],
)
def test_accepted_tolerance_scalar_families_are_canonicalized(
    tolerance: int | float | np.integer | np.floating, expected: float
) -> None:
    """SV-HA-002: verify accepted scalar-family value preservation.

    Evidence ID
    -----------
    ``SV-HA-002``.
    Requirement
    -----------
    Python and NumPy integer/floating scalars are admitted and stored as float.
    Method
    ------
    Construct an Analyzer from one representative of each approved family.
    Oracle
    ------
    Explicit independently selected scalar values define expected conversion.
    Acceptance
    ----------
    Stored type is exactly ``float`` and value equals the expected value.
    Interpretation
    --------------
    Passing establishes runtime admission, canonical type, and preserved value.
    Limitations
    -----------
    Boolean is a rejected runtime semantic refinement. No matrix, scientific
    validation, UQ, or Rust conformance is covered.
    """

    analyzer = HermiticityAnalyzer(tolerance=tolerance, energy_unit="eV")

    assert type(analyzer.tolerance) is float
    assert analyzer.tolerance == expected


@pytest.mark.parametrize(
    "tolerance",
    [
        pytest.param(True, id="SV-HA-003-python-boolean-true"),
        pytest.param(False, id="SV-HA-003-python-boolean-false"),
        pytest.param(np.bool_(True), id="SV-HA-003-numpy-boolean"),
        pytest.param(None, id="SV-HA-003-none"),
        pytest.param("1e-12", id="SV-HA-003-string"),
        pytest.param(b"1e-12", id="SV-HA-003-bytes"),
        pytest.param(1.0 + 0.0j, id="SV-HA-003-python-complex"),
        pytest.param(np.complex128(1.0), id="SV-HA-003-numpy-complex"),
        pytest.param(object(), id="SV-HA-003-arbitrary-object"),
    ],
)
def test_invalid_tolerance_semantic_types_are_rejected(tolerance: Any) -> None:
    """SV-HA-003: verify invalid tolerance semantic-type rejection.

    Evidence ID
    -----------
    ``SV-HA-003``.
    Requirement
    -----------
    Non-real semantic families, including Booleans, raise ``TypeError``.
    Method
    ------
    Pass independently identified invalid public inputs without coercion.
    Oracle
    ------
    The approved scalar taxonomy defines the rejected families.
    Acceptance
    ----------
    Exact exception type is ``TypeError`` with a real-number diagnostic.
    Interpretation
    --------------
    Passing establishes rejection rather than accidental numeric coercion.
    Limitations
    -----------
    ``Any`` is confined to this deliberate invalid-input boundary; no numerical
    residual, scientific validation, UQ, or Rust conformance is tested.
    """

    with pytest.raises(TypeError, match="real number"):
        HermiticityAnalyzer(tolerance=cast(Any, tolerance), energy_unit="eV")


@pytest.mark.parametrize(
    "tolerance",
    [
        pytest.param(float("nan"), id="SV-HA-004-nan"),
        pytest.param(float("inf"), id="SV-HA-004-positive-infinity"),
        pytest.param(float("-inf"), id="SV-HA-004-negative-infinity"),
        pytest.param(10**10000, id="SV-HA-004-huge-positive-integer"),
        pytest.param(-(10**10000), id="SV-HA-004-huge-negative-integer"),
    ],
)
def test_nonfinite_or_overflowing_tolerances_use_value_error(
    tolerance: int | float,
) -> None:
    """SV-HA-004: verify nonfinite and conversion-overflow rejection.

    Evidence ID
    -----------
    ``SV-HA-004``.
    Requirement
    -----------
    Nonfinite values and binary64 conversion overflow raise ``ValueError``.
    Method
    ------
    Construct with NaN, both infinities, and huge signed Python integers.
    Oracle
    ------
    IEEE-754 classification and the approved finite-number taxonomy are used.
    Acceptance
    ----------
    ``ValueError`` with a finite-number diagnostic occurs; ``OverflowError``
    cannot escape because the exact expected exception is asserted.
    Interpretation
    --------------
    Passing establishes the public conversion-failure taxonomy.
    Limitations
    -----------
    It does not test matrix arithmetic, scientific validation, UQ, or Rust.
    """

    with pytest.raises(ValueError, match="finite"):
        HermiticityAnalyzer(tolerance=tolerance, energy_unit="eV")


@pytest.mark.parametrize(
    "tolerance",
    [
        pytest.param(-1.0, id="SV-HA-005-python-negative"),
        pytest.param(np.float64(-1.0e-12), id="SV-HA-005-numpy-negative"),
    ],
)
def test_finite_negative_tolerances_are_rejected(
    tolerance: float | np.floating,
) -> None:
    """SV-HA-005: verify the nonnegative tolerance invariant.

    Evidence ID
    -----------
    ``SV-HA-005``.
    Requirement
    -----------
    A finite negative tolerance is invalid ActionObject policy.
    Method
    ------
    Construct with representative Python and NumPy negative floating values.
    Oracle
    ------
    The approved invariant is ``tolerance >= 0``.
    Acceptance
    ----------
    ``ValueError`` contains the semantic fragment ``non-negative``.
    Interpretation
    --------------
    Passing establishes sign validation after scalar admission.
    Limitations
    -----------
    It does not select a scientifically appropriate nonnegative tolerance or
    establish scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError, match="non-negative"):
        HermiticityAnalyzer(tolerance=tolerance, energy_unit="eV")


def test_energy_unit_is_a_required_explicit_argument() -> None:
    """SV-HA-006: verify omission of the required energy-unit argument.

    Evidence ID
    -----------
    ``SV-HA-006``.
    Requirement
    -----------
    Analyzer construction has no implicit or unitless energy-unit path.
    Method
    ------
    Omit only ``energy_unit`` from an otherwise valid constructor call.
    Oracle
    ------
    The approved public signature requires ``energy_unit``.
    Acceptance
    ----------
    ``TypeError`` mentions the stable argument name without freezing full text.
    Interpretation
    --------------
    Passing establishes required explicit unit configuration.
    Limitations
    -----------
    No default is inferred; unit validity, scientific validation, UQ, and Rust
    conformance are not established.
    """

    with pytest.raises(TypeError, match="energy_unit"):
        HermiticityAnalyzer(tolerance=1.0e-12)  # type: ignore[call-arg]


@pytest.mark.parametrize(
    "energy_unit",
    [
        pytest.param(None, id="SV-HA-007-none"),
        pytest.param(True, id="SV-HA-007-boolean-true"),
        pytest.param(False, id="SV-HA-007-boolean-false"),
        pytest.param(1, id="SV-HA-007-integer"),
        pytest.param(b"eV", id="SV-HA-007-bytes"),
        pytest.param(object(), id="SV-HA-007-arbitrary-object"),
    ],
)
def test_invalid_energy_unit_semantic_types_are_rejected(energy_unit: Any) -> None:
    """SV-HA-007: verify energy-unit semantic-type rejection.

    Evidence ID
    -----------
    ``SV-HA-007``.
    Requirement
    -----------
    The configured energy unit must be a Python string.
    Method
    ------
    Pass representative non-string public values without coercion.
    Oracle
    ------
    The approved exact energy-unit metadata policy defines string admission.
    Acceptance
    ----------
    Exact ``TypeError`` category includes a string diagnostic.
    Interpretation
    --------------
    Passing establishes the public unit-type boundary.
    Limitations
    -----------
    ``Any`` is confined to invalid inputs. Unit registries, conversion,
    scientific validation, UQ, and Rust conformance are excluded.
    """

    with pytest.raises(TypeError, match="string"):
        HermiticityAnalyzer(tolerance=0.0, energy_unit=cast(Any, energy_unit))


def test_empty_energy_unit_is_rejected() -> None:
    """SV-HA-008: verify the nonempty energy-unit invariant.

    Evidence ID
    -----------
    ``SV-HA-008``.
    Requirement
    -----------
    The Analyzer unit string must not be empty.
    Method
    ------
    Construct with the exact empty string.
    Oracle
    ------
    The approved metadata invariant distinguishes empty from nonempty strings.
    Acceptance
    ----------
    ``ValueError`` includes the semantic fragment ``not be empty``.
    Interpretation
    --------------
    Passing establishes nonemptiness without normalization.
    Limitations
    -----------
    No trimming, case folding, registry, conversion, scientific validation, UQ,
    or Rust conformance is established.
    """

    with pytest.raises(ValueError, match="not be empty"):
        HermiticityAnalyzer(tolerance=0.0, energy_unit="")


def test_configuration_is_frozen_slotted_and_has_exact_fields() -> None:
    """SV-HA-009: verify frozen, slotted Analyzer configuration.

    Evidence ID
    -----------
    ``SV-HA-009``.
    Requirement
    -----------
    Stored fields are exactly ``tolerance`` and ``energy_unit`` and immutable.
    Method
    ------
    Inspect public dataclass fields and attempt ordinary assignment to each.
    Oracle
    ------
    The approved frozen/slotted ActionObject declaration defines the state.
    Acceptance
    ----------
    Field names match exactly, ``__dict__`` is absent, and each assignment raises
    the exact ``FrozenInstanceError`` dataclass exception.
    Interpretation
    --------------
    Passing establishes ordinary API-level configuration immutability.
    Limitations
    -----------
    Hash behavior is deliberately untested; scientific validation, UQ, and Rust
    conformance are not established.
    """

    analyzer = HermiticityAnalyzer(tolerance=1.0e-12, energy_unit="eV")

    assert tuple(field.name for field in fields(analyzer)) == (
        "tolerance",
        "energy_unit",
    )
    assert not hasattr(analyzer, "__dict__")
    with pytest.raises(FrozenInstanceError):
        analyzer.tolerance = 0.0  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        analyzer.energy_unit = "hartree"  # type: ignore[misc]


def test_analyzer_has_no_serialization_api() -> None:
    """SV-HA-010: verify exclusion of Analyzer serialization APIs.

    Evidence ID
    -----------
    ``SV-HA-010``.
    Requirement
    -----------
    Analyzer policy has no approved wire or dictionary format.
    Method
    ------
    Check the six prohibited serialization/deserialization names on an instance.
    Oracle
    ------
    Serialization belongs to ``OperatorRecordJsonSerializer`` only.
    Acceptance
    ----------
    Every unsupported API name is absent.
    Interpretation
    --------------
    Passing establishes ActionObject serialization exclusion.
    Limitations
    -----------
    It does not prohibit a future separately approved serializer and establishes
    no scientific validation, UQ, or Rust conformance.
    """

    analyzer = HermiticityAnalyzer(tolerance=0.0, energy_unit="eV")

    for name in (
        "to_json",
        "to_dict",
        "serialize",
        "from_json",
        "from_dict",
        "deserialize",
    ):
        assert not hasattr(analyzer, name)
