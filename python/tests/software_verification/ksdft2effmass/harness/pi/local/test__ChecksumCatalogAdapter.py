r"""Software verification of ``ChecksumCatalogAdapter``.

Evidence profile: claim_bearing

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

The module verifies adaptation of explicit checksum-catalog bytes.

Intrinsic and cross-object scope

``ChecksumCatalogAdapter`` is the sole system under test.

VVUQ and scientific exclusions

Passing establishes software behavior only, not scientific validation or UQ.
"""

from typing import Any, cast

import pytest

from ksdft2effmass.harness.pi.local import ChecksumCatalogAdapter

pytestmark = pytest.mark.software_verification
SUT = ChecksumCatalogAdapter


def test_method__execute__sorts_entries_and_rejects_malformed_lines() -> None:
    """Evidence ID: SV-HL-042

    Requirement: Explicit checksum entries are sorted and malformed catalogs fail
    closed.

    Method: Adapt two reversed valid lines and one line without the required separator.

    Oracle: The adapter contract fixes lexical path ordering and the checksum-line
    shape.

    Acceptance: Valid paths equal ``["a", "z"]``; malformed input fails with no value.

    Interpretation: Failure indicates ordering drift or permissive parsing.

    Limitations: The test does not hash referenced files or establish scientific
    validity or UQ.
    """
    result = ChecksumCatalogAdapter().execute(
        b"b" * 64 + b"  z\n" + b"a" * 64 + b"  a\n"
    )
    assert result.validation.status == "PASS"
    assert [item.path for item in cast(Any, result.value).entries] == ["a", "z"]
    malformed = ChecksumCatalogAdapter().execute(b"no separator")
    assert malformed.validation.status == "FAIL"
    assert malformed.value is None
