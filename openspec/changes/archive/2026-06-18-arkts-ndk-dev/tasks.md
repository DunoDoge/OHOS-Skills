## 1. 创建 skill 目录结构

- [x] 1.1 创建 `arkts-ndk-dev/` 目录及 `arkts-ndk-dev/references/` 子目录
- [x] 1.2 确认目录结构与 `arkts-helper` / `arkts-debug` / `arkts-build` 一致（`SKILL.md` 在根，参考文档在 `references/`）

## 2. 编写 references/INDEX.md 索引文件

- [x] 2.1 编写 `references/INDEX.md`，包含：各文档角色一句话说明、按任务类型（Node-API 开发 / NDK 工程创建与构建 / Rawfile / NativeBundle / 编译工具链 / 调试性能分析 / 硬件兼容性）的查阅路径表、Node-API 关键红线速记（线程安全 / 生命周期 / 模块注册 / 异步任务 / 对象绑定 / 性能）
- [x] 2.2 在 INDEX.md 顶部标注「必先阅读」提示与「API 版本差异以官网为准」说明

## 3. 编写 references/ 离线参考文档

- [x] 3.1 编写 `01-ndk-overview.md`：NDK 适用场景、必备基础知识（Linux C/CMake/Node Addons/Clang/Node-API）、目录简介（build/build-tools/llvm/sysroot）、常用模块（标准库/Node-API/FFRT/libuv/Rawfile/XComponent/Drawing/OpenGL/OpenSL ES），来源 `ndk-development-overview`
- [x] 3.2 编写 `02-create-ndk-project.md`：通过 DevEco Studio 创建 Native C++ 工程、工程目录结构（entry/src/main/cpp 等），来源 `create-with-ndk`
- [x] 3.3 编写 `03-build-ndk-project.md`：CMake 构建系统、hmos.toolchain.cmake 核心配置、OHOS_STL（c++_shared/c++_static）/ OHOS_ARCH（armeabi-v7a/arm64-v8a/x86_64）参数、命令行构建步骤（Linux/Mac/Windows）、预构建库使用、同一应用 C++ 链接方式一致性约束，来源 `build-with-ndk`
- [x] 3.4 编写 `04-node-api-overview.md`：Node-API 简介（基于 Node.js 18.x LTS 扩展，不完全兼容）、架构组成（Native Module/Node-API/ModuleManager/ScopeManager/ReferenceManager/NativeEngine/ArkTS Runtime）、初始化阶段流程（import → 加载 so → 注册模块 → 挂载 exports）、调用阶段流程（ArkTS 调用 → 引擎查找 → C/C++ 方法执行），来源 `coding` 中 Node-API 简介
- [x] 3.5 编写 `05-node-api-development.md`：**核心文档**——使用 Node-API 实现跨语言交互的完整开发流程：模块注册（napi_module + __attribute__((constructor))）、模块初始化/接口映射（napi_property_descriptor + napi_define_properties）、index.d.ts 声明、oh-package.json5 关联、CMakeLists.txt 配置（target_link_libraries libace_napi.z.so）、Native 方法实现（napi_get_cb_info/napi_get_value_*/napi_create_*/napi_call_function）、ArkTS 侧调用（import from libentry.so）、约束限制（SO 命名规则/多线程限制/调试建议），含完整代码示例，来源 `coding` 中 Node-API 开发流程
- [x] 3.6 编写 `06-node-api-best-practices.md`：**核心文档**——Node-API 开发规范与红线：参数获取规范（argv 长度/argc 初始化）、生命周期管理（napi_open_handle_scope/napi_close_handle_scope）、上下文敏感（禁止跨 napi_env）、异常处理（每次调用后检查返回值）、异步任务（推荐 napi_threadsafe_function，不推荐 uv_queue_work）、对象绑定（napi_wrap result 传 nullptr vs 非 nullptr）、高性能数组（ArrayBuffer vs JSArray，性能差 400 倍+）、数据转换优化、模块注册与命名约束（Init 加 static/函数名唯一/nm_modname 与 so 名匹配/一个 so 一个模块）、dlopen 场景（导出 napi_onLoad）、napi_create_external 限制（仅当前线程/跨线程用 napi_coerce_to_native_binding_object）、buffer 释放（napi_get_arraybuffer_info 返回的 data 不可手动释放），来源 `coding` 中 Node-API 开发规范
- [x] 3.7 编写 `07-rawfile.md`：Native Rawfile 接口（OH_ResourceManager_InitNativeResourceManager/OpenRawDir/GetRawFileCount/GetRawFileName/OpenRawFile/GetRawFileSize/ReadRawFile/CloseRawFile/GetRawFileDescriptor/IsRawDir/ReleaseNativeResourceManager）、64 后缀大文件接口、开发步骤（CMakeLists.txt 添加依赖/index.d.ts 声明/代码实现：GetFileList/GetRawFileContent/GetRawFileDescriptor/IsRawDir），来源 `rawfile-guidelines`
- [x] 3.8 编写 `08-native-bundle.md`：Native Bundle 接口（OH_NativeBundle_GetCurrentApplicationInfo/GetAppId/GetAppIdentifier/GetMainElementName/GetCompatibleDeviceType/IsDebugMode/GetModuleMetadata/GetAbilityResourceInfo）、开发步骤（CMakeLists.txt 添加依赖/头文件/Node-API 映射）、内存管理（返回的 char* 需手动 free），来源 `native-bundle-guidelines`
- [x] 3.9 编写 `09-build-toolchain.md`：编译工具链配置（CMake/GN/Make/Configure 构建 ohos.toolchain.cmake）、lycium 交叉编译框架、跨语言调用复杂参数传递、Native 侧子线程与 UI 主线程通信，来源 `build-toolchain`
- [x] 3.10 编写 `10-debugging-profiling.md`：C/C++ 内存错误检测（ASan 启用方式/CMake 编译选项/DevEco Studio 配置）、LLDB 高性能调试器基本使用，概览形式 + 官方链接，来源 `debugging-profiling`
- [x] 3.11 编写 `11-hardware-compatibility.md`：HarmonyOS ABI 类型（armeabi-v7a/arm64-v8a/x86_64）、CPU 特性查询、Neon 指令扩展启用方式，概览形式 + 官方链接，来源 `hardware-compatibility`
- [x] 3.12 为每份参考文档顶部标注上游 URL 与抓取时间

