Periodic migration crosswalk
============================

The periodic migration crosswalk is a map from historical software objects to their
intended scientific and software meanings. It prevents a class name, array shape, or
location in the source tree from silently deciding what an object represents.

The crosswalk is migration documentation. It does not change a physical definition,
validate a material model, or authorize a calculation.

Objects kept separate
---------------------

A crosswalk row first identifies which kind of object is being migrated:

Scientific model
   The modeled periodic system and its physical or mathematical parameters. A model is
   not a matrix merely because one numerical method can represent it as a matrix.

Retained subspace
   A state space selected from an identified parent. It records what was retained and
   how it was selected. Gauge-dependent frame or projector coordinates are separate
   represented data.

Retained operator
   The exact restriction of an identified parent operator to an identified retained
   subspace. Exactness is relative to that parent; a finite numerical parent remains
   distinct from an untruncated mathematical model.

Represented operator
   Coordinates of an operator in a finite, ordered basis with explicit state space,
   geometry, units, energy reference, and provenance.

Effective model
   An approximation in a declared restricted model class, produced by an explicit
   truncation, fitting, or reduction route.

Encoded campaign document
   Preserved bytes and their content identity. Preservation does not turn a document
   into a scientific model or retained operator.

Campaign definition, request, or result
   Immutable controls and observations belonging to an executable study. Campaign
   policy does not become part of the scientific model it evaluates.

Supporting numerical owner
   A mesh, basis, coefficient container, transform, serializer, or diagnostic that does
   not acquire scientific identity solely from its use by a campaign.

How to read a row
-----------------

Each ``PERIODIC-XWALK-*`` row answers four questions:

#. What does the historical object actually contain?
#. Which target category and owner match that meaning?
#. Must the object be kept, moved, renamed, split, replaced, or removed?
#. Which values, conventions, bytes, identities, and provenance must remain unchanged?

A completed row also links its source implementation, supported imports, tests,
architecture pages, and Sphinx documentation. A pending row names the missing work. A
blocked row identifies information or authority that cannot be inferred safely.

Scientific conventions
----------------------

A scientist should not need to inspect constructors to discover the convention used by
an object. Applicable documentation states:

- parent state space and operator;
- finite basis and ordering;
- reciprocal domain and boundary sewing;
- basis and gauge convention;
- geometry, physical units, and energy reference;
- scalar dtype and array shape;
- selection, projection, transformation, interpolation, truncation, or fitting route;
  and
- exactness and approximation boundaries.

Equal dimensions, similar spectra, matching filenames, or content hashes do not prove
that two operators share a state space, basis, gauge, normalization, or scientific
meaning.

Documentation carried with implementation
-----------------------------------------

Every migrated public contract is documented together across:

- authoritative Markdown specifications, research assumptions, computational
  procedures, and architecture;
- NumPy-style Python docstrings;
- inline comments explaining non-obvious scientific conventions and algorithmic
  choices;
- public Sphinx API and concept pages;
- documented software and numerical tests; and
- retained calculation manifests or reports when the row consumes preserved evidence.

Comments explain why a convention or invariant exists; they do not merely repeat the
code. Public docstrings identify units, shapes, parentage, provenance, failures, and
limitations where applicable.

Tests are part of the maintained explanation. Module, ``Test...`` class, and test-method
docstrings state the evidence scope and the behavior established. Numerical evidence
also identifies the fixture class, represented space, units, oracle, comparator, norm,
tolerance, and validity domain. Synthetic fixtures, retained calculated data,
manufactured references, and literature values are labeled rather than presented as
interchangeable evidence.

Evidence and claim boundary
---------------------------

The migration keeps five evidence classes separate:

- software verification;
- numerical verification;
- scientific validation;
- uncertainty quantification; and
- human acceptance.

Passing unit tests can establish the implemented software contract. It cannot, by
itself, establish convergence, physical adequacy, a validated effective mass,
uncertainty bounds, or acceptance of a scientific conclusion.

The active architecture inventory and its scientist-facing documentation gate are
maintained under ``docs/architecture/v2/ksdft2effmass/periodic/``.
