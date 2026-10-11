# `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.definition`

## Purpose and status

Prospective module for the immutable HSH-1 problem definition. No source module exists.

## Prospective public contract inventory

- [`Periodic2DHoppingShellHierarchyDefinition`](Periodic2DHoppingShellHierarchyDefinition/index.md) — DataObject containing the complete frozen scientific and numerical problem.

No public module-level function, mutable constant, exception, or implicit default is
planned. Derived inventories are exposed as read-only properties of the definition.

## Represented objects

The definition binds one exact `Periodic2DIsolatedBandCampaignDefinition`, consumed
source digests, the raw finite source blocks, the builder-projected target, orbit
ordering and multiplicities, nested shell radii, coefficient box, source and withheld
coordinates, positive channel weights, thresholds, metric normalization, certificate
method identity, and separate positive tolerances. The producer and verifier recompute
the projection rather than trusting the projected target field.

Coordinates are reduced reciprocal pairs. Coefficients and energies use the declared
source energy unit. Distances and losses are dimensionless after the fixed $E_G$
normalization.

## Invariants and failure behavior

Construction rejects non-built-in scalars, booleans, nonfinite values, malformed
digests, nonpositive scales/weights/thresholds, non-nested shells, incomplete orbit
coverage, inconsistent source/target lengths, overlapping training/withheld roles, and
source controls inconsistent with the retained $\lambda_{xy}=0.30$ parent. Exact
source-projection correlation and target containment with the declared box margin are
execution premises reconstructed by the producer and verifier.

Exact-type failures raise `TypeError`; inconsistent finite values raise `ValueError`.
No constructor performs file I/O or silently repairs inputs.

## Dependencies and neighboring owners

The module composes the exact scalar parent definition from
`periodic2d.campaign.nbands_1`. It does not own parent execution, retained-file decoding,
quadratic construction, dispositions, or verification.

## Class navigation

- [`Periodic2DHoppingShellHierarchyDefinition`](Periodic2DHoppingShellHierarchyDefinition/index.md)

## Prospective code mapping

| Planned path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/definition.py` | Module | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.definition` | Immutable HSH-1 controls |
| same | Class | `...definition.Periodic2DHoppingShellHierarchyDefinition` | Complete frozen definition |

## Test mapping

Planned owner:
`python/tests/software_verification/ksdft2effmass/analysis/model_adequacy/test__Periodic2DHoppingShellHierarchyCalculator.py`, class
`TestPeriodic2DHoppingShellHierarchyCalculator`. Planned construction tests cover exact
parent composition, strict scalar types, digest syntax, orbit/shell correlation,
positive weights, target-containing box margin, and disjoint mesh roles.

## Sphinx mapping

No Sphinx page exists. Before support, the class will be exposed through
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license. Controls derive from the HSH-1 draft
protocol; unresolved controls remain explicit required fields rather than defaults.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Module and tests do not exist | None |
| Numerical verification | Not applicable | Definition performs validation, not calculation | None |
| Scientific validation | Not evaluated | Synthetic draft controls | None |
| Uncertainty quantification | Not evaluated | No uncertainty model | None |
| Human acceptance | Not evaluated | Definition is not frozen | None |

## Limitations and deviations

The precise weight formula, box rule, thresholds, and interval method are unresolved.
This page records required ownership without choosing those values.
