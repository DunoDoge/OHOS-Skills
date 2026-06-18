## Context

当前项目已有三个 ArkTS 相关 skill：
- `arkts-build`：命令行构建/测试/部署
- `arkts-debug`：编译报错修复（22 类错误目录）
- `arkts-ndk-dev`：NDK / Node-API / C++ 互操作

但缺少一个覆盖 **ArkTS 语言本身** 的指导 skill。开发者在编写 ArkTS 代码时面临以下痛点：
1. 不了解 ArkTS 与 TypeScript 的关键差异，写出不合规代码
2. 不知道如何将现有 TS 代码迁移到 ArkTS
3. 不熟悉 ArkTS 高性能编程最佳实践
4. 不了解 ArkTS 基础类库（XML/Buffer/JSON/容器）和并发编程模型

华为官方文档分散在多个页面，且内容量大，开发者难以快速定位所需信息。

## Goals / Non-Goals

**Goals:**
- 提供离线参考文档集，覆盖 ArkTS 语言语法、TS→ArkTS 迁移、高性能编程、基础类库与并发编程
- 定义清晰的触发条件，使 Agent 能准确判断何时启用本 skill
- 与已有 skill（arkts-debug、arkts-ndk-dev、arkts-build）建立明确边界，避免职责重叠
- 提供 INDEX.md 索引和按场景的查阅路径，提升信息检索效率
- 提供速查表（TS→ArkTS 差异速查、高性能编程红线），覆盖高频决策场景

**Non-Goals:**
- 不覆盖编译报错修复（由 arkts-debug 负责）
- 不覆盖 NDK/C++/Node-API 详细开发（由 arkts-ndk-dev 负责）
- 不覆盖命令行构建/部署（由 arkts-build 负责）
- 不覆盖 ArkUI 声明式 UI 开发（属于独立领域，超出本 skill 范围）
- 不提供在线文档抓取能力，参考文档为离线快照

## Decisions

### Decision 1: 采用离线参考文档集模式（与 arkts-build/arkts-ndk-dev 一致）

**选择**：使用 `references/` 目录 + `INDEX.md` + 编号文档的模式

**理由**：
- 与项目已有 skill 保持一致的组织方式
- 离线文档确保 Agent 无需网络即可获取准确指导
- INDEX.md 提供按场景的查阅路径，减少全量加载

**备选方案**：
- 使用 `reference/`（单数）+ assets 模式（如 arkts-debug）→ 不适合，本 skill 不是错误修复目录
- 纯 SKILL.md 无参考文档 → 不适合，内容量太大无法内联

### Decision 2: 参考文档按主题分文件，共约 10-12 篇

**选择**：按以下主题拆分参考文档：

| 编号 | 文件名 | 主题 | 来源 |
|------|--------|------|------|
| 01 | arkts-language-introduction.md | ArkTS 语言介绍（声明/类型/运算符/语句/函数/类/接口/泛型/枚举） | introduction-to-arkts |
| 02 | arkts-coding-style.md | ArkTS 编程规范 | arkts-coding-style-guide |
| 03 | ts-to-arkts-migration-background.md | TS→ArkTS 语法适配背景 | arkts-migration-background |
| 04 | ts-to-arkts-migration-rules.md | TS→ArkTS 适配规则 | typescript-to-arkts-migration-guide |
| 05 | ts-to-arkts-migration-cases.md | 适配指导案例 | arkts-more-cases |
| 06 | arkts-high-performance.md | ArkTS 高性能编程实践 | arkts-high-performance-programming |
| 07 | arkts-stdlib-overview.md | ArkTS 基础类库概述 | arkts-utils-overview |
| 08 | arkts-xml-buffer-json.md | XML/Buffer/JSON 扩展库 | xml-generation-parsing-conversion + buffer + arkts-json |
| 09 | arkts-container-library.md | ArkTS 容器类库 | containers |
| 10 | arkts-concurrency-async.md | 异步并发（Promise/async-await） | async-concurrency-overview |
| 11 | arkts-concurrency-multithread.md | 多线程并发与线程间通信 | multithread-concurrency + interthread-communication |
| 12 | arkts-cross-language-overview.md | 跨语言交互概览（入口级） | arkts-cross-language-interaction |

**理由**：按主题拆分便于按需加载，避免单文件过长；与 arkts-build/arkts-ndk-dev 的编号模式一致

### Decision 3: SKILL.md 包含 TS→ArkTS 差异速查表和高性能编程红线表

**选择**：在 SKILL.md 中内联两个速查表

**理由**：
- TS→ArkTS 差异是开发者最高频的查询需求，速查表可避免每次都加载完整参考文档
- 高性能编程红线是容易违反的规则，需要醒目提醒
- 与 arkts-build 的高频命令速查表、arkts-ndk-dev 的红线速查表模式一致

### Decision 4: 跨语言交互仅提供概览级内容

**选择**：12 号文档仅包含 Node-API 概念介绍和开发流程入口，不深入 Node-API 接口细节

**理由**：Node-API 详细开发由 arkts-ndk-dev skill 覆盖，避免内容重复

## Risks / Trade-offs

- **[文档时效性]** 离线快照可能滞后于官方最新文档 → 在 SKILL.md 中标注抓取日期，建议定期更新
- **[内容量]** 12 篇参考文档总量较大 → 通过 INDEX.md 按场景查阅路径引导按需加载
- **[与 arkts-debug 边界模糊]** TS→ArkTS 迁移规则与编译报错修复有交叉 → 明确边界：本 skill 负责「如何写合规代码」，arkts-debug 负责「报错后如何修复」
- **[与 arkts-ndk-dev 边界模糊]** 跨语言交互概览与 NDK 开发有交叉 → 明确边界：本 skill 仅提供概念入口，arkts-ndk-dev 提供完整开发指导
