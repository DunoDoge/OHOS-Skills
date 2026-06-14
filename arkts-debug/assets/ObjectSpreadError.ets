// ObjectSpreadError.ets - replace untyped spread with explicit copy
interface Point {
  x: number;
  y: number;
}

// BAD: spread of object with inferred type
// const a = { x: 1, y: 2 };
// const b = { x: 3, y: 4 };
// const merged = { ...a, ...b }; // arkts-no-spread

// GOOD: explicit type + explicit fields
const a: Point = { x: 1, y: 2 };
const b: Point = { x: 3, y: 4 };
const merged: Point = { x: b.x, y: b.y };

// GOOD: typed merge helper
function mergePoint(base: Point, patch: Partial<Point>): Point {
  return { x: patch.x ?? base.x, y: patch.y ?? base.y };
}

export const result: Point = mergePoint(a, { x: 10 });
