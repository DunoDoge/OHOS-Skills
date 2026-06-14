# Object Literal Interface Errors

## Symptom

```
arkts-no-untyped-obj-literals
Object literal must correspond to some explicitly declared class or interface.
```

## Root Cause

ArkTS forbids "shape-only" object literals. Every literal must be assignable to a previously declared `interface` or `class`. There is no structural typing inferred from the literal itself.

## Canonical Fix

Declare the shape first, then construct with that type as context:

```ts
interface UserCard {
  id: number;
  name: string;
  avatar: ResourceStr;
}

const card: UserCard = { id: 1, name: 'Alice', avatar: $r('app.media.avatar') };
```

When passing inline, the parameter type already provides context:

```ts
function render(card: UserCard) {}
render({ id: 1, name: 'Alice', avatar: $r('app.media.avatar') }); // OK
```

## Notes

- Use `interface` for plain data, `class` when you need methods or default initializers.
- Do not rely on TS index signatures (`{ [k: string]: any }`) - they are restricted.

## See Also

- `assets/ObjectLiteralInterfaceError.ets`
