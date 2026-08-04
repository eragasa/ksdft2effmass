"""Evidence class and represented meaning
--------------------------------------
Software verification of the Workflow CPN Python public import/API surface, a runtime
software artifact rather than a physical or numerical model.

Owned contract, oracle, and scope
---------------------------------
The Workflow CPN Python public import/API surface is the primary artifact owner. Its
approved Python export contract is the exact runtime oracle within version 1 scope.

VVUQ and scientific exclusions
------------------------------
Passing confirms only the inspected Python API contract; failure indicates contract or
evidence drift. Numerical verification, scientific validation, uncertainty
quantification, physical correctness, engine execution, persistence, and cross-language
conformance are excluded."""

import pytest

import ksdft2effmass.workflows.cpn as cpn

pytestmark = pytest.mark.software_verification


def test_artifact__public_api__exposes_approved_export_inventory() -> None:
    """Evidence ID
    SV-CPN-023

    Requirement
    The Workflow CPN package exposes the approved 49-name sorted, unique, resolvable
    public export surface.

    Method
    Inspect the public ``__all__`` sequence and resolve every listed public attribute;
    no warnings are expected.

    Oracle
    The accepted package contract fixes cardinality 49, sorted uniqueness, and
    name-to-object identity.

    Acceptance
    The sequence has length 49, equals its sorted set, and every resolved object has the
    listed ``__name__``.

    Interpretation
    Pass supports the exercised public API surface; failure may arise from package or
    evidence-contract drift.

    Limitations
    An independent fixed 49-name inventory is not asserted. Import topology, runtime
    behavior, scientific validation, UQ, and cross-language claims are excluded."""
    assert len(cpn.__all__) == 49
    assert cpn.__all__ == sorted(set(cpn.__all__))
    for name in cpn.__all__:
        assert getattr(cpn, name).__name__ == name
