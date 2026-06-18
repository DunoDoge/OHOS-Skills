---
name: arkts-ndk-dev
description: Use when developing HarmonyOS NDK / Node-API / C++ interop code, configuring CMake toolchain for native builds, or handling napi_wrap, napi_threadsafe_function, napi_env threading, module registration, Rawfile, NativeBundle, ASan, LLDB, ABI, or Neon. Triggers include Node-API, napi, NDK, C++ interop, Native, CMake, so, napi_wrap, napi_threadsafe_function, Rawfile, NativeBundle, ASan, LLDB, ABI, Neon, ohos.toolchain.cmake, libace_napi.z.so, napi_module_register, napi_define_properties, napi_get_cb_info, napi_create_external, napi_open_handle_scope, cross-language, cross-thread, or any topic under the HarmonyOS NDK development documentation. Loads the offline NDK reference set so the agent can give real HarmonyOS Node-API code instead of guessing from Node.js N-API knowledge.
---

# arkts-ndk-dev

HarmonyOS 的 Node-API 虽基于 Node.js 18.x LTS 的 Node-API 规范扩展，但**不完全兼容**：

- 模块注册方式不同：鸿蒙使用 `napi_module` 结构体 + `__attribute__((constructor))` 自动注册，而非 Node.js 的 `napi_register_module_v1`。
- 线程模型不同：Node-API 接口只能在 ArkTS 线程使用，`napi_env` 与特定 ArkTS 线程绑定；跨线程必须使用 `napi_threadsafe_function`，而非 Node.js 社区常用的 `uv_queue_work`。
- SO 命名强约束：`nm_modname` 必须与 so 名完全匹配（区分大小写），一个 so 只能注册一个模块。
- 性能陷阱：JSArray vs ArrayBuffer 性能差距达 400 倍以上，`napi_wrap` 的 result 参数传 nullptr vs 非 nullptr 有不同的内存管理语义。

Agent 凭通用 Node.js N-API 经验写出的代码，在鸿蒙上**极易崩溃或内存泄漏**。本 skill 提供的离线参考文档（`references/` 下 11 篇 + INDEX）是华为官方「NDK 开发」系列文档的离线副本，是处理 NDK / Node-API 任务时的**权威依据**。

## 何时启用本 skill

满足以下任一条件就应当遵循本 skill 的工作流程：

- 用户要求**使用 Node-API 实现 ArkTS 与 C/C++ 交互**（模块注册、接口映射、类型转换、回调调用）
- 用户提到 `napi_*` 系列接口（`napi_wrap`、`napi_threadsafe_function`、`napi_get_cb_info`、`napi_define_properties`、`napi_open_handle_scope` 等）
- 用户要求**创建/构建 NDK 工程**（Native C++ 模板、CMakeLists.txt、ohos.toolchain.cmake、CMake 命令行构建）
- 用户要求**配置编译工具链**（CMake/GN/Make/Configure 交叉编译、lycium 框架）
- 用户要求**Native 侧资源管理**（Rawfile 读写、NativeBundle 获取应用信息）
- 用户要求**Native 子线程与 UI 主线程通信**（跨线程回调、线程安全函数）
- 用户要求**NDK 调试/性能分析**（ASan 内存检测、LLDB 调试）
- 用户要求**硬件兼容性配置**（ABI 设置、CPU 特性、Neon 指令扩展）
- 用户提到 `libace_napi.z.so`、`napi_module_register`、`napi_onLoad`、`napi_create_external`、`napi_coerce_to_native_binding_object` 等鸿蒙 NDK 专有接口
- 项目中存在 `CMakeLists.txt` 且包含 `libace_napi.z.so` 链接，或 `entry/src/main/cpp/` 目录

不要在「纯 ArkTS 语法/迁移」「ArkTS 编译报错修复」「命令行构建/部署」场景下强行套用本 skill；这些场景请使用对应 skill（见下文边界）。

## 与已有 skill 的边界

本 skill 负责**「NDK 代码怎么写 / CMake 怎么配 / Node-API 怎么用」**，不负责**「ArkTS 语法怎么改」「编译报错怎么修」「构建命令怎么调」**。当 NDK 任务中遇到以下问题时，应交叉引用对应 skill：

| 问题类型 | 交叉引用 skill | 边界说明 |
| --- | --- | --- |
| ArkTS 语法/迁移/编码规范 | `arkts-helper` | 本 skill 只讲 Node-API/C++ 侧，不讲 ArkTS 语法 |
| ArkTS 编译报错（`arkts-no-*` 规则等） | `arkts-debug` | NDK 开发中遇到的 ArkTS 编译报错，用 `arkts-debug` 修复代码 |
| 命令行构建/部署/签名/流水线 | `arkts-build` | 本 skill 只覆盖「CMakeLists.txt 怎么写 / CMake 工具链变量怎么配」；`hvigorw` 构建命令本身归 `arkts-build` |

