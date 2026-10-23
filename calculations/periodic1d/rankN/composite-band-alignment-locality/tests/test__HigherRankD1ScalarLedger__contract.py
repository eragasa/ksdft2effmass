"""Software verification for the higher-rank D1 scalar ledger value."""

from __future__ import annotations

import pytest
from workflow import (
    HigherRankD1ScalarLedger,
    HigherRankD1ScalarLedgerEntry,
)

pytestmark = pytest.mark.software_verification


class TestHigherRankD1ScalarLedger:
    """Establish immutable ordered path/value semantics."""

    def test_value__retains_order_and_exact_path_lookup(self) -> None:
        """The ledger retains deterministic order and exact scalar lookup."""
        ledger = HigherRankD1ScalarLedger(
            (
                HigherRankD1ScalarLedgerEntry("/first", 1.0),
                HigherRankD1ScalarLedgerEntry("/second", 2.0),
            )
        )

        assert ledger.paths == ("/first", "/second")
        assert ledger.value("/first") == 1.0
        assert ledger.value("/second") == 2.0
        with pytest.raises(KeyError):
            ledger.value("/absent")

    def test_with_prefix__returns_new_immutable_ledger(self) -> None:
        """Prefixing preserves values and leaves the original ledger unchanged."""
        ledger = HigherRankD1ScalarLedger(
            (HigherRankD1ScalarLedgerEntry("/metric", 3.0),)
        )

        prefixed = ledger.with_prefix("/channels/A0")

        assert ledger.paths == ("/metric",)
        assert prefixed.paths == ("/channels/A0/metric",)
        assert prefixed.value("/channels/A0/metric") == 3.0

    def test_attributes__reject_duplicate_paths(self) -> None:
        """A retained path identifies exactly one scalar."""
        duplicate = HigherRankD1ScalarLedgerEntry("/metric", 1.0)

        with pytest.raises(ValueError, match="paths must be unique"):
            HigherRankD1ScalarLedger((duplicate, duplicate))
