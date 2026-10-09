# `Periodic1DReductionChallengeCampaignDefinition`

## Role

Frozen, slotted DataObject for one complete version-one reduction-challenge control
document. Its short `__post_init__` delegates cohesive identity, quantity, finite-
representation, potential-shape, sampling, and route checks. Exact nominal types are
enforced; booleans and numeric strings do not cross numeric boundaries.

## Important invariants

- nonempty exact experiment identity and a nonempty increasing unitless
  potential-strength axis;
- positive increasing plane-wave cutoffs and finite-difference grid sizes whose matrix
  dimensions contain every compared band;
- at least two compared bands and increasing nonnegative challenged-band indices, each
  with the upper neighbor needed by the isolation diagnostic;
- a larger reference cutoff whose finite matrix contains every represented
  potential-shape harmonic;
- unique named unitless finite-Fourier shapes with one common period;
- strictly increasing even reciprocal meshes of at least two points;
- positive unitless isolation threshold and exact route controls; and
- agreement between the declared primary and route hopping ranges and mesh inventory.

The object is a campaign definition, not a physical parent Hamiltonian, finite matrix,
retained space, represented operator, effective model, result, or provenance record.

## Evidence

`test__Periodic1DReductionChallengeCampaignJsonSerializer.py` reconstructs the complete
retained definition and historical wire-key boundary. Exact retained content identity
is separately owned by the row-060 artifact integration test.
