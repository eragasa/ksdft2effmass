# Paper 1 v3 claim and commitment inventory

## Purpose

This is the complete audit ledger for what Paper 1 v3 presents, relies on, explicitly
excludes, or promises as later work. It is an editorial and readiness aid, not a new
scientific authority or evidence package. Mathematical definitions remain authoritative
in the manuscript and supplement; numerical provenance remains owned by the maintained
1-D experiment and its calculation records.

The inventory covers `manuscript.tex`, `supplementary.tex`, `README.md`, and
`novelty-and-convention-audit.md`. “Delivered” means that the working paper currently
contains the stated proof, implementation, or bounded development result. It does not
mean reviewed publication evidence.

## Status vocabulary

- **Analytic—delivered:** proved in the paper under explicit assumptions.
- **Development—delivered:** implemented and observed on a declared sampled inventory,
  but not retained publication evidence.
- **Contract—delivered:** a method, definition, boundary, or failure rule is explicit.
- **Follow-up—active:** another maintained experiment now exercises the promised rung,
  but it is not evidence for Paper 1 v3.
- **Open before submission:** required to support the current numerical headline as
  final publication evidence.
- **Outside Paper 1:** deliberately excluded and must not be imported as Paper 1
  evidence.

## 1. Central contribution and novelty boundary

| ID | What the paper sells | Exact scope | Status and owner |
|---|---|---|---|
| C01 | Band equivalence does not determine hopping locality. | Pointwise unitary-equivalent finite-rank Bloch fields can have different Fourier hopping distributions in declared coordinates. | **Analytic—delivered**; main Eqs. for the attacked field and hopping convolution. |
| C02 | Representation efficiency must be compared at equal accuracy, not merely equal cutoff. | Finite ordinary-lattice truncations of two complete gauge-related representations; sampled band and matrix criteria remain separate. | **Development—delivered** by the maintained 1-D experiment. |
| C03 | The contribution is the combined analytic-to-dispersive benchmark and channel-resolved protocol. | No priority claim for gauge-dependent locality, Wannier localization, hopping truncation, Procrustes alignment, Parseval, or Weyl bounds individually. | **Contract—delivered** in Background and the novelty audit. |
| C04 | Complete gauge-related fields remain physically equivalent before truncation. | Equality is under the generating momentum-dependent unitary; the nonzero residual uses only the restricted global alignment family. | **Contract—delivered** and repeated throughout the manuscript. |
| C05 | Locality cost is representation efficiency, not an observable physical inequivalence. | The reported cutoff and block-count costs belong to the declared basis, gauge, support rule, and accuracy criterion. | **Contract—delivered**. |
| C06 | The alignment diagnostic is not the MLWF spread decomposition. | It is a contract-dependent cross-model Hamiltonian loss, not `Omega_I`, `Omega_tilde`, or a new localization principle. | **Analytic/contract—delivered** in Supplement S1.6 and related work. |

## 2. Analytic results

