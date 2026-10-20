"""Software verification for :class:`FiniteTranslationDomain`."""

from __future__ import annotations

import pytest

from ksdft2effmass.operators.representations.domains import (
    FiniteDomainABC,
    FiniteTranslationDomain,
)

pytestmark = pytest.mark.software_verification


class TestFiniteTranslationDomain:
    """Establish ordered exact integer-translation inventories."""

    def test_construction__retains_order_dimension_and_uniqueness(self) -> None:
        """Translation vectors are exact ordered integer tuples."""
        domain = FiniteTranslationDomain(
            identifier="symmetric-r1",
            translations=((-1,), (0,), (1,)),
            coordinate_convention_id="integer-cell-translation.v1",
        )

        assert isinstance(domain, FiniteDomainABC)
        assert domain.identity == "symmetric-r1"
        assert domain.cardinality == 3
        assert domain.dimension == 1
        assert domain.translations == ((-1,), (0,), (1,))

    @pytest.mark.parametrize(
        ("translations", "message"),
        [
            pytest.param(((0,), (0,)), "unique", id="duplicate"),
            pytest.param(((0,), (1, 0)), "common dimension", id="dimension"),
            pytest.param(((True,),), "integers", id="boolean"),
            pytest.param((("1",),), "integers", id="numeric_string"),
            pytest.param(((),), "positive dimension", id="empty_vector"),
        ],
    )
    def test_construction__rejects_invalid_inventories(
        self,
        translations: tuple[tuple[int, ...], ...],
        message: str,
    ) -> None:
        """Malformed translation inventories are never canonicalized silently."""
        with pytest.raises((TypeError, ValueError), match=message):
            FiniteTranslationDomain(
                "translations",
                translations,
                "integer-cell-translation.v1",
            )
