# `periodic1d.campaign.refinement`

## Purpose and status

This implemented canonical package owns campaign-specific refinement studies that vary
explicit approximation or finite-representation axes without conflating their error
channels. Row 063 moved the continuum-refinement family here without aliases or wire
changes.

Refinement campaigns do not define reusable parent models, retained spaces, represented
operators, or generic convergence policy. Those scientific and numerical owners remain
separate; this package owns campaign inputs, axis definitions, observations, verification
policy, and retained evidence for named studies.

## Child map

| Child | Responsibility | Canonical page |
|---|---|---|
| `continuum` | Separated continuum-mesh, continuum-domain, lattice-supercell, lattice-scale, and profile-family study | [Continuum refinement](continuum/index.md) |

## Dependency boundary

Campaigns may consume explicit parent models, finite representations, represented
operators, and authenticated retained sources. Scientific model and representation
packages must not import campaign repository paths, encoded documents, criteria,
retained conclusions, or acceptance policy.

Repository location belongs to explicit operation boundaries rather than encoded-byte
records. Mesh refinement, finite-domain growth, supercell growth, lattice-scale change,
and profile broadening remain distinct operations and error channels.

## Evidence and limitations

Rows 042, 057, and 063 cover the encoded-document/location split, result-document
ownership, and complete canonical campaign-family move. This evidence does not prove an
asymptotic continuum theorem, validate a material model, establish transferability,
quantify uncertainty, or record acceptance.

Original local work under the repository license.
