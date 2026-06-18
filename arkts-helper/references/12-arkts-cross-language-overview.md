# ArkTS 跨语言交互概览

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-cross-language-interaction
> **抓取时间**: 2026-06-18

---

## 1. 概述

HarmonyOS 的 ArkTS 跨语言交互基于 **Node-API** 机制实现，允许 ArkTS 代码与 C/C++ 原生代码进行互操作。这使得开发者可以：

- 在 ArkTS 中调用 C/C++ 实现的高性能计算库
- 复用现有的 C/C++ 生态和第三方库
- 实现对硬件底层的直接访问
- 满足性能敏感场景的需求

---

## 2. Node-API 基本概念

### 2.1 什么是 Node-API

Node-API（原名 N-API）是 HarmonyOS 提供的一套 C/C++ 接口，用于构建与 ArkTS 运行时交互的原生模块。它基于 Node.js 社区的 Node-API 标准进行了扩展，但**不完全兼容** Node.js 版本。

### 2.2 与 Node.js Node-API 的关系

| 特性 | Node.js Node-API | HarmonyOS Node-API |
|------|-------------------|---------------------|
| 基础接口 | 标准 Node-API | 基于标准扩展 |
| ABI 稳定性 | ✅ | ✅ |
| 完全兼容 | - | ❌（不完全兼容） |
| 扩展接口 | - | ✅（新增 HarmonyOS 专有接口） |
| 模块注册 | napi_module_register | napi_module_register |
| 线程安全 | napi_threadsafe_function | napi_threadsafe_function（扩展） |

> ⚠️ **重要**：HarmonyOS Node-API 不完全兼容 Node.js 版本。直接移植 Node.js 原生模块时需要适配。

### 2.3 核心概念

| 概念 | 说明 |
|------|------|
| `napi_env` | Node-API 运行环境上下文，几乎所有 API 的第一个参数 |
| `napi_value` | 对 JavaScript 值的抽象表示 |
| `napi_callback_info` | 回调函数的上下文信息 |
| `napi_status` | API 调用的返回状态码 |
| `napi_callback` | C/C++ 中对应 JavaScript 调用的函数指针 |
| `napi_property_descriptor` | 对象属性的描述符 |
| `napi_threadsafe_function` | 线程安全函数，用于跨线程调用 JavaScript |

---

## 3. 开发流程入口

### 3.1 整体流程

```
1. 创建 C/C++ 源文件
   ↓
2. 配置 CMake 构建脚本
   ↓
3. 注册 Node-API 模块
   ↓
4. 实现 ArkTS 与 C/C++ 的接口映射
   ↓
5. 构建编译生成 .so 动态库
   ↓
6. 在 ArkTS 中加载并调用原生模块
```

### 3.2 项目结构

```
项目根目录/
├── entry/
│   └── src/
│       └── main/
│           ├── ets/                    # ArkTS 源码
│           │   └── entryability/
│           │       └── EntryAbility.ets
│           ├── cpp/                    # C/C++ 源码
│           │   ├── CMakeLists.txt      # CMake 构建配置
│           │   ├── hello.cpp           # 原生模块实现
│           │   └── types/              # 接口声明
│           │       └── libhello/
│           │           └── index.d.ts  # TypeScript 声明
│           └── module.json5            # 模块配置
```

### 3.3 CMakeLists.txt 配置

```cmake
cmake_minimum_required(VERSION 3.4.1)

project(hello)

# 添加 Node-API 头文件路径
include_directories(${CMAKE_CURRENT_SOURCE_DIR})

# 构建动态库
add_library(hello SHARED hello.cpp)

# 链接 Node-API 库
target_link_libraries(hello ace_napi.z)
```

### 3.4 模块注册

