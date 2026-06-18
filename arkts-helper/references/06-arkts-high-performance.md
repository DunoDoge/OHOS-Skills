# ArkTS 高性能编程

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-high-performance-programming
> **抓取时间**: 2026-06-18

本文档介绍 ArkTS 高性能编程的最佳实践，涵盖声明与表达式、函数、数组、容器、并发等方面的优化建议。每个优化项包含不合规代码和合规代码的对比示例。

---

## 声明与表达式优化

### 使用 const 声明不变的值

`const` 声明使编译器能进行更多优化，同时提高代码可读性。

**不合规：**
```typescript
let PI: number = 3.14159
let MAX_SIZE: number = 100
let APP_NAME: string = 'MyApp'

function calculateArea(radius: number): number {
  let multiplier: number = 2
  return PI * radius * multiplier
}
```

**合规：**
```typescript
const PI: number = 3.14159
const MAX_SIZE: number = 100
const APP_NAME: string = 'MyApp'

function calculateArea(radius: number): number {
  const multiplier: number = 2
  return PI * radius * multiplier
}
```

### 避免整型与浮点型混用

ArkTS 中 `number` 类型统一表示数字，但整型与浮点型的运算可能导致额外的类型转换开销。应尽量保持运算类型一致。

**不合规：**
```typescript
let a: number = 10       // 整型
let b: number = 3.14     // 浮点型
let result: number = a + b  // 混合运算，需要类型转换
```

**合规：**
```typescript
let a: number = 10.0     // 统一使用浮点型
let b: number = 3.14
let result: number = a + b  // 同类型运算，无转换开销
```

### 避免数值溢出

数值溢出会导致运行时错误或不可预期的行为，应在代码中进行边界检查。

**不合规：**
```typescript
function factorial(n: number): number {
  if (n <= 1) {
    return 1
  }
  return n * factorial(n - 1)  // 大数时溢出
}

let result: number = factorial(100)  // 溢出
```

**合规：**
```typescript
function factorial(n: number): number {
  if (n < 0) {
    throw new Error('Negative input')
  }
  if (n <= 1) {
    return 1
  }
  let result: number = 1
  for (let i: number = 2; i <= n; i++) {
    result *= i
    if (!isFinite(result)) {
      throw new Error('Overflow')
    }
  }
  return result
}
```

### 循环常量提取

将循环中不变的计算提取到循环外部，避免重复计算。

**不合规：**
```typescript
function processItems(items: number[]): number[] {
  let results: number[] = []
  for (let i = 0; i < items.length; i++) {
    // 每次循环都重新计算 Math.PI * 2
    results.push(items[i] * Math.PI * 2)
  }
  return results
}
```

**合规：**
```typescript
function processItems(items: number[]): number[] {
  const FACTOR: number = Math.PI * 2  // 提取到循环外
  const len: number = items.length     // 提取 length
  let results: number[] = []
  for (let i: number = 0; i < len; i++) {
    results.push(items[i] * FACTOR)
  }
  return results
}
```

---

## 函数优化

### 参数传递优化

避免传递大对象，优先传递基本类型或引用。

**不合规：**
```typescript
function processArray(arr: number[]): number {
  // 传递整个数组，可能产生拷贝开销
  let sum: number = 0
  for (let item of arr) {
    sum += item
  }
  return sum
}
```

**合规：**
```typescript
function processArray(arr: number[]): number {
  let sum: number = 0
  const len: number = arr.length
  for (let i: number = 0; i < len; i++) {
    sum += arr[i]
  }
  return sum
}
```

### 避免可选参数

可选参数在运行时需要额外的检查逻辑，如果参数是必需的，应声明为必选参数。

**不合规：**
```typescript
function createUser(name?: string, age?: number): string {
  let userName: string = name ?? 'Anonymous'
  let userAge: number = age ?? 0
  return `${userName}, ${userAge}`
}
```

**合规：**
```typescript
function createUser(name: string, age: number): string {
  return `${name}, ${age}`
}

// 如果确实需要默认值，使用默认参数
function createUserWithDefault(name: string = 'Anonymous', age: number = 0): string {
  return `${name}, ${age}`
}
```

### 避免函数参数重新赋值

在函数体内重新赋值参数会降低代码可读性，也可能影响优化。

**不合规：**
```typescript
function calculateTotal(price: number, quantity: number): number {
  price = price * 0.9  // 重新赋值参数
  quantity = Math.max(quantity, 1)  // 重新赋值参数
  return price * quantity
}
```

**合规：**
```typescript
function calculateTotal(price: number, quantity: number): number {
  const discountedPrice: number = price * 0.9
  const effectiveQuantity: number = Math.max(quantity, 1)
  return discountedPrice * effectiveQuantity
}
```

---

## 数组优化

### 数组初始化

预分配数组大小可以避免频繁的内存重新分配。

**不合规：**
```typescript
function generateSequence(n: number): number[] {
  let result: number[] = []
  for (let i: number = 0; i < n; i++) {
    result.push(i)  // 每次 push 可能触发扩容
  }
  return result
}
```

**合规：**
```typescript
function generateSequence(n: number): number[] {
  // 预分配数组大小
  let result: number[] = new Array<number>(n)
  for (let i: number = 0; i < n; i++) {
    result[i] = i
  }
  return result
}
```

### 避免稀疏数组

稀疏数组（存在未赋值的索引）会导致性能下降，应确保数组是连续的。

**不合规：**
```typescript
let arr: number[] = []
arr[100] = 42  // 稀疏数组，索引 0-99 未赋值
```

**合规：**
```typescript
let arr: number[] = new Array<number>(101)
for (let i: number = 0; i < 101; i++) {
  arr[i] = 0  // 初始化所有元素
}
arr[100] = 42
```

### 使用合适的数组遍历方式

**不合规：**
```typescript
let arr: number[] = [1, 2, 3, 4, 5]

// forEach 会创建额外的函数调用
arr.forEach((item: number) => {
  console.log(item)
})
```

**合规：**
```typescript
let arr: number[] = [1, 2, 3, 4, 5]

// 使用 for 循环，避免函数调用开销
const len: number = arr.length
for (let i: number = 0; i < len; i++) {
  console.log(arr[i])
}
```

---

## 容器优化

### 使用 ArkTS 容器类替代 Array

ArkTS 提供了高性能的容器类，在特定场景下比 `Array` 性能更好。

#### ArrayList

适用于频繁的随机访问和尾部添加/删除操作：

**不合规：**
```typescript
let list: number[] = []
for (let i: number = 0; i < 10000; i++) {
  list.push(i)
}
// 随机访问
let value: number = list[5000]
```

**合规：**
```typescript
import { ArrayList } from '@kit.ArkTS'

let list: ArrayList<number> = new ArrayList<number>()
for (let i: number = 0; i < 10000; i++) {
  list.add(i)
}
// 随机访问
let value: number = list[5000]
```

#### HashMap

适用于键值对存储和快速查找：

**不合规：**
```typescript
let map: Record<string, number> = {}
map['key1'] = 1
map['key2'] = 2
let value: number = map['key1']
```

**合规：**
```typescript
import { HashMap } from '@kit.ArkTS'

let map: HashMap<string, number> = new HashMap<string, number>()
map.set('key1', 1)
map.set('key2', 2)
let value: number = map.get('key1') as number
```

#### LinkedList

适用于频繁的头部和中间插入/删除操作：

**不合规：**
```typescript
let list: number[] = []
// 频繁在头部插入
list.unshift(1)
list.unshift(2)
list.unshift(3)
```

**合规：**
```typescript
import { LinkedList } from '@kit.ArkTS'

let list: LinkedList<number> = new LinkedList<number>()
list.addFirst(1)
list.addFirst(2)
list.addFirst(3)
```

#### 常用容器类对照表

| ArkTS 容器类 | 替代的 Array/对象用法 | 适用场景 |
|-------------|---------------------|---------|
| ArrayList | Array | 频繁随机访问、尾部增删 |
| LinkedList | Array（头部操作） | 频繁头部/中间增删 |
| HashMap | Record / Object | 键值对存储、快速查找 |
| HashSet | Array（去重） | 唯一值集合 |
| TreeMap | Record（有序） | 有序键值对 |
| TreeSet | Array（有序去重） | 有序唯一值集合 |
| Deque | Array（双端操作） | 双端队列操作 |
| Queue | Array（FIFO） | 先进先出队列 |
| Stack | Array（LIFO） | 后进先出栈 |

---

## 并发优化

### 使用 TaskPool 执行耗时任务

TaskPool 是 ArkTS 提供的线程池，适用于执行独立的耗时任务。

**不合规：**
```typescript
import { taskpool } from '@kit.ArkTS'

// 在主线程执行耗时计算，阻塞 UI
function heavyComputation(n: number): number {
  let result: number = 0
  for (let i: number = 0; i < n; i++) {
    result += Math.sqrt(i)
  }
  return result
}

let result: number = heavyComputation(10000000)  // 阻塞主线程
console.log(`Result: ${result}`)
```

**合规：**
```typescript
import { taskpool } from '@kit.ArkTS'

@Concurrent
function heavyComputation(n: number): number {
  let result: number = 0
  for (let i: number = 0; i < n; i++) {
    result += Math.sqrt(i)
  }
  return result
}

async function runComputation(): Promise<void> {
  let task: taskpool.Task = new taskpool.Task(heavyComputation, 10000000)
  let result: number = await taskpool.execute(task) as number
  console.log(`Result: ${result}`)
}
```

### 使用 Worker 处理长时间运行的任务

Worker 适用于需要长时间运行的后台任务，如数据处理、文件读写等。

**不合规：**
```typescript
// 在主线程处理大量数据
function processLargeData(data: string[]): string[] {
  let results: string[] = []
  for (let item of data) {
    // 复杂的数据处理
    results.push(item.toUpperCase().trim())
  }
  return results
}

let data: string[] = loadLargeDataset()
let results: string[] = processLargeData(data)  // 阻塞主线程
```

**合规：**
```typescript
// worker.ets
import { worker, MessageEvents } from '@kit.ArkTS'

let workerPort = worker.workerPort

workerPort.onmessage = (e: MessageEvents): void => {
  let data: string[] = e.data as string[]
  let results: string[] = []
  for (let item of data) {
    results.push(item.toUpperCase().trim())
  }
  workerPort.postMessage(results)
}

// main.ets
import { worker } from '@kit.ArkTS'

let workerInstance = new worker.ThreadWorker('entry/ets/workers/Worker.ets')

workerInstance.onmessage = (e: MessageEvents): void => {
  let results: string[] = e.data as string[]
  console.log(`Processed ${results.length} items`)
}

let data: string[] = loadLargeDataset()
workerInstance.postMessage(data)
```

### TaskPool 与 Worker 的选择

| 特性 | TaskPool | Worker |
|------|----------|--------|
| 生命周期 | 自动管理 | 手动管理 |
| 线程数量 | 自动调度（最多与 CPU 核心数相同） | 手动创建 |
| 通信方式 | Promise | onmessage/postMessage |
| 适用场景 | 独立的耗时计算任务 | 长时间运行的后台任务 |
| 任务取消 | 支持 | 需自行实现 |
| 优先级 | 支持 | 不支持 |

---

## 其他优化建议

### 避免频繁创建短生命周期对象

频繁创建和销毁短生命周期对象会增加垃圾回收压力。

**不合规：**
```typescript
function processItems(items: number[]): void {
  for (let item of items) {
    // 每次循环创建新对象
    let point = new Point(item, item * 2)
    drawPoint(point)
  }
}
```

**合规：**
```typescript
function processItems(items: number[]): void {
  // 复用对象
  let point = new Point(0, 0)
  for (let item of items) {
    point.x = item
    point.y = item * 2
    drawPoint(point)
  }
}
```

### 使用位运算替代部分数学运算

对于整数运算，位运算通常比数学函数更快。

**不合规：**
```typescript
let x: number = 10
let floor: number = Math.floor(x / 2)  // 除法 + 取整
let power: number = Math.pow(2, 3)     // 幂运算
```

**合规：**
```typescript
let x: number = 10
let floor: number = x >> 1     // 右移一位 = 除以 2 取整
let power: number = 1 << 3     // 左移三位 = 2 的 3 次方
```

### 避免在热路径中使用字符串拼接

**不合规：**
```typescript
function buildMessage(items: string[]): string {
  let message: string = ''
  for (let item of items) {
    message += item + ', '  // 每次拼接创建新字符串
  }
  return message
}
```

**合规：**
```typescript
function buildMessage(items: string[]): string {
  // 使用数组 join 减少中间字符串创建
  return items.join(', ')
}
```

### 合理使用懒加载

对于不立即需要的资源，使用懒加载减少启动时间。

**不合规：**
```typescript
// 启动时加载所有模块
import { ModuleA } from './ModuleA'
import { ModuleB } from './ModuleB'
import { ModuleC } from './ModuleC'

function useModuleA(): void {
  ModuleA.doSomething()
}
```

**合规：**
```typescript
// 按需加载模块
async function useModuleA(): Promise<void> {
  let module = await import('./ModuleA')
  module.doSomething()
}
```

### 减少闭包捕获

闭包会捕获外部变量，增加内存占用。在性能敏感的场景中，应减少不必要的闭包使用。

**不合规：**
```typescript
function createHandlers(items: number[]): (() => void)[] {
  let handlers: (() => void)[] = []
  for (let i: number = 0; i < items.length; i++) {
    // 每个闭包都捕获了 items 和 i
    handlers.push(() => {
      console.log(items[i])
    })
  }
  return handlers
}
```

**合规：**
```typescript
function createHandler(item: number): () => void {
  // 只捕获必要的值
  return (): void => {
    console.log(item)
  }
}

function createHandlers(items: number[]): (() => void)[] {
  let handlers: (() => void)[] = []
  for (let item of items) {
    handlers.push(createHandler(item))
  }
  return handlers
}
```

### 性能优化检查清单

- [ ] 不变的值使用 `const` 声明
- [ ] 循环中不变的计算已提取到循环外
- [ ] 数组已预分配大小
- [ ] 不存在稀疏数组
- [ ] 使用 ArkTS 容器类替代 Array（适用场景）
- [ ] 耗时任务使用 TaskPool 或 Worker
- [ ] 避免频繁创建短生命周期对象
- [ ] 避免在热路径中使用字符串拼接
- [ ] 减少不必要的闭包捕获
- [ ] 函数参数不被重新赋值
