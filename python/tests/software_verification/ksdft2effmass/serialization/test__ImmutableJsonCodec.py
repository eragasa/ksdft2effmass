r"""Routine software verification of shared immutable JSON serialization.

Evidence profile: routine

The synthetic tests establish strict one-pass closed-value decoding, recursive
immutability, canonical encoding, exact public types, and binary64 conversion failures.
They do not
assign a schema, scientific identity, provenance, units, validation status, or evidence
acceptance to a JSON document.
"""

from dataclasses import FrozenInstanceError

import pytest

import ksdft2effmass.serialization as serialization_package
from ksdft2effmass.serialization import JsonCodec
from ksdft2effmass.serialization.json import (
    ImmutableJsonArray,
    ImmutableJsonCodec,
    ImmutableJsonObject,
    JsonValue,
    StrictJsonDecoder,
)

pytestmark = pytest.mark.software_verification
SUT = ImmutableJsonCodec


class TestImmutableJsonCodec:
    """Own routine evidence for the shared immutable JSON boundary."""

    def test_types__are_exact_recursive_immutable_values(self) -> None:
        """Evidence ID: SV-SERIALIZATION-IMMUTABLE-JSON-001.

        Requirement: Immutable JSON containers accept only exact immutable recursive
        representations with canonical unique object keys.

        Acceptance: Valid nested values are frozen and slotted; mutable/subtyped
        containers, unordered or duplicate keys, unsupported values, and nonfinite
        floats fail closed.
        """
        assert ImmutableJsonCodec.__module__ == (
            "ksdft2effmass.serialization.json.immutable"
        )
        assert not hasattr(serialization_package, "ImmutableJsonCodec")
        nested = ImmutableJsonObject(
            (
                ("array", ImmutableJsonArray((None, False, 3, 1.25, "value"))),
                ("object", ImmutableJsonObject((("key", "value"),))),
            )
        )
        assert nested.field("array") == ImmutableJsonArray(
            (None, False, 3, 1.25, "value")
        )
        with pytest.raises(FrozenInstanceError):
            nested.fields = ()  # type: ignore[misc]
        with pytest.raises((AttributeError, TypeError)):
            nested.extra = "forbidden"  # type: ignore[attr-defined]

        class TupleSubclass(tuple[object, ...]):
            """Provide a tuple subtype outside the exact container contract."""

        with pytest.raises(TypeError, match="values must be an exact tuple"):
            ImmutableJsonArray(TupleSubclass())  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="fields must be an exact tuple"):
            ImmutableJsonObject(TupleSubclass())  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="exact key-value tuple"):
            ImmutableJsonObject((("key", "value"), ["other", 2]))  # type: ignore[list-item]
        with pytest.raises(ValueError, match="unique and lexically ordered"):
            ImmutableJsonObject((("z", 1), ("a", 2)))
        with pytest.raises(ValueError, match="unique and lexically ordered"):
            ImmutableJsonObject((("a", 1), ("a", 2)))
        with pytest.raises(TypeError, match="immutable JSON value"):
            ImmutableJsonArray(([],))  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="must be finite"):
            ImmutableJsonArray((float("inf"),))

    def test_decoder__rejects_non_strict_or_erased_wires(self) -> None:
        """Evidence ID: SV-SERIALIZATION-IMMUTABLE-JSON-002.

        Requirement: Wire decoding must preserve strict JSON boundaries before immutable
        adaptation.

        Acceptance: Duplicate keys, nonfinite extensions, malformed UTF-8, non-object
        roots, and bytes subtypes are rejected.
        """
        codec = SUT()
        assert not hasattr(codec, "decoder")

        class BytesSubclass(bytes):
            """Provide a bytes subtype outside the exact wire contract."""

        with pytest.raises(TypeError, match="payload must be bytes"):
            codec.deserialize(BytesSubclass(b"{}"))
        with pytest.raises(ValueError, match="duplicate JSON key"):
            codec.deserialize(b'{"a":1,"a":2}')
        with pytest.raises(ValueError, match="non-finite JSON constant"):
            codec.deserialize(b'{"value":NaN}')
        with pytest.raises(ValueError, match="strict UTF-8 JSON"):
            codec.deserialize(b"\xff")
        with pytest.raises(TypeError, match="root must be a JSON object"):
            codec.deserialize(b"[]")

    def test_codec__round_trips_complete_meaning_canonically(self) -> None:
        """Evidence ID: SV-SERIALIZATION-IMMUTABLE-JSON-003.

        Requirement: One shared codec must retain every closed JSON value immutably and
        emit deterministic canonical bytes without preserving source formatting.

        Acceptance: The complete tree is lexically ordered, canonical bytes are exact,
        decoding those bytes preserves the tree, and built-in conversion is defensive.
        """
        source = (
            b'{ "z": [null, true, 2, 3.5, "text", {"b": 1}], "a": {"nested": false} }\n'
        )
        codec = SUT()

        root = codec.deserialize(source)
        canonical = codec.serialize(root)
        builtins = codec.builtin_value(root)

        assert isinstance(codec, JsonCodec)
        assert tuple(key for key, _ in root.fields) == ("a", "z")
        assert canonical == (
            b'{"a":{"nested":false},"z":[null,true,2,3.5,"text",{"b":1}]}\n'
        )
        assert codec.deserialize(canonical) == root
        assert type(builtins) is dict
        builtins["changed"] = True
        assert tuple(key for key, _ in root.fields) == ("a", "z")
        with pytest.raises(TypeError, match="record must be ImmutableJsonObject"):
            codec.serialize(ImmutableJsonArray(()))  # type: ignore[arg-type]

    def test_decoder__reports_unrepresentable_binary64_conversion(self) -> None:
        """Evidence ID: SV-SERIALIZATION-IMMUTABLE-JSON-004.

        Requirement: Generic JSON integers remain exact until an explicit binary64
        conversion, which must fail closed outside binary64 range.

        Acceptance: The immutable tree retains an arbitrarily large integer exactly,
        while the explicit real adapter raises ``OverflowError``.
        """
        huge = 10**400
        root = SUT().deserialize(f'{{"huge":{huge}}}'.encode())

        assert root.field("huge") == huge
        with pytest.raises(OverflowError):
            StrictJsonDecoder.real(huge, "huge")

    def test_decoder__adapts_after_one_recursive_validation_pass(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Evidence ID: SV-SERIALIZATION-IMMUTABLE-JSON-005.

        Requirement: Immutable adaptation must consume the already validated JSON tree
        without recursively revalidating every nested subtree.

        Acceptance: A deeply nested object causes exactly one top-level strict mapping
        validation before immutable adaptation.
        """
        mapping_calls = 0
        original_mapping = StrictJsonDecoder.mapping

        def counting_mapping(
            decoder: StrictJsonDecoder, value: object, name: str
        ) -> dict[str, JsonValue]:
            nonlocal mapping_calls
            mapping_calls += 1
            return original_mapping(decoder, value, name)

        monkeypatch.setattr(StrictJsonDecoder, "mapping", counting_mapping)
        depth = 40
        wire = b'{"nested":' * depth + b"0" + b"}" * depth

        root = SUT().deserialize(wire)

        assert type(root) is ImmutableJsonObject
        assert mapping_calls == 1

    def test_adapter__converts_validated_tree_without_redecoding(self) -> None:
        """Evidence ID: SV-SERIALIZATION-IMMUTABLE-JSON-006.

        Requirement: Schema decoders can adapt an already strict-decoded object into an
        immutable snapshot without a second wire parse or recursive strict validation.

        Acceptance: Public object/value adaptation preserves exact scalar distinctions
        and produces the same immutable object as direct wire deserialization.
        """
        wire = b'{"boolean":true,"integer":1,"nested":[{"value":2.5}]}'
        decoded = StrictJsonDecoder().document(wire)
        codec = SUT()

        adapted = codec.immutable_object(decoded)

        assert adapted == codec.deserialize(wire)
        assert codec.immutable_value(decoded["boolean"]) is True
        assert type(codec.immutable_value(decoded["integer"])) is int
