---
name: arkts-ndk-dev
description: Use when building HarmonyOS / OpenHarmony NDK (native C/C++) modules, writing or reviewing Node-API (`napi_*`) or JSVM-API (`OH_JSVM_*`) code, configuring CMake / DevEco Studio native projects, dealing with `.so` / ABI / `arm64-v8a` issues, ArkTS to C++ interop, `napi_threadsafe_function`, `napi_async_work`, `napi_wrap`, Sendable native binding, fdsan, ASan, OpenHarmony musl / libc++, Rawfile, QoS, Neon, or any topic under `application-dev/napi/` of the OpenHarmony docs. Loads the offline NDK reference set so the agent can answer and code against the real spec instead of guessing from generic Node.js N-API knowledge.
---

# arkts-ndk-dev

HarmonyOS / OpenHarmony 的 NDK（Native Development Kit）和社区 Node.js / Android NDK 都**不是同一套东西**：

- 它的 Node-API 是**裁剪 + 扩展**版的社区 N-API：保留了核心 `napi_*` 接口，但增加了 Sendable 对象、`napi_load_module_with_info`、扩展事件循环 / 上下文 / 临界区等接口；社区 Node 上能用的写法在 OpenHarmony 上**不一定生效**，反之亦然。
- 工具链是 **OpenHarmony NDK + musl libc + libc++**，CMake 必须走官方工具链文件并通过 `OHOS_STL`、`OHOS_PLATFORM`、`OHOS_ARCH` 等变量定参；不能用宿主 gcc / glibc 习惯。
- ABI 仅限 `arm64-v8a` / `x86_64`（HarmonyOS NEXT 实机只剩 arm64），`.so` 必须放到 `libs/<abi>/`。
- 跨语言交互的红线（线程绑定、handle scope、pending exception、引用计数）和社区 N-API **有差异**，凭 Node.js 经验下笔极易写出运行期崩溃。

本 skill 提供的离线参考文档（`references/` 下 42 篇官方文档）是 OpenHarmony 官方 `application-dev/napi/` 一节的离线副本，是处理 NDK 任务时的**权威依据**。

## 何时启用本 skill

满足以下任一条件就应当遵循本 skill 的工作流程：

- 用户在写、改、审 OpenHarmony / HarmonyOS 工程下的 C / C++ / `.cpp` / `.h` 代码，且涉及 `napi_*` / `OH_JSVM_*` / `Init` 注册函数 / `napi_module_register`
- 项目根 / 模块下存在 `CMakeLists.txt` + `src/main/cpp/` + `oh-package.json5`，或工程使用 DevEco Studio Native C++ 模板
- 用户提到 HarmonyOS NDK、OpenHarmony NDK、Node-API、N-API（在 HarmonyOS 上下文）、JSVM-API、`napi_threadsafe_function`、`napi_async_work`、`napi_wrap`、Sendable native binding、`napi_load_module_with_info`、ohos-sdk、`OHOS_STL`、musl、libc++、ASan、fdsan、Rawfile、QoS、ohos-abi、`arm64-v8a` HarmonyOS、Neon HarmonyOS
- 用户问「ArkTS 怎么调 C++」「C++ 怎么回调 ArkTS」「native 异步任务返回 Promise 怎么写」「`napi_status` 报某错误码什么意思」「DevEco Studio 怎么链接第三方 .so」「.so ABI 兼容性」「OpenHarmony 上能不能用 std::thread / pthread / libuv」

不要在「纯 Node.js / Electron / 通用 V8 嵌入」场景下强行套用本 skill；社区 Node N-API 任务请使用更通用的资料。

## 工作流程（严格遵守）

### 1. 先读索引，再决定看哪份文档

任何 NDK 任务开始前，**必须先读** `references/INDEX.md`。它给出 42 份文档的角色、按场景的查阅路径以及关键红线速记，能避免你把整个 reference 目录全文读进上下文。

### 2. 按问题类型加载对应文档

