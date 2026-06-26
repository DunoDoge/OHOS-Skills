# INDEX - arkts-ndk-dev Reference Documentation

> **Must read first**: Before handling any NDK / Node-API task, read this file first to determine which documents to load, then read them as needed — avoid loading the entire reference directory into context at once.
>
> **API version differences: refer to the official documentation**: This document is an offline snapshot. HarmonyOS NDK / Node-API interfaces may change with version updates; if uncertain about an API, consult the latest official documentation.

## Document Roles

| File | Role |
|---|---|
| `01-ndk-overview.md` | NDK use cases, required background knowledge, directory overview, common modules |
| `02-create-ndk-project.md` | Creating Native C++ projects via DevEco Studio |
| `03-build-ndk-project.md` | CMake build system, hmos.toolchain.cmake configuration, command-line build steps, prebuilt libraries |
| `04-node-api-overview.md` | Node-API introduction, architecture, initialization and call flow, differences from Node.js |
| `05-node-api-development.md` | **Core** — Full Node-API development workflow: module registration, interface mapping, type conversion, calling from ArkTS |
| `06-node-api-best-practices.md` | **Core** — Node-API development rules and constraints: thread safety, lifecycle, error handling, async tasks, object binding, performance |
| `07-rawfile.md` | Native Rawfile interface: enumerate / open / read / close, 64-suffix large file APIs |
| `08-native-bundle.md` | Native Bundle interface: retrieve app info, appId, entry info, device type |
| `09-build-toolchain.md` | Build toolchain configuration (CMake/GN/Make/Configure), lycium cross-compilation, cross-language complex parameter passing, worker thread to UI thread communication |
| `10-debugging-profiling.md` | C/C++ memory error detection (ASan), LLDB debugger |
| `11-hardware-compatibility.md` | HarmonyOS ABI, CPU features, Neon instruction extensions |

## Reading Paths by Task Type

| Task Type | Required Reading |
|---|---|
| **Node-API module development** (registration / interface mapping / type conversion) | `05-node-api-development.md` |
| **Node-API rule troubleshooting** (thread safety / lifecycle / crashes / performance) | `06-node-api-best-practices.md` |
| **Node-API architecture understanding** (components / flow / Node.js differences) | `04-node-api-overview.md` |
| **Creating NDK projects** | `02-create-ndk-project.md` |
| **Building NDK projects** (CMake / toolchain / command-line build) | `03-build-ndk-project.md` |
| **Rawfile resource access** | `07-rawfile.md` |
| **Native Bundle for app info** | `08-native-bundle.md` |
| **Build toolchain configuration** (CMake/GN/Make/Configure/lycium) | `09-build-toolchain.md` |
| **Cross-language complex parameter passing** | `09-build-toolchain.md` (cross-language complex parameter passing section) |
| **Native worker thread to UI main thread communication** | `09-build-toolchain.md` (native worker thread to UI main thread communication section) |
| **C/C++ memory error detection** | `10-debugging-profiling.md` |
| **LLDB debugging** | `10-debugging-profiling.md` |
| **ABI / CPU features / Neon** | `11-hardware-compatibility.md` |
| **NDK introduction** (use cases / prerequisites / common modules) | `01-ndk-overview.md` |

## Node-API Key Rules Quick Reference

| Category | Rule |
|---|---|
| **Thread Safety** | Node-API can only be used on the ArkTS thread; `napi_env` is bound to the ArkTS thread and must not be passed across threads; use `napi_threadsafe_function` for cross-thread communication |
| **Lifecycle** | When creating JS objects frequently in loops, always pair `napi_open_handle_scope` / `napi_close_handle_scope` |
| **Module Registration** | `nm_modname` must exactly match the so name (case-sensitive); one so can only register one module; make the Init function static; ensure the registration entry function name is unique |
| **Async Tasks** | Prefer `napi_threadsafe_function` over `uv_queue_work`; if using `uv_queue_work`, callbacks must include `handle_scope` |
| **Object Binding** | When `napi_wrap` result is nullptr, the system manages it; when non-nullptr, manual `napi_remove_wrap` is required |
| **Performance** | Use ArrayBuffer instead of JSArray (400x+ performance difference); minimize data conversions; avoid unnecessary copies |
