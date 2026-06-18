# ArkTS 语言介绍

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts
> **抓取时间**: 2026-06-18

ArkTS 是 HarmonyOS 优选的主力应用开发语言。ArkTS 基于 TypeScript（简称 TS）语言，扩展了声明式 UI 语法，提供了更简洁、更自然的 UI 开发体验。同时，ArkTS 通过规范约束，在运行时性能和程序稳定性方面做了进一步增强。

与 TS 相比，ArkTS 的主要差异包括：
- **强制静态类型**：禁止使用 `any` 和 `unknown` 类型
- **禁止运行时变更对象布局**：不允许动态添加或删除属性
- **使用 `let` 而非 `var`**：变量声明必须使用 `let` 或 `const`
- **使用 class 而非 function**：不支持通过 function 构造器创建类

---

## 基本知识

### 程序入口

ArkTS 程序从 `main` 函数开始执行：

```typescript
function main(): void {
  console.log('Hello, World!')
}
```

### 打印输出

使用 `console.log` 进行标准输出：

```typescript
console.log('Print a message')
console.log('Value:', 42)
```

### 变量声明

使用 `let` 声明可变变量，使用 `const` 声明不可变常量：

```typescript
let message: string = 'Hello'
const MAX_COUNT: number = 100
```

---

## 声明

### 变量声明

ArkTS 中使用 `let` 和 `const` 声明变量，**禁止使用 `var`**：

```typescript
let name: string = 'ArkTS'
const PI: number = 3.14159

// 禁止使用 var
// var x = 10  // 编译错误
```

`const` 声明的变量必须在声明时初始化，且之后不可重新赋值：

```typescript
const VERSION: string = '1.0.0'
// VERSION = '2.0.0'  // 编译错误

let count: number = 0
count = 1  // 正确，let 声明的变量可以重新赋值
```

---

## 类型

### 基本类型

#### number

ArkTS 中所有数字均为 `number` 类型，不区分整数和浮点数：

```typescript
let integer: number = 42
let float: number = 3.14
let hex: number = 0xFF
let binary: number = 0b1010
let octal: number = 0o744
```

#### string

```typescript
let greeting: string = 'Hello'
let name: string = "ArkTS"
let template: string = `Hello, ${name}!`
```

#### boolean

```typescript
let isActive: boolean = true
let isComplete: boolean = false
```

#### void

`void` 用于表示函数没有返回值：

```typescript
function logMessage(msg: string): void {
  console.log(msg)
}
```

#### Object

`Object` 是所有类的基类：

```typescript
let obj: Object = new Object()
```

#### Array

数组使用 `Array<T>` 或 `T[]` 语法：

```typescript
let numbers: number[] = [1, 2, 3, 4, 5]
let names: Array<string> = ['Alice', 'Bob', 'Charlie']

// 通过索引访问
let first: number = numbers[0]

// 修改元素
numbers[0] = 10
```

#### enum

枚举用于定义一组命名常量：

```typescript
enum Direction {
  Up,
  Down,
  Left,
  Right
}

let dir: Direction = Direction.Up
```

#### union（联合类型）

联合类型表示一个值可以是几种类型之一：

```typescript
type StringOrNumber = string | number

let value: StringOrNumber = 'hello'
value = 42
```

#### 类型别名

使用 `type` 关键字为类型创建别名：

```typescript
type UserID = string
type Point = { x: number; y: number }

let uid: UserID = 'user_001'
let p: Point = { x: 10, y: 20 }
```

#### 字面量类型

字面量类型允许指定更精确的值：

```typescript
type Status = 'active' | 'inactive' | 'pending'

let currentStatus: Status = 'active'

type Digit = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
let d: Digit = 5
```

---

## 运算符

### 赋值运算符

```typescript
let a: number = 10
a += 5   // a = 15
a -= 3   // a = 12
a *= 2   // a = 24
a /= 4   // a = 6
a %= 4   // a = 2
```

### 比较运算符

```typescript
let x: number = 10
let y: number = 20

let eq: boolean = x === y    // 严格相等
let neq: boolean = x !== y   // 严格不等
let gt: boolean = x > y      // 大于
let lt: boolean = x < y      // 小于
let gte: boolean = x >= y    // 大于等于
let lte: boolean = x <= y    // 小于等于
```

