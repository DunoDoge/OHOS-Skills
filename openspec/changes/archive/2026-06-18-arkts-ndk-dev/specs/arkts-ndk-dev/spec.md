## ADDED Requirements

### Requirement: Skill 触发条件

`arkts-ndk-dev` skill SHALL 在 Agent 面向 HarmonyOS / OpenHarmony 工程执行「NDK 开发 / Node-API 跨语言交互 / C++ 互操作 / CMake 工具链配置 / Native 资源管理 / NDK 调试性能分析 / 硬件兼容性」类任务时被激活。`SKILL.md` MUST 列出明确的触发关键词与场景清单，使 Agent 能稳定判断何时启用本 skill。

#### Scenario: 用户要求使用 Node-API 实现跨语言交互
- **WHEN** 用户提出「用 Node-API 实现 ArkTS 与 C/C++ 交互」「napi 怎么注册模块」「napi_wrap 怎么用」「napi_threadsafe_function 怎么用」等 Node-API 类请求
- **THEN** Agent 启用 `arkts-ndk-dev` skill，按工作流先读 `references/INDEX.md`，再加载 `05-node-api-development.md` 与 `06-node-api-best-practices.md`，给出符合鸿蒙规范的 Node-API 代码

#### Scenario: 用户要求创建/构建 NDK 工程
- **WHEN** 用户提出「创建 Native C++ 工程」「NDK 工程怎么构建」「CMake 怎么配」「ohos.toolchain.cmake 怎么用」等 NDK 工程类请求
- **THEN** Agent 启用本 skill，加载 `02-create-ndk-project.md` 与 `03-build-ndk-project.md`，给出正确的工程创建与 CMake 配置

#### Scenario: 用户要求使用 Rawfile 或 NativeBundle 接口
- **WHEN** 用户提出「Native 侧读 rawfile」「OH_ResourceManager 怎么用」「Native Bundle 获取应用信息」等资源管理类请求
- **THEN** Agent 启用本 skill，加载 `07-rawfile.md` 或 `08-native-bundle.md`，给出正确的接口调用代码

#### Scenario: 用户要求 NDK 调试或硬件兼容性配置
- **WHEN** 用户提出「NDK 内存错误检测」「ASan 怎么开」「LLDB 调试」「ABI 兼容性」「Neon 指令」等调试/硬件类请求
- **THEN** Agent 启用本 skill，加载 `10-debugging-profiling.md` 或 `11-hardware-compatibility.md`，给出配置步骤与注意事项

### Requirement: 离线参考文档集

`arkts-ndk-dev` skill MUST 提供 `references/` 目录，包含覆盖 HarmonyOS NDK 开发的离线参考文档。文档 MUST 按场景/主题拆分为独立文件，并配备 `INDEX.md` 索引文件。文档内容 MUST 来源于华为开发者官网公开文档的离线快照，每份文档 MUST 标注上游 URL 与抓取时间。

#### Scenario: 按需加载文档
- **WHEN** Agent 处理一个具体的 NDK / Node-API 任务
- **THEN** Agent 先读 `references/INDEX.md` 获取「任务类型 → 必读文件」映射，再按需加载对应的 1-3 份文档，而非一次性读取全部文档

#### Scenario: 文档覆盖范围
- **WHEN** 检查 `references/` 目录内容
- **THEN** 目录 MUST 至少包含以下文件：`INDEX.md`、`01-ndk-overview.md`（NDK 导读）、`02-create-ndk-project.md`（创建工程）、`03-build-ndk-project.md`（构建工程）、`04-node-api-overview.md`（Node-API 概览）、`05-node-api-development.md`（Node-API 开发流程）、`06-node-api-best-practices.md`（Node-API 最佳实践与红线）、`07-rawfile.md`（Rawfile）、`08-native-bundle.md`（NativeBundle）、`09-build-toolchain.md`（编译工具链）、`10-debugging-profiling.md`（调试性能分析）、`11-hardware-compatibility.md`（硬件兼容性）

### Requirement: INDEX 索引文件

`references/INDEX.md` MUST 作为 Agent 的必先阅读文件，提供「任务类型 → 必读文件」映射表、各文档角色说明、关键红线速记，使 Agent 能在不读全所有文档的前提下定位到正确的参考文档。

#### Scenario: Agent 首次进入 skill
- **WHEN** Agent 启用 `arkts-ndk-dev` skill 处理任意任务
- **THEN** Agent MUST 先读 `references/INDEX.md`，再根据任务类型按映射表加载具体文档

