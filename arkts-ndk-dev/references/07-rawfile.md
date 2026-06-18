<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/rawfile-guidelines -->
<!-- 抓取时间: 2026-06-18 -->

# Rawfile 资源文件操作

## 场景说明

使用 Native Rawfile 接口对 Rawfile 目录和文件进行操作，包括遍历、打开、搜索、读取、关闭等。64 后缀接口支持大于 2GB 的文件操作。

## 接口总览

| 接口名称 | 说明 |
|---------|------|
| OH_ResourceManager_InitNativeResourceManager | 初始化 Native 资源管理器 |
| OH_ResourceManager_OpenRawDir | 打开 Rawfile 目录 |
| OH_ResourceManager_GetRawFileCount | 获取目录下 Rawfile 文件数量 |
| OH_ResourceManager_GetRawFileName | 获取指定索引的 Rawfile 文件名 |
| OH_ResourceManager_OpenRawFile | 打开 Rawfile 文件 |
| OH_ResourceManager_GetRawFileSize | 获取 Rawfile 文件大小 |
| OH_ResourceManager_ReadRawFile | 读取 Rawfile 文件内容 |
| OH_ResourceManager_CloseRawFile | 关闭 Rawfile 文件 |
| OH_ResourceManager_CloseRawDir | 关闭 Rawfile 目录 |
| OH_ResourceManager_GetRawFileDescriptor | 获取 Rawfile 文件描述符 |
| OH_ResourceManager_IsRawDir | 判断路径是否为目录 |
| OH_ResourceManager_ReleaseNativeResourceManager | 释放 Native 资源管理器 |

> **说明**：64 后缀版本（如 `OH_ResourceManager_OpenRawFile64`、`OH_ResourceManager_GetRawFileSize64`、`OH_ResourceManager_ReadRawFile64`）支持大于 2GB 的文件操作。

## 开发步骤

### 1. CMakeLists.txt 配置

在 CMakeLists.txt 中添加依赖库：

```cmake
target_link_libraries(entry PUBLIC
    librawfile.z.so
    libhilog_ndk.z.so
)
```

### 2. index.d.ts 声明

在 `index.d.ts` 中声明导出接口：

```typescript
export const getFileList: (resMgr: object, path: string) => Array<string>;
export const getRawFileContent: (resMgr: object, path: string) => Uint8Array;
export const getRawFileDescriptor: (resMgr: object, path: string) => object;
export const isRawDir: (resMgr: object, path: string) => boolean;
```

### 3. 代码示例

#### 获取文件列表（GetFileList）

```cpp
#include <rawfile/raw_file_manager.h>
#include <rawfile/raw_dir.h>

static napi_value GetFileList(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    // 获取 NativeResourceManager
    NativeResourceManager *nativeResMgr = OH_ResourceManager_InitNativeResourceManager(env, args[0]);

    // 获取路径字符串
    size_t pathSize = 0;
    napi_get_value_string_utf8(env, args[1], nullptr, 0, &pathSize);
    char *path = new char[pathSize + 1];
    napi_get_value_string_utf8(env, args[1], path, pathSize + 1, &pathSize);

    // 打开目录
    RawDir *rawDir = OH_ResourceManager_OpenRawDir(nativeResMgr, path);
    int count = OH_ResourceManager_GetRawFileCount(rawDir);

    // 构造返回数组
    napi_value fileArray;
    napi_create_array(env, &fileArray);
    for (int i = 0; i < count; i++) {
        const char *fileName = OH_ResourceManager_GetRawFileName(rawDir, i);
        napi_value nameStr;
        napi_create_string_utf8(env, fileName, NAPI_AUTO_LENGTH, &nameStr);
        napi_set_element(env, fileArray, i, nameStr);
    }

    OH_ResourceManager_CloseRawDir(rawDir);
    OH_ResourceManager_ReleaseNativeResourceManager(nativeResMgr);
    delete[] path;

    return fileArray;
}
```

#### 读取 Rawfile 内容（GetRawFileContent）

