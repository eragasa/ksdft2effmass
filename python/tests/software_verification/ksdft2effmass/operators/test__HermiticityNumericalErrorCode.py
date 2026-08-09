r"""Software verification of ``HermiticityNumericalErrorCode``.

Facet and represented meaning

-----------------------------
This class-owned module owns the HermiticityNumericalErrorCode facet. System under
test
-----------------
``HermiticityNumericalErrorCode`` is the closed public numerical-error-code enum
for Hermiticity residual calculation. Its only approved member is
``NONFINITE_RESIDUAL`` with stable machine-readable value
``"nonfinite_residual"``. ``HermiticityAnalyzer`` owns production emission when
analysis cannot produce a finite binary64 value for

.. math::

\varepsilon_{\mathrm H}
=
\max_{i,j}\left|H_{ij}-H_{ji}^{*}\right|.

This can occur even for individually finite stored matrix entries because
forming :math:`H-H^\dagger` can overflow. The enum itself performs no matrix
operation, floating-point detection, or exception construction.

Taxonomy separation
-------------------
The structured Hermiticity failures are distinct:

.. code-block:: text

unit disagreement
HermiticityUnitMismatchError

finite residual greater than tolerance
HermiticityRequirementError

residual cannot be represented as finite
HermiticityNumericalErrorCode.NONFINITE_RESIDUAL

The Hermiticity numerical code is also separate from represented-difference
``OperatorRecordDifferenceNumericalErrorCode`` and residual-comparison
``OperatorRecordComparisonNumericalErrorCode``. These taxonomies are not
aliases and are not merged. A nonfinite residual is a software/numerical failure,
not evidence that the underlying physical Hamiltonian is non-Hermitian.

Evidence class, strategy, and oracle
------------------------------------
This cohesive module provides software-verification evidence ``SV-HNEC-001``
through ``SV-HNEC-006``. An independently written literal tuple is the oracle
for exact name, value, count, and order. Public ``Enum.__members__``, Python 3.14
``StrEnum`` behavior, public name/value lookups, and standard Enum exception
classes verify the remaining closed-vocabulary contract. Production emission
belongs to Analyzer software-verification evidence; residual accuracy belongs to
numerical verification.

Interpretation and VVUQ boundaries
----------------------------------
Passing establishes enum vocabulary, no-alias policy, machine-string behavior,
and lookup taxonomy only. Failure may indicate an enum regression,
documentation mismatch, or evidence defect requiring investigation. These tests
invoke no Analyzer, Result, record, NumPy operation, overflow case, warning
filter, private helper, or dependent exception. They establish no Analyzer
emission, residual accuracy, backend-independent floating-point behavior,
physical tolerance suitability, physical Hermiticity, scientific validation,
uncertainty quantification, Rust implementation, or Rust conformance.
``StrEnum`` behavior does not approve a numerical-error wire format.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``HermiticityNumericalErrorCode``; collaborators only construct
inputs or expose public outcomes. Accepted public contracts, literal expected
values, Python language semantics, and assigned schema or fixture artifacts provide
the oracles. No runtime warning is accepted unless a test explicitly states
otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

import re
from enum import StrEnum

import pytest

from ksdft2effmass.operators import HermiticityNumericalErrorCode

pytestmark = pytest.mark.software_verification

SUT = HermiticityNumericalErrorCode


# This immutable literal is independent of production enum iteration so an
# implementation change cannot regenerate its own expected contract.
EXPECTED_MEMBERS = (
    (
        "NONFINITE_RESIDUAL",
        "nonfinite_residual",
    ),
)


def test_field__exact_closed_member_sequence_and_stable_value__is_exact() -> None:
    r"""Evidence ID: SV-HNEC-001

    Requirement: Public iteration contains exactly ``NONFINITE_RESIDUAL`` with stable
    value
    ``nonfinite_residual`` in the sole declaration-order position.

    Method: Compare public enum iteration with the independently written literal
    ``EXPECTED_MEMBERS`` tuple.

    Oracle: The approved closed contract is the literal ordered name/value sequence, not
    a
    sequence generated from production members.

    Acceptance: Iterated name/value pairs equal ``EXPECTED_MEMBERS`` exactly.

    Interpretation: Passing establishes one member, exact name and value, deterministic
    order, and
    absence of unapproved additional iterable members.

    Limitations: This does not inspect source location or establish Analyzer emission,
    numerical
    accuracy, physical Hermiticity, scientific validation, uncertainty quantification,
    or Rust conformance.
    """

    assert (
        tuple((code.name, code.value) for code in HermiticityNumericalErrorCode)
        == EXPECTED_MEMBERS
    )


def test_field__public_member_registry_contains_no_aliases__is_exact() -> None:
    r"""Evidence ID: SV-HNEC-002

    Requirement: The public Enum registry contains only ``NONFINITE_RESIDUAL`` mapped to
    the sole
    canonical member.

    Method: Compare documented ``Enum.__members__`` with an independently explicit
    one-entry
    dictionary and compare registry and iteration counts.

    Oracle: The approved no-alias contract permits exactly one declared public name and
    one
    iterable member.

    Acceptance: Registry equality and both explicit lengths equal one.

    Interpretation: Passing establishes no compatibility aliases or hidden declared
    names.

    Limitations: No private Enum internals, Analyzer behavior, numerical verification,
    serialization,
    scientific validation, uncertainty quantification, or Rust conformance is tested.
    """

    expected_registry = {
        "NONFINITE_RESIDUAL": HermiticityNumericalErrorCode.NONFINITE_RESIDUAL,
    }

    assert HermiticityNumericalErrorCode.__members__ == expected_registry
    assert len(HermiticityNumericalErrorCode.__members__) == 1
    assert len(tuple(HermiticityNumericalErrorCode)) == 1


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            HermiticityNumericalErrorCode.NONFINITE_RESIDUAL, id="nonfinite_residual"
        ),
    ],
)
def test_field__represented_state__strenum_machine_value(
    code: HermiticityNumericalErrorCode,
) -> None:
    r"""Evidence ID: SV-HNEC-003

    Requirement: The enum subclasses ``StrEnum`` and its member behaves as the ASCII
    lowercase
    snake-case machine-readable string ``nonfinite_residual``.

    Method: Inspect public inheritance, string type/equality, ``str()``, lexical full
    match, and
    ASCII encoding.

    Oracle: Python 3.14 ``StrEnum`` semantics and the approved literal machine value and
    lexical
    convention.

    Acceptance: Every inheritance, string, lexical, and ASCII check succeeds.

    Interpretation: Passing establishes deterministic in-memory Python machine-string
    behavior for the
    sole member.

    Limitations: ``repr()``, hash, pickle, JSON, wire formats, numerical detection,
    scientific
    validation, uncertainty quantification, and Rust conformance are not tested.
    """

    assert issubclass(HermiticityNumericalErrorCode, StrEnum)
    assert isinstance(code, str)
    assert code == "nonfinite_residual"
    assert str(code) == "nonfinite_residual"
    assert re.fullmatch(r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*", code.value) is not None
    assert code.value.encode("ascii") == b"nonfinite_residual"


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            HermiticityNumericalErrorCode.NONFINITE_RESIDUAL, id="nonfinite_residual"
        ),
    ],
)
def test_method__call__value_based_lookup_round_trips(
    code: HermiticityNumericalErrorCode,
) -> None:
    r"""Evidence ID: SV-HNEC-004

    Requirement: ``EnumClass(value)`` returns the canonical member for both its public
    value and the
    independently literal ``nonfinite_residual`` string.

    Method: Perform both public value-construction forms and compare by identity.

    Oracle: Standard Enum value lookup and the approved stable literal value.

    Acceptance: Both lookups return the exact canonical singleton.

    Interpretation: Passing establishes deterministic value-based round trips.

    Limitations: Uppercase, padded, byte, integer, and unrelated-enum coercions are not
    approved as
    successful behavior. No Analyzer execution, numerical verification, scientific
    validation, UQ, or Rust conformance is tested.
    """

    assert HermiticityNumericalErrorCode(code.value) is code
    assert HermiticityNumericalErrorCode("nonfinite_residual") is code


@pytest.mark.parametrize(
    "code",
    [
        pytest.param(
            HermiticityNumericalErrorCode.NONFINITE_RESIDUAL, id="nonfinite_residual"
        ),
    ],
)
def test_method__getitem__name_based_lookup_round_trips(
    code: HermiticityNumericalErrorCode,
) -> None:
    r"""Evidence ID: SV-HNEC-005

    Requirement: ``EnumClass[name]`` returns the canonical member for both its public
    name and the
    independently literal ``NONFINITE_RESIDUAL`` name.

    Method: Perform both public name-subscription forms and compare by identity.

    Oracle: Standard Enum name lookup and the approved literal public name.

    Acceptance: Both lookups return the exact canonical singleton.

    Interpretation: Passing establishes name lookup separately from value construction.

    Limitations: The member name is not the lowercase machine value. No Analyzer
    emission, numerical
    verification, serialization, scientific validation, uncertainty quantification, or
    Rust conformance is tested.
    """

    assert HermiticityNumericalErrorCode[code.name] is code
    assert HermiticityNumericalErrorCode["NONFINITE_RESIDUAL"] is code


@pytest.mark.parametrize(
    "lookup_kind",
    [
        pytest.param("invalid-value", id="invalid_value"),
        pytest.param("invalid-name", id="invalid_name"),
    ],
)
def test_constructor__invalid_lookup_exception_taxonomy__is_enforced(
    lookup_kind: str,
) -> None:
    r"""Evidence ID: SV-HNEC-006

    Requirement: An unknown value raises ``ValueError`` and an unknown name raises
    ``KeyError``
    through their distinct public lookup forms.

    Method: Exercise one invalid ``EnumClass(value)`` construction and one invalid
    ``EnumClass[name]`` subscription without a broad exception tuple.

    Oracle: Standard Enum taxonomy specifies ``ValueError`` for invalid values and
    ``KeyError``
    for invalid names.

    Acceptance: Each parameter raises exactly its required standard exception class.

    Interpretation: Passing establishes predictable lookup-failure taxonomy.

    Limitations: Standard-library message wording is not frozen. No Analyzer, matrix,
    numerical
    algorithm, dependent exception, scientific validation, uncertainty quantification,
    or Rust conformance is tested.
    """

    if lookup_kind == "invalid-value":
        with pytest.raises(ValueError):
            HermiticityNumericalErrorCode("unknown_hermiticity_numerical_error")
    else:
        with pytest.raises(KeyError):
            HermiticityNumericalErrorCode["UNKNOWN_HERMITICITY_NUMERICAL_ERROR"]
