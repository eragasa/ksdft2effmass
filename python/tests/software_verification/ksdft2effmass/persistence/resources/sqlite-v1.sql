-- Synthetic private format-v1 compatibility input, not domain or calculated data.
-- SHA-256 framing: fixed prefix, u64be lengths for stream/revision/schema/content/
-- payload/key; predecessor byte 00 for absent, 01 + u64be length/value for present.
-- UTF-8 surrogatepass identities are BLOBs. Digests below are independently
-- evaluated from hand-written framed hex, not the production row serializer.
CREATE TABLE store_format (format BLOB NOT NULL, version INTEGER NOT NULL);
CREATE TABLE revisions (stream BLOB NOT NULL, revision BLOB NOT NULL, predecessor BLOB, schema_id BLOB NOT NULL, content BLOB NOT NULL, payload BLOB NOT NULL, idempotency BLOB NOT NULL UNIQUE, envelope INTEGER NOT NULL, digest BLOB NOT NULL, PRIMARY KEY (stream, revision), FOREIGN KEY (stream, predecessor) REFERENCES revisions (stream, revision));
CREATE TABLE heads (stream BLOB PRIMARY KEY NOT NULL, revision BLOB NOT NULL, FOREIGN KEY (stream, revision) REFERENCES revisions (stream, revision));
INSERT INTO store_format VALUES (X'6b73646674326566666d6173732e73716c6974652e7265766973696f6e73', 1);
INSERT INTO revisions VALUES (X'73', X'7231', NULL, X'736368656d61', X'636f6e74656e74', X'00ff', X'6b31', 1, X'01aa55290d7c26fb2c97b172b4f681321c799239dad65c7550146f4846c3d1ee');
INSERT INTO revisions VALUES (X'73', X'7232', X'7231', X'736368656d61', X'636f6e74656e74', X'02', X'6b32', 1, X'afcae97cd9af2fd5c57769e57c9bb2edfcd4ffccf8d59514ea0f89575611757a');
INSERT INTO heads VALUES (X'73', X'7232');
