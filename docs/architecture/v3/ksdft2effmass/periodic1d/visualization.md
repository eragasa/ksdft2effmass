# Visualization migration plan

## Temporary status and destination

This page is temporary Architecture v3 planning documentation. It is not the maintained
runtime owner of plot names, projection fields, rendering inventories, or figure
behavior.

Each study implementation migrates its section into the appropriate installed source
subpackage. The source owner provides concrete typed classes for:

- authenticated visualization data;
- a closed plot enumeration;
- model-specific plot, subplot, and figure actions as needed;
- encoding-only figure renderers; and
- the family visualizer that checks verification and projection digests.

Calculation-side `run_03_render.py` scripts compose those classes and own only paths,
atomic publication, report assembly, and execution-specific provenance. They do not
reimplement plot behavior.

The expected destinations are:

| Study | Source destination or prospective destination |
|---|---|
| Mathieu1D | Implemented by `ksdft2effmass.model_systems.mathieu1d.visualization` |
| Compatible rank-one control | `ksdft2effmass.periodic1d.fourier_locality.visualization` |
| Rank-two band equivalence | `ksdft2effmass.periodic1d.band_equivalence_locality.visualization` |
| Rank-two composite alignment | `ksdft2effmass.periodic1d.composite_band_alignment.visualization` |
| Confirmatory admissible sets | `ksdft2effmass.periodic1d.admissible_sets.confirmatory_visualization` |
| Scalar/direct demonstration | `ksdft2effmass.periodic1d.admissible_sets.scalar_demonstration_visualization` |
| Threshold sensitivity | `ksdft2effmass.periodic1d.admissible_sets.threshold_sensitivity_visualization` |
| Higher-rank composite alignment | A cohesive higher-rank source owner selected in Phase 5 after its reusable behavior is established; no placeholder package is created by this plan. |

The Mathieu1D path is implemented and documented under
[`model_systems.mathieu1d`](../model_systems/mathieu1d/index.md). The other destinations
are prospective and become supported only in their implementation slices. There is no generic `Periodic1DVisualizationData`, universal Periodic1D plot
enum, or compatibility facade.

After all eight sections have implemented source owners, public API documentation, and
tests, this page is reduced to links to those source contracts or removed through a
reviewed documentation cleanup. It must not remain a competing normative plot catalog.

## Closed planning inventory

Periodic1D renders **eight baseline PNG figures**, one for each separate study. Every
baseline figure consumes only the authenticated typed projection derived during
independent KSD verification.

A study may additionally render **one certificate-obligation PNG** only after it has an
admitted compact certificate export and checker result. The execution declares either a
`native_only` or `native_plus_certificate` inventory before rendering. A certificate
placeholder is never emitted.

Therefore the program has:

- exactly 8 baseline figures; and
- from 0 to 8 certificate supplements, each bound to one actual checked export.

A plot presents already calculated or checked values. It is not itself verification,
proof, scientific acceptance, or additional evidence.

## Shared rendering rules

- Every point, curve, interval, threshold, support boundary, witness, category, and
  highlighted decision exists in the authenticated projection before rendering.
- The renderer may select axes and scales but does not calculate new scientific values.
- Connected markers are visual guides across an explicitly ordered finite inventory,
  not interpolation.
- Captions say `declared finite inventory` where connected markers are used.
- Outward interval whiskers are enclosure bounds, not statistical error bars.
- Rejected, unresolved, failed, and unavailable cases remain visible.
- Threshold lines, Pareto flags, first-passing markers, and witness selections are
  verifier or checker outputs rather than renderer decisions.
- Each baseline or certificate item is one PNG. PDF and report derivatives remain
  report outputs unless a family explicitly admits them into a separate closed
  inventory.

## 1. Mathieu1D direct vertical slice — migrated

The runtime contract now belongs to
`ksdft2effmass.model_systems.mathieu1d.visualization`; this temporary page no longer owns
its projection fields or plot composition. The closed native inventory contains
`mathieu1d-finite-reduction.png` and `mathieu1d-publication-summary.png`. Concrete typed
projection, plot, subplot, figure, renderer, plot-enum, and authenticated visualizer
classes own both layouts. The complete view has four recorded panels: finite
representation refinement, the ordered finite evaluation inventory, complete
finite-transform hopping magnitudes, and range-indexed diagnostics. The compact
publication view reuses only authenticated range errors and omitted-block norms; it
derives no additional scientific values.

The implementation emits no certificate supplement because no certificate export or
checker result is admitted. It draws no continuum-convergence rate, inferred uncertainty
band, smooth feasibility region, or claim that a sampled gap proves continuum isolation.

