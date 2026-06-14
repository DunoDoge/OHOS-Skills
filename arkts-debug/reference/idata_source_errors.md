# IDataSource Type Errors

## Symptom

```
Argument of type 'X[]' is not assignable to parameter of type 'IDataSource'.
LazyForEach requires its data source to implement IDataSource.
```

## Root Cause

`LazyForEach` is designed for incremental rendering; it needs change-notification hooks (`registerDataChangeListener`, etc.) that a plain array does not provide. ArkTS therefore rejects raw arrays as the data argument.

## Canonical Fix

Implement `IDataSource` once and reuse it:

```ts
class ArrayDataSource<T> implements IDataSource {
  private items: T[] = [];
  private listeners: DataChangeListener[] = [];
  constructor(items: T[]) { this.items = items; }
  totalCount(): number { return this.items.length; }
  getData(index: number): T { return this.items[index]; }
  registerDataChangeListener(l: DataChangeListener): void { this.listeners.push(l); }
  unregisterDataChangeListener(l: DataChangeListener): void {
    this.listeners = this.listeners.filter(x => x !== l);
  }
  push(item: T): void {
    this.items.push(item);
    this.listeners.forEach(l => l.onDataAdd(this.items.length - 1));
  }
}

@State source: ArrayDataSource<User> = new ArrayDataSource<User>([]);

build() {
  List() {
    LazyForEach(this.source, (u: User) => ListItem() { Text(u.name) }, (u: User) => `${u.id}`);
  }
}
```

## Notes

- For static lists, use `ForEach` with a plain array instead - simpler and zero boilerplate.
- The third argument to `LazyForEach` (key generator) is mandatory for correct diffing.

## See Also

- `assets/IDataSourceError.ets`
