// WindowRectSizeError.ets - use {left, top, width, height} for window.Rect
import { window } from '@kit.ArkUI';

// BAD: DOM-style {x, y, right, bottom} does not match window.Rect
// const bad: window.Rect = { x: 0, y: 0, right: 100, bottom: 200 };

// GOOD: correct shape
export const fullRect: window.Rect = {
  left: 0,
  top: 0,
  width: 1080,
  height: 1920
};

export const fullSize: window.Size = {
  width: 1080,
  height: 1920
};

export function rightEdge(r: window.Rect): number {
  return r.left + r.width;
}

export function bottomEdge(r: window.Rect): number {
  return r.top + r.height;
}

// Reading from the system
export function readGeometry(win: window.Window): window.Rect {
  return win.getWindowProperties().windowRect;
}
