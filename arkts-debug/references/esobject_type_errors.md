# ESObject Type Errors

## Symptom

```
arkts-no-esobject (variant)
'ESObject' is restricted; use a concrete type or 'ESModule' instead.
Type 'ESObject' is not assignable to type 'X'.
```

## Root Cause

`ESObject` is an escape hatch for interop with native ES modules. ArkTS strict rules disallow it from leaking into application logic - it cannot be assigned to typed locals, returned from app APIs, or used as a generic argument.

## Canonical Fix

Replace with a concrete type. If the value comes from a native module, declare an interface that mirrors the actual shape:

```ts
interface NativeUser {
  id: number;
  name: string;
}

import nativeUser from 'libnativeuser.so';
const u: NativeUser = nativeUser.getCurrent();
```

For dynamic JS modules loaded via `import()`, type the imported namespace explicitly with `ESModule`-compatible declarations rather than dumping into an `ESObject` variable.

## Notes

- Do not use `ESObject` to silence other ArkTS errors - it shifts the failure point but does not fix the design.
- If the native side genuinely returns a free-form value, parse it through a typed adapter.

## See Also

- `assets/ESObjectTypeError.ets`
