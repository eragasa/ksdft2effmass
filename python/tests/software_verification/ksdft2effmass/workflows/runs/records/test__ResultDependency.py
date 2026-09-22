r"""Software verification of ``ResultDependency``.

Evidence profile: routine

Bounded artifact scope: the public ``ResultDependency`` contract.

Facet and represented meaning

This module verifies the exact public structure owned by ``ResultDependency``.

Intrinsic and cross-object scope

The evidence is limited to the class-owned field, member, or constructor contract.
Cross-record replay and package-export agreement remain with their owning evidence.

VVUQ and scientific exclusions

This is software verification only. It establishes no execution, persistence,
scientific validation, uncertainty quantification, authority, or human acceptance.
"""

from dataclasses import fields

import pytest

from ksdft2effmass.workflows.runs import ResultDependency

pytestmark = pytest.mark.software_verification
SUT = ResultDependency


class TestResultDependency:
    """Own software evidence for ``ResultDependency``."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose the exact documented immutable field inventory.

        Evidence ID: SV-WFR-RESULT-DEPENDENCY-001

        Requirement: ``ResultDependency`` declares exactly its documented public
        DataObject
        or ResultObject fields in constructor order.

        Acceptance: :func:`dataclasses.fields` returns the exact field-name tuple.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "result_reference_identity",
            "producer_workflow_run_identity",
            "consumer_workflow_run_identity",
            "consumer_task_instance_identity",
            "consumer_activation_identity",
            "input_name",
        )
