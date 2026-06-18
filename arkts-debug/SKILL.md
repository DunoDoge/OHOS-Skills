---
name: arkts-debug
description: Use when fixing ArkTS / .ets compilation errors and type mismatches in HarmonyOS / OpenHarmony app development. Triggers include errors mentioning ContentType, AppStorage.get, @StorageLink, getLastWindow, AvoidArea, TitleButtonRect, IDataSource, ESObject, LazyForEach, duplicate @Entry, "Object literal must correspond to some explicitly declared class or interface", "Possibly null", "Standalone function uses this", "Indexed access is not supported", arkts-no-props-by-index, "Declaration merging is not supported", arkts-no-decl-merging, "Cannot find module", "Maximum call stack", "inferred type cannot be named", or any arkts-no-* rule reported by hvigor / ArkCompiler. Loads a curated catalog of common HarmonyOS build errors and their canonical fixes.
---

# Harmony Error Fixes

This skill provides solutions for common ArkTS compilation errors and type mismatches encountered during HarmonyOS / OpenHarmony development. Each entry has a focused reference document under `references/` and a minimal `.ets` example under `assets/`.

## When to use this skill

Activate this skill whenever **any** of the following holds:

- The user pastes an ArkTS / `.ets` compile error from DevEco Studio, hvigor, or ArkCompiler.
- The error contains rule codes from the `arkts-no-*` family, or mentions any of: `ContentType`, `AppStorage.get`, `@StorageLink`, `getLastWindow`, `AvoidArea`, `TitleButtonRect`, `IDataSource`, `ESObject`, `LazyForEach`, duplicate `@Entry`, "Possibly 'null'", "Object literal must correspond to some explicitly declared class or interface", "Standalone function ... uses `this`", "Indexed access is not supported", `arkts-no-props-by-index`, "Declaration merging is not supported", `arkts-no-decl-merging`, "Cannot find module", "Maximum call stack", "inferred type cannot be named".
- The user asks how to fix a HarmonyOS build failure or strict ArkTS type error.
- You are reviewing `.ets` code and want to pre-empt the most common compile errors.

If the task is general ArkTS authoring / migration / style (not a concrete error to fix), prefer `arkts-helper` instead. Use both together when the user is migrating TS to ArkTS and hits compile errors.

## Workflow (follow strictly)

### 1. Identify the error category

Read the user's error message and map it to one row in the **Error Categories** table below. The mapping is based on the diagnostic text or the API/decorator that triggered it. If the error does not match any row, fall back to `arkts-helper/references/05-typescript-to-arkts-migration-guide.md` for the underlying `arkts-no-*` rule.

### 2. Open the matching reference + asset

For each category there are two files:

- `references/<topic>.md` - root cause, canonical fix, edge-case notes.
- `assets/<Topic>.ets` - minimal **before / after** code that compiles cleanly.

Read **both** for the matched category before editing the user's code. Do not skim only the Quick Reference table.

### 3. Apply the canonical fix

Apply the fix exactly as documented. Do **not** silence errors with `as any`, `// @ts-ignore`, `ESObject`, or by deleting type annotations - these patterns are themselves flagged by ArkTS strict mode and will resurface elsewhere.

If the user's code has multiple errors, fix them one category at a time and re-check the build before moving on; one fix often unblocks or reshapes the next error.

### 4. Cite the reference

When you reply, cite the specific reference file you used, e.g.:

> Fix per `arkts-debug/references/possibly_null_errors.md`.

## Error Categories

