"""Explicit Git-object acquisition for the current-fact supplement."""

from __future__ import annotations

import hashlib
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from python_public_import_current_fact_supplement_model import (
    AbsentTreeEntry,
    AcquisitionManifest,
    CommitTopology,
    DeltaLedgerEntry,
    DeltaStatus,
    DeltaTouch,
    ExtractionRole,
    InputVariant,
    ManifestInput,
    MaterialityCategory,
    PresentTreeEntry,
    SelectionCategory,
    SelectionEntry,
    SelectionSerializer,
    SupplementFormatError,
    SupplementJsonCodec,
)
from python_public_import_foundation_model import JsonRecord, JsonValue

BASE_COMMIT = "daa984a30916435dcdcd591e1c85e023b45dc852"
BASE_TREE = "f05ed040aaab743c76c0cb673769db794f9c4b22"
MERGE_COMMIT = "224a07a30180127e4efa3652bf0861757ff10316"
MERGE_TREE = "985b118cb7b68781e4e2c5e62242bc8952daad05"
MERGE_PARENTS = (
    BASE_COMMIT,
    "8fa5bdd812eca429bb1d6747fa71b291f81d2c01",
)
TARGET_COMMIT = "c3cf9b1081e797c4a4ec500e558193f0ec2bd77d"
TARGET_TREE = "e98abfeee96c2e7969a6b61d4b266c695aaa7d71"
TARGET_PARENT = "d0f921411dbb5d009daae9afebebbc4b510731e0"
NAME_STATUS_LF_SHA256 = (
    "11553fb9ea0fcb97f87e761a073132afd3e6973536ac3ac034be4b60ed632322"
)
NAME_STATUS_NUL_SHA256 = (
    "5a1b32d6836a0d4ab2171d7e567a90ee154c9f91a8763368ce29e7e3fb5c925d"
)
SHORTSTAT_TEXT = "565 files changed, 129391 insertions(+), 21234 deletions(-)"
SHORTSTAT_INSERTIONS = 129391
SHORTSTAT_DELETIONS = 21234


@dataclass(frozen=True, slots=True)
class GitTreeRecord:
    """Represent one regular-file entry from an exact Git tree."""

    mode: str
    oid: str


@dataclass(frozen=True, slots=True)
class ExplicitGitObjectReader:
    """Read only named commits, trees, and blobs from an explicit repository."""

    repository_root: Path

    def execute(
        self, arguments: tuple[str, ...], *, input_bytes: bytes | None = None
    ) -> bytes:
        """Run one bounded Git object command without branch or HEAD discovery."""
        completed = subprocess.run(
            ("git", "-C", str(self.repository_root), *arguments),
            input=input_bytes,
            check=False,
            capture_output=True,
            env={"LANG": "C", "LC_ALL": "C", "PATH": os.defpath},
        )
        if completed.returncode != 0:
            message = completed.stderr.decode("utf-8", errors="replace").strip()
            raise SupplementFormatError(f"explicit Git acquisition failed: {message}")
        return completed.stdout

    def text(self, arguments: tuple[str, ...]) -> str:
        """Return one LF-trimmed ASCII Git result."""
        try:
            return self.execute(arguments).decode("ascii").strip()
        except UnicodeDecodeError as exc:
            raise SupplementFormatError("Git identity output is not ASCII") from exc

    def tree(self, tree_oid: str) -> dict[str, GitTreeRecord]:
        """Return the complete named tree as normalized path records."""
        raw = self.execute(("ls-tree", "-r", "-z", tree_oid))
        records: dict[str, GitTreeRecord] = {}
        for item in raw.split(b"\0"):
            if not item:
                continue
            metadata, separator, raw_path = item.partition(b"\t")
            if not separator:
                raise SupplementFormatError("malformed ls-tree record")
            fields = metadata.decode("ascii").split(" ")
            if len(fields) != 3 or fields[1] != "blob":
                raise SupplementFormatError("only blob tree records are supported")
            try:
                path = raw_path.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise SupplementFormatError("Git tree path is not UTF-8") from exc
            if path in records:
                raise SupplementFormatError(f"duplicate Git tree path: {path}")
            records[path] = GitTreeRecord(mode=fields[0], oid=fields[2])
        return records

    def blob(self, oid: str) -> bytes:
        """Return exact bytes for one named blob object."""
        return self.execute(("cat-file", "blob", oid))

    def changed_paths(self, older: str, newer: str) -> tuple[tuple[str, str], ...]:
        """Return one exact no-rename NUL-delimited name-status stream."""
        raw = self.execute(
            ("diff", "--no-renames", "--name-status", "-z", older, newer)
        )
        fields = raw.split(b"\0")
        if fields and not fields[-1]:
            fields.pop()
        if len(fields) % 2 != 0:
            raise SupplementFormatError("malformed no-rename name-status stream")
        rows: list[tuple[str, str]] = []
        for index in range(0, len(fields), 2):
            try:
                status = fields[index].decode("ascii")
                path = fields[index + 1].decode("utf-8")
            except UnicodeDecodeError as exc:
                raise SupplementFormatError(
                    "name-status stream encoding is invalid"
                ) from exc
            rows.append((status, path))
        return tuple(rows)


