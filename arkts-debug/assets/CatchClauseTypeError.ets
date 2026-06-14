// CatchClauseTypeError.ets - no type annotation on catch parameter
import { BusinessError } from '@kit.BasicServicesKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG: string = 'CatchDemo';

function risky(): void {
  throw new Error('boom');
}

// BAD: catch (e: Error) is not allowed
// try { risky(); } catch (e: Error) { ... }

// GOOD: no annotation; cast inside the block if needed
export function safe(): void {
  try {
    risky();
  } catch (e) {
    const err = e as BusinessError;
    hilog.error(0x0000, TAG, 'failed: code=%{public}d msg=%{public}s',
      err.code ?? -1, err.message ?? 'unknown');
  }
}
