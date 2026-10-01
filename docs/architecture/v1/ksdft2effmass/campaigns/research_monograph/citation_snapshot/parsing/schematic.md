# Parsing schematic

```mermaid
flowchart LR
    tex[Exact UTF-8 TeX bytes] --> comments[Offset-preserving comment mask]
    comments --> grammar[Closed command and definition grammar]
    grammar --> events[Calls, markers, includes, source gaps]
    bib[Exact UTF-8 BibLaTeX bytes] --> entries[Ordered entry boundaries and keys]
    grammar --> fail[Fail closed]
    entries --> fail
```

Parsed records are internal observations. They retain keys, command metadata,
relative include tokens, and character spans only; the compiler converts spans to
UTF-8 byte locators against exact source identities.