| Category | Description |
|----------|-------------|
| Notification API Type Errors | `ContentType` type incompatibility |
| Window API Type Errors | Type inference issues with `window.getLastWindow` |
| AppStorage Type Errors | Type inference errors with `AppStorage.get()` |
| Object Spread Type Errors | Type inference issues with object spread |
| @StorageLink Default Value Errors | Missing default values for `@StorageLink` properties |
| Object Literal Interface Errors | Object literals without explicit interfaces |
| Object Literal Type Errors | Using object literal types in return type annotations |
| Function Return Type Errors | Limited return type inference |
| Arrow Function Conversion Errors | Using function expressions instead of arrow functions |
| Color Property Errors | Non-existent `Color` properties |
| Interface Method Signature Errors | Method signature mismatches in object literals |
| AvoidArea Type Errors | Missing `visible` property in `AvoidArea` type |
| Standalone Function `this` Errors | Using `this` in standalone functions |
| TitleButtonRect Type Errors | Incorrect return type for `getTitleButtonRect`; non-existent `left`/`top` |
| Catch Clause Type Errors | Type annotations in `catch` clauses |
| ESObject Type Errors | Restricted usage of `ESObject` type |
| Resource Conversion Errors | `Resource` to string/number conversion errors |
| Unused Variable Warnings | Declared but never used variables |
| IDataSource Type Errors | `LazyForEach` requires `IDataSource` implementation |
| Duplicate Entry Errors | Multiple `@Entry` decorators in the same file |
| Possibly Null Errors | Object possibly null when accessing properties |
| Window Rect/Size Type Errors | `window.Rect` / `window.Size` shape mismatch |
| Indexed Access Errors | `arkts-no-props-by-index` — bracket notation property access |
| Declaration Merging Errors | `arkts-no-decl-merging` — duplicate declarations or namespace merging |
| Inferred Type Naming Errors | Exported symbol's inferred type cannot be named without internal reference |
| Array Type Inference Errors | Missing element type in array declarations (e.g., `[][]`) |
| Module Resolution Errors | Cannot find module or no exported member |
| Circular Import Errors | Circular module dependencies causing stack overflow |

## Quick Reference

| Error Type | Solution |
|------------|----------|
| Notification type error | Cast to `number` type |
| Window type error | Use callback pattern for `getLastWindow` |
| AppStorage type error | Use `@StorageLink` with `LocalStorage` or `AppStorage.setAndLink` (avoid `setOrCreate`) |
| Object spread error | Explicitly type objects |
| @StorageLink default value error | Add `= undefined` or a specific default value |
| Object literal interface error | Define an interface before using the object literal |
| Object literal type error | Define an interface and use it as the return type |
| Function return type error | Add explicit return type annotation |
| Arrow function conversion error | Convert `function` to arrow function `=>` |
| Color property error | Use hex color values instead of non-existent Color properties |
| Interface method signature error | Use property syntax `method: () => {}` instead of method syntax |
| AvoidArea type error | Add `visible: false` property to `AvoidArea` object |
| Standalone function `this` error | Pass context as parameter: `function foo(context: Context)` |
| TitleButtonRect type error | Use `window.TitleButtonRect`; only `width`/`height` are available |
| Catch clause type error | Remove type annotation from the catch parameter |
| ESObject type error | Use a concrete type or `ESModule` instead of `ESObject` |
| Resource conversion error | Use `Resource` directly in UI or `ResourceManager` for runtime values |
| Unused variable warning | Use the value or delete the declaration |
| IDataSource type error | Implement `IDataSource` for `LazyForEach` |
| Duplicate Entry error | Remove extra `@Entry`; use `@Component` for child components |
| Possibly Null error | Add `!== null` check or use optional chaining |
| Window Rect/Size type error | Use the correct `window.Rect` / `window.Size` shape |
| Indexed access error | Use dot notation or `Map` instead of bracket notation |
| Declaration merging error | Consolidate into a single declaration or use `extends` |
| Inferred type naming error | Add explicit return type annotation to exported symbols |
| Array type inference error | Specify explicit element type (e.g., `string[][]` instead of `[][]`) |
| Module resolution error | Check `oh-package.json5`, import path, and case sensitivity |
| Circular import error | Extract shared types into a separate module |

## Detailed Error Solutions

### Notification API Type Errors
- [Notification Type Error](./references/notification_errors.md)
- [Code Example](./assets/NotificationError.ets)

### Window API Type Errors
- [Window Type Inference Error](./references/window_type_errors.md)
- [Code Example](./assets/WindowTypeError.ets)

### AppStorage Type Errors
- [AppStorage Type Error](./references/appstorage_errors.md)
- [Code Example](./assets/AppStorageError.ets)

