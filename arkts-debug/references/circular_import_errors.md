# Circular Import Errors

## Symptom

```
Could not load ${file1} (imported by ${file2}): Maximum call stack size exceeded
```

## Root Cause

Circular imports occur when two or more modules import each other, forming a dependency cycle (e.g., A imports B, and B imports A). ArkTS's module system does not support circular dependencies — the module loader cannot resolve the initialization order, leading to a stack overflow during module loading.

This commonly happens when:
- Two utility modules reference each other's types
- A model module imports a service that also imports the model
- Shared constants are split across files that cross-reference each other

## Canonical Fix

Extract shared types and constants into a separate module that both importing modules depend on, breaking the cycle:

```ts
// shared/types.ets (new file — no imports from A or B)
export interface User {
  id: number;
  name: string;
}

// moduleA.ets
import { User } from './shared/types';
export function processUser(u: User): string { return u.name; }

// moduleB.ets
import { User } from './shared/types';
export function formatUser(u: User): string { return `User: ${u.name}`; }
```

If only types are needed across modules, consider using `import type` to make the dependency type-only (though ArkTS still discourages circular imports even for types).

## Notes

- Circular imports are a design issue, not a syntax error. The fix requires restructuring module boundaries.
- The error message may reference different files in the cycle than the ones you expect — trace the full import chain.
- In large projects, use a dependency graph tool to detect cycles early.
- Reference: [Huawei FAQ - Maximum call stack size exceeded](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-hvigor-faqs)

## See Also

- `assets/CircularImportError.ets`
