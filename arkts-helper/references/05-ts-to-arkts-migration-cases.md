# ArkTS 适配指导案例

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-more-cases
> **抓取时间**: 2026-06-18

本文档提供 ArkTS 适配过程中常见问题的具体案例，每个案例包含问题描述、不合规代码和合规代码。

---

## arkts-identifiers-as-prop-names

### 问题描述

ArkTS 要求对象属性名必须是合法的标识符，不支持使用字符串字面量作为属性名（如包含连字符、数字开头或保留字的属性名）。

### 不合规代码

```typescript
let obj = {
  'my-prop': 'value',
  '123abc': 'value',
  'class': 'value'
}
```

### 合规代码

```typescript
class Config {
  myProp: string = ''
  abc123: string = ''
  category: string = ''
}

let config = new Config()
config.myProp = 'value'
config.abc123 = 'value'
config.category = 'value'
```

---

## arkts-no-any-unknown

### 案例 1：将 any/unknown 改为具体类型

#### 问题描述

使用 `any` 或 `unknown` 类型会绕过类型检查，导致运行时错误。

#### 不合规代码

```typescript
let data: any = fetchData()
let name: string = data.name
let age: number = data.age

function process(input: any): any {
  return input.toString()
}
```

#### 合规代码

```typescript
class UserInfo {
  name: string = ''
  age: number = 0
}

let data: UserInfo = fetchData()
let name: string = data.name
let age: number = data.age

function process(input: string): string {
  return input.toString()
}
```

### 案例 2：JSON.parse 返回值类型标注

#### 问题描述

`JSON.parse` 默认返回 `any` 类型，在 ArkTS 中需要为其提供明确的类型标注。

#### 不合规代码

```typescript
let data = JSON.parse('{"name":"Alice","age":30}')
console.log(data.name)
```

#### 合规代码

```typescript
interface UserData {
  name: string
  age: number
}

let data: Record<string, Object> = JSON.parse('{"name":"Alice","age":30}') as Record<string, Object>
let name: string = data['name'] as string
let age: number = data['age'] as number

// 或定义具体类
class UserInfo {
  name: string = ''
  age: number = 0

  static fromJson(json: string): UserInfo {
    let data: Record<string, Object> = JSON.parse(json) as Record<string, Object>
    let user = new UserInfo()
    user.name = data['name'] as string
    user.age = data['age'] as number
    return user
  }
}

let user: UserInfo = UserInfo.fromJson('{"name":"Alice","age":30}')
```

### 案例 3：使用 Record 类型替代索引签名

#### 问题描述

当需要键值对结构时，不能使用 `any` 或索引签名，应使用 `Record` 类型。

#### 不合规代码

```typescript
let headers: any = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer token'
}

function getHeader(key: string): any {
  return headers[key]
}
```

#### 合规代码

```typescript
let headers: Record<string, string> = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer token'
}

function getHeader(key: string): string {
  return headers[key]
}
```

---

## arkts-no-call-signature

### 问题描述

ArkTS 不支持在接口中定义调用签名（call signature），即不能将接口定义为可调用的函数类型。

### 不合规代码

```typescript
interface Greeter {
  (name: string): string
  greeting: string
}

let greeter: Greeter = (() => 'Hello') as Greeter
greeter.greeting = 'Hi'
console.log(greeter('Alice'))
```

### 合规代码

```typescript
class Greeter {
  greeting: string = ''

  call(name: string): string {
    return `${this.greeting}, ${name}!`
  }
}

let greeter = new Greeter()
greeter.greeting = 'Hi'
console.log(greeter.call('Alice'))
```

---

## arkts-no-ctor-signatures-type

### 问题描述

ArkTS 不支持使用构造签名类型（constructor signature type），即不能在类型中使用 `new` 签名。

### 不合规代码

```typescript
type Constructor = new (name: string) => Person

function createInstance(ctor: Constructor, name: string): Person {
  return new ctor(name)
}
```

### 合规代码

