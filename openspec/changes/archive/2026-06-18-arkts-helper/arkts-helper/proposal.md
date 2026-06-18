## Why

当前项目已有 `arkts-build`（命令行构建）、`arkts-debug`（编译报错修复）、`arkts-ndk-dev`（NDK/C++互操作）三个 skill，但缺少一个覆盖 **ArkTS 语言本身的语法规范、TS→ArkTS 迁移指导、高性能编程实践、基础类库与并发编程** 的综合性 skill。开发者在编写 ArkTS 代码时，常因不熟悉 ArkTS 与 TypeScript 的差异（如强制静态类型、禁止运行时改变对象布局、不支持 Structural typing 等）而写出不符合规范的代码，导致编译错误或性能问题。需要一个 `arkts-helper` skill，基于华为官方文档提供准确的 ArkTS 开发指导。

## What Changes

- 新增 `arkts-helper` skill，包含 SKILL.md 和离线参考文档集（references/）
- 参考文档覆盖以下六大主题：
  1. **ArkTS 语言介绍**：基本知识、声明、类型、运算符、语句、函数、类、接口、泛型、枚举等
  2. **TS→ArkTS 适配规则**：强制静态类型、禁止运行时改变对象布局、限制运算符语义、不支持 Structural typing 等核心差异
  3. **ArkTS 高性能编程实践**：声明与表达式优化、函数优化、数组与容器优化、并发优化等
  4. **ArkTS 基础类库**：XML 生成解析转换、Buffer 与 FastBuffer、JSON 扩展库、容器类库
  5. **ArkTS 并发编程**：异步并发（Promise/async-await）、多线程并发（TaskPool/Worker）、线程间通信、Sendable 对象
  6. **ArkTS 跨语言交互概览**：Node-API 基本概念与开发流程入口（详细实现由 arkts-ndk-dev skill 覆盖）
- SKILL.md 定义触发条件、工作流程、与已有 skill 的边界、速查表

## Capabilities

### New Capabilities
- `arkts-language-guide`: ArkTS 语言语法规范与核心概念指导，覆盖声明、类型系统、运算符、语句、函数、类、接口、泛型、枚举等
- `arkts-migration-guide`: TypeScript 到 ArkTS 的适配迁移指导，覆盖语法差异、适配规则、适配案例
- `arkts-performance-guide`: ArkTS 高性能编程实践指导，覆盖声明优化、函数优化、数组与容器优化、并发优化
- `arkts-stdlib-guide`: ArkTS 基础类库与并发编程指导，覆盖 XML/Buffer/JSON/容器类库、异步并发、多线程并发、线程间通信

### Modified Capabilities
<!-- 无需修改现有 spec -->

## Impact

- 新增 `arkts-helper/` 目录，包含 SKILL.md 和 references/ 子目录（约 10-15 篇离线参考文档 + 1 份 INDEX.md）
- 需更新 `arkts-debug` 和 `arkts-ndk-dev` 的 SKILL.md 中与 arkts-helper 的边界说明
- 参考文档来源：华为开发者官网 `harmonyos-guides/learning-arkts` 和 `harmonyos-guides/arkts` 系列文档
