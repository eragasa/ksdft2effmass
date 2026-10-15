# `Periodic2DHoppingShellHierarchyDefinition`

## Purpose and status

Prospective immutable DataObject defining the complete HSH-1 problem. It is not
implemented or supported.

## Public contract

Planned construction accepts only explicit values. Read-only properties expose the
exact composed scalar parent, maximal orbit count, training/withheld coordinates, shell
masks, and parent model. No property performs file I/O or numerical fitting.

Planned supported route:
`ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.Periodic2DHoppingShellHierarchyDefinition`.

## State and identity

Stable identity is the nonempty `definition_id` together with exact canonical content.
The state includes:

- exact `Periodic2DIsolatedBandCampaignDefinition` source parent and source SHA-256
  identities;
- source coupling selector and common energy shift;
- centered representatives, raw complex source blocks, canonical orbit representatives,
  multiplicities, and builder-projected real target coefficients;
- shell squared radii and maximal-space active masks;
- positive source-mesh spectral weights and block/operator weights;
- lower/upper coefficient bounds containing the target with declared margin;
- positive spectral/operator thresholds and nonnegative separation resolution;
- training and withheld coordinates and direct-parent withheld energies;
- certificate-method identity and arithmetic policy; and
- separate projection, quadratic, feasibility, rounding, and verification tolerances.

All ordering is canonical and all maintained sequences are tuples.

## Invariants and failure behavior

The object enforces strict built-in types, finite values, positive energy scales and
weights, lowercase SHA-256 syntax, exact source/target length correlations, complete
disjoint orbit coverage, multiplicity sums, nested shells, full final support, disjoint
mesh roles, and exact source-parent controls. It rejects relative rescaling or
reordering that is not represented explicitly in a new definition. The producer and
verifier, not the constructor, establish exact projection correlation and target
containment with the declared box margin.

`TypeError` denotes an exact-type violation; `ValueError` denotes an invalid finite
problem definition.

## Dependencies and collaborators

The class composes, but does not subclass,
`Periodic2DIsolatedBandCampaignDefinition`. The calculator consumes it; results retain
its identity; serializers transport it or an exact correlated projection; verifiers
reconstruct its derived inventories.

## Data and action flow

A deterministic input builder decodes retained source records, copies the compact raw
block family, records its proposed projection, and constructs this object. The producer
and verifier independently reconstruct that projection before using it. The object
flows unchanged thereafter; evaluation cannot mutate it.

## Serialization and compatibility

The schema-v1 document retains every outcome-relevant control or a digest-bound
canonical input reference. Future defaults cannot reinterpret a v1 definition. Any
change to weights, thresholds, shells, box, metric, or arithmetic policy creates a new
definition identity.

## Scientific and numerical boundary

The definition describes one finite synthetic scalar parent and one hierarchy-relative
comparison. Thresholds are benchmark controls, not physical tolerances or uncertainty
intervals. See [scientific](../../scientific.md) and [numeric](../../numeric.md).

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/definition.py` | Class | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy.definition.Periodic2DHoppingShellHierarchyDefinition` | Complete frozen HSH-1 definition |
| same | Method | `...Periodic2DHoppingShellHierarchyDefinition.__post_init__` | Strict invariant enforcement |

## Test mapping

Planned node prefix:
`TestPeriodic2DHoppingShellHierarchyCalculator::test_construction__`. Tests will cover
composition, strict types, finite values, orbit/shell correlation, weights, target
margin, mesh roles, and tolerance signs. No test exists.

## Sphinx mapping

Prospective API page:
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`.

## Provenance

Original local work under the repository license. Meaning derives from the HSH-1 draft
protocol.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Class absent | None |
| Numerical verification | Not applicable | Definition only | None |
| Scientific validation | Not evaluated | Synthetic draft | None |
| Uncertainty quantification | Not evaluated | No uncertainty semantics | None |
| Human acceptance | Not evaluated | Controls remain unfrozen | None |

## Limitations and deviations

Final field names may change during implementation review, but no outcome-relevant
control may become implicit.