## 工作流程（严格遵守）

### 1. 先读索引，再决定看哪份文档

任何 NDK / Node-API 任务开始前，**必须先读** `references/INDEX.md`。它给出 11 份文档的角色、按任务类型的查阅路径以及 Node-API 关键红线速记，能避免你把整个 reference 目录全文读进上下文。

### 2. 按任务类型加载对应文档

| 任务类型 | 必读文件（在 `references/` 下） |
| -------- | ------------------------------ |
| Node-API 模块开发（注册/映射/类型转换） | `05-node-api-development.md` |
| Node-API 红线排查（线程安全/生命周期/崩溃/性能） | `06-node-api-best-practices.md` |
| Node-API 架构理解（组成/流程/与 Node.js 差异） | `04-node-api-overview.md` |
| 创建 NDK 工程 | `02-create-ndk-project.md` |
| 构建 NDK 工程（CMake/toolchain/命令行） | `03-build-ndk-project.md` |
| Rawfile 资源访问 | `07-rawfile.md` |
| Native Bundle 获取应用信息 | `08-native-bundle.md` |
| 编译工具链配置（CMake/GN/Make/Configure/lycium） | `09-build-toolchain.md` |
| 跨语言复杂参数传递 | `09-build-toolchain.md`（跨语言调用复杂参数传递一节） |
| Native 子线程与 UI 主线程通信 | `09-build-toolchain.md`（Native 侧子线程与 UI 主线程通信一节） |
| C/C++ 内存错误检测 | `10-debugging-profiling.md` |
| LLDB 调试 | `10-debugging-profiling.md` |
| ABI / CPU 特性 / Neon | `11-hardware-compatibility.md` |
| NDK 入门概览 | `01-ndk-overview.md` |

读取文档时优先用 `Grep`/`Read` 的 offset/limit 定位段落，不要把大文件一次性读全。

### 3. 落到代码时严格执行红线

写出 / 修改 Node-API 代码前自检以下高频红线（详细规则以文档原文为准）：

- **Node-API 只能在 ArkTS 线程使用**：`napi_env` 与 ArkTS 线程绑定，禁止跨线程传递；跨线程通信必须使用 `napi_threadsafe_function`
- **循环中创建 JS 对象必须加 scope**：`napi_open_handle_scope` / `napi_close_handle_scope` 成对使用
- **`nm_modname` 与 so 名完全匹配**：区分大小写；一个 so 只能注册一个模块；Init 函数加 static
- **异步任务推荐 `napi_threadsafe_function`**：不推荐 `uv_queue_work`；若用 `uv_queue_work`，回调必须加 `handle_scope`
- **`napi_wrap` result 传 nullptr**：由系统管理；传非 nullptr 需手动 `napi_remove_wrap`
- **ArrayBuffer 代替 JSArray**：存储值类型数据时性能差 400 倍以上
- **`napi_get_arraybuffer_info` 返回的 data 不可手动释放**：由引擎管理
- **`napi_create_external` 创建的对象仅当前线程可用**：跨线程需 `napi_coerce_to_native_binding_object`

不确定时，**回 `references/06-node-api-best-practices.md` 搜索相关红线原文**，再下笔。

### 4. 引用文档时给出来源

回答用户的 Node-API / NDK 问题时，建议在回复结尾标注引用，例如：

> 依据 `references/06-node-api-best-practices.md` 中「线程安全」一节。

### 5. 不要替换或省略本 skill 的检查

即便用户的 Node-API 代码「看起来就是合法的 Node.js N-API」，在 HarmonyOS 上下文中也要按本 skill 的红线核查后再回答；不能默认 Node.js N-API 知识可直接套用。

## Node-API 红线速查表

| 类别 | 红线 | 违规后果 |
| --- | --- | --- |
| **线程安全** | Node-API 只能在 ArkTS 线程使用；`napi_env` 禁止跨线程传递；跨线程用 `napi_threadsafe_function` | 跨线程使用 env 导致崩溃 |
| **生命周期** | 循环中频繁创建 JS 对象必须加 `napi_open_handle_scope` / `napi_close_handle_scope` | 内存泄漏 |
| **模块注册** | `nm_modname` 与 so 名完全匹配（区分大小写）；一个 so 只能注册一个模块；Init 加 static；注册入口函数名唯一 | 模块加载失败或匹配到错误模块 |
| **异步任务** | 推荐 `napi_threadsafe_function`，不推荐 `uv_queue_work`；若用 `uv_queue_work`，回调必须加 `handle_scope` | 内存泄漏或崩溃 |
| **对象绑定** | `napi_wrap` result 传 nullptr 由系统管理；传非 nullptr 需手动 `napi_remove_wrap` | 内存泄漏（napi_ref 未释放） |
| **性能** | ArrayBuffer 代替 JSArray（性能差 400 倍+）；减少数据转换次数；避免不必要复制 | 性能严重下降 |

