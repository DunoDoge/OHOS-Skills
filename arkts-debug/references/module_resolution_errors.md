# Module Resolution Errors

## Symptom

```
Cannot find module 'XXX' or its corresponding type declarations.
Module 'xxx' has no exported member 'yyy'.
```

## Root Cause

These errors occur when the ArkTS compiler cannot resolve an import statement. Common causes include:

1. **Missing dependency**: The package is not listed in `oh-package.json5` or not installed via `ohpm install`.
2. **Incorrect import path**: The relative path does not point to an existing file.
3. **Case sensitivity mismatch**: When `caseSensitiveCheck` is enabled in `build-profile.json5`, the import path must match the actual file name's case exactly. Importing a folder that only contains `Index.ets` (capital I) will fail if the import expects `index.ets` (lowercase i).
4. **Missing index file**: Importing a directory requires an `index.ets` or `index.ts` (lowercase i) file in that directory.

## Canonical Fix

**For missing dependencies**, ensure the package is installed:

```bash
ohpm install @kit/<kit-name>
```

Check `oh-package.json5` for the correct dependency entry.

**For incorrect import paths**, verify the relative path:

```ts
// BAD: wrong path
// import { Utils } from './util/helper';

// GOOD: correct path
import { Utils } from './utils/helper';
```

**For case sensitivity issues**, match the exact file name:

```ts
// BAD: case mismatch (actual file is Helper.ets)
// import { Helper } from './helper';

// GOOD: exact case match
import { Helper } from './Helper';
```

**For missing index files**, either import the specific file or add an `index.ets`:

```ts
// Instead of importing a folder:
// import { Utils } from './utils';

// Import the specific file:
import { Utils } from './utils/Utils';
```

## Notes

- Run `ohpm install` after adding new dependencies to `oh-package.json5`.
- The `caseSensitiveCheck` option in `build-profile.json5` defaults to `false` on some platforms but may be `true` in CI environments.
- Reference: [Huawei FAQ - Cannot find module](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-hvigor-faqs)

## See Also

- `assets/ModuleResolutionError.ets`
