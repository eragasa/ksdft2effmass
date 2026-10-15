# Experiments

This tree is the maintained destination for publication-independent numerical
experiments. An experiment selects models, cases, sample roles, thresholds, metrics,
protocols, executable composition, interpretation boundaries, schemas, independent
verification, and retained evidence while consuming reusable capabilities from
installed owner libraries. New maintained experiment execution must not be added under
publication-specific `calculations/` paths; those paths remain historical evidence and
design donors. Architecture mirrors
this source hierarchy under `docs/architecture/v2/experiments/`; every selected package,
subpackage, module, and public class uses `index.md`, `science.md`, `numerics.md`,
`implementation.md`, and `schematics.md`, with detail concentrated toward the
implementing `ClassName`.

Within `periodic-reduction/`, reusable scientific experiment families are grouped first
and dimensional realizations (`periodic1d/`, later `periodic2d/` or `periodic3d/`) are
children. A family container is organizational; each dimensional child retains its own
stable experiment-family identity. Empty dimensional placeholders are not created.

Experiment code is not part of the public `ksdft2effmass` wheel. Installed packages
must never import this tree. Reusable behavior is extracted into its domain owner and
consumed from the experiment; experiment-specific behavior is not promoted merely
because it is parameterized.

Every retained experiment must distinguish:

- stable experiment-family identity;
- immutable experiment-version identity;
- run identity;
- evidence-package identity and digests; and
- publication-side references.

Publication, conference, appendix, milestone, and historical stage labels are aliases,
not maintained experiment identities. Superseded material remains locatable through
exact Git versions and commits rather than duplicate `legacy/` or `historical/`
directories.

Maintained experiment work currently includes:

- `periodic-reduction/single-band-fourier-reduction/periodic1d/` — immutable `v1`
  supplied-band reduction composed with reusable KSD analysis, with strict schemas,
  independent reconstruction, exact predecessor provenance, and retained evidence;
- `periodic-reduction/composite-band-alignment-and-locality/periodic1d/` — prospective
  publication-independent successor for rank-two frame alignment and gauge-dependent
  locality; owner replacements are tracked as technical debt and no immutable version
  or maintained run exists;
- `model-adequacy/periodic1d/constrained-admissible-sets/` — owner-integrated
  constrained-quadratic geometry with composed rank-two parent derivation; evaluation,
  schemas, and evidence freezing remain incomplete;

Creating source or passing tests under this tree does not authorize protected
calculator execution and does not establish scientific validation, convergence,
uncertainty quantification, or publication evidence.
