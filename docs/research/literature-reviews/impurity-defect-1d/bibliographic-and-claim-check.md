# Bibliographic and claim-classification check

## Method

The bibliographic check was performed independently of the claim extraction:
metadata were compared across at least two of the publisher/DOI landing page,
arXiv abstract history, and the paper front matter. The claim check then
compared each proposed manuscript sentence with the source passage and the
fields in `claim-to-source-matrix.md`.

“Independent” here means an independent metadata or textual route, not an
independent human reviewer. Final human acceptance remains separate.

## Bibliographic outcomes

| Bibliography key | Identity check | Publication-status check | Outcome |
|---|---|---|---|
| `kosterSlater1954impurity` | APS/DOI and bibliographic record agree on title, authors, volume 95, pages 1167–1176, and DOI | Peer-reviewed article | Pass; technical use restricted to abstract-level content |
| `simon1976weak` | DOI metadata and front matter agree | Peer-reviewed article | Pass |
| `parzygnat2010` | APS/DOI, arXiv, and front matter agree | Peer-reviewed article | Pass |
| `hoeferWeinstein2011` | SIAM/DOI, arXiv, and front matter agree | Peer-reviewed article | Pass |
| `ducheneVukicevicWeinstein2015` | Journal/DOI, arXiv, and front matter agree | Peer-reviewed article | Pass |
| `nakamuraTadano2021` | EMS/DOI, arXiv, and front matter agree | Peer-reviewed article | Pass |
| `koenigLeeHammer2011` | APS/DOI, arXiv, and front matter agree | Peer-reviewed article | Pass |
| `kohnLuttinger1955donor` | APS/DOI and browser-rendered front matter agree | Peer-reviewed article | Pass; invalid local pseudo-PDF excluded |
| `gamble2015` | APS/DOI, arXiv, and front matter agree | Peer-reviewed article | Pass |
| `berlijnVoljaKu2011` | APS/DOI, arXiv `1004.1156`, and front matter agree | Peer-reviewed article | Pass |
| `corsettiMostofi2011` | APS/DOI, arXiv `1010.3921`, and front matter agree | Peer-reviewed article | Pass |
| `lihmPark2019` | APS/DOI, arXiv `1901.04259`, and front matter agree | Peer-reviewed article | Pass |
| `luParkZhouBernardi2020` | Nature/DOI, arXiv `1910.14516`, and front matter agree; volume 6, article 17 | Peer-reviewed article | Pass |
| `kangMuechler2026` | arXiv abstract/history and PDF front matter agree on v1 submitted 2026-06-08 | Preprint; no journal publication identified | Pass with mandatory preprint label |
| `shiXieZhangChuGong2026` | arXiv abstract/history and HTML front matter agree on v2 submitted 2026-08-04 | Preprint; no journal publication identified | Pass with mandatory preprint label |

Some downloaded arXiv PDFs displayed later generated “Dated” values than their
journal publication year. Journal year, volume, article/page number, and DOI
were therefore taken from the publisher/DOI and arXiv journal-reference fields,
not from a generated compilation date.

## Claim-classification outcomes

- **Finite-rank impurity methods:** Koster--Slater is used only as historical
  abstract-level precedent. The exact rank-one secular equation in the
  benchmark is attributed to the benchmark's matrix-determinant construction,
  not quoted as a formula verified from inaccessible Koster--Slater full text.
- **Weak binding:** Simon and Parzygnat et al. support existence/threshold
  context only. They do not support the finite-supercell numerical result.
- **Band-edge homogenization:** Hoefer--Weinstein and
  Duchêne--Vukićević--Weinstein support weak/slow near-edge limits with their
  own scaling. They do not support identifying profile broadening or numerical
  mesh refinement with that limit.
- **Discrete-to-continuum:** Nakamura--Tadano supports the need for an explicit
  map between changing state spaces and a lattice-spacing parameter. Its theorem
  is not claimed for the benchmark's multiorbital finite operator.
- **Finite periodic volume:** König--Lee--Hammer supports image-induced
  bound-state shifts under its finite-range three-dimensional assumptions. Its
  asymptotic coefficient is not transferred to the one-dimensional lattice.
- **Semiconductor donors:** Kohn--Luttinger and Gamble et al. support the
  multivalley and central-cell boundaries. They do not validate a phosphorus
  impurity operator produced by this project.
- **Wannier defect Hamiltonians:** Berlijn--Volja--Ku, Lu et al., and
  Corsetti--Mostofi support localized-basis defect differences, scalar
  potential alignment, interpolation, and finite-size considerations within
  their stated objectives. They do not establish blind map inference.
- **Gauge matching:** Lihm--Park supports permutation/orbital, spin, phase,
  potential, and Hamiltonian matching for model stitching. Shi et al. provides
  recent preprint evidence of Hungarian assignment, unitary Procrustes
  alignment, and an explicit overlap metric in a clean/defect Wannier workflow.
  Neither source supplies a uniqueness theorem or the synthetic stopping
  thresholds.
- **Reduced screening class:** Kang--Muechler is labeled a 2026 preprint and
  supports only a distinct onsite-only screening objective and its stated
  limitations. It is not presented as prior validation of full operator
  extraction.

## Declined inferences

The check rejected the following inference patterns:

- “cited theorem” therefore “benchmark continuum crossover proven”;
- “same final matrix dimension” therefore “same state space”;
- “Wannierized” therefore “gauge aligned”;
- “localized defect matrix elements” therefore “all nonlocal residuals are
  negligible”;
- “supercell result converged in one observable” therefore “isolated defect
  established”;
- “binding energy agrees” therefore “operator agrees”;
- “no exact search hit” therefore “method is novel or first”; and
- “recent preprint reports material results” therefore “peer-reviewed
  validation or transferability established.”

## Check result

All substantive claims proposed for the literature-positioning passages have a
matrix row and an access classification. No direct quotation is used. Koster--
Slater remains abstract-level, and both 2026 records remain explicitly labeled
preprints. The remaining limitation is search boundedness: this check cannot
prove comprehensive coverage or priority.
