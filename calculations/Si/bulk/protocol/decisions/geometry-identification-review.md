# Geometry-identification draft review

**ReviewOutcome: NO_BLOCKING_FINDINGS**  
**OperatorRequest: NONE**

**Ready to PRESENT for scientific-owner adoption decision: yes, as revised.** This is readiness of a conditional proposal—not adoption, source admission, completed CSD0/CSD1-V, scientific validation, or permission to emit a canonical state assertion.

## Version reviewed

Artifact: `calculations/Si/bulk/protocol/decisions/geometry-identification-draft.md`.

- Original: supplied 188-line version, SHA-256 `f71c53b7737e11d6c2da8be2f50aececa78e9ee671b15c15fc94f582b0815da2`.
- Focused parent revision: SHA-256 supplied as `37350ba5faa840162ec2ac16be438b2191bca71a36cfb67aaf2c9eef095a15cf`. I inspected the replacement paragraph and reread the complete revised draft.
- Branch and HEAD are as supplied. Neither hashes nor Git identity were independently recomputed.

Paths below are relative to `calculations/Si/bulk/` unless otherwise stated.

## Review

### Corrected finding: full CSD0 scope is unconditional

**Disposition: NO_ACTION_REQUIRED**

**Problem:** Original draft lines 143–146 made additional CSD0 obligations conditional, although the controlling protocol already requires authentication of the full-source physical and represented spaces.

**Evidence:** `research-protocol/controlled-reduction-protocol-hopping-first.tex:311–345,349–354` binds S30/S105/S110 and requires exact source, geometry, point, basis, gauge, unit and reference associations. Revised draft `:143–151` now explicitly preserves those obligations, identifies native coefficient-space authentication as only a sub-obligation, and stops full CSD0/CSD1 eligibility while the S30 nominal/native physical-space association remains unresolved.

**Consequence:** The revised text no longer permits pointwise lineage to substitute for full CSD0. It correctly identifies any intended pointwise replacement gate as requiring a **substantive amendment**, not this clarification.

**Next action:** None for this correction. The parent applied it; I made no edits.

### Technical assessment

- **Native association is coherent but insufficient for full admission.** Authenticated AMN and U_dis/U lineage, ordered band/point associations and projection semantics can identify their common native coefficient frame. Separately identifying nominal declarations prevents false geometry equality; it does **not**, by itself, resolve S30’s full physical/represented-space association. Revised `:143–151` makes that limitation decisive rather than merely postponing it.

- **Geometry and units are consistently distinguished.** S30 `characterization-result.json:5–40`, nominal S1 structure, NSCF `input/pw.in:27–34`, localization WIN `:21–31`, external NNKP `:5–24`, and NSCF XML `:365–377` support the listed declarations. The column-matrix convention agrees with the transposed vector-per-line inputs. Seven-decimal NNKP lattice entries are distinct from eight-decimal k-points. Nominal quarter-site floats are not silently equated with rendered decimal quarters.

- **Index association is not physical-wavevector identity.** Draft `:101–107,133–137` retains separate fractional presentations and native Cartesian records and forbids invented permutations, snapping and nearest-neighbor matching. The stated reciprocal conversion is consistent with column lattice vectors. Native and nominal Cartesian wavevectors are not asserted equal.

- **Overlap conventions remain bounded.** QE reference `pw2wannier90.f90:5132–5225` supports the ultrasoft `A=Ψ†SG` interpretation; its guiding-function comments near `:6620` reject pointwise normalization. Wannier90 projection definitions `projections.tex:339–349`, packed-window handling in `disentangle.F90:699–722,1019–1026`, and matrix output in `plot.F90:1661–1680` support the stated conventions, conditional on the retained occurrence associations. Reading these sources does not attest historical executable correspondence or independently establish full-grid packing checks.

- **No tolerance waiver or downstream reinterpretation is introduced.** Revised draft preserves the raw threshold, printing/parsing and arithmetic obligations, spin/trial conventions and original bindings. It withholds geometry-dependent distance, localization, hopping, sewing, velocity and mass claims. This respects the physical specification’s geometry/error separation and the numerical specification’s lattice-refinement—not identity—rule.

- **Adoption and migration remain separate.** Draft `:176–195` protects historical hash-bound requests and snapshots and introduces neither execution permission nor a generic verification framework. `native_inputs.py:107–119` and `source_admission.py:135–138,210–220,256–294` confirm that opaque labels and matching serialized declarations cannot prove scientific associations or replace actual prerequisite evidence.

**No issues found.**

## Evidence inspected and limitations

I inspected the bounded working-tree inventory and relevant protocol delta; the draft, dossier, prior review and preflight; request and S30 lattice/source entries; nominal S1; NSCF input, execution, saved-state-manifest excerpt and native XML excerpts; converter input/result; localization WIN, input/output manifests, execution and external inventory; NNKP and U/U_dis excerpts; relevant physical/numerical specifications; and the named QE/Wannier90 reference-source sections.

I did not run commands, hashes, tests, calculators, producer, verifier or replay; inspect withheld402 values or wavefunction contents; create assertions/receipts; or alter files/settings. Reported residuals, extrema, hash checks and full-grid observations remain parent observations—not independent recomputations.

Outstanding evidence remains precisely the full S30 nominal/native physical-space association and complete source-bound producer/inventory prerequisites. These do not block presenting this explicitly stopped proposal. They **do** block treating its review as actual source admission. Source-to-build correspondence and rounding assumptions also remain disclosed assumptions.