class DeltaMaterialityClassifier:
    """Own the ordered exhaustive 565-path materiality partition."""

    __slots__ = ()

    @staticmethod
    def execute(
        path: str,
        status: DeltaStatus,
    ) -> tuple[MaterialityCategory, tuple[ExtractionRole, ...], str | None]:
        """Return one closed category, extraction-role set, and optional reason."""
        if status is DeltaStatus.DELETED:
            category = DeltaMaterialityClassifier._category(path)
            return (
                category,
                (ExtractionRole.IDENTITY_ONLY,),
                "absent from target current universe; base identity retained",
            )
        return DeltaMaterialityClassifier._present(path)

    @staticmethod
    def _present(
        path: str,
    ) -> tuple[MaterialityCategory, tuple[ExtractionRole, ...], str | None]:
        if path == ".pi/evidence/python-conformance/module-inventory.json":
            return (
                MaterialityCategory.CONFORMANCE_INVENTORY,
                (ExtractionRole.IDENTITY_ONLY,),
                "generated verification/projection fact only",
            )
        if path.startswith(".pi/checkpoints/") and path.endswith(".json"):
            return MaterialityCategory.CHECKPOINT, (ExtractionRole.AUTHORITY,), None
        if path.startswith("calculations/") and path.endswith(".py"):
            return (
                MaterialityCategory.CALCULATION_PYTHON,
                (ExtractionRole.CONSUMER,),
                None,
            )
        if path.startswith("calculations/") and path.endswith(".md"):
            return (
                MaterialityCategory.CALCULATION_DOCUMENTATION,
                (ExtractionRole.DOCUMENTATION,),
                None,
            )
        if path.startswith("calculations/"):
            return (
                MaterialityCategory.CALCULATION_CONTEXT,
                (ExtractionRole.IDENTITY_ONLY,),
                "opaque scientific/calculation context",
            )
        if path.startswith(("docs/api/", "docs/user-guide/")):
            return (
                MaterialityCategory.PUBLIC_DOCUMENTATION,
                (ExtractionRole.DOCUMENTATION,),
                None,
            )
        if path.startswith("docs/architecture/"):
            return (
                MaterialityCategory.ARCHITECTURE_DOCUMENTATION,
                (ExtractionRole.AUTHORITY,),
                None,
            )
        if path.startswith("docs/publications/"):
            return (
                MaterialityCategory.PUBLICATION_CONTEXT,
                (ExtractionRole.IDENTITY_ONLY,),
                "identity-only publication context",
            )
        if path.startswith("harness/state/"):
            return (
                MaterialityCategory.HARNESS_STATE,
                (ExtractionRole.IDENTITY_ONLY,),
                "generated-state identity and metadata only",
            )
        if path == "harness/task-graph.json":
            return (
                MaterialityCategory.HARNESS_TASK_GRAPH,
                (ExtractionRole.IDENTITY_ONLY,),
                "generated projection identity only",
            )
        if path.startswith("python/src/") and path.endswith(".py"):
            return (
                MaterialityCategory.PRODUCTION_MODULE,
                (ExtractionRole.PRODUCTION, ExtractionRole.RUNTIME),
                None,
            )
        if path.startswith("python/tests/") and path.endswith(".py"):
            return MaterialityCategory.MAINTAINED_TEST, (ExtractionRole.CONSUMER,), None
        if path.startswith("python/tests/"):
            return (
                MaterialityCategory.TEST_RESOURCE,
                (ExtractionRole.IDENTITY_ONLY,),
                "non-Python maintained test resource; identity retained without semantic parsing",
            )
        if path in {"python/pyproject.toml", "python/uv.lock"}:
            return (
                MaterialityCategory.PYTHON_ENVIRONMENT,
                (ExtractionRole.IDENTITY_ONLY,),
                "package and runtime environment identity only",
            )
        if path.startswith("tasks/"):
            return MaterialityCategory.TASK_AUTHORITY, (ExtractionRole.AUTHORITY,), None
        if path == "THIRD_PARTY_NOTICES.md":
            return (
                MaterialityCategory.LICENSE_CONTEXT,
                (ExtractionRole.IDENTITY_ONLY,),
                "identity-only licensing context",
            )
        raise SupplementFormatError(f"delta path has no materiality category: {path}")

    @staticmethod
    def _category(path: str) -> MaterialityCategory:
        category, _, _ = DeltaMaterialityClassifier._present(path)
        return category


