## ADDED Requirements

### Requirement: Indexed access error reference document
The system SHALL provide a reference document `references/indexed_access_errors.md` that documents the `arkts-no-props-by-index` error, including Symptom, Root Cause, Canonical Fix, Notes, and See Also sections.

#### Scenario: User encounters arkts-no-props-by-index error
- **WHEN** a user's code uses indexed access syntax like `obj['key']` or `obj[variable]` and ArkCompiler reports `arkts-no-props-by-index`
- **THEN** the reference document SHALL explain that ArkTS prohibits indexed property access and recommend using dot notation (`obj.key`) or `Map<keyType, valueType>` as alternatives

### Requirement: Indexed access error code asset
The system SHALL provide a code asset `assets/IndexedAccessError.ets` that demonstrates the incorrect indexed access pattern (as BAD comment) and the correct dot-notation / Map pattern (as GOOD code), and the GOOD code SHALL compile under ArkTS strict mode.

#### Scenario: Code asset demonstrates indexed access fix
- **WHEN** the code asset is compiled with ArkTS strict mode
- **THEN** the GOOD section SHALL compile without errors and the BAD section SHALL be commented out showing the prohibited pattern
