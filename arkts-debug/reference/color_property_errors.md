# Color Property Errors

## Symptom

```
Property 'XXXX' does not exist on type 'typeof Color'.
```

For example `Color.LightBlue`, `Color.DarkGray`, `Color.Tomato` - none of these exist.

## Root Cause

The ArkUI `Color` enum exposes a small fixed palette: `White`, `Black`, `Blue`, `Brown`, `Gray`, `Green`, `Grey`, `Orange`, `Pink`, `Red`, `Yellow`, `Transparent`. CSS-style color names from the web are **not** present.

## Canonical Fix

Use a hex string (or rgb/rgba) for any color outside the enum:

```ts
Text('Hi').fontColor('#ADD8E6')        // light blue
Text('Hi').fontColor('rgba(255,0,0,0.5)')
```

Or define a constants module if the color is reused:

```ts
export class AppColor {
  static readonly LIGHT_BLUE: string = '#ADD8E6';
}
```

## Notes

- For theme-aware colors, prefer `$r('app.color.xxx')` Resource refs over raw hex.
- `Color.Grey` and `Color.Gray` both exist - be consistent across the codebase.

## See Also

- `assets/ColorPropertyError.ets`
