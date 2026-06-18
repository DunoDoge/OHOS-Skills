# Indexed Access Errors

## Symptom

```
Indexed access is not supported for fields (arkts-no-props-by-index)
```

Triggered by:

```ts
const val = obj['key'];
const val = obj[variable];
```

## Root Cause

ArkTS prohibits indexed (bracket notation) property access on objects. Unlike TypeScript, ArkTS requires all property access to be statically resolvable at compile time. Bracket notation with a string literal or variable bypasses static type checking, which conflicts with ArkTS's strict type system design for performance and safety.

## Canonical Fix

Use dot notation for known property names:

```ts
interface Config {
  host: string;
  port: number;
}

const config: Config = { host: 'localhost', port: 8080 };
const host: string = config.host;  // dot notation
```

For dynamic key-value lookups, use `Map` instead of indexed object access:

```ts
const headers: Map<string, string> = new Map();
headers.set('Content-Type', 'application/json');
const contentType: string | undefined = headers.get('Content-Type');
```

## Notes

- String literal bracket notation (`obj['knownKey']`) is also prohibited even when the key is a constant string — use dot notation instead.
- Array index access (`arr[0]`) is allowed since arrays have numeric indices.
- `Map.get()` returns `T | undefined`, so remember to guard against `undefined` (see `possibly_null_errors.md`).

## See Also

- `assets/IndexedAccessError.ets`
