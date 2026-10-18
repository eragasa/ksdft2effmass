# Novelty and convention audit

## Purpose

This audit records the related-work basis for the paper's contribution statement and the
Fourier-convention crosswalk between versions 2 and 3.

## Question audited

The narrow contribution under review is the combination of:

1. pointwise band equivalence under a momentum-dependent internal unitary;
2. comparison under a restricted momentum-independent real alignment;
3. exact common-curvature rank-two loss geometry and the smooth
   $J_0(2a)$ threshold laws;
4. the flat-parent identity between irreducible matrix residual and transferred
   non-onsite Fourier power;
5. extension through a controlled dispersive four-state parent homotopy; and
6. separate cyclic-conversion, interpolation, deliberate-truncation, total-error, and
   equal-sampled-accuracy first-passing range channels.

The audit does **not** ask whether gauge-dependent Wannier localization, the MLWF
spread decomposition, hopping truncation, Procrustes alignment, transported-frame
covariance of a Frobenius loss, Parseval identities, or spectral perturbation bounds are
individually new. They are not presented as such. In particular, the manuscript does
not identify its contract-dependent minimum operator loss with the MLWF quantity
$\Omega_{\mathrm I}$, and it does not identify the scalar excess above that minimum with
$\widetilde\Omega$.

## Search procedure

The search used combinations of the following terms in general web and Google Scholar
searches:

- `Wannier gauge hopping range truncation error`;
- `gauge hopping finite range band structure`;
- `fixed accuracy hopping range gauge Wannier tight binding`;
- `Procrustes Wannier gauge Hamiltonian alignment hopping`;
- `Bessel Wannier gauge hopping locality rotation`;
- `omitted hopping band error Wannier truncation`; and
- the exact phrase pair `band equivalence` / `hopping locality`.

The search was supplemented by the v3 bibliography and its cited review literature.
Metadata were checked through DOI/publisher, arXiv, or Google Scholar records. Gupta and
Bradlyn (2022) received a targeted reading of the abstract, introduction, Wannier
construction, and tight-binding range discussion.

## Closest literature and disposition

| Source | What it establishes for this paper | What it does not establish for this paper |
|---|---|---|
| Marzari and Vanderbilt (1997); Souza, Marzari, and Vanderbilt (2001); Marzari et al. (2012); Marrazzo et al. (2024) | Bloch/Wannier gauge freedom, the projector-/frame-dependent MLWF spread decomposition, localization, disentanglement, sparse real-space representations, and interpolation context. | A cross-model Hamiltonian-alignment theorem or the paper's restricted global-alignment geometry, $J_0(2a)$ laws, residual--power identity, or equal-accuracy range-inflation ledger. |
| Yates et al. (2007) | Wannier interpolation and the practical role of localized real-space matrix elements. | A comparison between gauge-related complete Hamiltonians under separately reconstructed truncation channels. |
| Danieli et al. (2021) | Local unitary constructions in all-bands-flat lattices can preserve flat spectra while changing lattice couplings. | The present Procrustes-restricted mismatch geometry or dense first-passing cutoff comparison. |
| Sathe and Roy (2024) | Compact and maximally localized Wannier functions need not coincide; exact compact support is a distinct localization question. | The present sampled accuracy-versus-range experiment or dispersive parent homotopy. |
| Gupta and Bradlyn (2022) | A Wannier-based 1-D photonic model can be improved systematically by retaining longer-range hoppings, in a setting that explicitly uses Wannier gauge freedom. | A controlled comparison of two gauge-related complete Hamiltonians at the same declared sampled accuracy. |
| Ghosh, Schankler, and Rappe (2025) | Hopping truncation can affect bands and wavefunction-dependent optoelectronic responses differently; band agreement is not sufficient for all observables. | The present exact rank-two formulas or representation-to-representation first-passing range inflation. |
| Schönemann (1966); Higham (1986) | Orthogonal/unitary Procrustes and polar-factor mathematics used by the alignment and transport algorithms. | Any materials or Wannier-specific novelty claim. |

The searches found papers on gauge-dependent localization, compact support, flat-band
locality, systematic hopping-range improvement, and truncation effects. They did not
locate a source combining the six items in the question above. The manuscript therefore
uses the following contribution statement:

> The contribution is a controlled analytic-to-dispersive benchmark and
> channel-resolved error-accounting protocol, not a priority claim for gauge-dependent
> locality itself.

The manuscript also states that the complete Hamiltonians are pointwise unitarily
equivalent and that the reported sampled range inflation quantifies representation
efficiency after truncation rather than physical inequivalence. The manuscript makes no
priority claim.

## Version 2 to version 3 convention crosswalk

Version 2 writes the dimensionless one-dimensional momentum as $k$ in expressions such
as

$$
T_R=\frac{1}{N}\sum_k e^{-2\pi i kR}H(k),
\qquad
H(k)=\sum_R e^{+2\pi i kR}T_R.
$$

Version 3 reserves $k$ for the physical wavenumber and defines
$q=k/G=ka_0/(2\pi)$. It uses the same Fourier signs:

$$
T_R=\frac{1}{N}\sum_q e^{-2\pi i qR}H(q),
\qquad
H_N(q)=\sum_R e^{+2\pi i qR}T_R.
$$

Thus the v2-to-v3 manuscript change is a coordinate rename and unit clarification, not a
momentum reversal. No $q\mapsto-q$ transformation is required to compare the stated v2
and v3 Fourier equations.

An external implementation using the opposite Bloch convention can be cross-walked by

$$
q\mapsto-q,
\qquad
T_R\mapsto T_{-R}.
$$

On a symmetric reciprocal mesh this reversal preserves spectra, Frobenius block powers,
omitted-power sums, Hermiticity norms, maximum/RMS errors, and first-passing symmetric
range decisions. It does **not** preserve signed or oriented quantities verbatim:
individual labelled blocks are exchanged, the smooth angle satisfies
$\theta_a(-q)=-\theta_a(q)$, and an oriented closure holonomy is reversed so its phases
may change sign and order. Those quantities must be compared only after applying the
explicit convention map.

## Required editorial boundary

- Keep the explicit v3 convention $q=k/G$ and the negative-exponent forward transform.
- Do not compare labelled $T_{+R}$ and $T_{-R}$ across conventions without reindexing.
- Keep closure phases as sewing diagnostics, not topological claims.
- Keep the literature statement bounded to related gauge, localization, and truncation
  phenomena plus the specific contribution language above.
- Re-run this audit if the manuscript adds a priority claim, a material claim, a
  higher-dimensional result, or a continuous-domain range law.