#### Scenario: 索引内容完整性
- **WHEN** 阅读 `INDEX.md`
- **THEN** 文件 MUST 包含：各文档的角色一句话说明、按任务类型（Node-API 开发 / NDK 工程创建与构建 / Rawfile / NativeBundle / 编译工具链 / 调试性能分析 / 硬件兼容性）的查阅路径表、Node-API 关键红线速记

### Requirement: Node-API 开发流程文档

`05-node-api-development.md` MUST 提供使用 Node-API 实现 ArkTS 与 C/C++ 跨语言交互的完整开发流程，包含模块注册、接口映射、类型声明、CMake 配置、参数获取与类型转换、ArkTS 侧调用的完整代码示例，以及约束限制。

#### Scenario: 模块注册流程
- **WHEN** Agent 需要指导用户注册一个 Native 模块
- **THEN** 文档 MUST 提供 `napi_module` 结构体定义 + `__attribute__((constructor))` 自动注册的完整代码模板，并说明 `nm_modname` 必须与 so 名完全匹配（区分大小写）

#### Scenario: 接口映射流程
- **WHEN** Agent 需要指导用户将 C/C++ 方法暴露给 ArkTS
- **THEN** 文档 MUST 提供 `napi_property_descriptor` 数组 + `napi_define_properties` 的完整代码模板，以及 `index.d.ts` 声明与 `oh-package.json5` 关联配置

#### Scenario: 参数获取与类型转换
- **WHEN** Agent 需要指导用户在 C/C++ 侧获取 ArkTS 传入的参数并返回结果
- **THEN** 文档 MUST 提供 `napi_get_cb_info` 获取参数、`napi_get_value_*` 系列转换类型、`napi_create_*` 系列返回结果的代码示例

### Requirement: Node-API 最佳实践与红线文档

`06-node-api-best-practices.md` MUST 提供 Node-API 开发规范与红线清单，覆盖参数获取规范、生命周期管理、上下文敏感、异常处理、异步任务、对象绑定、高性能数组、数据转换优化、模块注册与命名约束、dlopen 场景、napi_create_external 限制、buffer 释放等。每条红线 MUST 说明违规后果与正确做法。

#### Scenario: 线程安全红线
- **WHEN** Agent 写出或审查涉及多线程的 Node-API 代码
- **THEN** Agent MUST 确保代码遵循以下红线：Node-API 接口只能在 ArkTS 线程使用；`napi_env` 与特定 ArkTS 线程绑定，禁止跨线程使用；跨线程通信 MUST 使用 `napi_threadsafe_function` 系列接口，而非 `uv_queue_work`

#### Scenario: 生命周期管理红线
- **WHEN** Agent 写出在循环中频繁创建 JS 对象的 Node-API 代码
- **THEN** Agent MUST 确保代码使用 `napi_open_handle_scope` / `napi_close_handle_scope` 管理 `napi_value` 生命周期，避免内存泄漏

#### Scenario: 对象绑定红线
- **WHEN** Agent 写出使用 `napi_wrap` 的代码
- **THEN** Agent MUST 确保当 `napi_wrap` 最后一个参数 `result` 不为 nullptr 时，需手动调用 `napi_remove_wrap` 释放 `napi_ref`；一般传 nullptr 即可由系统管理

#### Scenario: 高性能数组红线
- **WHEN** Agent 写出在 Node-API 中存储值类型数据的代码
- **THEN** Agent MUST 优先使用 ArrayBuffer 代替 JSArray（性能差异可达 400 倍以上），使用 `napi_create_external_arraybuffer` + `napi_create_typedarray` 创建 TypedArray

#### Scenario: 模块注册与命名红线
- **WHEN** Agent 写出模块注册代码
- **THEN** Agent MUST 确保：Init 函数加 static；注册入口函数名确保唯一；`nm_modname` 与 so 名完全匹配（区分大小写）；一个 so 只能注册一个模块

#### Scenario: buffer 释放红线
- **WHEN** Agent 写出使用 `napi_get_arraybuffer_info` 的代码
- **THEN** Agent MUST 确保不手动释放返回的 data 指针（由引擎管理），防止重复释放导致崩溃

### Requirement: SKILL.md 工作流

`SKILL.md` MUST 定义严格的工作流，使 Agent 在启用本 skill 时按固定步骤执行：先读 INDEX → 按场景加载文档 → 写代码/配工具链 → 核对红线 → 引用来源。`SKILL.md` MUST 包含触发条件、与已有 skill 的边界、工作流步骤、Node-API 红线速查表、高频代码模板、目录结构、文档来源与维护说明。

