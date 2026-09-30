# `ksdft2effmass.publications.authoring`

**Status:** implemented first bounded vertical; proposal generation only.

This package owns a read-only target context, a minimal projection of external
retrieval and citation-identity status, a bounded local-inference request/response
port, deterministic prompt construction, and failed-closed proposal admission. Narrow
child modules own statuses, targets, evidence, requests, inference, proposals, and the
authoring action; the package facade only reexports their exact public objects. Every
maintained record is frozen and slotted. Every request, response, result, proposal,
target revision, target section, target span, and projected excerpt has a deterministic
content-derived identity.

## Authorized target record

The selected manuscript source remains unchanged:

| Field | Exact value |
|---|---|
| Path | `docs/publications/research-monograph/chapters/12-continuum-effective-mass.tex` |
| Section | `\section{Continuum effective-mass reduction}` |
| Label | `ch:continuum-effective-mass` |
| Source Git blob SHA-1 | `d48bf07571eba1098b3ba78176ec020b8508d8d4` |
| Complete source SHA-256 | `335ca731832d6cbd9db0705b5477dc239c3090ac9d4b792ebb4eb3263f4ae355` |
| Full section SHA-256 | `2042f749957be2b4e6ef3603459bb54bb421c5525f77406b23c8c977a2c0010a` |
| Selected span | Starts `The continuum stage introduces…` and ends `two records are provisional.}` |
| Selected span bytes | 773 UTF-8 bytes, excluding the following newline |
| Selected span SHA-256 | `556a3f886b3fce8ac61cb697c21b539924e80d4154264624816add5398137790` |
| Revision ID | `manuscript-target-revision:sha256:abd045e18e9fb2c4f885d7345ca24ce912e6e6d761e37cfdf76bee67f0b640d1` |
| Target ID | `manuscript-target:sha256:66ae3e481fac9af6f6ebc6882d82cf18e52ddf75c4d31265dd81468d55ba992f` |
| Span ID | `manuscript-target-span:sha256:a604746b344b1a52b2801cfec6f5c84b0a564a4a46ab71b8e8475dbb59f9384e` |

The full section is prompt context. Only the selected contiguous prose and
`\citationtodo{...}` passage is a proposal target. Equations, continuum-to-Wannier
embedding prose, and crossover-radius prose are excluded from replacement.

## Defining modules

- [`statuses`](statuses/index.md) — closed status vocabularies.
- [`target`](target/index.md) — exact read-only manuscript target.
- [`evidence`](evidence/index.md) — selected and retrieved evidence projections.
- [`contracts`](contracts/index.md) — bounded authoring request.
- [`inference`](inference/index.md) — local-inference records and port.
- [`proposal`](proposal/index.md) — citations, proposal, and closed result.
- [`author`](author/index.md) — the sole semantic composition action.

Each module index links its exact `ClassName/index.md` owners. No duplicate class page
or compatibility implementation is maintained at this package root.

## Contents

- [`schematic.md`](schematic.md) — package data and action flow.
- [`implementation.md`](implementation.md) — identities, prompt contract, failure
  closure, package decomposition, and deferred adapters.

```{toctree}
:hidden:

schematic
implementation
statuses/index
target/index
evidence/index
contracts/index
inference/index
proposal/index
author/index
```
