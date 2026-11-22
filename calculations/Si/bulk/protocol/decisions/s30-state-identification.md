# Adopted S30 source identification

## Decision and authority

**The scientific owner (current human operator) adopted the bounded interpretation below** by replying
“recommendation authorized” to the recommendation to identify the complete S30 model
with native retained spaces at the 216 construction indices, preserve nominal-geometry
diagnostics separately, and make no off-mesh embedding or production claim.

This adopts the scientific interpretation in the reviewed
[full S30 statement](../../analysis/wannier-window-remedy/s30-state-space-identification.md),
SHA-256 `06da1f2590c2700380efce4b90b2d25e2e4abcc828bc7701bda99f800c7c3610`.
Its [independent source-identification review](../../analysis/wannier-window-remedy/s30-state-identification-review.md),
SHA-256 `f13b8d96e8295f48c031662800bcb5a8d88e45bf62733f8e69212d7de4e48d5b`,
found `NO_BLOCKING_FINDINGS` and conditionally supported this particular association
within the existing CSD0 scope. The earlier
[dossier](../../analysis/wannier-window-remedy/source-associations.md) and
[source-association review](../../analysis/wannier-window-remedy/source-association-review.md)
retain their exact bytes and respective limitations.

**This is a source-specific identification under the existing protocol, not a new
protocol rule, a tolerance waiver, or adoption of the entire earlier geometry draft.**
The [controlling protocol](../../research-protocol/controlled-reduction-protocol-hopping-first.tex)
remains unchanged at SHA-256
`2cfc03bbd4edce4387c7dad3e0cf75129b35b61a45594a33c036d6217e605ec4`.
The full CSD0 requirements, CSD1/CSD1-V sequence, CSD2/CSD3 and HF0–HF4 remain intact.
No source-state declaration, hash check, or review flag grants execution authority.

## Adopted physical and represented-space meaning

- The full source is the **complete fixed S30 HR/WSvec matrix family**, with every
  one of its 383 effective integer representatives retained. Its native Wannier
  ordering, positive integer-translation Fourier phase, explicit Hermitian-part
  evaluation, eV units and unchanged energy zero are those in the reviewed statement.
  S105 retains `H_T=H_W`; this is not the complete KS operator or an already aligned
  atomic `sp3s-star` model.
- At each authenticated native construction index `j`, its coordinate fibre is
  identified with the native retained space through the statement's modeled
  `J_j=Phi_j V_j`. Physical twenty-band operators, coordinate matrices, modeled
  isometries and rounded file matrices remain distinct. No exact isometry is
  manufactured from printed U/U_dis, and no printing bound certifies the solver or
  the whole physical model.
- The statement's `J_j H_S30(q_j^U) J_j sharp` gives the adopted **source-point
  interpretation** of the existing model, not a new matrix calculation or an exact
  equality with the parent compression. The native physical frame is that of the
  actual NSCF occurrence, not a second calculation at the nominal cell.
- The complete finite interpolant is specified on its model reciprocal torus, but
  its physical association here is on **216 source indices only**. No isomorphism
  between the infinite model space and sampled KS states, off-mesh KS embedding,
  global native frame, fidelity result or production qualification is adopted.
- All nominal-geometry valley, mass, distance/locality and related diagnostics keep
  their original meanings and values. They are not relabeled as native-geometry
  results. Upstream Wannier90 geometry/center dependence is already encoded in the
  frozen HR/WSvec/gauge artifacts; fixed-payload evaluation is not a theorem that
  recomputation at another geometry would preserve them.

## Exact geometry and point conventions of this source

Use direct vectors as matrix columns:
`D(c)=c*[[1,1,0],[0,1,1],[1,0,1]]`; vector-per-line inputs use its transpose.
The distinct declarations are:

| Component | Nonzero cell entry | Meaning |
|---|---|---|
| Executed QE input | `2.73459105 angstrom` | Native physical parent input |
| Native XML | `5.167628147352816 bohr` | Bound output representation; QE reference conversion is `0.529177210903 angstrom/bohr` |
| S30/S1 nominal lattice | `2.7345910468201033 angstrom` | Retained nominal analysis geometry |
| WIN | `2.734591046820 angstrom` | Construction metadata |
| NNKP lattice | `2.7345910 angstrom` | Seven-decimal interface presentation |