### 算术运算符

```typescript
let a: number = 10
let b: number = 3

let sum: number = a + b      // 13
let diff: number = a - b     // 7
let product: number = a * b  // 30
let quotient: number = a / b // 3.333...
let remainder: number = a % b // 1
```

### 逻辑运算符

```typescript
let t: boolean = true
let f: boolean = false

let and: boolean = t && f  // false
let or: boolean = t || f   // true
let not: boolean = !t      // false
```

### 位运算符

```typescript
let a: number = 5   // 0101
let b: number = 3   // 0011

let and: number = a & b    // 0001 = 1
let or: number = a | b     // 0111 = 7
let xor: number = a ^ b    // 0110 = 6
let not: number = ~a       // 按位取反
let left: number = a << 1  // 1010 = 10
let right: number = a >> 1 // 0010 = 2
```

### 一元运算符

```typescript
let a: number = 5

let positive: number = +a   // 5（一元加法，仅用于数字）
let negative: number = -a   // -5
let incremented: number = ++a  // 6
let decremented: number = --a  // 5
```

### 条件（三元）运算符

```typescript
let age: number = 20
let category: string = age >= 18 ? 'adult' : 'minor'
```

### 类型运算符

使用 `instanceof` 检查对象是否为某个类的实例：

```typescript
class Animal {}
class Dog extends Animal {}

let dog: Dog = new Dog()
let isAnimal: boolean = dog instanceof Animal  // true
```

### 逗号运算符

```typescript
let a: number = 0
let b: number = (a++, a + 1)  // a = 1, b = 2
```

---

## 语句

### if 语句

```typescript
let score: number = 85

if (score >= 90) {
  console.log('优秀')
} else if (score >= 80) {
  console.log('良好')
} else if (score >= 60) {
  console.log('及格')
} else {
  console.log('不及格')
}
```

### switch 语句

```typescript
enum Color { Red, Green, Blue }

let color: Color = Color.Green

switch (color) {
  case Color.Red:
    console.log('红色')
    break
  case Color.Green:
    console.log('绿色')
    break
  case Color.Blue:
    console.log('蓝色')
    break
  default:
    console.log('未知颜色')
    break
}
```

### 条件表达式

```typescript
let x: number = 10
let y: number = 20
let max: number = x > y ? x : y  // 20
```

### for 循环

```typescript
let sum: number = 0
for (let i: number = 0; i < 10; i++) {
  sum += i
}
console.log(`Sum: ${sum}`)  // Sum: 45
```

### for-of 循环

```typescript
let fruits: string[] = ['apple', 'banana', 'cherry']
for (let fruit of fruits) {
  console.log(fruit)
}
```

### while 循环

```typescript
let count: number = 0
while (count < 5) {
  console.log(`Count: ${count}`)
  count++
}
```

### do-while 循环

```typescript
let num: number = 0
do {
  console.log(`Number: ${num}`)
  num++
} while (num < 3)
```

### break 语句

```typescript
for (let i: number = 0; i < 10; i++) {
  if (i === 5) {
    break  // 跳出循环
  }
  console.log(i)  // 输出 0, 1, 2, 3, 4
}
```

### continue 语句

```typescript
for (let i: number = 0; i < 10; i++) {
  if (i % 2 === 0) {
    continue  // 跳过偶数
  }
  console.log(i)  // 输出 1, 3, 5, 7, 9
}
```

### throw 语句

```typescript
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('Division by zero')
  }
  return a / b
}
```

### try-catch-finally 语句

```typescript
try {
  let result: number = divide(10, 0)
} catch (e) {
  console.log(`Error: ${(e as Error).message}`)
} finally {
  console.log('Cleanup')
}
```

---

## 函数

### 函数声明

```typescript
function add(a: number, b: number): number {
  return a + b
}
```

### 可选参数

使用 `?` 标记可选参数，可选参数必须位于必选参数之后：

```typescript
function greet(name: string, greeting?: string): string {
  if (greeting) {
    return `${greeting}, ${name}!`
  }
  return `Hello, ${name}!`
}

console.log(greet('Alice'))           // Hello, Alice!
console.log(greet('Alice', 'Hi'))     // Hi, Alice!
```

### rest 参数