| ID | Result | Assumptions and boundary | Status |
|---|---|---|---|
| A01 | Spectral and aligned matrix losses have the same diagonal quadratic curvature `diag(1,kappa)`. | Rank two; positive trace–traceless affine candidate; positive weights; one global real rotation. | **Analytic—delivered**, Theorem 1 and Supplement S1.1. |
| A02 | The continuously optimized correlation is obtained from one second harmonic. | Global `SO(2)` interval; harmonic amplitude degeneracy handled explicitly. | **Analytic—delivered**. |
| A03 | Unconstrained admissible sets are homothetic ellipses with explicit centers, radii, compatibility, and distance. | Full ellipses must be contained in the declared parameter rectangle; otherwise the certificate premise is invalid. | **Analytic—delivered**, Corollary 1 and Supplement S1.2. |
| A04 | A band-only false positive can have a positive certified operator incompatibility. | The explicitly constructed two-observation example and stated thresholds/box only. | **Analytic—delivered**, Proposition 1 and Supplement S1.3. |
| A05 | For `U_a(q)=R(a sin 2 pi q)`, `mu_max=J_0(2a)`. | Flat real-symmetric traceless rank-two parent; `0 <= a <= pi/4`. | **Analytic—delivered**. |
| A06 | Minimum-operator and joint thresholds obey the displayed Bessel laws and are nondecreasing. | Same flat-parent and amplitude assumptions; finite parameter bounds are not included in the unconstrained formula. | **Analytic—delivered**, Corollary 2 and Supplement S1.4. |
| A07 | The squared irreducible residual equals normalized non-onsite Fourier power. | Spectrally flat traceless parent; the generating and allowed global maps use the same real rotation orbit. | **Analytic—delivered**, locality theorem and Supplement S1.5. |
| A08 | The exact-spectrum joint threshold separates into non-onsite power and onsite-block mismatch. | Same flat-parent family. | **Analytic—delivered**. |
| A09 | The finite uniform-transform analogue of the residual–power identity holds. | Declared discrete transform and normalization; it is not a continuous localization certificate. | **Analytic—delivered** and numerically checked. |
| A10 | A compact admissible alignment family attains its minimum; transported constant frame changes preserve the contract and excess. | Equal finite retained rank, nonempty compact map family, simultaneous transport of operators and admissible maps. | **Analytic—delivered**, Supplement S1.6; explicitly not claimed as novel. |
| A11 | Momentum-dependent similarity convolves hopping indices; a constant basis change does not increase support. | Compatible Fourier expansions in one state space. | **Analytic—delivered**. |
| A12 | Weyl and Parseval relationships are verification constraints, not new physical laws. | Rank-two normalization and declared finite Fourier inventory. | **Contract—delivered**. |

## 3. Model, state-space, and comparison contract

| ID | Contract item | Paper commitment | Status |
|---|---|---|---|
| M01 | Parent | One synthetic 1-D four-state nearest-cell Hamiltonian with the displayed `T_0,T_+1,T_-1`; no material parametrization. | **Contract—delivered**. |
| M02 | Retained state space | Lowest two spectral states, rejected if the second-to-third external isolation gap fails its gate. | **Contract—delivered**; final retained gate value remains open. |
| M03 | Frame | Neighbor SVD/Procrustes transport, full-rank overlap gate, endpoint holonomy, and distributed periodic closure. | **Contract—delivered** and implemented. |
| M04 | Frame meaning | No backend-independent canonical eigenvector frame is claimed; projectors and reconstructed observables carry invariant meaning. | **Contract—delivered**. |
| M05 | Comparison attack | Smooth periodic `U_a(q)=R(a sin 2 pi q)`, `0 <= a <= pi/4`; historical finite-angle attacks are excluded. | **Contract—delivered**. |
| M06 | Candidate family | Common mean field plus centroid shift `s E_ref` and positive splitting scale `lambda`. | **Contract—delivered**. |
| M07 | Allowed alignment | One momentum-independent real rotation over the half-open fundamental interval; no momentum-dependent or unrestricted complex alignment. | **Contract—delivered**. |
| M08 | Energy normalization | `E_ref` is an arbitrary positive reference energy, not a material band gap. | **Contract—delivered**. |
| M09 | Momentum convention | `q=k/G=ka_0/(2 pi)` and the negative-exponent forward Fourier transform. | **Contract—delivered** and cross-walked to v2. |
| M10 | Fourier inventory | Centered finite-cyclic blocks, cyclic Nyquist semantics, ordinary-lattice conversion before truncation, and conjugate-closed supports. | **Contract—delivered** and implemented. |
| M11 | Range decision | First passing integer cutoff on every `R_c=0,...,16`; failure within the cap remains unresolved. | **Development contract—delivered**; final cap/expansion rule remains open. |
| M12 | Error channels | Cyclic conversion power, interpolation, deliberate truncation, and total error remain separate and are not added. | **Contract—delivered** and implemented for matrix and sorted-band errors. |
| M13 | Two accuracy questions | Rank-normalized Hamiltonian and band-error cutoffs remain separately named; neither is substituted for the other. | **Contract—delivered**. |
| M14 | Diagnostic order | Gap/subspace and frame/sewing gates precede alignment, Fourier locality, consequences, and cutoff decisions. | **Contract—delivered**. |
| M15 | Failure semantics | Failed numerical gates are calculation failures; empty components, invalid premises, or insufficient margins are unresolved scientific outcomes. | **Contract—delivered**. |

## 4. Numerical results actually presented

