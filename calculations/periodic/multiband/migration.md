# Shared periodic experiment-tree migration

This is not a central family checklist. It tracks only the four shared tracked files
identified by [`README.md`](README.md); every family migration is owned by its local
calculation surface.

- [x] Count baseline `40c84109bfd49718f1519f9bfd298f5ef90ddac0`: 197 tracked experiment files, 193 family-owned and four shared.
- [x] Assign every experiment-tree prefix to a calculation-side owner.
- [ ] Create a file-by-file manifest for all 197 tracked files at the baseline revision.
- [ ] Integrate applicable ownership/lifecycle content from `experiments/README.md` into `calculations/README.md` and Architecture v3.
- [ ] Integrate applicable script mechanics from `experiments/script-conventions.md` into the calculation contract.
- [ ] Move the band-equivalence parity contract to this calculation-program surface.
- [ ] Move the shared synthetic-strain protocol to this calculation-program surface.
- [ ] Update every family protocol and calculation README to the new shared-document paths.
- [ ] Prove every experiment file has exactly one destination or an explicit provenance-only disposition.
- [ ] Prove installed source, tests, docs, publications, and builds no longer depend on live `experiments/` paths.
- [ ] Preserve exact Git recovery for retained or historically consumed experiment bytes.
- [ ] Remove the experiment tree only after all family ledgers pass and separate deletion authorization is recorded.
