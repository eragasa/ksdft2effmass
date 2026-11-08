# Certification implementation

## Layering

The package uses proposition-specific leaves rather than a universal certificate base,
registry, or engine protocol. The current leaf is:

```text
certifications/
  periodic1d/
    rank1/
      first_passing_support/
        records.py
        validation.py
```

`records.py` owns exact rational values, nonnegative closed error intervals, the closed
objective inventory, tool identities, artifact bindings, first-passing classification,
and each record's typed mapping. Every maintained value derives from `BaseTypedRecord`;
the shared final `to_dict()`, `from_dict()`, `to_json()`, and `from_json()` methods own
the serialization boundary. `validation.py` correlates exact canonical request/result
bytes without claiming interval containment.

There is no parallel JSON Schema or proposition-specific codec. The domain schema is the
closed `_mapping()`/`_from_mapping()` contract plus constructor invariants, following the
maintained KSD record convention.

## Dependency boundary

The implemented core uses only the Python standard library and existing KSD
serialization contracts. It does not import an interval-arithmetic provider.

A future provider leaf may produce outward enclosures, but it must:

1. accept the exact proposition inputs without a binary64 round trip;
2. fail closed on nonfinite, unordered, singular, or unresolved operations;
3. retain working precision and directed-rounding policy;
4. produce a separately hashed trace sufficient for containment review; and
5. remain distinct from the independent containment verifier.

The provider and verifier may not be two entry points over the same implementation or
source hash. Structural wire validation is not containment verification.

## Current caller boundary

The first-passing-support request binds the exact controlled four-state parent,
construction and evaluation inventories, mediated and direct candidates, threshold,
selected support, source hashes, native result, and passing numerical-verification
artifact. The certification result supplies all 32 support/objective intervals in
canonical order and names distinct producer and verifier artifacts.

No current calculation automatically manufactures or accepts this result. Admission of
a retained certificate requires a separately reviewed composition after complete
producer and verifier capabilities exist.
