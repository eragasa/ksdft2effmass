# H4-HC01 human response

B — retain legacy authority and perform one bounded H4 correction.

Correct the H4-owned mypy failure in:

python/tests/software_verification/ksdft2effmass/harness/pi/local/test__local_public_api_and_models.py:116

Add an explicit type for the heterogeneous mutable test-case collection without changing the tested behavior, accepted public contract, assertions, or evidence meaning.

Then:

1. run focused H4 source-and-test mypy and require PASS;
2. run the focused H4 tests and require PASS;
3. run focused H4 Ruff and require PASS;
4. because the test is a replay input, create one replacement replay-input revision R2;
5. replay R2 once in an isolated clean worktree;
6. create evidence revision E2 referencing R2 without requiring E2 = R2;
7. update only t[118;1:3uhe affected H4 evidence and checkpoint records;
8. request only a targeted integration-review confirmation of this correction—do not rerun all three full reviews;
9. rerun the H4 completion validator;
10. return directly to H4-HC01 and stop.

The repository-wide 43 Ruff findings and pre-existing global mypy debt may remain explicitly retained baseline limitations. Verify and record that H4 introduced no new Ruff findings relative to its starting revision.

Do not expand this correction into baseline cleanup, another general review cycle, replay redesign, H5, P2, scientific/external execution, publication, or release work.