| ID | Presented result | Evidence boundary | Status |
|---|---|---|---|
| N01 | Flat complete bands agree to `2.22e-16`. | Synthetic flat family and binary64 development calculation. | **Development—delivered**. |
| N02 | At `a=pi/4`, normalized flat thresholds are `0.8815978972` and `1.0276174232`. | Direct Bessel formulas; analytic in amplitude. | **Analytic—delivered**, numerically evaluated. |
| N03 | Flat non-onsite power is `0.7772149` at `a=pi/4`; range-four tail is about `1.03e-5`. | `N=512` finite transform; not a continuum support certificate. | **Development—delivered**. |
| N04 | Flat momentum refinement is roundoff-limited over `N=32,...,512`. | Implemented channels and draft tolerances only. | **Development—delivered**. |
| N05 | The uniform amplitude interpolant fails the draft target and is not used. | Diagnostic grids through the stated interval counts. | **Development—delivered**; this is a rejected method, not an unresolved analytic claim. |
| N06 | Dispersive endpoint is sampled-gapped and frame-qualified. | At `N=512`: sampled gap `1.0566461 E_ref`, overlap singular value `0.9999997323`. | **Development—delivered**. |
| N07 | Dispersive complete bands agree to about `1.45e-15`; endpoint thresholds are `0.4004394264` and `0.4611609032`. | Directly sampled amplitudes only. | **Development—delivered**. |
| N08 | Dispersive comparison non-onsite power rises from `0.0323839143` to `0.1761532501`. | Finite-mesh blocks and declared frame. | **Development—delivered**. |
| N09 | Non-flat momentum study is converged under its declared refinement checks. | Momentum only; not continuous in amplitude and not retained evidence. | **Development—delivered**. |
| N10 | Restricted mismatch and excess non-onsite power persist across five sampled parent scales and 33 amplitudes. | Finite `rho` and amplitude inventory; no continuous-domain certificate. | **Development—delivered**. |
| N11 | The flat residual–tail identity deforms systematically with parent dispersion. | Calculated relation and cross term; no non-flat equality theorem. | **Development—delivered**. |
| N12 | Endpoint truncation at `R_c=3` gives reference/comparison band errors about `5.53e-8` and `1.86e-2 E_ref`; at `R_c=8`, about `4.22e-14` and `8.65e-7 E_ref`. | Sampled endpoint and disjoint evaluation mesh. | **Development—delivered**. |
| N13 | At `10^-8 E_ref`, endpoint first-passing band cutoffs are 4 and 10, so sampled inflation is 6. | Dense integer inventory `0,...,16`; development result. | **Development—delivered**; central numerical headline. |
| N14 | Endpoint band cutoffs at `10^-6,10^-8,10^-10,10^-12` are `(3,8),(4,10),(6,12),(7,14)`. | Same sampled endpoint and cap. | **Development—delivered**. |
| N15 | Positive sampled band inflation occurs at 159/165 points for `10^-6` and `10^-8`, and 156/165 for `10^-10` and `10^-12`. | Five parent scales by 33 amplitudes. | **Development—delivered**. |
| N16 | Hamiltonian and band criteria give the same `10^-8` endpoint cutoffs; comparison decisions agree at 158/165 points. | Different normalizations remain separate. | **Development—delivered**. |
| N17 | Nyquist conversion is about `1e-31 E_ref^2`; maximum interpolation band error is `2.35e-14 E_ref`. | Sampled inventory; conversion power is not a spectral error. | **Development—delivered**. |
| N18 | At endpoint, truncation error falls from `5.25e-1` at range zero to `8.65e-7` at range eight and `2.78e-11 E_ref` at range twelve. | Deliberate truncation channel. | **Development—delivered**. |
| N19 | Every sampled spectral error satisfies the Frobenius perturbation bound; the saturation ratio spans about `0.0087`–`0.9984`. | Sampled ledger only. | **Development—delivered**. |
| N20 | First-passing decisions are unchanged at `N=128,256,512`; every selected cutoff passes and its predecessor fails. | Threshold-adjacent development refinement, not a retained run. | **Development—delivered**. |
| N21 | Independent truncation reconstruction differs by at most `4.61e-13`. | Same binary64 ecosystem, separate control flow rather than independent hardware. | **Development—delivered**. |
| N22 | Frame and transform identities close near binary64 scale; closure phases remain non-topological diagnostics. | Five sampled parent scales. | **Development—delivered**. |

