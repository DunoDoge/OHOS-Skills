# ArkTS 容器类库

> **上游 URL**:
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/containers
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/linear-container
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/nonlinear-container
>
> **抓取时间**: 2026-06-18

---

## 1. 容器类库概述

ArkTS 容器类库由**线性容器**和**非线性容器**两大类组成，提供丰富的数据结构支持。

### 1.1 线性容器

线性容器是一种按照顺序存储和访问元素的数据结构，底层实现为数组或链表。

| 容器 | 底层结构 | 有序 | 可重复 | 线程安全 |
|------|----------|------|--------|----------|
| ArrayList | 数组 | ✅ | ✅ | ❌ |
| List | 数组 | ✅ | ✅ | ❌ |
| LinkedList | 双向链表 | ✅ | ✅ | ❌ |
| Deque | 数组 | ✅ | ✅ | ❌ |
| Queue | 数组 | ✅ | ✅ | ❌ |
| Stack | 数组 | ✅ | ✅ | ❌ |
| Vector | 数组 | ✅ | ✅ | ❌ |

### 1.2 非线性容器

非线性容器是一种基于哈希或树结构存储和访问元素的数据结构，不保证元素顺序（TreeMap/TreeSet 除外）。

| 容器 | 底层结构 | 有序 | 键/值可重复 | 线程安全 |
|------|----------|------|-------------|----------|
| HashMap | 哈希表 | ❌ | 键不可重复 | ❌ |
| HashSet | 哈希表 | ❌ | 不可重复 | ❌ |
| TreeMap | 红黑树 | ✅ | 键不可重复 | ❌ |
| TreeSet | 红黑树 | ✅ | 不可重复 | ❌ |
| LightWeightMap | 数组+哈希 | ❌ | 键不可重复 | ❌ |
| LightWeightSet | 数组+哈希 | ❌ | 不可重复 | ❌ |
| PlainArray | 数组 | ❌ | 键不可重复 | ❌ |

### 1.3 重要提示

> ⚠️ **所有容器类库均非多线程安全**。在多线程并发访问同一容器时，需要开发者自行加锁保护。

引入方式：

```typescript
import { collections } from '@kit.ArkTS';

// 或按需引入
let ArrayList = collections.ArrayList;
let HashMap = collections.HashMap;
// ...
```

---

# 第一部分：线性容器

## 2. ArrayList

### 2.1 特征

- 底层基于数组实现，支持动态扩容
- 随机访问效率高（O(1)）
- 尾部增删效率高，中间增删需要移动元素（O(n)）
- 支持通过索引访问元素

### 2.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let list = new collections.ArrayList<string>();

// 添加元素
list.add('apple');
list.add('banana');
list.add('cherry');

// 按索引访问
console.info(list[0]); // "apple"
console.info(list[1]); // "banana"

// 按索引修改
list[1] = 'blueberry';

// 插入元素
list.insert(1, 'avocado');

// 删除元素
list.remove('cherry');    // 按值删除
list.removeByIndex(0);   // 按索引删除

// 查询
console.info(`size: ${list.length}`);           // 元素数量
console.info(`has banana: ${list.has('banana')}`); // 是否包含

// 遍历
for (let item of list) {
  console.info(item);
}

// 转换为数组
let arr = list.toArray();

// 排序
list.sort((a: string, b: string) => a.localeCompare(b));

// 清空
list.clear();
```

### 2.3 主要方法

| 方法 | 说明 |
|------|------|
| `add(element)` | 添加元素到末尾 |
| `insert(index, element)` | 在指定位置插入元素 |
| `remove(element)` | 删除指定元素 |
| `removeByIndex(index)` | 删除指定位置元素 |
| `has(element)` | 是否包含指定元素 |
| `get(index)` | 获取指定位置元素 |
| `set(index, element)` | 设置指定位置元素 |
| `toArray()` | 转换为数组 |
| `sort(comparator)` | 排序 |
| `clear()` | 清空 |
| `length` | 元素数量 |

## 3. List

### 3.1 特征

- 底层基于数组实现
- 与 ArrayList 类似，但提供了更多便捷操作
- 支持通过索引访问

### 3.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let list = new collections.List<number>();

list.add(1);
list.add(2);
list.add(3);

// 替换指定位置元素
list.set(1, 20);

// 获取子列表
let sub = list.getSubList(0, 2);

// 遍历
list.forEach((value: number, index: number) => {
  console.info(`index: ${index}, value: ${value}`);
});

// 查找元素索引
let idx = list.getIndexOf(20);

// 从末尾查找
let lastIdx = list.getLastIndexOf(3);

// 转换
let arr = list.toArray();
```

