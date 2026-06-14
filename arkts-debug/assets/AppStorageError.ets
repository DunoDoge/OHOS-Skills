// AppStorageError.ets - prefer @StorageLink / setAndLink over get
class User {
  id: number = 0;
  name: string = '';
}

// BAD: get() returns User | undefined
// const u = AppStorage.get<User>('user');
// console.info(u.name); // possibly undefined

// GOOD 1: reactive binding inside a component
@Entry
@Component
struct ProfilePage {
  @StorageLink('user') user: User = new User();
  build() {
    Column() {
      Text(this.user.name)
    }
  }
}

// GOOD 2: typed handle outside component
export function readUser(): User {
  const link: SubscribedAbstractProperty<User> =
    AppStorage.setAndLink<User>('user', new User());
  return link.get();
}

// GOOD 3: explicit guard if you really must use get()
export function readUserSafe(): string {
  const u: User | undefined = AppStorage.get<User>('user');
  return u !== undefined ? u.name : 'anon';
}
