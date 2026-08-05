"""Evidence class and represented meaning
Software verification of portable artifact specification metadata.
Owned contract, oracle, and scope
ArtifactSpecification is the SUT; accepted P2 path and identifier rules are the oracle.
VVUQ and scientific exclusions
Evidence excludes filesystem resolution, numerical verification, scientific validation,
UQ, physical correctness, and cross-language conformance.
"""

from dataclasses import FrozenInstanceError

import pytest

from ksdft2effmass.provenance import ArtifactSpecification

SUT = ArtifactSpecification
pytestmark = pytest.mark.software_verification


def test_constructor__field_mapping_and_immutability__preserves_portable_metadata() -> (
    None
):
    """Evidence ID
    SV-PROV-004
    Requirement
    The specification stores exactly logical path, format, semantic role, and retention
    policy and is frozen.
    Method
    Construct through the public import, inspect fields, and attempt reassignment.
    Oracle
    The accepted P2 field vocabulary and frozen DataObject rule are exact.
    Acceptance
    The field tuple equals the inputs and reassignment raises FrozenInstanceError.
    Interpretation
    Failure indicates field drift or operational mutability.
    Limitations
    Values are synthetic metadata; no storage or retention action occurs.
    """
    value = SUT("outputs/result.json", "json", "result", "retain")
    assert (
        value.logical_path,
        value.format,
        value.semantic_role,
        value.retention_policy,
    ) == (
        "outputs/result.json",
        "json",
        "result",
        "retain",
    )
    with pytest.raises(FrozenInstanceError):
        value.format = "text"  # type: ignore[misc]


def test_constructor__root_relative_path__rejects_nonportable_forms() -> None:
    """Evidence ID
    SV-PROV-005
    Requirement
    Logical paths are nonempty NFC root-relative POSIX lexical paths without controls or
    Windows devices.
    Method
    Attempt absolute, parent, backslash, drive, device, non-NFC, and C1-control paths.
    Oracle
    The accepted H1/H2 lexical path partition incorporated by P2 is independently fixed.
    Acceptance
    Every prohibited path raises ValueError; a nested POSIX path is accepted.
    Interpretation
    Failure indicates a path-contract implementation or evidence defect.
    Limitations
    No filesystem, symlink, case-folding filesystem, or URI behavior is exercised.
    """
    assert SUT("a/b", "json", "result", "retain").logical_path == "a/b"
    for path in ("/a", "../a", "a\\b", "C:/a", "CON.txt", "e\u0301/a", "a\u0085b"):
        with pytest.raises(ValueError):
            SUT(path, "json", "result", "retain")
