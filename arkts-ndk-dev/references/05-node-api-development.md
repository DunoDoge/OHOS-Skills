<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/coding -->
<!-- 抓取时间: 2026-06-18 -->

# Node-API 开发流程

本文档是 Node-API 开发的**核心参考文档**，涵盖从创建项目到完成调用的完整开发流程及完整代码示例。

---

## 1. 创建 Native C++ 项目

在 DevEco Studio 中：

1. 选择 **File > New > Create Project**
2. 在模板选择页面，选择 **Native C++** 模板
3. 填写项目名称、包名等信息，点击 Finish

项目创建后，会自动生成 C/C++ 相关的目录结构和构建配置文件。

---

## 2. 模块注册

模块注册是 Node-API 开发的第一步，通过 `napi_module` 结构体声明模块信息，并使用 `__attribute__((constructor))` 在 `.so` 加载时自动注册。

```cpp
// napi_init.cpp

#include "napi/native_api.h"

// 模块注册结构体
static napi_module demoModule = {
    .nm_version = 1,          // 模块版本号
    .nm_flags = 0,            // 模块标志，默认为 0
    .nm_filename = nullptr,   // 模块文件名，无需指定
    .nm_register_func = Init, // 模块初始化回调函数
    .nm_modname = "entry",    // 模块名，必须与 so 名一致（大小写敏感）
    .nm_priv = ((void*)0),    // 私有数据，默认为 0
    .reserved = {0},          // 保留字段
};

// 模块注册入口函数
// __attribute__((constructor)) 确保 .so 加载时自动执行
extern "C" __attribute__((constructor)) void RegisterDemoModule() {
    napi_module_register(&demoModule);
}
```

> **⚠️ 关键约束**：`nm_modname` 必须与 `.so` 文件名严格匹配（大小写敏感）。例如 `nm_modname = "entry"` 对应 `libentry.so`。

---

## 3. 模块初始化 / 接口映射

`Init` 函数在模块注册后被引擎调用，负责将 C/C++ 函数映射为 ArkTS 可调用的接口。

```cpp
EXTERN_C_START

static napi_value Init(napi_env env, napi_value exports) {
    // 定义需要暴露给 ArkTS 的方法列表
    napi_property_descriptor desc[] = {
        // 方法名        回调函数
        {"callNative",    nullptr, CallNative,    nullptr, nullptr, nullptr, napi_default, nullptr},
        {"nativeCallArkTS", nullptr, NativeCallArkTS, nullptr, nullptr, nullptr, napi_default, nullptr}
    };

    // 将方法列表挂载到 exports 对象
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}

EXTERN_C_END
```

### napi_property_descriptor 字段说明

| 字段 | 说明 |
|------|------|
| 第 1 个 | 方法名（ArkTS 侧调用的名称） |
| 第 2 个 | 方法名（napi_method_name，一般传 nullptr） |
| 第 3 个 | 回调函数（C/C++ 实现） |
| 第 4 个 | getter 回调（属性访问时使用，方法传 nullptr） |
| 第 5 个 | setter 回调（属性设置时使用，方法传 nullptr） |
| 第 6 个 | value（属性值，方法传 nullptr） |
| 第 7 个 | 属性特性（通常使用 `napi_default`） |
| 第 8 个 | 附加数据（通常传 nullptr） |

---

## 4. 类型声明文件（index.d.ts）

为了让 ArkTS 侧获得类型提示，需要编写类型声明文件：

```typescript
// entry/src/main/cpp/types/libentry/index.d.ts

export const callNative: (a: number, b: number) => number;
export const nativeCallArkTS: (cb: (a: number) => number) => number;
```

---

## 5. oh-package.json5 关联配置

类型声明文件需要通过 `oh-package.json5` 与 `.so` 文件关联：

```json5
// entry/src/main/cpp/types/libentry/oh-package.json5

{
  "name": "libentry.so",
  "types": "./index.d.ts",
  "version": "",
  "description": "Please describe the basic information."
}
```

> **说明**：`name` 字段指定 `.so` 文件名，`types` 字段指定类型声明文件的相对路径。

---

## 6. CMakeLists.txt 配置

```cmake
# CMakeLists.txt

cmake_minimum_required(VERSION 3.4.1)
project(MyApplication)

set(NATIVERENDER_ROOT_PATH ${CMAKE_CURRENT_SOURCE_DIR})

# 添加头文件搜索路径
include_directories(${NATIVERENDER_ROOT_PATH}
                    ${NATIVERENDER_ROOT_PATH}/include)

# 构建共享库
add_library(entry SHARED napi_init.cpp)

# 链接 Node-API 库
target_link_libraries(entry PUBLIC libace_napi.z.so)
```

