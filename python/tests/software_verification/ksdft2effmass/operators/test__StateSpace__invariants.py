r"""Software verification of ``StateSpace``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

-----------------------------
This class-owned module owns the invariants facet. This module owns semantic-type
and value rejection for ``identifier``, ``kind``,
and ``dimension``. ``StateSpace`` represents finite metadata for
:math:`\dim\mathcal H=N`; its dimension is a positive built-in integer after
constructor canonicalization, and its descriptive strings are nonempty.

These tests address only DataObject-owned metadata. Boolean, floating, complex,
string, byte, and arbitrary-object dimensions are not coerced. Cross-object
agreement with basis ordering or matrix shape belongs to ``OperatorRecord``.
The approved architecture and Sphinx contract are the oracle. Passing establishes
exact constructor exception taxonomy; failure may indicate an implementation
regression, documentation mismatch, or evidence defect.

This module provides software-verification evidence ``SV-SS-006`` through
``SV-SS-011``. It performs no numerical algorithm and establishes no physical
Hilbert space, basis completeness, operator-domain correctness, matrix
compatibility, DFT or Wannier validity, scientific validation, uncertainty
quantification, or Rust conformance.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``StateSpace``; collaborators only construct inputs or expose
public outcomes. Accepted public contracts, literal expected values, Python language
semantics, and assigned schema or fixture artifacts provide the oracles. No runtime
warning is accepted unless a test explicitly states otherwise.

VVUQ and scientific exclusions

------------------------------
Passing establishes only the documented software contract and exact or explicitly
bounded acceptance rules. Failure may identify implementation, fixture, oracle,
environment, or contract defects. It does not establish numerical verification,
physical correctness, scientific validation, UQ, portability, or cross-language
agreement.
"""

from typing import Any, cast

import numpy as np
import pytest

from ksdft2effmass.operators import StateSpace

pytestmark = pytest.mark.software_verification

SUT = StateSpace


@pytest.mark.parametrize(
    "invalid_dimension",
    [
        pytest.param(True, id="sv_ss_006_boolean_true"),
        pytest.param(False, id="sv_ss_006_boolean_false"),
        pytest.param(np.bool_(True), id="sv_ss_006_numpy_boolean"),
        pytest.param(None, id="none"),
        pytest.param(2.0, id="sv_ss_006_python_float"),
        pytest.param(np.float64(2.0), id="sv_ss_006_numpy_floating"),
        pytest.param("2", id="sv_ss_006_raw_string"),
        pytest.param(b"2", id="bytes"),
        pytest.param(2 + 0j, id="complex"),
        pytest.param(np.complex128(2 + 0j), id="complex"),
        pytest.param(object(), id="sv_ss_006_arbitrary_object"),
    ],
)
def test_constructor__invalid_dimension_wrong_types_are_rejected__is_enforced(
    invalid_dimension: object,
) -> None:
    r"""Evidence ID: SV-SS-006

    Requirement: Boolean, ``None``, floating, numeric-string, bytes, complex, and
    arbitrary-object
    values are not dimensions and are not coerced.

    Method: Use ``Any`` and ``cast`` only at the deliberate invalid public constructor
    boundary.

    Oracle: The approved contract requires dimension to be a positive integer and treats
    Boolean
    rejection as a runtime semantic refinement.

    Acceptance: Every case raises exactly ``TypeError`` with the approved semantic
    fragment
    ``state-space dimension must be a positive integer``.

    Interpretation: Passing establishes strict dimension semantic typing without numeric
    string or
    integral-float coercion.

    Limitations: Positivity has separate evidence. No matrix, basis, numerical
    algorithm, scientific
    validation, UQ, or Rust conformance is tested.
    """

    with pytest.raises(
        TypeError,
        match="state-space dimension must be a positive integer",
    ):
        StateSpace(
            identifier="two-level",
            kind="finite synthetic",
            dimension=cast(Any, invalid_dimension),
        )


@pytest.mark.parametrize(
    "invalid_dimension",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative_python_integer"),
        pytest.param(np.int64(-2), id="negative_numpy_integer"),
    ],
)
def test_constructor__nonpositive_dimensions_are_rejected__is_enforced(
    invalid_dimension: int | np.integer,
) -> None:
    r"""Evidence ID: SV-SS-007

    Requirement: The represented finite state-space dimension is positive; no zero-
    dimensional
    convention exists and negatives are not reinterpreted.

    Method: Construct directly with correctly typed nonpositive values.

    Oracle: The approved intrinsic positivity invariant defines ``ValueError`` and the
    positive
    diagnostic fragment.

    Acceptance: Every case raises exactly ``ValueError`` with the approved positivity
    wording.

    Interpretation: Passing establishes the semantic-type/value taxonomy split; positive
    one admission
    is independently exercised by ``the owning evidence``.

    Limitations: This does not add a maximum or allocation policy and establishes no
    scientific
    validation, uncertainty quantification, or Rust conformance.
    """

    with pytest.raises(ValueError, match="state-space dimension must be positive"):
        StateSpace(
            identifier="two-level",
            kind="finite synthetic",
            dimension=invalid_dimension,
        )


