# Duplicate Entry Errors

## Symptom

```
Only one '@Entry' decorator is allowed per file.
ArkTS:ERROR Multiple '@Entry' components found.
```

## Root Cause

`@Entry` marks the page-level root component. The framework loads exactly one per `.ets` file. Adding a second `@Entry` to a child / sub-component breaks routing.

## Canonical Fix

Keep `@Entry` only on the page root. Decorate child components with plain `@Component`:

```ts
@Entry
@Component
struct PageRoot {
  build() { Column() { ChildView() } }
}

@Component
struct ChildView {
  build() { Text('child') }
}
```

If two screens really do live in the same file, split them into two files - one `@Entry` per file.

## Notes

- `@Entry` accepts an optional `LocalStorage` parameter; child components do not.
- Router pages are registered via `main_pages.json` - each entry there points at one file.

## See Also

- `assets/DuplicateEntryError.ets`
