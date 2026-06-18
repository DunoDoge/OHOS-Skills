# Unused Variable Warnings

## Symptom

```
'foo' is declared but its value is never read.
arkts-no-unused-vars (in strict configurations)
```

## Root Cause

ArkTS / hvigor's strict mode flags unused locals, parameters, and imports. Beyond hygiene, an unused variable often signals an incomplete refactor.

## Canonical Fix

- If you actually need the variable for a side effect or future use, **use** it - log it via `hilog` or `console.info`, or pass it through.
- Otherwise, **delete** it.
- For unused parameters in callbacks, prefix with `_`:

```ts
list.map((_item, index) => index);
```

For unused imports: remove them; do not keep them "for documentation".

## Notes

- Underscore-prefix is the standard "intentionally unused" marker accepted by lint.
- Test scaffolds: keep imports inside the test file even if visually unused, as long as they have side effects (e.g. registering matchers).

## See Also

- `assets/UnusedVariableWarning.ets`