## 4. LinkedList

### 4.1 特征

- 底层基于双向链表实现
- 头尾增删效率高（O(1)）
- 随机访问效率低（O(n)）
- 同时实现了 Queue 和 Deque 接口

### 4.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let linkedList = new collections.LinkedList<string>();

// 添加元素
linkedList.add('A');
linkedList.add('B');
linkedList.add('C');

// 头部操作
linkedList.addFirst('X');  // 头部插入
let first = linkedList.getFirst(); // 获取头部元素

// 尾部操作
linkedList.addLast('Z');   // 尾部插入
let last = linkedList.getLast();   // 获取尾部元素

// 删除
let removedFirst = linkedList.removeFirst(); // 删除并返回头部
let removedLast = linkedList.removeLast();   // 删除并返回尾部

// 队列操作（FIFO）
linkedList.add('D');
let peek = linkedList.peek();      // 查看队首
let poll = linkedList.poll();      // 取出队首

// 栈操作（LIFO）
linkedList.push('E');
let pop = linkedList.pop();
```

## 5. Deque

### 5.1 特征

- 双端队列，两端都可以增删元素
- 底层基于数组实现
- 适用于需要频繁在两端操作的场景

### 5.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let deque = new collections.Deque<number>();

// 头部操作
deque.addFirst(1);
deque.addFirst(2);
deque.addFirst(3);
// 当前顺序: 3, 2, 1

// 尾部操作
deque.addLast(4);
deque.addLast(5);
// 当前顺序: 3, 2, 1, 4, 5

// 查看
console.info(`first: ${deque.getFirst()}`); // 3
console.info(`last: ${deque.getLast()}`);   // 5

// 删除
let f = deque.removeFirst(); // 3
let l = deque.removeLast();  // 5

// 遍历
for (let item of deque) {
  console.info(item);
}
```

## 6. Queue

### 6.1 特征

- 先进先出（FIFO）队列
- 底层基于数组实现
- 只能在尾部添加，头部取出

### 6.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let queue = new collections.Queue<string>();

// 入队
queue.add('task1');
queue.add('task2');
queue.add('task3');

// 查看队首
let head = queue.peek(); // "task1"

// 出队
let task = queue.poll(); // "task1"

// 获取第一个元素
let first = queue.getFirst(); // "task2"

console.info(`size: ${queue.length}`);
```

## 7. Stack

### 7.1 特征

- 后进先出（LIFO）栈
- 底层基于数组实现
- 只能在栈顶操作

### 7.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let stack = new collections.Stack<number>();

// 入栈
stack.push(1);
stack.push(2);
stack.push(3);

// 查看栈顶
let top = stack.peek(); // 3

// 出栈
let popped = stack.pop(); // 3

// 查找元素（返回距栈顶的距离，栈顶为0）
let pos = stack.search(1); // 1（距栈顶1个位置）

console.info(`size: ${stack.length}`);
```

## 8. Vector

### 8.1 特征

- 底层基于数组实现，支持容量预分配
- 与 ArrayList 类似，但支持容量管理
- 适用于元素数量可预知的场景

### 8.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let vector = new collections.Vector<string>();

vector.add('a');
vector.add('b');
vector.add('c');

// 容量管理
let cap = vector.getCapacity(); // 获取当前容量
vector.setCapacity(20);         // 设置容量

// 访问
console.info(vector[0]); // "a"

// 插入
vector.insert(1, 'x');

// 删除
vector.remove('b');
vector.removeByIndex(0);

// 克隆
let cloned = vector.clone();

// 排序
vector.sort((a: string, b: string) => a.localeCompare(b));
```

## 9. 线性容器对比

| 特性 | ArrayList | List | LinkedList | Deque | Queue | Stack | Vector |
|------|-----------|------|------------|-------|-------|-------|--------|
| 底层结构 | 数组 | 数组 | 双向链表 | 数组 | 数组 | 数组 | 数组 |
| 随机访问 | O(1) | O(1) | O(n) | O(1) | O(1) | O(1) | O(1) |
| 头部增删 | O(n) | O(n) | O(1) | O(1) | - | - | O(n) |
| 尾部增删 | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) | O(1) |
| 中间增删 | O(n) | O(n) | O(n) | O(n) | - | - | O(n) |
| 容量管理 | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 队列操作 | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |
| 栈操作 | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ |

---

# 第二部分：非线性容器

## 10. HashMap

### 10.1 特征

- 基于哈希表实现的键值对容器
- 查找、插入、删除平均时间复杂度 O(1)
- 键不可重复，值可重复
- 不保证遍历顺序

### 10.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let map = new collections.HashMap<string, number>();

// 添加键值对
map.set('apple', 1);
map.set('banana', 2);
map.set('cherry', 3);

// 获取值
let val = map.get('apple'); // 1

// 检查键
console.info(`has apple: ${map.hasKey('apple')}`);   // true
console.info(`has value 2: ${map.hasValue(2)}`);     // true

// 删除
map.remove('banana');

// 替换
map.replace('apple', 10);

// 遍历键
for (let key of map.keys()) {
  console.info(`key: ${key}`);
}

// 遍历值
for (let value of map.values()) {
  console.info(`value: ${value}`);
}

// 遍历键值对
map.forEach((value: number, key: string) => {
  console.info(`${key}: ${value}`);
});

// 大小
console.info(`size: ${map.length}`);

// 清空
map.clear();
```