## 5. Software verification, serialization, and provenance sold by the paper

| ID | Commitment | Current state |
|---|---|---|
| V01 | Separate producer and verifier for the flat analytic family. | **Development—delivered**. |
| V02 | Separate producer and verifier for the smooth four-state parent/frame/Fourier calculation. | **Development—delivered** for current pointwise scope. |
| V03 | Separate producer and verifier for dense truncation and all first-passing decisions. | **Development—delivered**. |
| V04 | Strict development schemas reject unknown fields and invalid scalar types. | **Development—delivered** for smooth, non-flat, and truncation records. |
| V05 | Input/result digests bind applicable serialized records. | **Development—delivered**; no retained run identity is inferred. |
| V06 | Exact Optimization and PhysKit revisions are disclosed. | **Development—delivered** in the supplement and experiment README. |
| V07 | Analysis tables and figures are derived presentations, not independent provenance owners. | **Contract—delivered**. |
| V08 | Independent means separate scientific reconstruction/control flow, not different hardware, arithmetic, or all numerical libraries. | **Contract—delivered**. |
| V09 | A retained package would contain canonical records, convergence table, manifests, checksums, commands, platform, report, and distinct version/run/package identities. | **Open before submission**; this describes a future retained package only. |

## 6. Explicit nonclaims and exclusions

| ID | The paper does **not** sell | Required editorial behavior |
|---|---|---|
| X01 | Material validity, silicon, graphene, elasticity, phase stability, or a material deformation potential. | Keep all synthetic results labeled as such. |
| X02 | A Quantum ESPRESSO or Wannier90 calculation. | Do not import unrelated historical or later calculations as Paper 1 evidence. |
| X03 | Physical effective masses, velocities, or curvature errors. | Remain excluded until units, derivatives, internal nondegeneracy, and controls are reviewed. |
| X04 | Physical inequivalence of complete gauge-related Hamiltonians. | Always state pointwise unitary equivalence before truncation. |
| X05 | A universal hopping-range law, exponential-localization theorem, or universal tail-to-band-error bound. | Keep all cutoff results model-, mesh-, tolerance-, and inventory-specific. |
| X06 | Continuous non-flat dependence on amplitude or parent scale. | Keep non-flat statements pointwise; plotted lines are guides only. |
| X07 | A topological interpretation of closure phases. | Treat phases only as reciprocal-sewing diagnostics. |
| X08 | A canonical frame shared by numerical backends. | Report projector/reconstructed quantities and backend qualification. |
| X09 | An MLWF optimization or new Wannier-spread decomposition. | Preserve the explicit distinction in the related-work and covariance sections. |
| X10 | Full non-flat admissible-set, witness, or separation-certificate evidence. | Do not imply that the 14-step future certificate workflow has been executed. |
| X11 | Higher-dimensional, anisotropic, non-orthogonal, higher-rank, or complex-`U(N)` results **of Paper 1**. | Later experiment results may be cited as follow-up work only after separate review; they do not retroactively support Paper 1. |
| X12 | Retained, archived, released, or publication-qualified numerical evidence. | Keep development labels until the open readiness items are completed and separately authorized. |

## 7. Validation-ladder commitments

| ID | Rung sold in Paper 1 | Current repository status | Paper 1 relationship |
|---|---|---|---|
| R01 | 1-D rank-two global `SO(2)` known-parent benchmark. | Implemented analytic and bounded development centerpiece. | Current paper. |
| R02 | Independent 2-D orthogonal and non-orthogonal known-parent benchmarks. | Square and graphene-inspired/triangular families now have bounded smoke and first-refinement results. | **Follow-up—active**; not Paper 1 evidence. |
| R03 | Independent 3-D and anisotropic-support benchmarks. | Simple-cubic and silicon-inspired/FCC families now have bounded smoke and first-refinement results. | **Follow-up—active**; not Paper 1 evidence. |
| R04 | General non-orthogonal cells and physical-metric complete supports. | Triangular and FCC experiment families implement this at bounded development scope. | **Follow-up—active**. |
| R05 | Geometry/gauge stress under known synthetic deformation. | Rhombic and Bain M0/M1/M2 development controls now exist. | Additional follow-up; not promised evidence in Paper 1. |
| R06 | Higher-rank real `SO(N)` comparisons. | Paper 3 contains bounded bridge/witness work, but not a general qualified higher-rank campaign. | Still incomplete as a validation-ladder rung. |
| R07 | Full complex non-Abelian `U(N)` classes. | No qualified general campaign. | Future work. |
| R08 | Hidden/material target with first-principles and Wannier90. | Reserved for Paper 4/material silicon; no authorized execution here. | Future protected stage. |
| R09 | Separate parent-model, discretization, reduction, gauge, and truncation errors at the material stage. | Architectural commitment only. | Future work. |

