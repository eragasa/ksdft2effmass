# `ksdft2effmass.serialization`

## Purpose and status

This implemented package owns KSD's reusable typed JSON boundary. It converts immutable
scientific values into canonical JSON bytes and reconstructs the same typed values
without domain-specific parsing. The package incubates this capability in KSD until a
separately reviewed migration assigns it to PhysKit.

Source:

```text
python/src/ksdft2effmass/serialization/
├── contracts.py
├── enums.py
├── mapping_json.py
├── records.py
└── typed_values.py
```

## Public contracts

`JsonSerializer`, `JsonDeserializer`, and `JsonCodec` define exact record and wire
shapes. Their wire type is `str` or `bytes`; their record type remains explicit.

`TypedJsonValueCodec` owns recursive normalization for this closed inventory:

- built-in JSON scalars;
- finite NumPy integer, floating-point, and complex scalars;
- fixed-width NumPy arrays through 64-bit real components;
- canonical SciPy CSR arrays;
- PhysKit units and scalar, vector, dense-matrix, and CSR-matrix quantities;
- enums registered by an explicit identifier;
- tuples, lists, string-keyed mappings; and
- records exposing a typed mapping.

`TypedJsonMappingSerializer` and `TypedJsonMappingDeserializer` restrict the codec to a
string-keyed root mapping. `BaseTypedRecord` fixes the public representation pipeline:

```text
to_json → to_dict → TypedJsonMappingSerializer.serialize
from_json → TypedJsonMappingDeserializer.deserialize → from_dict
```

Concrete records implement `_mapping` and `_from_mapping`. They do not override the
final public conversion methods. `StringWireEnum` is a behavior-only ordinary `Enum`
base, not a `StrEnum`: it rejects non-string members when a concrete enum is defined,
concrete domain enums inherit stable `to_wire()` and `from_wire()` conversion, and
records explicitly project members to built-in strings in
`_mapping`, and `_from_mapping` validates an exact string before reconstruction. This
keeps domain vocabulary out of the generic JSON codec and avoids implicit string
admission. Domain enums whose internal values are not their wire labels retain a
separate family-owned bidirectional mapping action instead of inheriting this base.

## Canonical wire behavior

Canonical JSON uses UTF-8, sorted object keys, two-space indentation, a terminating
newline, and rejection of nonstandard floating-point constants. Typed values carry an
explicit `__ksd_type__` tag. The tag key is reserved in caller mappings.

Array records retain dtype, shape, byte order, and exact finite values. Complex arrays
retain independent real and imaginary components. CSR records retain data, column
indices, row offsets, and shape. Deserialization rejects integer overflow, Boolean or
object arrays, malformed CSR offsets and indices, unsupported dtypes, unknown enum
identifiers, duplicate JSON keys, and silent complex-to-real conversion.

## Domain boundary

Serialization owns representation mechanics. Domain records own field inventories,
units, dimensions, ordering, scientific correlations, and admissibility rules.
Filesystem paths, persistence, provenance policy, execution authority, and scientific
interpretation remain with their domain owners.

The PIAB1D successor composes this package directly. It contains no `.tolist()` array
transport and performs no JSON-list reconstruction in the model-system owner.
Historical versioned study serializers retain their exact legacy wire contracts and do
not define the successor architecture.

## Immutability and failure behavior

Deserialized NumPy values and quantity magnitudes are operationally read-only. Mapping
records defensively copy caller input before exposing read-only views. Every malformed
wire value fails at the narrowest owning boundary. No decoder supplies defaults for
missing scientific fields.

## Evidence boundary

Round-trip and malformed-input tests establish software behavior for the declared type
inventory. They do not establish scientific validity of a serialized record, producer
causality, publication status, or evidence acceptance.
