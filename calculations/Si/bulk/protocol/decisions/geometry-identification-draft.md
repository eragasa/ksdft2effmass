# Geometry identification for the historical common-space diagnosis

## Status and scope

**Draft for review, not adopted. Admission remains stopped.** Authorization to
prepare this proposal is not adoption of its scientific convention. This document
does not amend the [controlling hopping-first protocol](../../research-protocol/controlled-reduction-protocol-hopping-first.tex),
complete a gate, select a successor, authorize execution, or create a reviewed-state
assertion. The earlier [source-association review](../../analysis/wannier-window-remedy/source-association-review.md)
remains **REVIEW_INCONCLUSIVE**; this draft does not supersede it.

The proposal is limited to identifying the common native parent-band space for the
unchanged historical SSSP C6-B20-W21 pointwise overlap diagnosis. It does not qualify
that source for production or alter the required PseudoDojo parent. No new numerical
result, error bound, convergence result, or symmetry conclusion is supplied here.

## Problem and recorded evidence

The [source-association dossier](../../analysis/wannier-window-remedy/source-associations.md)
supports shared native band/gauge lineage for AMN and U_dis/U, but distinguishes
nominal geometry metadata from the geometry actually passed to QE. The current CSD0
rule requires explicit, exact geometry identification. Replacing that requirement
with “the cells are close enough” would be an unapproved tolerance waiver.

For clarity, write direct lattice vectors as matrix **columns**:

`D(c) = c * [[1,1,0],[0,1,1],[1,0,1]]`.

Files listing one vector per line contain the corresponding transpose. The recorded
entries are:

| Declaration | Nonzero direct-cell entry | Meaning |
|---|---|---|
| S30 lattice | `2.7345910468201033 angstrom` | Nominal retained analysis geometry |
| Localization WIN | `2.734591046820 angstrom` | Twelve-decimal construction metadata |
| Generated NNKP | `2.7345910 angstrom` | Seven-decimal direct-lattice interface presentation |
| Executed NSCF input | `2.73459105 angstrom` | Eight-decimal cell actually supplied to QE |
| NSCF XML | `5.167628147352816 bohr` | Native output representation, not an angstrom token |

The NNKP direct-lattice precision is **not** its eight-decimal fractional-k-point
precision. These declarations must not be collapsed into one supposedly identical
matrix. The dossier's previously calculated `3.1798967903284847e-9 angstrom`
residual concerns S30 versus the QE output converted with the stated QE constant;
it is not a bound on all representations or on any observable.

The nominal S1 structure also contains floating representations of the quarter-site
position, whereas QE/WIN render exact decimal quarters. Both cell and site-coordinate
renderings therefore belong to the identification question; scalar lattice length
alone is insufficient.

## Recommended prospective rule

The following is **proposed normative wording only**, requiring separate review and
explicit adoption before use:

> For this retained source, the physical parent geometry of the native band states
> shall be identified by the authenticated executed QE input and its bound native
> saved-state/output records. Nominal S1/S30, WIN, and NNKP geometry declarations shall
> remain separately identified metadata, with their actual values, units, axis/site
> order, and source identities preserved. They shall not be asserted to be exactly
> equal physical geometries.
>
> CSD0 may establish a common native finite-band space for the unchanged pointwise
> overlap reconstruction only through authenticated shared parent-state/gauge lineage,
> explicit ordered point/band associations, projection semantics, and a reviewed
> record of the distinct geometry and coordinate renderings. This is an identification
> of the native source used by both coefficient matrices, not an equivalence between
> Hamiltonians at different physical cells or Cartesian wavevectors.
>
> Identity-level checking shall remain exact for the declared source identities and
> the stated association. A geometric proximity test, native-code compatibility
> tolerance, matching spectrum, or opaque geometry name shall not substitute for that
> association. Missing, contradictory, or unsupported mappings shall stop admission.

This proposal identifies which already-executed source a matrix refers to; it does
**not** change that crystal structure. It also does not silently correct S30's nominal
geometry metadata or reinterpret all of S30's geometry-dependent results.

## Association that would have to be reviewed

A prospective declaration would have to contain or explicitly bind all of the
following, rather than merely supply a new `geometry_identity` string:

1. **Source geometry:** the executed QE cell and atomic-position tokens, units,
   primitive-vector convention, handedness, ordered sites, XML representation and
   declared conversion constants, with their byte identities. XML unit conversion
   and output precision must be accounted for explicitly; changing a constant to
   manufacture equality is forbidden.
2. **Nominal and interface geometry:** the unchanged S1/S30, WIN, and NNKP declarations
   and their source identities. For this non-tie example, the observed cell entries
   match the respective eight-, twelve-, and seven-decimal round-to-nearest
   presentations of the nominal entry. That relation is a checkable statement about
   these tokens, not proof of a general formatter rule or a new rounding policy.
   Site-coordinate renderings require their own explicit association. The exact
   generation path and relevant assumptions must be reviewed, not inferred from
   decimal appearance alone.
3. **Band and gauge origin:** the bound NSCF saved-state manifest, converter lineage,
   and localization input/output identities. The AMN and U_dis/U coefficient matrices
   must refer to the same native parent-band frame at each ordered index. Spectral
   agreement or a dimension count alone is insufficient. The ultrasoft S-metric
   interpretation and scalar spin block remain as documented in the dossier.
