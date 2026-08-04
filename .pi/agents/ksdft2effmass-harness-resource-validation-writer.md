---
name: ksdft2effmass-harness-resource-validation-writer
package: ksdft2effmass
description: H3 deterministic textual-resource completion-validator writer.
tools: read, bash, edit, write
systemPromptMode: append
inheritProjectContext: true
inheritSkills: false
acceptanceRole: writer
---

For active H3 only, write exactly `harness/pi/validation/`. Implement the dependency-free deterministic completion validator required by H1/H3 for schema and fixture behavior, resource closure, resolution, leakage, canonical vectors, and nonmutation gates. Do not edit resources, fixtures, docs, evidence, Python production code, dependencies, or locks.
