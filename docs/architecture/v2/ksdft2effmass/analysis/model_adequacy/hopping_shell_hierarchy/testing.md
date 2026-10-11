# HSH-1 testing and evidence plan

## Status

All entries on this page are prospective. No listed test currently exists, and no row
constitutes evidence until its exact implementation passes review and execution.

## Planned direct test owners

- `python/tests/software_verification/ksdft2effmass/analysis/model_adequacy/test__Periodic2DHoppingShellHierarchyCalculator.py`
- `python/tests/numerical_verification/ksdft2effmass/analysis/model_adequacy/test__Periodic2DHoppingShellHierarchyCalculator.py`

Each module should group tests beneath one cohesive
`TestPeriodic2DHoppingShellHierarchyCalculator` class, following repository test policy.
Retained-package tests may extend the software-verification class rather than creating
unrelated test containers.

## Planned claim-to-test map

| Intended behavior | Planned test suffix | Oracle or mutation |
|---|---|---|
| Exact parent is composed, not inherited | `test_construction__composes_exact_scalar_parent_definition` | Type and identity assertions |
| Canonical $D_4$ orbits cover the finite torus once | `test_execution__constructs_disjoint_complete_orbit_inventory` | Independent integer-orbit enumeration |
| Source defects are measured before projection | `test_execution__rejects_source_above_projection_tolerance` | Hermiticity, imaginary, and orbit mutations |
| Projection produces and correlates one exact real target | `test_execution__projects_source_to_exact_d4_target` | Independent orbit averaging and projected-field mutation |
| Shells are nested in one maximal space | `test_execution__embeds_nested_shell_masks_without_renormalization` | Inactive-coordinate and metric assertions |
| Relative spectral weights affect the problem and preserve declared symmetry | `test_execution__rejects_weight_miscorrelation` | Reordered, relatively rescaled, and $D_4$-asymmetric weights |
| Both loss channels reconstruct as quadratics | `test_execution__quadratics_match_direct_losses` | Random bounded points and full coefficient comparison |
| HSH wrapper delegates only active-coordinate evaluation | `test_result__quadratic_wrapper_validates_embedding_then_delegates` | Common primitive stub plus inactive-coordinate attacks |
| Box-constrained nonemptiness is respected | `test_execution__distinguishes_unconstrained_and_box_constrained_minima` | Center outside coefficient box |
| Empty sets do not emit distances | `test_result__empty_channel_has_no_distance_interval` | Disposition/result mutation |
| Feasible pairs bound distance above | `test_verification__reconstructs_constructive_upper_bounds` | Pair and upward-bound mutation |
| Support certificates bound distance below | `test_verification__reconstructs_outward_support_bound` | Direction, endpoint, dual norm, and rounding mutations |
| Small numerical objective is not compatibility | `test_result__requires_explicit_common_witness` | Near-zero distinct feasible pair |
| A compatible witness satisfies both channels | `test_verification__reconstructs_common_witness` | Threshold and witness mutation |
| Minimality requires all smaller classes resolved | `test_result__rejects_minimality_with_unresolved_smaller_class` | Earlier-class disposition mutation |
| Withheld coordinates are point-disjoint and cannot alter training decisions | `test_execution__withheld_role_is_disjoint_and_diagnostic_only` | Coordinate-overlap and withheld-energy mutations |
| Typed verification avoids producer execution | `test_verification__does_not_call_calculator` | Import/call boundary inspection |
| Typed verifier does not use common quadratic evaluation as its oracle | `test_verification__does_not_call_common_quadratic_constructor_or_evaluators` | Constructor/`squared_loss`/`root_loss` call traps while independent reconstruction passes |
| Standalone verification avoids producer imports | `test_retained_verifier__does_not_import_producer_modules` | AST/import inspection |
| Wire decoding fails closed | `test_retained_verifier__rejects_contract_tampering` | Unknown keys, booleans, strings, nonfinite values |
| Input generation is deterministic | `test_configuration__materializes_retained_input` | Byte-identical regeneration, including pointwise withheld direct-parent values |
| Withheld values bind exact generator provenance | `test_configuration__correlates_withheld_parent_generation` | Source/dependency/environment identity and energy mutation |
| Source bytes match manifest entries | `test_retained_verifier__rejects_source_manifest_miscorrelation` | Digest-entry mutation |

## Numerical oracles

At minimum, numerical verification should use:

1. a tiny analytically constructed orbit inventory with known multiplicities;
2. synthetic diagonal quadratics with exact empty, separated, tangent, and intersecting
   cases;
3. a support-function case whose lower bound is known in rational arithmetic;
4. a common-witness case with exact zero inactive coordinates;
5. direct dense-grid evaluation of retained quadratic values; and
6. an independent Fourier reconstruction of the source and withheld bands.

The outward-rounding implementation requires qualification against a higher-precision or
interval oracle over positive, negative, subnormal-adjacent, and cancellation-sensitive
support gaps. Platform scope and arithmetic assumptions must be retained.

## Adversarial coverage

Fail-closed mutations must cover source digests, orbit representatives, multiplicities,
shell order, energy shift, coordinate order, weights, box bounds, thresholds,
resolution, active indices, quadratic cross terms, feasible points, certificate
orientation, support endpoints, dual norm, lower/upper bounds, dispositions, critical
class, withheld roles, and figure-data correlation.

## Evidence classification

| Evidence kind | Status | Evidence or reason | Reference | Comparator/tolerance | Environment | Validity domain | Accepting authority |
|---|---|---|---|---|---|---|---|
| Software verification | Not evaluated | Planned tests do not exist | Planned paths above | Exact assertions and fail-closed mutations | Future locked Python environment | Planned API and retained schema | Not applicable |
| Numerical verification | Not evaluated | No oracle execution | Planned analytic and high-precision oracles | Frozen per-oracle tolerances | Future locked NumPy/SciPy and interval stack | Frozen finite hierarchy | Not applicable |
| Scientific validation | Not evaluated | Synthetic parent only | None | None | None | None | Not applicable |
| Uncertainty quantification | Not evaluated | No uncertainty model | None | None | None | None | Not applicable |
| Human acceptance | Not evaluated | No freeze or acceptance decision | Future decision record | Not applicable | Not applicable | Future frozen problem | Human owner not yet recorded |

## Residual risk

Producer and verifier may share numerical libraries, floating-point behavior, and
Fourier conventions. SHA-256 binds exact bytes but not semantic correctness,
chronology, or authorship. Passing tests will establish bounded implementation behavior,
not physical validity or a material conclusion.
