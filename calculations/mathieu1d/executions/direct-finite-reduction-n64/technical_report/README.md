# Mathieu1D direct finite-reduction technical report

## Scientific question

For the represented Hamiltonian

\[
H=-\frac{d^2}{dx^2}+0.5\cos(x),
\]

how do the recorded finite parent representations, the complete 64-point discrete
Fourier transform, and the declared symmetric hopping-range truncations behave on the
fixed training and disjoint evaluation inventories?

`technical-report.tex` is the maintained calculation-facing report source. Its two
figure inputs are report-local, so it builds without files outside this directory:

```console
latexmk -pdf -interaction=nonstopmode -halt-on-error technical-report.tex
```

The direct rendering stage copies this source, its retained review PDF, and the two
authenticated figures beside the execution:

- `mathieu1d-finite-reduction.png` provides the complete four-panel finite-data view;
- `mathieu1d-publication-summary.png` provides the compact finite-range view consumed
  by publication sources.

Both figures contain only values already present in the verifier-authenticated typed
projection. Connected marks follow explicitly ordered finite inventories; they do not
assert interpolation or continuum limits. The compact publication figure is a second
layout of the same authenticated projection, not an independent calculation.

The maintained report files are exact copies of those recorded beneath
`../executions/direct-finite-reduction-n64/technical_report/`:

| artifact | SHA-256 |
|---|---|
| `mathieu1d-finite-reduction.png` | `de0ae08bd6e4c16afee074b14a73be2a7efbfa133044fc08ee75492238886b7e` |
| `mathieu1d-publication-summary.png` | `243722cfd538943dce572b32b1104e587371d88b59d13181c369ccfdac7d6c6c` |
| `technical-report.pdf` | `ee5fde28270bc183df18175f8abd3b916a74351993ee44af639c4076abfd7416` |

The maintained three-page PDF is a review snapshot. The direct execution remains
unsealed. These artifacts do not establish continuum convergence, uncertainty
quantification, material validity, publication acceptance, or a sealed evidence
package.
