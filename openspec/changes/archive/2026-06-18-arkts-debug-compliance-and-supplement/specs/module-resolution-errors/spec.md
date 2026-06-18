## ADDED Requirements

### Requirement: Module resolution error reference document
The system SHALL provide a reference document `references/module_resolution_errors.md` that documents the errors "Cannot find module XXX or its corresponding type declarations" and "Module 'xxx' has no exported member 'yyy'", including Symptom, Root Cause, Canonical Fix, Notes, and See Also sections.

#### Scenario: User encounters Cannot find module error
- **WHEN** a user imports a module that cannot be resolved and ArkCompiler reports "Cannot find module XXX or its corresponding type declarations"
- **THEN** the reference document SHALL explain common causes (missing oh-package.json5 dependency, incorrect import path, case sensitivity mismatch) and recommend checking ohpm install, verifying import paths, and ensuring case-sensitive file names

### Requirement: Module resolution error code asset
The system SHALL provide a code asset `assets/ModuleResolutionError.ets` that demonstrates common module resolution mistakes (as BAD comment) and correct import patterns (as GOOD code), and the GOOD code SHALL compile under ArkTS strict mode.

#### Scenario: Code asset demonstrates module resolution fix
- **WHEN** the code asset is compiled with ArkTS strict mode
- **THEN** the GOOD section SHALL compile without errors and the BAD section SHALL be commented out showing the prohibited incorrect import pattern
