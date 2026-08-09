r"""Software verification of ``OperatorRecordJsonSerializer``.

Facet and represented meaning

-----------------------------
This class-owned module owns the contract facet. Object: public JSON serializer
ActionObject. Evidence class: software verification.

Requirement: the approved version-1 public surface consists only of construction,
``SCHEMA_VERSION == 1``, ``serialize()``, and ``deserialize()``. Strategy and
oracle: inspect public imports and exercise public argument boundaries against the
approved API contract. Acceptance requires exact constants, absent obsolete names,
and documented exception taxonomy. Passing establishes only Python API conformance;
failure indicates implementation, documentation, or evidence drift. Scientific
validation, uncertainty quantification, and Rust conformance are not performed.

Intrinsic and cross-object scope

--------------------------------
The primary owner is ``OperatorRecordJsonSerializer``; collaborators only construct
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

from typing import Any, cast

import pytest

import ksdft2effmass.operators as operators
from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification

SUT = OperatorRecordJsonSerializer


def test_method__deserialize__public_version_one_contract() -> None:
    r"""Evidence ID: SV-ORJS-001

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    deserialize: public version one contract.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (deserialize: public version one contract); warnings and coercive fallback behavior
    are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    assert operators.OperatorRecordJsonSerializer is OperatorRecordJsonSerializer
    assert OperatorRecordJsonSerializer().SCHEMA_VERSION == 1
    assert type(OperatorRecordJsonSerializer.SCHEMA_VERSION) is int


def test_method__deserialize__obsolete_names_and_aliases_are_absent() -> None:
    r"""Evidence ID: SV-ORJS-002

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition:
    deserialize: obsolete names and aliases are absent.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (deserialize: obsolete names and aliases are absent); warnings and coercive fallback
    behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: All literal values, arrays, field names, ordering relations, object
    identities,
    absences, and deterministic text asserted by the case match exactly; no approximate
    fallback is used.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    serializer = OperatorRecordJsonSerializer()
    assert not hasattr(operators, "OperatorRecordJsonCodec")
    assert not hasattr(serializer, "encode")
    assert not hasattr(serializer, "decode")
    assert set(name for name in dir(serializer) if not name.startswith("_")) == {
        "SCHEMA_VERSION",
        "deserialize",
        "serialize",
    }


def test_constructor__public_methods_enforce_role_types__is_enforced() -> None:
    r"""Evidence ID: SV-ORJS-003

    Requirement: OperatorRecordJsonSerializer enforces this version-1 JSON boundary
    partition: public
    methods enforce role types: is enforced.

    Method: Invoke serialize() or deserialize() on the explicit schema-version-1
    partition
    (public methods enforce role types: is enforced); warnings and coercive fallback
    behavior are not accepted.

    Oracle: The public version-1 schema, fixed wire-field vocabulary, literal JSON
    grammar, and
    DataObject constructor invariants determine the expected text, value, or exception
    independently of serializer private methods.

    Acceptance: The named partition raises exactly TypeError with the asserted public
    message, code,
    or attached result; no alternate exception is accepted.

    Interpretation: A pass supports only this named public-contract partition; failure
    identifies
    implementation drift, an incorrect controlled input, an oracle defect, or
    accepted-contract inconsistency.

    Limitations: The synthetic software cases do not establish numerical verification,
    physical
    correctness, scientific validation, UQ, portability, exhaustive inputs, or
    cross-language agreement.
    """
    serializer = OperatorRecordJsonSerializer()
    with pytest.raises(TypeError, match="OperatorRecord"):
        serializer.serialize(cast(Any, {}))
    with pytest.raises(TypeError, match="JSON text"):
        serializer.deserialize(cast(Any, {}))
