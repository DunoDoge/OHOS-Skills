## Why

当前仓库已有 `arkts-helper`（ArkTS 语法/迁移）、`arkts-debug`（ArkTS 编译报错修复）、`arkts-build`（命令行构建/测试/部署）三个 skill，但**缺少覆盖「HarmonyOS NDK / C++ / Node-API 互操作」的 skill**。

Agent 在被要求「用 Node-API 实现 ArkTS 与 C/C++ 交互」「NDK 工程怎么创建/构建」「CMake 工具链怎么配」「Node-API 多线程怎么处理」「napi_wrap/napi_threadsafe_function 怎么用」时，只能凭 Node.js N-API 经验猜测，极易给出**鸿蒙不支持的接口、错误的模块注册方式、或遗漏线程安全/生命周期管理红线**。HarmonyOS 的 Node-API 虽基于 Node.js 18.x LTS 的 Node-API 规范扩展，但**不完全兼容**——模块注册方式（`napi_module` + `__attribute__((constructor))`）、线程模型（env 与 ArkTS 线程绑定）、异步任务推荐方式（`napi_threadsafe_function` 而非 `uv_queue_work`）等均有差异，需要一份离线、权威、按场景索引的参考集。

本 change 新增 `arkts-ndk-dev` skill，把华为官方「NDK 开发」系列文档（NDK 导读 / 创建工程 / 构建工程 / 代码开发（重点 Node-API）/ Rawfile / NativeBundle / 编译工具链 / 调试性能分析 / 硬件兼容性）整理成离线参考文档 + 场景化工作流，让 Agent 在 NDK/C++ 互操作类任务中按真实规范下笔。

## What Changes

- 新增 skill 目录 `arkts-ndk-dev/`，包含 `SKILL.md`（触发条件、工作流、红线速查、目录结构）。
- 新增 `arkts-ndk-dev/references/` 离线参考文档集，覆盖以下官方文档（按场景拆分，便于按需加载）：
  - `01-ndk-overview.md`：NDK 适用场景、必备基础知识、目录简介、常用模块（标准库/Node-API/FFRT/libuv/Rawfile/XComponent/Drawing/OpenGL/OpenSL ES）。
  - `02-create-ndk-project.md`：通过 DevEco Studio 创建 Native C++ 工程、工程目录结构。
  - `03-build-ndk-project.md`：CMake 构建系统、hmos.toolchain.cmake 核心配置、OHOS_STL/OHOS_ARCH 参数、命令行构建步骤、预构建库使用。
  - `04-node-api-overview.md`：Node-API 简介、架构组成（Native Module/Node-API/ModuleManager/ScopeManager/ReferenceManager/NativeEngine/ArkTS Runtime）、初始化与调用流程。
  - `05-node-api-development.md`：**核心文档**——使用 Node-API 实现跨语言交互的完整开发流程：模块注册（napi_module + constructor）、接口映射（napi_property_descriptor + napi_define_properties）、index.d.ts 声明、oh-package.json5 关联、CMakeLists.txt 配置、参数获取与类型转换、ArkTS 侧调用、约束限制。
  - `06-node-api-best-practices.md`：**核心文档**——Node-API 开发规范与红线：参数获取规范、生命周期管理（handle_scope）、上下文敏感（禁止跨 env）、异常处理、异步任务（推荐 napi_threadsafe_function）、对象绑定（napi_wrap/napi_remove_wrap）、高性能数组（ArrayBuffer vs JSArray）、数据转换优化、模块注册与命名约束、dlopen 场景、napi_create_external 限制、buffer 释放。
  - `07-rawfile.md`：Native Rawfile 接口（遍历/打开/搜索/读取/关闭）、64 后缀大文件接口、开发步骤与代码示例。
  - `08-native-bundle.md`：Native Bundle 接口（获取应用信息/appId/appIdentifier/入口信息/设备类型/调试模式/元数据）、开发步骤与内存管理。
  - `09-build-toolchain.md`：编译工具链配置（CMake/GN/Make/Configure）、lycium 交叉编译框架、跨语言调用复杂参数传递、Native 子线程与 UI 主线程通信。
  - `10-debugging-profiling.md`：C/C++ 内存错误检测（ASan）、LLDB 高性能调试器。
  - `11-hardware-compatibility.md`：HarmonyOS ABI、CPU 特性、Neon 指令扩展。
  - `INDEX.md`：必先阅读的索引，给出每份文档角色、按场景的查阅路径、关键红线速记。
- `SKILL.md` 中明确**触发关键词**（Node-API / napi / NDK / C++ 互操作 / Native / CMake / so / napi_wrap / napi_threadsafe_function / Rawfile / NativeBundle / ASan / LLDB / ABI / Neon 等）与**与已有 skill 的边界**（构建命令归 `arkts-build`，ArkTS 语法归 `arkts-helper`，ArkTS 编译报错归 `arkts-debug`）。

## Capabilities

### New Capabilities
- `arkts-ndk-dev`: 指导 Agent 进行 HarmonyOS NDK 开发的 skill，重点覆盖 Node-API 跨语言交互（模块注册/接口映射/类型转换/生命周期/线程安全/异步任务/对象绑定/性能优化），同时覆盖 NDK 工程创建与构建、CMake 工具链配置、Rawfile/NativeBundle 接口、调试性能分析、硬件兼容性，含离线官方文档参考集与场景化工作流。

### Modified Capabilities
<!-- 无已有 spec 需要修改 -->

## Impact

- **新增代码/文件**：`arkts-ndk-dev/SKILL.md` + `arkts-ndk-dev/references/*.md`（约 11 份文档 + INDEX）。
- **无破坏性变更**：纯新增 skill，不影响现有 `arkts-helper` / `arkts-debug` / `arkts-build`。
- **依赖**：无运行时依赖；参考文档内容来自华为开发者官网公开文档（https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ 下「NDK 开发」系列），离线化后供 Agent 检索。
- **边界**：本 skill 不负责 ArkTS 语法/迁移（→ `arkts-helper`）、ArkTS 编译报错修复（→ `arkts-debug`）、命令行构建/部署（→ `arkts-build`）；当 NDK 任务中遇到这三类问题时，应交叉引用对应 skill。