4. **Points and presentations:** a declared one-to-one integer-index correspondence
   between native NSCF, converter, and Wannier records. Keep the NSCF/WIN input
   fractional coordinates, eight-decimal NNKP points, ten-decimal U/U_dis points, and
   native XML Cartesian coordinates explicit. A logical `(i,j,k)` grid label is not
   a replacement for any of those numeric records. No point permutation, snapping,
   or nearest-neighbor inference is permitted.
5. **Claim boundary:** which matrices inherit the actual native parent geometry, and
   which historical quantities were evaluated using nominal geometry metadata.
   Numerical-source assumptions and missing evidence must be stated. A declaration
   or its hash cannot prove its own scientific truth or review authorship.

These obligations are proposed review content, not a new schema, framework, or API.
The existing v1 admission code cannot establish their truth by accepting an opaque
label. No software or source-assertion payload is changed by this draft.

## Mathematical meaning and limits

Let `j` denote an authenticated native point index and `Psi_j` the modeled
S-orthonormal, twenty-band QE parent frame at that source point. Its coefficients
are interpreted using the existing conventions:

- `A_j = Psi_j† S_j G_j` for the native trial columns;
- `C_j = A_j T†` in the unchanged ordered atomic trial-coordinate convention;
- `W_j = U_dis,j U_j` in that same parent-band frame;
- `B_j = W_j† C_j` for the pointwise trial-to-retained overlap.

The proposed identification concerns this common coefficient space. It does not
certify actual solver orthonormality or introduce another S factor into `B_j`.
No matrix is recomputed, rescaled, whitened for acceptance, or otherwise repaired by
choosing a geometry label.

For a direct cell `D`, fractional coordinates `q` imply
`k_D(q) = 2*pi*D^(-transpose)*q`. Changing `D` changes that physical Cartesian
wavevector even if a logical or fractional label is shared. The proposed index
association therefore does **not** assert `k_native = k_nominal`. It does not
resample a Hamiltonian, identify operators at different geometries, provide a
unitary dilation between physical models, or justify operator subtraction.

The same distinction applies to real-space distances, optimized centers, hopping
geometry, localization measures, reciprocal sewing, velocities, and curvature/mass
interpretations. No existing dimensional result is relabeled as evaluated at the
executed QE cell. Such use requires its own explicit geometry interpretation and
appropriate error treatment before the relevant downstream claim can be made.
Full CSD0 unconditionally requires authentication of the exact S30 full untruncated
ten-dimensional operator, the S105 full-support disposition, and the S110 blocked
result, including their physical and represented state-space associations and the
other identity requirements in the controlling protocol. The proposed native
coefficient-space identification addresses only its stated sub-obligation; it does
not establish that full association. An unresolved S30 nominal/native physical-space
association stops full CSD0 and therefore CSD1 eligibility. Replacing full CSD0 with
a pointwise coefficient-space gate would require an explicitly proposed substantive
amendment, not this clarification; no such replacement is proposed here.

## Unchanged numerical and scientific constraints

- The original data, S30/S105/S110 records, bound request and protocol snapshots,
  source hashes, basis order, trial transformation, state dimensions, band packing,
  source windows, energy reference, and spin convention remain unchanged.
- The raw binary64 threshold `5.890206739032098e-7` and its strict comparison are
  unchanged. Native printing/parsing and arithmetic error requirements are unchanged;
  they do not absorb a geometry discrepancy.
- No geometric acceptance tolerance is introduced. In particular, the numerical
  specification's `1e-4 angstrom` lattice-refinement rule is not a CSD0 identity rule
  and must not be borrowed to admit this source. QE's `eps6` interface compatibility
  check is not an exact-geometry certificate either.
- Keep parent-model, numerical/discretization and rendering, and model-reduction
  errors distinct. This draft supplies no observable sensitivity bound and no claim
  that the geometry difference is physically negligible.
- Higher arithmetic precision cannot turn these distinct input declarations into
  equal geometries. No routine higher-precision campaign is proposed.
- Complete producer reconstruction, the missing symmetry-related point inventory,
  independent CSD1-V, CSD2, human CSD3, and HF0–HF4 remain outstanding prerequisites.
  No symmetry representation, new construction, fit, or candidate window is selected.

## Review and adoption boundary

Review should determine whether the proposed native finite-band identification
meets the intended CSD0 meaning without concealing nominal/executed geometry
inequality, whether the complete association above is substantiated, and whether
later geometry-dependent claims are adequately kept separate. Source-to-build and
rounding assumptions remain explicit; they are not upgraded to attestations.

Only after that review and explicit scientific-owner adoption could a prospective
change be incorporated into the controlling protocol and applied to a new admission
attempt. Any affected request/version or replay-routing changes must first be
identified and reviewed: old hash-bound requests must not silently resolve to new
protocol bytes, and historical evidence/review records must remain unchanged.
No such migration or implementation is selected or performed here.

The alternative remains to retain the current rule and the admission stop. Preparing
this recommended proposal does not decide between those policies, reopen execution,
or supersede the prior review. **Until adoption and actual prerequisite completion,
the current stop remains in force and no canonical reviewed-state assertion is due.**
