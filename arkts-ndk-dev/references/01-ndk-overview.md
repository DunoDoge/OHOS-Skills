<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ndk-development-overview -->
<!-- 抓取时间: 2026-06-18 -->

# NDK 开发概述

## NDK 简介

NDK（Native Development Kit）是 HarmonyOS 提供的原生开发套件，是 Native API、构建脚本和工具链的集合。通过 NDK，开发者可以在 HarmonyOS 应用中使用 C/C++ 语言进行开发，实现性能敏感型功能或复用已有的 C/C++ 库。

NDK 主要包含以下内容：

- **Native API**：HarmonyOS 提供的 C/C++ 接口集合
- **构建脚本**：基于 CMake 的构建配置文件
- **工具链**：基于 Clang/LLVM 的编译工具链

## NDK 适用场景

| 场景 | 说明 |
|------|------|
| 性能敏感型应用 | 游戏、音视频处理等对性能要求较高的场景，使用 C/C++ 可获得更好的执行效率 |
| 复用已有 C/C++ 库 | 需要复用已有的 C/C++ 开源库或自研库，避免重复开发 |
| CPU 特定指令优化 | 需要利用 ARM Neon 等 CPU 特定指令集进行优化的场景 |

## 不建议使用 NDK 的场景

| 场景 | 说明 |
|------|------|
| 纯 C/C++ 应用 | HarmonyOS 不支持纯 C/C++ 应用，应用入口必须是 ArkTS |
| 追求广泛设备兼容 | C/C++ 代码与 CPU 架构相关，需要为不同架构分别编译，兼容性不如 ArkTS |

## 前置知识要求

使用 NDK 进行开发前，建议具备以下知识：

- **Linux C 编程**：熟悉 Linux 环境下的 C 语言编程
- **CMake**：了解 CMake 构建系统的基本用法
- **Node Addons**：了解 Node.js 原生扩展的开发方式
- **Clang/LLVM**：了解 Clang/LLVM 编译器工具链
- **Node-API**：了解 Node-API（原 NAPI）的使用方式

> **注意**：HarmonyOS 的 Node-API 基于 Node.js 的 Node-API 实现，但**并不完全兼容**。开发时需参考 HarmonyOS 官方文档，不可直接套用 Node.js Node-API 的全部用法。

## NDK 目录结构

NDK 安装后的典型目录结构如下：

```
native/
├── build/              # 构建相关文件
│   └── cmake/
│       └── hmos.toolchain.cmake   # 核心 toolchain 文件
├── build-tools/        # 构建工具
│   └── cmake/          # CMake 3.16.5
├── llvm/               # 编译器工具链（基于 Clang/LLVM）
├── sysroot/            # 系统头文件和库
└── ...
```

### 主要目录说明

| 目录 | 说明 |
|------|------|
| `build/cmake/` | 包含 `hmos.toolchain.cmake`，是 CMake 构建的核心 toolchain 文件，预定义了编译参数 |
| `build-tools/cmake/` | 包含 CMake 3.16.5 构建工具 |
| `llvm/` | 包含基于 Clang/LLVM 的编译器，支持 C/C++ 编译、链接等操作 |

## 常用模块

NDK 提供的常用模块如下：

| 模块 | 说明 |
|------|------|
| 标准C库（musl） | 基于 musl 的标准 C 库实现 |
| 标准C++库 | 标准C++库支持 |
| 日志（HiLog） | 原生日志模块，用于 C/C++ 代码中输出日志 |
| Node-API | ArkTS 与 C/C++ 之间的互操作接口 |
| FFRT | 并发调度框架（Function Flow Runtime） |
| libuv | 异步 I/O 库 |
| zlib | 数据压缩库 |
| Rawfile | 资源文件访问接口 |
| XComponent | 用于嵌入 C/C++ 渲染内容的组件 |
| Drawing | 2D 图形绘制库 |
| OpenGL | OpenGL ES 图形接口 |
| OpenSL ES | 音频播放和录制接口 |
