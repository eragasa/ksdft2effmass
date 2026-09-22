# Control-plane cleanup Slice A

## Status

Slice A is complete at inventory base revision
`2027ebedae9427b4b82237d3a3429e2e308b234a`. It is observational: no tracked
surface was deleted, relocated, renamed, merged, replaced, or redesigned.
Slice B remains pending and has not begun.

## Graph inventory

The machine-readable report
[`control-plane-reachability.json`](control-plane-reachability.json) represents
the tracked control plane as the directed graph $G=(V,E)$. Each of the 1,404
tracked in-scope paths is assigned to exactly one node. The graph records 11,116
evidenced consumer, authority, generation, resolution, navigation, test, and
validation relationships from 65 explicit operational roots.

The inventory deliberately distinguishes evidence from operational dependency.
Historical records, tests, documentation, and generated projections can provide
edges without making their targets live. Filename similarity is never an edge.

## Classification summary

| Dimension | Count |
|---|---:|
| Authority | 140 |
| Runtime | 455 |
| Projection | 116 |
| Documentation | 47 |
| History | 646 |
| Cache | 0 |
| Retain | 403 |
| Delete candidate | 679 |
| Unresolved | 322 |

The 1,001 unreachable surfaces form one evidence-connected cluster. That
cluster contains all 322 unresolved surfaces, so it remains fail-closed. The
inventory proposes 635 Slice B candidates and 44 Slice C candidates, but these
are inventory conclusions only and authorize no deletion.

The unresolved set is concentrated in fixtures, tests, authored harness
narrative, reports, compatibility extensions, three package facades, intake,
and other mixed runtime or documentation surfaces. Each unresolved node records
explicit Slice B or Slice C resolution work. The connected cluster must remain
retained until that work resolves owner completeness, supported external
consumption, declarative resolution, generation provenance, or retained review
and offline-use purpose.

## Evidence and limitations

Edges are backed by tracked paths plus exact fields, symbols, imports, exports,
links, identifiers, manifest/profile entries, schema references, resolver
inputs, generation commands, or validation commands. Repository-local static
evidence cannot establish absence of all external consumers or user-global Pi
configuration. Those limitations are represented explicitly rather than being
converted into deletion findings.

Scientific source, numerical-verification evidence, scientific-validation and
UQ evidence, simulations, computational protocols, scientific schemas and
fixtures, research documentation, and publication artifacts remain excluded.
Only their control-plane references are represented where applicable.

## Next boundary

The active cleanup Task now waits at
`harness_control_plane_cleanup_active_slice_b_pending`. Slice B must not delete
an unresolved surface or any surface in a cluster connected to one. It begins
only as a separate slice after this inventory commit is durable.
