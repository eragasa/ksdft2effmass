r"""Software verification of petrinet.colored v1 value compatibility.

Evidence profile: routine

Bounded artifact scope: shared expected scalar behavior between the accepted v1
``ContractValue`` and v2 ``ColoredPetriNetValue`` public surfaces.

Facet and represented meaning

The artifact represents the explicitly retained finite tagged-value behavior,
not class identity, package ownership, token routing, or a wire format.

Intrinsic and cross-object scope

Exact stored built-in types and values plus exact exception classes are compared
at scalar boundaries. The two public classes remain nominally distinct.

VVUQ and scientific exclusions

These synthetic comparisons establish software compatibility only. They provide
no numerical verification, scientific validation, uncertainty quantification,
physical meaning, simulation execution, or human acceptance.
"""

import math

import pytest

from ksdft2effmass.petrinet.colored import (
    ColoredPetriNetValue,
    ColoredPetriNetValueKind,
)
from ksdft2effmass.workflows.cpn import ContractValue, ContractValueKind

pytestmark = pytest.mark.software_verification


@pytest.mark.parametrize(
    ("kind", "value"),
    [
        pytest.param("none", None, id="none"),
        pytest.param("boolean", False, id="boolean"),
        pytest.param("integer", -(2**63), id="minimum_i64"),
        pytest.param("integer", 2**63 - 1, id="maximum_i64"),
        pytest.param("real", 2**53 + 1, id="rounded_integer_real"),
        pytest.param("real", -2.5, id="finite_float_real"),
        pytest.param("string", "value", id="string"),
        pytest.param("string_sequence", ("a", "a"), id="ordered_duplicates"),
    ],
)
def test_artifact__compatible_values__preserves_v1_scalar_results(
    kind: str,
    value: object,
) -> None:
    """Evidence ID: SV-PETRINET-022

    Requirement: The v2 value slice retains the declared v1 finite tagged-scalar
    result behavior without aliasing the classes.

    Acceptance: Both public constructors store equal values of the exact same
    built-in type for every named compatible partition.
    """
    v1 = ContractValue(ContractValueKind(kind), value)  # type: ignore[arg-type]
    v2 = ColoredPetriNetValue(
        ColoredPetriNetValueKind(kind),
        value,  # type: ignore[arg-type]
    )
    assert type(v2.value) is type(v1.value)
    assert v2.value == v1.value


@pytest.mark.parametrize(
    ("kind", "value", "exception_type"),
    [
        pytest.param("integer", True, TypeError, id="boolean_integer"),
        pytest.param("real", "1.0", TypeError, id="numeric_string_real"),
        pytest.param("integer", 2**63, ValueError, id="integer_above_i64"),
        pytest.param("real", math.inf, ValueError, id="positive_infinity"),
        pytest.param(
            "string_sequence",
            ("",),
            ValueError,
            id="empty_sequence_member",
        ),
    ],
)
def test_artifact__compatible_failures__preserves_v1_exception_taxonomy(
    kind: str,
    value: object,
    exception_type: type[Exception],
) -> None:
    """Evidence ID: SV-PETRINET-023

    Requirement: The v2 value slice retains the declared v1 exception taxonomy
    at shared scalar boundaries.

    Acceptance: Both public constructors raise the same exact expected exception
    class for every named incompatible partition.
    """
    with pytest.raises(exception_type):
        ContractValue(ContractValueKind(kind), value)  # type: ignore[arg-type]
    with pytest.raises(exception_type):
        ColoredPetriNetValue(
            ColoredPetriNetValueKind(kind),
            value,  # type: ignore[arg-type]
        )
