# @StorageLink Default Value Errors

## Symptom

```
Property '...' has no initializer and is not definitely assigned in the constructor.
@StorageLink decorated property must have a default value.
```

## Root Cause

ArkTS components require every state-bound property to have a default value. Unlike TS class fields, you cannot leave a `@StorageLink` undefined hoping `AppStorage` fills it in. The compiler enforces an initializer at the declaration site.

## Canonical Fix

Always provide a default that matches the declared type:

```ts
@Component
struct Demo {
  @StorageLink('count') count: number = 0;
  @StorageLink('user') user: User = new User();
  @StorageLink('maybe') maybe: string | undefined = undefined;
  build() {}
}
```

If the underlying value is genuinely optional, type it as `T | undefined` and default to `undefined` (the explicit `= undefined` is required, not implied).

## Notes

- Same rule applies to `@LocalStorageLink`, `@StorageProp`, `@LocalStorageProp`, `@State`, `@Prop`, `@Link` (with the exception of `@Link`/`@Consume` which derive from parent).
- Do not use a placeholder cast like `null as User` to dodge the rule.

## See Also

- `assets/StorageLinkDefaultError.ets`
