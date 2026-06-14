# Possibly Null Errors

## Symptom

```
Object is possibly 'null'.
Object is possibly 'undefined'.
```

Triggered by accessing properties of values typed `T | null` or `T | undefined` without a guard.

## Root Cause

ArkTS uses strict null checks. Anything typed as nullable must be narrowed before property access, method call, or assignment to a non-nullable target. This applies to many platform APIs (e.g. `getContext()`, query selectors, `Map.get`).

## Canonical Fix

Use an explicit guard or optional chaining:

```ts
const ctx: Context | null = getContext();
if (ctx !== null) {
  ctx.eventHub.emit('ready');
}

// or
ctx?.eventHub.emit('ready');
```

For values you've already validated, narrow once into a `const`:

```ts
const ctx = getContext();
if (ctx === null) { return; }
ctx.eventHub.emit('ready'); // ctx is now Context
```

## Notes

- Avoid the non-null assertion `!.` unless you can prove the value is non-null at that point. Strict ArkTS configurations can disallow it.
- Default-using `??` is fine: `const name = user?.name ?? 'anon';`.

## See Also

- `assets/PossiblyNullError.ets`
