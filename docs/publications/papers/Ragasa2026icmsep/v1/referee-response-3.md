# Response to technical review 3 — silicon results and numerical conclusions

## Review disposition

- **Review outcome:** `CHANGES_REQUIRED`
- **Operator request:** `NONE`
- **Manuscript status:** silicon prose revised; independent reconstruction remains a publication blocker

The review is accepted. Its numerical reading is consistent with the retained evidence.
The requested evidence-boundary and interpretation changes have been made in the main
text. No new silicon calculation, fitting, threshold selection, QE execution,
Wannier90 execution, or SOC campaign was performed for this response.

## Responses and revisions

### 1. Producer-checked evidence status

**Disposition:** `NO_ACTION_REQUIRED` after revision

A prominent evidence box now opens the silicon-results section. It states that all
silicon results are authenticated producer-checked development calculations pending
independent reconstruction and are not an independently verified material
demonstration.

The same box separates the three reference roles:

1. the full rank-10 Wannier source is the reduction-fidelity reference;
2. the revealed DFT parent is the source-adequacy reference; and
3. experiment is not evaluated.

The gauge result remains described as spectrum preservation on the declared 408-point
inventory, while the finite-cyclic interpolation floors remain assigned to construction
and conversion rather than to the gauge attack.

### 2. Support-error frontier scope

**Disposition:** `NO_ACTION_REQUIRED` after revision

The prose now consistently describes the results as **observed support-error
frontiers** over the exhaustive declared finite support inventory. It explicitly states
that they are not universal support bounds and that equal-attained-error comparisons are
discrete rather than continuous interpolation in physical radius or support count.

### 3. Literal deletion, refitting, and coefficient bounds

**Disposition:** `NO_ACTION_REQUIRED` after revision

The literal H-shell-16 result is now identified as a near-full-support reduction:
371 of 383 representatives, or 96.9% of the source. It is not described as a compact
short-range model.

The refitted H-shell-16 examples remain constructive witnesses rather than optima. The
main text now reports that neither displayed H-shell-16 witness has an active coefficient
bound. All retained bound-active records occur only on H-shell-02, H-shell-06, and
H-shell-08. Gray cells continue to mean “no witness found by the bounded multistart
search,” not infeasibility.

### 4. Fidelity ladder and H-shell-10

**Disposition:** `NO_ACTION_REQUIRED` after revision

The silicon-results text now states directly that H-shell-10 is not a reliable
band-edge reduction: its dense all-band spectral RMS is 0.02785 eV, while a principal
conduction mass changes by 53.2%. The manuscript retains Parseval operator RMS as the
exact integrated finite-Fourier measure and describes the 12³–32³ comparison only as
stability over the tested mesh sequence.

### 5. Conduction search scope and mass conventions

**Disposition:** `NO_ACTION_REQUIRED` after revision

The results now use “identified conduction-sector minima” and place the search scope
next to the numerical conclusions: six signed-axis sectors, eight 32³ coarse starts plus
the source coordinate, a Cartesian refinement box of ±0.12 Å⁻¹, 240 iterations,
function tolerance 10⁻¹⁴, and gradient tolerance 10⁻¹⁰. The text explicitly denies a
global Brillouin-zone certificate.

DOS and conductivity masses are again identified adjacent to their values as curvature
conventions, not carrier-transport predictions.

### 6. Valence-manifold conclusion

**Disposition:** `NO_ACTION_REQUIRED` after revision

The main text now states the conceptual result explicitly:

> Subspace fidelity does not imply internal Hamiltonian fidelity.

The transported three-band quadratic Hamiltonian remains the primary valence object.
Ordered branches remain instability diagnostics only, and the non-SOC channels are not
assigned physical HH, LH, split-off, Luttinger, or acceptor meanings.

### 7. Symmetry-equivalent-point interpretation

**Disposition:** `NO_ACTION_REQUIRED` after revision

The text now says that the reductions introduce numerical inequivalence among points
that are symmetry-equivalent in the declared source construction. It explicitly denies
that the spreads independently establish exact physical silicon symmetry or an
experimentally established symmetry violation.

### 8. Role of the silicon case study

**Disposition:** `NO_ACTION_REQUIRED` after revision

The Discussion now assigns the central mathematical claim to the exact rank-two result
and presents silicon as a bounded material-derived application. The Conclusions retain
the silicon qualitative mechanism but label it producer-checked, use “observed
support-error frontiers,” and describe H-shell-16 as a 371-of-383 near-full-support
reduction.

### 9. Independent reconstruction

**Disposition:** `MUST_FIX`

Prose cannot resolve the principal evidence limitation. Before publication-qualified
claims, an independent implementation must reconstruct, from authenticated source
bytes:

1. the rank-10 attack and complete-spectrum invariance;
2. alignment, Fourier conversion, support curves, and Parseval channels;
3. literal and refitted frozen-model metrics; and
4. the fidelity-ladder, conduction, valence, and symmetry diagnostics.

The retained scientific selections and frozen models must not be changed during that
reconstruction. Passing producer tests or manuscript compilation does not satisfy this
requirement.
