Opaque revision persistence
===========================

``ksdft2effmass.persistence`` supplies immutable generic revision values and a
structural atomic-store protocol.  Payload bytes are opaque: Harness, Workflow,
calculator, and scientific interpretation remain with their domain owners.

The contract represents compare-and-swap inputs, idempotency correlation, exact
latest-or-explicit reads, reconciliation expectations, and closed outcomes.  It
does not provide a concrete database implementation or establish durable storage,
domain validity, numerical verification, scientific validation, or uncertainty
quantification.

Use the supported package-level imports shown below.

.. currentmodule:: ksdft2effmass.persistence

Selectors and statuses
----------------------

.. autoclass:: RevisionSelector
   :members:

.. autoclass:: RevisionReadStatus
   :members:

.. autoclass:: CommitStatus
   :members:

Immutable inputs
----------------

.. autoclass:: Revision
   :members:

.. autoclass:: RevisionReadRequest
   :members:

.. autoclass:: Commit
   :members:

Closed outcomes
---------------

.. autoclass:: StoreOperationalFailure
   :members:

.. autoclass:: RevisionReadResult
   :members:

.. autoclass:: CommitResult
   :members:

Structural store protocol
-------------------------

.. autoclass:: AtomicRevisionStore
   :members:
