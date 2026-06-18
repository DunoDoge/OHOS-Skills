---
name: arkts-helper
description: Use when writing, reviewing, or migrating ArkTS code for HarmonyOS / OpenHarmony app development. Triggers include ArkTS syntax, ArkTS type system, ArkTS class/interface/generics, ArkTS coding style, ArkTS language features, TypeScript to ArkTS migration, ArkTS performance optimization, ArkTS standard library, ArkTS concurrency, Promise, async/await, TaskPool, Worker, Sendable, ArkTS container classes, XML/Buffer/JSON, or any topic under the HarmonyOS ArkTS language documentation. Loads the offline ArkTS language reference set so the agent can give accurate ArkTS guidance instead of guessing from TypeScript knowledge.
---

# arkts-helper

ArkTS 是 HarmonyOS 应用开发的官方高级语言，在 TypeScript（TS）生态基础上做了扩展和约束：

- **强制静态类型**：所有变量必须声明类型，不支持 `any`/`unknown`，编译器在开发期进行更严格的类型检查。
- **禁止运行时改变对象布局**：不允许动态添加/删除对象属性，对象结构在编译期确定。
- **限制运算符语义**：一元加法运算符 `+` 仅能作用于数字，不能用于字符串转数字等场景。
- **不支持 Structural typing**：类型兼容性基于名义类型（nominal typing），不支持结构化类型。
- **使用 `let` 而非 `var`**：ArkTS 中必须使用 `let` 声明变量，不支持 `var`。

Agent 凭通用 TypeScript 经验写出的代码，在 HarmonyOS 上**极易编译失败或性能不达标**。本 skill 提供的离线参考文档（`references/` 下 12 篇 + INDEX）是华为官方「ArkTS 语言」系列文档的离线副本，是处理 ArkTS 语法/迁移/性能/基础类库任务时的**权威依据**。

## 何时启用本 skill

满足以下任一条件就应当遵循本 skill 的工作流程：

- 用户要求**编写或审查 ArkTS 代码**（语法、类型系统、类/接口/泛型/枚举）
- 用户要求**将 TypeScript 代码迁移到 ArkTS**（适配规则、适配案例）
- 用户要求**优化 ArkTS 代码性能**（高性能编程实践）
- 用户要求**使用 ArkTS 基础类库**（XML/Buffer/JSON/容器类库）
- 用户要求**ArkTS 并发编程**（Promise/async-await/TaskPool/Worker/Sendable）
- 用户询问 **ArkTS 与 TypeScript 的差异**
- 用户要求**ArkTS 编程规范**（命名、代码格式、注释）
- 用户提到 `arkts-no-*` 规则但需要了解语法规范而非修复报错
- 用户提到 ArkTS 语言特性（`@Concurrent`、Sendable、容器类等）

不要在「ArkTS 编译报错修复」「NDK/C++ 互操作」「命令行构建/部署」场景下强行套用本 skill；这些场景请使用对应 skill（见下文边界）。

## 与已有 skill 的边界

本 skill 负责**「ArkTS 语言语法与规范指导」**，不负责**「编译报错怎么修」「NDK 代码怎么写」「构建命令怎么调」**。当 ArkTS 开发任务中遇到以下问题时，应交叉引用对应 skill：

| 问题类型 | 交叉引用 skill | 边界说明 |
| --- | --- | --- |
| ArkTS 编译报错（`arkts-no-*` 规则等） | `arkts-debug` | 本 skill 讲「如何写合规代码」，`arkts-debug` 讲「报错后如何修复」 |
| NDK / C++ / Node-API 互操作 | `arkts-ndk-dev` | 本 skill 仅提供跨语言交互概览；Node-API 详细开发归 `arkts-ndk-dev` |
| 命令行构建/部署/签名/流水线 | `arkts-build` | 本 skill 不覆盖构建命令 |

## 工作流程（严格遵守）

### 1. 先读索引，再决定看哪份文档

任何 ArkTS 语法/迁移/性能任务开始前，**必须先读** `references/INDEX.md`。它给出 12 份文档的角色、按场景的查阅路径以及关键差异速记，能避免你把整个 reference 目录全文读进上下文。

### 2. 按任务类型加载对应文档

| 任务类型 | 必读文件（在 `references/` 下） |
| -------- | ------------------------------ |
| ArkTS 语法（声明/类型/运算符/语句/函数/类/接口/泛型/枚举） | `01-arkts-language-introduction.md` |
| ArkTS 编程规范 | `02-arkts-coding-style.md` |
| TS→ArkTS 适配背景 | `03-ts-to-arkts-migration-background.md` |
| **TS→ArkTS 适配规则** | `04-ts-to-arkts-migration-rules.md` |
| TS→ArkTS 适配案例 | `05-ts-to-arkts-migration-cases.md` |
| **ArkTS 高性能编程** | `06-arkts-high-performance.md` |
| ArkTS 基础类库概述 | `07-arkts-stdlib-overview.md` |
| XML/Buffer/JSON 扩展库 | `08-arkts-xml-buffer-json.md` |
| ArkTS 容器类库 | `09-arkts-container-library.md` |
| 异步并发（Promise/async-await） | `10-arkts-concurrency-async.md` |
| **多线程并发（TaskPool/Worker/Sendable）** | `11-arkts-concurrency-multithread.md` |
| 跨语言交互概览 | `12-arkts-cross-language-overview.md` |

读取文档时优先用 `Grep`/`Read` 的 offset/limit 定位段落，不要把大文件一次性读全。

### 3. 落到代码时严格执行红线

写出 / 修改 ArkTS 代码前自检以下高频红线（详细规则以文档原文为准）：

**TS→ArkTS 差异红线**：
- **禁止 `any`/`unknown`**：必须使用具体类型
- **禁止运行时改变对象布局**：不能动态添加/删除属性
- **禁止 `as` 类型断言**：使用显式类型声明
- **一元 `+` 仅用于数字**：字符串转数字用 `Number()` 或 `parseInt()`
- **使用 `let` 而非 `var`**：ArkTS 不支持 `var`
- **对象字面量必须对应已声明的类或接口**：不能使用匿名对象类型

**高性能编程红线**：
- **不变的变量必须用 `const`**：`let` 声明的变量若不修改应改为 `const`
- **避免整型和浮点型混用**：number 类型变量不要混用整数和浮点数
- **避免稀疏数组**：数组应连续初始化
- **避免函数参数重新赋值**：参数应视为只读
- **使用 ArkTS 容器类替代 Array**：ArrayList/HashMap/TreeMap 等性能更优

不确定时，**回 `references/04-ts-to-arkts-migration-rules.md` 或 `06-arkts-high-performance.md` 搜索相关红线原文**，再下笔。

### 4. 引用文档时给出来源

回答用户的 ArkTS 语法/迁移/性能问题时，建议在回复结尾标注引用，例如：

> 依据 `references/04-ts-to-arkts-migration-rules.md` 中「强制使用静态类型」一节。

### 5. 不要替换或省略本 skill 的检查

即便用户的代码「看起来就是合法的 TypeScript」，在 HarmonyOS 上下文中也要按本 skill 的红线核查后再回答；不能默认 TypeScript 知识可直接套用于 ArkTS。

## TS→ArkTS 差异速查表

| 差异项 | TypeScript | ArkTS | 说明 |
| --- | --- | --- | --- |
| 类型系统 | 可选静态类型 | **强制静态类型** | 禁止 `any`/`unknown`，所有变量必须声明类型 |
| 对象布局 | 运行时可动态添加/删除属性 | **禁止运行时改变对象布局** | 对象结构在编译期确定，不能动态增删属性 |
| 运算符语义 | 一元 `+` 可用于字符串转数字 | **限制运算符语义** | 一元 `+` 仅用于数字，字符串转数字用 `Number()`/`parseInt()` |
| 类型兼容 | Structural typing（结构化类型） | **不支持 Structural typing** | 类型兼容性基于名义类型（nominal typing） |
| 变量声明 | `var`/`let`/`const` | **使用 `let`/`const`，禁止 `var`** | 必须使用 `let` 或 `const` |
| 类型断言 | `as` 类型断言 | **限制 `as` 类型断言** | 部分场景禁止 `as`，优先使用显式类型声明 |
| 对象字面量 | 可使用匿名对象类型 | **必须对应已声明的类或接口** | 对象字面量必须对应显式声明的 class 或 interface |
| 索引签名 | 支持 `[key: string]: type` | **不支持索引签名** | 使用 `Record` 或 `Map` 替代 |
| 装饰器 | 实验性支持 | **原生支持** | `@Entry`/`@Component`/`@State` 等 ArkUI 装饰器 |
| 枚举 | 数字枚举/字符串枚举/异构枚举 | **仅支持数字枚举和字符串枚举** | 不支持异构枚举 |
| 函数 | 支持函数重载 | **不支持函数重载** | 使用联合类型或可选参数替代 |
| `in` 运算符 | 支持属性检查 | **限制 `in` 运算符** | 仅支持 `for...in` 和 `keyof` 场景 |

