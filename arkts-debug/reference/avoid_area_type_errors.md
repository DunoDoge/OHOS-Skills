# AvoidArea Type Errors

## Symptom

```
Property 'visible' is missing in type '{ topRect: ...; ... }' but required in type 'AvoidArea'.
```

When constructing a default `window.AvoidArea` literal:

```ts
const area: window.AvoidArea = {
  topRect: { left: 0, top: 0, width: 0, height: 0 },
  leftRect: { left: 0, top: 0, width: 0, height: 0 },
  rightRect: { left: 0, top: 0, width: 0, height: 0 },
  bottomRect: { left: 0, top: 0, width: 0, height: 0 }
}; // missing `visible`
```

## Root Cause

`window.AvoidArea` declares a required `visible: boolean` field. It is easy to forget when copying older snippets that omit it.

## Canonical Fix

Always include `visible`:

```ts
const empty: window.AvoidArea = {
  visible: false,
  topRect: { left: 0, top: 0, width: 0, height: 0 },
  leftRect: { left: 0, top: 0, width: 0, height: 0 },
  rightRect: { left: 0, top: 0, width: 0, height: 0 },
  bottomRect: { left: 0, top: 0, width: 0, height: 0 }
};
```

## Notes

- `visible: true` means the system bar is currently shown; default to `false` for placeholder values.
- Each `Rect` here is `window.Rect` (`left/top/width/height`), not DOMRect.

## See Also

- `assets/AvoidAreaTypeError.ets`
- `reference/window_rect_size_errors.md`
