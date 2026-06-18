<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/coding -->
<!-- 抓取时间: 2026-06-18 -->

# Node-API 开发红线与最佳实践

本文档是 Node-API 开发的**核心红线文档**，涵盖所有开发规范与约束。违反以下规则可能导致崩溃、内存泄漏或不可预期的行为。

---

## 1. 获取 JS 参数

### 规则

- `argv` 数组长度必须 ≥ `argc` 的值
- `argc` 必须正确初始化为期望的参数数量

### ❌ 错误示例：未初始化 argc

```cpp
static napi_value IncorrectGetArgs(napi_env env, napi_callback_info info) {
    size_t argc;  // 未初始化！argc 值不确定
    napi_value args[2];
    // argc 未初始化，可能导致越界访问或参数获取失败
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    // ...
    return nullptr;
}
```

### ❌ 错误示例：argc 大于 argv 长度

```cpp
static napi_value IncorrectGetArgs2(napi_env env, napi_callback_info info) {
    size_t argc = 3;  // 期望 3 个参数
    napi_value args[2]; // 但 argv 数组只有 2 个元素！越界写入！
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    // ...
    return nullptr;
}
```

### ✅ 正确示例

```cpp
static napi_value CorrectGetArgs(napi_env env, napi_callback_info info) {
    size_t argc = 2;       // 正确初始化 argc
    napi_value args[2] = {nullptr};  // argv 长度 ≥ argc
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    // ...
    return nullptr;
}
```

---

## 2. 生命周期管理

### 规则

- 必须使用 `napi_open_handle_scope` / `napi_close_handle_scope` 管理 `napi_value` 的生命周期
- 在循环中创建大量 `napi_value` 时，必须使用 scope 及时释放，否则会导致内存泄漏

### ❌ 错误示例：循环中未使用 scope

```cpp
static napi_value IncorrectScope(napi_env env, napi_callback_info info) {
    // 在循环中创建 napi_value 但不管理 scope
    // 每次迭代创建的 napi_value 都会累积，导致内存泄漏
    for (int i = 0; i < 10000; i++) {
        napi_value str;
        napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &str);
        // str 不会被自动回收，内存持续增长
    }
    return nullptr;
}
```

### ✅ 正确示例：在循环中使用 scope

```cpp
static napi_value CorrectScope(napi_env env, napi_callback_info info) {
    for (int i = 0; i < 10000; i++) {
        napi_handle_scope scope;
        napi_open_handle_scope(env, &scope);

        napi_value str;
        napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &str);
        // 使用 str ...

        // 每次迭代结束关闭 scope，释放本次创建的 napi_value
        napi_close_handle_scope(env, scope);
    }
    return nullptr;
}
```

---

## 3. 上下文敏感性（跨 env 访问）

### 🔴 红线规则

**严禁跨 `napi_env` 实例访问 JS 对象！** 不同 `napi_env` 对应不同的引擎上下文，跨 env 操作会导致崩溃。

### ❌ 错误示例：跨 env 访问

```cpp
// 在 env1 中创建的 JS 字符串，设置到 env2 的对象上
static napi_value IncorrectCrossEnv(napi_env env1, napi_value exports1,
                                     napi_env env2, napi_value exports2) {
    napi_value str;
    napi_create_string_utf8(env1, "hello", NAPI_AUTO_LENGTH, &str);

    // 🔴 严重错误！str 是在 env1 中创建的，不能在 env2 中使用
    napi_set_named_property(env2, exports2, "key", str);
    // 这将导致崩溃！
    return nullptr;
}
```

### ✅ 正确做法

每个 `napi_env` 中独立创建和使用 JS 对象，不跨 env 传递 `napi_value`。

---

## 4. 异常处理

### 规则

- 每次 Node-API 调用后必须检查 `napi_status` 返回值
- 发生异常后，在异常被处理前不能再调用 Node-API（除异常相关的 API）

### ❌ 错误示例：不检查返回值

```cpp
static napi_value IncorrectException(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    double value;
    // 不检查返回值，如果 args[0] 不是 number，转换失败但继续执行
    napi_get_value_double(env, args[0], &value);
    // value 可能是未定义的值，后续逻辑出错
    return nullptr;
}
```

### ✅ 正确示例：检查每次调用的状态