## 高性能编程红线表

| 类别 | 红线 | 违规后果 |
| --- | --- | --- |
| **声明** | 不变的变量必须用 `const` 声明 | 编译器无法优化，性能下降 |
| **数值** | number 类型变量避免整型和浮点型混用 | 运行时类型检查开销 |
| **数值** | 数值计算避免溢出 | 运行时异常 |
| **循环** | 循环中常量提取，减少属性访问次数 | 不必要的重复属性访问 |
| **函数** | 建议使用参数传递函数外的变量 | 闭包捕获变量导致性能下降 |
| **函数** | 避免使用可选参数 | 运行时类型检查开销 |
| **函数** | 避免函数参数重新赋值 | 编译器无法优化 |
| **数组** | 避免稀疏数组 | 运行时额外检查 |
| **容器** | 使用 ArkTS 容器类（ArrayList/HashMap 等）替代 Array | Array 操作性能不如专用容器 |
| **并发** | 耗时任务使用 TaskPool/Worker，避免阻塞主线程 | UI 卡顿 |

## 目录结构

```
arkts-helper/
├── SKILL.md                                          # 本文件
└── references/
    ├── INDEX.md                                      # 必先阅读
    ├── 01-arkts-language-introduction.md             # ArkTS 语言介绍
    ├── 02-arkts-coding-style.md                      # ArkTS 编程规范
    ├── 03-ts-to-arkts-migration-background.md        # TS→ArkTS 适配背景
    ├── 04-ts-to-arkts-migration-rules.md             # TS→ArkTS 适配规则
    ├── 05-ts-to-arkts-migration-cases.md             # TS→ArkTS 适配案例
    ├── 06-arkts-high-performance.md                  # ArkTS 高性能编程实践
    ├── 07-arkts-stdlib-overview.md                   # ArkTS 基础类库概述
    ├── 08-arkts-xml-buffer-json.md                   # XML/Buffer/JSON 扩展库
    ├── 09-arkts-container-library.md                 # ArkTS 容器类库
    ├── 10-arkts-concurrency-async.md                 # 异步并发（Promise/async-await）
    ├── 11-arkts-concurrency-multithread.md           # 多线程并发与线程间通信
    └── 12-arkts-cross-language-overview.md           # 跨语言交互概览
```

## 文档来源与维护

- 上游：华为开发者官网「文档中心 › 应用开发」系列，路径 `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/` 下：
  - `introduction-to-arkts`（ArkTS 语言介绍）
  - `arkts-coding-style-guide`（ArkTS 编程规范）
  - `arkts-migration-background`（适配背景）
  - `typescript-to-arkts-migration-guide`（适配规则）
  - `arkts-more-cases`（适配案例）
  - `arkts-high-performance-programming`（高性能编程）
  - `arkts-utils-overview`（基础类库概述）
  - `xml-generation-parsing-conversion` + `buffer` + `arkts-json`（XML/Buffer/JSON）
  - `containers` + `linear-container` + `nonlinear-container`（容器类库）
  - `async-concurrency-overview`（异步并发）
  - `multithread-concurrency` + `interthread-communication`（多线程并发）
  - `arkts-cross-language-interaction`（跨语言交互）
- 文档为 2026-06-18 抓取的离线快照，每份文档顶部标注了上游 URL 与抓取时间。
- 如需更新到最新版本，重新运行抓取（从上游 URL `curl`/WebFetch 各 md 文件覆盖到 `references/` 即可）；若需扩充文件清单，请同步更新 `references/INDEX.md`。
- ArkTS 语言规范会随 HarmonyOS 版本更新，遇到不确定的语法请查阅官网最新文档。
