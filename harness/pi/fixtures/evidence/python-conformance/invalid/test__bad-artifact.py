"""Software verification of a bad artifact.

Evidence class and represented meaning
This deliberately uses a superseded heading.
Owned contract, oracle, and scope
This deliberately uses a second superseded heading.
VVUQ and scientific exclusions
This controlled fixture is invalid evidence.
"""
import pytest

def _helper_1():
    """Undocumented private helper."""

@pytest.mark.parametrize("value", [pytest.param(1, id="case_1"), pytest.param(2, id="bad id"), pytest.param(3)])
def test_equality(value):
    """Evidence ID: BAD-001"""
    for item in (value, value):
        assert item == value
