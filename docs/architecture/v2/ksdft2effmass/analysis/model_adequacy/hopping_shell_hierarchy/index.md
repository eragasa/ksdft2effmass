# `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy`

## Purpose and status

This is the **prospective** architecture for HSH-1, the controlled scalar
periodic-two-dimensional hopping-shell hierarchy described by the draft
[calculation protocol](../../../../../../../calculations/ICMSEP2026/conference/paper_1/hopping-shell-hierarchy/protocol.md).
No Python package, supported export, calculation result, or evidence claim exists yet.

The active [isotropic 2-D development task](../../../../../../tasks/dev/experiments/isotropic2d/index.md)
and canonical [experiment architecture](../../../../experiments/model-adequacy/periodic2d/hopping-shell-hierarchy/index.md)
place the concrete scientific composition under a publication-independent experiment.
Therefore the prospective installed-package mappings below are retained as a design
inventory, not authorization to implement HSH-specific controls in `python/src/`.
Orbit, weight, threshold, certificate, schema, and disposition ownership must be
reconciled with the experiment boundary before implementation; only demonstrably
reusable numerical behavior may later move to an installed owner.

The target package will own a nested family of real, square-symmetric hopping models
embedded in one maximal coefficient space. It will compare spectral and represented-
operator admissible sets, retain constructive upper bounds and independently
reconstructable lower certificates, and report a smallest tested compatible class only
when every smaller class is resolved. Its witness, separation, unresolved, correlation,
and verification meanings follow the shared
[admissible-set evidence semantics](../admissible-set-evidence-semantics.md); its
parameter space, metric, masks, certificates, empty-set states, and hierarchy logic
remain HSH-local.

## Prospective public contract

| Module | Intended public responsibility |
|---|---|
| [`definition`](definition/index.md) | Immutable parent binding, orbit inventory, shell hierarchy, weights, coefficient box, thresholds, mesh roles, and tolerances |
| [`calculate`](calculate/index.md) | Pure deterministic producer for target projection, quadratic sets, witnesses, distance bounds, and withheld diagnostics |
| [`results`](results/index.md) | Immutable quadratic proof objects, support certificates, per-class outcomes, and hierarchy result |
| [`serialization`](serialization/index.md) | Strict canonical schema-v1 result encoding and decoding |
| [`verify`](verify/index.md) | Independent typed-result reconstruction and bounded verification result |

Cross-cutting drafts:

- [scientific boundary](scientific.md);
- [calculation schematic](schematic.md);
- [numerical contract](numeric.md);
- [implementation plan](implementation.md); and
- [testing and evidence plan](testing.md).

No route is supported until implementation, deliberate export, direct tests, Sphinx
API documentation, strict retained codecs, and evidence review are complete.

## Ownership boundary

The package will own:

- canonical finite-torus $D_4$ orbit ordering and multiplicities for HSH-1;
- exact embedding of every shell class into one maximal real coefficient space;
- HSH-1 spectral and represented-operator losses and their relative weights;
- the one fixed orbit-multiplicity distance metric;
- channel nonemptiness, feasible points, common witnesses, upper bounds, and support
  certificates;
- per-class and hierarchy-level dispositions; and
- strict correlation among controls, proof objects, diagnostics, and dispositions.

It will not own the original two-dimensional parent calculation, reusable periodic
model/Fourier primitives, arbitrary point-group representation theory, material
validation, gauge optimization, uncertainty calibration, or protected calculator
execution. The retained source parent remains owned by
`periodic2d.campaign.nbands_1`; this outward analysis package owns source/result
correlation and HSH adequacy policy. The sibling
`analysis.model_adequacy.losses.quadratic` module owns only normalized dimensionless
positive-definite quadratic storage and evaluation. HSH-1 retains all shell, channel,
energy unit/scale, active-index, weight, threshold, box, metric, reconstruction, and
certificate meaning.

## Dependency rules

Permitted direct dependencies are immutable records and parent/model primitives from
`ksdft2effmass.periodic2d`, the sibling
`ksdft2effmass.analysis.model_adequacy.losses` package, NumPy/SciPy numerical kernels,
and project serialization primitives. The dependency direction is outward:
`analysis.model_adequacy.hopping_shell_hierarchy -> periodic2d`; no `periodic2d` module
may import the HSH adequacy layer. HSH-1 composes its source parent and
`DimensionlessPositiveDefiniteQuadraticLoss`; it must not subclass either one or reuse
the M4/M5 scaffolds in `periodic2d.studies`.

The producer and typed verifier must perform no file I/O and no external execution.
Retained scripts may decode files and manifests but must not place wire mechanics in the
scientific objects. Withheld values are downstream diagnostics and cannot alter source
projection, weights, thresholds, feasible points, certificates, or dispositions.

## Selected analysis layering

The canonical shared primitive is defined in
`ksdft2effmass.analysis.model_adequacy.losses.quadratic` and deliberately exported as
`ksdft2effmass.analysis.model_adequacy.losses.DimensionlessPositiveDefiniteQuadraticLoss`.
It accepts only explicitly normalized dimensionless canonical coordinates. HSH owns the
energy unit and scale and maps active energy coefficients to dimensionless ratios before
delegation. Certificate generalization remains explicitly out of scope: HSH's
outward-rounded weighted-metric support certificate stays HSH-local.

## Child map

- [`definition`](definition/index.md)
- [`calculate`](calculate/index.md)
- [`results`](results/index.md)
- [`serialization`](serialization/index.md)
- [`verify`](verify/index.md)

## Prospective code mapping

| Planned code path | Symbol kind | Planned qualified name | Architecture responsibility |
|---|---|---|---|
| `python/src/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy/__init__.py` | Package | `ksdft2effmass.analysis.model_adequacy.hopping_shell_hierarchy` | Deliberate HSH-1 exports |
| `.../definition.py` | Module | `...hopping_shell_hierarchy.definition` | Frozen problem definition |
| `.../calculate.py` | Module | `...hopping_shell_hierarchy.calculate` | Producer ActionObject |
| `.../results.py` | Module | `...hopping_shell_hierarchy.results` | Proof and result DataObjects |
| `.../serialization.py` | Module | `...hopping_shell_hierarchy.serialization` | Strict wire format |
| `.../verify.py` | Module | `...hopping_shell_hierarchy.verify` | Independent reconstruction |

All paths are targets, not current-source mappings.

## Test and Sphinx mapping

Planned direct test ownership is documented in [testing.md](testing.md). The intended
user-facing page is
`doc/sphinx/api/ksdft2effmass/analysis/model_adequacy/hopping_shell_hierarchy.rst`; it does not yet
exist and is required before any supported export.

## Provenance

Original local work under the repository license. The architecture derives its bounded
meaning from the HSH-1 draft protocol and the retained scalar parent; it does not alter
either source.

## Evidence

| Evidence kind | Status | Evidence or reason | Validity domain |
|---|---|---|---|
| Software verification | Not evaluated | Target package and tests do not exist | None |
| Numerical verification | Not evaluated | HSH-1 has not been executed | None |
| Scientific validation | Not evaluated | Synthetic parent; no material comparator | None |
| Uncertainty quantification | Not evaluated | Thresholds are not uncertainty models | None |
| Human acceptance | Not evaluated | Architecture and controls remain draft | None |

## Limitations and deviations

The exact spectral weights, coefficient-box rule, thresholds, separation resolution,
outward-rounding implementation, and final manuscript placement remain unresolved. The
draft therefore defines ownership and proof obligations but does not freeze numerical
controls. Class pages below are prospective contracts and intentionally have no current
code, test, or Sphinx mapping.
