---
name: arkts-helper
description: Use when writing, reviewing, or migrating ArkTS / .ets / .ts code for HarmonyOS / OpenHarmony apps, or whenever the user mentions ArkTS, ArkUI, .ets files, HarmonyOS NEXT, OpenHarmony app development, ArkCompiler, or asks about ArkTS syntax constraints, coding style, TypeScript-to-ArkTS migration rules (arkts-no-*), or ArkTS high-performance programming. Loads the official "学习ArkTS语言" reference set so the agent can answer and code against the real spec instead of guessing from TypeScript.
---

# arkts-helper

ArkTS（Ark TypeScript）是 HarmonyOS / OpenHarmony 的应用开发语言。它在 TypeScript 基础上做了**强约束**，编译期就会拒绝大量在 TS 中合法的写法。Agent 仅凭 TS 经验写出的代码，在 ArkTS 项目里 **极易踩到强约束规则**（典型如 `arkts-no-any-unknown`、`arkts-no-untyped-obj-literals`、`arkts-no-props-by-index` 等）。

本 skill 提供的离线参考文档（`references/` 下 9 篇官方文档）是 OpenHarmony 官方「学习ArkTS语言」一节的完整离线副本，是处理 ArkTS 任务时的**权威依据**。

## 何时启用本 skill

满足以下任一条件就应当遵循本 skill 的工作流程：

- 用户在写、改、审 `.ets` / ArkTS 文件，或代码涉及 ArkUI / `@Component` / `@Entry` / `@State` 等装饰器
- 项目根存在 `oh-package.json5` / `build-profile.json5` / `module.json5` / `app.json5` 等鸿蒙工程标志
- 用户提到 HarmonyOS、OpenHarmony、HarmonyOS NEXT、DevEco Studio、ArkCompiler、方舟编译器、ArkTS、ArkUI
- 用户问到「这段 TS 在 ArkTS 里能不能用 / 怎么改」「ArkTS 报 `arkts-xxx` 错误怎么办」「ArkTS 性能优化」「ArkTS 命名/编码规范」

不要在「只是普通 TypeScript / 浏览器前端 / Node.js」场景下强行套用本 skill 的强约束。

## 工作流程（严格遵守）

### 1. 先读索引，再决定看哪份文档

任何 ArkTS 任务开始前，**必须先读** `references/INDEX.md`。它给出 9 份文档的角色、按场景的查阅路径以及关键强约束速记，能避免你把整个 reference 目录全文读进上下文。

### 2. 按问题类型加载对应文档

| 任务类型 | 必读文件（在 `references/` 下） |
| -------- | ------------------------------ |
| 通用语法（类、接口、泛型、模块、空安全等）写法确认 | `02-introduction-to-arkts.md` |
| 命名、缩进、注释、目录组织等编码风格 | `03-arkts-coding-style-guide.md` |
| **判断某种 TS 写法在 ArkTS 中是否被禁止 / 报 `arkts-xxx` 错** | `05-typescript-to-arkts-migration-guide.md`（按规则 ID 检索） |
| 某条规则的正/反例与改写方式 | `06-arkts-more-cases.md`（与 05 中规则 ID 一一对应） |
| 性能敏感场景的写法选择 | `07-arkts-high-performance-programming.md` |
| 给只熟悉 Java/Swift 的开发者解释 | `08-…-java-programmers.md` / `09-…-swift-programmers.md` |
| 整体定位、设计动机 | `01-arkts-get-started.md` + `04-arkts-migration-background.md` |

`05` 文档是按规则 ID（`arkts-no-any-unknown`、`arkts-no-untyped-obj-literals` …）组织的，可以用 grep 直接定位。`06` 中的二级标题与 `05` 的规则 ID 同名，便于交叉参考。

读取文档时优先用 `Grep`/`Read` 的 offset/limit 定位段落，不要把 100KB 的 `02` 或 `05` 一次性读全。

### 3. 落到代码时严格执行强约束

写出 / 修改 ArkTS 代码前自检以下高频红线（详细规则以文档原文为准）：

- **不写 `any` / `unknown`**：所有变量、参数、返回值都要有具体类型；不能用类型推断回退到 `any`
- **不用对象字面量当类型**：`let x: { a: number }` 写法被禁，改为 `interface` 或 `class`
- **不允许无类型的对象字面量初始化**：`{ a: 1 }` 必须有上下文类型；可用 `as InterfaceName` 或显式类型注解
- **不能动态增删属性**：禁止 `obj.newField = ...` 或 `obj['x'] = ...` 修改对象布局；改用 `class` / 索引签名替代方案见 `06`
- **不允许结构化类型匹配**：类型按名称匹配，不再按形状匹配
- **不允许 `Function`、构造签名类型、调用签名类型**
- **限制运算符语义**：`+` 仅用于数字与字符串，`-`/`*`/`/` 仅用于数字；不要 `+x` 强转
- **`catch` 不能写类型注解**：`try { … } catch (e) { … }`，`e` 一律是 `Error` 类
- **不用 `with`、`eval`、`Function` 构造、`__proto__`、运行时改 prototype**
- **数组优先用同类型元素**；性能敏感场景见 `07` 中关于循环、TypedArray 的建议
- **模块**：使用 ES Module 语法，不要 CommonJS；动态 `import()` 受限

不确定时，**回 `references/05-…migration-guide.md` 搜索 `arkts-no-` 相关规则原文**，再下笔。

### 4. 引用文档时给出来源

回答用户的语法 / 规则类问题时，建议在回复结尾标注引用，例如：

> 依据 `references/05-typescript-to-arkts-migration-guide.md` 中 `arkts-no-untyped-obj-literals` 一节。

这样用户可以快速核对原文。

### 5. 不要替换或省略本 skill 的检查

即便用户的代码段「看起来就是合法 TS」，在 ArkTS 上下文中也要按本 skill 的规则核查后再回答；不能默认 TS 知识可直接套用。

## 目录结构

```
arkts-helper/
├── SKILL.md                                          # 本文件
└── references/
    ├── INDEX.md                                      # 必先阅读
    ├── 01-arkts-get-started.md                       # 初识ArkTS语言
    ├── 02-introduction-to-arkts.md                   # ArkTS语言介绍（语法手册）
    ├── 03-arkts-coding-style-guide.md                # ArkTS编程规范
    ├── 04-arkts-migration-background.md              # 适配背景
    ├── 05-typescript-to-arkts-migration-guide.md     # 强约束规则清单（核心）
    ├── 06-arkts-more-cases.md                        # 规则配套案例
    ├── 07-arkts-high-performance-programming.md      # 高性能编程实践
    ├── 08-getting-started-with-arkts-for-java-programmers.md
    └── 09-getting-started-with-arkts-for-swift-programmers.md
```

## 文档来源与维护

- 上游：<https://gitee.com/openharmony/docs>，路径 `zh-cn/application-dev/quick-start/`，分支 `master`
- 文档为 OpenHarmony 开源版本，与华为开发者官网「文档中心 › 学习ArkTS语言」一节同源
- 如需更新到最新版本，重新运行抓取（直接从上游 raw URL `curl` 各 md 文件覆盖到 `references/` 即可）
