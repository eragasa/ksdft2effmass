r"""Software verification of private decoded-wire value implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of structural decoded-JSON conversion delegated by the
private harness wire codecs. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private decoded-wire value implementation.
``_WireValueDecoder`` is used only as a direct implementation access point; its name,
defining module, constructor, and identity are not public contracts. Exact Python and
JSON structural semantics are the behavioral oracles.

VVUQ and scientific exclusions

Passing checks only private implementation behavior supporting the public wire
contract. It does not make the private class public or establish numerical
verification, scientific validation, uncertainty quantification, physical correctness,
or human acceptance.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.wire.records import _WireValueDecoder

pytestmark = pytest.mark.software_verification
SUT = _WireValueDecoder
ROOT = Path(__file__).resolve().parents[7]


def test_artifact__decoded_values__enforces_structural_conversion() -> None:
    """Evidence ID: software-verification.harness.wire.value-decoder.contract

    Requirement: Decoded JSON values are frozen and structurally checked before record
    construction.

    Method: Exercise recursive array freezing, object and array admission, and exact
    field-set validation.

    Oracle: Exact Python container semantics and the accepted strict wire contract.

    Acceptance: Arrays become nested tuples, valid structures are returned unchanged,
    and invalid structures or field sets raise their exact exception families.

    Interpretation: Failure identifies decoded-value conversion or strictness drift.

    Limitations: Domain record construction remains covered by each domain codec test.
    """
    values = SUT()
    assert values.freeze([1, [2, 3]]) == (1, (2, 3))
    obj = {"schema_version": 1}
    assert values.record_object(obj) is obj
    array = [1, 2]
    assert values.array(array, "items") is array
    values.require_fields(obj, ("schema_version",))

    with pytest.raises(TypeError, match="nested wire record must be an object"):
        values.record_object([])
    with pytest.raises(TypeError, match="items must be a JSON array"):
        values.array((), "items")
    with pytest.raises(KeyError, match="unknown:extra"):
        values.require_fields({"schema_version": 1, "extra": 2}, ("schema_version",))
    with pytest.raises(KeyError, match="missing:schema_version"):
        values.require_fields({}, ("schema_version",))


def test_artifact__dependency__wire_helpers_have_explicit_class_owners() -> None:
    """Evidence ID: software-verification.harness.wire.dependency.no-dangling-functions

    Requirement: New wire decomposition behavior has explicit class ownership rather
    than module-level helper functions.

    Method: Parse every wire-package module and validation.py, collecting module-level
    function definitions introduced by the decomposition.

    Oracle: The active R2.5 Task contract and current human direction require explicit
    owners for wire mechanics and permit no dangling wire helper functions.

    Acceptance: Wire-package modules define no module-level functions, and validation.py
    defines no module-level ``_is_wire_record`` helper.

    Interpretation: Failure identifies wire behavior left outside its owning class.

    Limitations: This structural check does not establish runtime codec behavior or
    whether unchanged validation helpers have appropriate historical ownership.
    """
    package = ROOT / "python/src/ksdft2effmass/harness/pi/wire"
    wire_package_module_functions = {
        path.name: tuple(
            node.name
            for node in ast.parse(path.read_text(encoding="utf-8")).body
            if isinstance(node, ast.FunctionDef)
        )
        for path in package.glob("*.py")
    }
    assert wire_package_module_functions == {
        "__init__.py": (),
        "canonical_json.py": (),
        "checkpoints.py": (),
        "dispatch.py": (),
        "human_review.py": (),
        "records.py": (),
        "resources.py": (),
    }

    validation_path = ROOT / "python/src/ksdft2effmass/harness/pi/validation.py"
    validation_tree = ast.parse(validation_path.read_text(encoding="utf-8"))
    validation_function_names = {
        node.name for node in validation_tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "_is_wire_record" not in validation_function_names
