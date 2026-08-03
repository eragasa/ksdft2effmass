"""OperatorRecordJsonSerializer contract software verification.

Object: public JSON serializer ActionObject. Evidence class: software verification.
Requirement: the approved version-1 public surface consists only of construction,
``SCHEMA_VERSION == 1``, ``serialize()``, and ``deserialize()``. Strategy and
oracle: inspect public imports and exercise public argument boundaries against the
approved API contract. Acceptance requires exact constants, absent obsolete names,
and documented exception taxonomy. Passing establishes only Python API conformance;
failure indicates implementation, documentation, or evidence drift. Scientific
validation, uncertainty quantification, and Rust conformance are not performed.
"""

from typing import Any, cast

import pytest

import ksdft2effmass.operators as operators
from ksdft2effmass.operators import OperatorRecordJsonSerializer

pytestmark = pytest.mark.software_verification


def test_public_version_one_contract() -> None:
    """Evidence ID: SV-ORJS-001.

    Requirement: the canonical package exports the serializer with version one.
    Method: import through the public package and construct it. Oracle: the approved
    API and schema-version decision. Interpretation: a pass fixes the public name
    and integer value; failure is API drift. Limitations: no payload, scientific
    validation, UQ, or Rust conformance is tested.
    """
    assert operators.OperatorRecordJsonSerializer is OperatorRecordJsonSerializer
    assert OperatorRecordJsonSerializer().SCHEMA_VERSION == 1
    assert type(OperatorRecordJsonSerializer.SCHEMA_VERSION) is int


def test_obsolete_names_and_aliases_are_absent() -> None:
    """Evidence ID: SV-ORJS-002.

    Requirement: codec, encode/decode, and record-owned aliases are unsupported.
    Method: inspect only documented public objects. Oracle: the approved replacement
    contract. Interpretation: a pass prevents accidental compatibility widening;
    failure indicates an unauthorized alias. Limitations: historical third-party
    usage, scientific validation, UQ, and Rust conformance are not assessed.
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


def test_public_methods_enforce_role_types() -> None:
    """Evidence ID: SV-ORJS-003.

    Requirement: serialize accepts only OperatorRecord and deserialize only str.
    Method: submit representative wrong public-role values. Oracle: documented
    TypeError taxonomy. Acceptance requires exact TypeError boundaries.
    Interpretation: failure indicates unintended coercion or taxonomy drift.
    Limitations: malformed string contents belong to other facets; no scientific
    validation, UQ, or Rust conformance is established.
    """
    serializer = OperatorRecordJsonSerializer()
    with pytest.raises(TypeError, match="OperatorRecord"):
        serializer.serialize(cast(Any, {}))
    with pytest.raises(TypeError, match="JSON text"):
        serializer.deserialize(cast(Any, {}))
