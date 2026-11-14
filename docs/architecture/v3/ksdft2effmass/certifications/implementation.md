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
        arb/
          records.py
          parent.py
          mediated.py
```

`records.py` owns exact rational values, nonnegative closed error intervals, the closed
objective inventory, tool identities, artifact bindings, first-passing classification,
and each record's typed mapping. Every maintained value derives from `BaseTypedRecord`;
the shared final `to_dict()`, `from_dict()`, `to_json()`, and `from_json()` methods own
the serialization boundary. `validation.py` correlates exact canonical request/result
bytes without claiming interval containment.

The optional `arb` leaf owns Python-FLINT-specific result records, a frozen-parent
lowest-eigenvalue encloser, and a transform-mediated maximum-error encloser. It does not
produce the direct objective, a complete certification artifact, an independent
containment verification, or a final result assembly. The dependency-free package root
does not import this provider leaf.

There is no parallel JSON Schema or proposition-specific codec. The domain schema is the
closed `_mapping()`/`_from_mapping()` contract plus constructor invariants, following the
maintained KSD record convention.

## Dependency boundary

The implemented core uses only the Python standard library and existing KSD
serialization contracts. It does not import an interval-arithmetic provider. The
optional `certificates` extra pins `python-flint==0.9.0`; importing the `arb` leaf is an
explicit provider choice.

The Arb provider:

1. accepts exact rational coordinates and support identifiers without a binary64 round
   trip;
2. fails closed when the lowest eigenvalue enclosure is not isolated;
3. retains working precision in immutable result values; and
4. exports signed parent and nonnegative mediated-error balls as exact rationals.

A future complete producer must add the direct objective, producer identity, source and
artifact digests, directed-rounding and error-budget identities, and a trace sufficient
for review. A separately authored containment verifier must not call or wrap that
producer. Structural wire validation remains distinct from containment verification.

## Current caller boundary

The first-passing-support request binds the exact controlled four-state parent,
construction and evaluation inventories, mediated and direct candidates, threshold,
selected support, source hashes, native result, and passing numerical-verification
artifact. The certification result supplies all 32 support/objective intervals in
canonical order and names distinct producer and verifier artifacts.

No current calculation automatically manufactures, persists, or accepts this result.
Admission of a retained certificate still requires a separately reviewed composition
that writes exact producer and verifier bytes without changing historical executions.
