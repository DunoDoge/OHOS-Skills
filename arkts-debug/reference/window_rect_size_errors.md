# Window Rect/Size Type Errors

## Symptom

```
Type '{ x: number, y: number, width: number, height: number }' is not assignable to type 'window.Rect'.
Property 'left' is missing in type ... but required in type 'window.Rect'.
```

Or accessing DOM-style fields like `rect.x`, `rect.right`, `rect.bottom` on a `window.Rect`.

## Root Cause

`window.Rect` uses `{ left, top, width, height }`. `window.Size` uses `{ width, height }`. The DOM `DOMRect` shape (`x, y, right, bottom`) does **not** apply.

## Canonical Fix

Always construct and consume rects with the correct shape:

```ts
const rect: window.Rect = { left: 0, top: 0, width: 1080, height: 1920 };
const size: window.Size = { width: 1080, height: 1920 };

const right: number = rect.left + rect.width;
const bottom: number = rect.top + rect.height;
```

When reading from the system:

```ts
const props = win.getWindowProperties();
const r: window.Rect = props.windowRect; // has left/top/width/height
```

## Notes

- `getTitleButtonRect()` is special - see `title_button_rect_type_errors.md`.
- For `display.Rect` (in `@kit.ArkUI` display module), confirm the field names; some display APIs use `{ left, top, width, height }`, others `{ x, y, width, height }`. Read the d.ts before assigning.

## See Also

- `assets/WindowRectSizeError.ets`
- `reference/title_button_rect_type_errors.md`
