# `periodic1d.campaign.model.toy_defects.alignment` target mapping

## Purpose and status

The behavior remains temporarily implemented in the legacy underscored campaign
namespace pending canonical ownership migration. It constructs controlled
finite-periodic site, orbital, phase, and spin basis maps. Row 018 renamed the operation input from
`Periodic1DBasisScramblingModel` to `Periodic1DBasisScramblingDefinition` without a
compatibility alias.

## Public inventory

| Symbol | Category | Responsibility |
|---|---|---|
| `Periodic1DBasisScramblingDefinition` | Operation definition | Translation, orbital permutation/rotation/phases, site phase, and spin rotation controls |
| `Periodic1DBasisScramblingRequest` | Action request | Definition, cell count, reduced momentum, and spin factor |
| `Periodic1DBasisScramblingResult` | Represented map result | Reference-to-candidate unitary and explicit adjoint inverse |
| `Periodic1DBasisScramblingConstructor` | ActionObject | Deterministic finite-periodic map construction |

## Mathematical and directional convention

The result explicitly stores `reference_to_candidate = U` and
`candidate_to_reference = U^dagger`. Finite translations include the authored Bloch
boundary phase. Orbital operations and optional spin-half SU(2) rotation are composed in
the documented direction. The definition itself contains no energy shift or scientific
alignment decision.

## Class navigation

- [`Periodic1DBasisScramblingDefinition`](Periodic1DBasisScramblingDefinition/index.md)

## Code, tests, and Sphinx

| Kind | Path or node | Responsibility |
|---|---|---|
| Code | `python/src/ksdft2effmass/campaigns/periodic_1d/model/toy_defects/alignment.py` | Definition and unitary construction |
| Test | `python/tests/ksdft2effmass/campaigns/periodic_1d/model/toy_defects/test__Periodic1DBasisScramblingConstructor.py::TestPeriodic1DBasisScramblingConstructor` | Neutral element, nontrivial unitary directions, retired name |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | Public route |

## Provenance and evidence

Original local work under the repository license. Authored identity and nontrivial
unitary oracles establish bounded software/numerical behavior. They do not identify a
physical map, validate a material model, quantify uncertainty, or accept a campaign
conclusion.

## Limitations

The module supports the authored two-orbital and spinless/spin-half conventions only.
It does not discover maps from wavefunctions or align independently sourced operators.
