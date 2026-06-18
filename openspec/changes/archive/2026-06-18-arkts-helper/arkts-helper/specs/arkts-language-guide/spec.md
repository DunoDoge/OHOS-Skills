## ADDED Requirements

### Requirement: ArkTS 语言语法参考文档
系统 SHALL 提供离线参考文档 `references/01-arkts-language-introduction.md`，覆盖 ArkTS 语言的核心语法，包括：基本知识、声明（变量/常量）、类型系统（基本类型/引用类型/联合类型/类型别名）、运算符、语句（条件/循环/异常处理）、函数（声明/可选参数/rest参数/箭头函数/闭包）、类（定义/继承/接口实现）、接口、泛型、枚举。

#### Scenario: 开发者查询 ArkTS 类型系统
- **WHEN** 开发者询问 ArkTS 支持哪些类型或如何定义类型别名/联合类型
- **THEN** 系统 SHALL 从 `references/01-arkts-language-introduction.md` 中提取类型系统相关内容并提供准确指导

#### Scenario: 开发者查询 ArkTS 类与接口
- **WHEN** 开发者询问如何在 ArkTS 中定义类、实现接口或使用泛型
- **THEN** 系统 SHALL 从 `references/01-arkts-language-introduction.md` 中提取类/接口/泛型相关内容并提供准确指导

### Requirement: ArkTS 编程规范参考文档
系统 SHALL 提供离线参考文档 `references/02-arkts-coding-style.md`，覆盖 ArkTS 编程规范，包括命名规范、代码格式、注释规范等。

#### Scenario: 开发者查询 ArkTS 编码规范
- **WHEN** 开发者询问 ArkTS 的命名规范、代码格式等编程规范
- **THEN** 系统 SHALL 从 `references/02-arkts-coding-style.md` 中提取相关内容并提供指导

### Requirement: SKILL.md 包含 TS→ArkTS 差异速查表
SKILL.md SHALL 包含 TypeScript 与 ArkTS 关键差异速查表，至少覆盖：强制静态类型、禁止运行时改变对象布局、限制运算符语义、不支持 Structural typing、一元加法运算符限制等核心差异项。

#### Scenario: 开发者快速了解 TS 与 ArkTS 差异
- **WHEN** 开发者询问 ArkTS 与 TypeScript 有什么不同
- **THEN** 系统 SHALL 直接从 SKILL.md 的速查表中提供核心差异概览，无需加载完整参考文档

### Requirement: 触发条件定义
SKILL.md SHALL 定义明确的触发条件，当用户意图涉及以下场景时启用本 skill：ArkTS 语法、ArkTS 类型系统、ArkTS 类/接口/泛型、ArkTS 编程规范、ArkTS 语言特性、ArkTS 与 TypeScript 差异。

#### Scenario: 用户询问 ArkTS 语法问题
- **WHEN** 用户询问 "ArkTS 如何定义枚举" 或 "ArkTS 泛型怎么用" 等语法问题
- **THEN** 系统 SHALL 启用 arkts-helper skill 并从对应参考文档中提供指导

#### Scenario: 用户询问 TypeScript 与 ArkTS 差异
- **WHEN** 用户询问 "ArkTS 和 TypeScript 有什么区别" 或 "为什么 ArkTS 不支持某 TS 特性"
- **THEN** 系统 SHALL 启用 arkts-helper skill 并从速查表或参考文档中提供差异说明

### Requirement: 与已有 skill 的边界定义
SKILL.md SHALL 明确定义与 arkts-debug、arkts-ndk-dev、arkts-build 的边界：本 skill 负责「ArkTS 语言语法与规范指导」，arkts-debug 负责「编译报错修复」，arkts-ndk-dev 负责「NDK/C++/Node-API 开发」，arkts-build 负责「命令行构建/部署」。

#### Scenario: 编译报错场景的 skill 边界
- **WHEN** 用户遇到 ArkTS 编译报错需要修复
- **THEN** 系统 SHALL 引导用户使用 arkts-debug skill 而非本 skill

#### Scenario: NDK 开发场景的 skill 边界
- **WHEN** 用户询问如何使用 Node-API 进行 C++ 互操作开发
- **THEN** 系统 SHALL 引导用户使用 arkts-ndk-dev skill 而非本 skill
