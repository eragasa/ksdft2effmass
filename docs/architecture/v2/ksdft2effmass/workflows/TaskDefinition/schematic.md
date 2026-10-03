# `TaskDefinition` schematic

```mermaid
classDiagram
    class TaskDefinitionIdentity
    class TaskExecutionKind
    class TaskDefinition {
        <<concrete frozen DataObject>>
        +identity TaskDefinitionIdentity
        +execution_kind TaskExecutionKind
    }
    class AbstractTask {
        <<ABC>>
        +identity TaskDefinitionIdentity*
        +definition TaskDefinition
    }

    TaskDefinition --> TaskDefinitionIdentity
    TaskDefinition --> TaskExecutionKind
    AbstractTask --> TaskDefinition : constructs final generic value
```

One generic definition type serves every operation. Scientific and calculator-specific
configuration remains with its domain owner rather than producing Task-definition
subclasses.
