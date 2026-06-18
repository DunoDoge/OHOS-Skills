// IDataSourceError.ets - implement IDataSource for LazyForEach
class User {
  id: number = 0;
  name: string = '';
  constructor(id: number, name: string) {
    this.id = id;
    this.name = name;
  }
}

class ArrayDataSource<T> implements IDataSource {
  private items: T[] = [];
  private listeners: DataChangeListener[] = [];

  constructor(items: T[]) {
    this.items = items;
  }

  totalCount(): number { return this.items.length; }
  getData(index: number): T { return this.items[index]; }

  registerDataChangeListener(l: DataChangeListener): void {
    if (this.listeners.indexOf(l) < 0) {
      this.listeners.push(l);
    }
  }
  unregisterDataChangeListener(l: DataChangeListener): void {
    this.listeners = this.listeners.filter((x: DataChangeListener): boolean => x !== l);
  }

  push(item: T): void {
    this.items.push(item);
    this.listeners.forEach((l: DataChangeListener): void => l.onDataAdd(this.items.length - 1));
  }
}

@Entry
@Component
struct UserList {
  @State source: ArrayDataSource<User> = new ArrayDataSource<User>([
    new User(1, 'Alice'),
    new User(2, 'Bob')
  ]);

  build() {
    List() {
      LazyForEach(
        this.source,
        (u: User) => {
          ListItem() { Text(u.name) }
        },
        (u: User): string => `${u.id}`
      )
    }
  }
}
