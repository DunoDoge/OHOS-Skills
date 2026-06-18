<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/build-with-ndk -->
<!-- 抓取时间: 2026-06-18 -->

# 构建 NDK 工程

## 构建系统概述

NDK 默认使用 **CMake** 作为构建系统。核心构建脚本是 `hmos.toolchain.cmake`，该文件预定义了 HarmonyOS 平台所需的编译参数和工具链配置。

## hmos.toolchain.cmake

`hmos.toolchain.cmake` 是 NDK 构建的核心 toolchain 文件，位于 `{ndk_root}/build/cmake/` 目录下。它预定义了编译器路径、系统头文件路径、链接参数等关键配置。

### 关键参数

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `OHOS_STL` | `c++_shared`、`c++_static` | C++ 标准库链接方式。`c++_shared` 表示动态链接 libc++_shared.so，`c++_static` 表示静态链接 |
| `OHOS_ARCH` | `armeabi-v7a`、`arm64-v8a`、`x86_64` | 目标 CPU 架构 |
| `OHOS_PLATFORM` | `OHOS` | 目标平台，固定为 `OHOS` |

### 编译器参数

NDK 编译器使用以下关键参数：

- `--target={arch}-linux-ohos`：指定目标平台三元组
- `--sysroot={ndk_root}/sysroot`：指定系统头文件和库的根路径

其中 `{arch}` 与 `OHOS_ARCH` 对应：

| OHOS_ARCH | --target 值 |
|-----------|-------------|
| `armeabi-v7a` | `armv7-unknown-linux-ohos` |
| `arm64-v8a` | `aarch64-unknown-linux-ohos` |
| `x86_64` | `x86_64-unknown-linux-ohos` |

### C++ 链接约束

> **重要**：同一个应用中的**所有**原生库必须使用相同的 C++ 链接方式（`c++_shared` 或 `c++_static`）。混用会导致运行时错误。

## 通过 DevEco Studio 构建

### CMakeLists.txt 示例

```cmake
cmake_minimum_required(VERSION 3.4.1)
project(hello)

add_library(hello SHARED hello.cpp)

target_include_directories(hello PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(hello PUBLIC ace_napi.z)
```

### externalNativeOptions 配置

在 `build-profile.json5` 中可通过 `externalNativeOptions` 配置 CMake 构建参数：

```json5
{
  "apiType": "stageMode",
  "buildOption": {
    "externalNativeOptions": {
      "path": "./src/main/cpp/CMakeLists.txt",   // CMakeLists.txt 路径
      "arguments": "",                            // CMake 额外参数
      "cppFlags": "",                             // C++ 编译选项
      "abiFilters": ["arm64-v8a"]                 // 目标 ABI 架构过滤
    }
  }
}
```

| 字段 | 说明 |
|------|------|
| `path` | CMakeLists.txt 文件路径（相对于模块目录） |
| `arguments` | 传递给 CMake 的额外参数 |
| `cppFlags` | C++ 编译器额外选项 |
| `abiFilters` | 需要构建的目标 ABI 架构列表 |

## 通过命令行构建

### 获取 NDK 包

可通过以下方式获取 NDK：

- 通过 HarmonyOS 命令行工具下载
- 通过 DevEco Studio 的 SDK Manager 自动安装

NDK 安装路径为：

```
$SDK目录/sdk/default/openharmony/native
```

### 配置环境变量

将 NDK 中的 CMake 添加到 PATH：

```bash
# Linux/Mac
export PATH=$PATH:$SDK_DIR/sdk/default/openharmony/native/build-tools/cmake/bin

# Windows
set PATH=%PATH%;%SDK_DIR%\sdk\default\openharmony\native\build-tools\cmake\bin
```

### Linux/Mac 构建

```bash
mkdir build && cd build
cmake \
  -D OHOS_STL=c++_shared \
  -D OHOS_ARCH=arm64-v8a \
  -D OHOS_PLATFORM=OHOS \
  -D CMAKE_TOOLCHAIN_FILE={ohos-sdk}/linux/native/build/cmake/ohos.toolchain.cmake \
  ..
cmake --build .
```

### Windows 构建

Windows 下需额外添加 `-G "Ninja"` 参数指定生成器：

```bash
mkdir build && cd build
cmake \
  -G "Ninja" \
  -D OHOS_STL=c++_shared \
  -D OHOS_ARCH=arm64-v8a \
  -D OHOS_PLATFORM=OHOS \
  -D CMAKE_TOOLCHAIN_FILE={ohos-sdk}/windows/native/build/cmake/ohos.toolchain.cmake \
  ..
cmake --build .
```

### Debug 构建

如需构建 Debug 版本，添加 `-D CMAKE_BUILD_TYPE=Debug`：

```bash
cmake \
  -D CMAKE_BUILD_TYPE=Debug \
  -D OHOS_STL=c++_shared \
  -D OHOS_ARCH=arm64-v8a \
  -D OHOS_PLATFORM=OHOS \
  -D CMAKE_TOOLCHAIN_FILE={ohos-sdk}/linux/native/build/cmake/ohos.toolchain.cmake \
  ..
cmake --build .
```

## 使用预构建库

### 约束条件

- 预构建库**必须**使用 HarmonyOS NDK 工具链编译
- 预构建库的依赖库也必须使用 NDK 工具链编译
- 同一应用中所有原生库的 C++ 链接方式必须一致

### 直接导入方式

在 CMakeLists.txt 中通过 `add_library` 的 `IMPORTED` 选项导入预构建库：

```cmake
# 声明预构建库
add_library(prebuilt_lib SHARED IMPORTED)

# 设置库文件路径
set_target_properties(prebuilt_lib PROPERTIES
  IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/libs/${OHOS_ARCH}/libprebuilt.so
)

# 链接预构建库
target_link_libraries(hello PUBLIC prebuilt_lib)
```

### SONAME 要求

预构建的 `.so` 文件**必须**设置 SONAME。可通过 `llvm-readelf` 工具验证：

```bash
llvm-readelf -d libprebuilt.so | grep SONAME
```

如果输出中包含 `SONAME` 字段，则说明已正确设置。如果没有，需要重新编译该库并确保链接时设置了 SONAME。

### 远程 HAR 预构建库

通过 ohpm 发布的 HAR 包中可以包含预构建的原生库。在 `oh-package.json5` 中声明依赖后，CMakeLists.txt 中可通过特定路径引用。

### 本地 HAR 预构建库

将包含预构建原生库的 HAR 包放在本地，在 `oh-package.json5` 中以本地路径引用，然后在 CMakeLists.txt 中配置导入路径。

## BiSheng 编译器（进阶）

BiSheng 编译器是华为自研的编程语言编译器，支持对 C/C++ 代码进行额外的安全检查和优化。属于可选的高级功能，适用于对安全性有更高要求的场景。详细用法请参考官方文档。
