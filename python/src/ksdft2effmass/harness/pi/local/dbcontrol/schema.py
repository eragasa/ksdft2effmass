"""Exact SQLite schema and deterministic table ordering."""

from __future__ import annotations

_SCHEMA = r"""
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = FULL;
PRAGMA page_size = 4096;
CREATE TABLE harness_metadata (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
) WITHOUT ROWID;
CREATE TABLE task_definition (
  task_id TEXT PRIMARY KEY,
  schema_version INTEGER NOT NULL CHECK(schema_version IN (1,2,3)),
  title TEXT NOT NULL,
  objective TEXT NOT NULL,
  source_path TEXT NOT NULL UNIQUE,
  status_detail TEXT,
  explicit_activation_required INTEGER NOT NULL CHECK(explicit_activation_required IN (0,1)),
  intake_path TEXT,
  archive_path TEXT,
  archive_sha256 TEXT CHECK(archive_sha256 IS NULL OR length(archive_sha256)=64)
) WITHOUT ROWID;
CREATE TABLE task_alias (
  alias_id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  alias_kind TEXT NOT NULL CHECK(alias_kind='historical')
) WITHOUT ROWID;
CREATE TABLE task_relationship (
  source_task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  target_task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  relationship_kind TEXT NOT NULL CHECK(relationship_kind IN ('child_of','depends_on','superseded_by','ordered_before')),
  PRIMARY KEY(source_task_id,target_task_id,relationship_kind),
  CHECK(source_task_id<>target_task_id)
) WITHOUT ROWID;
CREATE TABLE task_external_prerequisite (
  task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  prerequisite_id TEXT NOT NULL,
  ordinal INTEGER NOT NULL CHECK(ordinal>=0),
  PRIMARY KEY(task_id,prerequisite_id), UNIQUE(task_id,ordinal)
) WITHOUT ROWID;
CREATE TABLE task_text (
  task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  text_kind TEXT NOT NULL CHECK(text_kind IN ('authority_reference','authorized_scope','completion_criterion','exclusion')),
  ordinal INTEGER NOT NULL CHECK(ordinal>=0),
  value TEXT NOT NULL,
  PRIMARY KEY(task_id,text_kind,ordinal), UNIQUE(task_id,text_kind,value)
) WITHOUT ROWID;
CREATE TABLE task_state (
  task_id TEXT PRIMARY KEY REFERENCES task_definition(task_id),
  lifecycle_status TEXT NOT NULL,
  is_active INTEGER NOT NULL CHECK(is_active IN (0,1)),
  automatic_successor_enabled INTEGER NOT NULL CHECK(automatic_successor_enabled IN (0,1))
) WITHOUT ROWID;
CREATE UNIQUE INDEX one_active_task ON task_state(is_active) WHERE is_active=1;
CREATE TABLE task_state_event (
  event_id TEXT PRIMARY KEY,
  task_id TEXT NOT NULL REFERENCES task_definition(task_id),
  event_ordinal INTEGER NOT NULL CHECK(event_ordinal>=0),
  lifecycle_status TEXT NOT NULL,
  event_kind TEXT NOT NULL CHECK(event_kind IN ('imported','activated','completed','superseded','deferred')),
  UNIQUE(task_id,event_ordinal)
) WITHOUT ROWID;
CREATE TABLE evidence_claim (
  evidence_id TEXT PRIMARY KEY,
  evidence_class TEXT NOT NULL CHECK(evidence_class IN ('software-verification','numerical-verification','scientific-validation','uncertainty-quantification')),
  claim_summary TEXT NOT NULL,
  naming_status TEXT NOT NULL CHECK(naming_status IN ('semantic','temporary-legacy'))
) WITHOUT ROWID;
CREATE TABLE evidence_alias (
  alias_id TEXT PRIMARY KEY,
  evidence_id TEXT NOT NULL REFERENCES evidence_claim(evidence_id),
  alias_kind TEXT NOT NULL CHECK(alias_kind='historical')
) WITHOUT ROWID;
CREATE TABLE test_module (
  module_id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  ownership_kind TEXT NOT NULL CHECK(ownership_kind IN ('class_owned','artifact_owned')),
  owner_subject TEXT NOT NULL,
  evidence_class TEXT NOT NULL CHECK(evidence_class IN ('software-verification','numerical-verification','scientific-validation','uncertainty-quantification')),
  evidence_profile TEXT NOT NULL CHECK(evidence_profile IN ('routine','claim_bearing'))
) WITHOUT ROWID;
CREATE TABLE evidence_predecessor (
  evidence_id TEXT NOT NULL REFERENCES evidence_claim(evidence_id),
  predecessor_node_id TEXT NOT NULL,
  PRIMARY KEY(evidence_id, predecessor_node_id)
) WITHOUT ROWID;
CREATE TABLE evidence_owner (
  evidence_id TEXT PRIMARY KEY REFERENCES evidence_claim(evidence_id),
  module_id TEXT NOT NULL REFERENCES test_module(module_id),
  owner_node_id TEXT NOT NULL UNIQUE,
  owner_kind TEXT NOT NULL CHECK(owner_kind IN ('test_function','artifact_test'))
) WITHOUT ROWID;
CREATE TABLE test_node (
  node_id TEXT PRIMARY KEY,
  module_id TEXT NOT NULL REFERENCES test_module(module_id),
  evidence_id TEXT REFERENCES evidence_claim(evidence_id),
  parameter_id TEXT,
  CHECK(parameter_id IS NULL OR parameter_id GLOB '[a-z0-9_]*')
) WITHOUT ROWID;
CREATE TABLE agent_definition (
  agent_id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  lifecycle TEXT NOT NULL CHECK(lifecycle IN ('durable','historical')),
  access_class TEXT NOT NULL CHECK(access_class IN ('writer','read_only')),
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1))
) WITHOUT ROWID;
CREATE TABLE skill_definition (
  skill_id TEXT PRIMARY KEY,
  canonical_path TEXT NOT NULL,
  live_path TEXT NOT NULL UNIQUE,
  descriptor_path TEXT,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1))
) WITHOUT ROWID;
CREATE TABLE agent_skill_route (
  agent_id TEXT NOT NULL REFERENCES agent_definition(agent_id),
  skill_id TEXT NOT NULL REFERENCES skill_definition(skill_id),
  PRIMARY KEY(agent_id,skill_id)
) WITHOUT ROWID;
CREATE TABLE resource_definition (
  resource_id TEXT PRIMARY KEY,
  layer TEXT NOT NULL CHECK(layer IN ('generic','project_local')),
  resource_kind TEXT NOT NULL,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  format_version INTEGER NOT NULL CHECK(format_version>0),
  enabled INTEGER NOT NULL CHECK(enabled IN (0,1))
) WITHOUT ROWID;
CREATE TABLE resource_dependency (
  dependent_resource_id TEXT NOT NULL REFERENCES resource_definition(resource_id),
  prerequisite_resource_id TEXT NOT NULL REFERENCES resource_definition(resource_id),
  PRIMARY KEY(dependent_resource_id,prerequisite_resource_id),
  CHECK(dependent_resource_id<>prerequisite_resource_id)
) WITHOUT ROWID;
CREATE TABLE resource_profile_membership (
  profile_id TEXT NOT NULL,
  resource_id TEXT NOT NULL REFERENCES resource_definition(resource_id),
  ordinal INTEGER NOT NULL CHECK(ordinal>=0),
  PRIMARY KEY(profile_id,resource_id), UNIQUE(profile_id,ordinal)
) WITHOUT ROWID;
CREATE TABLE decision_reference (
  decision_id TEXT PRIMARY KEY,
  source_path TEXT NOT NULL UNIQUE,
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  related_task_id TEXT REFERENCES task_definition(task_id),
  disposition TEXT,
  resolution_state TEXT NOT NULL CHECK(resolution_state IN ('resolved','unresolved'))
) WITHOUT ROWID;
CREATE TABLE projection_record (
  projection_path TEXT PRIMARY KEY,
  projection_kind TEXT NOT NULL CHECK(projection_kind IN ('task-json','task-graph-json','task-index-markdown','task-markdown','resource-manifest-json','evidence-module-inventory-json')),
  sha256 TEXT NOT NULL CHECK(length(sha256)=64),
  byte_count INTEGER NOT NULL CHECK(byte_count>=0),
  generating_action_id TEXT NOT NULL
) WITHOUT ROWID;
"""  # noqa: E501
_TABLE_ORDER = (
    "harness_metadata",
    "task_definition",
    "task_alias",
    "task_relationship",
    "task_external_prerequisite",
    "task_text",
    "task_state",
    "task_state_event",
    "evidence_claim",
    "evidence_alias",
    "test_module",
    "evidence_predecessor",
    "evidence_owner",
    "test_node",
    "agent_definition",
    "skill_definition",
    "agent_skill_route",
    "resource_definition",
    "resource_dependency",
    "resource_profile_membership",
    "decision_reference",
    "projection_record",
)