```cpp
static napi_value CorrectException(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1] = {nullptr};
    napi_status status;

    status = napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (status != napi_ok) {
        return nullptr;
    }

    double value;
    status = napi_get_value_double(env, args[0], &value);
    if (status != napi_ok) {
        // 类型转换失败，可以抛出异常或返回默认值
        napi_throw_type_error(env, nullptr, "Expected number argument");
        return nullptr;
    }

    // 正常处理逻辑
    napi_value result;
    napi_create_double(env, value * 2, &result);
    return result;
}
```

---

## 5. 异步任务

### 规则

- **推荐**使用 `napi_threadsafe_function` 处理异步任务
- 如果使用 `uv_queue_work`，回调函数中**必须**添加 `handle_scope`

### 推荐方案：napi_threadsafe_function

`napi_threadsafe_function` 是官方推荐的线程安全回调方案，支持从任意线程安全地调用 ArkTS 回调。

### 使用 uv_queue_work 的正确方式

```cpp
#include <uv.h>

// 工作线程回调
void WorkCallback(uv_work_t* req) {
    // 在工作线程中执行耗时操作
    // 注意：此处不能调用任何 Node-API
}

// 主线程回调（工作完成后在 ArkTS 线程执行）
void AfterWorkCallback(uv_work_t* req, int status) {
    // ✅ 必须添加 handle_scope！
    napi_handle_scope scope;
    napi_open_handle_scope(env, &scope);

    // 在此处可以安全调用 Node-API
    napi_value result;
    napi_create_double(env, 42, &result);
    // ... 处理结果

    // 关闭 scope
    napi_close_handle_scope(env, scope);
    delete req;
}

// 发起异步任务
void StartAsyncWork(napi_env env) {
    uv_work_t* req = new uv_work_t;
    uv_queue_work(uv_default_loop(), req, WorkCallback, AfterWorkCallback);
}
```

### ❌ 错误示例：uv_queue_work 回调中缺少 scope

```cpp
void AfterWorkCallbackNoScope(uv_work_t* req, int status) {
    // 🔴 缺少 handle_scope，创建的 napi_value 无法被回收
    napi_value result;
    napi_create_double(env, 42, &result);
    // 内存泄漏！
    delete req;
}
```

---

## 6. 对象绑定（napi_wrap）

### 规则

- 当 `result` 参数传 **非 nullptr** 时，必须手动调用 `napi_remove_wrap` 释放
- 一般情况下传 **nullptr** 作为 result，由系统自动管理生命周期

### 方式一：result 传 nullptr（推荐，系统自动管理）

```cpp
static napi_value WrapAutoManaged(napi_env env, napi_callback_info info) {
    napi_value jsThis;
    napi_get_cb_info(env, info, nullptr, nullptr, &jsThis, nullptr);

    MyClass* nativeObj = new MyClass();

    // result 传 nullptr，系统自动管理 native 对象与 JS 对象的绑定关系
    napi_status status = napi_wrap(env, jsThis, nativeObj,
        [](napi_env env, void* data, void* hint) {
            // 析构回调：JS 对象被 GC 时自动调用
            delete static_cast<MyClass*>(data);
        },
        nullptr,  // hint
        nullptr   // result 传 nullptr，系统管理
    );

    return jsThis;
}
```

### 方式二：result 传非 nullptr（需手动管理）

```cpp
static napi_value WrapManualManaged(napi_env env, napi_callback_info info) {
    napi_value jsThis;
    napi_get_cb_info(env, info, nullptr, nullptr, &jsThis, nullptr);

    MyClass* nativeObj = new MyClass();
    napi_ref ref;

    // result 传 &ref，获得引用，需手动管理
    napi_wrap(env, jsThis, nativeObj,
        [](napi_env env, void* data, void* hint) {
            delete static_cast<MyClass*>(data);
        },
        nullptr,
        &ref  // ⚠️ 非 nullptr，必须手动调用 napi_remove_wrap
    );

    // ... 使用 ref ...

    // ⚠️ 必须手动移除 wrap，否则内存泄漏
    napi_remove_wrap(env, jsThis, nullptr);
    napi_delete_reference(env, ref);

    return jsThis;
}
```

---

## 7. 高性能数组操作

### 性能对比

| 方式 | 耗时 | 说明 |
|------|------|------|
| JSArray | ~1566 μs | 通过 `napi_create_array` + `napi_set_element` 逐个设置 |
| ArrayBuffer | ~3.6 μs | 直接操作内存，性能提升约 **435 倍** |

