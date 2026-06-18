# TypeScript 到 ArkTS 适配规则

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/typescript-to-arkts-migration-guide
> **抓取时间**: 2026-06-18

本文档详细描述从 TypeScript 迁移到 ArkTS 时需要遵循的适配规则。每条规则均包含不合规的 TS 代码和合规的 ArkTS 代码的对比示例。

---

## 1. 强制使用静态类型

### 1.1 禁止使用 any 类型

`any` 类型会绕过类型检查，导致编译期无法发现潜在的类型错误。

**不合规（TS）：**
```typescript
let value: any = 10
value = 'hello'
value.someMethod()
```

**合规（ArkTS）：**
```typescript
let value: number = 10
// value = 'hello'  // 编译错误：不能将 string 赋值给 number
```

### 1.2 禁止使用 unknown 类型

`unknown` 类型虽然比 `any` 更安全，但在 ArkTS 中同样被禁止，因为运行时类型检查会带来性能开销。

**不合规（TS）：**
```typescript
let value: unknown = fetchData()
if (typeof value === 'string') {
  console.log(value.toUpperCase())
}
```

**合规（ArkTS）：**
```typescript
let value: string = fetchData()
console.log(value.toUpperCase())
```

### 1.3 所有变量声明必须有类型标注

**不合规（TS）：**
```typescript
let name = 'Alice'
let items = [1, 2, 3]
```

**合规（ArkTS）：**
```typescript
let name: string = 'Alice'
let items: number[] = [1, 2, 3]
```

### 1.4 函数参数和返回值必须有类型标注

**不合规（TS）：**
```typescript
function add(a, b) {
  return a + b
}
```

**合规（ArkTS）：**
```typescript
function add(a: number, b: number): number {
  return a + b
}
```

### 1.5 禁止隐式 any

**不合规（TS）：**
```typescript
function process(data) {
  return data.length
}
```

**合规（ArkTS）：**
```typescript
function process(data: string): number {
  return data.length
}
```

---

## 2. 禁止在运行时变更对象布局

### 2.1 禁止动态添加属性

**不合规（TS）：**
```typescript
class Person {
  name: string = ''
}

let p = new Person()
(p as any).age = 30  // 动态添加属性
```

**合规（ArkTS）：**
```typescript
class Person {
  name: string = ''
  age: number = 0
}

let p = new Person()
p.age = 30
```

### 2.2 禁止动态删除属性

**不合规（TS）：**
```typescript
class Person {
  name: string = ''
  age: number = 0
}

let p = new Person()
delete p.age  // 动态删除属性
```

**合规（ArkTS）：**
```typescript
class Person {
  name: string = ''
  age: number | null = null
}

let p = new Person()
p.age = null  // 使用 null 表示属性无效
```

### 2.3 禁止使用 delete 运算符

**不合规（TS）：**
```typescript
let obj: Record<string, number> = { a: 1, b: 2 }
delete obj.a
```

**合规（ArkTS）：**
```typescript
class Config {
  a: number = 0
  b: number = 0
}

let config = new Config()
config.a = 0  // 重置为默认值，而非删除
```

---

## 3. 限制运算符的语义

### 3.1 一元加法运算符（+）仅用于数字

**不合规（TS）：**
```typescript
let str: string = '123'
let num: number = +str  // 将字符串转换为数字
```

**合规（ArkTS）：**
```typescript
let str: string = '123'
let num: number = Number(str)  // 使用 Number() 进行转换
// 或
let num2: number = parseInt(str, 10)  // 使用 parseInt()
```

### 3.2 二元加法运算符（+）不允许混合类型

**不合规（TS）：**
```typescript
let result = 'Age: ' + 25  // 字符串与数字拼接
```

**合规（ArkTS）：**
```typescript
let result: string = `Age: ${25}`  // 使用模板字符串
// 或
let result2: string = 'Age: ' + 25.toString()
```

### 3.3 禁止使用 == 和 !=

ArkTS 要求使用严格相等运算符 `===` 和 `!==`，避免隐式类型转换。

**不合规（TS）：**
```typescript
if (value == null) {}
if (count != 0) {}
```

**合规（ArkTS）：**
```typescript
if (value === null) {}
if (count !== 0) {}
```

---

## 4. 不支持 structural typing

TypeScript 使用结构化类型系统（structural typing），即只要两个类型的结构相同，就认为它们是兼容的。ArkTS 不支持这种特性，要求类型之间必须有明确的继承或实现关系。

### 4.1 对象字面量必须对应显式声明的类或接口

**不合规（TS）：**
```typescript
let point = { x: 10, y: 20 }

function printPoint(p: { x: number; y: number }): void {
  console.log(`(${p.x}, ${p.y})`)
}
```

**合规（ArkTS）：**
```typescript
class Point {
  x: number = 0
  y: number = 0
}

let point = new Point()
point.x = 10
point.y = 20

function printPoint(p: Point): void {
  console.log(`(${p.x}, ${p.y})`)
}
```

### 4.2 类型兼容性基于声明关系而非结构

