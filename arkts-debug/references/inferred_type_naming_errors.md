# Inferred Type Naming Errors

## Symptom

```
The inferred type of 'xxx' cannot be named without a reference to 'xxx'. This is likely not portable. A type annotation is necessary.
```

Triggered by exported functions or variables whose inferred return type references an internal module that is not re-exported.

## Root Cause

When an exported symbol's type is inferred (not explicitly annotated), the ArkTS compiler must be able to name that type using only the public API surface. If the inferred type depends on a type from an internal or un-re-exported module, the compiler cannot produce a portable type declaration. ArkTS enforces this strictly to ensure that compiled output is self-contained and does not leak internal module references.

## Canonical Fix

Add an explicit return type annotation to the exported symbol:

```ts
import { InternalHelper } from './internal';

// BAD: inferred return type references InternalHelper
// export function createHelper() {
//   return new InternalHelper();
// }

// GOOD: explicit return type
export function createHelper(): InternalHelper {
  return new InternalHelper();
}
```

If the return type itself is from an internal module, either re-export the type or use a public interface:

```ts
// Re-export the type so consumers can name it
export { InternalHelper } from './internal';

// Or use a public interface as the return type
export interface Helper {
  doWork(): void;
}

export function createHelper(): Helper {
  return new InternalHelper();
}
```

## Notes

- This error commonly appears when refactoring modules — moving a type to a new file without updating exports.
- The fix is always an explicit type annotation; `as` type assertions do not resolve this error.
- If the function returns a complex type (e.g., a union or intersection), consider defining a named type alias for it.

## See Also

- `assets/InferredTypeNamingError.ets`
