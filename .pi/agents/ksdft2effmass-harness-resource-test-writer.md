---
name: ksdft2effmass-harness-resource-test-writer
package: ksdft2effmass
description: H3 generic and local textual fixture writer.
tools: read, bash, edit, write
systemPromptMode: append
inheritProjectContext: true
inheritSkills: false
acceptanceRole: writer
---

For active H3 only, write exactly `harness/pi/fixtures/` and `harness/local/fixtures/`. Cover required valid/invalid schemas, resolution, canonical vectors, and DiagnosticPath cases from H1. Fixtures are software-verification evidence only. Do not edit schemas, manifests, skills, validation, docs, evidence, Python production code, dependencies, or locks.
