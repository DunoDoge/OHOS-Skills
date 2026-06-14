# Resource Conversion Errors

## Symptom

```
Type 'Resource' is not assignable to type 'string'.
Type 'Resource' is not assignable to type 'number'.
```

Triggered when assigning a `$r('...')` resource to a plain `string`/`number`, or concatenating it into a template literal.

## Root Cause

`$r(...)` and `$rawfile(...)` return a `Resource` object - a typed handle resolved by the framework, not the resolved value. Many UI props accept `ResourceStr = string | Resource`, so passing the `Resource` directly is fine. Assigning to `string` is not.

## Canonical Fix

For UI: pass the `Resource` straight through, and type intermediaries as `ResourceStr` (or `ResourceColor`, `ResourceNumber`, etc.):

```ts
@State title: ResourceStr = $r('app.string.page_title');

build() { Text(this.title) }
```

For runtime values (logging, network payloads), resolve through `ResourceManager`:

```ts
import { common } from '@kit.AbilityKit';

async function getTitle(context: common.UIAbilityContext): Promise<string> {
  return await context.resourceManager.getStringValue($r('app.string.page_title').id);
}
```

## Notes

- Never `String($r(...))` - it stringifies the handle, not the value.
- For numeric resources use `getNumberValue`; for media use `getMediaContent`.

## See Also

- `assets/ResourceConversionError.ets`
