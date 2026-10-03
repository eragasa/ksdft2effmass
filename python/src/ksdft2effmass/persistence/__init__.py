"""Public opaque revision-persistence contracts.

The package exports immutable generic revision values and a nominal atomic
store ABC with a local SQLite implementation. Domain repositories remain
separate concerns; storage observations do not establish domain validity.
"""

from .sqlite import SQLiteAtomicRevisionStore
from .store import (
    AbstractAtomicRevisionStore,
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
    "AbstractAtomicRevisionStore",
    "Commit",
    "CommitResult",
    "CommitStatus",
    "Revision",
    "RevisionReadRequest",
    "RevisionReadResult",
    "RevisionReadStatus",
    "RevisionSelector",
    "StoreOperationalFailure",
    "SQLiteAtomicRevisionStore",
)
