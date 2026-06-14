// WindowTypeError.ets - prefer callback form for getLastWindow
import { window } from '@kit.ArkUI';
import { common } from '@kit.AbilityKit';
import { BusinessError } from '@kit.BasicServicesKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG: string = 'WindowDemo';

// BAD (TS-style; ArkTS picks ambiguous overload, win is mistyped)
// const win = await window.getLastWindow(context);
// win.setWindowSystemBarEnable(['status']);

// GOOD: callback form
export function setupWindow(context: common.UIAbilityContext): void {
  window.getLastWindow(context, (err: BusinessError, win: window.Window) => {
    if (err.code !== 0) {
      hilog.error(0x0000, TAG, 'getLastWindow failed: %{public}s', JSON.stringify(err));
      return;
    }
    win.setWindowSystemBarEnable(['status', 'navigation']);
  });
}

// GOOD: promise form with explicit annotation
export async function setupWindowAsync(context: common.UIAbilityContext): Promise<void> {
  const win: window.Window = await window.getLastWindow(context);
  await win.setWindowSystemBarEnable(['status', 'navigation']);
}
