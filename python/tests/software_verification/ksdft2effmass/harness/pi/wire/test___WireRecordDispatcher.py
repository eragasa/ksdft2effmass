r"""Software verification of private wire-record dispatcher implementation.

Evidence profile: routine

Bounded artifact scope: the module's declared evidence owner.

Facet and represented meaning

Routine software verification of closed-kind wire routing delegated by the public
harness wire boundary. No physical model, mathematical operator, or numerical
representation is represented.

Intrinsic and cross-object scope

The primary owner is the private wire-record dispatcher implementation.
``_WireRecordDispatcher`` is used only as a direct implementation access point; its
name, defining module, constructor, and identity are not public contracts. Fixed
accepted fixtures and exact Python or JSON semantics are the behavioral oracles.

VVUQ and scientific exclusions

Passing checks only private implementation behavior supporting the public contract. It
does not make the private class public or establish numerical verification, scientific
validation, uncertainty quantification, physical correctness, or human acceptance.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from ksdft2effmass.harness.pi.wire.dispatch import _WireRecordDispatcher

pytestmark = pytest.mark.software_verification
SUT = _WireRecordDispatcher
ROOT = Path(__file__).resolve().parents[7]


def test_artifact__dependency__wire_modules_have_explicit_owners() -> None:
    """Evidence ID: software-verification.harness.wire.dependency.explicit-decomposition

    Requirement: The wire package has one explicit module owner for canonical JSON,
    each supported domain mapping, common records, and dispatch.

    Method: Enumerate the maintained Python modules directly below the wire package.

    Oracle: The active R2.5 Task contract fixes the complete bounded module layout.

    Acceptance: The observed module names equal the eight contract-selected names.

    Interpretation: Failure identifies missing, extra, or misplaced wire ownership.

    Limitations: Module presence does not establish dependency direction or behavior.
    """
    package = ROOT / "python/src/ksdft2effmass/harness/pi/wire"
    expected_modules = {
        "__init__.py",
        "canonical_json.py",
        "checkpoints.py",
        "dispatch.py",
        "human_review.py",
        "records.py",
        "resources.py",
        "tasks.py",
    }
    assert {path.name for path in package.glob("*.py")} == expected_modules


def test_artifact__dependency__dispatch_is_routing_only() -> None:
    """Evidence ID: software-verification.harness.wire.dependency.thin-dispatch

    Requirement: Dispatch owns only explicit routing, without field mappings or
    persistence operations.

    Method: Parse dispatch.py and inspect its module-level functions, dictionary
    construction, referenced names, and referenced attributes.

    Oracle: The R2.5 contract fixes one private routing ActionObject with encode,
    decode, and supports methods, leaving domain mapping and SQLite ownership elsewhere.

    Acceptance: Dispatch defines only _WireRecordDispatcher; its routing methods contain
    no dictionary construction or listed SQLite connection, execution, or transaction
    operations.

    Interpretation: Failure identifies domain mechanism or persistence leakage into
    dispatch.

    Limitations: This structural check does not establish routing result correctness.
    """
    path = ROOT / "python/src/ksdft2effmass/harness/pi/wire/dispatch.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
    assert [node.name for node in classes] == ["_WireRecordDispatcher"]
    methods = [
        node
        for node in classes[0].body
        if isinstance(node, ast.FunctionDef) and node.name != "__init__"
    ]
    assert {node.name for node in methods} == {"encode", "decode", "supports"}
    assert not any(
        isinstance(node, ast.Dict) for method in methods for node in ast.walk(method)
    )
    names = {
        node.id
        for method in methods
        for node in ast.walk(method)
        if isinstance(node, ast.Name)
    }
    attributes = {
        node.attr
        for method in methods
        for node in ast.walk(method)
        if isinstance(node, ast.Attribute)
    }
    persistence_operations = {
        "sqlite3",
        "connect",
        "execute",
        "executemany",
        "executescript",
        "commit",
        "rollback",
    }
    assert names.isdisjoint(persistence_operations)
    assert attributes.isdisjoint(persistence_operations)


def test_artifact__dependency__validation_owns_public_wire_actions() -> None:
    """Evidence ID: software-verification.harness.wire.dependency.public-facade

    Requirement: validation.py remains the source owner of the accepted public wire
    Actions while delegating codec mechanics to the wire subpackage.

    Method: Parse validation.py and collect its module-level class definitions.

    Oracle: The accepted compatibility contract assigns JsonRecordSerializer and
    JsonRecordDeserializer to validation.py.

    Acceptance: Both exact public ActionObject class names are defined by validation.py.

    Interpretation: Failure identifies public Action ownership or compatibility drift.

    Limitations: Class ownership does not establish execute-signature or runtime
    behavior, which remain covered by their class-owned test modules.
    """
    path = ROOT / "python/src/ksdft2effmass/harness/pi/validation.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    classes = {node.name for node in tree.body if isinstance(node, ast.ClassDef)}
    assert {"JsonRecordSerializer", "JsonRecordDeserializer"} <= classes


def test_artifact__routing__routes_closed_union() -> None:
    """Evidence ID: software-verification.harness.wire.record-dispatcher.routing

    Requirement: Dispatch routes explicit wire kinds without inference or registration.

    Method: Decode a caller-selected resource kind, re-encode it, and query support.

    Oracle: The accepted resource-reference fixture and closed-union contract.

    Acceptance: Mapping is exact, the decoded record is supported, and object is not.

    Interpretation: Failure identifies routing or closed-union drift.

    Limitations: Complete public behavior remains covered by the public Action tests.
    """
    path = (
        Path(__file__).resolve().parents[7]
        / "harness/pi/fixtures/valid/resource-reference.json"
    )
    obj = json.loads(path.read_text())
    dispatcher = SUT()
    record = dispatcher.decode("ResourceReference", obj)
    assert dispatcher.encode(record) == obj
    assert dispatcher.supports(record)
    assert not dispatcher.supports(object())
