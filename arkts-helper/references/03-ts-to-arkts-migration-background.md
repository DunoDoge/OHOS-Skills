# ArkTS 语法适配背景

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-migration-background
> **抓取时间**: 2026-06-18

ArkTS 在 TypeScript（TS）的基础上进行了语法规范约束，这些约束旨在提升程序的稳定性和性能。本文档介绍 ArkTS 语法适配的背景和动机。

---

## 程序稳定性

### 静态类型提升稳定性

TypeScript 的类型系统是可选的（optional typing），开发者可以随时使用 `any` 类型绕过类型检查，也可以在运行时动态添加或删除对象属性。这种灵活性虽然降低了编码门槛，但也带来了以下问题：

1. **运行时类型错误**：使用 `any` 类型会导致编译期无法发现的类型错误，这些错误只能在运行时暴露，增加了程序崩溃的风险。
2. **动态属性访问**：运行时动态添加或删除对象属性会导致对象布局不确定，使得代码行为难以预测。
3. **隐式类型转换**：TS/JS 中的隐式类型转换（如 `+` 运算符既可以用于数字加法，也可以用于字符串拼接）容易引入难以发现的 Bug。

ArkTS 通过强制静态类型解决了这些问题：

```typescript
// TypeScript - 可能导致运行时错误
let data: any = fetchData()
data.nonExistentMethod()  // 编译通过，运行时崩溃

// ArkTS - 编译期发现错误
let data: UserInfo = fetchData()
data.nonExistentMethod()  // 编译错误：属性不存在
```

### 禁止运行时变更对象布局

ArkTS 禁止在运行时动态添加或删除对象属性，确保对象布局在编译期确定：

```typescript
// TypeScript - 允许动态添加属性
let obj: any = {}
obj.newProp = 'value'  // 运行时添加属性

// ArkTS - 禁止动态添加属性
class Config {
  host: string = ''
  port: number = 0
}
let config = new Config()
// config.newProp = 'value'  // 编译错误
```

---

## 程序性能

### 静态类型优化执行性能

静态类型信息使编译器能够进行更激进的优化：

1. **内联缓存（Inline Cache）**：当对象布局固定时，运行时可以缓存属性访问的偏移量，避免每次访问都进行字典查找。
2. **类型特化**：编译器可以根据类型信息生成针对特定类型的优化代码，避免通用代码中的类型检查开销。
3. **提前编译（AOT）**：静态类型信息使 AOT 编译成为可能，可以将高级语言直接编译为机器码，避免解释执行和 JIT 编译的启动开销。

```typescript
// 静态类型使编译器可以进行优化
class Point {
  x: number = 0
  y: number = 0
}

function distance(p1: Point, p2: Point): number {
  let dx: number = p2.x - p1.x
  let dy: number = p2.y - p1.y
  return Math.sqrt(dx * dx + dy * dy)
}
```

### 避免运行时类型检查开销

在动态类型系统中，每次操作都可能需要运行时类型检查。ArkTS 的静态类型消除了大部分运行时类型检查：

```typescript
// TypeScript - 运行时需要类型检查
function add(a: any, b: any): any {
  return a + b  // 运行时需要判断 a 和 b 的类型
}

// ArkTS - 编译期确定类型，无需运行时检查
function add(a: number, b: number): number {
  return a + b  // 直接执行数值加法
}
```

---

## .ets 代码兼容性

ArkTS 代码以 `.ets` 为文件扩展名。`.ets` 文件完全兼容 `.ts` 文件的语法，但增加了以下约束：

1. **强制静态类型**：所有变量、参数和返回值必须有明确的类型标注。
2. **禁止 `any` 和 `unknown`**：不允许使用 `any` 和 `unknown` 类型。
3. **禁止 `var`**：变量声明必须使用 `let` 或 `const`。
4. **禁止运行时变更对象布局**：不允许动态添加或删除对象属性。

这些约束确保了 `.ets` 代码在编译期就能捕获尽可能多的错误，同时为运行时优化提供了必要的信息。

```typescript
// .ets 文件中的代码
class User {
  name: string = ''
  age: number = 0
}

function createUser(name: string, age: number): User {
  let user = new User()
  user.name = name
  user.age = age
  return user
}
```

---

## 支持与 TS/JS 的交互

ArkTS 支持与 TypeScript 和 JavaScript 的互操作，允许在项目中混合使用 `.ets`、`.ts` 和 `.js` 文件：

1. **导入 JS/TS 模块**：ArkTS 代码可以导入 `.ts` 和 `.js` 文件导出的模块。
2. **类型声明文件**：通过 `.d.ts` 文件为 JS 模块提供类型信息。
3. **跨语言调用**：ArkTS 可以调用 JS/TS 中定义的函数和类。

```typescript
// 在 .ets 文件中导入 .ts 模块
import { utilityFunction } from './utils'  // utils.ts

// 使用导入的函数
let result: string = utilityFunction('input')
```

### 交互注意事项

- 从 JS/TS 模块导入的值在 ArkTS 中可能被视为 `any` 类型，需要进行适当的类型标注。
- ArkTS 代码导出的接口和类可以被 TS/JS 代码正常使用。
- 建议为 JS 模块提供 `.d.ts` 类型声明文件，以确保类型安全。

---

## 方舟运行时兼容 TS/JS

方舟运行时（Ark Runtime）是 HarmonyOS 的 JavaScript/TypeScript 运行时环境，它完全兼容 TS/JS 的标准语义：

1. **ECMAScript 标准兼容**：方舟运行时支持 ECMAScript 标准，TS/JS 代码可以在方舟运行时上正常运行。
2. **TypeScript 支持**：方舟运行时支持 TypeScript 的类型系统，包括泛型、枚举、装饰器等特性。
3. **性能优化**：方舟运行时针对 ArkTS 的静态类型特性进行了优化，包括 AOT 编译、内联缓存等。

### 运行时架构

```
┌─────────────────────────────────────┐
│           ArkTS Application         │
├─────────────────────────────────────┤
│           ArkTS Compiler            │
│    (静态类型检查 + AOT 编译)         │
├─────────────────────────────────────┤
│           Ark Runtime               │
│  (方舟运行时，兼容 TS/JS 标准语义)    │
├─────────────────────────────────────┤
│           Operating System          │
│         (HarmonyOS Kernel)          │
└─────────────────────────────────────┘
```

### 兼容性保证

- 方舟运行时确保现有的 TS/JS 代码无需修改即可运行。
- ArkTS 代码经过编译器约束后，可以在方舟运行时上获得更好的性能。
- 方舟运行时同时支持解释执行和 AOT 编译执行两种模式，开发者可以根据需要选择。