### ❌ 低性能方式：JSArray

```cpp
static napi_value LowPerfArray(napi_env env, napi_callback_info info) {
    constexpr int size = 10000;
    napi_value arr;
    napi_create_array(env, &arr);

    for (int i = 0; i < size; i++) {
        napi_value num;
        napi_create_double(env, i, &num);
        napi_set_element(env, arr, i, num);  // 每次调用都有 JS 开销
    }

    return arr;
}
```

### ✅ 高性能方式：ArrayBuffer

```cpp
static napi_value HighPerfArray(napi_env env, napi_callback_info info) {
    constexpr int size = 10000;

    // 创建 ArrayBuffer
    napi_value arraybuffer;
    void* data = nullptr;
    napi_create_arraybuffer(env, size * sizeof(double), &data, &arraybuffer);

    // 直接操作内存，零 JS 开销
    double* doubleData = static_cast<double*>(data);
    for (int i = 0; i < size; i++) {
        doubleData[i] = static_cast<double>(i);
    }

    return arraybuffer;
}
```

---

## 8. 数据转换优化

### 优化原则

1. **减少转换次数**：尽量在 C/C++ 层完成计算，减少 ArkTS ↔ C/C++ 的数据交互
2. **避免不必要的拷贝**：使用指针或引用传递大数据，而非值传递
3. **使用缓存**：对频繁访问的 JS 对象使用 `napi_ref` 缓存引用

### ❌ 低效方式：频繁转换

```cpp
// 每次调用都重新获取和转换
static napi_value InefficientConvert(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    // 每次调用都从 JS 对象获取属性并转换
    napi_value prop;
    napi_get_named_property(env, args[0], "value", &prop);
    double val;
    napi_get_value_double(env, prop, &val);
    // ...
    return nullptr;
}
```

### ✅ 高效方式：缓存引用

```cpp
// 使用 napi_ref 缓存频繁访问的对象
static napi_ref cachedRef = nullptr;

static napi_value EfficientConvert(napi_env env, napi_callback_info info) {
    if (cachedRef == nullptr) {
        // 首次调用时创建引用
        size_t argc = 1;
        napi_value args[1];
        napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
        napi_create_reference(env, args[0], 1, &cachedRef);
    }

    // 后续调用直接从引用获取
    napi_value obj;
    napi_get_reference_value(env, cachedRef, &obj);
    // ...
    return nullptr;
}
```

---

## 9. 模块注册与命名约束

### 红线规则汇总

| 规则 | 说明 |
|------|------|
| Init 函数加 static | 避免符号冲突 |
| 注册入口函数名唯一 | `RegisterXxxModule` 函数名在项目中必须唯一 |
| nm_modname 必须与 so 名完全一致 | 大小写敏感，`entry` → `libentry.so` |
| 一个 SO 只能注册一个模块 | 不允许同一 `.so` 注册多个 `napi_module` |

### ❌ 错误示例 1：Init 函数缺少 static

```cpp
// 缺少 static，可能导致符号冲突
EXTERN_C_START
napi_value Init(napi_env env, napi_value exports) {
    // ...
    return exports;
}
EXTERN_C_END
```

### ✅ 正确示例 1：Init 函数加 static

```cpp
EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports) {
    // ...
    return exports;
}
EXTERN_C_END
```

### ❌ 错误示例 2：nm_modname 与 so 名不匹配

```cpp
// so 文件名为 libentry.so，但 nm_modname 写成了 "Entry"（大小写不一致）
static napi_module demoModule = {
    .nm_modname = "Entry",  // 🔴 错误！大小写不匹配
    // ...
};
```

### ✅ 正确示例 2：nm_modname 与 so 名严格匹配

```cpp
// so 文件名为 libentry.so，nm_modname 为 "entry"
static napi_module demoModule = {
    .nm_modname = "entry",  // ✅ 正确，与 libentry.so 匹配
    // ...
};
```

### ❌ 错误示例 3：一个 SO 注册多个模块

```cpp
// 🔴 禁止！一个 .so 中注册两个模块
static napi_module module1 = {
    .nm_modname = "module1",
    .nm_register_func = Init1,
    // ...
};

static napi_module module2 = {
    .nm_modname = "module2",
    .nm_register_func = Init2,
    // ...
};

extern "C" __attribute__((constructor)) void RegisterModules() {
    napi_module_register(&module1);
    napi_module_register(&module2);  // 🔴 不允许！
}
```

