"""Artifact-owned verification of the public CPN package contract.

Evidence class: software verification. The tests use synthetic contract artifacts and
independent language/runtime or static-structure oracles. Passing is not numerical
verification, scientific validation, uncertainty quantification, engine execution,
persistence, or Rust conformance evidence.
"""

import pytest

import ksdft2effmass.workflows.cpn as cpn

pytestmark = pytest.mark.software_verification


def test_cpn_sv_p1_023_public_export_inventory() -> None:
    """SV-CPN-023: verify the fixed public package export inventory.

    Requirement: the package exposes exactly the approved 49 sorted unique names.
    Method: inspect public ``__all__`` and resolve every export. Oracle: approved
    package inventory cardinality plus name/class identity. Acceptance requires all
    equalities. Failure signals public-contract drift. Import topology is separate.
    """
    assert len(cpn.__all__) == 49
    assert cpn.__all__ == sorted(set(cpn.__all__))
    for name in cpn.__all__:
        assert getattr(cpn, name).__name__ == name
