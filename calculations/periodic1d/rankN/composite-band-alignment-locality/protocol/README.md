# Planned higher-rank one-dimensional study

This directory contains the detailed plan for a synthetic one-dimensional calculation
that has not been run as retained evidence. The calculation asks how increasing the
number of retained states and the depth of momentum-dependent basis rotations changes
the range of the resulting real-space hopping matrices.

The protocol's short labels mean:

- **D1:** one spatial dimension;
- **P0:** the retained subspace is fixed rather than moving with momentum; and
- **G0:** the basis rotations are real orthogonal rotations.

“Protocol candidate” means that the proposed cases, meshes, tolerances, outputs, and
checking method have been written down. The stable result files and independent checker
have not been implemented, and no retained calculation has been run.

| File | SHA-256 |
|---|---|
| [`experimental-protocol.tex`](experimental-protocol.tex) | `160b61b2c2dc87e7628524c710c779f8e3b2c547f0a2d228615300aa06bdce0b` |

The TeX file is an exact-byte migration of
`experiments/periodic-reduction/higher-rank-composite-band-alignment-and-locality/experimental-protocol.tex`
at predecessor revision `81f7c09a5edc50be698bd3a5f047438cd61d4eca`.

The plan specifies the one-dimensional cases, file contents, independent checking
method, resource limits, and rules for deciding whether a future result may be kept. Its
references to `verify_d1_p0_g0_controls.py` name the old finite-grid formula-check script;
the maintained replacement is
[`../verify_analytic_controls.py`](../verify_analytic_controls.py). The current
development runner does not yet produce the planned stable result files or perform the
planned independent check.

Build only in scratch so tracked review inputs are not overwritten:

```console
build_dir="$(mktemp -d /tmp/ksd-higher-rank-protocol.XXXXXX)"
cp experimental-protocol.tex "${build_dir}/"
(
  cd "${build_dir}"
  latexmk -pdf -interaction=nonstopmode -halt-on-error experimental-protocol.tex
)
```

A successful build establishes document buildability only. It does not create an
immutable version, authorize execution, or establish numerical or scientific validation.