@dataclass(frozen=True, slots=True)
class CurrentFactSupplementAcquirer:
    """Acquire and materialize the explicit content-identified supplement inputs."""

    repository_root: Path
    snapshot_root: Path

    def execute(self, selection_path: Path) -> AcquisitionManifest:
        """Acquire exact commits and selected bytes into one isolated snapshot."""
        selection_payload = selection_path.read_bytes()
        selections = SelectionSerializer().decode(selection_payload)
        git = ExplicitGitObjectReader(self.repository_root)
        topology = self._topology(git)
        base_tree = git.tree(BASE_TREE)
        target_tree = git.tree(TARGET_TREE)
        delta_rows = git.changed_paths(BASE_COMMIT, TARGET_COMMIT)
        nul_payload = b"".join(
            status.encode("ascii") + b"\0" + path.encode("utf-8") + b"\0"
            for status, path in delta_rows
        )
        lf_payload = b"".join(
            status.encode("ascii") + b"\t" + path.encode("utf-8") + b"\n"
            for status, path in delta_rows
        )
        if (
            hashlib.sha256(nul_payload).hexdigest() != NAME_STATUS_NUL_SHA256
            or hashlib.sha256(lf_payload).hexdigest() != NAME_STATUS_LF_SHA256
        ):
            raise SupplementFormatError("no-rename name-status identity mismatch")
        merge_paths = {path for _, path in git.changed_paths(BASE_COMMIT, MERGE_COMMIT)}
        cleanup_paths = {
            path for _, path in git.changed_paths(MERGE_COMMIT, TARGET_COMMIT)
        }
        ledger = tuple(
            self._ledger_entry(
                status, path, base_tree, target_tree, merge_paths, cleanup_paths, git
            )
            for status, path in delta_rows
        )
        if tuple(item.path.as_posix() for item in ledger) != tuple(
            sorted(item.path.as_posix() for item in ledger)
        ):
            raise SupplementFormatError("delta ledger is not path sorted")
        inputs = tuple(
            self._input(entry, target_tree, base_tree, git) for entry in selections
        )
        return AcquisitionManifest(
            schema_version=1,
            subject_identity="ksdft2effmass.python.public-import-current-fact-supplement-inputs",
            topology=topology,
            selection_sha256=hashlib.sha256(selection_payload).hexdigest(),
            inputs=inputs,
            delta_ledger=ledger,
        )

    @staticmethod
    def _topology(git: ExplicitGitObjectReader) -> CommitTopology:
        expected = {
            BASE_COMMIT: BASE_TREE,
            MERGE_COMMIT: MERGE_TREE,
            TARGET_COMMIT: TARGET_TREE,
        }
        for commit, tree in expected.items():
            if git.text(("rev-parse", f"{commit}^{{tree}}")) != tree:
                raise SupplementFormatError(f"tree identity mismatch for {commit}")
        merge_parents = tuple(
            git.text(("show", "-s", "--format=%P", MERGE_COMMIT)).split()
        )
        target_parents = tuple(
            git.text(("show", "-s", "--format=%P", TARGET_COMMIT)).split()
        )
        if merge_parents != MERGE_PARENTS or target_parents != (TARGET_PARENT,):
            raise SupplementFormatError("fixed commit parent topology mismatch")
        if (
            git.text(("diff", "--shortstat", BASE_COMMIT, TARGET_COMMIT))
            != SHORTSTAT_TEXT
        ):
            raise SupplementFormatError("fixed interval shortstat mismatch")
        if (
            git.execute(("merge-base", "--is-ancestor", BASE_COMMIT, TARGET_COMMIT))
            != b""
        ):
            raise SupplementFormatError("base commit is not an ancestor of target")
        return CommitTopology(
            base_commit=BASE_COMMIT,
            base_tree=BASE_TREE,
            merge_commit=MERGE_COMMIT,
            merge_tree=MERGE_TREE,
            merge_parents=MERGE_PARENTS,
            target_commit=TARGET_COMMIT,
            target_tree=TARGET_TREE,
            target_parent=TARGET_PARENT,
            name_status_lf_sha256=NAME_STATUS_LF_SHA256,
            name_status_nul_sha256=NAME_STATUS_NUL_SHA256,
            shortstat_insertions=SHORTSTAT_INSERTIONS,
            shortstat_deletions=SHORTSTAT_DELETIONS,
        )

    def _ledger_entry(
        self,
        status: str,
        path: str,
        base_tree: dict[str, GitTreeRecord],
        target_tree: dict[str, GitTreeRecord],
        merge_paths: set[str],
        cleanup_paths: set[str],
        git: ExplicitGitObjectReader,
    ) -> DeltaLedgerEntry:
        if status not in {"A", "D", "M"}:
            raise SupplementFormatError(f"unsupported no-rename delta status: {status}")
        target = (
            AbsentTreeEntry()
            if status == "D"
            else self._present(target_tree, path, git)
        )
        base = (
            AbsentTreeEntry() if status == "A" else self._present(base_tree, path, git)
        )
        in_merge, in_cleanup = path in merge_paths, path in cleanup_paths
        if in_merge and in_cleanup:
            touch = DeltaTouch.BOTH
        elif in_merge:
            touch = DeltaTouch.MERGE_ONLY
        elif in_cleanup:
            touch = DeltaTouch.POST_MERGE_ONLY
        else:
            raise SupplementFormatError(f"delta path has no commit provenance: {path}")
        delta_status = {
            "A": DeltaStatus.ADDED,
            "D": DeltaStatus.DELETED,
            "M": DeltaStatus.MODIFIED,
        }[status]
        category, roles, reason = DeltaMaterialityClassifier.execute(path, delta_status)
        return DeltaLedgerEntry(
            path=PurePosixPath(path),
            status=delta_status,
            base=base,
            target=target,
            touch=touch,
            category=category,
            extraction_roles=roles,
            identity_only_reason=reason,
        )

    def _input(
        self,
        selection: SelectionEntry,
        target_tree: dict[str, GitTreeRecord],
        base_tree: dict[str, GitTreeRecord],
        git: ExplicitGitObjectReader,
    ) -> ManifestInput:
        path = selection.path.as_posix()
        if selection.variant is InputVariant.TASK_TOOL:
            absolute = (self.repository_root / path).resolve()
            if (
                not absolute.is_relative_to(self.repository_root.resolve())
                or not absolute.is_file()
                or absolute.is_symlink()
            ):
                raise SupplementFormatError(
                    f"task tool is not a regular confined file: {path}"
                )
            payload = absolute.read_bytes()
            oid = hashlib.sha1(
                f"blob {len(payload)}\0".encode("ascii") + payload
            ).hexdigest()
            mode = "100755" if absolute.stat().st_mode & 0o111 else "100644"
            present = PresentTreeEntry(
                mode=mode,
                blob_oid=oid,
                sha256=hashlib.sha256(payload).hexdigest(),
                byte_count=len(payload),
            )
            namespace = PurePosixPath("task-tools") / selection.path
        else:
            tree = (
                base_tree
                if selection.variant is InputVariant.BASE_TREE
                else target_tree
            )
            present = self._present(tree, path, git)
            payload = git.blob(present.blob_oid)
            namespace = (
                PurePosixPath(
                    "base" if selection.variant is InputVariant.BASE_TREE else "target"
                )
                / selection.path
            )
        snapshot_path: PurePosixPath | None = None
        if ExtractionRole.IDENTITY_ONLY not in selection.roles:
            snapshot_path = namespace
            destination = self.snapshot_root / namespace.as_posix()
            destination.parent.mkdir(parents=True, exist_ok=True)
            if destination.exists():
                raise SupplementFormatError(
                    f"snapshot destination already exists: {namespace}"
                )
            destination.write_bytes(payload)
        return ManifestInput(
            selection=selection, tree_entry=present, snapshot_path=snapshot_path
        )

    @staticmethod
    def _present(
        tree: dict[str, GitTreeRecord], path: str, git: ExplicitGitObjectReader
    ) -> PresentTreeEntry:
        record = tree.get(path)
        if record is None:
            raise SupplementFormatError(
                f"selected path is absent from exact tree: {path}"
            )
        payload = git.blob(record.oid)
        return PresentTreeEntry(
            mode=record.mode,
            blob_oid=record.oid,
            sha256=hashlib.sha256(payload).hexdigest(),
            byte_count=len(payload),
        )


