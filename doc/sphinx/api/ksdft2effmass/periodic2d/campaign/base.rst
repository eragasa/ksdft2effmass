Periodic2d campaign base
========================

Purpose and public contract
---------------------------

``Periodic2DCampaign`` is the lightweight common DataObject base for canonical
periodic two-dimensional campaigns. It provides only a nominal campaign type and the
exact spatial dimension ``2``. Concrete campaigns continue to own their models,
requests, results, serializers, correlation, verification, tolerances, and execution
behavior.

Represented meaning
-------------------

The class represents software organization for campaigns whose modeled domain is
two-dimensional and periodic. It does not represent a physical Hamiltonian, a
mathematical operator, a finite matrix, a basis, a lattice geometry, or a retained
calculation result. Those identities remain explicit on concrete owners.

Symbols, units, and domains
---------------------------

.. list-table:: Base contract
   :header-rows: 1

   * - Name
     - Meaning
     - Domain and unit
   * - ``spatial_dimension``
     - Number of spatial directions in the periodic model family
     - Exact built-in integer ``2``; unitless

Assumptions, invariants, and exclusions
---------------------------------------

Every canonical periodic2d campaign inherits this base. Inheritance alone does not
make two campaign models compatible and does not unify their band rank, state space,
energy reference, basis, gauge, units, geometry, numerical method, retained format, or
acceptance policy. The base intentionally declares no abstract correlation,
verification, serialization, or Workflow method because those signatures currently
differ among concrete campaigns.

Data flow and failure policy
----------------------------

Constructing the base stores no campaign-specific state. Reading
``spatial_dimension`` returns ``2`` without conversion, tolerance, allocation, file
access, or external execution. The base introduces no numerical failure mode and no
scientific pass/fail criterion.

Compatibility and serialization
--------------------------------

The base is a source-level nominal type in the alpha API. It has no wire format and
adds no serialized field to concrete campaigns. The removed
``ksdft2effmass.campaigns.periodic2d`` namespace has no compatibility façade; callers
use ``ksdft2effmass.periodic2d`` or
``ksdft2effmass.periodic2d.campaign``.

Implementation and evidence mapping
-----------------------------------

* Source:
  ``python/src/ksdft2effmass/periodic2d/campaign/base.py``
* Software verification:
  ``python/tests/software_verification/ksdft2effmass/periodic2d/campaign/test__Periodic2DCampaign.py``
* Concrete one-band campaign:
  ``python/src/ksdft2effmass/periodic2d/campaign/nbands_1/``

The software evidence checks the exact spatial dimension and inheritance of every
currently canonical periodic2d campaign. It does not execute calculations or inspect
retained scientific values.

Reference and provenance
------------------------

This lightweight ownership boundary is a repository-derived alpha software contract.
It does not rely on an external scientific method reference.

Evidence status and limitations
-------------------------------

The mapped tests provide software verification only. No numerical verification,
scientific validation, uncertainty quantification, or human acceptance follows from
inheritance. A cross-dimensional periodic campaign base remains proposed work until
periodic1d and periodic2d contracts have been reconciled without erasing meaningful
differences.

Public API
----------

.. currentmodule:: ksdft2effmass.periodic2d.campaign

.. autoclass:: Periodic2DCampaign
   :members:
