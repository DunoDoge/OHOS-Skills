<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/build-toolchain -->
<!-- 抓取时间: 2026-06-18 -->

# 构建工具链配置

## CMake 构建工具链配置

使用 HarmonyOS NDK 提供的 `ohos.toolchain.cmake` 进行交叉编译配置：

```cmake
# 设置工具链文件
set(CMAKE_TOOLCHAIN_FILE ${OHOS_NDK}/native/build/cmake/ohos.toolchain.cmake)

# 关键变量
set(OHOS_ARCH arm64-v8a)           # 目标架构
set(OHOS_PLATFORM OHOS)            # 目标平台
set(CMAKE_BUILD_TYPE Debug)         # 构建类型
```

## GN 构建配置

- 适配 HarmonyOS 平台宏定义
- 配置 clang 工具链路径
- 设置 sysroot 指向 NDK sysroot
- 为每个架构配置 `ohos_clang_toolchain`

## Make 构建配置

手动设置交叉编译工具链：

```makefile
CC = $(NDK_PATH)/native/llvm/bin/clang
AR = $(NDK_PATH)/native/llvm/bin/llvm-ar
RANLIB = $(NDK_PATH)/native/llvm/bin/llvm-ranlib

CFLAGS += --target=aarch64-linux-ohos
CFLAGS += --sysroot=$(NDK_PATH)/native/sysroot
```

## Configure 构建配置

通过环境变量配置交叉编译：

```bash
export CC=${NDK_PATH}/native/llvm/bin/clang
export CXX=${NDK_PATH}/native/llvm/bin/clang++
export AR=${NDK_PATH}/native/llvm/bin/llvm-ar
export RANLIB=${NDK_PATH}/native/llvm/bin/llvm-ranlib
export CFLAGS="--target=aarch64-linux-ohos --sysroot=${NDK_PATH}/native/sysroot"
export CXXFLAGS="--target=aarch64-linux-ohos --sysroot=${NDK_PATH}/native/sysroot"

./configure --host=aarch64-linux
```

## lycium 交叉编译框架

### HPKBUILD 模板

HPKBUILD 是 lycium 框架的构建描述文件，定义了源码获取、补丁、构建和安装步骤：

```bash
pkgname=example
pkgver=1.0.0
source=("https://example.com/${pkgname}-${pkgver}.tar.gz")

build() {
    cd ${pkgname}-${pkgver}
    ./configure --host=${HOST} --prefix=${PREFIX}
    make -j${NPROC}
}

package() {
    make install
}
```

### build.sh 使用

```bash
# 编译指定库
./build.sh example

# 编译指定架构
./build.sh example --arch arm64-v8a
```

## 跨语言复杂参数传递

### ArrayBuffer 传递

```cpp
// ArkTS 侧
// let buffer = new ArrayBuffer(1024);
// nativeFunc(buffer);

// Native 侧
static napi_value NativeFunc(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    void *data = nullptr;
    size_t length = 0;
    napi_get_arraybuffer_info(env, args[0], &data, &length);
    // 使用 data 指针操作 ArrayBuffer 数据
    return nullptr;
}
```

### Object 传递

```cpp
static napi_value NativeFunc(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_value key;
    napi_create_string_utf8(env, "name", NAPI_AUTO_LENGTH, &key);
    napi_value value;
    napi_get_property(env, args[0], key, &value);
    // 读取 Object 属性
    return nullptr;
}
```

### HashMap 传递

```cpp
// ArkTS 侧 Map 需要转换为 Object 后传递
// Native 侧通过 napi_get_property_names 遍历键值对
static napi_value NativeFunc(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_value keys;
    napi_get_property_names(env, args[0], &keys);
    uint32_t keyCount = 0;
    napi_get_array_length(env, keys, &keyCount);

    for (uint32_t i = 0; i < keyCount; i++) {
        napi_value key, value;
        napi_get_element(env, keys, i, &key);
        napi_get_property(env, args[0], key, &value);
        // 处理键值对
    }
    return nullptr;
}
```

### PixelMap 传递

```cpp
#include <multimedia/image_framework/image_pixel_map_mdk.h>

static napi_value NativeFunc(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    // 获取 PixelMap Native 指针
    OhosPixelMapInfo pixelMapInfo;
    OH_GetImageInfo(env, args[0], &pixelMapInfo);
    // 使用 pixelMapInfo 数据
    return nullptr;
}
```

### Class 类型传递