```typescript
class Person {
  name: string = ''
  constructor(name: string) {
    this.name = name
  }
}

function createInstance(name: string): Person {
  return new Person(name)
}

// 如果需要支持多种类型创建，使用工厂模式
interface Factory {
  create(name: string): Person
}

class PersonFactory implements Factory {
  create(name: string): Person {
    return new Person(name)
  }
}
```

---

## arkts-no-indexed-signatures

### 问题描述

ArkTS 不支持索引签名（indexed signature），即不能使用 `[key: type]: type` 语法定义动态属性。

### 不合规代码

```typescript
interface Dictionary {
  [key: string]: string
}

let dict: Dictionary = {}
dict['hello'] = 'world'
```

### 合规代码

```typescript
// 方案 1：使用 Record 类型
let dict: Record<string, string> = {}
dict['hello'] = 'world'

// 方案 2：使用类定义固定属性
class Dictionary {
  hello: string = ''
  world: string = ''
}

let d = new Dictionary()
d.hello = 'world'

// 方案 3：使用 Map
let map: Map<string, string> = new Map()
map.set('hello', 'world')
```

---

## arkts-no-typing-with-this

### 问题描述

ArkTS 不支持在类型标注中使用 `this` 类型，包括返回值类型为 `this` 的情况。

### 不合规代码

```typescript
class Builder {
  name: string = ''

  setName(name: string): this {
    this.name = name
    return this
  }

  build(): this {
    return this
  }
}
```

### 合规代码

```typescript
class Builder {
  name: string = ''

  setName(name: string): Builder {
    this.name = name
    return this
  }

  build(): Builder {
    return this
  }
}
```

对于链式调用场景，如果子类需要返回自身类型，使用泛型：

```typescript
class Builder<T extends Builder<T>> {
  name: string = ''

  setName(name: string): T {
    this.name = name
    return this as T
  }
}

class ConcreteBuilder extends Builder<ConcreteBuilder> {
  value: number = 0

  setValue(value: number): ConcreteBuilder {
    this.value = value
    return this
  }
}
```

---

## arkts-no-ctor-prop-decls

### 问题描述

ArkTS 不支持在构造函数参数中直接声明属性（constructor parameter properties），即不能在构造函数参数前加修饰符来自动声明和初始化类属性。

### 不合规代码

```typescript
class Person {
  constructor(public name: string, private age: number) {}
}
```

### 合规代码

```typescript
class Person {
  public name: string
  private age: number

  constructor(name: string, age: number) {
    this.name = name
    this.age = age
  }
}
```

---

## arkts-no-ctor-signatures-iface

### 问题描述

ArkTS 不支持在接口中定义构造签名。

### 不合规代码

```typescript
interface IFactory {
  new (type: string): Product
}

function createProduct(factory: IFactory, type: string): Product {
  return new factory(type)
}
```

### 合规代码

```typescript
class Product {
  type: string = ''
  constructor(type: string) {
    this.type = type
  }
}

// 使用工厂函数
function createProduct(type: string): Product {
  return new Product(type)
}

// 或使用抽象工厂模式
interface ProductFactory {
  create(type: string): Product
}

class DefaultProductFactory implements ProductFactory {
  create(type: string): Product {
    return new Product(type)
  }
}
```

---

## 其他常见适配案例

### 案例 1：对象字面量必须对应显式声明的类或接口

#### 不合规代码

```typescript
let point = { x: 10, y: 20 }
let config = { host: 'localhost', port: 8080 }

function printPoint(p: { x: number; y: number }): void {
  console.log(`(${p.x}, ${p.y})`)
}
```

#### 合规代码

```typescript
class Point {
  x: number = 0
  y: number = 0
}

class Config {
  host: string = ''
  port: number = 0
}

let point = new Point()
point.x = 10
point.y = 20

let config = new Config()
config.host = 'localhost'
config.port = 8080

function printPoint(p: Point): void {
  console.log(`(${p.x}, ${p.y})`)
}
```

### 案例 2：禁止使用函数重载

#### 不合规代码