## 2. Compatible rank-one Fourier-locality control

### Baseline

`rank1-fourier-locality.png`, three panels:

1. declared momentum versus scalar represented energy, overlaying the direct field,
   complete Fourier reconstruction, and selected finite-support reconstructions;
2. centered cell representative versus `|t_R| / E_ref`, with support markers; and
3. support identifier versus separately authenticated interpolation, truncation, total
   evaluation, and fit-route errors, with declared thresholds and the actual finite
   first-passing member.

### Certificate supplement

`rank1-fourier-certificate-obligations.png` is limited to finite transform/inversion,
Parseval/tail, support, and scalar-conjugation obligations.

### Excluded

No gauge angle, phase optimization, gauge-locality, or alignment-improvement plot.
Scalar `U(1)` conjugation is operator-trivial. Phase-unwrapping, localization, and
continuum-decay claims are outside this study.

## 3. Rank-two band equivalence versus hopping locality

### Baseline

`rank2-band-equivalence-locality.png`, four panels:

1. **Bands** — declared momentum versus ordered lower and upper energies for the
   reference and candidate, using stable case and alignment identifiers.
2. **Pointwise spectral discrepancy** — the same finite momentum inventory versus the
   maximum ordered-band difference divided by `E_ref`, with the numerical verification
   tolerance.
3. **Locality** — centered cell representative versus block Frobenius norm
   `||T_R||_F / E_ref`, one trace per represented Hamiltonian under the same declared
   comparison alignment.
4. **Finite truncation consequence** — support identifier versus separate spectral and
   operator/Frobenius errors, normalized by their own declared thresholds when shown on
   one axis. Only actual common passing decisions are marked.

### Certificate supplement

`rank2-band-equivalence-certificate-obligations.png` contains:

1. outward intervals for ordered-band discrepancy and the certified unnormalized
   Frobenius bound, indexed by finite case and momentum; and
2. exact or enclosing values for every scalar, support, and alignment premise, with its
   boundary and checker status.

The supplement does not label a stronger normalized spectral bound as proved unless the
checked theorem inventory actually includes it.

### Excluded

No invisible equal-spectrum overplot presented as proof, interpolated continuum momentum
curve, locality envelope assembled from different representations, or inference that
pointwise spectral equivalence ensures finite-range adequacy.

## 4. Rank-two composite-band alignment and locality

### Baseline

`rank2-alignment-locality.png`, four panels:

1. declared momentum versus alignment objective or residual, with separate unaligned,
   global-fixed, pointwise, and declared analytical-control channels;
2. momentum or case identifier versus independently verified sewing residual and
   conditioning diagnostics, using separate axes when units differ and explicit markers
   for failed qualifications;
3. centered cell representative versus `||T_R||_F / E_ref`, separated by alignment
   channel; and
4. support identifier versus separate spectral and operator interpolation/truncation
   consequences, showing only attainable channel/support decisions.

### Certificate supplement

`rank2-alignment-certificate-obligations.png` displays exact or enclosing unitarity,
Frobenius-invariance, Fourier-equivariance, and support obligations for the fixed/global
channel. Point-dependent channels are labeled as separate finite reconstructions and do
not inherit fixed-unitary conclusions.

### Excluded

No curve implying that point-dependent `U(k)` commutes with Fourier transformation, no
best-gauge claim across incomparable families, no topology panel, and no silent omission
of failed conditioning cases.

## 5. Confirmatory constrained admissible sets

### Baseline

`confirmatory-admissible-sets.png`, two panels:

1. declared `s` versus declared `lambda`, plotting the actual finite candidate inventory
   with categorical markers for spectral-only pass, operator-only pass, joint pass,
   fail-both, and unresolved. Show the prespecified domain boundary without filling
   between sampled points.
2. authenticated spectral loss versus authenticated operator loss for the same
   candidates, with prespecified threshold lines and only genuine common witnesses
   highlighted. Candidate, support, and alignment identifiers remain inspectable in the
   projection and caption.

### Certificate supplement

`confirmatory-admissible-certificate-obligations.png`, two panels:

1. exact or enclosing ellipse geometry, candidate rectangle, encoded witness, and
   certified separation segment or gap. Interval-enclosed parameters use conservative
   boundary bands rather than one falsely exact curve.
2. interval whiskers for the recorded quadratic and geometric premises, containment,
   witness, and separation margins, with checker status.

### Excluded

No interpolated feasibility heatmap, convex hull, smoothed boundary from samples,
channel-wise minima from different candidates, or filled proof region not derived from
exact or enclosing certificate geometry.