class AcquisitionManifestSerializer:
    """Serialize and parse the closed acquisition manifest."""

    __slots__ = ()

    def encode(self, manifest: AcquisitionManifest) -> bytes:
        """Return canonical bytes for one validated manifest."""
        root: JsonRecord = {
            "delta_ledger": [
                self.ledger_record(item) for item in manifest.delta_ledger
            ],
            "inputs": [self._input_record(item) for item in manifest.inputs],
            "schema_version": manifest.schema_version,
            "selection_sha256": manifest.selection_sha256,
            "subject_identity": manifest.subject_identity,
            "topology": self.topology_record(manifest.topology),
        }
        return SupplementJsonCodec().encode(root)

    def decode(self, payload: bytes) -> AcquisitionManifest:
        """Decode exact canonical manifest bytes into closed records."""
        root = self._record(SupplementJsonCodec().decode(payload), "manifest")
        self._keys(
            root,
            {
                "delta_ledger",
                "inputs",
                "schema_version",
                "selection_sha256",
                "subject_identity",
                "topology",
            },
            "manifest",
        )
        topology = self.parse_topology_value(root["topology"])
        inputs = tuple(
            self._parse_input(value, index)
            for index, value in enumerate(self._array(root["inputs"], "inputs"))
        )
        ledger = self.parse_ledger_values(root["delta_ledger"])
        manifest = AcquisitionManifest(
            schema_version=self._integer(root["schema_version"], "schema_version"),
            subject_identity=self._text(root["subject_identity"], "subject_identity"),
            topology=topology,
            selection_sha256=self._text(root["selection_sha256"], "selection_sha256"),
            inputs=inputs,
            delta_ledger=ledger,
        )
        if self.encode(manifest) != payload:
            raise SupplementFormatError("manifest JSON is not canonical")
        return manifest

    @staticmethod
    def _tree(entry: PresentTreeEntry | AbsentTreeEntry) -> JsonRecord:
        if isinstance(entry, AbsentTreeEntry):
            return {"kind": "AbsentTreeEntry", "state": entry.state}
        return {
            "blob_oid": entry.blob_oid,
            "byte_count": entry.byte_count,
            "kind": "PresentTreeEntry",
            "mode": entry.mode,
            "sha256": entry.sha256,
        }

    @classmethod
    def ledger_record(cls, item: DeltaLedgerEntry) -> JsonRecord:
        return {
            "base": cls._tree(item.base),
            "category": item.category.value,
            "extraction_roles": [role.value for role in item.extraction_roles],
            "identity_only_reason": item.identity_only_reason,
            "path": item.path.as_posix(),
            "status": item.status.value,
            "target": cls._tree(item.target),
            "touch": item.touch.value,
        }

    @classmethod
    def _input_record(cls, item: ManifestInput) -> JsonRecord:
        return {
            "category": item.selection.category.value,
            "path": item.selection.path.as_posix(),
            "roles": [role.value for role in item.selection.roles],
            "snapshot_path": None
            if item.snapshot_path is None
            else item.snapshot_path.as_posix(),
            "source": cls._tree(item.tree_entry),
            "variant": item.selection.variant.value,
        }

    @staticmethod
    def topology_record(item: CommitTopology) -> JsonRecord:
        return {
            "base_commit": item.base_commit,
            "base_tree": item.base_tree,
            "merge_commit": item.merge_commit,
            "merge_parents": list(item.merge_parents),
            "merge_tree": item.merge_tree,
            "name_status_lf_sha256": item.name_status_lf_sha256,
            "name_status_nul_sha256": item.name_status_nul_sha256,
            "shortstat_deletions": item.shortstat_deletions,
            "shortstat_insertions": item.shortstat_insertions,
            "target_commit": item.target_commit,
            "target_parent": item.target_parent,
            "target_tree": item.target_tree,
        }

    def _parse_input(self, value: JsonValue, index: int) -> ManifestInput:
        label = f"inputs[{index}]"
        row = self._record(value, label)
        self._keys(
            row,
            {"category", "path", "roles", "snapshot_path", "source", "variant"},
            label,
        )
        raw_snapshot = row["snapshot_path"]
        if raw_snapshot is not None and type(raw_snapshot) is not str:
            raise SupplementFormatError(f"{label}.snapshot_path must be text or null")
        selection = SelectionEntry(
            variant=InputVariant(self._text(row["variant"], f"{label}.variant")),
            category=SelectionCategory(
                self._text(row["category"], f"{label}.category")
            ),
            roles=tuple(
                ExtractionRole(self._text(item, f"{label}.roles"))
                for item in self._array(row["roles"], f"{label}.roles")
            ),
            path=PurePosixPath(self._text(row["path"], f"{label}.path")),
        )
        source = self._parse_tree(
            self._record(row["source"], f"{label}.source"), f"{label}.source"
        )
        if type(source) is not PresentTreeEntry:
            raise SupplementFormatError(f"{label}.source must be present")
        return ManifestInput(
            selection=selection,
            tree_entry=source,
            snapshot_path=None if raw_snapshot is None else PurePosixPath(raw_snapshot),
        )

    def parse_ledger_values(self, value: JsonValue) -> tuple[DeltaLedgerEntry, ...]:
        """Parse a closed canonical ledger array."""
        return tuple(
            self._parse_ledger(item, index)
            for index, item in enumerate(self._array(value, "delta_ledger"))
        )

    def _parse_ledger(self, value: JsonValue, index: int) -> DeltaLedgerEntry:
        label = f"delta_ledger[{index}]"
        row = self._record(value, label)
        self._keys(
            row,
            {
                "base",
                "category",
                "extraction_roles",
                "identity_only_reason",
                "path",
                "status",
                "target",
                "touch",
            },
            label,
        )
        base = self._parse_tree(
            self._record(row["base"], f"{label}.base"), f"{label}.base"
        )
        target = self._parse_tree(
            self._record(row["target"], f"{label}.target"), f"{label}.target"
        )
        reason = row["identity_only_reason"]
        if reason is not None and type(reason) is not str:
            raise SupplementFormatError(
                f"{label}.identity_only_reason must be text or null"
            )
        return DeltaLedgerEntry(
            path=PurePosixPath(self._text(row["path"], f"{label}.path")),
            status=DeltaStatus(self._text(row["status"], f"{label}.status")),
            base=base,
            target=target,
            touch=DeltaTouch(self._text(row["touch"], f"{label}.touch")),
            category=MaterialityCategory(
                self._text(row["category"], f"{label}.category")
            ),
            extraction_roles=tuple(
                ExtractionRole(self._text(item, f"{label}.extraction_roles"))
                for item in self._array(
                    row["extraction_roles"], f"{label}.extraction_roles"
                )
            ),
            identity_only_reason=reason,
        )

    def parse_topology_value(self, value: JsonValue) -> CommitTopology:
        """Parse one closed topology value."""
        row = self._record(value, "topology")
        keys = {
            "base_commit",
            "base_tree",
            "merge_commit",
            "merge_parents",
            "merge_tree",
            "name_status_lf_sha256",
            "name_status_nul_sha256",
            "shortstat_deletions",
            "shortstat_insertions",
            "target_commit",
            "target_parent",
            "target_tree",
        }
        self._keys(row, keys, "topology")
        parents = self._array(row["merge_parents"], "merge_parents")
        if len(parents) != 2:
            raise SupplementFormatError("merge_parents must contain two values")
        return CommitTopology(
            base_commit=self._text(row["base_commit"], "base_commit"),
            base_tree=self._text(row["base_tree"], "base_tree"),
            merge_commit=self._text(row["merge_commit"], "merge_commit"),
            merge_tree=self._text(row["merge_tree"], "merge_tree"),
            merge_parents=(
                self._text(parents[0], "merge_parent"),
                self._text(parents[1], "merge_parent"),
            ),
            target_commit=self._text(row["target_commit"], "target_commit"),
            target_tree=self._text(row["target_tree"], "target_tree"),
            target_parent=self._text(row["target_parent"], "target_parent"),
            name_status_lf_sha256=self._text(
                row["name_status_lf_sha256"], "name_status_lf_sha256"
            ),
            name_status_nul_sha256=self._text(
                row["name_status_nul_sha256"], "name_status_nul_sha256"
            ),
            shortstat_insertions=self._integer(
                row["shortstat_insertions"], "shortstat_insertions"
            ),
            shortstat_deletions=self._integer(
                row["shortstat_deletions"], "shortstat_deletions"
            ),
        )

    def _parse_tree(
        self, row: JsonRecord, label: str
    ) -> PresentTreeEntry | AbsentTreeEntry:
        kind = self._text(row.get("kind"), f"{label}.kind")
        if kind == "AbsentTreeEntry":
            self._keys(row, {"kind", "state"}, label)
            return AbsentTreeEntry(state=self._text(row["state"], f"{label}.state"))
        if kind == "PresentTreeEntry":
            self._keys(row, {"blob_oid", "byte_count", "kind", "mode", "sha256"}, label)
            return PresentTreeEntry(
                mode=self._text(row["mode"], f"{label}.mode"),
                blob_oid=self._text(row["blob_oid"], f"{label}.blob_oid"),
                sha256=self._text(row["sha256"], f"{label}.sha256"),
                byte_count=self._integer(row["byte_count"], f"{label}.byte_count"),
            )
        raise SupplementFormatError(f"{label} has unknown tree-entry discriminant")

    @staticmethod
    def _record(value: JsonValue | None, label: str) -> JsonRecord:
        if type(value) is not dict:
            raise SupplementFormatError(f"{label} must be an object")
        return value

    @staticmethod
    def _array(value: JsonValue | None, label: str) -> list[JsonValue]:
        if type(value) is not list:
            raise SupplementFormatError(f"{label} must be an array")
        return value

    @staticmethod
    def _text(value: JsonValue | None, label: str) -> str:
        if type(value) is not str:
            raise SupplementFormatError(f"{label} must be text")
        return value

    @staticmethod
    def _integer(value: JsonValue | None, label: str) -> int:
        if type(value) is not int:
            raise SupplementFormatError(f"{label} must be a built-in integer")
        return value

    @staticmethod
    def _keys(row: JsonRecord, expected: set[str], label: str) -> None:
        if set(row) != expected:
            raise SupplementFormatError(
                f"{label} fields do not match the closed contract"
            )