@pytest.mark.parametrize(
    "invalid_identifier",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_ss_008_boolean_true"),
        pytest.param(False, id="sv_ss_008_boolean_false"),
        pytest.param(1, id="sv_ss_008_integer"),
        pytest.param(b"space", id="bytes"),
        pytest.param(object(), id="sv_ss_008_arbitrary_object"),
    ],
)
def test_constructor__invalid_identifier_wrong_types_are_rejected__is_enforced(
    invalid_identifier: object,
) -> None:
    r"""Evidence ID: SV-SS-008

    Requirement: ``identifier`` names the represented space and must be a string; other
    values are
    not coerced into names.

    Method: Use ``Any`` and ``cast`` only for the deliberate invalid identifier at the
    public
    constructor boundary while other fields remain valid.

    Oracle: The approved field-specific contract requires a state-space identifier
    string.

    Acceptance: Every case raises exactly ``TypeError`` and the diagnostic identifies
    ``state-space
    identifier`` and the string requirement.

    Interpretation: Passing establishes identifier typing independently of ``kind``.

    Limitations: Label suitability and physical identity are not validated; no
    scientific validation,
    UQ, or Rust conformance is established.
    """

    with pytest.raises(TypeError) as exc_info:
        StateSpace(
            identifier=cast(Any, invalid_identifier),
            kind="finite synthetic",
            dimension=2,
        )

    message = str(exc_info.value)
    assert "state-space identifier" in message
    assert "string" in message


def test_constructor__empty_identifier_is_rejected_without__is_enforced() -> None:
    r"""Evidence ID: SV-SS-009

    Requirement: Identifier metadata must be nonempty; this task introduces no trimming,
    case
    folding, slug conversion, or Unicode normalization.

    Method: Construct directly with ``identifier=""`` and valid other fields.

    Oracle: The approved intrinsic invariant defines field-specific ``ValueError``.

    Acceptance: Construction raises exactly ``ValueError`` with identifier and empty-
    value wording.

    Interpretation: Passing establishes only the explicit empty-string boundary.

    Limitations: The evidence does not approve whitespace-only or every possible label
    and
    establishes no scientific validation, UQ, or Rust conformance.
    """

    with pytest.raises(ValueError) as exc_info:
        StateSpace(identifier="", kind="finite synthetic", dimension=2)

    message = str(exc_info.value)
    assert "state-space identifier" in message
    assert "must not be empty" in message


@pytest.mark.parametrize(
    "invalid_kind",
    [
        pytest.param(None, id="none"),
        pytest.param(True, id="sv_ss_010_boolean_true"),
        pytest.param(False, id="sv_ss_010_boolean_false"),
        pytest.param(1, id="sv_ss_010_integer"),
        pytest.param(b"finite", id="bytes"),
        pytest.param(object(), id="sv_ss_010_arbitrary_object"),
    ],
)
def test_constructor__invalid_kind_wrong_types_are_rejected__is_enforced(
    invalid_kind: object,
) -> None:
    r"""Evidence ID: SV-SS-010

    Requirement: ``kind`` is separate descriptive metadata and must be a string; other
    values are not
    coerced or treated as an enumeration.

    Method: Use ``Any`` and ``cast`` only for the deliberate invalid kind at the public
    constructor boundary while other fields remain valid.

    Oracle: The approved field-specific contract requires a state-space kind string.

    Acceptance: Every case raises exactly ``TypeError`` and the diagnostic identifies
    ``state-space
    kind`` and the string requirement.

    Interpretation: Passing establishes kind typing independently of ``identifier``.

    Limitations: No closed kind vocabulary or physical interpretation is validated; no
    scientific
    validation, UQ, or Rust conformance is established.
    """

    with pytest.raises(TypeError) as exc_info:
        StateSpace(
            identifier="two-level",
            kind=cast(Any, invalid_kind),
            dimension=2,
        )

    message = str(exc_info.value)
    assert "state-space kind" in message
    assert "string" in message


def test_constructor__empty_kind_is_rejected_without_enumeration__is_enforced() -> None:
    r"""Evidence ID: SV-SS-011

    Requirement: Kind metadata must be nonempty but remains a descriptive exact string,
    not a
    controlled enum.

    Method: Construct directly with ``kind=""`` and valid other fields.

    Oracle: The approved intrinsic invariant defines field-specific ``ValueError``.

    Acceptance: Construction raises exactly ``ValueError`` with kind and empty-value
    wording.

    Interpretation: Passing establishes only the explicit empty-string boundary.

    Limitations: No normalization, vocabulary suitability, physical meaning, scientific
    validation,
    UQ, or Rust conformance is established.
    """

    with pytest.raises(ValueError) as exc_info:
        StateSpace(identifier="two-level", kind="", dimension=2)

    message = str(exc_info.value)
    assert "state-space kind" in message
    assert "must not be empty" in message
