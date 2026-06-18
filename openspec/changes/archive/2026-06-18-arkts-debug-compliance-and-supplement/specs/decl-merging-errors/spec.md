## ADDED Requirements

### Requirement: Declaration merging error reference document
The system SHALL provide a reference document `references/decl_merging_errors.md` that documents the `arkts-no-decl-merging` error and `Cannot redeclare block-scoped variable` error, including Symptom, Root Cause, Canonical Fix, Notes, and See Also sections.

#### Scenario: User encounters arkts-no-decl-merging error
- **WHEN** a user's code merges declarations (e.g., same-named interface declared twice, or namespace merging) and ArkCompiler reports `arkts-no-decl-merging`
- **THEN** the reference document SHALL explain that ArkTS prohibits declaration merging and recommend consolidating into a single declaration

### Requirement: Declaration merging error code asset
The system SHALL provide a code asset `assets/DeclMergingError.ets` that demonstrates the incorrect declaration merging pattern (as BAD comment) and the correct single-declaration pattern (as GOOD code), and the GOOD code SHALL compile under ArkTS strict mode.

#### Scenario: Code asset demonstrates declaration merging fix
- **WHEN** the code asset is compiled with ArkTS strict mode
- **THEN** the GOOD section SHALL compile without errors and the BAD section SHALL be commented out showing the prohibited merging pattern
