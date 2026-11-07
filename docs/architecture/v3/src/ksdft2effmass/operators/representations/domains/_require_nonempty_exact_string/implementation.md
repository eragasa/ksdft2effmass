# Implementation

A non-exact string raises `TypeError` using the supplied field name. Empty text raises
`ValueError`. The function returns its input so constructors may validate inline. It is
private, absent from `__all__`, and intentionally local to the domain module.