## 6. Minimal scalar/direct admissible-set demonstration

### Baseline

`scalar-direct-admissible-demonstration.png`, two panels:

1. the declared scalar parameter domain, plotting only directly evaluated candidates,
   their two channel classifications, and the declared witness; and
2. candidate or parameter versus the two authenticated loss values, separated by axes
   or normalized by their own thresholds, with declared budgets.

### Certificate supplement

`scalar-direct-certificate-geometry.png` displays exact algebraic or outward-enclosed
sublevel boundaries, the witness, certified separation, and a compact obligation-status
panel.

### Excluded

No presentation as confirmatory evidence, extension of one witness to an entire family,
or continuous feasible region drawn from binary64 samples without an exact or interval
certificate.

## 7. Post-hoc threshold sensitivity

### Baseline

`threshold-sensitivity-finite-ledger.png`, two panels:

1. enumerated spectral threshold versus enumerated operator threshold, with one discrete
   marker per declared pair categorized as common pass, no common pass, or unresolved.
   Highlight the original confirmatory pair without changing it.
2. spectral objective versus operator objective for every attainable finite decision,
   with the selected threshold rectangle, finite Pareto-efficient points, and the actual
   selected common witness. Use points only, with no hull or interpolated front.

For a one-dimensional sensitivity inventory, panel 1 instead uses the declared threshold
index or value versus categorical disposition and actual first-passing support or cost.
Every earlier member is inspected; no monotonicity is inferred.

### Certificate supplement

`threshold-sensitivity-certificate-obligations.png` shows each decision and channel's
exact value or outward interval against its threshold, visible unresolved overlaps, and
the checker-derived finite mask or first-passage status.

### Excluded

No continuous phase boundary, interpolated threshold surface, monotone fit, componentwise
best envelope, curve through unattainable objective pairs, or relabeling of a post-hoc
threshold as confirmatory.

## 8. Higher-rank composite alignment and locality

### Baseline

`higher-rank-alignment-locality.png`, four panels or fixed small multiples:

1. **Qualification matrix** — declared depth or case versus retained rank, faceted by
   alignment family, with categorical qualified, reason-coded failure, and unavailable
   cells.
2. **Alignment and sewing diagnostics** — stable case identifier versus authenticated
   alignment residual, sewing residual, or conditioning quantity, separated by unit or
   scale.
3. **Finite locality** — support identifier versus separate interpolation and truncation
   errors for every actual qualified rank, depth, and alignment case. Small multiples
   are preferred to an unreadable aggregate.
4. **Attainable decision set** — cost or support versus one declared objective, with the
   second objective in a second small multiple or marker field. Mark only actual finite
   Pareto-efficient decisions and retain case and alignment identifiers.

### Certificate supplement

`higher-rank-certificate-obligations.png` shows exact or enclosing obligations for the
fixed-global unitary channel, finite Fourier and support relations, and any checked
finite decision table. Pointwise alignment receives no fixed-unitary equivariance mark.
Each rank and depth case remains separate.

### Excluded

No line across rank or depth implying a scaling law, rank-limit extrapolation,
componentwise Pareto envelope, merged feasible set across alignment families,
point-dependent conclusion borrowed from a fixed-unitary theorem, or inference from rank
two to higher rank.

## Migration completion gate

A study's section moves out of this temporary page only after its implementation provides:

1. a typed projection derived by the byte-owning verifier;
2. a closed enum with exact renderer-inventory equality;
3. concrete plot, subplot, figure, renderer, and visualizer classes appropriate to the
   figure rather than empty marker classes;
4. tests for digest correlation, failed-verification rejection, projection tampering,
   enum closure, filenames, and admitted PNG bytes;
5. public API and Architecture v3 documentation at the source owner; and
6. a thin direct render script that performs no scientific calculation.

The implementation review copies no calculation-local plotting kernel into source
without assigning it to a cohesive domain class. Once migrated, changes occur at the
source owner and its tests rather than by editing this planning inventory.

## Global exclusions

Do not title or caption a plot as proof, formal validation, continuum convergence,
uncertainty, global optimum, or universal locality unless a separately owned contract
establishes that exact claim. Mesh and cutoff comparisons remain discrete finite
diagnostics: no asymptotic fit, extrapolated intercept, confidence band, or inferred
rate is rendered.

Smooth heatmaps, splines, triangulations, hulls, and componentwise envelopes are excluded
unless every displayed value is an authenticated attainable decision or an exact or
enclosing analytic set admitted from a checker result. A certificate supplement is a
presentation of checked obligations; visual appearance supplies no additional theorem.
