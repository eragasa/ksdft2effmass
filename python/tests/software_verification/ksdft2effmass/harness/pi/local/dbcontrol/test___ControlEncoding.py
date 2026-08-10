r"""Software verification of ``_ControlEncoding``.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_ControlEncoding``.

Intrinsic and cross-object scope

Only the owner's bounded contract is exercised with literal or immutable inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

import pytest

from ksdft2effmass.harness.pi.local.dbcontrol.encoding import _ControlEncoding

SUT = _ControlEncoding

pytestmark = pytest.mark.software_verification


def test_staticmethod__encodings__match_independent_literals() -> None:
    """Evidence ID: software-verification.harness.dbcontrol.control-encoding.static-method.literal-encodings

    Requirement: Control hashing and JSON encodings are deterministic exact-byte contracts.

    Method: Encode immutable ASCII inputs through each operation.

    Oracle: The SHA-256 of ``abc`` and canonical JSON bytes are fixed published/language-level literals.

    Acceptance: Results equal the exact independent digest and byte strings.

    Interpretation: Failure indicates identity or projection encoding drift.

    Limitations: Unicode normalization is excluded.
    """  # noqa: E501
    assert (
        _ControlEncoding.sha256(b"abc")
        == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    )
    assert _ControlEncoding.json_bytes({"b": 1}) == b'{\n  "b": 1\n}\n'
    assert _ControlEncoding.canonical_json_bytes({"b": 1, "a": 2}) == b'{"a":2,"b":1}\n'
    assert _ControlEncoding.slug("HTTP Value") == "http-value"