```typescript
function render(content: string): void
function render(content: string, style: string): void
function render(content: string, style?: string): void {
  if (style) {
    console.log(`Render: ${content} with ${style}`)
  } else {
    console.log(`Render: ${content}`)
  }
}
```

#### 合规代码

```typescript
function render(content: string, style?: string): void {
  if (style !== undefined) {
    console.log(`Render: ${content} with ${style}`)
  } else {
    console.log(`Render: ${content}`)
  }
}
```

### 案例 3：禁止使用 in 运算符

#### 不合规代码

```typescript
interface Dog {
  bark(): void
}

interface Cat {
  meow(): void
}

function speak(animal: Dog | Cat): void {
  if ('bark' in animal) {
    animal.bark()
  } else {
    animal.meow()
  }
}
```

#### 合规代码

```typescript
class Dog {
  bark(): void {
    console.log('Woof!')
  }
}

class Cat {
  meow(): void {
    console.log('Meow!')
  }
}

function speak(animal: Dog | Cat): void {
  if (animal instanceof Dog) {
    animal.bark()
  } else {
    animal.meow()
  }
}
```

### 案例 4：数组类型适配

#### 不合规代码

```typescript
let arr: any[] = [1, 'hello', true]
let first: any = arr[0]
```

#### 合规代码

```typescript
// 同类型数组
let numbers: number[] = [1, 2, 3]
let strings: string[] = ['hello', 'world']

// 需要混合类型时使用联合类型
let mixed: (number | string)[] = [1, 'hello']
```

### 案例 5：Promise 类型适配

#### 不合规代码

```typescript
async function fetchData(): Promise<any> {
  let response = await fetch('/api/data')
  return response.json()
}
```

#### 合规代码

```typescript
class ApiData {
  id: number = 0
  name: string = ''
}

async function fetchData(): Promise<ApiData> {
  let response = await fetch('/api/data')
  let json: Record<string, Object> = await response.json() as Record<string, Object>
  let data = new ApiData()
  data.id = json['id'] as number
  data.name = json['name'] as string
  return data
}
```

### 案例 6：事件回调类型适配

#### 不合规代码

```typescript
let callbacks: { [key: string]: Function } = {}

function on(event: string, callback: Function): void {
  callbacks[event] = callback
}
```

#### 合规代码

```typescript
type EventCallback = (data: string) => void

let callbacks: Record<string, EventCallback> = {}

function on(event: string, callback: EventCallback): void {
  callbacks[event] = callback
}
```

### 案例 7：泛型约束适配

#### 不合规代码

```typescript
function getProperty(obj: any, key: string): any {
  return obj[key]
}
```

#### 合规代码

```typescript
function getProperty<T>(obj: T, key: keyof T): T[keyof T] {
  return obj[key]
}

// 或使用更明确的约束
interface HasId {
  id: number
}

function getId<T extends HasId>(obj: T): number {
  return obj.id
}
```

### 案例 8：禁止使用 as const 断言

#### 不�述规代码

```typescript
const config = {
  host: 'localhost',
  port: 8080
} as const
```

#### 合规代码

```typescript
class Config {
  readonly host: string = 'localhost'
  readonly port: number = 8080
}

const config = new Config()
```

### 案例 9：禁止使用命名空间合并

#### 不合规代码

```typescript
namespace Utils {
  export function helper(): void {}
}

namespace Utils {
  export function anotherHelper(): void {}
}
```

#### 合规代码

```typescript
namespace Utils {
  export function helper(): void {}
  export function anotherHelper(): void {}
}
```

### 案例 10：禁止使用枚举的异构成员

#### 不合规代码

```typescript
enum Mixed {
  Name = 'Alice',
  Age = 30
}
```

#### 合规代码

```typescript
// 使用纯字符串枚举
enum StringEnum {
  Name = 'Alice'
}

// 使用纯数字枚举
enum NumberEnum {
  Age = 30
}

// 需要混合类型时使用类
class UserInfo {
  name: string = 'Alice'
  age: number = 30
}
```
