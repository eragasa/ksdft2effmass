r"""Software verification of ``PythonTestModuleParser``.

Evidence profile: routine

Bounded artifact scope: class-owned test-method discovery from exact Python source.

Facet and represented meaning

The parser represents direct test and helper methods beneath explicit pytest owner
classes as immutable function facts.

Intrinsic and cross-object scope

The evidence covers discovery and classification only. Repository-level conformance
policy remains owned by the composed validator.

VVUQ and scientific exclusions

The synthetic Python source is test data. This module establishes no numerical
verification, scientific validation, uncertainty quantification, or human acceptance.
"""

import pytest

from ksdft2effmass.harness.pi.conformance.python.model import (
    PythonTestOwnerDiscoveryMode,
)
from ksdft2effmass.harness.pi.conformance.python.parser import PythonTestModuleParser

SUT = PythonTestModuleParser


class TestPythonTestModuleParser:
    """Verify class-owned callable discovery at the parser boundary."""

    def test_method__execute__class_owned_methods_returns_complete_function_facts(
        self,
    ) -> None:
        """Evidence ID: SV-PY-CONFORMANCE-PARSER-CLASS-001

        Requirement: Maintained tests grouped beneath an explicit ``Test...`` owner
        are visible to the canonical parser with their owner-qualified identity.

        Method: Parse synthetic source containing one test method with a loop and one
        static helper method directly beneath a top-level pytest owner class.

        Acceptance: Both methods are returned in source order, the test is classified
        as a test, and its loop is observable.
        """
        payload = b'''"""Synthetic maintained evidence."""

class TestExample:
    def test_execute__valid_case__returns_value(self) -> None:
        """Evidence ID: SYNTHETIC-001"""
        for value in (1,):
            assert value == 1

    @staticmethod
    def expected_value() -> int:
        """Return synthetic expected data."""
        return 1
'''

        path = "python/tests/software_verification/example/test__Example.py"
        model = SUT.execute_with_test_owner(path, payload)
        compatibility_model = SUT.execute_class_owned(path, payload)

        assert compatibility_model == model
        assert (
            model.test_owner_discovery_mode is PythonTestOwnerDiscoveryMode.TEST_OWNER
        )
        assert tuple(function.name for function in model.functions) == (
            "test_execute__valid_case__returns_value",
            "expected_value",
        )
        assert tuple(function.owner_class_name for function in model.functions) == (
            "TestExample",
            "TestExample",
        )
        assert tuple(function.owner_node_name for function in model.functions) == (
            "TestExample::test_execute__valid_case__returns_value",
            "TestExample::expected_value",
        )
        assert model.functions[0].is_test
        assert model.functions[0].has_loop
        assert not model.functions[1].is_test

    def test_method__execute__missing_test_owner_class__raises_syntax_error(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.parser.missing-owner.rejected

        Requirement: Normal test-owner discovery rejects an unlisted module-level
        test instead of silently retaining compatibility behavior.

        Method: Parse synthetic source containing only one module-level test.

        Acceptance: Parsing raises ``SyntaxError``.
        """
        payload = b"def test_artifact__legacy__case() -> None:\n    pass\n"

        with pytest.raises(SyntaxError):
            SUT.execute_with_test_owner("python/tests/test__missing_owner.py", payload)

    def test_method__execute__multiple_test_owner_classes__raises_syntax_error(
        self,
    ) -> None:
        """Evidence ID: software-verification.harness.parser.multiple-owners.rejected

        Requirement: Multiple top-level ``Test...`` classes fail closed rather than
        creating ambiguous structural pytest ownership.

        Method: Parse synthetic source containing two top-level pytest owner classes.

        Acceptance: Parsing raises ``SyntaxError``.
        """
        payload = b"class TestOne:\n    pass\n\nclass TestTwo:\n    pass\n"

        with pytest.raises(SyntaxError):
            SUT.execute_with_test_owner(
                "python/tests/test__ambiguous_owner.py", payload
            )
