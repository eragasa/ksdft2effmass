# Migration phase 6: control-model catalog execution

## Status

**Proposed.** `PeriodicControlModelCatalog` is implemented, but no cross-model
campaign consumes an exact catalog snapshot.

## Purpose

Make cross-model iteration explicit and reproducible without filesystem scanning,
subclass discovery, structural protocol matching, or a common calculation method.

## Required deliverables

1. Register only concrete models that completed nominal migration in phase 5 or an
   applicable later phase.
2. Construct one immutable `PeriodicControlModelCatalog` with deterministic tuple order
   and unique stable model identities.
3. Define an immutable campaign request that contains the exact catalog snapshot and
   explicit per-model evaluation adapters or declared observation request.
4. Return typed observations that preserve model identity, spatial dimension, role,
   evaluated quantity, unit, method, and availability.
5. Represent incompatible or unavailable evaluations explicitly rather than omitting a
   model or coercing unlike quantities.

The campaign may establish catalog consumption and typed observation routing. It must
not invent a generic solver, serializer, tolerance, or scientific acceptance method
for all periodic models.

## Catalog invariants

- Registration is explicit; no module scan or subclass enumeration is allowed.
- Catalog order is semantically retained and deterministic.
- Each entry is a nominal `PeriodicModel` with exact `CONTROL_MODEL` role.
- Model identifiers are nonempty and unique.
- Reported dimension agrees with nominal dimension membership.
- A catalog snapshot used by a campaign is immutable and retained in the request or
  result identity.

## Excluded work

Phase 6 does not register material-reference models, compare incompatible operators,
claim all control models share one numerical method, or establish scientific acceptance.

## Completion gate

- At least one maintained control-model inventory is registered.
- One campaign consumes an exact immutable snapshot without rediscovery.
- Tests cover deterministic order, duplicate rejection, nominal membership, snapshot
  preservation, explicit unavailability, and stable observation identity.
- Public documentation states the bounded quantity and evidence class produced by the
  campaign.
- Typing, pytest, Ruff, formatting, Sphinx, links, and diff checks pass.
