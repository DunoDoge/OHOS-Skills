## ADDED Requirements

### Requirement: Inferred type naming error reference document
The system SHALL provide a reference document `references/inferred_type_naming_errors.md` that documents the error "The inferred type of 'xxx' cannot be named without a reference to 'xxx'. This is likely not portable. A type annotation is necessary.", including Symptom, Root Cause, Canonical Fix, Notes, and See Also sections.

#### Scenario: User encounters inferred type naming error
- **WHEN** a user's exported function/variable has a return type that the compiler cannot name without referencing an internal module and ArkCompiler reports the inferred type naming error
- **THEN** the reference document SHALL explain that ArkTS requires explicit type annotations for exported symbols and recommend adding explicit return type annotations or re-exporting the dependent type

### Requirement: Inferred type naming error code asset
The system SHALL provide a code asset `assets/InferredTypeNamingError.ets` that demonstrates the incorrect implicit return type pattern (as BAD comment) and the correct explicit type annotation pattern (as GOOD code), and the GOOD code SHALL compile under ArkTS strict mode.

#### Scenario: Code asset demonstrates inferred type naming fix
- **WHEN** the code asset is compiled with ArkTS strict mode
- **THEN** the GOOD section SHALL compile without errors and the BAD section SHALL be commented out showing the prohibited implicit type pattern
