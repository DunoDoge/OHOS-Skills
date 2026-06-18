# AppStorage Type Errors

## Symptom

```
Type 'undefined' is not assignable to type 'T'.
Object is possibly 'undefined'.
arkts-no-any-unknown
```

Caused by:

```ts
const user = AppStorage.get<User>('user'); // user: User | undefined
console.log(user.name); // error: possibly undefined
```

Or by `AppStorage.setOrCreate` losing type info.

## Root Cause

`AppStorage.get<T>(key)` returns `T | undefined`. Strict ArkTS forbids accessing properties without a null/undefined guard, and forbids `any`/`unknown` fallbacks.

## Canonical Fix

Prefer reactive bindings over manual `get`:

```ts
@Component
struct Profile {
  @StorageLink('user') user: User = new User();
  build() { Text(this.user.name) }
}
```

For non-component code, use `AppStorage.setAndLink` to obtain a typed `SubscribedAbstractProperty`:

```ts
const link: SubscribedAbstractProperty<User> = AppStorage.setAndLink<User>('user', new User());
const u: User = link.get();
```

If you must use `get`, narrow with a guard:

```ts
const user: User | undefined = AppStorage.get<User>('user');
if (user !== undefined) {
  console.info(user.name);
}
```

## Notes

- Avoid `AppStorage.setOrCreate` when a typed default value is available - it does not enforce the type as strictly as `setAndLink`.
- Do not store untyped object literals; pre-declare with a `class` so the value carries a nominal type.

## See Also

- `assets/AppStorageError.ets`
