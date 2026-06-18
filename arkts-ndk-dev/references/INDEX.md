# arkts-ndk-dev 参考文档索引

> **必先阅读**：处理任何 NDK / Node-API 任务前，先读本文件确定需要加载哪些文档，再按需读取，避免一次性灌满上下文。
>
> **API 版本差异以官网为准**：本文档为离线快照，HarmonyOS NDK / Node-API 接口会随版本更新，遇到不确定的接口请查阅官网最新文档。

## 文档角色一览

| 文件 | 角色 |
|---|---|
| `01-ndk-overview.md` | NDK 适用场景、必备基础知识、目录简介、常用模块总览 |
| `02-create-ndk-project.md` | 通过 DevEco Studio 创建 Native C++ 工程 |
| `03-build-ndk-project.md` | CMake 构建系统、hmos.toolchain.cmake 配置、命令行构建步骤、预构建库 |
| `04-node-api-overview.md` | Node-API 简介与架构组成、初始化与调用流程、与 Node.js 差异 |
| `05-node-api-development.md` | **核心**——Node-API 完整开发流程：模块注册、接口映射、类型转换、ArkTS 调用 |
| `06-node-api-best-practices.md` | **核心**——Node-API 开发规范与红线：线程安全、生命周期、异常处理、异步任务、对象绑定、性能 |
| `07-rawfile.md` | Native Rawfile 接口：遍历/打开/读取/关闭、64 后缀大文件接口 |
| `08-native-bundle.md` | Native Bundle 接口：获取应用信息、appId、入口信息、设备类型 |
| `09-build-toolchain.md` | 编译工具链配置（CMake/GN/Make/Configure）、lycium 交叉编译、跨语言复杂参数传递、子线程与主线程通信 |
| `10-debugging-profiling.md` | C/C++ 内存错误检测（ASan）、LLDB 调试器 |
| `11-hardware-compatibility.md` | HarmonyOS ABI、CPU 特性、Neon 指令扩展 |

## 按任务类型的查阅路径

| 任务类型 | 必读文件 |
|---|---|
| **Node-API 模块开发**（注册模块/映射接口/类型转换） | `05-node-api-development.md` |
| **Node-API 红线排查**（线程安全/生命周期/崩溃/性能） | `06-node-api-best-practices.md` |
| **Node-API 架构理解**（组成/流程/与 Node.js 差异） | `04-node-api-overview.md` |
| **创建 NDK 工程** | `02-create-ndk-project.md` |
| **构建 NDK 工程**（CMake/toolchain/命令行构建） | `03-build-ndk-project.md` |
| **Rawfile 资源访问** | `07-rawfile.md` |
| **Native Bundle 获取应用信息** | `08-native-bundle.md` |
| **编译工具链配置**（CMake/GN/Make/Configure/lycium） | `09-build-toolchain.md` |
| **跨语言复杂参数传递** | `09-build-toolchain.md`（跨语言调用复杂参数传递一节） |
| **Native 子线程与 UI 主线程通信** | `09-build-toolchain.md`（Native 侧子线程与 UI 主线程通信一节） |
| **C/C++ 内存错误检测** | `10-debugging-profiling.md` |
| **LLDB 调试** | `10-debugging-profiling.md` |
| **ABI / CPU 特性 / Neon** | `11-hardware-compatibility.md` |
| **NDK 入门概览**（适用场景/前置知识/常用模块） | `01-ndk-overview.md` |

## Node-API 关键红线速记

| 类别 | 红线 |
|---|---|
| **线程安全** | Node-API 只能在 ArkTS 线程使用；`napi_env` 与 ArkTS 线程绑定，禁止跨线程传递；跨线程通信用 `napi_threadsafe_function` |
| **生命周期** | 循环中频繁创建 JS 对象必须加 `napi_open_handle_scope` / `napi_close_handle_scope` |
| **模块注册** | `nm_modname` 与 so 名完全匹配（区分大小写）；一个 so 只能注册一个模块；Init 函数加 static；注册入口函数名确保唯一 |
| **异步任务** | 推荐 `napi_threadsafe_function`，不推荐 `uv_queue_work`；若用 `uv_queue_work`，回调必须加 `handle_scope` |
| **对象绑定** | `napi_wrap` result 传 nullptr 由系统管理；传非 nullptr 需手动 `napi_remove_wrap` |
| **性能** | ArrayBuffer 代替 JSArray（性能差 400 倍+）；减少数据转换次数；避免不必要复制 |