| 任务类型 | 必读文件（在 `references/` 下） |
| -------- | ------------------------------ |
| 整体定位 / 与 ArkTS 关系 | `01-ndk-development-overview.md` |
| 新建 / IDE 构建 native 工程 | `02-create-with-ndk.md` + `04-build-with-ndk-ide.md` |
| **命令行 CMake 构建、工具链变量、链接 .so** | `03-build-with-ndk-overview.md` + `05-build-with-ndk-cmake.md` + `06-build-with-ndk-prebuilts.md` |
| C/C++ 标准库（musl / libc++）链接行为、fdsan | `08-c-cpp-overview.md` + `09-fdsan.md` |
| **`napi_*` 接口该怎么调（接口总览）** | `12-napi-data-types-interfaces.md` |
| **`napi_status` 错误码含义** | `11-napi-status-introduction.md`（按错误码 grep） |
| **Node-API 红线 / 规范** | `13-napi-guidelines.md` |
| 写第一个跨语言模块的整体流程 | `14-use-napi-process.md` |
| 处理某种值类型（string/array/object/class/function/promise/error 等） | `15-23` 中对应专题 |
| 异步任务 / 跨 native 线程回调 ArkTS | `24-use-napi-asynchronous-task.md` + `25-use-napi-thread-safety.md` |
| native 对象绑到 ArkTS（普通 / Sendable） | `26-use-napi-object-wrap.md` + `27-use-sendable-napi.md` |
| native 主动加载 ArkTS 模块 | `28-use-napi-load-module-with-info.md` |
| 崩溃 / 异常日志分析 | `29-use-napi-about-crash.md` + `37` + `38` |
| 嵌入独立 JS 引擎（V8） | `31-jsvm-introduction.md` → `32` → `33` |
| Rawfile / QoS / NativeBundle | `34` / `35` / `36` |
| ABI / CPU / Neon | `40-ohos-abi.md` + `41` + `42` |

`11`、`12`、`32` 是大文件（>40KB），读取时**必须**用 `Grep` / `Read` 的 offset/limit 定位段落，不要一次性读全。

### 3. 落到代码时严格执行红线

写出 / 修改 NDK 代码前自检以下高频红线（详细规则以文档原文为准）：

- **每次调 `napi_xxx` 都判断返回值**：`!= napi_ok` 时通常先 `napi_get_and_clear_last_exception(env, &err)` 处理 pending exception，再决定是否抛错或退出当前 callback；异常未清理时不要继续调其他 napi 接口（13 / 22）
- **`napi_value` 不能跨 handle scope / callback / `napi_env` 使用**：需要长期保留必须 `napi_create_reference` → `napi_ref`；析构时 `napi_delete_reference`，并配套 `napi_reference_ref/unref` 管理引用计数
- **`napi_env` 与线程一对一**：`napi_env` 只能在创建它的 ArkTS 线程上使用；任意 native 线程访问 ArkTS 必须走 `napi_threadsafe_function` 或 `napi_async_work`（24 / 25）
- **耗时 native 工作不能直接在 napi callback 里跑**：用 `napi_create_async_work` 在 worker 线程执行，complete 回到 ArkTS 线程再回调；UI / 主线程被阻塞会造成卡顿（24 + 35）
- **跨进程 / 跨线程数据传递走 Sendable 或裸内存**：普通 `napi_value` 不可 share；多线程共享 native 对象要用 Sendable wrap（27）
- **`napi_wrap` 必须配 finalizer**：在析构回调里释放 native C++ 对象，否则 GC 后悬挂指针（26）
- **CMake 走官方工具链**：`-DCMAKE_TOOLCHAIN_FILE=$OHOS_NDK/build/cmake/ohos.toolchain.cmake -DOHOS_STL=c++_shared -DOHOS_ARCH=arm64-v8a -DOHOS_PLATFORM=OHOS`；不要替换为宿主 gcc / clang（05）
- **`OHOS_STL` 必须全工程一致**：所有 .so 用同一种（推荐 `c++_shared`），混用 `c++_static` 会出现 STL 实例分裂导致崩溃（05 / 08）
- **ABI 只允许 arm64-v8a / x86_64**：`build-profile.json5` 的 `abiFilters` 与 `libs/<abi>/` 目录命名严格对应（40）
- **预构建 .so 必须依赖 OpenHarmony NDK 编译产物**：直接拿 Android NDK / Linux gcc 产物会因为 musl / libc++ ABI 不一致崩溃（06 + 08）
- **资源文件读取走 Rawfile API**：不能假定 `/data/...` 文件路径布局，跨设备会失效（34）
- **不要 `dlopen` 系统私有库 / 越过白名单**：OpenHarmony NDK 暴露的 .so 列表是有限白名单
- **fdsan 默认开启**：随便 `close(fd)` 一个被 owner 标记的 fd 会被 abort（09）
- **catch native exception 不能让其穿越 napi 边界**：所有抛到 ArkTS 的错都要先转成 `napi_throw_*` / `napi_throw_error`（22）
- **module 注册唯一**：`napi_module_register` 只能在 `__attribute__((constructor))` 中调一次，重复注册会冲突
- **JSVM 与 Node-API 不通用**：JSVM 是独立 V8 引擎，`napi_value` 与 `JSVM_Value` 不能互转，不要混用（31）

