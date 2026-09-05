r"""Software verification of ``ImportedRetainedResultProducer``.

Evidence profile: routine

Bounded artifact scope: the public ``ImportedRetainedResultProducer`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by
``ImportedRetainedResultProducer``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import ImportedRetainedResultProducer

pytestmark = pytest.mark.software_verification
SUT = ImportedRetainedResultProducer


class TestImportedRetainedResultProducer:
    """Own software evidence for ``ImportedRetainedResultProducer``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-IMPORTED-RETAINED-RESULT-PRODUCER-001

        Requirement: ``ImportedRetainedResultProducer`` declares exactly its
        documented public DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "source_identity",
            "evidence_identities",
            "limitations",
        )
