"""Evidence class and represented meaning
Software verification of the exact manifest lifecycle-state enum artifact.
Owned contract, oracle, and scope
ManifestState is the SUT; the accepted version-1 lifecycle vocabulary is the oracle.
VVUQ and scientific exclusions
Evidence excludes execution, solver acceptance, numerical verification, scientific
validation, UQ, physical correctness, and cross-language conformance.
"""

import pytest

from ksdft2effmass.provenance import ManifestState

SUT = ManifestState
pytestmark = pytest.mark.software_verification


def test_artifact__enum_values__matches_exact_manifest_lifecycle_vocabulary() -> None:
    """Evidence ID
    SV-PROV-075
    Requirement
    Public manifest states are exactly declared, complete, and failed.
    Method
    Enumerate public names and values without constructing or executing a manifest.
    Oracle
    The accepted version-1 lifecycle artifact fixes exact ordered names and values.
    Acceptance
    Names and lowercase values match the fixed tuples exactly.
    Interpretation
    Failure indicates public/schema lifecycle vocabulary drift.
    Limitations
    COMPLETE is not solver convergence, scientific validation, UQ, or human acceptance.
    """
    assert tuple(item.name for item in SUT) == ("DECLARED", "COMPLETE", "FAILED")
    assert tuple(item.value for item in SUT) == ("declared", "complete", "failed")
