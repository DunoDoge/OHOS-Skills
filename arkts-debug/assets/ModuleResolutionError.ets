// ModuleResolutionError.ets - correct import paths and module references
// NOTE: This file demonstrates import patterns. In a real project,
// the imported modules must exist in the corresponding paths.

// BAD: incorrect import path
// import { Utils } from './util/helper';     // wrong directory name

// BAD: case mismatch (actual file is Helper.ets)
// import { Helper } from './helper';         // lowercase vs actual uppercase

// BAD: importing folder without index.ets
// import { Utils } from './utils';           // no index.ets in folder

// GOOD: import from specific file with correct path and case
// import { Utils } from './utils/Helper';

// GOOD: import from @kit packages
import { common } from '@kit.AbilityKit';

// GOOD: import from ohpm packages (ensure oh-package.json5 has the dependency)
// import { SomeLib } from '@ohos/some-lib';

export function getContext(): common.UIAbilityContext | null {
  return null;
}
