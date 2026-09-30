# `ManuscriptTargetContext`

`ManuscriptTargetContext` is a frozen, slotted read-only target record. It carries the
root-relative path, exact section heading and label, externally observed Git blob and
complete-file digests, complete section text, and one uniquely occurring selected
span. Init-false revision, target, and span IDs bind these exact values without line
numbers. Construction performs no file or Git access.
