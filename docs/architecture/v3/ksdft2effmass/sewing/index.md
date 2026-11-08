# Sewing

## Purpose

`ksdft2effmass.sewing` is the authoritative source owner for explicit identification
between scientifically related state spaces. It owns both the implemented
reciprocal-endpoint values and the reserved categories whose executable contracts remain
unselected. The legacy `ksdft2effmass.solidstate.reciprocal_sewing` module and
`ksdft2effmass.solidstate` re-exports are removed rather than retained as compatibility
facades.

## Scientific categories

The package keeps seven sewing problems separate:

```text
IdentityReciprocalSewing                 concrete reciprocal-endpoint construction
EmbeddedPositionReciprocalSewing         reserved abstract category
PermutationPhaseReciprocalSewing         reserved abstract category
PlaneWaveIndexSewing                     reserved abstract category
ProjectedSubspaceSewing                  reserved abstract category
SymmetrySewing                           reserved abstract category
FiniteBoundarySewing                     reserved abstract category
```

Their applicability conditions remain distinct:

- exact coordinate periodicity;
- position-phase sewing derived from an ordered embedding;
- declared endpoint permutation and phases;
- reciprocal-index relabeling in a plane-wave representation;
- restriction of an admitted ambient sewing map to selected subspaces;
- unitary or antiunitary symmetry action; and
- identification across a finite real-space quotient seam.

The package does not define a generic sewing base, protocol, request/result pair,
`apply()` operation, or overloaded identity helper. Unimplemented categories expose only
an abstract, non-executable `execute()` reservation returning `Never`.

## Implemented reciprocal-endpoint contract

`ReciprocalEndpointSewingMap` retains:

- a nonempty construction identifier;
- a finite, nonempty, square, unitless complex matrix; and
- the ambient dimension derived from that matrix.

The matrix acts from the left on coefficients in one ordered ambient basis. The value
does not infer the basis, gauge, Bloch convention, map direction, or scientific
correlation. Those remain obligations of the calculation or model that constructs and
consumes the map.

`IdentityReciprocalSewing(ambient_dimension=n)` constructs

\[
Q_{\mathbf G}=I_n.
\]

Here `n` is the ambient-space dimension, not automatically the retained rank. Selecting
the identity asserts that the two reciprocal endpoints use the same ordered ambient
basis and Bloch convention. Periodic spectra or equal matrix dimensions alone do not
establish that assertion.

`ReciprocalEndpointSewingInventory` retains one nonempty tuple of positive-axis maps in
zero-based reciprocal-axis order. Every map must act on the same ambient dimension.
Tuple position, rather than an inferred label or sorted matrix property, identifies the
axis. `map_for_axis()` validates a built-in integer index and performs no fallback.

## Identity and invariants

The named identity construction retains the wire identifier
`identity-periodic-endpoint-sewing.v1`. Migration changes source ownership only; it does
not change this identifier, the coefficient matrix, axis ordering, typed-record fields,
or canonical JSON bytes.

The implemented values are frozen, slotted dataclasses. Public numeric construction
rejects booleans, numeric strings, and foreign scalar types through exact built-in type
checks. `basis_identifier` remains deliberately unresolved and is not introduced by this
migration.

## Dependencies and flow

```text
calculation/model convention
  -> ReciprocalEndpointSewingMap or IdentityReciprocalSewing
  -> ReciprocalEndpointSewingInventory for multidimensional axes
  -> frame transport / alignment / band-equivalence consumer
  -> retained result serialization
```

The periodic-2D and periodic-3D rank-N frame-transport requests now follow the same
contract as their rank-two counterparts: each receives an explicit axis-ordered
`ReciprocalEndpointSewingInventory`, validates its spatial and ambient dimensions, and
passes it to transport diagnostics without manufacturing identity inside the transport
action. Synthetic v1 aggregate compositions continue to select named ambient-space
identity sewing explicitly at their composition boundaries. The parent-independent 3D
field-analysis policy carries the selected inventory, so Wannier-derived fields can use a
qualified nonidentity sewing without changing the transport implementation.

The sewing package depends on Project Koios unit-bearing matrix quantities and the
repository-native typed-record serialization boundary. It does not own lattice geometry,
frame construction, eigensolvers, Fourier transforms, projected closure, Wilson-loop
interpretation, or acceptance policy.

## Serialization and provenance

`ReciprocalEndpointSewingMap` and `ReciprocalEndpointSewingInventory` use
`BaseTypedRecord._mapping()` and `_from_mapping()`. The map fields remain `identifier`
and `coefficient_map`; the inventory field remains `positive_axis_maps`. No parallel
codec, compatibility read, alias, or schema is introduced.

Calculations that accept arbitrary sewing retain the exact map with their result.
Legacy v1 calculation records that support only deterministic named identity sewing
continue to reject arbitrary maps rather than silently discarding them.

## Scientific boundary

Ambient sewing and projected closure are different operations. For selected frames
`F_start` and `F_end`, the retained-space closure

\[
F_{\mathrm{end}}^\dagger Q_{\mathbf G}F_{\mathrm{start}}
\]

may be nonidentity even when the ambient sewing is identity. Conversely, a square
finite-cutoff plane-wave index shift must not be promoted to an exact unitary reciprocal
sewing map without its own qualification.

## Verification and navigation

- Source: `python/src/ksdft2effmass/sewing/`
- Focused software verification:
  `python/tests/software_verification/ksdft2effmass/sewing/test__Sewing.py`
- Public API: `doc/sphinx/api/sewing.rst`
- Reciprocal embedding and Wilson prerequisites:
  [`../periodic/basis_embedding/index.md`](../periodic/basis_embedding/index.md)
- Periodic-1D consumer composition:
  [`../periodic1d/implementation.md`](../periodic1d/implementation.md)

Software tests establish construction, validation, serialization, import ownership, and
consumer behavior. They do not establish that identity sewing is scientifically valid
for an arbitrary basis or calculation.
