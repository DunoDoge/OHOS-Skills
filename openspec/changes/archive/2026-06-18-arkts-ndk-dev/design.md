## Context

仓库 `OHOS-Skills` 已有三个鸿蒙开发 skill：

- `arkts-helper`：ArkTS 语法/迁移/编码规范（离线官方「学习ArkTS语言」9 篇）。
- `arkts-debug`：ArkTS 编译报错修复（22 类常见错误的 reference + assets）。
- `arkts-build`：命令行构建/测试/部署（8 篇命令行工具离线文档）。

三者分别覆盖「写代码」「改报错」「构建部署」，但**NDK / C++ / Node-API 互操作**这一关键场景是空白。HarmonyOS 的 Node-API 虽基于 Node.js 18.x LTS 的 Node-API 规范扩展，但存在显著差异：

- **模块注册方式不同**：鸿蒙使用 `napi_module` 结构体 + `__attribute__((constructor))` 自动注册，而非 Node.js 的 `napi_register_module_v1`。
- **线程模型不同**：Node-API 接口只能在 ArkTS 线程使用，`napi_env` 与特定 ArkTS 线程绑定；跨线程必须使用 `napi_threadsafe_function`，而非 Node.js 社区常用的 `uv_queue_work`。
- **不完全兼容**：部分 Node.js Node-API 接口在鸿蒙上不可用或行为不同，Agent 凭 Node.js 经验写出的代码可能无法编译或运行时崩溃。
- **SO 命名强约束**：`nm_modname` 必须与 so 名完全匹配（区分大小写），一个 so 只能注册一个模块。
- **性能陷阱**：JSArray vs ArrayBuffer 性能差距达 400 倍以上，`napi_wrap` 的 result 参数传 nullptr vs 非 nullptr 有不同的内存管理语义。

Agent 凭通用 Node.js N-API 经验下笔会给出平台不支持的接口、错误的线程模型、或遗漏关键红线。本设计新增 `arkts-ndk-dev` skill，把官方「NDK 开发」系列文档离线化 + 场景化索引，与已有三个 skill 形成「写代码 / 改报错 / 调 native / 构建部署」的完整闭环。

## Goals / Non-Goals

**Goals:**

- 提供 `arkts-ndk-dev` skill，让 Agent 在 NDK / Node-API / C++ 互操作类任务中按真实鸿蒙规范下笔。
- 离线化官方 NDK 开发文档（NDK 导读 / 创建工程 / 构建工程 / 代码开发 / Rawfile / NativeBundle / 编译工具链 / 调试性能分析 / 硬件兼容性），按场景拆分文件，支持按需加载，避免一次性灌满上下文。
- **重点覆盖 Node-API**：模块注册、接口映射、类型转换、生命周期管理、线程安全、异步任务、对象绑定、性能优化等核心开发流程与红线。
- 明确触发条件与场景化查阅路径（INDEX.md），降低 Agent 选错文档的概率。
- 明确与 `arkts-helper` / `arkts-debug` / `arkts-build` 的边界，避免职责重叠。

**Non-Goals:**

- 不覆盖 ArkTS 语法/迁移/编码规范（→ `arkts-helper`）。
- 不覆盖 ArkTS 编译报错的根因与修复（→ `arkts-debug`）。
- 不覆盖命令行构建/部署/签名/流水线（→ `arkts-build`）；本 skill 只负责「NDK 代码怎么写 / CMake 怎么配 / Node-API 怎么用」，构建命令本身归 `arkts-build`。
- 不覆盖 JSVM-API（另一套 JS 与 C/C++ 交互机制，非 Node-API）；本 skill 聚焦 Node-API。
- 不覆盖 Longque-JS-API。
- 不做文档的自动同步/抓取工具；参考文档为离线快照，更新靠手动重新抓取覆盖。

## Decisions

### 决策 1：参考文档按「场景/主题」拆分为 11 份 + 1 份 INDEX，而非单一大文件

**选择**：`references/` 下按场景拆分（01-ndk-overview / 02-create-ndk-project / 03-build-ndk-project / 04-node-api-overview / 05-node-api-development / 06-node-api-best-practices / 07-rawfile / 08-native-bundle / 09-build-toolchain / 10-debugging-profiling / 11-hardware-compatibility）+ `INDEX.md`。

