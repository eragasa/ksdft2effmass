# Conference paper 7: SOC impurity operators for Si:P and Si:B

## Prospective role

Paper 7 is reserved for the first-principles material application to substitutional
phosphorus and boron in silicon under a common fully relativistic spinor program. It
consumes the bulk-reduction lessons of Paper 4, the common-space extraction contract of
Paper 5, and the Paper 6 obstruction diagnostics only when their escalation conditions
apply.

The proposed application contains three separately qualified branches:

1. pristine silicon with SOC in every matched supercell used for subtraction;
2. neutral substitutional Si:P with SOC; and
3. neutral substitutional Si:B with SOC.

Each doped branch is compared with a pristine-Si SOC calculation using the same
supercell lattice, numerical representation, relativistic convention, spinor ordering,
energy-reference method, and compatible Wannier construction. The scalar non-SOC Paper
4 operator is a baseline and methodological predecessor, not the direct subtraction
reference.

## Required compatibility controls

A shared matrix dimension is not sufficient. Before subtraction, each branch must bind
and qualify:

- fully relativistic pseudopotential family, exact files, and hashes;
- supercell geometry, reciprocal folding, cutoffs, meshes, and execution identity;
- noncollinear spinor convention and magnetic-state interpretation;
- retained rank, projections, windows, centers, ordering, and boundary sewing;
- common-space bundle compatibility or an explicit projection/embedding;
- double-space-group information for the pristine reference and the surviving defect
  subgroup used by the alignment;
- scalar energy-reference alignment and uncertainty;
- localized defect states and any resulting change in retained-space content; and
- independent reconstruction of the aligned impurity operator.

The ten-spatial-orbital non-SOC $sp^3s^\ast$ representation of Paper 4 would correspond
to twenty spinor components before any separately justified rank change. Spin-up and
spin-down are not treated as independently conserved labels under SOC.

P:Si and B:Si remain distinct physical branches. Their electron counts, magnetic states,
SOC response, target observables, pseudopotentials, projection choices, and surviving
symmetries must not be averaged into a shared result merely because both use spinors.

## Specification and evidence boundary

The current physical-specification v1 selects a scalar-relativistic non-SOC primary P:Si
branch and a fully relativistic SOC branch for final B:Si claims. The proposed Paper 7
SOC P:Si branch therefore requires a reviewed specification amendment or successor.
This README does not make that amendment and does not select exact pseudopotentials,
structures, occupations, windows, meshes, tolerances, or acceptance requirements.

No production calculation, retained impurity operator, donor or acceptor result,
continuum reduction, model-selection conclusion, submission, publication, release, or
promotion is asserted or authorized.
