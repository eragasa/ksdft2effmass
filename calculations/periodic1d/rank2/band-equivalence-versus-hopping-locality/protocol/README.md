# Prospective experimental protocol

This directory owns the complete buildable prospective protocol for the periodic-1D
rank-two band-equivalence-versus-hopping-locality calculation.

The following files moved byte-exactly from the experiment tree at baseline revision
`c49aaf816702c321cdd649e2567af70da57246fe`:

| File | SHA-256 |
|---|---|
| [`experimental-protocol.tex`](experimental-protocol.tex) | `3b1cff165ebd3ec803469d4df8cd40422f4bf80b73472ec220ca67ed1c982725` |
| [`experimental-protocol.pdf`](experimental-protocol.pdf) | `c367f0ea701ee39fffb5ab80ab0c1a0dcd4cd5850dff00b5b77f0ce630b5d74d` |
| [`experimental-protocol.bib`](experimental-protocol.bib) | `360e4a9e83f700650d1bb9319fcead9a2e39e737cf161c2a3d32ef43a3986202` |

The PDF is the retained review snapshot corresponding to this migrated protocol bundle.
The bundle remains pre-version design material: it is not an immutable protocol, retained
calculation, scientific validation, publication, or execution authorization.

The exact TeX source retains its original relative dependency names. Its authoritative
calculation-side dependencies are:

| Staged build path | Calculation-owned source |
|---|---|
| `smooth-threshold-continuum.csv` | [`../simulations/development/inputs/smooth-threshold-continuum.csv`](../simulations/development/inputs/smooth-threshold-continuum.csv) |
| `analysis/band-equivalence-versus-hopping-locality.pdf` | [`../analysis/development/figures/band-equivalence-versus-hopping-locality.pdf`](../analysis/development/figures/band-equivalence-versus-hopping-locality.pdf) |
| `analysis/nonflat-four-state-exploratory.pdf` | [`../analysis/development/figures/nonflat-four-state-exploratory.pdf`](../analysis/development/figures/nonflat-four-state-exploratory.pdf) |
| `analysis/band-equivalence-locality-scientific-story.pdf` | [`../analysis/development/figures/band-equivalence-locality-scientific-story.pdf`](../analysis/development/figures/band-equivalence-locality-scientific-story.pdf) |
| `analysis/truncation-band-consequences.pdf` | [`../analysis/development/figures/truncation-band-consequences.pdf`](../analysis/development/figures/truncation-band-consequences.pdf) |

Build in scratch so the selected tracked PDF is not overwritten:

```console
build_dir="$(mktemp -d /tmp/ksd-band-protocol.XXXXXX)"
mkdir -p "${build_dir}/analysis"
cp experimental-protocol.tex experimental-protocol.bib "${build_dir}/"
cp ../simulations/development/inputs/smooth-threshold-continuum.csv "${build_dir}/"
cp ../analysis/development/figures/{band-equivalence-versus-hopping-locality,nonflat-four-state-exploratory,band-equivalence-locality-scientific-story,truncation-band-consequences}.pdf "${build_dir}/analysis/"
(
  cd "${build_dir}"
  latexmk -pdf -interaction=nonstopmode -halt-on-error experimental-protocol.tex
)
```

This recipe produced a 31-page PDF whose Ghostscript 72-dpi page renderings were
byte-exact against the tracked snapshot. Raw PDF bytes were not identical and are not
substituted for the tracked artifact.

[`../protocol.md`](../protocol.md) records the concise calculation boundary and migration
targets. Authority and conflict rules are explicit in
[`../protocol-authority-and-historical-donors.md`](../protocol-authority-and-historical-donors.md).
[`../technical-report/`](../technical-report/) is a separate calculation-facing migration
report; it does not replace this protocol.
