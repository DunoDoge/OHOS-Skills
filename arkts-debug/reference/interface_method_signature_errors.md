# Interface Method Signature Errors

## Symptom

```
Type '(x: number) => void' is not assignable to type '(x: number) => void'.
Method 'foo' in object literal does not match the signature of property 'foo' in interface 'I'.
```

The two signatures look identical, but ArkTS distinguishes **method-style** (`foo(x: number): void`) from **property-style** (`foo: (x: number) => void`).

## Root Cause

In ArkTS, an interface declared with method syntax is **not** structurally compatible with an object literal that uses arrow-property syntax (and vice-versa). Pick one style and use it consistently.

## Canonical Fix

Prefer **property syntax with arrow types** in interfaces - it composes well with arrow callbacks and avoids `this` ambiguity:

```ts
interface Handlers {
  onLoad: (id: number) => void;
  onError: (err: Error) => void;
}

const h: Handlers = {
  onLoad: (id: number) => { console.info(`${id}`); },
  onError: (err: Error) => { console.error(err.message); }
};
```

## Notes

- Method syntax is fine for **classes**, where `this` binding is well-defined.
- When porting TS code, change the interface definition rather than every call site.

## See Also

- `assets/InterfaceMethodSignatureError.ets`