## 8. Items still required before Paper 1 v3 submission

These are not optional enhancements if the current numerical headline is to appear as
final publication evidence.

| ID | Required item | Why it remains open |
|---|---|---|
| S01 | Freeze the exact numerical claim set. | Decide whether the paper retains only the sampled range headline or also activates instance-specific admissible-set/certificate claims. |
| S02 | Freeze the external-gap and transport-overlap gates, including equality and margin policy. | Current values are draft/candidate controls. |
| S03 | Freeze channel-specific numerical tolerances. | The current shared draft tolerance is explicitly provisional. |
| S04 | Freeze the cutoff cap and prospective expansion/failure rule. | `0,...,16` is dense but remains a development cap. |
| S05 | Freeze construction/evaluation levels and coordinate-disjointness tolerance. | Current meshes are development choices. |
| S06 | Freeze exact dependency revisions and resolved environments. | The manuscript snapshot revisions are disclosed historically; a separately authorized confirmatory run still requires newly frozen revisions and a resolved environment, while current live development pins may advance. |
| S07 | Add retained schemas with immutable experiment-version and run identities. | Development schemas intentionally deny retained status. |
| S08 | Record exact source/dependency manifests, commands, platform, and checksums. | No retained evidence package exists. |
| S09 | Obtain separate authorization and execute the frozen local confirmatory calculation. | Protected retained-evidence execution has not been authorized merely by manuscript development. |
| S10 | Run the independent retained verifier and reject any mismatch or failed gate. | Development verification cannot be relabeled as retained verification. |
| S11 | Produce the readable retained report and public archival record/identifier. | The Data and Code Availability section currently promises these before submission. |
| S12 | Complete acknowledgments and final date/version metadata. | The manuscript still contains an author placeholder. |
| S13 | Re-run the novelty/convention audit if a priority, material, higher-dimensional, or continuous-domain range claim is added. | Required by the existing audit boundary. |
| S14 | Reduce any future roadmap updates without implying that follow-up smoke calculations are Paper 1 evidence. | The repository has advanced beyond the original “design only” wording. |
| S15 | Resolve the main-manuscript LaTeX warnings and visibly inspect the final two-column PDF. | The current build succeeds, but it still reports pre-existing underfull boxes, several overfull equations (including one about 57 pt), and a `nameref` package warning. The supplement builds cleanly. |

## 9. Scope-dependent items that are **not** blockers for the current headline

The following become required only if the manuscript expands its current claim set:

- full non-flat admissible-set quadratics and rectangle minima;
- parameter-rectangle freeze;
- spectral/operator admissibility thresholds for an instance-specific decision;
- witness search and original-residual verification;
- containment support points and conservative separation bounds;
- a declared separation resolution;
- post-decision evaluation of a selected witness;
- adaptive continuous-amplitude certification for the non-flat family;
- velocity, curvature, or effective-mass consequences; and
- higher-dimensional, higher-rank, material, or topology claims.

## 10. Audit conclusion

Paper 1 v3 currently sells one complete rank-two analytic mechanism and one strongly
checked but still development-status 1-D numerical consequence. The mathematics,
comparison contract, dense-cutoff result, diagnostic separation, and independent
development reconstruction are present. The remaining blockers are evidence-lifecycle
controls—freeze, retained identities and provenance, authorized confirmatory execution,
independent retained verification, archival disclosure, and final editorial metadata—not
an absent central analytic result.

The dimensional and strain campaigns now satisfy part of the roadmap as independent
bounded follow-up work. They must remain separately identified and must not be used to
upgrade Paper 1's numerical evidence status.
