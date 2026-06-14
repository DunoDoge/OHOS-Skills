// ArrowFunctionConversionError.ets - use arrow functions for callbacks
@Entry
@Component
struct Counter {
  @State count: number = 0;

  // BAD: function expression captures its own `this`
  // build() {
  //   Button('Tap').onClick(function () { this.count++; });
  // }

  // GOOD: arrow function captures component `this`
  build() {
    Column() {
      Text(`count = ${this.count}`)
      Button('Tap').onClick((): void => {
        this.count++;
      })
    }
  }

  // GOOD: arrow function field
  private reset = (): void => { this.count = 0; };
}
