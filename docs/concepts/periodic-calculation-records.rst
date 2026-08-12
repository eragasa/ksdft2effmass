Periodic calculation records from QEXSD
=======================================

The bounded extraction path for the accepted Quantum ESPRESSO tutorial artifact
is:

.. code-block:: text

   explicit QEXSD bytes and source identity
   -> ParseQexsdDocument
   -> immutable QexsdDocument
   -> ConstructPeriodicCalculationRecord
   -> immutable PeriodicCalculationRecord
   -> canonical retained JSON

The two transformations are intentionally distinct:

.. code-block:: text

   QEXSD parsing
   !=
   semantic periodic-record construction

``ParseQexsdDocument`` owns namespace, root, QEXSD-version, native-value,
source-order, declared-unit, and XML-structure handling. It receives
``QexsdSource`` bytes explicitly and performs no path discovery or file opening.
``ConstructPeriodicCalculationRecord`` contains no XML behavior. It maps the
native document to the minimal backend-neutral observation while preserving
native units and provenance and recording unavailable interpretation with typed
reasons.

The version-1 record stores ordered lattice and reciprocal-lattice vectors,
species and atoms, sampled k points and unnormalized weights, Kohn--Sham
eigenvalues and occupations, total energy, FFT grids, exit status, and exact
external source identity. The arrays are immutable nested tuples in Python and
ordered arrays on the wire. Kohn--Sham eigenvalues are not treated as a complete
many-body spectrum or a uniquely identified basis-independent operator.

Absolute energy reference, Fermi alignment, retained subspace, gauge, phase,
basis identity, and spin convention are unavailable for this source. The parser
does not infer them. A valid record does not establish convergence sufficiency,
numerical verification, scientific validation, uncertainty quantification, or
human acceptance.

Current retained evidence and later workflow
--------------------------------------------

* :download:`calculations/bulk-silicon/qe-example01-si-scf-davidson/artifact-inventory.json <../../calculations/bulk-silicon/qe-example01-si-scf-davidson/artifact-inventory.json>`
* :download:`calculations/bulk-silicon/qe-example01-si-scf-davidson/periodic-calculation-record.json <../../calculations/bulk-silicon/qe-example01-si-scf-davidson/periodic-calculation-record.json>`
* :download:`docs/computational/wannier/wannier-tutorial-catalog.md <../computational/wannier/wannier-tutorial-catalog.md>`

The Wannier catalog describes proposed later work only. This extraction does not
run or implement Wannier90.
