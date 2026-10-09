# `periodic1d.campaign.oracle`

## Purpose and status

This implemented canonical package groups named campaign-specific oracle studies. Row
064 moved the finite-rank-oracle family here without compatibility aliases or wire
changes. This package does not define a generic oracle engine, registry, factory,
plugin system, discovery mechanism, qualification service, or production acceptance
abstraction.

## Child map

| Child | Responsibility | Canonical page |
|---|---|---|
| `finite_rank` | Bounded finite-rank Bloch-resolvent versus site-space campaign | [Finite-rank oracle campaign](finite_rank/index.md) |

## Ownership boundary

A named oracle campaign may own its encoded inputs, finite comparison policy,
observations, retained evidence, and independent verification. It does not thereby own
general retained-space mathematics, production oracle qualification, scientific
validation, or acceptance policy outside its exact evidence class and validity domain.

Original local work under the repository license.
