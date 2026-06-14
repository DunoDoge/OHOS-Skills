# Object Spread Type Errors

## Symptom

```
Spread types may only be created from object types.
arkts-no-spread
Property '...' does not exist on type 'Object'.
```

Triggered by:

```ts
const merged = { ...a, ...b }; // a, b inferred as Object
```

## Root Cause

ArkTS does not allow spreading values whose static type is the unconstrained `Object`. The result type cannot be reliably synthesized, and structural typing is not used.

## Canonical Fix

Give every operand an explicit interface or class type, and write the merged result with the same type:

```ts
interface Point { x: number; y: number; }
const a: Point = { x: 1, y: 2 };
const b: Point = { x: 3, y: 4 };
const merged: Point = { x: b.x, y: b.y }; // explicit copy
```

If you genuinely need a partial-merge helper, write it as a typed function:

```ts
function mergePoint(a: Point, b: Partial<Point>): Point {
  return { x: b.x ?? a.x, y: b.y ?? a.y };
}
```

## Notes

- Array spread (`[...arr]`) is allowed when `arr` has a concrete element type.
- Do not silence with `as any` - prefer rewriting to explicit field copies.

## See Also

- `assets/ObjectSpreadError.ets`
