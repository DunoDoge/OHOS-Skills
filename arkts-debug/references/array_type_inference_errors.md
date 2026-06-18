# Array Type Inference Errors

## Symptom

```
Cannot read properties of undefined (reading 'XXX')
```

This error can appear at runtime when an array is declared with an empty element type, causing the compiler to infer `undefined` as the element type.

Triggered by:

```ts
class MyClass {
  public a: [][] = [];  // missing inner element type
}
```

## Root Cause

ArkTS requires all array declarations to specify a concrete element type. When you write `[][]` (array of arrays with no element type), the compiler cannot determine what the inner arrays contain. This leads to undefined behavior at runtime when accessing elements, because the type system has no information about the array's contents.

## Canonical Fix

Always specify the full element type, including the inner type for nested arrays:

```ts
class MyClass {
  public a: string[][] = [];  // explicit inner element type
}
```

For single-dimensional arrays:

```ts
const names: string[] = [];    // not: names: [] = []
const counts: number[] = [];   // not: counts: [] = []
```

## Notes

- This is a common mistake when migrating from TypeScript where `any[]` is the default fallback — ArkTS does not allow `any`.
- The error message "Cannot read properties of undefined" can be misleading; always check array type declarations when it occurs on array access.
- Reference: [Huawei FAQ - "Cannot read properties of undefined(reading 'kind')"](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-hvigor-faqs)

## See Also

- `assets/ArrayTypeInferenceError.ets`
