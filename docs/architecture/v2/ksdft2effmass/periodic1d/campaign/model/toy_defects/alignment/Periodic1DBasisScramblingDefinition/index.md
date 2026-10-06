# `Periodic1DBasisScramblingDefinition`

## Purpose and status

`Periodic1DBasisScramblingDefinition` is the implemented row-018 immutable operation
definition for a controlled change of finite-periodic coordinates. It is not a
scientific model.

## Public contract

The current transitional import is
`ksdft2effmass.campaigns.periodic_1d.model.toy_defects`. Canonical ownership must use
the non-underscored `periodic1d` namespace and must not retain a compatibility alias.

The definition stores an integer cell translation, exact two-orbital permutation,
orbital rotation angle, two orbital phases, linear site/orbital phase step, nonzero
three-component spin axis, and spin-half rotation angle. Angles are in radians.

## Invariants and failure behavior

Translation is an exact integer and the orbital permutation is exactly `{0, 1}`. Angle
and axis entries are finite real non-Boolean scalars, and the spin axis is nonzero before
normalization. Wrong semantic types raise `TypeError`; invalid permutation, nonfinite
controls, or zero spin axis raise `ValueError`. A short `__post_init__` delegates
translation, permutation, real-control, and axis invariant families.

## Scientific boundary

The definition specifies authored numerical coordinates only. It owns no campaign phase,
retained path, parent operator, energy alignment, threshold, provenance, or acceptance
policy. A constructor request supplies finite geometry, reciprocal momentum, and spin
factor; the result supplies both map directions.

## Code and evidence mapping

| Kind | Path or node | Established behavior |
|---|---|---|
| Code | `python/src/ksdft2effmass/campaigns/periodic_1d/model/toy_defects/alignment.py:Periodic1DBasisScramblingDefinition` | Immutable operation controls |
| Test | `TestPeriodic1DBasisScramblingConstructor::test_method__execute__constructs_identity_for_zero_scrambling` | Neutral definition |
| Test | `TestPeriodic1DBasisScramblingConstructor::test_method__execute__returns_inverse_unitary_directions` | Nontrivial unitary composition and map direction |
| Test | `TestPeriodic1DBasisScramblingConstructor::test_public_api__definition__has_no_retired_model_alias` | Definition terminology and alias removal |
| Sphinx | `doc/sphinx/api/research-monograph-campaigns.rst` | Current public route |

## Provenance and evidence

Original local work under the repository license. Synthetic analytic map tests establish
bounded software/numerical behavior. They do not identify a physical basis map,
establish material validation, quantify uncertainty, or record acceptance.

## Limitations

The definition assumes exactly two authored orbital labels and a three-axis spin
rotation control. It does not generalize basis alignment across unidentified spaces.