**不合规（TS）：**
```typescript
interface Point2D {
  x: number
  y: number
}

interface Point3D {
  x: number
  y: number
  z: number
}

let p2: Point2D = { x: 1, y: 2 }
let p3: Point3D = { x: 1, y: 2, z: 3 }
p2 = p3  // TS 中允许，因为结构兼容
```

**合规（ArkTS）：**
```typescript
class Point2D {
  x: number = 0
  y: number = 0
}

class Point3D extends Point2D {
  z: number = 0
}

let p2: Point2D = new Point2D()
let p3: Point3D = new Point3D()
p2 = p3  // 允许，因为 Point3D 继承自 Point2D
```

---

## 5. 约束说明

### 5.1 对象属性名必须是合法标识符

**不合规（TS）：**
```typescript
let obj = {
  'prop-name': 'value',
  '123abc': 'value'
}
```

**合规（ArkTS）：**
```typescript
class Config {
  propName: string = ''
  abc123: string = ''
}
```

### 5.2 类型命名唯一

同一作用域内不允许存在同名类型声明。

**不合规（TS）：**
```typescript
type Result = string
type Result = number  // 重复定义
```

**合规（ArkTS）：**
```typescript
type StringResult = string
type NumberResult = number
```

### 5.3 使用 let 而非 var

**不合规（TS）：**
```typescript
var count = 0
var name = 'Alice'
```

**合规（ArkTS）：**
```typescript
let count: number = 0
let name: string = 'Alice'
```

### 5.4 使用 class 而非 function 构造器

**不合规（TS）：**
```typescript
function Person(name: string, age: number) {
  this.name = name
  this.age = age
}

let p = new Person('Alice', 30)
```

**合规（ArkTS）：**
```typescript
class Person {
  name: string = ''
  age: number = 0

  constructor(name: string, age: number) {
    this.name = name
    this.age = age
  }
}

let p = new Person('Alice', 30)
```

### 5.5 禁止 as 类型断言

ArkTS 不支持 `as` 类型断言（除少数场景外），应使用类型声明或适当的类型转换。

**不合规（TS）：**
```typescript
let value: any = 'hello'
let len: number = (value as string).length
```

**合规（ArkTS）：**
```typescript
let value: string = 'hello'
let len: number = value.length
```

对于 `JSON.parse` 等返回值的场景，使用 `Record` 类型：

**不合规（TS）：**
```typescript
let obj: any = JSON.parse('{"name":"Alice"}')
let name: string = (obj as any).name
```

**合规（ArkTS）：**
```typescript
let obj: Record<string, Object> = JSON.parse('{"name":"Alice"}') as Record<string, Object>
let name: string = obj['name'] as string
```

### 5.6 禁止使用 eval

**不合规（TS）：**
```typescript
let result = eval('1 + 2')
```

**合规（ArkTS）：**
```typescript
let result: number = 1 + 2
```

---

## 6. 其他适配规则

### 6.1 禁止索引签名

**不合规（TS）：**
```typescript
interface Config {
  [key: string]: string
}
```

**合规（ArkTS）：**
```typescript
class Config {
  host: string = ''
  port: string = ''
  path: string = ''
}

// 或使用 Record 类型
let config: Record<string, string> = {}
```

### 6.2 禁止函数重载

**不合规（TS）：**
```typescript
function greet(name: string): string
function(name: string, age: number): string
function greet(name: string, age?: number): string {
  if (age !== undefined) {
    return `Hello, ${name}, age ${age}!`
  }
  return `Hello, ${name}!`
}
```

**合规（ArkTS）：**
```typescript
function greet(name: string, age?: number): string {
  if (age !== undefined) {
    return `Hello, ${name}, age ${age}!`
  }
  return `Hello, ${name}!`
}
```

### 6.3 禁止 in 运算符属性检查

**不合规（TS）：**
```typescript
if ('name' in obj) {
  console.log(obj.name)
}
```

**合规（ArkTS）：**
```typescript
// 使用 instanceof 检查类型
if (obj instanceof Person) {
  console.log(obj.name)
}

// 或使用明确的类型判断
if (obj !== null && obj !== undefined) {
  console.log(obj.name)
}
```

### 6.4 禁止使用 Object 类型的大写形式作为类型标注

应使用具体的类或接口替代 `Object` 类型。

**不合规（TS）：**
```typescript
let obj: Object = { name: 'Alice' }
function process(data: Object): void {}
```

**合规（ArkTS）：**
```typescript
class UserData {
  name: string = ''
}

let obj: UserData = new UserData()
obj.name = 'Alice'

function process(data: UserData): void {}
```

### 6.5 禁止使用 typeof 运算符作为类型查询

**不合规（TS）：**
```typescript
let name = 'Alice'
type NameType = typeof name
```

**合规（ArkTS）：**
```typescript
let name: string = 'Alice'
type NameType = string
```

### 6.6 禁止使用命名空间（namespace）中的非导出声明

**不合规（TS）：**
```typescript
namespace Utils {
  function internalHelper(): void {}  // 未导出
  export function publicApi(): void {
    internalHelper()
  }
}
```

