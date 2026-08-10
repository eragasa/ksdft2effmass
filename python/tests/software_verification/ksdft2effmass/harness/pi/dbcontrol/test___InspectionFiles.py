r"""Software verification of ``_InspectionFiles``.

Facet and represented meaning

The module owns the intrinsic represented behavior of ``_InspectionFiles``.

Intrinsic and cross-object scope

Only the object's bounded contract is exercised; collaborators are literal inputs.

VVUQ and scientific exclusions

This is software verification only; scientific validation and UQ are excluded.
"""

from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.dbcontrol.files import _InspectionFiles

SUT = _InspectionFiles

pytestmark = pytest.mark.software_verification


def test_method__inspect_literal_file__returns_exact_bytes(tmp_path: Path) -> None:
    """Evidence ID: software-verification.harness.dbcontrol.inspection-files.method.literal-file

    Requirement: Root-confined inspection reads the exact declared regular file.

    Method: Write immutable literal bytes beneath a canonical temporary root and inspect the relative path.

    Oracle: The literal payload is independently supplied as ``b"control"``.

    Acceptance: Exact bytes are returned and the path occurs in inspected and read sets only.

    Interpretation: Failure indicates read tracking or byte-preservation drift.

    Limitations: Symlink and race behavior are excluded.
    """  # noqa: E501
    (tmp_path / "state.json").write_bytes(b"control")
    files = _InspectionFiles(tmp_path.resolve(), "task.test")
    assert files.inspect("state.json") == b"control"
    assert files.inspected == files.read == {"state.json"}
    assert files.missing == set()
