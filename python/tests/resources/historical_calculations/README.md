# Historical calculation fixtures

These files are exact byte copies of selected historical periodic-1D and
periodic-2D campaign documents and source adapters. They are test-owned resources
for maintained campaign serializers, workflows, correlators, and independent
verifiers.

They do **not** restore the removed
`calculations/research-monograph/periodic-1d/` or
`calculations/research-monograph/periodic-2d/` trees as active calculation
owners. They must not be used as authorization to execute a calculation, as a
new provenance location, or as evidence that the superseded calculation layout
is maintained.

`manifest.json` records each historical path, recovery revision, byte count,
and SHA-256 digest. All fixtures come from revision
`c5d34a93b4710a4a430738c404c775865d418d42`, the parent of removal commit
`6c17150bce8bf339e9c818453a0ef0572d34e17a`. The periodic-2D resources retain a
repository-shaped subtree because the independent verifiers authenticate historical
source-path identities embedded in the result documents.

Tests should read these resources directly rather than depending on an absent
historical calculation tree. Scientific interpretation remains bounded by the
original records and is not strengthened by their use as software or numerical
verification fixtures.
