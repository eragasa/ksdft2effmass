# `ksdft2effmass.publications.authoring`

**Status:** implemented first bounded vertical; proposal generation only.

This package owns a read-only target context, a minimal projection of external
retrieval and citation-identity status, a bounded local-inference request/response
port, deterministic prompt construction, and failed-closed proposal admission. Narrow
child modules own statuses, targets, evidence, requests, inference, proposals, owner
adapters, and the authoring action; the package facade only reexports their exact
public objects. Every
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
| Revision ID | `manuscript-target-revision:sha256:66b555a07eafff255e49e4d58cc26aa719c5b97d9d06db476e21d5693329a6b0` |
| Target ID | `manuscript-target:sha256:0abc7ab91a393c4c01d361eb05159baa923405d40477e2f17ed692e706116df2` |
| Span ID | `manuscript-target-span:sha256:eb4816286570ad63c18aa6ea0884d1490af4aa9af2e92e0be638f559f9c2f539` |

The full section is prompt context. Only the selected contiguous prose and
`\citationtodo{...}` passage is a proposal target. Equations, continuum-to-Wannier
embedding prose, and crossover-radius prose are excluded from replacement.

## Runtime status

The fixed-model loopback adapter is implemented and synthetically verified. A separate
explicit ad-hoc path admits only publisher metadata and abstracts from the three
authorized APS abstract pages, with `AUTHOR_SUPPLIED_AD_HOC` provenance and
`PUBLISHER_ABSTRACT` scope. Full text remains authorization-gated and is not accessed.
This path permits a bounded local draft with evidence markers for prospective citekeys;
it does not establish full-paper review, rights, scientific validity, publication
readiness, or human acceptance.

## Defining modules

- [`adapters`](adapters/index.md) — exact Project Koios owner-result adapters and the
  loopback-only fixed-model inference adapter.
- [`statuses`](statuses/index.md) — closed status vocabularies.
- [`target`](target/index.md) — exact read-only manuscript target.
- [`evidence`](evidence/index.md) — strict selected and retrieved evidence projections.
- [`ad_hoc_evidence`](ad_hoc_evidence/index.md) — author-supplied publisher abstracts.
- [`contracts`](contracts/index.md) — bounded authoring request.
- [`inference`](inference/index.md) — local-inference records and port.
- [`proposal`](proposal/index.md) — citations, proposal, and closed result.
- [`author`](author/index.md) — the sole semantic composition action.
- [`local_run`](local_run/index.md) — retained local-inference Workflow.

Each module index links its exact `ClassName/index.md` owners. No duplicate class page
or compatibility implementation is maintained at this package root.

## Contents

- [`schematic.md`](schematic.md) — package data and action flow.
- [`implementation.md`](implementation.md) — identities, prompt contract, failure
  closure, package decomposition, adapter contracts, and runtime stop condition.

```{toctree}
:hidden:

schematic
implementation
adapters/index
statuses/index
target/index
evidence/index
ad_hoc_evidence/index
contracts/index
inference/index
proposal/index
author/index
local_run/index
```