```cpp
#include <rawfile/raw_file_manager.h>

static napi_value GetRawFileContent(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    NativeResourceManager *nativeResMgr = OH_ResourceManager_InitNativeResourceManager(env, args[0]);

    size_t pathSize = 0;
    napi_get_value_string_utf8(env, args[1], nullptr, 0, &pathSize);
    char *path = new char[pathSize + 1];
    napi_get_value_string_utf8(env, args[1], path, pathSize + 1, &pathSize);

    RawFile *rawFile = OH_ResourceManager_OpenRawFile(nativeResMgr, path);
    long len = OH_ResourceManager_GetRawFileSize(rawFile);

    // 使用 napi_create_external_arraybuffer + napi_create_typedarray
    uint8_t *buffer = new uint8_t[len];
    OH_ResourceManager_ReadRawFile(rawFile, buffer, len);

    napi_value arrayBuffer;
    napi_create_external_arraybuffer(env, buffer, len,
        [](napi_env env, void *data, void *hint) {
            delete[] static_cast<uint8_t *>(data);
        }, nullptr, &arrayBuffer);

    napi_value typedArray;
    napi_create_typedarray(env, napi_uint8_array, len, arrayBuffer, 0, &typedArray);

    OH_ResourceManager_CloseRawFile(rawFile);
    OH_ResourceManager_ReleaseNativeResourceManager(nativeResMgr);
    delete[] path;

    return typedArray;
}
```

#### 获取 Rawfile 文件描述符（GetRawFileDescriptor）

```cpp
#include <rawfile/raw_file_manager.h>

static napi_value GetRawFileDescriptor(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    NativeResourceManager *nativeResMgr = OH_ResourceManager_InitNativeResourceManager(env, args[0]);

    size_t pathSize = 0;
    napi_get_value_string_utf8(env, args[1], nullptr, 0, &pathSize);
    char *path = new char[pathSize + 1];
    napi_get_value_string_utf8(env, args[1], path, pathSize + 1, &pathSize);

    RawFile *rawFile = OH_ResourceManager_OpenRawFile(nativeResMgr, path);
    RawFileDescriptor descriptor;
    OH_ResourceManager_GetRawFileDescriptor(rawFile, &descriptor);

    napi_value result;
    napi_create_object(env, &result);

    napi_value fd;
    napi_create_int32(env, descriptor.fd, &fd);
    napi_set_named_property(env, result, "fd", fd);

    napi_value offset;
    napi_create_int64(env, descriptor.start, &offset);
    napi_set_named_property(env, result, "offset", offset);

    napi_value length;
    napi_create_int64(env, descriptor.length, &length);
    napi_set_named_property(env, result, "length", length);

    OH_ResourceManager_CloseRawFile(rawFile);
    OH_ResourceManager_ReleaseNativeResourceManager(nativeResMgr);
    delete[] path;

    return result;
}
```

#### 判断是否为目录（IsRawDir）

```cpp
#include <rawfile/raw_file_manager.h>

static napi_value IsRawDir(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    NativeResourceManager *nativeResMgr = OH_ResourceManager_InitNativeResourceManager(env, args[0]);

    size_t pathSize = 0;
    napi_get_value_string_utf8(env, args[1], nullptr, 0, &pathSize);
    char *path = new char[pathSize + 1];
    napi_get_value_string_utf8(env, args[1], path, pathSize + 1, &pathSize);

    bool isDir = OH_ResourceManager_IsRawDir(nativeResMgr, path);

    napi_value result;
    napi_get_boolean(env, isDir, &result);

    OH_ResourceManager_ReleaseNativeResourceManager(nativeResMgr);
    delete[] path;

    return result;
}
```

### 4. ArkTS 侧调用

```typescript
import rawfile from 'libentry.so';

// 获取资源管理器
const resMgr = getContext().resourceManager;

// 获取文件列表
const fileList: Array<string> = rawfile.getFileList(resMgr, "subdir/");

// 读取文件内容
const content: Uint8Array = rawfile.getRawFileContent(resMgr, "example.txt");

// 获取文件描述符
const descriptor = rawfile.getRawFileDescriptor(resMgr, "example.txt");

// 判断是否为目录
const isDir: boolean = rawfile.isRawDir(resMgr, "subdir/");
```

## 注意事项

- 使用 `OH_ResourceManager_InitNativeResourceManager` 获取的 `NativeResourceManager` 指针，在使用完毕后必须调用 `OH_ResourceManager_ReleaseNativeResourceManager` 释放。
- 使用 `napi_create_external_arraybuffer` 创建的 ArrayBuffer，其内存通过回调自动释放，无需手动 `delete[]`。
- 64 后缀接口适用于大于 2GB 的文件，返回值类型为 `int64_t`。
