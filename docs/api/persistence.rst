Opaque revision persistence
===========================

``ksdft2effmass.persistence`` supplies immutable generic revision values and a
structural atomic-store protocol with a local SQLite implementation. Payload
bytes are opaque: Harness, Workflow,
calculator, and scientific interpretation remain with their domain owners.

The contract represents compare-and-swap inputs, idempotency correlation, exact
latest-or-explicit reads, reconciliation expectations, and closed outcomes.  It
does not establish domain validity, numerical verification, scientific validation,
or uncertainty quantification. The concrete local transaction and operational
limits are described in :doc:`../concepts/sqlite-revision-store`.

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

Local SQLite implementation
---------------------------

.. autoclass:: SQLiteAtomicRevisionStore
   :members:
