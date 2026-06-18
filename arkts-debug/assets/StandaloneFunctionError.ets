// StandaloneFunctionError.ets - pass context as parameter
import { common } from '@kit.AbilityKit';

// BAD: 'this' in standalone function
// function refresh() {
//   this.context.eventHub.emit('refresh');
// }

// GOOD: receive context explicitly
export function refresh(context: common.UIAbilityContext): void {
  context.eventHub.emit('refresh');
}

// GOOD: methods on a class can use `this`
class Refresher {
  private context: common.UIAbilityContext;
  constructor(context: common.UIAbilityContext) {
    this.context = context;
  }
  refresh(): void {
    this.context.eventHub.emit('refresh');
  }
}

export { Refresher };