## 高频代码模板

### 模块注册模板

```cpp
EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports) {
    napi_property_descriptor desc[] = {
        {"methodName", nullptr, MethodName, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "entry",  // 必须与 so 名匹配：libentry.so
    .nm_priv = ((void*)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterEntryModule() {
    napi_module_register(&demoModule);
}
```

### 接口映射模板

```cpp
static napi_value MethodName(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value argv[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, argv, nullptr, nullptr);

    // 参数获取与类型转换...
    double value0;
    napi_get_value_double(env, argv[0], &value0);

    // 返回结果
    napi_value result;
    napi_create_double(env, value0, &result);
    return result;
}
```

### 参数获取与类型转换模板

```cpp
// 获取字符串
size_t strSize;
char strBuf[256];
napi_get_value_string_utf8(env, argv[0], strBuf, sizeof(strBuf), &strSize);

// 获取整数
int32_t intValue;
napi_get_value_int32(env, argv[0], &intValue);

// 获取布尔值
bool boolValue;
napi_get_value_bool(env, argv[0], &boolValue);

// 创建对象并设置属性
napi_value obj;
napi_create_object(env, &obj);
napi_value propValue;
napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &propValue);
napi_set_named_property(env, obj, "key", propValue);
```

### napi_threadsafe_function 模板

```cpp
napi_threadsafe_function tsFn;

// 主线程：创建线程安全函数
napi_value workName;
napi_create_string_utf8(env, "MyThreadSafeFunc", NAPI_AUTO_LENGTH, &workName);
napi_create_threadsafe_function(env, jsCallback, nullptr, workName, 0, 1,
    nullptr, nullptr, nullptr, CallJsCallback, &tsFn);

// 子线程：调用线程安全函数
napi_acquire_threadsafe_function(tsFn);
napi_call_threadsafe_function(tsFn, data, napi_tsfn_nonblocking);
napi_release_threadsafe_function(tsFn, napi_tsfn_release);

// 回调实现
static void CallJsCallback(napi_env env, napi_value js_cb, void* context, void* data) {
    // 在 ArkTS 线程中执行，可以安全使用 Node-API
    napi_value argv;
    napi_create_int32(env, 42, &argv);
    napi_value result;
    napi_call_function(env, nullptr, js_cb, 1, &argv, &result);
}
```

## 目录结构

```
arkts-ndk-dev/
├── SKILL.md                                          # 本文件
└── references/
    ├── INDEX.md                                      # 必先阅读
    ├── 01-ndk-overview.md                            # NDK 开发导读
    ├── 02-create-ndk-project.md                      # 创建 NDK 工程
    ├── 03-build-ndk-project.md                       # 构建 NDK 工程
    ├── 04-node-api-overview.md                       # Node-API 概览与架构
    ├── 05-node-api-development.md                    # Node-API 开发流程（核心）
    ├── 06-node-api-best-practices.md                 # Node-API 开发规范与红线（核心）
    ├── 07-rawfile.md                                 # Rawfile 开发指导
    ├── 08-native-bundle.md                           # NativeBundle 开发指导
    ├── 09-build-toolchain.md                         # 编译工具链配置
    ├── 10-debugging-profiling.md                     # 调试和性能分析
    └── 11-hardware-compatibility.md                  # 硬件兼容性
```

## 文档来源与维护

- 上游：华为开发者官网「文档中心 › 应用开发 › NDK 开发」系列，路径 `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/` 下：
  - `ndk-development-overview`（NDK 导读）
  - `create-with-ndk`（创建工程）
  - `build-with-ndk`（构建工程）
  - `coding`（代码开发，含 Node-API）
  - `rawfile-guidelines`（Rawfile）
  - `native-bundle-guidelines`（NativeBundle）
  - `build-toolchain`（编译工具链）
  - `debugging-profiling`（调试性能分析）
  - `hardware-compatibility`（硬件兼容性）
- 文档为 2026-06-18 抓取的离线快照，每份文档顶部标注了上游 URL 与抓取时间。
- 如需更新到最新版本，重新运行抓取（从上游 URL `curl`/WebFetch 各 md 文件覆盖到 `references/` 即可）；若需扩充文件清单，请同步更新 `references/INDEX.md`。
- Node-API 接口会随 HarmonyOS 版本更新，遇到不确定的接口请查阅官网最新文档。
