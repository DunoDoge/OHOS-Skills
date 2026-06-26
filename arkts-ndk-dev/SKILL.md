---
name: arkts-ndk-dev
description: Use when developing HarmonyOS NDK / Node-API / C++ interop code, configuring CMake toolchain for native builds, or handling napi_wrap, napi_threadsafe_function, napi_env threading, module registration, Rawfile, NativeBundle, ASan, LLDB, ABI, or Neon. Triggers include Node-API, napi, NDK, C++ interop, Native, CMake, so, napi_wrap, napi_threadsafe_function, Rawfile, NativeBundle, ASan, LLDB, ABI, Neon, ohos.toolchain.cmake, libace_napi.z.so, napi_module_register, napi_define_properties, napi_get_cb_info, napi_create_external, napi_open_handle_scope, cross-language, cross-thread, or any topic under the HarmonyOS NDK development documentation. Loads the offline NDK reference set so the agent can give real HarmonyOS Node-API code instead of guessing from Node.js N-API knowledge.
---

# arkts-ndk-dev

HarmonyOS's Node-API is based on the Node.js 18.x LTS Node-API specification but is **not fully compatible**:

- Module registration differs: HarmonyOS uses the `napi_module` struct + `__attribute__((constructor))` for auto-registration, not Node.js's `napi_register_module_v1`.
- Thread model differs: Node-API interfaces can only be used on the ArkTS thread; `napi_env` is bound to a specific ArkTS thread. Cross-thread communication must use `napi_threadsafe_function`, not the `uv_queue_work` commonly used in the Node.js community.
- SO naming is strictly constrained: `nm_modname` must exactly match the so name (case-sensitive); one so can only register one module.
- Performance pitfalls: JSArray vs ArrayBuffer performance differs by 400x or more; `napi_wrap`'s result parameter has different memory management semantics depending on whether nullptr or non-nullptr is passed.

Code written by agents using generic Node.js N-API experience is **highly likely to crash or leak memory on HarmonyOS**. This skill provides offline reference documents (11 docs + INDEX under `references/`) which are offline copies of Huawei's official "NDK Development" documentation series, serving as the **authoritative reference** for NDK / Node-API tasks.

## When to Use This Skill

Follow this skill's workflow whenever any of the following conditions are met:

- The user requests **using Node-API for ArkTS and C/C++ interop** (module registration, interface mapping, type conversion, callback invocation)
- The user mentions `napi_*` series interfaces (`napi_wrap`, `napi_threadsafe_function`, `napi_get_cb_info`, `napi_define_properties`, `napi_open_handle_scope`, etc.)
- The user requests **creating/building NDK projects** (Native C++ templates, CMakeLists.txt, ohos.toolchain.cmake, CMake command-line builds)
- The user requests **configuring compilation toolchains** (CMake/GN/Make/Configure cross-compilation, lycium framework)
- The user requests **Native-side resource management** (Rawfile read/write, NativeBundle for app info)
- The user requests **Native worker thread to UI main thread communication** (cross-thread callbacks, thread-safe functions)
- The user requests **NDK debugging/profiling** (ASan memory detection, LLDB debugging)
- The user requests **hardware compatibility configuration** (ABI settings, CPU features, Neon instruction extensions)
- The user mentions `libace_napi.z.so`, `napi_module_register`, `napi_onLoad`, `napi_create_external`, `napi_coerce_to_native_binding_object`, or other HarmonyOS NDK-specific interfaces
- The project contains `CMakeLists.txt` with `libace_napi.z.so` linkage, or an `entry/src/main/cpp/` directory

Do not force this skill onto "pure ArkTS syntax/migration", "ArkTS compilation error fixes", or "command-line build/deploy" scenarios — use the corresponding skills instead (see boundary below).

## Boundary with Other Skills

This skill covers **"how to write NDK code / configure CMake / use Node-API"**, not **"how to modify ArkTS syntax"**, **"how to fix compilation errors"**, or **"how to invoke build commands"**. When NDK tasks involve the following issues, cross-reference the corresponding skill:

| Issue Type | Cross-reference Skill | Boundary |
| --- | --- | --- |
| ArkTS syntax / migration / coding style | `arkts-helper` | This skill only covers the Node-API/C++ side, not ArkTS syntax |
| ArkTS compilation errors (`arkts-no-*` rules, etc.) | `arkts-debug` | Use `arkts-debug` to fix ArkTS compilation errors encountered during NDK development |
| Command-line build/deploy/signing/pipeline | `arkts-build` | This skill only covers "how to write CMakeLists.txt / configure CMake toolchain variables"; `hvigorw` build commands themselves belong to `arkts-build` |
| NDK / Native APIs not covered by offline docs | `harmony-fetch` | If the 11 offline docs in this skill are insufficient to answer a question (e.g., new NDK interfaces, Node-API version changes, ASan/LLDB new features), use `harmony-fetch` to fetch the latest documentation from the Huawei developer portal |

