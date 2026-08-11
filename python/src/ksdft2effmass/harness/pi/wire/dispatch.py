"""Thin explicit routing for the closed harness wire-kind union."""

from __future__ import annotations

from typing import Any

from .checkpoints import _CheckpointRecordSerializer
from .human_review import _ReviewOwnershipWireSerializer
from .records import _CommonWireRecordSerializer
from .resources import _ResourceWireSerializer
from .tasks import _TaskWireSerializer


class _WireRecordDispatcher:
    """Route closed wire kinds to explicit private domain codecs."""

    __slots__ = (
        "_checkpoints",
        "_common",
        "_review_ownership",
        "_resources",
        "_tasks",
    )

    def __init__(self) -> None:
        common = _CommonWireRecordSerializer()
        review_ownership = _ReviewOwnershipWireSerializer()
        self._checkpoints = _CheckpointRecordSerializer()
        self._common = common
        self._review_ownership = review_ownership
        self._resources = _ResourceWireSerializer(common, review_ownership)
        self._tasks = _TaskWireSerializer()

    def encode(self, record: object) -> dict[str, object]:
        """Route a concrete record to its explicit domain field mapping."""
        from ..chains import ChainView, TaskReference
        from ..checkpoints import CheckpointRecord
        from ..ownership import (
            AgentDescriptorView,
            OwnershipManifestView,
            OwnershipScope,
        )
        from ..profiles import ProjectProfile
        from ..resources import ResourceManifest, ResourceReference, SkillDescriptor

        if type(record) is CheckpointRecord:
            return self._checkpoints.encode(record)
        if type(record) in (TaskReference, ChainView):
            return self._tasks.encode(record)
        if type(record) in (
            ResourceReference,
            ResourceManifest,
            ProjectProfile,
            SkillDescriptor,
        ):
            return self._resources.encode(record)
        if type(record) in (OwnershipScope, AgentDescriptorView, OwnershipManifestView):
            return self._review_ownership.encode(record)
        return self._common.encode(record)

    def decode(self, kind_name: str, obj: dict[str, Any]) -> object:
        """Route one caller-selected wire kind without inference or registration."""
        if kind_name == "CheckpointRecord":
            return self._checkpoints.decode(obj)
        if kind_name in ("TaskReference", "ChainView"):
            return self._tasks.decode(kind_name, obj)
        if kind_name in (
            "ResourceReference",
            "ResourceManifest",
            "ProjectProfile",
            "SkillDescriptor",
        ):
            return self._resources.decode(kind_name, obj)
        if kind_name in (
            "OwnershipScope",
            "AgentDescriptorView",
            "OwnershipManifestView",
        ):
            return self._review_ownership.decode(kind_name, obj)
        return self._common.decode(kind_name, obj)

    def supports(self, record: object) -> bool:
        """Return whether the record belongs to the closed wire union."""
        try:
            self.encode(record)
        except TypeError:
            return False
        return True
