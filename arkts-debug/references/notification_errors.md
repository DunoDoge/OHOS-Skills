# Notification API Type Errors

## Symptom

```
Type 'notificationManager.ContentType' is not assignable to type 'number'.
Argument of type 'ContentType' is not assignable to parameter of type 'number'.
```

Triggered when calling `notificationManager.publish()` with a `NotificationRequest` whose `content.contentType` is set to one of the `notificationManager.ContentType.NOTIFICATION_CONTENT_*` enum values. ArkTS treats the API parameter as `number`, not as the enum, so the assignment is rejected.

## Root Cause

In ArkTS the underlying `NotificationContent.contentType` field is typed `number`. ArkTS does not implicitly widen enum members to their numeric base type the way TypeScript does in some configurations.

## Canonical Fix

Cast the enum value to `number` at the assignment site:

```ts
const content: notificationManager.NotificationContent = {
  contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT as number,
  normal: { title: 'Title', text: 'Body', additionalText: '' }
};
```

## Notes

- Do **not** cast through `as any` - it will trip `arkts-no-any-unknown`.
- If you have many call sites, define a helper:
  ```ts
  function asContentType(v: notificationManager.ContentType): number { return v as number; }
  ```
- The same pattern applies to `SlotType` and other notification enums that hit the same `number` parameter typing.

## See Also

- `assets/NotificationError.ets`
