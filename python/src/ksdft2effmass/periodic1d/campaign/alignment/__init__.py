"""Canonical periodic-1D alignment campaign families.

Alignment campaigns infer or apply coordinate relationships between explicitly
identified finite representations. They do not infer physical-model identity,
state-space compatibility, gauge, or provenance from matrix dimensions or spectra.
"""

from .blind import BlindAlignmentCampaign, BlindAlignmentEncodedDocuments

__all__ = [
    "BlindAlignmentCampaign",
    "BlindAlignmentEncodedDocuments",
]