使用 `...` 语法声明 rest 参数，rest 参数必须是函数的最后一个参数：

```typescript
function sum(...numbers: number[]): number {
  let total: number = 0
  for (let num of numbers) {
    total += num
  }
  return total
}

console.log(sum(1, 2, 3))      // 6
console.log(sum(1, 2, 3, 4))   // 10
```

### 返回类型

函数可以显式声明返回类型。如果没有返回值，使用 `void`：

```typescript
function multiply(a: number, b: number): number {
  return a * b
}

function log(msg: string): void {
  console.log(msg)
}
```

### 作用域

ArkTS 使用词法作用域（静态作用域），内层函数可以访问外层函数的变量：

```typescript
function outer(): void {
  let outerVar: string = 'outer'

  function inner(): void {
    console.log(outerVar)  // 可以访问外层变量
  }

  inner()
}
```

### 函数调用

```typescript
function add(a: number, b: number): number {
  return a + b
}

let result: number = add(3, 5)  // 8
```

### 函数类型

可以将函数类型赋值给变量：

```typescript
type MathOp = (a: number, b: number) => number

let add: MathOp = (a: number, b: number): number => a + b
let subtract: MathOp = (a: number, b: number): number => a - b

console.log(add(10, 5))       // 15
console.log(subtract(10, 5))  // 5
```

### 箭头函数

箭头函数提供简洁的函数定义方式：

```typescript
let double = (x: number): number => x * 2
let add = (a: number, b: number): number => a + b

// 多行箭头函数
let greet = (name: string): string => {
  let message: string = `Hello, ${name}!`
  return message
}
```

### 闭包

闭包是指函数与其词法环境的组合。内部函数可以访问外部函数的变量，即使外部函数已经返回：

```typescript
function makeCounter(): () => number {
  let count: number = 0
  return (): number => {
    count++
    return count
  }
}

let counter = makeCounter()
console.log(counter())  // 1
console.log(counter())  // 2
console.log(counter())  // 3
```

---

## 类

### 定义类

```typescript
class Person {
  name: string = ''
  age: number = 0
}
```

### 字段

类的字段可以在声明时初始化，也可以在构造函数中初始化：

```typescript
class Person {
  name: string = ''
  age: number = 0
  email: string = ''
}
```

### 方法

```typescript
class Person {
  name: string = ''
  age: number = 0

  greet(): string {
    return `Hello, my name is ${this.name}.`
  }
}
```

### 构造函数

使用 `constructor` 定义构造函数：

```typescript
class Person {
  name: string
  age: number

  constructor(name: string, age: number) {
    this.name = name
    this.age = age
  }

  greet(): string {
    return `Hello, my name is ${this.name}, I'm ${this.age} years old.`
  }
}

let person = new Person('Alice', 30)
console.log(person.greet())
```

### 继承

使用 `extends` 实现类的继承：

```typescript
class Animal {
  name: string = ''

  speak(): string {
    return `${this.name} makes a sound.`
  }
}

class Dog extends Animal {
  breed: string = ''

  speak(): string {
    return `${this.name} barks.`
  }
}

let dog = new Dog()
dog.name = 'Buddy'
dog.breed = 'Golden Retriever'
console.log(dog.speak())  // Buddy barks.
```

### 重写

子类可以使用 `override` 关键字重写父类方法：

```typescript
class Shape {
  area(): number {
    return 0
  }
}

class Circle extends Shape {
  radius: number = 0

  override area(): number {
    return Math.PI * this.radius * this.radius
  }
}

class Rectangle extends Shape {
  width: number = 0
  height: number = 0

  override area(): number {
    return this.width * this.height
  }
}
```

### 对象字面量

ArkTS 中对象字面量必须对应一个显式声明的类或接口：

```typescript
class Point {
  x: number = 0
  y: number = 0
}

let p: Point = { x: 10, y: 20 }

interface Config {
  host: string
  port: number
}

let config: Config = { host: 'localhost', port: 8080 }
```

---

## 接口

### 定义接口

```typescript
interface Person {
  name: string
  age: number
  greet(): string
}
```

### 实现接口

使用 `implements` 关键字实现接口：

```typescript
interface Printable {
  print(): void
}

class Document implements Printable {
  content: string = ''