```cpp
// hello.cpp
#include "napi/native_api.h"

// 实现 ArkTS 可调用的函数
static napi_value Add(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    double a, b;
    napi_get_value_double(env, args[0], &a);
    napi_get_value_double(env, args[1], &b);

    napi_value result;
    napi_create_double(env, a + b, &result);
    return result;
}

// 模块导出描述
EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports) {
    napi_property_descriptor desc[] = {
        { "add", nullptr, Add, nullptr, nullptr, nullptr, napi_default, nullptr }
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

// 模块注册
static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "hello",  // 模块名，与 CMake 中 add_library 名一致
    .nm_priv = nullptr,
    .reserved = { 0 },
};

extern "C" __attribute__((constructor)) void RegisterModule(void) {
    napi_module_register(&demoModule);
}
```

### 3.5 ArkTS 声明文件

```typescript
// types/libhello/index.d.ts
export const add: (a: number, b: number) => number;
```

### 3.6 ArkTS 调用

```typescript
// 在 ArkTS 中导入并使用
import { add } from 'libhello.so';

let result = add(1, 2);
console.info(`1 + 2 = ${result}`); // 3
```

---

## 4. Node-API 扩展能力接口

HarmonyOS 在标准 Node-API 基础上提供了以下扩展能力：

### 4.1 扩展接口分类

| 分类 | 接口 | 说明 |
|------|------|------|
| 线程安全 | `napi_threadsafe_function` 扩展 | 跨线程回调 ArkTS 函数 |
| 异步工作 | `napi_create_async_work` 扩展 | 异步执行 C/C++ 任务 |
| 生命周期 | `napi_open_handle_scope` 等 | 管理 napi_value 的生命周期 |
| 类型转换 | 扩展的类型转换接口 | 支持 HarmonyOS 特有类型 |
| 错误处理 | `napi_throw_error` 等 | 抛出和获取错误信息 |
| 对象操作 | `napi_create_object` 等 | 创建和操作 JavaScript 对象 |
| 函数操作 | `napi_create_function` 等 | 创建和调用 JavaScript 函数 |
| Promise | `napi_create_promise` 等 | 在 C++ 中创建和操作 Promise |
| ArrayBuffer | `napi_create_arraybuffer` 等 | 操作二进制数据 |
| Rawfile | Rawfile 接口 | 读取 HAP 包内的原始文件 |

### 4.2 常用扩展场景

#### 线程安全函数

```cpp
// 在 C++ 子线程中回调 ArkTS 函数
napi_threadsafe_function tsfn;

// 创建线程安全函数
napi_value callback = ...; // ArkTS 传入的回调函数
napi_create_threadsafe_function(env, callback, ...);

// 在 C++ 子线程中调用
napi_call_threadsafe_function(tsfn, ...);

// 释放
napi_release_threadsafe_function(tsfn, napi_tsfn_release);
```

#### 异步工作

```cpp
// 在子线程执行耗时 C++ 操作，完成后回调主线程
napi_async_work async_work;
napi_create_async_work(env, nullptr, resource_name,
    execute_cb,    // 在子线程执行
    complete_cb,   // 在主线程执行
    data, &async_work);
napi_queue_async_work(env, async_work);
```

---

## 5. Node-API 开发规范和常见问题

### 5.1 开发规范

| 规范 | 说明 |
|------|------|
| 模块名一致性 | CMake 中的库名、`nm_modname`、ArkTS 导入路径必须一致 |
| 线程安全 | 不要在非主线程直接调用 Node-API（除 `napi_threadsafe_function` 外） |
| 生命周期管理 | 及时调用 `napi_close_handle_scope` 释放 napi_value |
| 错误检查 | 每次调用 Node-API 后检查 `napi_status` 返回值 |
| 参数校验 | 在 C++ 侧校验 ArkTS 传入参数的类型和数量 |
| 内存管理 | 注意 C++ 侧的内存分配和释放，避免泄漏 |

