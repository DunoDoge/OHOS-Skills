## MODIFIED Requirements

### Requirement: PossiblyNullError.ets SHALL use constructor instead of type assertion
The code asset `assets/PossiblyNullError.ets` SHALL NOT use `as User` type assertion on object literals. The `findUser` function SHALL use `new User()` constructor to create User instances instead of `{ id: 1, name: 'Alice' } as User`.

#### Scenario: PossiblyNullError.ets compiles without as-assertion
- **WHEN** `PossiblyNullError.ets` is compiled with ArkTS strict mode
- **THEN** the code SHALL NOT contain any `as User` type assertion on object literals and SHALL compile without errors

### Requirement: IDataSourceError.ets SHALL use correct LazyForEach callback signature
The code asset `assets/IDataSourceError.ets` SHALL NOT annotate the LazyForEach item builder callback with `: void` return type. The callback SHALL let the compiler infer the component return type.

#### Scenario: IDataSourceError.ets compiles with correct LazyForEach signature
- **WHEN** `IDataSourceError.ets` is compiled with ArkTS strict mode
- **THEN** the LazyForEach second argument SHALL NOT have `: void` return type annotation and SHALL compile without errors

### Requirement: ObjectSpreadError.ets SHALL NOT use Partial mapped type
The code asset `assets/ObjectSpreadError.ets` SHALL NOT use `Partial<Point>` utility type. The merge helper SHALL use an explicitly defined interface (e.g., `PatchPoint`) with optional fields instead.

#### Scenario: ObjectSpreadError.ets compiles without Partial type
- **WHEN** `ObjectSpreadError.ets` is compiled with ArkTS strict mode
- **THEN** the code SHALL NOT contain `Partial<>` and SHALL compile without errors

### Requirement: StandaloneFunctionError.ets SHALL NOT use constructor parameter properties
The code asset `assets/StandaloneFunctionError.ets` SHALL NOT use `constructor(private context: ...)` parameter property shorthand. The class SHALL declare the `private context` field explicitly and assign it in the constructor body.

#### Scenario: StandaloneFunctionError.ets compiles without parameter properties
- **WHEN** `StandaloneFunctionError.ets` is compiled with ArkTS strict mode
- **THEN** the code SHALL NOT use constructor parameter property shorthand and SHALL compile without errors

### Requirement: Reference documents SHALL match updated asset code
The corresponding reference documents (`references/possibly_null_errors.md`, `references/idata_source_errors.md`, `references/object_spread_errors.md`, `references/standalone_function_errors.md`) SHALL be updated to reflect the code changes in their respective assets.

#### Scenario: Reference docs show compliant code examples
- **WHEN** a user reads any of the four reference documents
- **THEN** the code examples SHALL match the updated asset files and SHALL NOT contain ArkTS-prohibited patterns (as-assertion on literals, Partial type, constructor parameter properties, void return on LazyForEach callback)
