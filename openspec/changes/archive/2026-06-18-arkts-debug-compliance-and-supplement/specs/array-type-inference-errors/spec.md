## ADDED Requirements

### Requirement: Array type inference error reference document
The system SHALL provide a reference document `references/array_type_inference_errors.md` that documents the error caused by empty array declarations with missing element types (e.g., `[][] = []`), including Symptom, Root Cause, Canonical Fix, Notes, and See Also sections.

#### Scenario: User encounters empty array type inference error
- **WHEN** a user declares an array with missing element type like `public a: [][] = []` and ArkCompiler reports "Cannot read properties of undefined" or a type inference error
- **THEN** the reference document SHALL explain that ArkTS requires explicit element types for all array declarations and recommend using `string[][]` instead of `[][]`

### Requirement: Array type inference error code asset
The system SHALL provide a code asset `assets/ArrayTypeInferenceError.ets` that demonstrates the incorrect empty array type pattern (as BAD comment) and the correct explicit element type pattern (as GOOD code), and the GOOD code SHALL compile under ArkTS strict mode.

#### Scenario: Code asset demonstrates array type inference fix
- **WHEN** the code asset is compiled with ArkTS strict mode
- **THEN** the GOOD section SHALL compile without errors and the BAD section SHALL be commented out showing the prohibited `[][]` pattern