### 5.2 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 模块加载失败 | 模块名不一致 | 检查 CMake、注册代码、导入路径 |
| 崩溃：非法 napi_env | 在非主线程调用 Node-API | 使用 `napi_threadsafe_function` |
| 内存泄漏 | 未释放 handle scope | 配对使用 `open/close_handle_scope` |
| 参数类型错误 | 未校验 ArkTS 传入类型 | 使用 `napi_typeof` 检查类型 |
| 编译错误：找不到头文件 | CMake 配置问题 | 确保 `include_directories` 正确 |
| .so 文件未打包 | 模块配置缺失 | 检查 `module.json5` 配置 |

### 5.3 性能建议

1. **减少跨语言调用次数**：批量传递数据而非逐个调用
2. **使用 ArrayBuffer**：传递二进制数据时使用 ArrayBuffer 而非数组
3. **避免频繁创建 napi_value**：复用对象，减少 GC 压力
4. **异步处理**：耗时 C++ 操作使用 `napi_create_async_work`
5. **合理使用缓存**：缓存频繁使用的 napi_value 引用

---

## 6. 引导：详细 Node-API 开发

本文档仅提供跨语言交互的概览级介绍。详细的 Node-API 开发指导，包括：

- 完整的 Node-API 接口参考
- CMake 工具链配置
- napi_wrap / napi_threadsafe_function 详解
- Rawfile / NativeBundle 使用
- ASan / LLDB 调试
- ABI 兼容性
- Neon 指令集优化
- 完整代码示例和最佳实践

**请使用 `arkts-ndk-dev` skill 获取详细的 Node-API 开发支持。**

`arkts-ndk-dev` skill 提供了离线的 HarmonyOS NDK 参考文档集合，涵盖所有 Node-API 开发主题，可帮助您：

- 快速查找正确的 Node-API 函数签名和用法
- 了解 HarmonyOS 特有的扩展接口
- 解决常见的编译和运行时错误
- 配置 CMake 工具链和构建流程
- 实现线程安全的跨语言交互

---

## 7. 快速参考：Node-API 状态码

| 状态码 | 值 | 说明 |
|--------|-----|------|
| `napi_ok` | 0 | 成功 |
| `napi_invalid_arg` | 1 | 无效参数 |
| `napi_object_expected` | 2 | 期望对象类型 |
| `napi_string_expected` | 3 | 期望字符串类型 |
| `napi_name_expected` | 4 | 期望名称类型 |
| `napi_function_expected` | 5 | 期望函数类型 |
| `napi_number_expected` | 6 | 期望数字类型 |
| `napi_boolean_expected` | 7 | 期望布尔类型 |
| `napi_array_expected` | 8 | 期望数组类型 |
| `napi_generic_failure` | 9 | 通用失败 |
| `napi_pending_exception` | 10 | 存在未处理的异常 |
| `napi_cancelled` | 11 | 操作被取消 |
| `napi_escape_called_twice` | 12 | escape 被调用两次 |
| `napi_handle_scope_mismatch` | 13 | handle scope 不匹配 |
| `napi_callback_scope_mismatch` | 14 | callback scope 不匹配 |
| `napi_queue_full` | 15 | 队列已满 |
| `napi_closing` | 16 | 正在关闭 |
| `napi_bigint_expected` | 17 | 期望 BigInt 类型 |
| `napi_date_expected` | 18 | 期望 Date 类型 |
| `napi_arraybuffer_expected` | 19 | 期望 ArrayBuffer 类型 |
| `napi_detachable_arraybuffer_expected` | 20 | 期望可分离的 ArrayBuffer |
| `napi_would_deadlock` | 21 | 可能死锁 |

---

## 8. 相关参考

| 主题 | 文档 |
|------|------|
| ArkTS 基础类库 | [07-arkts-stdlib-overview.md](07-arkts-stdlib-overview.md) |
| 异步并发 | [10-arkts-concurrency-async.md](10-arkts-concurrency-async.md) |
| 多线程并发 | [11-arkts-concurrency-multithread.md](11-arkts-concurrency-multithread.md) |
| 详细 Node-API 开发 | **使用 `arkts-ndk-dev` skill** |
