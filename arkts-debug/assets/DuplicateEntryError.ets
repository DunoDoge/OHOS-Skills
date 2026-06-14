// DuplicateEntryError.ets - only one @Entry per file
// BAD: two @Entry decorators in the same file
// @Entry
// @Component
// struct PageA { build() { Text('A') } }
//
// @Entry
// @Component
// struct PageB { build() { Text('B') } }

// GOOD: one @Entry, the rest are plain @Component
@Entry
@Component
struct PageRoot {
  build() {
    Column() {
      Header()
      Body()
    }
  }
}

@Component
struct Header {
  build() { Text('header') }
}

@Component
struct Body {
  build() { Text('body') }
}
