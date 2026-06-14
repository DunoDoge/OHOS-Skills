// ColorPropertyError.ets - hex colors instead of non-existent Color members
// BAD: Color.LightBlue / Color.Tomato do not exist
// Text('hi').fontColor(Color.LightBlue);

// GOOD: hex string for any non-enum color
export class AppColor {
  static readonly LIGHT_BLUE: string = '#ADD8E6';
  static readonly TOMATO: string = '#FF6347';
}

@Entry
@Component
struct ColorDemo {
  build() {
    Column() {
      Text('builtin').fontColor(Color.Blue)
      Text('hex').fontColor(AppColor.LIGHT_BLUE)
      Text('rgba').fontColor('rgba(255, 99, 71, 0.8)')
      Text('resource').fontColor($r('app.color.brand'))
    }
  }
}
