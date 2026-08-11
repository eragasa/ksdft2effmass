r"""Software verification of private duplicate-key result implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of duplicate-key diagnostic transport delegated by the
public harness wire boundary. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private duplicate-key result implementation. ``_DuplicateKey``
is used only as a direct implementation access point; its name, defining module,
constructor, and identity are not public contracts. Fixed accepted fixtures and exact
Python or JSON semantics are the behavioral oracles.

VVUQ and scientific exclusions

Passing checks only private implementation behavior supporting the public contract. It
does not make the private class public or establish numerical verification, scientific
validation, uncertainty quantification, physical correctness, or human acceptance.
"""

from __future__ import annotations

import pytest

from ksdft2effmass.harness.pi.wire.canonical_json import _DuplicateKey

pytestmark = pytest.mark.software_verification
SUT = _DuplicateKey


def test_artifact__duplicate_key__retains_value_error_contract() -> None:
    """Evidence ID: software-verification.harness.wire.duplicate-key.construction

    Requirement: Duplicate-key diagnostics retain the rejected key through standard
    ValueError semantics.

    Method: Exercise the private result implementation with one fixed duplicate-key
    spelling.

    Oracle: Python ValueError argument semantics and the strict parser contract.

    Acceptance: ValueError compatibility, the argument tuple, and string value are
    exact.

    Interpretation: Failure identifies exception or diagnostic-value drift.

    Limitations: Construction does not establish parser duplicate detection.
    """
    error = SUT("task_id")
    assert type(error) is SUT
    assert isinstance(error, ValueError)
    assert error.args == ("task_id",)
    assert str(error) == "task_id"