QE/WIN and native trial centers use fractional origin and the body-diagonal quarter
site. The nominal S1 record's second-site floats
`(0.2500000000000001,0.2500000000000001,0.24999999999999956)` remain distinct from
rendered decimal quarters. No source value is overwritten, and numerical proximity
is not declared physical equality.

Source order is `j=36*i+6*l+m`, with `i,l,m=0,...,5` and the last index fastest.
The declaration's coordinate array is the **ten-decimal U/U_dis presentation** of
`(i/6,l/6,m/6)`, converted by correctly rounded binary64 parsing. It is not a claim
that those floats equal NSCF/WIN twelve-decimal coordinates, NNKP eight-decimal
coordinates, an unrounded rational grid, or native Cartesian wavevectors. Their
integer-index correspondence comes from the reviewed occurrence lineage. AMN has
no coordinate records. No snapping, permutation, resampling, or inferred weights
are introduced.

The spin convention is one scalar orbital block of nonmagnetic, scalar-relativistic,
non-SOC historical Si USPP data. Native AMN has the reviewed `Psi† S G` meaning;
coefficient-space products use the standard metric of the modeled orthonormal band
frame, not a second S factor. Trial order and the radial-channel meaning are exactly
those in the unchanged development request and reviewed dossier.

## Explicit source-path bindings for declaration preparation

Paths below are explicit bindings, not basename search or an admission fallback.
Repository-relative paths resolve under
`/Users/eugene/worktrees/ksdft2effmass-silicon-main-package-0matampv`.
For compactness, these external prefixes are fixed:

- `C = /Users/eugene/projects/ksdft2effmass/si-accepted-s1-pw2wannier90-c6-b20-w21-aiida-precise-v1/run`
- `L = /Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier90-localization-c6-b20-w21-aiida-precise-v1/run`
- `N = /Users/eugene/projects/ksdft2effmass/si-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20-v1/run`

| Role | Explicit path | Expected bytes | Expected SHA-256 |
|---|---|---:|---|
| Development request | `calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/common-space-diagnosis-request.json` | 5458 | `0dd0d97cdc6134a30073b9d54a54077bba93b579882ef709de47534ca59ff89e` |
| S30 | `calculations/Si/bulk/analysis/c6-b20-w21-untruncated-characterization/characterization-result.json` | 56310 | `37f654ae31bc21e43b768bf2b9da5edabd88c195e3f6e1c87708eaa1c4773c18` |
| S105 | `calculations/Si/bulk/analysis/c6-b20-w21-spatial-truncation-disposition/spatial-truncation-disposition.json` | 6187 | `519adfcf1101f7caa7916e04f3bf37879f4ad82b0f30e4ef38adc39770224f68` |
| S110 | `calculations/Si/bulk/analysis/c6-b20-w21-slater-koster-definition-fit/slater-koster-definition-fit-result.json` | 119010 | `b9b8403dfc8b24df01e1671f582697440e1a211d60e0e70c9b0f621dfa086e98` |
| Protocol | `calculations/Si/bulk/research-protocol/controlled-reduction-protocol-hopping-first.tex` | 68518 | `2cfc03bbd4edce4387c7dad3e0cf75129b35b61a45594a33c036d6217e605ec4` |
| AMN | `C/silicon.amn` | 2894499 | `9186cd5b8802bede18f81b96188f0a2035eb97565c2f811f5ca7769f2ebefece` |
| U | `L/silicon_u.mat` | 679824 | `41758b721b79cae233689b4fb9fa359e750b82da8ed5bcd13b1d5faf3c5d8bf3` |
| U_dis | `L/silicon_u_dis.mat` | 1349424 | `3c1d3574f3bf783cf7b54d8e9fd00fa5811ef05a56240850d46f43a2c95b7ace` |
| EIG, explicit relocated evidence | `C/silicon.eig` | 168480 | `a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2` |
| HR | `L/silicon_hr.dat` | 1396475 | `24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55` |
| WSvec | `L/silicon_wsvec.dat` | 1365185 | `f40fa7f81afaa9bcf9614c6e3c53c14db0db6b0b429b84bfd10f2e40474de1a0` |
| NSCF input copy | `calculations/Si/bulk/simulations/evidence/sssp-1.3.0-pbe-efficiency-qe-7.5-accepted-s1-wannier-nscf-6x6x6-b20-david-c6-b20/input/pw.in` | 13911 | `20a6ee6e55d632bb66b1afcaac91592bf49c73a3e53e275659d1ccb03e47e1f9` |
| NSCF XML | `N/tmp/system.save/data-file-schema.xml` | 371723 | `2e1b5e157142d18210d18710fb9f5f3e813b17d8331acf96e11af9b9d4f7ef8c` |
| NSCF saved-state manifest | `N/nscf-saved-state-manifest.json` | 44898 | `24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac` |
| S1 nominal geometry | `calculations/Si/bulk/simulations/structures/Si.PrimitiveUnitCell.RightHanded.RelaxedS1.json` | 758 | `d131107753512c53dc0a32b9e07e0081f8277d8eeafcb9fad5f1fc7f153ded03` |
| Localization input manifest copy | `calculations/Si/bulk/simulations/evidence/wannier-localization/run-001/input/localization-input-manifest.json` | 1413 | `523515dffc883abf1bc0ff3e1427eea13e85a12774a5ce2040e3dd43c396568e` |

