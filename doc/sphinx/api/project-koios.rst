Project Koios integration
=========================

``ksdft2effmass.integration.projectkoios`` is an optional, one-way
anti-corruption boundary from a complete replay-valid research-monograph citation
Result to the neutral target DTOs owned by ``projectkoios.references.citations``.
Install the ``project-koios-citation`` extra to use this boundary.

The adapter preserves literal case-sensitive keys, owner ordering, target-owned
identities, excerpt-free locators, content identities, source gaps, and closure
tuples.  The deliberate field renames are ``bibliography_entry_id`` to ``entry_id``
and ``bibliography_path`` to ``bibliography_source_path``.  It leaves
``source_bibliography_observation_id`` unset.  It does not parse BibTeX, rescan TeX,
write files, acquire sources, decide bibliographic identity, record availability or
rights, or assign processing and projection status.

.. currentmodule:: ksdft2effmass.integration.projectkoios

.. autoclass:: ResearchMonographCitationTargetSnapshotAdapter
   :members:
