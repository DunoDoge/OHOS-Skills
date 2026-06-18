# ArkTS 编程规范

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-coding-style-guide
> **抓取时间**: 2026-06-18

---

## 总体原则

1. **可读性优先**：代码首先是给人阅读的，其次才是给机器执行的。编写清晰、易读的代码比编写聪明的代码更重要。
2. **一致性**：在整个项目中保持一致的编码风格，有助于降低理解成本和维护成本。
3. **简洁性**：避免过度设计，保持代码简洁明了。
4. **类型安全**：充分利用 ArkTS 的静态类型系统，在编译期尽可能多地发现错误。
5. **性能意识**：编写代码时应考虑运行时性能，避免不必要的开销。

---

## 命名规范

### UpperCamelCase（大驼峰）

用于类名、接口名、枚举名、类型别名、命名空间名：

```typescript
// 类名
class UserProfile {}

// 接口名
interface EventHandler {}

// 枚举名
enum ColorScheme {}

// 类型别名
type CallbackFunction = () => void

// 命名空间名
namespace NetworkModule {}
```

### lowerCamelCase（小驼峰）

用于变量名、函数名、方法名、参数名：

```typescript
// 变量
let userName: string = 'Alice'
let itemCount: number = 0

// 函数
function calculateTotal(price: number, quantity: number): number {
  return price * quantity
}

// 方法
class Calculator {
  addNumbers(a: number, b: number): number {
    return a + b
  }
}

// 参数
function greet(personName: string, greetingMessage: string): void {
  console.log(`${greetingMessage}, ${personName}!`)
}
```

### 常量命名

常量使用全大写字母，单词之间用下划线分隔（UPPER_SNAKE_CASE）：

```typescript
const MAX_RETRY_COUNT: number = 3
const DEFAULT_TIMEOUT: number = 5000
const API_BASE_URL: string = 'https://api.example.com'
const PI: number = 3.14159265
```

### 枚举成员命名

枚举成员使用 UpperCamelCase：

```typescript
enum Direction {
  Up,
  Down,
  Left,
  Right
}

enum HttpStatus {
  Ok = 200,
  NotFound = 404,
  InternalServerError = 500
}
```

### 文件名

文件名使用小写字母，单词之间用连字符（kebab-case）分隔：

```
user-profile.ets
network-module.ets
data-parser.ets
```

### 布尔变量/方法命名

布尔类型的变量和方法应以 `is`、`has`、`should`、`can`、`will` 等开头：

```typescript
let isActive: boolean = true
let hasPermission: boolean = false
let shouldRetry: boolean = true
let canEdit: boolean = false

function isValid(): boolean {
  return true
}

function hasChildren(): boolean {
  return false
}
```

---

## 代码格式

### 缩进

使用 2 个空格缩进，**不使用 Tab**：

```typescript
function example(): void {
  if (true) {
    console.log('indented with 2 spaces')
  }
}
```

### 行宽

每行代码不超过 120 个字符。超长行应适当换行：

```typescript
// 超长函数调用换行
let result = someLongFunctionName(
  firstArgument,
  secondArgument,
  thirdArgument
)

// 超长条件表达式换行
if (someLongCondition &&
    anotherLongCondition &&
    yetAnotherCondition) {
  // do something
}
```

### 空行

- 类、接口、枚举之间保留 1 个空行
- 方法之间保留 1 个空行
- 逻辑块之间保留 1 个空行
- 文件末尾保留 1 个空行

```typescript
class User {
  name: string = ''
  age: number = 0

  constructor(name: string, age: number) {
    this.name = name
    this.age = age
  }

  greet(): string {
    return `Hello, ${this.name}!`
  }

  // 逻辑块之间空行
  isAdult(): boolean {
    return this.age >= 18
  }
}
```

### 大括号

左大括号不换行（K&R 风格）：

```typescript
// 正确
class MyClass {
  method(): void {
    if (condition) {
      // ...
    } else {
      // ...
    }
  }
}

// 错误 - 左大括号换行
class MyClass
{
  method(): void
  {
    // ...
  }
}
```

`if/else`、`for`、`while`、`do` 等语句体必须使用大括号，即使只有一行：

```typescript
// 正确
if (condition) {
  doSomething()
}

// 错误 - 缺少大括号
if (condition)
  doSomething()
```

### 空格使用

- 二元运算符两侧加空格
- 逗号后加空格
- 关键字后加空格
- 函数名与括号之间不加空格

```typescript
// 正确
let sum: number = a + b
let arr: number[] = [1, 2, 3]
if (condition) {}
function add(a: number, b: number): number {}

// 错误
let sum:number=a+b
let arr:number[]=[1,2,3]
if(condition) {}
function add (a:number, b:number):number {}
```

---

## 注释规范

### 文件头注释

在文件开头添加文件说明注释：

```typescript
/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

### 类和接口注释

使用 JSDoc 风格注释说明类和接口的用途：

```typescript
/**
 * 用户信息类，用于存储和管理用户的基本信息
 */
class User {
  /** 用户名称 */
  name: string = ''

  /** 用户年龄 */
  age: number = 0
}

/**
 * 数据回调接口
 */
interface DataCallback {
  /**
   * 数据更新时的回调方法
   * @param data - 更新的数据
   */
  onDataChanged(data: string): void
}
```

### 方法注释

```typescript
/**
 * 计算两个数的和
 * @param a - 第一个加数
 * @param b - 第二个加数
 * @returns 两数之和
 */
function add(a: number, b: number): number {
  return a + b
}
```

### 行内注释

使用 `//` 进行行内注释，注释与代码之间至少一个空格：

```typescript
let total: number = price * quantity  // 计算总价
```

### TODO 注释

使用 `TODO` 标记待办事项：

```typescript
// TODO: 优化此算法的时间复杂度
function processData(data: number[]): number[] {
  return data.filter(x => x > 0)
}
```

---

## 编程实践

### 类型安全

#### 始终提供显式类型标注

```typescript
// 正确 - 显式类型标注
let name: string = 'Alice'
let age: number = 30
let items: string[] = ['a', 'b', 'c']

// 不推荐 - 依赖类型推断（虽然合法，但显式标注更清晰）
let name = 'Alice'
let age = 30
```

#### 禁止使用 any 和 unknown

```typescript
// 错误 - 使用 any
let data: any = getData()

// 正确 - 使用具体类型
let data: UserInfo = getData()
```

#### 优先使用 const

```typescript
// 正确 - 不会变更的值使用 const
const MAX_SIZE: number = 100
const API_URL: string = '/api/v1'

// 仅在需要重新赋值时使用 let
let count: number = 0
count++
```

### 错误处理

#### 使用 try-catch 处理可能的异常

```typescript
function parseJSON(jsonStr: string): Record<string, Object> {
  try {
    let obj: Record<string, Object> = JSON.parse(jsonStr) as Record<string, Object>
    return obj
  } catch (e) {
    console.error(`JSON parse error: ${(e as Error).message}`)
    return {} as Record<string, Object>
  }
}
```

#### 不要忽略 catch 中的错误

```typescript
// 错误 - 忽略错误
try {
  doSomething()
} catch (e) {
  // 什么都不做
}

// 正确 - 至少记录错误
try {
  doSomething()
} catch (e) {
  console.error(`Error: ${(e as Error).message}`)
}
```

#### 提供有意义的错误信息

```typescript
// 错误 - 错误信息不明确
throw new Error('Error')

// 正确 - 错误信息清晰
throw new Error('Failed to connect to server: connection timeout after 5000ms')
```

### 性能优化

#### 避免在循环中创建对象

```typescript
// 不推荐 - 每次循环创建新对象
for (let i = 0; i < 1000; i++) {
  let point = { x: i, y: i * 2 }
  processPoint(point)
}

// 推荐 - 复用对象
let point = { x: 0, y: 0 }
for (let i = 0; i < 1000; i++) {
  point.x = i
  point.y = i * 2
  processPoint(point)
}
```

#### 提取循环中的不变计算

```typescript
// 不推荐 - 每次循环重复计算
for (let i = 0; i < array.length; i++) {
  let value = array[i] * Math.PI * 2
}

// 推荐 - 提取不变量
const FACTOR: number = Math.PI * 2
const len: number = array.length
for (let i = 0; i < len; i++) {
  let value = array[i] * FACTOR
}
```

#### 使用 const 声明不变的值

```typescript
// 推荐
const MAX_RETRIES: number = 3
const TIMEOUT_MS: number = 5000

// 不推荐 - 不变的值使用 let
let MAX_RETRIES: number = 3
let TIMEOUT_MS: number = 5000
```
