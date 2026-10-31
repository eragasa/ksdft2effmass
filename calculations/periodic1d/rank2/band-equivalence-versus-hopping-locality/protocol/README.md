# Prospective experimental protocol

This directory owns the complete buildable prospective protocol for the periodic-1D
rank-two band-equivalence-versus-hopping-locality calculation.

The following files initially moved byte-exactly from the experiment tree at baseline
revision `c49aaf816702c321cdd649e2567af70da57246fe`. The hashes record those baseline
migration identities; the maintained TeX source and review PDF may subsequently add
calculation-owned lifecycle contracts without rewriting the historical identity.

| File | Baseline SHA-256 |
|---|---|
| [`experimental-protocol.tex`](experimental-protocol.tex) | `3b1cff165ebd3ec803469d4df8cd40422f4bf80b73472ec220ca67ed1c982725` |
| [`experimental-protocol.pdf`](experimental-protocol.pdf) | `c367f0ea701ee39fffb5ab80ab0c1a0dcd4cd5850dff00b5b77f0ce630b5d74d` |
| [`experimental-protocol.bib`](experimental-protocol.bib) | `360e4a9e83f700650d1bb9319fcead9a2e39e737cf161c2a3d32ef43a3986202` |

The PDF is the selected current review snapshot corresponding to the maintained protocol
source. The bundle remains pre-version design material: it is not an immutable protocol,
retained calculation, scientific validation, publication, or execution authorization.

The maintained TeX source retains its historical relative dependencies and adds optional
authenticated direct-lifecycle figure slots. Its authoritative calculation-side
dependencies are:

| Staged build path | Calculation-owned source |
|---|---|
| `smooth-threshold-continuum.csv` | [`../simulations/development/inputs/smooth-threshold-continuum.csv`](../simulations/development/inputs/smooth-threshold-continuum.csv) |
| `analysis/band-equivalence-versus-hopping-locality.pdf` | [`../analysis/development/figures/band-equivalence-versus-hopping-locality.pdf`](../analysis/development/figures/band-equivalence-versus-hopping-locality.pdf) |
| `analysis/nonflat-four-state-exploratory.pdf` | [`../analysis/development/figures/nonflat-four-state-exploratory.pdf`](../analysis/development/figures/nonflat-four-state-exploratory.pdf) |
| `analysis/band-equivalence-locality-scientific-story.pdf` | [`../analysis/development/figures/band-equivalence-locality-scientific-story.pdf`](../analysis/development/figures/band-equivalence-locality-scientific-story.pdf) |
| `analysis/truncation-band-consequences.pdf` | [`../analysis/development/figures/truncation-band-consequences.pdf`](../analysis/development/figures/truncation-band-consequences.pdf) |
| `figures/embedded-rank2-momentum-refinement.png` | Authorized direct execution, when present |
| `figures/embedded-rank2-adaptive-amplitude-refinement.png` | Authorized direct execution, when present |
| `figures/embedded-rank2-truncation-consequences.png` | Authorized direct execution, when present |

Build in scratch so the selected tracked PDF is not overwritten:

```console
build_dir="$(mktemp -d /tmp/ksd-band-protocol.XXXXXX)"
mkdir -p "${build_dir}/analysis" "${build_dir}/figures"
cp experimental-protocol.tex experimental-protocol.bib "${build_dir}/"
cp ../simulations/development/inputs/smooth-threshold-continuum.csv "${build_dir}/"
cp ../analysis/development/figures/{band-equivalence-versus-hopping-locality,nonflat-four-state-exploratory,band-equivalence-locality-scientific-story,truncation-band-consequences}.pdf "${build_dir}/analysis/"
figure_root="../executions/direct-embedded-rank2-controlled-v2/figures"
for figure in embedded-rank2-{momentum-refinement,adaptive-amplitude-refinement,truncation-consequences}.png; do
  if test -f "${figure_root}/${figure}"; then
    cp "${figure_root}/${figure}" "${build_dir}/figures/"
  fi
done
(
  cd "${build_dir}"
  latexmk -pdf -interaction=nonstopmode -halt-on-error experimental-protocol.tex
)
```

The baseline recipe produced a 31-page PDF whose Ghostscript 72-dpi page renderings were
byte-exact against the baseline tracked snapshot. The maintained source now stages the three authenticated aggregate plots from the
passing unsealed `v2` execution. It displays explicit placeholders when those
artifacts are absent and never substitutes development figures for authenticated slots. Raw PDF bytes are not treated
as scientific identities.

[`../protocol.md`](../protocol.md) records the concise calculation boundary and migration
targets. Authority and conflict rules are explicit in
[`../protocol-authority-and-historical-donors.md`](../protocol-authority-and-historical-donors.md).
[`../technical-report/`](../technical-report/) is a separate calculation-facing migration
report; it does not replace this protocol.
