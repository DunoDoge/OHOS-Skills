# Arrow Function Conversion Errors

## Symptom

```
arkts-no-standalone-functions (variant)
Type '() => void' is not assignable to parameter expecting an arrow callback.
'this' is not allowed in standalone functions.
```

Or the IDE quick-fix prompts: "Convert function expression to arrow function".

## Root Cause

In ArkUI event handlers and most callback APIs, the parameter type is an **arrow function** (e.g. `() => void`). A `function () { ... }` expression is not the same type in ArkTS - it brings its own dynamic `this` and is rejected by stricter rules. Arrow functions also capture the surrounding `this`, which is what UI handlers need.

## Canonical Fix

Replace `function` expressions with arrow functions:

```ts
// Bad
Button('Tap').onClick(function () { this.count++; });

// Good
Button('Tap').onClick(() => { this.count++; });
```

For named helpers, prefer `const fn = (): void => { ... }` or methods on the component.

## Notes

- Do not use `.bind(this)` to work around it - arrow functions are the idiomatic fix.
- Top-level `function foo()` declarations are allowed; the issue is specifically with **function expressions used where an arrow type is expected**.

## See Also

- `assets/ArrowFunctionConversionError.ets`