### 关键配置说明

| 配置项 | 说明 |
|--------|------|
| `add_library(entry SHARED ...)` | 构建名为 `entry` 的共享库，生成 `libentry.so` |
| `target_link_libraries(entry PUBLIC libace_napi.z.so)` | 链接 Node-API 系统库 |

---

## 7. 原生方法实现

### 7.1 CallNative —— 两数相加

```cpp
static napi_value CallNative(napi_env env, napi_callback_info info) {
    // 获取参数数量
    size_t argc = 2;
    napi_value args[2] = {nullptr};

    // 从回调信息中提取参数
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    // 将 JS 参数转换为 C++ 类型
    double a = 0.0;
    double b = 0.0;
    napi_get_value_double(env, args[0], &a);
    napi_get_value_double(env, args[1], &b);

    // 执行 C++ 计算
    double result = a + b;

    // 将结果转换为 JS 值并返回
    napi_value sum;
    napi_create_double(env, result, &sum);
    return sum;
}
```

### 7.2 NativeCallArkTS —— 从 C++ 调用 ArkTS 回调

```cpp
static napi_value NativeCallArkTS(napi_env env, napi_callback_info info) {
    // 获取回调函数参数
    size_t argc = 1;
    napi_value args[1] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    // args[0] 即为 ArkTS 传入的回调函数
    napi_value func = args[0];

    // 构造传递给回调函数的参数
    napi_value arg;
    napi_create_double(env, 2.0, &arg);

    // 从 C++ 调用 ArkTS 回调函数
    napi_value result;
    napi_call_function(env, nullptr, func, 1, &arg, &result);

    // 获取回调函数的返回值
    double ret = 0.0;
    napi_get_value_double(env, result, &ret);

    // 将回调返回值作为本函数的返回值
    napi_value returnValue;
    napi_create_double(env, ret, &returnValue);
    return returnValue;
}
```

### napi_call_function 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| env | napi_env | Node-API 环境上下文 |
| recv | napi_value | this 对象，传 `nullptr` 表示 undefined |
| func | napi_value | 要调用的 JS 函数 |
| argc | size_t | 参数个数 |
| argv | const napi_value* | 参数数组 |
| result | napi_value* | 函数返回值（输出参数） |

---

## 8. ArkTS 侧调用

```typescript
// 导入原生模块
import nativeModule from 'libentry.so'

@Entry
@Component
struct Index {
  build() {
    Column() {
      Button('调用 CallNative')
        .onClick(() => {
          // 调用 C++ 的加法方法
          let result = nativeModule.callNative(2, 3);  // result = 5
          console.info(`CallNative result: ${result}`);
        })

      Button('调用 NativeCallArkTS')
        .onClick(() => {
          // 传入回调函数，C++ 侧会调用该回调
          let result = nativeModule.nativeCallArkTS((a: number) => {
            return a * 3;  // C++ 传入 2，回调返回 6
          });
          console.info(`NativeCallArkTS result: ${result}`);  // result = 6
        })
    }
  }
}
```

---

## 9. 开发约束

### 9.1 SO 命名约束

| 规则 | 说明 |
|------|------|
| 模块名与 SO 名一致 | `nm_modname` 必须与 `.so` 文件名大小写完全匹配 |
| 示例 | `nm_modname = "entry"` → 生成 `libentry.so` |
| 反例 | `nm_modname = "Entry"` → 无法匹配 `libentry.so`，加载失败 |

### 9.2 注册约束

| 规则 | 说明 |
|------|------|
| Init 函数加 static | 避免符号冲突，Init 函数应声明为 `static` |
| 注册入口函数名唯一 | `RegisterDemoModule` 等注册函数名在项目中必须唯一 |
| 一个 SO 只能注册一个模块 | 不允许在同一个 `.so` 中注册多个 `napi_module` |

### 9.3 多线程约束

| 规则 | 说明 |
|------|------|
| Node-API 仅限 ArkTS 线程 | 所有 Node-API 调用必须在 ArkTS 主线程执行 |
| env 绑定线程 | `napi_env` 与特定的 ArkTS 线程绑定，不可跨线程使用 |
| 线程安全 | 子线程中不可直接调用 Node-API，需使用 `napi_threadsafe_function` |
| env 销毁后访问崩溃 | 引擎销毁后访问 `napi_env` 会导致崩溃 |

### 9.4 调试约束

| 建议 | 说明 |
|------|------|
| 优先使用真机调试 | 真机调试更稳定，模拟器可能存在兼容性问题 |
| 禁止使用预览器调试 | 预览器不支持 Node-API 调试，可能导致异常 |
