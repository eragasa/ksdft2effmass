"""Public QEXSD extraction and periodic-calculation record API.

QEXSD parsing is distinct from semantic periodic-record construction.  The
public boundary performs no filesystem discovery, Quantum ESPRESSO execution,
Wannier execution, unit conversion, energy alignment, or scientific acceptance.
"""

from .construction import ConstructPeriodicCalculationRecord
from .qexsd import ParseQexsdDocument
from .records import (
    PeriodicCalculationRecord,
    QexsdDocument,
    QexsdSource,
    UnavailableReason,
)
from .serialization import PeriodicCalculationRecordJsonSerializer

__all__ = [
    "ConstructPeriodicCalculationRecord",
    "ParseQexsdDocument",
    "PeriodicCalculationRecord",
    "PeriodicCalculationRecordJsonSerializer",
    "QexsdDocument",
    "QexsdSource",
    "UnavailableReason",
]