### Object Spread Type Errors
- [Object Spread Type Error](./references/object_spread_errors.md)
- [Code Example](./assets/ObjectSpreadError.ets)

### @StorageLink Default Value Errors
- [@StorageLink Default Value Error](./references/storage_link_default_errors.md)
- [Code Example](./assets/StorageLinkDefaultError.ets)

### Object Literal Interface Errors
- [Object Literal Interface Error](./references/object_literal_interface_errors.md)
- [Code Example](./assets/ObjectLiteralInterfaceError.ets)

### Object Literal Type Errors
- [Object Literal Type Error](./references/object_literal_type_errors.md)
- [Code Example](./assets/ObjectLiteralTypeError.ets)

### Function Return Type Errors
- [Function Return Type Error](./references/function_return_type_errors.md)
- [Code Example](./assets/FunctionReturnTypeError.ets)

### Arrow Function Conversion Errors
- [Arrow Function Conversion Error](./references/arrow_function_conversion_errors.md)
- [Code Example](./assets/ArrowFunctionConversionError.ets)

### Color Property Errors
- [Color Property Error](./references/color_property_errors.md)
- [Code Example](./assets/ColorPropertyError.ets)

### Interface Method Signature Errors
- [Interface Method Signature Error](./references/interface_method_signature_errors.md)
- [Code Example](./assets/InterfaceMethodSignatureError.ets)

### AvoidArea Type Errors
- [AvoidArea Type Error](./references/avoid_area_type_errors.md)
- [Code Example](./assets/AvoidAreaTypeError.ets)

### Standalone Function `this` Errors
- [Standalone Function `this` Error](./references/standalone_function_errors.md)
- [Code Example](./assets/StandaloneFunctionError.ets)

### TitleButtonRect Type Errors
- [TitleButtonRect Type Error](./references/title_button_rect_type_errors.md)
- [Code Example](./assets/TitleButtonRectTypeError.ets)

### Catch Clause Type Errors
- [Catch Clause Type Error](./references/catch_clause_type_errors.md)
- [Code Example](./assets/CatchClauseTypeError.ets)

### ESObject Type Errors
- [ESObject Type Error](./references/esobject_type_errors.md)
- [Code Example](./assets/ESObjectTypeError.ets)

### Resource Conversion Errors
- [Resource Conversion Error](./references/resource_conversion_errors.md)
- [Code Example](./assets/ResourceConversionError.ets)

### Unused Variable Warnings
- [Unused Variable Warning](./references/unused_variable_warnings.md)
- [Code Example](./assets/UnusedVariableWarning.ets)

### IDataSource Type Errors
- [IDataSource Type Error](./references/idata_source_errors.md)
- [Code Example](./assets/IDataSourceError.ets)

### Duplicate Entry Errors
- [Duplicate Entry Error](./references/duplicate_entry_errors.md)
- [Code Example](./assets/DuplicateEntryError.ets)

### Possibly Null Errors
- [Possibly Null Error](./references/possibly_null_errors.md)
- [Code Example](./assets/PossiblyNullError.ets)

### Window Rect/Size Type Errors
- [Window Rect/Size Type Error](./references/window_rect_size_errors.md)
- [Code Example](./assets/WindowRectSizeError.ets)

### Indexed Access Errors
- [Indexed Access Error](./references/indexed_access_errors.md)
- [Code Example](./assets/IndexedAccessError.ets)

### Declaration Merging Errors
- [Declaration Merging Error](./references/decl_merging_errors.md)
- [Code Example](./assets/DeclMergingError.ets)

### Inferred Type Naming Errors
- [Inferred Type Naming Error](./references/inferred_type_naming_errors.md)
- [Code Example](./assets/InferredTypeNamingError.ets)

### Array Type Inference Errors
- [Array Type Inference Error](./references/array_type_inference_errors.md)
- [Code Example](./assets/ArrayTypeInferenceError.ets)

### Module Resolution Errors
- [Module Resolution Error](./references/module_resolution_errors.md)
- [Code Example](./assets/ModuleResolutionError.ets)

### Circular Import Errors
- [Circular Import Error](./references/circular_import_errors.md)
- [Code Example](./assets/CircularImportError.ets)
