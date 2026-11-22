# Full S30 operator and state-space identification statement

## Status and question

**Proposed scientific identification for independent review; not a canonical source
assertion, protocol amendment, adoption decision, or completed CSD0 record. Admission
remains stopped.** This statement identifies the complete encoded S30 model and its
source-point relationship to the native parent, rather than substituting AMN/U
lineage for the full-source obligation.

The [controlling protocol](../../research-protocol/controlled-reduction-protocol-hopping-first.tex)
still requires the S30/S105/S110 physical and represented-space associations and all
other CSD0 identities. The [reviewed geometry proposal](../../protocol/decisions/geometry-identification-draft.md)
is unadopted and does not discharge those requirements. This statement introduces no
replacement gate. Its question is whether the full model, maps, and limits below
provide the required S30 association on the declared construction-point domain, or
which additional identification remains unsupported. It does not ask a reviewer to
accept nominal and executed geometries as equal.

Scope is the unchanged historical SSSP scalar-relativistic, non-SOC C6-B20-W21 source,
not production qualification of the required PseudoDojo parent. No calculations,
source operators, or numerical error bounds are newly produced by this statement.

## 1. Evidence and complete construction

The [S30 implementation](../c6-b20-w21-untruncated-characterization/run_analysis.py)
has SHA-256 `985dcc7e000fdd0aea76e046f8cfbf8cf12b73990decdc2808be517fd50a538e`;
the [retained result](../c6-b20-w21-untruncated-characterization/characterization-result.json)
has SHA-256 `37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18`.
S105 binds S100, whose input records bind both this S30 implementation and result.
The read-only audit checked that chain and the six S30 source-payload identities.
These are provenance correlations, not running-process or source-to-build attestations.

S30 consumes the unchanged nominal S1 structure and EIG, HR, U, U_dis, and WSvec
payloads identified in its `sources` section. `FiniteWannierOperator.from_native`
(lines 349–382) expands every HR matrix entry using its element-specific WS shifts.
For native representative `r`, HR degeneracy `d_r`, entry `(m,n)`, and its stored
shift list `T_rmn` of length `n_rmn`, the effective coefficient construction is

`h_tilde[p]_(m,n) += H_HR[r]_(m,n) / (d_r * n_rmn)`

for every `t` in that list, with `p=r+t`. Coincident contributions are summed. No
physical-radius mask is applied to this construction. The retained inventory reports
279 native representatives and 383 effective integer representatives; “full” means
all of this encoded finite support, **not** the full KS Hilbert space or all twenty
parent bands. S105 defines `H_T=H_W` with all 383 representatives retained; it does
not supply an additional state-space embedding.

The exact mathematical family described by the evaluation recipe is

`H_S30(q) = Her[sum_p h_tilde[p] * exp(+2*pi*i*q·p)]`,

where `Her(M)=(M+M†)/2`, `q` is dimensionless reciprocal-fractional, matrix entries
are eV, and `p` is an integer translation label. The explicit Hermitian part is in
`FiniteWannierOperator.matrices` (lines 421–424); it must not be omitted when stating
the implemented recipe. The retained result separately reports pair closure and
real-space Hermiticity. Those earlier numerical observations were not recomputed
for this statement.

This identifies the **whole finite Laurent-matrix model** on the reciprocal torus,
not only its values at 216 points. Its fibre domain and codomain are the same ordered
`C^10` native Wannier-coordinate space. A conventional convolution realization on
`ell^2(Z^3) tensor C^10` follows from these finite coefficients (using the coefficients
of the stated Hermitian part). That mathematical realization is not a claim that
S30 constructed or authenticated an infinite physical Wannier basis in the KS space.
The source class itself evaluates the matrix family, not such a physical embedding.

The order is native Wannier indices 1–10 and the phase is the integer-translation,
cell-gauge Fourier convention above. No additional orbital-center phase is inserted
by S30. This is **not** an already identified atomic `sp3s-star` basis. S110's attempted
atomic-trial alignment remains blocked; no fit or successful atomic-basis map is
inferred from the existence of this ten-dimensional model.

## 2. Native parent and construction-point maps

Let `j=0,...,215` identify the authenticated source order, and let `H_j^20` denote
the parent operator restricted to the native twenty-band physical source space at
that NSCF point. Its diagonal coordinates in the parent frame below are `E_j`;
the operator and this matrix are distinct. Twenty bands are not the complete KS space. Their common parent/gauge origin is the NSCF saved
state → converter AMN/MMN/EIG → localization input/output chain documented in the
[source-association dossier](source-associations.md), not an inference from spectra
or equal dimensions. No bands are excluded in this occurrence, and its original
outer-window packing starts at band 1 everywhere, as separately documented there.