## 4. 编写 SKILL.md

- [x] 4.1 编写 frontmatter（`name: arkts-ndk-dev` + `description`，description 含触发关键词：Node-API/napi/NDK/C++ 互操作/Native/CMake/so/napi_wrap/napi_threadsafe_function/Rawfile/NativeBundle/ASan/LLDB/ABI/Neon 等）
- [x] 4.2 编写「何时启用本 skill」章节，列出触发条件与关键词清单
- [x] 4.3 编写「与已有 skill 的边界」章节，明确与 `arkts-helper`/`arkts-debug`/`arkts-build` 的交叉引用关系
- [x] 4.4 编写「工作流程（严格遵守）」章节：先读 INDEX → 按场景加载文档 → 写代码/配工具链 → 核对红线 → 引用来源
- [x] 4.5 编写「Node-API 红线速查表」：线程安全 / 生命周期 / 模块注册 / 异步任务 / 对象绑定 / 性能 6 大类红线
- [x] 4.6 编写「高频代码模板」：模块注册模板 / 接口映射模板 / 参数获取与类型转换模板 / napi_threadsafe_function 模板
- [x] 4.7 编写「目录结构」与「文档来源与维护」章节（上游 URL、更新方式说明）

## 5. 验证与收尾

- [x] 5.1 检查 `references/` 目录文件清单与 SKILL.md 中「目录结构」章节一致
- [x] 5.2 检查 SKILL.md 的 frontmatter 格式与已有 skill（arkts-build/arkts-helper/arkts-debug）一致
- [x] 5.3 检查所有参考文档顶部均标注上游 URL 与抓取时间
- [x] 5.4 检查 INDEX.md 的「任务类型 → 必读文件」映射表覆盖所有 11 份文档
- [x] 5.5 检查 `05-node-api-development.md` 和 `06-node-api-best-practices.md` 的红线内容与 SKILL.md 红线速查表一致
- [x] 5.6 运行 `openspec status --change "arkts-ndk-dev"` 确认所有 artifact 完成
