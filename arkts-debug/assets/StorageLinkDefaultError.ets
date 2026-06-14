// StorageLinkDefaultError.ets - all storage-bound props need defaults
class User {
  id: number = 0;
  name: string = '';
}

// BAD
// @Component
// struct Bad {
//   @StorageLink('count') count: number; // error: missing initializer
//   @StorageLink('user') user: User;     // error: missing initializer
//   build() {}
// }

// GOOD
@Entry
@Component
struct Demo {
  @StorageLink('count') count: number = 0;
  @StorageLink('user') user: User = new User();
  @StorageLink('maybe') maybe: string | undefined = undefined;

  build() {
    Column() {
      Text(`count: ${this.count}`)
      Text(`user: ${this.user.name}`)
      Text(`maybe: ${this.maybe ?? '-'}`)
    }
  }
}
