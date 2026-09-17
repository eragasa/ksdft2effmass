r"""Software verification of ``WorkflowRunCommitBinding``.

Bounded artifact scope: intrinsic durable transaction/key/writer labels.

Evidence profile: claim_bearing

Facet and represented meaning

The binding preserves three independently meaningful exact labels for future bytes.

Intrinsic and cross-object scope

Only record invariants are tested, not repository confirmation or receipt derivation.

VVUQ and scientific exclusions

Software verification only; no persistence, execution, scientific validation
or authority.
"""

from dataclasses import FrozenInstanceError, replace

import pytest
from ksdft2effmass.workflows import WorkflowRunCommitBinding

pytestmark = pytest.mark.software_verification
SUT = WorkflowRunCommitBinding


class TestWorkflowRunCommitBinding:
    """Intrinsic immutable durable labels, with no inferred receipt evidence."""

    @staticmethod
    def make_binding() -> WorkflowRunCommitBinding:
        return WorkflowRunCommitBinding(
            transaction_identity="transaction",
            commit_idempotency_identity="key",
            persistence_implementation_identity="historical-writer:9",
        )

    def test_constructor__labels__preserves_historical_writer(self) -> None:
        """Evidence ID: SV-WFR-BINDING-001

        Requirement: The durable binding retains caller operation, key and writer.

        Method: Construct directly and inspect the three public fields.

        Oracle: Explicit input labels and the intrinsic record contract.

        Acceptance: All three labels retain exact independent supplied values.

        Interpretation: Construction neither replaces nor recognizes writer support.

        Limitations: Unknown writer support belongs to the future repository.
        """
        value = self.make_binding()
        assert value.transaction_identity == "transaction"
        assert value.commit_idempotency_identity == "key"
        assert value.persistence_implementation_identity == "historical-writer:9"

    @pytest.mark.parametrize(
        "field",
        [
            pytest.param("transaction", id="transaction_label"),
            pytest.param("key", id="commit_key"),
            pytest.param("writer", id="historical_writer"),
        ],
    )
    def test_constructor__labels__rejects_empty(self, field: str) -> None:
        """Evidence ID: SV-WFR-BINDING-002

        Requirement: Empty durable binding labels are invalid.

        Method: Replace one label with an empty exact built-in string.

        Oracle: Nonempty-label intrinsic invariant.

        Acceptance: Each empty exact string raises ValueError.

        Interpretation: All durable labels are required, not inferred defaults.

        Limitations: Lexical validity does not establish a committed operation.
        """
        value = self.make_binding()
        with pytest.raises(ValueError):
            if field == "transaction":
                replace(value, transaction_identity="")
            elif field == "key":
                replace(value, commit_idempotency_identity="")
            else:
                replace(value, persistence_implementation_identity="")

    @pytest.mark.parametrize(
        "invalid",
        [
            pytest.param(True, id="boolean"),
            pytest.param(1, id="integer"),
            pytest.param(b"key", id="bytes"),
        ],
    )
    def test_constructor__labels__rejects_wrong_type(
        self, invalid: bool | int | bytes
    ) -> None:
        """Evidence ID: SV-WFR-BINDING-003

        Requirement: Wrong semantic label types are rejected, not coerced.

        Method: Pass explicit nonstring inputs at the exact intentional invalid call.

        Oracle: Exact built-in string field contract.

        Acceptance: Nonstring operation labels raise TypeError.

        Interpretation: The Python boundary performs no string coercion.

        Limitations: Closed invalid partitions do not enumerate all Python objects.
        """
        with pytest.raises(TypeError):
            WorkflowRunCommitBinding(
                transaction_identity=invalid,  # type: ignore[arg-type]
                commit_idempotency_identity="key",
                persistence_implementation_identity="writer",
            )

    def test_field__transaction_identity__is_immutable(self) -> None:
        """Evidence ID: SV-WFR-BINDING-004

        Requirement: Maintained commit-binding values are immutable.

        Method: Attempt direct field assignment on a constructed record.

        Oracle: Frozen dataclass language semantics and the original input label.

        Acceptance: Assignment raises FrozenInstanceError and original is retained.

        Interpretation: Ordinary callers cannot rewrite durable operation identity.

        Limitations: This is operational immutability, not hostile-memory protection.
        """
        value = self.make_binding()
        with pytest.raises(FrozenInstanceError):
            value.transaction_identity = "replacement"  # type: ignore[misc]
        assert value.transaction_identity == "transaction"
