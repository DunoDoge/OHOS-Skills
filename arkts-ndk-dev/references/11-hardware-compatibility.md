<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hardware-compatibility -->
<!-- 抓取时间: 2026-06-18 -->

# 硬件兼容性

## HarmonyOS ABI 定义

### 基本特性

| 特性 | 说明 |
|------|------|
| 字节序 | 小端序（Little-endian） |
| 32 位数据模型 | ILP32（int/long/pointer 均为 32 位） |
| 64 位数据模型 | LP64（long/pointer 为 64 位，int 为 32 位） |
| C++ ABI | libc++（Itanium C++ ABI） |
| 浮点数 | IEEE 754 标准 |
| 二进制格式 | ELF |

## 支持的架构

### armeabi-v7a

| 特性 | 值 |
|------|-----|
| 指令集 | ARMv7a |
| 浮点 ABI | `-mfloat-abi=softfp` |
| long double | 64 位 |
| Neon | 可选（DevEco Studio 构建不支持，需使用 CMake 命令行） |

### arm64-v8a

| 特性 | 值 |
|------|-----|
| 指令集 | AArch64 |
| Neon | 默认启用 |
| long double | 128 位 |

### x86_64

| 特性 | 值 |
|------|-----|
| SIMD 指令 | MMX/SSE/SSE2/SSE3/SSSE3/SSE4.1 |
| long double | 128 位 |

## ABI 设置方式

### 方式一：build-profile.json5

在 `build-profile.json5` 中通过 `abiFilters` 字段指定目标架构：

```json5
{
  "app": {
    "products": [
      {
        "name": "default",
        "abiFilters": ["arm64-v8a", "armeabi-v7a"]
      }
    ]
  }
}
```

### 方式二：CMake OHOS_ARCH

在 CMakeLists.txt 中通过 `OHOS_ARCH` 变量获取当前构建架构：

```cmake
message(STATUS "Current architecture: ${OHOS_ARCH}")

if(OHOS_ARCH STREQUAL "arm64-v8a")
    # arm64-v8a 特定配置
elseif(OHOS_ARCH STREQUAL "armeabi-v7a")
    # armeabi-v7a 特定配置
elseif(OHOS_ARCH STREQUAL "x86_64")
    # x86_64 特定配置
endif()
```

## CPU 特性检测

### 方式一：cpu_features 库（推荐）

使用 Google 的 cpu_features 库进行运行时 CPU 特性检测：

```cpp
#include <cpu_features/cpuinfo_arm.h>
#include <hilog/log.h>

void CheckCpuFeatures() {
    const ArmFeatures features = GetArmInfo().features;

    #if defined(__arm__)
    // armeabi-v7a 检测
    if (features.neon) {
        OH_LOG_INFO(LOG_APP, "Neon supported");
    }
    if (features.vfpv3) {
        OH_LOG_INFO(LOG_APP, "VFPv3 supported");
    }
    #elif defined(__aarch64__)
    // arm64-v8a 检测
    if (features.asimd) {
        OH_LOG_INFO(LOG_APP, "ASIMD (Neon) supported");
    }
    #endif
}
```

依赖配置：

```cmake
# CMakeLists.txt 中添加 cpu_features 库
target_link_libraries(entry PUBLIC cpu_features)
```

### 方式二：读取 /proc/cpuinfo

```cpp
#include <fstream>
#include <string>
#include <hilog/log.h>

void ReadCpuInfo() {
    std::ifstream cpuinfo("/proc/cpuinfo");
    std::string line;
    while (std::getline(cpuinfo, line)) {
        // 解析 CPU 特性信息
        if (line.find("Features") != std::string::npos) {
            OH_LOG_INFO(LOG_APP, "CPU Features: %{public}s", line.c_str());
        }
    }
}
```

### 方式三：getauxval

```cpp
#include <sys/auxv.h>
#include <hilog/log.h>

void CheckHwCap() {
    unsigned long hwcap = getauxval(AT_HWCAP);

    #if defined(__aarch64__)
    if (hwcap & HWCAP_ASIMD) {
        OH_LOG_INFO(LOG_APP, "ASIMD (Neon) supported via getauxval");
    }
    #elif defined(__arm__)
    if (hwcap & HWCAP_NEON) {
        OH_LOG_INFO(LOG_APP, "Neon supported via getauxval");
    }
    #endif
}
```

## Neon 指令扩展

### 各架构 Neon 支持情况

| 架构 | Neon 默认状态 | 启用方式 |
|------|-------------|---------|
| arm64-v8a | ✅ 默认启用 | 无需额外配置 |
| armeabi-v7a | ❌ 默认禁用 | 需手动启用 |

### armeabi-v7a 启用 Neon

在 CMakeLists.txt 中添加编译选项：

```cmake
if(OHOS_ARCH STREQUAL "armeabi-v7a")
    target_compile_options(entry PRIVATE
        -mfpu=neon
        -mfloat-abi=softfp
    )
endif()
```

### Neon 使用方式

#### 方式一：自动向量化（Auto-Vectorization）

编译器自动将标量代码向量化，无需修改代码：

```cmake
# CMakeLists.txt 中开启优化
target_compile_options(entry PRIVATE -O2 -ftree-vectorize)
```

#### 方式二：Neon 内联函数（Intrinsics）

```cpp
#include <arm_neon.h>

void NeonAddExample(const float *a, const float *b, float *result, int count) {
    int i = 0;
    // 每次处理 4 个 float（128 位 Neon 寄存器）
    for (; i + 3 < count; i += 4) {
        float32x4_t va = vld1q_f32(a + i);
        float32x4_t vb = vld1q_f32(b + i);
        float32x4_t vr = vaddq_f32(va, vb);
        vst1q_f32(result + i, vr);
    }
    // 处理剩余元素
    for (; i < count; i++) {
        result[i] = a[i] + b[i];
    }
}
```

使用 cpu_features 宏进行运行时保护：

```cpp
#include <arm_neon.h>
#include <cpu_features/cpuinfo_arm.h>

void SafeNeonAdd(const float *a, const float *b, float *result, int count) {
    const ArmInfo info = GetArmInfo();

    if (info.features.neon) {
        // 使用 Neon 加速路径
        NeonAddExample(a, b, result, count);
    } else {
        // 回退到标量实现
        for (int i = 0; i < count; i++) {
            result[i] = a[i] + b[i];
        }
    }
}
```

#### 方式三：手写汇编

```cpp
// 在 .S 汇编文件中
// 使用 Neon 汇编指令实现高性能计算
// 需要配合 CMake 构建
```

```cmake
# CMakeLists.txt 中添加汇编文件
enable_language(ASM)
target_sources(entry PRIVATE neon_impl.S)
```

### Neon 开发注意事项

1. **armeabi-v7a 上 Neon 非默认启用**，必须手动添加 `-mfpu=neon -mfloat-abi=softfp` 编译选项。
2. **运行时检测**：始终使用 cpu_features 库或 `getauxval` 检测 Neon 支持，提供标量回退路径。
3. **DevEco Studio 限制**：DevEco Studio 的 armeabi-v7a 构建不支持 Neon，需使用 CMake 命令行构建。
4. **数据对齐**：Neon 加载/存储操作建议使用 16 字节对齐的内存，以获得最佳性能。
