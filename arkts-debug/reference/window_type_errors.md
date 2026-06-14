# Window API Type Inference Errors

## Symptom

```
Type 'Promise<window.Window>' is missing the following properties from type 'window.Window': ...
'await' has no effect on the type of this expression.
```

Or, when chaining off the promise, the methods on `window.Window` are not found because TypeScript inferred the variable as the un-awaited promise.

## Root Cause

`window.getLastWindow(context)` is overloaded. ArkTS picks the **callback** signature when no explicit type annotation is given, leaving `await` returning the wrong type. Also, the promise overload's resolution may be ambiguous in strict ArkTS.

## Canonical Fix

Use the explicit **callback** form, which is unambiguous and avoids the inference trap:

```ts
window.getLastWindow(context, (err, win: window.Window) => {
  if (err.code) {
    hilog.error(0x0000, 'tag', 'getLastWindow failed: %{public}s', JSON.stringify(err));
    return;
  }
  win.setWindowSystemBarEnable(['status', 'navigation']);
});
```

If you must use the promise form, annotate the variable:

```ts
const win: window.Window = await window.getLastWindow(context);
```

## Notes

- Same pattern applies to `window.findWindow` and `window.create`.
- Wrap the callback body in `try/catch` if it calls APIs that throw.

## See Also

- `assets/WindowTypeError.ets`
