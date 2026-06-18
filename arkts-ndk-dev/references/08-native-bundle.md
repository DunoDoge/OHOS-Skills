<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/native-bundle-guidelines -->
<!-- 抓取时间: 2026-06-18 -->

# Native Bundle 应用信息获取

## 场景说明

使用 Native Bundle 接口获取应用自身信息，包括应用 ID、应用标识、主元素名、兼容设备类型等。

## 接口总览

| 接口名称 | 最低 API 版本 | 说明 |
|---------|-------------|------|
| OH_NativeBundle_GetCurrentApplicationInfo | 11 | 获取当前应用信息结构体 |
| OH_NativeBundle_GetAppId | 12 | 获取应用 ID |
| OH_NativeBundle_GetAppIdentifier | 12 | 获取应用标识 |
| OH_NativeBundle_GetMainElementName | 12 | 获取主元素名 |
| OH_NativeBundle_GetCompatibleDeviceType | 12 | 获取兼容设备类型 |
| OH_NativeBundle_IsDebugMode | 20 | 判断是否为调试模式 |
| OH_NativeBundle_GetModuleMetadata | 20 | 获取模块元数据 |
| OH_NativeBundle_GetAbilityResourceInfo | 21 | 获取 Ability 资源信息 |

## 开发步骤

### 1. CMakeLists.txt 配置

在 CMakeLists.txt 中添加依赖库：

```cmake
target_link_libraries(entry PUBLIC
    libbundle_ndk.so
)
```

### 2. 头文件引入

```cpp
#include <bundle/native_interface_bundle.h>
#include <bundle/ability_resource_info.h>  // API 21+
```

### 3. 代码示例

#### 获取当前应用信息（GetCurrentApplicationInfo）

```cpp
#include <bundle/native_interface_bundle.h>
#include <hilog/log.h>

void GetCurrentApplicationInfoExample() {
    ApplicationInfo *appInfo = OH_NativeBundle_GetCurrentApplicationInfo();
    if (appInfo == nullptr) {
        OH_LOG_ERROR(LOG_APP, "Failed to get application info");
        return;
    }

    // 使用 appInfo 中的字段
    // appInfo->bundleName 等字段

    // 注意：使用完毕后无需手动释放 ApplicationInfo 结构体本身
    // 但其中返回 char* 的接口需要手动 free
}
```

#### 获取应用 ID（GetAppId）

```cpp
#include <bundle/native_interface_bundle.h>
#include <hilog/log.h>
#include <cstdlib>  // for free()

void GetAppIdExample() {
    char *appId = OH_NativeBundle_GetAppId();
    if (appId != nullptr) {
        OH_LOG_INFO(LOG_APP, "AppId: %{public}s", appId);
        free(appId);  // ⚠️ 必须手动释放，否则内存泄漏
    }
}
```

#### 获取应用标识（GetAppIdentifier）

```cpp
#include <bundle/native_interface_bundle.h>
#include <hilog/log.h>
#include <cstdlib>

void GetAppIdentifierExample() {
    char *appIdentifier = OH_NativeBundle_GetAppIdentifier();
    if (appIdentifier != nullptr) {
        OH_LOG_INFO(LOG_APP, "AppIdentifier: %{public}s", appIdentifier);
        free(appIdentifier);  // ⚠️ 必须手动释放
    }
}
```

#### 获取主元素名（GetMainElementName）

```cpp
#include <bundle/native_interface_bundle.h>
#include <hilog/log.h>
#include <cstdlib>

void GetMainElementNameExample() {
    char *mainElementName = OH_NativeBundle_GetMainElementName();
    if (mainElementName != nullptr) {
        OH_LOG_INFO(LOG_APP, "MainElementName: %{public}s", mainElementName);
        free(mainElementName);  // ⚠️ 必须手动释放
    }
}
```

#### 获取兼容设备类型（GetCompatibleDeviceType）

```cpp
#include <bundle/native_interface_bundle.h>
#include <hilog/log.h>
#include <cstdlib>

void GetCompatibleDeviceTypeExample() {
    char *deviceType = OH_NativeBundle_GetCompatibleDeviceType();
    if (deviceType != nullptr) {
        OH_LOG_INFO(LOG_APP, "CompatibleDeviceType: %{public}s", deviceType);
        free(deviceType);  // ⚠️ 必须手动释放
    }
}
```

#### 判断是否为调试模式（IsDebugMode）

```cpp
#include <bundle/native_interface_bundle.h>
#include <hilog/log.h>

// API 20+
void IsDebugModeExample() {
    bool isDebug = OH_NativeBundle_IsDebugMode();
    OH_LOG_INFO(LOG_APP, "IsDebugMode: %{public}s", isDebug ? "true" : "false");
}
```

#### 获取模块元数据（GetModuleMetadata）

```cpp
#include <bundle/native_interface_bundle.h>
#include <hilog/log.h>
#include <cstdlib>

// API 20+
void GetModuleMetadataExample() {
    char *metadata = OH_NativeBundle_GetModuleMetadata();
    if (metadata != nullptr) {
        OH_LOG_INFO(LOG_APP, "ModuleMetadata: %{public}s", metadata);
        free(metadata);  // ⚠️ 必须手动释放
    }
}
```

## ⚠️ 重要注意事项

**Native Bundle 接口返回的 `char*` 指针必须手动调用 `free()` 释放，否则会导致内存泄漏！**

以下接口返回的 `char*` 需要手动释放：

| 接口 | 返回值 | 需要手动 free |
|------|--------|-------------|
| OH_NativeBundle_GetAppId | `char*` | ✅ 是 |
| OH_NativeBundle_GetAppIdentifier | `char*` | ✅ 是 |
| OH_NativeBundle_GetMainElementName | `char*` | ✅ 是 |
| OH_NativeBundle_GetCompatibleDeviceType | `char*` | ✅ 是 |
| OH_NativeBundle_GetModuleMetadata | `char*` | ✅ 是 |

正确的内存管理模式：

```cpp
char *result = OH_NativeBundle_GetAppId();
if (result != nullptr) {
    // 使用 result ...
    free(result);   // 必须调用 free() 释放
    result = nullptr;
}
```
