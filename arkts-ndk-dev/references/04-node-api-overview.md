<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/coding -->
<!-- 抓取时间: 2026-06-18 -->

# Node-API 概述

## 基本介绍

Node-API（简称 NAPI）是 HarmonyOS 提供的一套 ArkTS/JS 与 C/C++ 交互的接口规范。该规范基于 Node.js 18.x LTS 的 Node-API 规范，但**并非完全兼容**——HarmonyOS 在此基础上进行了扩展和裁剪，开发者不可直接将 Node.js 的原生模块无修改地移植到 HarmonyOS 上运行。

## 主要应用场景

| 场景 | 说明 |
|------|------|
| 系统框架层能力暴露 | 系统框架将底层 C/C++ 能力通过 Node-API 暴露给 ArkTS/JS 层调用 |
| 应用层高性能核心封装 | 应用开发者将性能敏感的核心函数用 C/C++ 实现，通过 Node-API 供 ArkTS/JS 调用 |

## 架构说明

Node-API 在 HarmonyOS 中的整体架构如下：

```
┌─────────────────────────────────────────────────────┐
│                   ArkTS/JS 应用层                    │
│              import nativeModule from 'libentry.so'  │
└───────────────────────┬─────────────────────────────┘
                        │ 调用
                        ▼
┌─────────────────────────────────────────────────────┐
│                  Native Module                       │
│         开发者创建的原生模块，在 ArkTS 中导入使用       │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                    Node-API                          │
│           ArkTS ↔ C/C++ 交互逻辑接口层               │
└───────────────────────┬─────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ ModuleManager│ │ ScopeManager │ │ReferenceManager│
│  原生模块管理  │ │ napi_value   │ │  napi_ref     │
│ 加载、查找模块 │ │  生命周期管理  │ │  生命周期管理   │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│                  NativeEngine                        │
│            ArkTS 引擎抽象层                           │
└───────────────────────┬─────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│           ArkCompiler ArkTS Runtime                  │
│              ArkTS 运行时                             │
└─────────────────────────────────────────────────────┘
```

### 各层职责

| 组件 | 职责 |
|------|------|
| **Native Module** | 开发者创建的原生模块，在 ArkTS 中通过 `import` 导入使用 |
| **Node-API** | 提供 ArkTS 与 C/C++ 之间的交互逻辑，包括类型转换、函数调用、异常处理等 |
| **ModuleManager** | 负责原生模块的加载和查找管理 |
| **ScopeManager** | 管理 `napi_value` 的生命周期，通过 scope 机制自动回收 |
| **ReferenceManager** | 管理 `napi_ref` 的生命周期，用于跨 scope 持有 JS 对象引用 |
| **NativeEngine** | ArkTS 引擎的抽象层，屏蔽底层引擎差异 |
| **ArkCompiler ArkTS Runtime** | 底层 ArkTS 运行时环境 |

## 关键交互流程

### 1. 初始化流程

```
ArkTS import 原生模块
       │
       ▼
引擎调用 ModuleManager 加载 .so 文件
       │
       ▼
首次加载触发模块注册（RegisterDemoModule）
       │
       ▼
调用 Init 函数，将 C/C++ 方法挂载到 exports 对象
       │
       ▼
ArkTS 侧获得可调用的原生方法
```

详细步骤：

1. ArkTS 侧通过 `import nativeModule from 'libentry.so'` 导入原生模块
2. ArkTS 引擎调用 ModuleManager 查找并加载对应的 `.so` 文件
3. `.so` 文件首次加载时，自动执行 `__attribute__((constructor))` 标记的注册函数
4. 注册函数调用 `napi_module_register()` 完成模块注册
5. 引擎调用模块的 `Init` 函数，将 C/C++ 方法通过 `napi_define_properties` 挂载到 `exports` 对象
6. ArkTS 侧获得包含原生方法的 `exports` 对象，即可调用

### 2. 调用流程

```
ArkTS 调用原生方法（如 nativeModule.callNative(2, 3)）
       │
       ▼
引擎根据方法名查找对应的 C/C++ 函数
       │
       ▼
执行 C/C++ 函数，通过 Node-API 进行参数解析和返回值构造
       │
       ▼
返回结果给 ArkTS 侧
```

详细步骤：

1. ArkTS 调用挂载在模块上的方法
2. 引擎根据注册时的映射关系，找到对应的 C/C++ 函数
3. 执行 C/C++ 函数，通过 `napi_get_cb_info` 获取参数，通过 `napi_create_*` 构造返回值
4. 将 C/C++ 函数的返回值传递回 ArkTS 侧
