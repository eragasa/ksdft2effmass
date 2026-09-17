"""Minimal outward result-codec composition public surface.

Only explicit seven-family codec routing is implemented here. No application root,
configuration resolver, store defaults, execution service or scientific claim exists.
"""

from .result_values import ApplicationResultValueSerializer

__all__ = ["ApplicationResultValueSerializer"]