```cpp
// ArkTS 侧传递类实例，Native 侧通过 napi_unwrap 获取原生对象
static napi_value NativeFunc(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    void *nativeObj = nullptr;
    napi_unwrap(env, args[0], &nativeObj);
    // 使用 nativeObj
    return nullptr;
}
```

## Native 子线程与 UI 主线程通信

### ⚠️ 关键约束

**`napi_env`、`napi_value`、`napi_ref` 不能在子线程中直接使用！** 这些对象绑定到创建它们的线程，跨线程使用会导致未定义行为或崩溃。

### 方法一：napi_threadsafe_function（推荐）

使用线程安全函数机制，子线程通过回调将任务投递到主线程执行：

```cpp
#include <thread>
#include <napi/native_api.h>
#include <hilog/log.h>

static napi_threadsafe_function tsfn = nullptr;

// 子线程调用函数
void CallJs(napi_env env, napi_value js_cb, void *context, void *data) {
    if (env == nullptr || js_cb == nullptr) {
        return;
    }

    int *value = static_cast<int *>(data);
    napi_value argv[1];
    napi_create_int32(env, *value, &argv[0]);
    delete value;

    napi_value undefined;
    napi_get_undefined(env, &undefined);

    napi_call_function(env, undefined, js_cb, 1, argv, nullptr);
}

// 创建线程安全函数
static napi_value CreateThreadsafeFunc(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    napi_value workName;
    napi_create_string_utf8(env, "ThreadSafeFunc", NAPI_AUTO_LENGTH, &workName);

    napi_create_threadsafe_function(env, args[0], nullptr, workName, 0, 1,
        nullptr, nullptr, nullptr, CallJs, &tsfn);

    // 启动子线程
    std::thread([]() {
        for (int i = 0; i < 10; i++) {
            int *data = new int(i);
            napi_acquire_threadsafe_function(tsfn);
            napi_call_threadsafe_function(tsfn, data, napi_tsfn_nonblocking);
            napi_release_threadsafe_function(tsfn, napi_tsfn_release);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }).detach();

    return nullptr;
}

// 释放线程安全函数
static napi_value ReleaseThreadsafeFunc(napi_env env, napi_callback_info info) {
    if (tsfn != nullptr) {
        napi_release_threadsafe_function(tsfn, napi_tsfn_release);
        tsfn = nullptr;
    }
    return nullptr;
}
```

### 方法二：libuv uv_async_send

使用 libuv 异步机制将任务投递到主线程事件循环：

```cpp
#include <thread>
#include <uv.h>
#include <napi/native_api.h>
#include <hilog/log.h>

struct AsyncData {
    napi_async_work work;
    napi_ref callbackRef;
    int result;
};

static napi_value AsyncWorkExample(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    AsyncData *asyncData = new AsyncData();
    napi_create_reference(env, args[0], 1, &asyncData->callbackRef);

    napi_value workName;
    napi_create_string_utf8(env, "AsyncWork", NAPI_AUTO_LENGTH, &workName);

    napi_create_async_work(env, nullptr, workName,
        // Execute 回调：在子线程执行
        [](napi_env env, void *data) {
            AsyncData *asyncData = static_cast<AsyncData *>(data);
            // 执行耗时操作
            asyncData->result = 42;
        },
        // Complete 回调：在主线程执行
        [](napi_env env, napi_status status, void *data) {
            AsyncData *asyncData = static_cast<AsyncData *>(data);

            napi_value callback;
            napi_get_reference_value(env, asyncData->callbackRef, &callback);

            napi_value argv[1];
            napi_create_int32(env, asyncData->result, &argv[0]);

            napi_value undefined;
            napi_get_undefined(env, &undefined);
            napi_call_function(env, undefined, callback, 1, argv, nullptr);

            napi_delete_reference(env, asyncData->callbackRef);
            napi_delete_async_work(env, asyncData->work);
            delete asyncData;
        },
        asyncData, &asyncData->work);

    napi_queue_async_work(env, asyncData->work);
    return nullptr;
}
```

### 两种方法对比

| 特性 | napi_threadsafe_function | libuv uv_async_send |
|------|------------------------|-------------------|
| 推荐程度 | ✅ 推荐 | 备选方案 |
| 调用方式 | 子线程直接调用 | 通过事件循环投递 |
| 复杂度 | 中等 | 较高 |
| 线程安全 | 原生支持 | 需要额外处理 |
| 适用场景 | 高频子线程回调 | 低频异步任务 |
