# Standalone Function `this` Errors

## Symptom

```
'this' is not allowed in standalone functions.
arkts-no-standalone-functions-this
```

Triggered by:

```ts
function refresh() {
  this.context.requestRefresh(); // 'this' undefined here
}
```

## Root Cause

ArkTS forbids `this` inside top-level `function` declarations. Unlike TS, there is no implicit dynamic `this` binding for standalone functions; the rule prevents brittle runtime behavior.

## Canonical Fix

Pass the dependency you need as a parameter:

```ts
import { common } from '@kit.AbilityKit';

function refresh(context: common.UIAbilityContext): void {
  context.eventHub.emit('refresh');
}
```

If the function is conceptually a method, move it onto a class or component:

```ts
@Component
struct Page {
  private refresh = (): void => { /* this.* is OK here */ };
}
```

## Notes

- Arrow functions defined as fields on a class still see the surrounding `this`.
- For shared utilities, prefer pure functions that take their inputs explicitly.

## See Also

- `assets/StandaloneFunctionError.ets`