### ✅ 正确示例 3：一个 SO 只注册一个模块

```cpp
static napi_module demoModule = {
    .nm_modname = "entry",
    .nm_register_func = Init,
    // ...
};

extern "C" __attribute__((constructor)) void RegisterDemoModule() {
    napi_module_register(&demoModule);  // ✅ 只注册一个
}
```

---

## 10. dlopen 场景

### 规则

如果模块在之前已被 `dlopen` 加载过，需要在模块中导出 `napi_onLoad` 函数来实现延迟注册。

### 代码示例

```cpp
// 当模块可能被 dlopen 加载时，需要实现 napi_onLoad
extern "C" __attribute__((visibility("default"))) void napi_onLoad(napi_env env,
                                                                     napi_value exports) {
    // 在此处进行模块初始化，替代或补充 Init 函数的功能
    napi_property_descriptor desc[] = {
        {"callNative", nullptr, CallNative, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
}
```

> **说明**：`napi_onLoad` 在模块被 `dlopen` 加载后由引擎调用，用于在动态加载场景下完成模块注册和初始化。

---

## 11. napi_create_external 限制

### 规则

- 通过 `napi_create_external` 创建的 JS 对象**只能在当前线程使用**
- 跨线程传递需使用 `napi_coerce_to_native_binding_object`

### ❌ 错误示例：Worker 线程 postMessage 传递 external 对象

```typescript
// 主线程
import worker from '@ohos.worker'
import nativeModule from 'libentry.so'

let externalObj = nativeModule.createExternalObject(); // napi_create_external 创建

let workerInstance = new worker.ThreadWorker('workers/MyWorker.ts');
// 🔴 严重错误！external 对象不能跨线程传递
workerInstance.postMessage(externalObj);
// 将导致崩溃或不可预期的行为！
```

### ✅ 正确做法

- 在目标线程中独立创建 external 对象
- 如需跨线程传递原生数据，使用 `napi_coerce_to_native_binding_object` 进行转换

---

## 12. Buffer 释放

### 🔴 红线规则

`napi_get_arraybuffer_info` 返回的数据指针由引擎管理，**开发者绝对不能调用 `free` 释放！**

### ❌ 错误示例：手动释放 ArrayBuffer 数据

```cpp
static napi_value IncorrectBufferFree(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    void* data = nullptr;
    size_t length = 0;
    napi_get_arraybuffer_info(env, args[0], &data, &length);

    // 使用 data ...

    // 🔴 严重错误！data 由引擎管理，不能手动释放
    free(data);  // 将导致双重释放或崩溃！

    return nullptr;
}
```

### ✅ 正确示例：不释放引擎管理的内存

```cpp
static napi_value CorrectBufferUsage(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);

    void* data = nullptr;
    size_t length = 0;
    napi_get_arraybuffer_info(env, args[0], &data, &length);

    // 使用 data 进行读取或写入操作
    // ...

    // ✅ 不释放 data，由引擎自动管理
    return nullptr;
}
```

---

## 红线规则速查表

| 编号 | 红线规则 | 违反后果 |
|------|----------|----------|
| 1 | argv 长度 ≥ argc，argc 必须初始化 | 越界访问、参数获取失败 |
| 2 | 使用 scope 管理 napi_value 生命周期 | 内存泄漏 |
| 3 | 禁止跨 napi_env 访问 JS 对象 | 崩溃 |
| 4 | 检查每次 Node-API 调用的 napi_status | 未定义行为、逻辑错误 |
| 5 | uv_queue_work 回调必须加 handle_scope | 内存泄漏 |
| 6 | napi_wrap result 非 nullptr 时必须手动 remove | 内存泄漏 |
| 7 | 大数组使用 ArrayBuffer 而非 JSArray | 性能下降 400+ 倍 |
| 8 | 减少数据转换次数，使用缓存 | 性能下降 |
| 9 | Init 加 static，函数名唯一，nm_modname 匹配 so 名 | 加载失败、符号冲突 |
| 10 | dlopen 场景需导出 napi_onLoad | 模块无法加载 |
| 11 | napi_create_external 对象不可跨线程使用 | 崩溃 |
| 12 | 禁止释放 ArrayBuffer 的 data 指针 | 双重释放、崩溃 |
