# HarmonyOS NDK 参考文档索引

本目录文档来源于 OpenHarmony 文档仓库 `zh-cn/application-dev/napi/`，与华为开发者文档站「应用开发 › NDK」一节同源（开源版本）。

- 上游仓库：<https://gitee.com/openharmony/docs>
- 上游路径：`zh-cn/application-dev/napi/`
- 分支：`master`
- 抓取时点：见各文件 git 历史；本地副本仅作离线参考使用

> 文档中的相对链接（如 `../reference/native-lib/musl.md`、`../arkts-utils/...`）指向上游仓库的兄弟目录，本地副本未跟随抓取。如需展开请到上游仓库查阅。

## 文件清单（按主题分组）

### A. 入门与工程创建（01-02）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 01 | [01-ndk-development-overview.md](./01-ndk-development-overview.md) | NDK 开发导读：定位、能力范围、与 ArkTS 关系、典型流程 |
| 02 | [02-create-with-ndk.md](./02-create-with-ndk.md) | 创建 NDK 工程（DevEco Studio Native C++ 模板） |

### B. 工程构建（03-06）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 03 | [03-build-with-ndk-overview.md](./03-build-with-ndk-overview.md) | NDK 工程构建概述 |
| 04 | [04-build-with-ndk-ide.md](./04-build-with-ndk-ide.md) | 使用 DevEco Studio 模板构建 |
| 05 | [05-build-with-ndk-cmake.md](./05-build-with-ndk-cmake.md) | **使用命令行 CMake 构建**（CMake 工具链、编译选项、链接 .so） |
| 06 | [06-build-with-ndk-prebuilts.md](./06-build-with-ndk-prebuilts.md) | 在 NDK 工程中使用预构建库（导入第三方 .so / .a） |

### C. 代码开发与 C/C++ 标准库（07-09）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 07 | [07-develop-code-overview.md](./07-develop-code-overview.md) | 代码开发概述（开放能力库索引） |
| 08 | [08-c-cpp-overview.md](./08-c-cpp-overview.md) | C/C++ 标准库（musl libc、libc++）机制概述 |
| 09 | [09-fdsan.md](./09-fdsan.md) | fdsan 文件描述符防护使用指导 |

### D. Node-API 规范与流程（10-14）— 跨语言交互核心

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 10 | [10-napi-introduction.md](./10-napi-introduction.md) | Node-API 简介、与社区版差异 |
| 11 | [11-napi-status-introduction.md](./11-napi-status-introduction.md) | Node-API **状态码**详解（`napi_status` 全集，按错误码 grep） |
| 12 | [12-napi-data-types-interfaces.md](./12-napi-data-types-interfaces.md) | Node-API **数据类型与接口总览**（`napi_value` / `napi_ref` 等） |
| 13 | [13-napi-guidelines.md](./13-napi-guidelines.md) | **Node-API 开发规范**（环境/作用域/线程/异常/引用计数红线） |
| 14 | [14-use-napi-process.md](./14-use-napi-process.md) | 使用 Node-API 实现跨语言交互的整体开发流程 |

### E. Node-API 使用指导（15-23）— 按值类型/能力分类

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 15 | [15-use-napi-basic-data-types.md](./15-use-napi-basic-data-types.md) | 基本数据类型（boolean / number / null / undefined） |
| 16 | [16-use-napi-about-string.md](./16-use-napi-about-string.md) | string 创建与读取（utf8 / utf16 / latin1） |
| 17 | [17-use-napi-about-array.md](./17-use-napi-about-array.md) | array 操作（含 typed array） |
| 18 | [18-use-napi-about-arraybuffer.md](./18-use-napi-about-arraybuffer.md) | arraybuffer 与外部内存 |
| 19 | [19-use-napi-about-object.md](./19-use-napi-about-object.md) | object 创建、属性读写 |
| 20 | [20-use-napi-about-class.md](./20-use-napi-about-class.md) | class 定义、构造、方法绑定 |
| 21 | [21-use-napi-about-function.md](./21-use-napi-about-function.md) | function 创建、调用 ArkTS 侧函数 |
| 22 | [22-use-napi-about-error.md](./22-use-napi-about-error.md) | 错误处理：`napi_throw_*`、pending exception 模型 |
| 23 | [23-use-napi-about-promise.md](./23-use-napi-about-promise.md) | Promise / deferred 异步返回 |

### F. Node-API 典型场景（24-30）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 24 | [24-use-napi-asynchronous-task.md](./24-use-napi-asynchronous-task.md) | **异步任务**（`napi_async_work`，避免阻塞 ArkTS 主线程） |
| 25 | [25-use-napi-thread-safety.md](./25-use-napi-thread-safety.md) | **线程安全函数**（`napi_threadsafe_function`，跨 native 线程回调 ArkTS） |
| 26 | [26-use-napi-object-wrap.md](./26-use-napi-object-wrap.md) | `napi_wrap` 将 native C++ 对象绑定到 ArkTS 对象 |
| 27 | [27-use-sendable-napi.md](./27-use-sendable-napi.md) | 与 Sendable ArkTS 对象绑定（多线程共享） |
| 28 | [28-use-napi-load-module-with-info.md](./28-use-napi-load-module-with-info.md) | native 侧主动加载 ArkTS 模块（`napi_load_module_with_info`） |
| 29 | [29-use-napi-about-crash.md](./29-use-napi-about-crash.md) | Node-API 异常日志 / 崩溃分析 |
| 30 | [30-use-napi-faqs.md](./30-use-napi-faqs.md) | Node-API 常见问题 FAQ |

