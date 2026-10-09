# Immutable JSON serialization

## Purpose

`ksdft2effmass.serialization.json.immutable` owns a reusable, recursively immutable
representation of JSON values and deterministic conversion between a top-level JSON
object and UTF-8 bytes.

The reviewed import route is:

```python
from ksdft2effmass.serialization.json import (
    ImmutableJsonArray,
    ImmutableJsonCodec,
    ImmutableJsonObject,
    ImmutableJsonScalar,
    ImmutableJsonValue,
)
```

These names are not flattened into the root `ksdft2effmass.serialization` facade.
Domain packages compose this library rather than renaming or aliasing its types.

## Value contract

`ImmutableJsonArray` owns an exact tuple of immutable JSON values.
`ImmutableJsonObject` owns an exact tuple of key-value tuples with unique built-in
string keys in lexical order. The recursive value set is closed to:

- JSON null;
- exact built-in Boolean, integer, finite float, and string scalars;
- `ImmutableJsonArray`; and
- `ImmutableJsonObject`.

Mutable containers, tuple subclasses, unsupported values, duplicate or unordered object
keys, and nonfinite floats fail closed. Generic JSON integers remain exact Python
integers. Conversion to binary64 is a separate explicit operation and raises
`OverflowError` when the integer lies outside binary64 range.

## Codec contract

`ImmutableJsonCodec.deserialize` delegates syntax and primitive checks to
`StrictJsonDecoder`, then constructs a complete immutable object tree. It rejects:

- nonexact byte inputs;
- malformed UTF-8 or JSON;
- duplicate object keys;
- `NaN` and infinity extensions; and
- non-object document roots.

`ImmutableJsonCodec.immutable_value` and `immutable_object` adapt a closed tree already
validated by `StrictJsonDecoder` without a second wire parse or recursive strict
validation pass. This public composition boundary lets schema-specific decoders retain
exact immutable snapshots while performing typed field adaptation from the same decoded
tree.

`ImmutableJsonCodec.serialize` accepts an exact `ImmutableJsonObject` and emits compact,
sorted, newline-terminated UTF-8 JSON with `allow_nan=False`. Encoding and decoding are
linear in the number of JSON values and require memory proportional to the complete
in-memory tree and wire. `MemoryError` can occur for resource-exhausting inputs, and
`RecursionError` can occur when nesting exceeds the Python parser or adapter recursion
depth. No additional arbitrary size cap is imposed.

Canonical bytes preserve JSON meaning but need not preserve source whitespace or source
object-field order. Exact historical bytes therefore remain the responsibility of an
encoded-document owner when byte identity matters.

## Evidence

Routine class-owned evidence resides at:

```text
python/tests/software_verification/ksdft2effmass/serialization/test__ImmutableJsonCodec.py
```

Evidence IDs:

- `SV-SERIALIZATION-IMMUTABLE-JSON-001` — exact recursive immutable containers;
- `SV-SERIALIZATION-IMMUTABLE-JSON-002` — strict wire rejection;
- `SV-SERIALIZATION-IMMUTABLE-JSON-003` — complete canonical round trip and defensive
  built-in conversion; and
- `SV-SERIALIZATION-IMMUTABLE-JSON-004` — exact large-integer retention and explicit
  binary64 overflow; and
- `SV-SERIALIZATION-IMMUTABLE-JSON-005` — one recursive strict-validation pass before
  immutable adaptation; and
- `SV-SERIALIZATION-IMMUTABLE-JSON-006` — public adaptation of an already validated tree
  without wire redecoding.

## Claim boundary

The library assigns no schema, scientific identity, model, basis, gauge, units, state
space, represented operator, result kind, source-file presence, provenance, validation,
uncertainty, or acceptance. It does not access the filesystem or infer meaning from a
path, filename, identifier, shape, or digest.