## 11. HashSet

### 11.1 特征

- 基于哈希表实现的集合容器
- 元素不可重复
- 不保证遍历顺序
- 查找、插入、删除平均 O(1)

### 11.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let set = new collections.HashSet<string>();

// 添加元素
set.add('apple');
set.add('banana');
set.add('cherry');
set.add('apple'); // 重复添加无效

console.info(`size: ${set.length}`); // 3

// 检查
console.info(`has apple: ${set.has('apple')}`); // true

// 删除
set.remove('banana');

// 遍历
for (let item of set) {
  console.info(item);
}

// 转数组
let arr = set.toArray();
```

## 12. TreeMap

### 12.1 特征

- 基于红黑树实现的有序键值对容器
- 键按自然顺序或自定义比较器排序
- 查找、插入、删除时间复杂度 O(log n)
- 键不可重复

### 12.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let treeMap = new collections.TreeMap<string, number>();

treeMap.set('cherry', 3);
treeMap.set('apple', 1);
treeMap.set('banana', 2);

// 按键有序遍历
for (let [key, value] of treeMap) {
  console.info(`${key}: ${value}`);
}
// 输出顺序: apple:1, banana:2, cherry:3

// 获取最小/最大键
let firstKey = treeMap.getFirstKey();   // "apple"
let lastKey = treeMap.getLastKey();     // "cherry"

// 范围查询
let lower = treeMap.getLowerKey('cherry'); // "banana"
let higher = treeMap.getHigherKey('apple'); // "banana"
```

## 13. TreeSet

### 13.1 特征

- 基于红黑树实现的有序集合
- 元素按自然顺序或自定义比较器排序
- 元素不可重复
- 查找、插入、删除 O(log n)

### 13.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let treeSet = new collections.TreeSet<number>();

treeSet.add(30);
treeSet.add(10);
treeSet.add(20);

// 有序遍历
for (let item of treeSet) {
  console.info(item); // 10, 20, 30
}

// 获取最小/最大值
let first = treeSet.getFirst(); // 10
let last = treeSet.getLast();   // 30

// 范围查询
let lower = treeSet.getLower(20);  // 10
let higher = treeSet.getHigher(20); // 30
```

## 14. LightWeightMap

### 14.1 特征

- 轻量级键值对容器，底层使用数组+哈希实现
- 内存占用比 HashMap 更少
- 适用于小数据量场景
- 键不可重复

### 14.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let lwMap = new collections.LightWeightMap<string, number>();

lwMap.set('a', 1);
lwMap.set('b', 2);
lwMap.set('c', 3);

// 访问
let val = lwMap.get('a'); // 1
let valWithDefault = lwMap.getOrDefault('d', 0); // 0

// 遍历
lwMap.forEach((value: number, key: string) => {
  console.info(`${key}: ${value}`);
});

// 增量操作
lwMap.set('a', 10); // 覆盖
console.info(`size: ${lwMap.length}`);
```

## 15. LightWeightSet

### 15.1 特征

- 轻量级集合容器，底层使用数组+哈希实现
- 内存占用比 HashSet 更少
- 适用于小数据量场景
- 元素不可重复

### 15.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let lwSet = new collections.LightWeightSet<string>();

lwSet.add('x');
lwSet.add('y');
lwSet.add('z');

// 检查
console.info(`has x: ${lwSet.has('x')}`); // true

// 遍历
for (let item of lwSet) {
  console.info(item);
}

// 交集
let other = new collections.LightWeightSet<string>();
other.add('y');
other.add('w');
let intersection = lwSet.intersection(other);

// 转数组
let arr = lwSet.toArray();
```

## 16. PlainArray

### 16.1 特征

- 稀疏数组容器，键为整型
- 底层基于数组实现
- 适用于键为连续或稀疏整型的场景
- 内存效率高

### 16.2 代码示例

```typescript
import { collections } from '@kit.ArkTS';