**理由**：
- 与 `arkts-build`（8 篇 + INDEX）、`arkts-helper`（9 篇 + INDEX）的拆分风格一致，便于 `Grep`/`Read` offset/limit 定位。
- Node-API 是本 skill 的重点，拆分为 3 份（04 概览 / 05 开发流程 / 06 最佳实践与红线），让 Agent 在不同深度场景下按需加载：简单问题只看 05 的流程步骤，红线问题查 06，架构问题看 04。
- `INDEX.md` 给出「任务类型 → 必读文件」映射表，Agent 先读 INDEX 再按需加载，与已有 skill 工作流一致。

**备选**：单文件 `references.md`。**否决**：上下文成本太高，且无法按需加载。

**备选**：Node-API 合并为 1 份。**否决**：Node-API 内容量大（开发流程 + 最佳实践 + 红线），合并后单文件超 50KB，Agent 难以定位；拆分后「写代码」看 05、「查红线」看 06、「理解架构」看 04，职责清晰。

### 决策 2：Node-API 拆分为「概览 / 开发流程 / 最佳实践」三份文档

**选择**：
- `04-node-api-overview.md`：架构组成、初始化与调用流程、与 Node.js 的差异概览。
- `05-node-api-development.md`：完整开发流程——模块注册、接口映射、index.d.ts 声明、oh-package.json5 关联、CMakeLists.txt 配置、参数获取与类型转换、ArkTS 侧调用、约束限制。含完整代码示例。
- `06-node-api-best-practices.md`：开发规范与红线——参数获取规范、生命周期管理（handle_scope）、上下文敏感、异常处理、异步任务（napi_threadsafe_function）、对象绑定、高性能数组、数据转换优化、模块注册与命名约束、dlopen 场景、napi_create_external 限制、buffer 释放。

**理由**：
- Agent 在「写一个 Node-API 模块」时需要 05 的完整流程与代码模板；在「排查 Node-API 崩溃/性能问题」时需要 06 的红线与最佳实践；在「理解 Node-API 架构」时需要 04 的概览。三种场景深度不同，拆分后按需加载效率更高。
- 06 中的红线清单可作为 Agent 的自检清单，在写出 Node-API 代码后逐条核对。

**备选**：合并为 1 份 `node-api.md`。**否决**：单文件超 50KB，且「写代码」与「查红线」场景混在一起，Agent 难以快速定位。

### 决策 3：SKILL.md 内置「Node-API 红线速查」+「高频代码模板」，而非只给文档链接

**选择**：`SKILL.md` 中包含：
- 触发关键词清单（Node-API / napi / NDK / C++ 互操作 / Native / CMake / so / napi_wrap / napi_threadsafe_function / Rawfile / NativeBundle / ASan / LLDB / ABI / Neon 等）。
- 与已有 skill 的边界说明。
- 工作流（先读 INDEX → 按场景加载文档 → 写代码/配工具链 → 核对红线 → 引用来源）。
- **Node-API 红线速查表**（线程安全 / 生命周期 / 模块注册 / 异步任务 / 对象绑定 / 性能等 6 大类红线）。
- **高频代码模板**（模块注册模板 / 接口映射模板 / 参数获取与类型转换模板 / napi_threadsafe_function 模板）。
- 目录结构与文档来源说明。

**理由**：
- 与 `arkts-build`（命令速查表 + 红线）、`arkts-debug`（Quick Reference 表）风格一致。
- 80% 的 Node-API 任务只需红线速查 + 代码模板即可回答，无需打开 reference；复杂场景再查文档。
- 红线能直接拦截「跨线程用 env」「uv_queue_work 替代 napi_threadsafe_function」「napi_wrap result 不传 nullptr」等高频错误。

**备选**：SKILL.md 只放触发条件 + 文档链接。**否决**：Agent 每次都要读 reference 才能下笔，效率低且易漏红线。

### 决策 4：参考文档来源为华为开发者官网公开文档的离线快照

**选择**：`references/` 内容抓取自 `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/` 下「NDK 开发」系列（ndk-development-overview / create-with-ndk / build-with-ndk / coding / rawfile-guidelines / native-bundle-guidelines / build-toolchain / debugging-profiling / hardware-compatibility），清洗为 Markdown 后离线存放。每份文档顶部标注上游 URL 与更新时间。