The EIG binding is explicitly to the converter-declared external occurrence. It does
not make the absent historical S30 relative path exist or claim that S30's original
script is replayable as written. A future action must consume explicit bound bytes
under its contract, not search for replacements.

The provider is the existing `projectkoios-simulations==0.1.0.dev0`, locked to commit
`841f5e34afd0a83c9a63da10c41a9d513c1caa80`. The complete seven-module closure is
`CommonSpaceProviderBinding.REQUIRED_MODULES` in its declared order. Six module digests
are the unchanged request's explicit `provider.modules`; the additional
`projectkoios.integrations.wannier90.artifacts` digest is
`f4f4736ef96093ecb5f06f7a5f27cd2a215e726b0b68146e4e9b83f99c6f4be8`,
from that locked commit. Matching installed source bytes must precede native parsing.
This is not a dependency change or a second native parser.

## Declaration identities and uncertainty model

The prepared [source-state declaration](../../analysis/wannier-window-remedy/source-state-assertions.json)
uses the existing `common-space-source-assertions-v1` wire contract:

- `parent_band_state_identity` is `qe-nscf-saved-state:24ee9d483141ab54d099bc6e6403d0da46108cc7a30c5b019992da3a1d7ef3ac:bands-1-20:216-native-indices`.
- `gauge_state_identity` is `converter:b8cc1b5df05fdda09fbbad13374635aed08aa630d11b16d554010f12ed8ed37a:localization-input:523515dffc883abf1bc0ff3e1427eea13e85a12774a5ce2040e3dd43c396568e`.
- `energy_reference_identity` is `native-S30-eV:EIG:a54f31f8f72cd32b63ad78e47378cd0a8ce97474ad223606f88d48c97c890dd2:HR:24a411c875b3e66bba37e28cc6bf2d95c38ef521c39f81fde40cd0bfa294ea55:no-shift`.
- `geometry_identity` is `s30-source-geometry:sha256:` followed by this decision
  file's SHA-256. It references the complete adopted distinction above; it is not
  an unexplained assertion of equal geometries.
- `review_reference` is this repository-relative decision path followed by
  `#sha256=` and its digest. This decision binds the original reviewed statement
  and verbatim independent report above; it does not claim human authorship of
  the AI technical review.

The native component bounds remain `1/(2*10^12)` for AMN and `1/(2*10^10)` for U and
U_dis, under declared nearest absolute decimal rounding, with correctly rounded IEEE
binary64 parsing. They bound printing/parsing relative to computed source quantities,
not all physical/solver error. Source-to-build correspondence remains an assumption.
The frozen threshold is the exact rational value of the original binary64
`5.890206739032098e-7`, not a new decimal/normalized threshold or a geometry bound.

## What remains stopped

The declaration records reviewed/adopted scientific source meaning; its generation
is not successful admission. This task does not prepare a complete ordered verifier
evidence bundle: actual producer reconstruction, symmetry-related point inventory
and truthful completion evidence are still required. No such evidence is fabricated
here.

No producer, full source-admission authentication, independent verifier, calculator,
fit, CSD2/CSD3 disposition, HF gate, successor activation, commit or push is performed
or authorized by this record. The existing partial producer's missing point-inventory
extension remains missing. Future execution and complete CSD0 evidence still require
their applicable checks and authorization; this source-specific adoption does not
turn a reviewed declaration into a completed gate.
