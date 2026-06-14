// UnusedVariableWarning.ets - remove or mark unused locals
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG: string = 'UnusedDemo';

// BAD: declared but never read
// function foo() {
//   const helper = 'tmp'; // 'helper' is declared but never read
//   return 1;
// }

// GOOD 1: actually use the value
export function foo(): number {
  const helper: string = 'tmp';
  hilog.info(0x0000, TAG, 'helper=%{public}s', helper);
  return 1;
}

// GOOD 2: prefix with _ for intentionally unused parameters
export function pickIndex<T>(list: T[]): number[] {
  return list.map((_item: T, index: number): number => index);
}
