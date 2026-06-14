// AvoidAreaTypeError.ets - AvoidArea requires `visible`
import { window } from '@kit.ArkUI';

// BAD: missing `visible`
// const bad: window.AvoidArea = {
//   topRect: { left: 0, top: 0, width: 0, height: 0 },
//   leftRect: { left: 0, top: 0, width: 0, height: 0 },
//   rightRect: { left: 0, top: 0, width: 0, height: 0 },
//   bottomRect: { left: 0, top: 0, width: 0, height: 0 }
// };

// GOOD: include visible
export const empty: window.AvoidArea = {
  visible: false,
  topRect: { left: 0, top: 0, width: 0, height: 0 },
  leftRect: { left: 0, top: 0, width: 0, height: 0 },
  rightRect: { left: 0, top: 0, width: 0, height: 0 },
  bottomRect: { left: 0, top: 0, width: 0, height: 0 }
};