For the **idealized backend interpretation**, write `Phi_j` for the parent-band
frame in the QE ultrasoft overlap metric `S_j`, and `V_j=D_j U_j` for the native
rank-ten retained frame. With `sharp` denoting the adjoint in that physical metric,
the modeled frame conditions and identification are

- `Phi_j sharp Phi_j = I_20`, `V_j† V_j = I_10`;
- `J_j = Phi_j V_j : C^10 -> S_j^ret = range(Phi_j V_j)`;
- `J_j sharp J_j = I_10`.

These equations state the declared orthonormal-frame model and the direction of its
representation map. They are **not** numerical certificates of the historical
solver, pre-print arrays, or printed matrices. Neither `Phi_j` nor `J_j` was computed
by the present audit. Parent numerical errors remain distinct from printing/parsing
error; the model-to-computed-frame relationship is not certified by the latter.
No polar correction, pseudoinverse, deleted direction, or pointwise completion is
introduced to manufacture an exact isometry from parsed data.

In that frame model, the parent compression has coordinates

`K_j = V_j† E_j V_j = J_j sharp H_j^20 J_j`.

This is a compression on the disentangled retained space, not an assertion that it
is an invariant spectral subspace, a full-parent restriction, or an exact downfolded
Hamiltonian obtained by eliminating the complementary sector. The finite band
coefficient metric is Euclidean in this interpretation; the ultrasoft S factor is
not inserted a second time into `V_j† E_j V_j` or the AMN-based overlap.

The historical S30 code instead works with **parsed numerical representatives**:
`W_file,j = U_dis,file,j U_file,j` and
`K_file,j = W_file,j† diag(E_file,j) W_file,j` (lines 448–494).
`W_file,j` must not be declared exactly isometric merely because its modeled source
frame is isometric. Native component-rounding and parsing hypotheses connect these
file representatives to computed source quantities; they do not certify the entire
idealized physical model.

## 3. Identification of the full model at source points

Let `q_j^U` be the coordinate presentation stored with U/U_dis. S30 compares
`H_S30(q_j^U)` with `K_file,j` at the same ordered index (lines 663–737). It reports
a format-aware reconstruction comparison, **not exact equality of these matrices**.
Its bound construction propagates HR/U/U_dis/EIG printing errors (lines 739–781);
that does not by itself prove physical point association, geometry equality, or an
error bound for every coordinate/convention mismatch.

The proposed physical/represented-space association is explicit: at native source
point `j`, the coordinate basis of the complete model's fibre is identified with
`J_j`, in the modeled interpretation above. The associated model action on that
retained native space would be

`H_assoc,j = J_j H_S30(q_j^U) J_j sharp`, with domain/codomain `S_j^ret`.

This formula states a **candidate interpretation of the existing model coefficients**,
not a newly calculated Hamiltonian, a replacement source, or an operation already
performed by S30. It uses an isometric *modeled* `J_j`; substituting the rounded
`W_file,j` as an exact isometry would be invalid. It does not identify
`H_assoc,j` with the exact parent compression. The retained reconstruction comparison
and its stated numerical assumptions remain the relevant limited evidence for that
approximation, separately from parent-model and model-reduction errors.

Thus the complete model object and every source-point coordinate-space map are
specified, not only an AMN/U relationship. However, a finite list of source-point
maps is **not** an isomorphism from the whole convolution-model Hilbert space to the
native sampled KS space. Sampling is not an injective identification of arbitrary
model functions. No such global identification is claimed.

## 4. Logical order, geometry, and dimensional interpretation

The identification is indexed by the actual source lineage. `q_j^U` is not silently
replaced by the NSCF/WIN twelve-decimal input, NNKP eight-decimal presentation, or an
ideal unrounded `(i/6,j/6,k/6)` value. Keep all presentations and native XML Cartesian
coordinates explicit. An integer index correspondence does not assert identical
physical Cartesian wavevectors. No permutation, snapping, resampling, or geometry
change is performed.

The executed QE cell has nonzero entries `2.73459105 angstrom`; S30's nominal
structure has `2.7345910468201033 angstrom`, WIN uses twelve decimals, and NNKP's
cell uses seven decimals. Their exact source identities and distinct meanings are
recorded in the dossier and geometry draft. Using the same logical `q` with different
direct matrices changes `k(q)=2*pi*D^(-transpose)*q`. The maps above attach source-point
fibres to the **native parent**; they do not prove nominal/native cell equality or
identify physical Hamiltonians at two different geometries.

