# Catch Clause Type Errors

## Symptom

```
arkts-no-types-in-catch-clause
Type annotation in 'catch' clause is not allowed.
```

Triggered by:

```ts
try { ... } catch (e: Error) { ... } // not allowed
```

## Root Cause

ArkTS mandates that the catch parameter has no type annotation; the runtime always provides an `Error` (or subtype). Annotating it - even with `any` or `unknown` - is rejected.

## Canonical Fix

Drop the annotation. The parameter is implicitly typed as a `BusinessError` / `Error`:

```ts
import { BusinessError } from '@kit.BasicServicesKit';

try {
  doWork();
} catch (e) {
  const err = e as BusinessError;
  hilog.error(0x0000, 'tag', 'failed: code=%{public}d msg=%{public}s', err.code, err.message);
}
```

If you need a narrower type, cast inside the block (`as BusinessError`).

## Notes

- Do not write `catch (e: any)` or `catch (e: unknown)` - both are flagged.
- For async code, the same rule applies to the variable inside `.catch((e) => ...)` callbacks.

## See Also

- `assets/CatchClauseTypeError.ets`
