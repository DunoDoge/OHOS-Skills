// TitleButtonRectTypeError.ets - TitleButtonRect has only width/height
import { window } from '@kit.ArkUI';

// BAD: wrong return type, accessing left/top
// const r: window.Rect = win.getTitleButtonRect();
// const x = r.left; // does not exist on TitleButtonRect

// GOOD
export function readTitleButtonSize(win: window.Window): string {
  const rect: window.TitleButtonRect = win.getTitleButtonRect();
  return `${rect.width}x${rect.height}`;
}

// For full window geometry, use windowRect (window.Rect with left/top)
export function readWindowGeometry(win: window.Window): string {
  const r: window.Rect = win.getWindowProperties().windowRect;
  return `(${r.left},${r.top}) ${r.width}x${r.height}`;
}
