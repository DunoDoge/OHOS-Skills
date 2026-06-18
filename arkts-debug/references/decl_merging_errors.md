# Declaration Merging Errors

## Symptom

```
Declaration merging is not supported (arkts-no-decl-merging)
Cannot redeclare block-scoped variable 'xxx'
```

Triggered by:

```ts
interface User { name: string; }
interface User { age: number; }  // arkts-no-decl-merging

namespace Utils {
  export function foo(): void {}
}
namespace Utils {
  export function bar(): void {}  // arkts-no-decl-merging
}
```

## Root Cause

ArkTS does not support declaration merging — the TypeScript feature where multiple declarations with the same name are automatically combined into a single type. This includes interface merging, namespace merging, and variable redeclaration. ArkTS requires each name to have exactly one declaration in its scope to ensure static type safety and predictable runtime behavior.

## Canonical Fix

Consolidate all members into a single declaration:

```ts
interface User {
  name: string;
  age: number;
}

namespace Utils {
  export function foo(): void {}
  export function bar(): void {}
}
```

If you need to extend an existing interface, use `extends`:

```ts
interface UserBase {
  name: string;
}

interface User extends UserBase {
  age: number;
}
```

## Notes

- This also applies to `enum` merging and class-function merging, which are likewise prohibited.
- Variable redeclaration (`let x = 1; let x = 2;`) is caught by the same rule.
- If you are augmenting a third-party type, create a new interface that `extends` the original rather than redeclaring it.

## See Also

- `assets/DeclMergingError.ets`