## Workflow (Follow Strictly)

### 1. Read the Index First, Then Decide Which Doc to Load

Before any NDK / Node-API task, **you must read** `references/INDEX.md` first. It provides the role of each of the 11 documents, reading paths by task type, and Node-API key rule quick references — this prevents loading the entire reference directory into context.

### 2. Load the Corresponding Document by Task Type

| Task Type | Required Reading (under `references/`) |
| -------- | ------------------------------ |
| Node-API module development (registration/mapping/type conversion) | `05-node-api-development.md` |
| Node-API rule troubleshooting (thread safety/lifecycle/crashes/performance) | `06-node-api-best-practices.md` |
| Node-API architecture understanding (components/flow/Node.js differences) | `04-node-api-overview.md` |
| Creating NDK projects | `02-create-ndk-project.md` |
| Building NDK projects (CMake/toolchain/command-line) | `03-build-ndk-project.md` |
| Rawfile resource access | `07-rawfile.md` |
| Native Bundle for app info | `08-native-bundle.md` |
| Build toolchain configuration (CMake/GN/Make/Configure/lycium) | `09-build-toolchain.md` |
| Cross-language complex parameter passing | `09-build-toolchain.md` (cross-language complex parameter passing section) |
| Native worker thread to UI main thread communication | `09-build-toolchain.md` (native worker thread to UI main thread communication section) |
| C/C++ memory error detection | `10-debugging-profiling.md` |
| LLDB debugging | `10-debugging-profiling.md` |
| ABI / CPU features / Neon | `11-hardware-compatibility.md` |
| NDK introduction overview | `01-ndk-overview.md` |

When reading documents, prefer using `Grep`/`Read` with offset/limit to locate specific sections — do not read large files in their entirety at once.

### 3. Strictly Enforce Red Lines When Writing Code

Before writing or modifying Node-API code, self-check the following high-frequency red lines (detailed rules are subject to the original documentation):

- **Node-API can only be used on the ArkTS thread**: `napi_env` is bound to the ArkTS thread and must not be passed across threads; cross-thread communication must use `napi_threadsafe_function`
- **Must add scope when creating JS objects in loops**: `napi_open_handle_scope` / `napi_close_handle_scope` must be used in pairs
- **`nm_modname` must exactly match the so name**: Case-sensitive; one so can only register one module; make Init functions static
- **Prefer `napi_threadsafe_function` for async tasks**: `uv_queue_work` is not recommended; if using `uv_queue_work`, callbacks must include `handle_scope`
- **Pass nullptr for `napi_wrap` result**: Managed by the system; passing non-nullptr requires manual `napi_remove_wrap`
- **Use ArrayBuffer instead of JSArray**: Performance differs by 400x or more for value-type data storage
- **`napi_get_arraybuffer_info` returned data must not be manually freed**: Managed by the engine
- **Objects created by `napi_create_external` are only usable on the current thread**: Cross-thread requires `napi_coerce_to_native_binding_object`

When uncertain, **search the original text in `references/06-node-api-best-practices.md` for the relevant red line** before writing.

### 4. Cite the Source When Referencing Documents

When answering Node-API / NDK questions, include a citation at the end of the response, e.g.:

> Per the "Thread Safety" section in `references/06-node-api-best-practices.md`.

### 5. Do Not Skip or Replace This Skill's Checks

Even if the user's Node-API code "looks like valid Node.js N-API", in the HarmonyOS context you must verify against this skill's red lines before answering — do not assume Node.js N-API knowledge can be directly applied.

## Node-API Rules Quick Reference

| Category | Rule | Violation Consequence |
| --- | --- | --- |
| **Thread Safety** | Node-API can only be used on the ArkTS thread; `napi_env` must not be passed across threads; use `napi_threadsafe_function` for cross-thread | Using env across threads causes crashes |
| **Lifecycle** | Must add `napi_open_handle_scope` / `napi_close_handle_scope` when frequently creating JS objects in loops | Memory leaks |
| **Module Registration** | `nm_modname` must exactly match so name (case-sensitive); one so can only register one module; make Init static; registration entry function name must be unique | Module load failure or matching wrong module |
| **Async Tasks** | Prefer `napi_threadsafe_function`, not `uv_queue_work`; if using `uv_queue_work`, callbacks must include `handle_scope` | Memory leaks or crashes |
| **Object Binding** | `napi_wrap` result nullptr: managed by system; non-nullptr: requires manual `napi_remove_wrap` | Memory leaks (napi_ref not released) |
| **Performance** | Use ArrayBuffer instead of JSArray (400x+ performance difference); minimize data conversions; avoid unnecessary copies | Severe performance degradation |

