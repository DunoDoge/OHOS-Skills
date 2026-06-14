// ResourceConversionError.ets - keep Resource as Resource; resolve via ResourceManager when needed
import { common } from '@kit.AbilityKit';

// BAD: assigning Resource to string / interpolating into template
// const title: string = $r('app.string.page_title'); // type error
// const s: string = `title=${$r('app.string.page_title')}`; // stringifies handle, not value

// GOOD: pass through to UI props that accept ResourceStr
@Entry
@Component
struct ResDemo {
  @State title: ResourceStr = $r('app.string.page_title');
  build() {
    Column() {
      Text(this.title)
    }
  }
}

// GOOD: resolve to plain string at runtime via ResourceManager
export async function getTitle(context: common.UIAbilityContext): Promise<string> {
  return await context.resourceManager.getStringValue($r('app.string.page_title').id);
}
