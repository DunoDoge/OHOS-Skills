// ObjectLiteralTypeError.ets - inline object types are forbidden
// BAD: inline object type literal in return position
// function getInfo(): { name: string; age: number } { ... } // arkts-no-obj-literals-as-types

// GOOD
interface Info {
  name: string;
  age: number;
}

export function getInfo(): Info {
  return { name: 'Alice', age: 30 };
}

// BAD type alias of object literal
// type Pair = { a: number; b: number };

// GOOD
interface Pair {
  a: number;
  b: number;
}

export function makePair(): Pair {
  return { a: 1, b: 2 };
}
