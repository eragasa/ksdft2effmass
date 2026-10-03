r"""Software verification of nominal ``AbstractResultObject`` membership."""

import inspect
from dataclasses import dataclass, field

import pytest

from ksdft2effmass.workflows import AbstractResultObject, ResultObjectIdentity

pytestmark = pytest.mark.software_verification


class TestAbstractResultObject:
    """Verify explicit nominal result membership without structural fallback."""

    def test_nominal_subclass_satisfies_boundary(self) -> None:
        """Accept a frozen result that explicitly inherits the result ABC.

        Evidence ID: SV-WFM-ABSTRACT-RESULT-OBJECT-001
        """

        @dataclass(frozen=True, slots=True)
        class ConcreteResult(AbstractResultObject):
            identity: ResultObjectIdentity = field()

        result = ConcreteResult(ResultObjectIdentity("result.one"))
        assert isinstance(result, AbstractResultObject)
        assert not inspect.isabstract(ConcreteResult)

    def test_structural_lookalike_is_rejected(self) -> None:
        """Reject an independent class with the same attribute spelling.

        Evidence ID: SV-WFM-ABSTRACT-RESULT-OBJECT-002
        """

        @dataclass(frozen=True, slots=True)
        class ResultLookalike:
            identity: ResultObjectIdentity

        value = ResultLookalike(ResultObjectIdentity("result.lookalike"))
        assert not isinstance(value, AbstractResultObject)
