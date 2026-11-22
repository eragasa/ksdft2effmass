# Independent S30 identification review

**ReviewOutcome: NO_BLOCKING_FINDINGS**  
**OperatorRequest: NONE**

## Scope and version

Read-only scientific identification review—not numerical verification or source admission.

Reviewed `calculations/Si/bulk/analysis/wannier-window-remedy/s30-state-space-identification.md`, supplied original SHA-256:

`06da1f2590c2700380efce4b90b2d25e2e4abcc828bc7701bda99f800c7c3610`

No revision was requested or inspected; no revised hash applies. Hashes and supplied branch/HEAD were not independently recomputed. `watchdog_diff` identified the statement as untracked in the deliberately dirty worktree.

Below, calculation paths are relative to `calculations/Si/bulk/`.

## Association verdict

**The particular full-S30 association obligation is supportable, conditionally, on CSD0’s declared 216-point domain.** The statement identifies the entire encoded model—not merely AMN/U lineage—and supplies its native physical-space interpretation at every construction index. Under its explicit source-lineage, backend-frame and numerical-model assumptions, no additional physical map is missing for that bounded association.

The distinction is important:

- The **whole finite matrix family** is identified on the reciprocal torus.
- Its **physical association is identified at the 216 native source indices** through modeled `J_j`.
- Those maps collectively identify the sampled coordinate fibres with their native retained spaces. They do **not** identify the infinite convolution-model Hilbert space with sampled KS states.

CSD0 declares 216 construction points and separates identification from physical adequacy (`research-protocol/controlled-reduction-protocol-hopping-first.tex:319–354`). It does not require an off-mesh KS embedding or global fidelity proof. Requiring those here would strengthen the controlling obligation.

This conclusion is **not full CSD0/CSD1-V passage**. Exact geometry/convention admission, reviewed assertions, complete producer/inventory evidence and scientific-owner adoption remain separate outstanding matters.

## Review

### Correct: complete represented object

Statement `:33–72` matches `run_analysis.py:349–382,421–424`: every HR entry receives both degeneracy weights, element-specific WS shifts are accumulated, and evaluation explicitly takes the Hermitian part with positive Fourier phase.

The retained result records 279 native and 383 effective representatives, without spatial truncation (`characterization-result.json:48–55`). S105 preserves that complete support rather than adding an embedding (`spatial-truncation-disposition.json:52–63`). S100’s opening bindings identify the supplied S30 implementation and result hashes.

The finite Laurent/convolution claim is mathematically justified; the statement correctly withholds an authenticated infinite physical Wannier basis.

### Correct: maps, metric and approximation boundary

Statement `:76–118,129–147` correctly distinguishes:

- physical twenty-band `H_j^20` from its coordinate matrix `E_j`;
- modeled S-orthonormal `Phi_j`, retained `V_j` and isometric `J_j`;
- parsed, not exactly isometric, `W_file,j`;
- compression from invariant restriction or complementary-sector downfolding.

`J_j sharp H_j^20 J_j` and `J_j H_S30(q_j^U) J_j sharp` have the stated domains and directions. No normalization, inverse repair or second ultrasoft S factor is introduced. This agrees with Appendix C’s operator/compression distinctions and QE reference `pw2wannier90.f90:5132–5225`.

The actual implementation forms parsed `W† E W` (`run_analysis.py:448–494`). Its retained reconstruction comparison and printing-bound correction establish neither exact matrix equality nor certified physical-model error (`:663–781`; retained result `:1323–1371`).

### Correct: native association is explicit, not geometry equality

Statement `:152–183` preserves `q_j^U` while associating its fibre by authenticated source index with native point `j`. This is a defensible source relationship—not a claim that nominal and native Cartesian wavevectors coincide.

Converter records, localization input/output manifests and execution correlate EIG/AMN/MMN with U/U_dis/HR/WSvec. The parent remains historical scalar USPP, not production PseudoDojo. Source-to-historical-build correspondence and modeled frame conditions remain assumptions, not attestations.

Fixed-payload loading has no lattice argument (`run_analysis.py:533–578`). Upstream geometry dependence remains explicit: Wannier90 `ws_distance.F90:66–144` uses lattice/centres; `hamiltonian.F90:209–303` constructs gauge-transformed Fourier data. Nominal valley, mass and radius diagnostics are not relabeled as native-geometry results.

### Correct: relocated evidence and controls

The original relative EIG directory lacks `silicon.eig`. The converter names the external EIG; its recorded 168480-byte identity agrees with S30 and the parent audit’s relocated check. Statement `:211–217` correctly distinguishes that evidence from fallback admission or historical replayability.

Full CSD0 remains unconditional (`:201–207`). Thresholds, windows, energy/spin conventions and historical bindings are preserved.

## Finding

**FindingDisposition: NO_ACTION_REQUIRED**

**Problem assessed:** Whether finite source-point maps leave the required full-S30 association incomplete.

**Evidence:** Complete-model identification at statement `:33–72`, explicit maps at `:129–147`, and CSD0’s construction-point scope at protocol `:319–354`.

**Consequence:** No additional map is required for the stated sampled-domain association under the disclosed assumptions. A stronger physical association over arbitrary off-mesh points would require a compatible native embedding family `J(q)`, its gauge/sewing conventions and provenance—not merely smooth model coefficients. That stronger claim is neither established nor required here.

**Next action:** None for this statement. Preserve the admission stop and separate adoption/prerequisite process.

**No issues found.**

## Limits and residual risks

I read the named implementation seams, retained results/correction, protocol, admission contracts, lineage records, geometry proposals/reviews, architecture/Appendix C and reference-source sections. Parent hash checks, packing checks and residuals were inspected as recorded observations, not independently reproduced.

No files/settings were changed; no commands, calculators, replay, producer or verifier were run; no withheld402 values, wavefunction contents, assertions or receipts were produced or inspected. Favorable identification review grants no execution or admission permission.