### G. JSVM-API（31-33）— 独立 JS 引擎（区别于 ArkTS Runtime 的 Node-API）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 31 | [31-jsvm-introduction.md](./31-jsvm-introduction.md) | JSVM-API 简介（V8 引擎，与 Node-API 的差异） |
| 32 | [32-jsvm-data-types-interfaces.md](./32-jsvm-data-types-interfaces.md) | JSVM-API 数据类型与接口总览 |
| 33 | [33-jsvm-guidelines.md](./33-jsvm-guidelines.md) | JSVM-API 使用规范 |

### H. 资源 / 线程 / 包（34-36）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 34 | [34-rawfile-guidelines.md](./34-rawfile-guidelines.md) | Rawfile 资源访问（native 侧读 `resources/rawfile`） |
| 35 | [35-qos-guidelines.md](./35-qos-guidelines.md) | QoS 线程优先级开发指导 |
| 36 | [36-native-bundle-guidelines.md](./36-native-bundle-guidelines.md) | NativeBundle 包信息查询 |

### I. 调试与性能分析（37-38）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 37 | [37-debug-performance-profiling-overview.md](./37-debug-performance-profiling-overview.md) | 调试与性能分析概述 |
| 38 | [38-debug-asan.md](./38-debug-asan.md) | C/C++ 内存错误检测（ASan） |

### J. 硬件兼容性（39-42）

| 序号 | 文件 | 用途 |
| ---- | ---- | ---- |
| 39 | [39-hw-guide.md](./39-hw-guide.md) | 硬件兼容性简介 |
| 40 | [40-ohos-abi.md](./40-ohos-abi.md) | **OpenHarmony ABI**（arm64-v8a / x86_64） |
| 41 | [41-cpu-features.md](./41-cpu-features.md) | CPU 特性检测 |
| 42 | [42-neon-guide.md](./42-neon-guide.md) | 使用 Neon 指令扩展 |

## 按场景检索

| 你想做的事 | 优先看 |
| --------- | ----- |
| 第一次接触 NDK，搞清整体定位 | 01 → 07 → 10 |
| 新建一个 native C++ 工程 | 02 → 04 |
| 命令行 CMake 构建（不用 IDE） | 03 → 05 → 06 |
| 写第一个 C++ ↔ ArkTS 跨语言接口 | 14 → 13 → 15 |
| 查 `napi_xxx` 接口怎么调 | 12（接口总览） + 对应专题（15-28） |
| 看到 `napi_status` 非 0 想查错误码 | 11（按 `napi_invalid_arg`、`napi_pending_exception` 等 grep） |
| native 侧抛 / 接异常 | 22 + 29 |
| 不阻塞 ArkTS 的耗时 native 调用 | 24（async work）；跨 native 线程回调用 25 |
| 把 C++ 对象交给 ArkTS 持有 | 26（普通） / 27（Sendable 跨线程） |
| native 反向调用 ArkTS 模块 / 方法 | 28 + 21 |
| 性能 / 崩溃定位 | 29 + 37 + 38 |
| 选 ABI、链接 musl / libc++ | 08 + 40 |
| 用 SIMD 优化 | 41 + 42 |
| 嵌入 V8 跑独立 JS（非 ArkTS） | 31 → 32 → 33 |

## 关键红线速记（出自 13 / 22 / 29 / 40）

> 下列条目仅为提示，**任何具体编码决策都必须回到对应文档原文中确认**。

- **每次调用 `napi_xxx` 都要检查返回的 `napi_status`**：失败时通常需要 `napi_get_and_clear_last_exception` 处理 pending exception，不能在异常未清理时继续调用其他 napi 接口
- **`napi_value` 仅在所属 handle scope / callback 内有效**：跨 callback 必须用 `napi_create_reference` 提升为 `napi_ref`；跨 `napi_env` 严格禁止
- **`napi_env` 与线程绑定**：不能把 `napi_env` 直接传到任意 native 线程使用；跨线程访问 ArkTS 必须走 `napi_threadsafe_function` 或 async work
- **不要在 native 线程直接持有/回调 ArkTS 函数**：`napi_value`、`napi_ref` 都不可跨线程裸传
- **CMake 必须使用 OpenHarmony NDK 工具链**：通过 `OHOS_STL`、`OHOS_PLATFORM`、`OHOS_ARCH` 设置 ABI 与 STL；不要用宿主默认编译器
- **ABI 限定为 `arm64-v8a` / `x86_64`**（HarmonyOS NEXT 设备只剩 arm64）；目录布局严格遵循 `libs/<abi>/lib*.so`
- **C++ STL 链接默认 `c++_shared`**：多个 .so 之间共享 STL 必须保持一致，否则会内存崩溃
- **不要用 musl 之外的 libc / 静态链接 libc**：OpenHarmony 仅认 musl
- **资源访问只能走 Rawfile API**（34）：不能假定 `/data/...` 文件路径布局
- **崩溃分析必看 hilog + 故障栈**（29）：native crash 通常输出到 `faultlogger`

完整规范以对应文档原文为准。

