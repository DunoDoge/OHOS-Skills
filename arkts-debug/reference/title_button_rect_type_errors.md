# TitleButtonRect Type Errors

## Symptom

```
Property 'left' does not exist on type 'TitleButtonRect'.
Property 'top' does not exist on type 'TitleButtonRect'.
Type 'TitleButtonRect' is not assignable to type 'window.Rect'.
```

Or:

```ts
const rect: window.Rect = win.getTitleButtonRect(); // wrong return type
```

## Root Cause

`window.Window.getTitleButtonRect()` returns `window.TitleButtonRect`, **not** `window.Rect`. `TitleButtonRect` has only `width` and `height` (plus `right`, depending on API version) - it does **not** have `left` and `top`.

## Canonical Fix

Use the right return type and only access existing fields:

```ts
const rect: window.TitleButtonRect = win.getTitleButtonRect();
const w: number = rect.width;
const h: number = rect.height;
```

If you need an absolute position, compute it from window dimensions and the layout direction; do not reach for non-existent `left`/`top`.

## Notes

- `getWindowProperties().windowRect` returns `window.Rect` and **does** have `left`/`top`/`width`/`height`. Use that for full-window geometry.

## See Also

- `assets/TitleButtonRectTypeError.ets`
- `reference/window_rect_size_errors.md`