let plainArray = new collections.PlainArray<string>();

// 添加
plainArray.add(1, 'one');
plainArray.add(5, 'five');
plainArray.add(100, 'hundred');

// 获取
let val = plainArray.get(5); // "five"

// 按索引获取键
let key = plainArray.getKeyAt(1); // 5

// 按索引获取值
let value = plainArray.getValueAt(0); // "one"

// 遍历
plainArray.forEach((value: string, key: number) => {
  console.info(`${key}: ${value}`);
});

// 删除
plainArray.remove(5);

// 大小
console.info(`size: ${plainArray.length}`);
```

## 17. 非线性容器对比

| 特性 | HashMap | HashSet | TreeMap | TreeSet | LightWeightMap | LightWeightSet | PlainArray |
|------|---------|---------|---------|---------|----------------|----------------|------------|
| 底层结构 | 哈希表 | 哈希表 | 红黑树 | 红黑树 | 数组+哈希 | 数组+哈希 | 数组 |
| 有序性 | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 查找 | O(1) | O(1) | O(log n) | O(log n) | O(1) | O(1) | O(1) |
| 插入 | O(1) | O(1) | O(log n) | O(log n) | O(1) | O(1) | O(1) |
| 删除 | O(1) | O(1) | O(log n) | O(log n) | O(1) | O(1) | O(1) |
| 内存占用 | 中 | 中 | 高 | 高 | 低 | 低 | 低 |
| 键类型 | 任意 | - | 可比较 | 可比较 | 任意 | - | 整型 |
| 数据量 | 大 | 大 | 大 | 大 | 小 | 小 | 小 |

---

# 第三部分：容器选择指南

## 18. 按场景推荐容器

### 18.1 需要按索引随机访问

| 场景 | 推荐容器 | 原因 |
|------|----------|------|
| 通用列表 | ArrayList | 随机访问 O(1)，尾部增删 O(1) |
| 需要容量管理 | Vector | 支持预分配容量，减少扩容开销 |
| 频繁头部增删 | LinkedList | 头尾增删 O(1) |

### 18.2 需要队列/栈操作

| 场景 | 推荐容器 | 原因 |
|------|----------|------|
| FIFO 队列 | Queue | 语义清晰，先进先出 |
| 双端队列 | Deque | 两端均可操作 |
| LIFO 栈 | Stack | 语义清晰，后进先出 |
| 同时需要队列和栈 | LinkedList | 同时实现 Queue 和 Deque 接口 |

### 18.3 需要键值对存储

| 场景 | 推荐容器 | 原因 |
|------|----------|------|
| 通用键值对 | HashMap | 查找 O(1)，性能最优 |
| 需要有序遍历 | TreeMap | 按键有序，范围查询 |
| 小数据量 | LightWeightMap | 内存占用更少 |
| 整型键 | PlainArray | 稀疏数组，内存效率高 |

### 18.4 需要集合（去重）

| 场景 | 推荐容器 | 原因 |
|------|----------|------|
| 通用去重集合 | HashSet | 查找 O(1) |
| 需要有序遍历 | TreeSet | 按自然顺序排序 |
| 小数据量 | LightWeightSet | 内存占用更少 |

### 18.5 性能敏感场景

| 场景 | 推荐容器 | 原因 |
|------|----------|------|
| 大量随机访问 | ArrayList / HashMap | O(1) 访问 |
| 大量头部插入 | LinkedList / Deque | O(1) 头部操作 |
| 需要排序 | TreeMap / TreeSet | 红黑树自动排序 |
| 内存受限 | LightWeightMap / LightWeightSet / PlainArray | 内存占用低 |

## 19. 容器选择决策树

```
需要键值对存储？
├── 是
│   ├── 需要有序遍历？
│   │   ├── 是 → TreeMap
│   │   └── 否
│   │       ├── 键为整型？
│   │       │   ├── 是 → PlainArray
│   │       │   └── 否
│   │       │       ├── 数据量小？→ LightWeightMap
│   │       │       └── 数据量大？→ HashMap
│   └── 否（需要集合）
│       ├── 需要有序遍历？
│       │   ├── 是 → TreeSet
│       │   └── 否
│       │       ├── 数据量小？→ LightWeightSet
│       │       └── 数据量大？→ HashSet
└── 否（需要列表）
    ├── 需要队列操作？
    │   ├── 是 → Queue / Deque / LinkedList
    │   └── 否
    │       ├── 需要栈操作？
    │       │   ├── 是 → Stack / LinkedList
    │       │   └── 否
    │       │       ├── 频繁头部增删？→ LinkedList
    │       │       └── 通用场景 → ArrayList
```
