r"""Software verification of private canonical JSON serializer implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of canonical JSON serialization delegated by the public
harness wire boundary. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private canonical JSON serializer implementation.
``_CanonicalJsonSerializer`` is used only as a direct implementation access point; its
name, defining module, constructor, and identity are not public contracts. Fixed
accepted fixtures and exact Python or JSON semantics are the behavioral oracles.

VVUQ and scientific exclusions

Passing checks only private implementation behavior supporting the public contract. It
does not make the private class public or establish numerical verification, scientific
validation, uncertainty quantification, physical correctness, or human acceptance.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.wire.canonical_json import (
    _CanonicalJsonSerializer,
    _DuplicateKey,
)

pytestmark = pytest.mark.software_verification
SUT = _CanonicalJsonSerializer
ROOT = Path(__file__).resolve().parents[7]


def test_artifact__dependency__canonical_json_has_no_domain_imports() -> None:
    """Evidence ID: software-verification.harness.wire.dependency.canonical-json

    Requirement: Canonical JSON mechanics remain independent of harness domains.

    Method: Parse canonical_json.py and collect its direct absolute imports.

    Oracle: The R2.5 dependency contract permits only the Python json dependency.

    Acceptance: The complete direct absolute-import set is exactly ``{"json"}``.

    Interpretation: Failure identifies domain coupling in canonical JSON mechanics.

    Limitations: Import direction alone does not establish canonical-byte behavior.
    """
    path = ROOT / "python/src/ksdft2effmass/harness/pi/wire/canonical_json.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert imports == {"json"}


def test_artifact__canonical_json__enforces_canonical_strict_json() -> None:
    """Evidence ID: software-verification.harness.wire.canonical-json-codec.contract

    Requirement: The codec emits canonical UTF-8 JSON plus LF and rejects duplicates.

    Method: Encode an unsorted object, decode its text, and decode a duplicate-key text.

    Oracle: The accepted canonical JSON byte contract and strict duplicate-key rule.

    Acceptance: Bytes and decoded value are exact; duplicate decoding raises the
    private duplicate-key result with the exact key.

    Interpretation: Failure identifies canonicalization or strictness drift.

    Limitations: This does not cover every malformed RFC 8259 input.
    """
    codec = SUT()
    payload = codec.encode({"z": 2, "a": "é"})
    assert payload == '{"a":"é","z":2}\n'.encode()
    assert codec.decode(payload.decode()) == {"a": "é", "z": 2}
    with pytest.raises(_DuplicateKey, match="^a$"):
        codec.decode('{"a":1,"a":2}')
