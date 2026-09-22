r"""Software verification of ``ScientificExecutionAuthoritySnapshot``.

Evidence profile: routine

Bounded artifact scope: the public immutable authority-snapshot DataObject.

Facet and represented meaning

This module verifies exact fields, UTC bounds, and immutable snapshot state.

Intrinsic and cross-object scope

Intrinsic snapshot invariants belong here; grant compatibility belongs to the
authorizer.

VVUQ and scientific exclusions

This is software verification only. It performs no authentication, authority-source
access, execution, scientific validation, uncertainty quantification, or acceptance.
"""

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime

import pytest

from ksdft2effmass.workflows import ScientificExecutionAuthoritySnapshot

from .resources.scenarios import ControlScenarioFactory

pytestmark = pytest.mark.software_verification
SUT = ScientificExecutionAuthoritySnapshot


class TestScientificExecutionAuthoritySnapshot:
    """Own software evidence for the immutable authority snapshot."""

    def test_fields__public_contract__matches_exact_inventory(self) -> None:
        """Expose every documented authority-source correlation and time bound.

        Evidence ID: SV-WCI-AUTHORITY-SNAPSHOT-001

        Requirement: The snapshot exposes exactly its documented fields.

        Acceptance: ``dataclasses.fields`` returns the exact constructor order.
        """
        assert tuple(field.name for field in fields(SUT)) == (
            "identity",
            "source_identity",
            "issuer_identity",
            "trust_configuration_identity",
            "content_verification_identity",
            "authentication_verification_identity",
            "predecessor_closure_identity",
            "revocation_closure_identity",
            "content_verification",
            "authentication_verification",
            "predecessor_closure",
            "revocation_closure",
            "valid_from",
            "valid_until",
            "verified_at",
            "fresh_until",
            "resolver_implementation_identity",
        )

    def test_constructor__time_bounds__require_utc_order_and_immutability(
        self,
    ) -> None:
        """Reject naive times and prohibit mutation of represented checks.

        Evidence ID: SV-WCI-AUTHORITY-SNAPSHOT-002

        Requirement: Snapshot times are ordered timezone-aware UTC values and the
        represented snapshot is immutable.

        Acceptance: A naive replacement raises ``ValueError`` and field assignment
        raises ``FrozenInstanceError``.
        """
        snapshot = ControlScenarioFactory.snapshot()
        with pytest.raises(ValueError):
            replace(snapshot, verified_at=datetime(2026, 1, 1, 1))
        with pytest.raises(FrozenInstanceError):
            snapshot.source_identity = "changed"  # type: ignore[misc]