**合规（ArkTS）：**
```typescript
namespace Utils {
  export function internalHelper(): void {}  // 必须导出
  export function publicApi(): void {
    internalHelper()
  }
}
```

### 6.7 禁止使用 getter/setter 与同名字段

**不合规（TS）：**
```typescript
class Person {
  private _name: string = ''

  get name(): string {
    return this._name
  }

  set name(value: string) {
    this._name = value
  }
}
```

**合规（ArkTS）：**
```typescript
class Person {
  name: string = ''
}
```

> 注意：ArkTS 对 getter/setter 的支持有限制。如果确实需要 getter/setter 逻辑，请确保不与同名字段冲突。

### 6.8 禁止使用 Symbol

**不合规（TS）：**
```typescript
const key = Symbol('key')
let obj = { [key]: 'value' }
```

**合规（ArkTS）：**
```typescript
class Config {
  key: string = 'value'
}
```

### 6.9 禁止使用 for-in 循环

**不合规（TS）：**
```typescript
let obj = { a: 1, b: 2, c: 3 }
for (let key in obj) {
  console.log(key, obj[key])
}
```

**合规（ArkTS）：**
```typescript
class Config {
  a: number = 1
  b: number = 2
  c: number = 3
}

let config = new Config()
// 使用 Object.keys 或直接访问属性
let keys: string[] = Object.keys(config) as string[]
for (let key of keys) {
  console.log(key, config[key])
}
```

### 6.10 禁止使用 with 语句

**不合规（TS）：**
```typescript
with (obj) {
  console.log(name)
}
```

**合规（ArkTS）：**
```typescript
console.log(obj.name)
```

### 6.11 类中禁止使用 constructor 签名类型

**不合规（TS）：**
```typescript
type Constructor = new (name: string) => Person
```

**合规（ArkTS）：**
```typescript
// 使用类类型本身
class Person {
  name: string = ''
  constructor(name: string) {
    this.name = name
  }
}

function createPerson(ctor: Person, name: string): Person {
  let p = new Person(name)
  return p
}
```

### 6.12 禁止使用 this 类型

**不合规（TS）：**
```typescript
class Container {
  data: string = ''

  clone(): this {
    // ...
    return this
  }
}
```

**合规（ArkTS）：**
```typescript
class Container {
  data: string = ''

  clone(): Container {
    // ...
    return this
  }
}
```

### 6.13 禁止在接口中定义构造签名

**不合规（TS）：**
```typescript
interface IFactory {
  new (name: string): Product
}
```

**合规（ArkTS）：**
```typescript
class Product {
  name: string = ''
  constructor(name: string) {
    this.name = name
  }
}

// 使用工厂函数代替
function createProduct(name: string): Product {
  return new Product(name)
}
```

### 6.14 禁止在接口中定义调用签名

**不合规（TS）：**
```typescript
interface Callable {
  (x: number): string
}
```

**合规（ArkTS）：**
```typescript
type Callable = (x: number) => string

// 或使用函数类型
let callable: (x: number) => string = (x: number): string => x.toString()
```

### 6.15 禁止使用条件类型

**不合规（TS）：**
```typescript
type Result<T> = T extends string ? string : number
```

**合规（ArkTS）：**
```typescript
// 使用联合类型或重载替代
type StringOrNumber = string | number
```

### 6.16 禁止使用映射类型

**不合规（TS）：**
```typescript
type Readonly<T> = {
  readonly [P in keyof T]: T[P]
}
```

**合规（ArkTS）：**
```typescript
// 显式定义每个属性
class ReadonlyConfig {
  readonly host: string = ''
  readonly port: number = 0
}
```

---

## 适配规则速查表

| 规则 | TS 写法 | ArkTS 写法 |
|------|---------|------------|
| 禁止 any | `let x: any` | `let x: 具体类型` |
| 禁止 unknown | `let x: unknown` | `let x: 具体类型` |
| 禁止 var | `var x = 1` | `let x: number = 1` |
| 禁止动态添加属性 | `obj.newProp = v` | 在 class 中声明属性 |
| 禁止动态删除属性 | `delete obj.prop` | 设为 null 或默认值 |
| 禁止 as 断言 | `x as string` | 使用具体类型声明 |
| 禁止索引签名 | `[key: string]: T` | 使用 class 或 Record |
| 禁止函数重载 | 多个签名 | 使用可选参数 |
| 禁止 in 属性检查 | `'key' in obj` | 使用 instanceof |
| 禁止 for-in | `for (k in obj)` | `for (k of keys)` |
| 禁止 eval | `eval('code')` | 直接编写代码 |
| 禁止 with | `with (obj) {}` | 直接引用 `obj.prop` |
| 禁止 Symbol | `Symbol('key')` | 使用字符串属性名 |
| 禁止 typeof 类型查询 | `typeof x` | 直接写类型名 |
| 禁止条件类型 | `T extends ? :` | 使用联合类型 |
| 禁止映射类型 | `{[P in K]: T}` | 显式定义属性 |
| 一元+仅用于数字 | `+str` | `Number(str)` |
| 严格相等 | `==` / `!=` | `===` / `!==` |
| 使用 class | `function Ctor() {}` | `class Ctor {}` |