#### Scenario: 工作流执行
- **WHEN** Agent 启用本 skill 处理任务
- **THEN** Agent MUST 按以下步骤执行：(1) 读 `references/INDEX.md`；(2) 按任务类型加载对应文档；(3) 按文档内容给出代码/配置；(4) 核对红线速查表；(5) 在回复中标注引用的 reference 文件

#### Scenario: Node-API 红线速查
- **WHEN** Agent 给出 Node-API 代码
- **THEN** Agent MUST 自检以下红线：(1) 线程安全——Node-API 只能在 ArkTS 线程使用，跨线程用 napi_threadsafe_function；(2) 生命周期——循环中创建 JS 对象必须加 handle_scope；(3) 模块注册——nm_modname 与 so 名完全匹配，一个 so 只能注册一个模块；(4) 异步任务——推荐 napi_threadsafe_function，不推荐 uv_queue_work；(5) 对象绑定——napi_wrap result 传 nullptr 由系统管理；(6) 性能——ArrayBuffer 代替 JSArray

### Requirement: 代码准确性

本 skill 给出的所有 Node-API 代码 MUST 遵循 HarmonyOS Node-API 规范，不得用 Node.js N-API 的不兼容接口替代。模块注册方式（`napi_module` + `__attribute__((constructor))`）、线程模型（env 与 ArkTS 线程绑定）、异步任务推荐方式（`napi_threadsafe_function`）MUST 与官方文档一致。对版本相关的 API 或行为差异，MUST 在文档中标注说明。

#### Scenario: 模块注册方式
- **WHEN** Agent 指导用户注册 Native 模块
- **THEN** Agent MUST 使用 `napi_module` 结构体 + `__attribute__((constructor)) void RegisterXxxModule()` 方式，而非 Node.js 的 `napi_register_module_v1` 导出方式

#### Scenario: 异步任务方式
- **WHEN** Agent 指导用户在 Native 侧执行异步任务
- **THEN** Agent MUST 推荐 `napi_threadsafe_function` 系列接口，而非 `uv_queue_work`；若用户代码使用 `uv_queue_work`，MUST 提示回调需加 handle_scope 并建议迁移

### Requirement: 与已有 skill 的边界

`SKILL.md` MUST 明确本 skill 与 `arkts-helper`、`arkts-debug`、`arkts-build` 的职责边界，使用交叉引用而非互斥策略。本 skill 负责「NDK 代码怎么写 / CMake 怎么配 / Node-API 怎么用」，不负责「ArkTS 语法/迁移」「ArkTS 编译报错修复」「命令行构建/部署」；当 NDK 任务中遇到这三类问题时，MUST 提示用户交叉引用对应 skill。

#### Scenario: NDK 任务涉及 ArkTS 侧代码
- **WHEN** 用户在 NDK 开发中遇到 ArkTS 语法/迁移问题
- **THEN** Agent 在本 skill 内给出 NDK 层建议后，MUST 提示用户使用 `arkts-helper` skill 处理 ArkTS 语法层问题

#### Scenario: NDK 任务涉及构建命令
- **WHEN** 用户要求构建包含 native C++ 模块的工程
- **THEN** 本 skill 只覆盖「CMakeLists.txt 怎么写 / CMake 工具链变量怎么配 / ohos.toolchain.cmake 参数」；`hvigorw` 构建命令本身 MUST 交叉引用 `arkts-build` skill

#### Scenario: NDK 任务涉及 ArkTS 编译报错
- **WHEN** 用户在 NDK 开发中遇到 ArkTS 编译报错
- **THEN** Agent MUST 提示用户使用 `arkts-debug` skill 处理编译报错

### Requirement: 调试性能分析与硬件兼容性概览化

`10-debugging-profiling.md` 和 `11-hardware-compatibility.md` MUST 以概览形式提供关键配置步骤与官方链接，不逐个展开完整文档。概览 MUST 包含：ASan 启用方式、LLDB 基本使用、HarmonyOS ABI 类型、CPU 特性查询、Neon 指令扩展启用方式。

#### Scenario: ASan 内存检测
- **WHEN** 用户要求检测 C/C++ 内存错误
- **THEN** Agent 从 `10-debugging-profiling.md` 获取 ASan 启用配置步骤，给出 CMake 编译选项与 DevEco Studio 配置方式

#### Scenario: 硬件兼容性查询
- **WHEN** 用户询问 HarmonyOS ABI 或 CPU 特性
- **THEN** Agent 从 `11-hardware-compatibility.md` 获取 ABI 类型列表与 CPU 特性查询方式，给出概览说明并提示查阅官网详情
