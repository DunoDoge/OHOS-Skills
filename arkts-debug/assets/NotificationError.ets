// NotificationError.ets - ContentType cast required
import { notificationManager } from '@kit.NotificationKit';
import { BusinessError } from '@kit.BasicServicesKit';

// BAD: ContentType enum is rejected where `number` is expected
// const badContent: notificationManager.NotificationContent = {
//   contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT, // error
//   normal: { title: 't', text: 'b', additionalText: '' }
// };

// GOOD: cast to number
function buildRequest(): notificationManager.NotificationRequest {
  const content: notificationManager.NotificationContent = {
    contentType: notificationManager.ContentType.NOTIFICATION_CONTENT_BASIC_TEXT as number,
    normal: { title: 'Title', text: 'Body', additionalText: '' }
  };
  const request: notificationManager.NotificationRequest = {
    id: 1,
    content: content
  };
  return request;
}

export function publishHello(): void {
  notificationManager.publish(buildRequest()).then((): void => {
    console.info('published');
  }).catch((err: BusinessError): void => {
    console.error(`publish failed code=${err.code} msg=${err.message}`);
  });
}
