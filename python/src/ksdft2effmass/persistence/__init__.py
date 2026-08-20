"""Public opaque revision-persistence contracts.

The package exports immutable generic revision values and a structural atomic
store protocol.  Concrete SQLite storage and domain repositories are separate,
subsequent concerns.
"""

from .store import (
    AtomicRevisionStore,
    Commit,
    CommitResult,
    CommitStatus,
    Revision,
    RevisionReadRequest,
    RevisionReadResult,
    RevisionReadStatus,
    RevisionSelector,
    StoreOperationalFailure,
)

__all__ = (
    "AtomicRevisionStore",
    "Commit",
    "CommitResult",
    "CommitStatus",
    "Revision",
    "RevisionReadRequest",
    "RevisionReadResult",
    "RevisionReadStatus",
    "RevisionSelector",
    "StoreOperationalFailure",
)
