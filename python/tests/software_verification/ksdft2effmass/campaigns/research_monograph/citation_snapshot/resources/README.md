# Citation snapshot regression inputs

`baseline-revision.txt` pins the historical research-monograph input to the exact
existing Git commit `dac209a60aec502ae05fe84abd0c5eca23d3b4df`. The 49-file,
138-entry citation regression expectations belong to that revision, not the live
working manuscript. Do not refresh this pin merely because the manuscript changes.

The baseline fixture uses a temporary local shared clone and detached checkout.
It requires that commit and its objects in the source checkout's local history
(CI fetches full history). It does not fetch, create a research commit, stage owner
files, or substitute a fabricated revision. Missing history is a fixture error,
not permission to skip authentication. The production compiler still checks every
consumed source against its actual HEAD blob.

A separate temporary fixture copies the structurally audited working composition
and bibliography, then creates a **local test-fixture commit** of those copied
bytes. This is test input construction, not a commit to the research repository,
historical source/build provenance, publication acceptance, or a citation-quality
assessment. Its compiler test explicitly covers Chapter 9, Appendix N and the
expanded citation counts independently of the unchanged historical expectations.
The grammar suite continues to test rejection of dirty manuscript/bibliography
bytes and untracked included sources without mocking revision verification.

All materialized clones, copied sources and generated Git metadata are runtime
scratch under pytest temporary directories. The maintained fixture identity is
this directory's exact revision pin; no duplicate monograph archive is stored here.