Given **fixed HR/WSvec payloads**, S30's coefficient construction, matrix evaluation,
and source reconstruction comparison do not consult `SiliconLattice`. That is a
source-level dependency fact, not a geometry-independence theorem for the production
of those payloads. Wannier90's `ws_translate_dist` uses `real_lattice` and Wannier
centres to choose translations (`src/ws_distance.F90:66–144`); its Hamiltonian
construction uses the Wannier gauge and `kpt_latt` for Fourier phases
(`src/hamiltonian.F90:209–303`). Geometry and gauge choices have already entered the
frozen artifacts. No claim that recomputing them at another cell would preserve the
coefficients is justified.

S30 loads the **nominal** S1 lattice separately (`SiliconLattice.from_structure`,
lines 216–254). Its reciprocal basis enters Cartesian valley classification and
coordinates (lines 908–949) and Cartesian mass-stencil conversion (lines 1016–1053).
Its direct basis enters physical-radius shells (lines 1065–1073). Those results remain
nominal-geometry diagnostics. No mass, radius, center, sewing result, or physical
wavevector is relabeled as evaluated at the executed QE cell. No observable sensitivity
bound or negligible-geometry-error conclusion follows from the small cell difference.

## 5. Claim boundary and remaining evidence

Supported construction evidence is the full fixed HR/WSvec model, its S105 unchanged
support, and its source-point relationship to the native band/gauge frame. This is
stronger than matching dimensions or eigenvalues, but it remains conditional on the
explicit source, frame, coordinate and numerical-model assumptions above.

For off-mesh `q`, `H_S30(q)` is a defined model matrix. Retained U/U_dis do not provide
a KS embedding `J(q)` at arbitrary off-mesh points. No global native-frame extension,
physical sewing, locality adequacy, off-mesh parent fidelity, or geometry-dependent
operator equivalence is established here. These are not inferred from polynomial
smoothness or a successful structural round trip. Conversely, the absence of such
validation must not be silently converted into a newly invented CSD0 requirement:
review must distinguish the protocol's source identification from later scientific
adequacy and frame/fidelity tasks.

Full CSD0's S30/S105/S110 physical and represented-space obligations remain
unconditional. The review must decide whether this full-object identification and
construction-point map supply the intended source identification on CSD0's declared
216-point domain, or identify the exact additional association required. If a stronger
physical/global claim is required, this statement does not establish it, and the stop
must remain. No weaker pointwise replacement gate is proposed, and no review outcome
by itself adopts a new interpretation of the protocol.

## 6. Provenance, replay limitation, and unchanged controls

S30's bulk-relative EIG path is absent in the current checkout. The read-only audit
explicitly checked the external EIG named by the bound converter result against both
that result and S30's expected byte count/hash. The original path was not declared
resolved. This is identified relocated evidence, not a fallback admission rule or a
claim that the historical script is currently replayable as written. Any future run
must explicitly resolve its required source paths under the applicable contract.
The historical S30 script was not imported or rerun.

The raw overlap threshold, source windows/projections, spin block, native eV energy
reference, matrix data, old requests/protocol snapshots, and source-code bindings are
unchanged. The geometry proposal remains unadopted; the prior reviews remain unchanged.
Printing/parsing bounds do not absorb geometry or parent numerical error. No source
assertion, completion receipt, full CSD0/CSD1 execution, CSD1-V verification, symmetry
attribution, CSD3 decision, fit, calculator occurrence, or publication is claimed.

The [architecture's space/operator distinction](../../../../../docs/architecture/v2/ksdft2effmass/periodic/retained-spaces-and-operators.md)
and monograph compression conventions govern the terminology here. Wannier90 reference
source inspected during the audit includes `src/hamiltonian.F90` (SHA-256
`68a3a988e16b8f82f2cd0b90064cfbcaec52b528a8ce3608362b1a85b3081d19`) and
`src/ws_distance.F90` (`0a51e9be68b7bc2f91986cd9164a6a7ff478df5894e139d0097cafead307a4ad`)
under `/Users/eugene/projects/wannier90-3.1.0/`. These reference copies and the earlier
QE source explain conventions; they are not attestations that those exact sources
produced the historical executable builds. Source association review is not independent
numerical verification or material validation.