**理由**：
- 与 `arkts-build`（来源华为官网）、`arkts-helper`（来源 gitee openharmony docs）策略一致。
- 离线化保证 Agent 在无网环境下也能检索；华为官网文档是鸿蒙 NDK 的权威来源。
- 标注上游 URL 便于后续手动更新。

**备选**：实时 WebFetch 官网。**否决**：每次任务都要联网抓取，慢且不可靠；文档结构不稳定，难以按需定位段落。

### 决策 5：与已有 skill 的边界用「交叉引用」而非「互斥」

**选择**：`SKILL.md` 明确：
- NDK 任务中遇到 ArkTS 语法/迁移问题 → 交叉引用 `arkts-helper`。
- NDK 任务中遇到 ArkTS 编译报错 → 交叉引用 `arkts-debug`。
- NDK 任务中需要构建/部署命令 → 交叉引用 `arkts-build`（本 skill 只负责 CMakeLists.txt 怎么写 / CMake 工具链变量怎么配，不负责 `hvigorw` 命令本身）。

**理由**：
- NDK 开发经常涉及 ArkTS 侧调用代码、构建命令等，强行互斥会让 Agent 来回切换 skill；交叉引用让 Agent 在本 skill 内给出 NDK 层建议后，提示用户用对应 skill 处理其他层问题。
- 与 `arkts-build` 中「NDK 归 arkts-ndk-dev」的交叉引用风格一致。

### 决策 6：调试性能分析（ASan/LLDB）和硬件兼容性（ABI/Neon）做概览文档，不逐个展开

**选择**：`10-debugging-profiling.md` 和 `11-hardware-compatibility.md` 只做概览索引，列出关键配置步骤与官方链接，不把 ASan/LLDB/ABI/Neon 的完整文档都搬进来。

**理由**：
- ASan/LLDB 的完整配置步骤较长，但 Agent 在 NDK 上下文中主要需要「知道有这些工具 + 基本启用方式」，深入配置按需查官网。
- ABI/Neon 属于进阶场景，概览 + 官方链接足够。
- 与 `arkts-build` 中 `07-debugging-commands.md` 只做索引的策略一致。

**备选**：把 ASan/LLDB/ABI/Neon 每个都展开成独立 md。**否决**：体积与维护成本过高，且超出 Node-API 主线。

## Risks / Trade-offs

- **[文档时效性]** 官网文档会随 HarmonyOS 版本更新（如 Node-API 新增接口、ASan 配置变化），离线快照可能滞后。
  → **缓解**：每份文档顶部标注上游 URL 与抓取时间；`SKILL.md` 的「文档来源与维护」一节说明更新方式（重新抓取覆盖）；INDEX.md 提示「API 版本差异以官网为准」。

- **[Node-API 与 Node.js 差异]** Agent 可能凭 Node.js N-API 经验给出鸿蒙不支持的接口或错误用法。
  → **缓解**：`04-node-api-overview.md` 明确标注与 Node.js 的差异；`06-node-api-best-practices.md` 逐条列出红线；SKILL.md 红线速查表作为 Agent 自检清单。

- **[线程安全红线]** Node-API 只能在 ArkTS 线程使用是最容易踩的坑，Agent 可能给出跨线程直接使用 env 的代码。
  → **缓解**：`06-node-api-best-practices.md` 线程安全章节详细说明；SKILL.md 红线速查表首条即为线程安全红线；`05-node-api-development.md` 约束限制章节强调此点。

- **[与 arkts-build 重叠]** NDK 构建既涉及 CMakeLists.txt / CMake 工具链（本 skill），又涉及 hvigorw 构建命令（arkts-build）。
  → **缓解**：本 skill 覆盖「CMakeLists.txt 怎么写 / CMake 工具链变量怎么配 / ohos.toolchain.cmake 参数」；`hvigorw` 命令本身归 `arkts-build`。SKILL.md 边界说明中明确这一点。

- **[SO 命名约束]** nm_modname 与 so 名大小写必须完全匹配，Agent 可能忽略此约束导致运行时模块加载失败。
  → **缓解**：`05-node-api-development.md` 和 `06-node-api-best-practices.md` 均强调此约束；SKILL.md 红线速查表包含此条。