不确定时，**回 `references/13-napi-guidelines.md` 或对应专题文档搜索原文**，再下笔。

### 4. 引用文档时给出来源

回答用户的接口 / 红线类问题时，建议在回复结尾标注引用，例如：

> 依据 `references/13-napi-guidelines.md` 中关于 `napi_threadsafe_function` 一节，以及 `references/25-use-napi-thread-safety.md` 的示例。

这样用户可以快速核对原文。

### 5. 不要替换或省略本 skill 的检查

即便用户的代码段「看起来就是合法社区 N-API」，在 OpenHarmony 上下文中也要按本 skill 的规则核查后再回答；不能默认 Node.js / Android NDK 知识可直接套用。

## 目录结构

```
arkts-ndk-dev/
├── SKILL.md                                           # 本文件
└── references/
    ├── INDEX.md                                       # 必先阅读
    ├── LICENSE                                        # 上游许可证
    ├── NOTICE.md                                      # 来源与归属
    ├── 01-ndk-development-overview.md
    ├── 02-create-with-ndk.md
    ├── 03-build-with-ndk-overview.md
    ├── 04-build-with-ndk-ide.md
    ├── 05-build-with-ndk-cmake.md
    ├── 06-build-with-ndk-prebuilts.md
    ├── 07-develop-code-overview.md
    ├── 08-c-cpp-overview.md
    ├── 09-fdsan.md
    ├── 10-napi-introduction.md
    ├── 11-napi-status-introduction.md
    ├── 12-napi-data-types-interfaces.md
    ├── 13-napi-guidelines.md
    ├── 14-use-napi-process.md
    ├── 15-use-napi-basic-data-types.md
    ├── 16-use-napi-about-string.md
    ├── 17-use-napi-about-array.md
    ├── 18-use-napi-about-arraybuffer.md
    ├── 19-use-napi-about-object.md
    ├── 20-use-napi-about-class.md
    ├── 21-use-napi-about-function.md
    ├── 22-use-napi-about-error.md
    ├── 23-use-napi-about-promise.md
    ├── 24-use-napi-asynchronous-task.md
    ├── 25-use-napi-thread-safety.md
    ├── 26-use-napi-object-wrap.md
    ├── 27-use-sendable-napi.md
    ├── 28-use-napi-load-module-with-info.md
    ├── 29-use-napi-about-crash.md
    ├── 30-use-napi-faqs.md
    ├── 31-jsvm-introduction.md
    ├── 32-jsvm-data-types-interfaces.md
    ├── 33-jsvm-guidelines.md
    ├── 34-rawfile-guidelines.md
    ├── 35-qos-guidelines.md
    ├── 36-native-bundle-guidelines.md
    ├── 37-debug-performance-profiling-overview.md
    ├── 38-debug-asan.md
    ├── 39-hw-guide.md
    ├── 40-ohos-abi.md
    ├── 41-cpu-features.md
    └── 42-neon-guide.md
```

## 文档来源与维护

- 上游：<https://gitee.com/openharmony/docs>，路径 `zh-cn/application-dev/napi/`，分支 `master`
- 文档为 OpenHarmony 开源版本，与华为开发者官网「文档中心 › 应用开发 › NDK」一节同源
- 上游 Readme（含完整索引）：<https://gitee.com/openharmony/docs/raw/master/zh-cn/application-dev/napi/Readme-CN.md>
- 如需更新到最新版本，重新运行抓取（直接从上游 raw URL `curl` 各 md 文件覆盖到 `references/` 即可）；若需扩充文件清单，请同步更新 `references/INDEX.md`