## High-Frequency Code Templates

### Module Registration Template

```cpp
EXTERN_C_START
static napi_value Init(napi_env env, napi_value exports) {
    napi_property_descriptor desc[] = {
        {"methodName", nullptr, MethodName, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}
EXTERN_C_END

static napi_module demoModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "entry",  // Must match so name: libentry.so
    .nm_priv = ((void*)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterEntryModule() {
    napi_module_register(&demoModule);
}
```

### Interface Mapping Template

```cpp
static napi_value MethodName(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value argv[2] = {nullptr};
    napi_get_cb_info(env, info, &argc, argv, nullptr, nullptr);

    // Parameter retrieval and type conversion...
    double value0;
    napi_get_value_double(env, argv[0], &value0);

    // Return result
    napi_value result;
    napi_create_double(env, value0, &result);
    return result;
}
```

### Parameter Retrieval and Type Conversion Template

```cpp
// Get string
size_t strSize;
char strBuf[256];
napi_get_value_string_utf8(env, argv[0], strBuf, sizeof(strBuf), &strSize);

// Get integer
int32_t intValue;
napi_get_value_int32(env, argv[0], &intValue);

// Get boolean
bool boolValue;
napi_get_value_bool(env, argv[0], &boolValue);

// Create object and set properties
napi_value obj;
napi_create_object(env, &obj);
napi_value propValue;
napi_create_string_utf8(env, "hello", NAPI_AUTO_LENGTH, &propValue);
napi_set_named_property(env, obj, "key", propValue);
```

### napi_threadsafe_function Template

```cpp
napi_threadsafe_function tsFn;

// Main thread: Create thread-safe function
napi_value workName;
napi_create_string_utf8(env, "MyThreadSafeFunc", NAPI_AUTO_LENGTH, &workName);
napi_create_threadsafe_function(env, jsCallback, nullptr, workName, 0, 1,
    nullptr, nullptr, nullptr, CallJsCallback, &tsFn);

// Worker thread: Call thread-safe function
napi_acquire_threadsafe_function(tsFn);
napi_call_threadsafe_function(tsFn, data, napi_tsfn_nonblocking);
napi_release_threadsafe_function(tsFn, napi_tsfn_release);

// Callback implementation
static void CallJsCallback(napi_env env, napi_value js_cb, void* context, void* data) {
    // Executes on ArkTS thread; Node-API is safe to use here
    napi_value argv;
    napi_create_int32(env, 42, &argv);
    napi_value result;
    napi_call_function(env, nullptr, js_cb, 1, &argv, &result);
}
```

## Directory Structure

```
arkts-ndk-dev/
├── SKILL.md                                          # This file
└── references/
    ├── INDEX.md                                      # Must read first
    ├── 01-ndk-overview.md                            # NDK development introduction
    ├── 02-create-ndk-project.md                      # Creating NDK projects
    ├── 03-build-ndk-project.md                       # Building NDK projects
    ├── 04-node-api-overview.md                       # Node-API overview & architecture
    ├── 05-node-api-development.md                    # Node-API development workflow (core)
    ├── 06-node-api-best-practices.md                 # Node-API development rules & constraints (core)
    ├── 07-rawfile.md                                 # Rawfile development guide
    ├── 08-native-bundle.md                           # NativeBundle development guide
    ├── 09-build-toolchain.md                         # Build toolchain configuration
    ├── 10-debugging-profiling.md                     # Debugging and profiling
    └── 11-hardware-compatibility.md                  # Hardware compatibility
```

## Documentation Source & Maintenance

- Upstream: Huawei Developer official site "Documentation Center › Application Development › NDK Development" series, under `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/`:
  - `ndk-development-overview` (NDK introduction)
  - `create-with-ndk` (creating projects)
  - `build-with-ndk` (building projects)
  - `coding` (code development, including Node-API)
  - `rawfile-guidelines` (Rawfile)
  - `native-bundle-guidelines` (NativeBundle)
  - `build-toolchain` (build toolchain)
  - `debugging-profiling` (debugging and profiling)
  - `hardware-compatibility` (hardware compatibility)
- Documents are offline snapshots taken on 2026-06-18; each document includes the upstream URL and fetch timestamp at the top.
- To update to the latest version, re-run the fetch (use `curl`/WebFetch from the upstream URLs to overwrite files in `references/`); if expanding the file list, also update `references/INDEX.md`.
- Node-API interfaces may change with HarmonyOS version updates; if uncertain about an interface, consult the latest official documentation.
