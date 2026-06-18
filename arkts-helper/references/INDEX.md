<!-- 必先阅读 -->
<!-- ArkTS 语言规范以官网为准：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts -->

# INDEX - arkts-helper 参考文档索引

> **必先阅读**：任何 arkts-helper 任务开始前，**必须先读本文件**，再根据任务类型按映射表加载对应文档。
>
> **ArkTS 语言规范以官网为准**：ArkTS 语法与适配规则会随 HarmonyOS 版本更新，本文档为 2026-06-18 抓取的离线快照，遇到不确定的语法请查阅上游官网文档。

## 文档角色一览

| 文件 | 角色 |
| --- | --- |
| `01-arkts-language-introduction.md` | ArkTS 语言介绍：基本知识、声明、类型、运算符、语句、函数、类、接口、泛型、枚举、模块、空安全 |
| `02-arkts-coding-style.md` | ArkTS 编程规范：命名规范、代码格式、注释规范、编程实践 |
| `03-ts-to-arkts-migration-background.md` | TS→ArkTS 适配背景：程序稳定性、程序性能、兼容性、方舟运行时 |
| `04-ts-to-arkts-migration-rules.md` | **TS→ArkTS 适配规则（核心）**：强制静态类型、禁止运行时变更对象布局、限制运算符语义、不支持 structural typing、约束说明 |
| `05-ts-to-arkts-migration-cases.md` | TS→ArkTS 适配案例：arkts-no-* 规则的具体适配实例 |
| `06-arkts-high-performance.md` | **ArkTS 高性能编程（核心）**：声明优化、函数优化、数组优化、容器优化、并发优化 |
| `07-arkts-stdlib-overview.md` | ArkTS 基础类库概述：XML/Buffer/容器/URL/Decimal/JSON |
| `08-arkts-xml-buffer-json.md` | XML 生成解析转换 + Buffer/FastBuffer + JSON 扩展库 |
| `09-arkts-container-library.md` | ArkTS 容器类库：线性容器（7种）+ 非线性容器（7种）+ 选择指南 |
| `10-arkts-concurrency-async.md` | 异步并发：Promise/async-await/组合方法/最佳实践 |
| `11-arkts-concurrency-multithread.md` | **多线程并发（核心）**：TaskPool/Worker/线程间通信/Sendable |
| `12-arkts-cross-language-overview.md` | 跨语言交互概览：Node-API 概念与开发流程入口（详细开发转 arkts-ndk-dev） |

## 按场景的查阅路径

| 场景 | 必读文件（在 `references/` 下） |
| --- | --- |
| 学习 ArkTS 语法 | `01-arkts-language-introduction.md`, `02-arkts-coding-style.md` |
| TS 代码迁移到 ArkTS | `03-ts-to-arkts-migration-background.md` → `04-ts-to-arkts-migration-rules.md` → `05-ts-to-arkts-migration-cases.md` |
| 优化 ArkTS 代码性能 | `06-arkts-high-performance.md` |
| 使用基础类库 | `07-arkts-stdlib-overview.md`, `08-arkts-xml-buffer-json.md`, `09-arkts-container-library.md` |
| 并发编程 | `10-arkts-concurrency-async.md`, `11-arkts-concurrency-multithread.md` |
| 与 C++ 交互 | `12-arkts-cross-language-overview.md`（详细开发转 `arkts-ndk-dev` skill） |
| 编译报错修复 | 转 `arkts-debug` skill |

## TS→ArkTS 关键差异速记

| 差异项 | TS | ArkTS |
| --- | --- | --- |
| 类型系统 | 可选静态 | **强制静态**，禁止 any/unknown |
| 对象布局 | 运行时可变 | **禁止运行时变更** |
| 运算符 | 一元 + 可转数字 | **一元 + 仅用于数字** |
| 类型兼容 | Structural typing | **不支持**，基于名义类型 |
| 变量声明 | var/let/const | **禁止 var**，仅 let/const |
| 类型断言 | as 随意使用 | **限制 as**，优先显式声明 |
| 对象字面量 | 匿名类型 | **必须对应 class/interface** |
| 索引签名 | 支持 | **不支持**，用 Record/Map |
| 函数重载 | 支持 | **不支持**，用联合类型/可选参数 |

## 高性能编程红线速记

- **const**：不变的变量必须用 const
- **数值**：避免整型浮点混用
- **循环**：常量提取，减少属性访问
- **函数**：避免可选参数、避免参数重新赋值
- **数组**：避免稀疏数组
- **容器**：使用 ArkTS 容器类（ArrayList/HashMap 等）替代 Array
- **并发**：耗时任务用 TaskPool/Worker，避免阻塞主线程