  print(): void {
    console.log(this.content)
  }
}
```

### 扩展接口

使用 `extends` 扩展接口：

```typescript
interface Animal {
  name: string
}

interface Pet extends Animal {
  owner: string
}

class Dog implements Pet {
  name: string = ''
  owner: string = ''
}
```

---

## 泛型

### 泛型函数

```typescript
function identity<T>(value: T): T {
  return value
}

let num: number = identity<number>(42)
let str: string = identity<string>('hello')
```

### 泛型类

```typescript
class Stack<T> {
  private items: T[] = []

  push(item: T): void {
    this.items.push(item)
  }

  pop(): T | undefined {
    return this.items.pop()
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1]
  }

  size(): number {
    return this.items.length
  }
}

let numberStack = new Stack<number>()
numberStack.push(1)
numberStack.push(2)
console.log(numberStack.pop())  // 2
```

### 泛型约束

使用 `extends` 对泛型参数进行约束：

```typescript
interface HasLength {
  length: number
}

function logLength<T extends HasLength>(value: T): void {
  console.log(value.length)
}

logLength('hello')      // 5
logLength([1, 2, 3])    // 3

// logLength(123)       // 编译错误：number 没有 length 属性
```

---

## 枚举

### 数字枚举

```typescript
enum Direction {
  Up,      // 0
  Down,    // 1
  Left,    // 2
  Right    // 3
}

let dir: Direction = Direction.Up
console.log(dir)  // 0

// 可以指定起始值
enum Status {
  Active = 1,
  Inactive,  // 2
  Pending    // 3
}
```

### 字符串枚举

```typescript
enum FileType {
  Text = 'text',
  Image = 'image',
  Video = 'video',
  Audio = 'audio'
}

let type: FileType = FileType.Image
console.log(type)  // "image"
```

---

## 模块

### 导出

使用 `export` 关键字导出模块成员：

```typescript
// utils.ets
export function add(a: number, b: number): number {
  return a + b
}

export const PI: number = 3.14159

export class Calculator {
  static multiply(a: number, b: number): number {
    return a * b
  }
}
```

### 导入

使用 `import` 关键字导入模块成员：

```typescript
// main.ets
import { add, PI, Calculator } from './utils'

console.log(add(1, 2))              // 3
console.log(PI)                      // 3.14159
console.log(Calculator.multiply(3, 4))  // 12
```

也可以使用 `* as` 导入整个模块：

```typescript
import * as utils from './utils'

console.log(utils.add(1, 2))
console.log(utils.PI)
```

---

## 顶层语句

ArkTS 支持顶层语句，即不需要包裹在函数中的语句：

```typescript
// 顶层语句
let message: string = 'Hello, ArkTS!'
console.log(message)

// 顶层表达式
let x: number = 10 + 20
```

---

## 空安全

### 可空类型

使用 `| null` 表示可空类型：

```typescript
let name: string | null = null
name = 'Alice'

let age: number | null = null
age = 30
```

### 非空断言

使用 `!` 操作符对可空值进行非空断言。当确定值不为 null 时使用：

```typescript
let name: string | null = 'Alice'
let length: number = name!.length  // 非空断言

// 注意：如果值为 null，非空断言会导致运行时错误
let empty: string | null = null
// empty!.length  // 运行时崩溃
```

### 可选链

使用 `?.` 进行安全的属性访问。如果对象为 null 或 undefined，表达式短路返回 undefined：

```typescript
interface Address {
  city: string
  street: string
}

interface User {
  name: string
  address?: Address
}

let user: User = { name: 'Alice' }
let city: string | undefined = user.address?.city  // undefined

user.address = { city: 'Beijing', street: 'Chaoyang' }
let city2: string | undefined = user.address?.city  // 'Beijing'
```

### 空值合并

使用 `??` 运算符为 null 或 undefined 提供默认值：

```typescript
let name: string | null = null
let displayName: string = name ?? 'Anonymous'  // 'Anonymous'

let count: number | null = 0
let displayCount: number = count ?? 1  // 0（0 不是 null/undefined，所以保留原值）
```

结合可选链和空值合并：

```typescript
interface Config {
  timeout?: number
}

let config: Config = {}
let timeout: number = config.timeout ?? 3000  // 3000
```
