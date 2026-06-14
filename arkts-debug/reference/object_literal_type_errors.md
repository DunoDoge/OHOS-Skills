# Object Literal Type Errors

## Symptom

```
arkts-no-obj-literals-as-types
Object type literals are not allowed; use an interface or class instead.
```

Example:

```ts
function getInfo(): { name: string; age: number } { ... } // not allowed
```

## Root Cause

ArkTS bans inline object type literals (`{ a: number; b: string }`) in type positions: return types, parameter types, type aliases, generic arguments. Types must be **named**.

## Canonical Fix

Promote the inline type to an interface:

```ts
interface Info {
  name: string;
  age: number;
}

function getInfo(): Info {
  return { name: 'Alice', age: 30 };
}
```

## Notes

- This also applies to `Array<{ a: number }>` - replace with `Array<Info>`.
- Type aliases of object literals (`type T = { a: number }`) are also forbidden; use `interface T { a: number }`.

## See Also

- `assets/ObjectLiteralTypeError.ets`
