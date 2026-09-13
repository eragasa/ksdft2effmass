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

from ksdft2effmass.harness.pi.conformance.python.parser import PythonTestModuleParser

SUT = PythonTestModuleParser


class TestPythonTestModuleParser:
    """Verify class-owned callable discovery at the parser boundary."""

    def test_method__execute__class_owned_methods_returns_complete_function_facts(
        self,
    ) -> None:
        """Evidence ID: SV-PY-CONFORMANCE-PARSER-CLASS-001

        Requirement: Maintained tests grouped beneath an explicit ``Test...`` owner
        are visible to opt-in downstream conformance without changing the legacy
        top-level parser surface.

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
        compatibility_model = SUT.execute(path, payload)
        model = SUT.execute_class_owned(path, payload)

        assert compatibility_model.functions == ()
        assert tuple(function.name for function in model.functions) == (
            "test_execute__valid_case__returns_value",
            "expected_value",
        )
        assert model.functions[0].is_test
        assert model.functions[0].has_loop
        assert not model.functions[1].is_test
