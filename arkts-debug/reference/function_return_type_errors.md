# Function Return Type Errors

## Symptom

```
Function lacks ending return statement and return type does not include 'undefined'.
Type '...' is not assignable to type '...'.
arkts-no-implicit-return-types (in strict configurations)
```

## Root Cause

ArkTS infers return types only from very simple shapes. As soon as a function has multiple return paths, async, or returns a class instance built via builder calls, inference falls back to a too-wide type and downstream usage fails.

## Canonical Fix

Always annotate non-trivial functions with an explicit return type:

```ts
function loadUser(id: number): Promise<User> {
  return userApi.fetch(id);
}

function pickName(u: User | undefined): string {
  return u?.name ?? 'anon';
}
```

For builders / chained DSLs, annotate even one-liners:

```ts
function makeRequest(): http.HttpRequest {
  return http.createHttp();
}
```

## Notes

- Combine with explicit parameter types - never rely on contextual typing alone.
- For `void` callbacks, write `: void` explicitly to prevent accidental returns being typed.

## See Also

- `assets/FunctionReturnTypeError.ets`
