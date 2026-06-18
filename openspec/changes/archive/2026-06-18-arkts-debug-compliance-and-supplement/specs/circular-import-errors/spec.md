## ADDED Requirements

### Requirement: Circular import error reference document
The system SHALL provide a reference document `references/circular_import_errors.md` that documents the error "Could not load ${file1} (imported by ${file2}): Maximum call stack size exceeded", including Symptom, Root Cause, Canonical Fix, Notes, and See Also sections.

#### Scenario: User encounters circular import error
- **WHEN** a user has circular imports between modules and ArkCompiler reports "Maximum call stack size exceeded" during module loading
- **THEN** the reference document SHALL explain that ArkTS does not support circular module dependencies and recommend extracting shared types into a separate module or using lazy imports

### Requirement: Circular import error code asset
The system SHALL provide a code asset `assets/CircularImportError.ets` that demonstrates the circular import anti-pattern (as BAD comment) and the correct shared-module extraction pattern (as GOOD code), and the GOOD code SHALL compile under ArkTS strict mode.

#### Scenario: Code asset demonstrates circular import fix
- **WHEN** the code asset is compiled with ArkTS strict mode
- **THEN** the GOOD section SHALL compile without errors and the BAD section SHALL be commented out showing the prohibited circular import pattern
