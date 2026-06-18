## ADDED Requirements

### Requirement: ArkTS 基础类库概述参考文档
系统 SHALL 提供离线参考文档 `references/07-arkts-stdlib-overview.md`，覆盖 ArkTS 基础类库概述，包括基础类库的组成、能力范围和使用方式。

#### Scenario: 开发者了解基础类库能力
- **WHEN** 开发者询问 "ArkTS 提供了哪些基础类库" 或 "ArkTS 基础类库能做什么"
- **THEN** 系统 SHALL 从 `references/07-arkts-stdlib-overview.md` 中提取类库概述

### Requirement: XML/Buffer/JSON 扩展库参考文档
系统 SHALL 提供离线参考文档 `references/08-arkts-xml-buffer-json.md`，覆盖 XML 生成解析转换、Buffer 与 FastBuffer、JSON 扩展库的使用方法。

#### Scenario: 开发者使用 XML 处理
- **WHEN** 开发者询问 "ArkTS 如何生成/解析/转换 XML"
- **THEN** 系统 SHALL 从 `references/08-arkts-xml-buffer-json.md` 中提取 XML 相关内容

#### Scenario: 开发者使用 Buffer
- **WHEN** 开发者询问 "ArkTS Buffer 和 FastBuffer 怎么用"
- **THEN** 系统 SHALL 从 `references/08-arkts-xml-buffer-json.md` 中提取 Buffer 相关内容

#### Scenario: 开发者使用 JSON 扩展库
- **WHEN** 开发者询问 "ArkTS JSON 扩展库有哪些能力"
- **THEN** 系统 SHALL 从 `references/08-arkts-xml-buffer-json.md` 中提取 JSON 相关内容

### Requirement: ArkTS 容器类库参考文档
系统 SHALL 提供离线参考文档 `references/09-arkts-container-library.md`，覆盖 ArkTS 容器类库，包括线性容器（ArrayList/LinkedList/Deque/Queue/Stack 等）、键值对容器（HashMap/TreeMap/LightWeightMap 等）、集合容器（HashSet/TreeSet/LightWeightSet）的使用方法和性能特征。

#### Scenario: 开发者选择合适的容器
- **WHEN** 开发者询问 "ArkTS 中应该用 ArrayList 还是 LinkedList" 或 "HashMap 和 TreeMap 有什么区别"
- **THEN** 系统 SHALL 从 `references/09-arkts-container-library.md` 中提取容器对比和选择建议

### Requirement: 异步并发参考文档
系统 SHALL 提供离线参考文档 `references/10-arkts-concurrency-async.md`，覆盖异步并发编程，包括 Promise 和 async/await 的使用方法、错误处理、异步编程最佳实践。

#### Scenario: 开发者使用异步编程
- **WHEN** 开发者询问 "ArkTS 如何使用 Promise" 或 "ArkTS async/await 怎么用"
- **THEN** 系统 SHALL 从 `references/10-arkts-concurrency-async.md` 中提取异步并发相关内容

### Requirement: 多线程并发参考文档
系统 SHALL 提供离线参考文档 `references/11-arkts-concurrency-multithread.md`，覆盖多线程并发编程，包括 TaskPool 和 Worker 两种并发 API 的使用、线程间通信、Sendable 对象、应用多线程开发实践。

#### Scenario: 开发者使用 TaskPool
- **WHEN** 开发者询问 "ArkTS TaskPool 怎么用" 或 "TaskPool 和 Worker 选哪个"
- **THEN** 系统 SHALL 从 `references/11-arkts-concurrency-multithread.md` 中提取 TaskPool 相关内容

#### Scenario: 开发者使用 Sendable 对象
- **WHEN** 开发者询问 "ArkTS Sendable 对象是什么" 或 "线程间如何高效传递数据"
- **THEN** 系统 SHALL 从 `references/11-arkts-concurrency-multithread.md` 中提取 Sendable 相关内容

### Requirement: 跨语言交互概览参考文档
系统 SHALL 提供离线参考文档 `references/12-arkts-cross-language-overview.md`，提供跨语言交互的概览级内容，包括 Node-API 基本概念、开发流程入口。详细 Node-API 开发指导 SHALL 引导至 arkts-ndk-dev skill。

#### Scenario: 开发者了解跨语言交互
- **WHEN** 开发者询问 "ArkTS 如何与 C++ 交互" 或 "Node-API 是什么"
- **THEN** 系统 SHALL 从 `references/12-arkts-cross-language-overview.md` 中提供概览级说明，并引导详细开发至 arkts-ndk-dev skill

### Requirement: INDEX.md 按场景查阅路径
references/INDEX.md SHALL 提供按场景的查阅路径表，至少包含以下场景路径：
- "学习 ArkTS 语法" → 01, 02
- "TS 代码迁移到 ArkTS" → 03, 04, 05
- "优化 ArkTS 代码性能" → 06
- "使用基础类库" → 07, 08, 09
- "并发编程" → 10, 11
- "与 C++ 交互" → 12（详细开发转 arkts-ndk-dev）

#### Scenario: 开发者按场景查阅
- **WHEN** 开发者需要学习 ArkTS 并发编程
- **THEN** 系统 SHALL 根据 INDEX.md 的查阅路径加载 10 和 11 号参考文档
