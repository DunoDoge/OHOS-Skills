# OHOS-Skills 有效性测试用例

基于各 skill 的 `SKILL.md` 触发条件、红线规则和边界定义生成。每条用例包含：测试输入、预期激活的 skill、预期行为（有/无 skill 对比）。

---

## 一、arkts-helper 触发与红线测试

### H-01：ArkTS 语法 — 禁止 any/unknown

**输入：**

> 帮我写一个 ArkTS 函数，接收任意类型的参数并打印它。

**预期激活：** `arkts-helper`

**无 skill 预期：** 可能写出 `function print(val: any) { console.log(val) }`

**有 skill 预期：** 使用具体类型或泛型，如 `function print<T>(val: T) { console.log(val) }`，并引用 `references/04-ts-to-arkts-migration-rules.md` 中「强制使用静态类型」一节。

---

### H-02：ArkTS 语法 — 禁止 var

**输入：**

> 以下 ArkTS 代码有什么问题？`var count = 0;`

**预期激活：** `arkts-helper`

**无 skill 预期：** 可能说没有问题，或仅建议用 `let` 作为风格偏好。

**有 skill 预期：** 明确指出 ArkTS 不支持 `var`，必须使用 `let` 或 `const`，引用 `references/04-ts-to-arkts-migration-rules.md`。

---

### H-03：ArkTS 语法 — 对象字面量必须对应已声明的类或接口

**输入：**

> 在 ArkTS 中，我想返回一个匿名对象 `{ name: "test", value: 42 }`，怎么写？

**预期激活：** `arkts-helper`

**无 skill 预期：** 可能直接返回匿名对象，认为 TypeScript 的写法没问题。

**有 skill 预期：** 先定义 interface 再使用，如 `interface Result { name: string; value: number }` 然后 `return { name: "test", value: 42 } as Result`，引用 `references/04-ts-to-arkts-migration-rules.md`。

---

### H-04：TS→ArkTS 迁移

**输入：**

> 我有一段 TypeScript 代码用了 `as` 类型断言和索引签名 `[key: string]: any`，怎么迁移到 ArkTS？

**预期激活：** `arkts-helper`

**无 skill 预期：** 可能保留 `as` 断言，建议用 `Record<string, any>` 替代索引签名。

**有 skill 预期：** 指出 ArkTS 限制 `as` 断言、不支持索引签名，建议使用显式类型声明和 `Map` 替代，引用 `references/04-ts-to-arkts-migration-rules.md` 和 `references/05-ts-to-arkts-migration-cases.md`。

---

### H-05：ArkTS 高性能编程 — const vs let

**输入：**

> 以下 ArkTS 代码有性能问题吗？`let MAX_SIZE = 100; let items: string[] = [];`

**预期激活：** `arkts-helper`

**无 skill 预期：** 可能只建议风格改进。

**有 skill 预期：** 指出 `MAX_SIZE` 不变应使用 `const`，引用 `references/06-arkts-high-performance.md` 中「不变的变量必须用 const 声明」红线。

---

### H-06：ArkTS 并发 — TaskPool/Worker

**输入：**

> ArkTS 中如何执行耗时计算任务而不阻塞主线程？

**预期激活：** `arkts-helper`

**无 skill 预期：** 可能建议用 `setTimeout` 或 Web Worker 语法。

**有 skill 预期：** 推荐使用 `TaskPool` 或 `Worker`，引用 `references/11-arkts-concurrency-multithread.md`，给出 `@Concurrent` 装饰器和 `taskpool.execute()` 示例。

---

### H-07：ArkTS 容器类库

**输入：**

> ArkTS 中用什么替代 JavaScript 的 Array 和 Object 来获得更好的性能？

**预期激活：** `arkts-helper`

**无 skill 预期：** 可能说 Array 性能足够，或建议用 TypedArray。

**有 skill 预期：** 推荐 `ArrayList`、`HashMap`、`TreeMap` 等 ArkTS 容器类，引用 `references/09-arkts-container-library.md`。

---

## 二、arkts-debug 触发与修复测试

### D-01：Possibly Null 错误

**输入：**

> 编译报错：`Property 'length' cannot be accessed on a value that is possibly null.` 代码：`let len = arr!.length`

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议加 `!` 非空断言或 `as` 强转。

**有 skill 预期：** 建议添加 `!== null` 检查或使用可选链 `?.`，引用 `references/possibly_null_errors.md`，给出 BAD/GOOD 对比。

---

### D-02：Indexed Access 错误 (arkts-no-props-by-index)

**输入：**

> 报错 `arkts-no-props-by-index`：`obj['key']` 不允许，怎么修改？

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议 `(obj as any)['key']` 绕过。

**有 skill 预期：** 使用点号访问 `obj.key` 或 `Map` 替代，引用 `references/indexed_access_errors.md`，明确禁止 `as any` 绕过。

---

### D-03：Declaration Merging 错误 (arkts-no-decl-merging)

**输入：**

> 报错 `arkts-no-decl-merging`：`Declaration merging is not supported`，我有两个同名的 interface 想合并。

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议用 `declare module` 扩展或 namespace 合并。

**有 skill 预期：** 合并为单个声明或使用 `extends`，引用 `references/decl_merging_errors.md`。

---

### D-04：AppStorage.get 类型错误

**输入：**

> `AppStorage.get('count')` 返回类型推断错误，怎么正确使用？

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议 `AppStorage.get<number>('count')` 泛型参数。

**有 skill 预期：** 推荐使用 `@StorageLink` 配合 `LocalStorage` 或 `AppStorage.setAndLink`，避免 `setOrCreate`，引用 `references/appstorage_errors.md`。

---

### D-05：@StorageLink 默认值错误

**输入：**

> `@StorageLink('key') value: string` 报错缺少默认值。

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议加 `!` 非空断言。

**有 skill 预期：** 添加 `= undefined` 或具体默认值，如 `@StorageLink('key') value: string = ''`，引用 `references/storage_link_default_errors.md`。

---

### D-06：Object Literal Interface 错误

**输入：**

> 报错 `Object literal must correspond to some explicitly declared class or interface`，代码是 `return { x: 1, y: 2 }`

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议加 `as Point` 类型断言。

**有 skill 预期：** 先定义 `interface Point { x: number; y: number }` 再使用，引用 `references/object_literal_interface_errors.md`。

---

### D-07：ESObject 类型错误

**输入：**

> 使用 `ESObject` 类型时报错，ArkTS 中如何处理动态类型？

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议用 `any` 或保留 `ESObject`。

**有 skill 预期：** 使用具体类型或 `ESModule` 替代 `ESObject`，引用 `references/esobject_type_errors.md`。

---

### D-08：IDataSource / LazyForEach 错误

**输入：**

> `LazyForEach` 报错：数据源必须实现 `IDataSource` 接口。

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议用普通 `ForEach` 替代。

**有 skill 预期：** 实现 `IDataSource` 接口的 `totalCount()`、`getData()`、`registerDataChangeListener()` 等方法，引用 `references/idata_source_errors.md`。

---

### D-09：Duplicate @Entry 错误

**输入：**

> 同一个 `.ets` 文件中有两个 `@Entry` 装饰器，报错怎么修？

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议删除一个 `@Entry` 但不解释原因。

**有 skill 预期：** 移除多余的 `@Entry`，子组件使用 `@Component`，引用 `references/duplicate_entry_errors.md`。

---

### D-10：Circular Import 错误

**输入：**

> 报错 `Maximum call stack` 或循环依赖，模块 A 导入 B，B 又导入 A。

**预期激活：** `arkts-debug`

**无 skill 预期：** 可能建议用 `import type` 延迟导入。

**有 skill 预期：** 将共享类型提取到独立模块，引用 `references/circular_import_errors.md`。

---

## 三、arkts-build 触发与命令测试

### B-01：命令行构建 HAP

**输入：**

> 如何用命令行构建 HarmonyOS debug HAP？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能给出 `gradle assembleDebug` 或 `npm run build`。

**有 skill 预期：** 给出 `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon`，引用 `references/04-hvigorw.md`，强调 CI 必须加 `--no-daemon`。

---

### B-02：构建前安装依赖

**输入：**

> 运行 `hvigorw assembleHap` 报依赖找不到，怎么办？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能建议 `npm install`。

**有 skill 预期：** 需要分别进入工程及各模块执行 `ohpm install`，引用 `references/05-ohpm.md` 和 `references/06-building-app.md`。

---

### B-03：codelinter CI 门禁

**输入：**

> 如何在 CI 中配置 codelinter 检查，有错误就失败？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能建议 `eslint --max-warnings 0`。

**有 skill 预期：** 给出 `codelinter -c code-linter.json5 -f json -o report.json --exit-on error`，解释 `--exit-on` 的二进制位组合逻辑，引用 `references/02-codelinter.md`。

---

### B-04：release 崩溃堆栈解析

**输入：**

> 线上 release 包崩溃了，有混淆堆栈，怎么还原？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能建议用 `source-map` npm 包或 Chrome DevTools。

**有 skill 预期：** 使用 `hstack`，需要 sourceMap + nameCache + so 归档目录，给出完整命令如 `hstack -i D:\crashDir -o D:\outputDir -s D:\sourcemapDir --so D:\soDir -n D:\nameCacheDir`，引用 `references/03-hstack.md`。

---

### B-05：签名 HAP

**输入：**

> 如何给 HarmonyOS HAP 签名？需要哪些文件？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能建议 `jarsigner` 或 `apksigner`。

**有 skill 预期：** 使用 `hap-sign-tool.jar`，需要 .p12（密钥）、.cer（证书）、.p7b（Profile）三件套，给出完整签名命令，引用 `references/06-building-app.md`。

---

### B-06：模块级构建参数

**输入：**

> 我想只构建 library 模块的 HSP，`hvigorw assembleHsp -p module=library@default` 为什么不生效？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能建议检查模块名拼写。

**有 skill 预期：** 指出 `-p module=` 必须搭配 `--mode module`，正确命令为 `hvigorw assembleHsp --mode module -p module=library@default -p product=default --no-daemon`，引用 `references/04-hvigorw.md`。

---

### B-07：ohpm 仓库配置

**输入：**

> `ohpm install` 报网络错误，怎么配置 ohpm 仓库地址？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能建议 `npm config set registry`。

**有 skill 预期：** 给出 `ohpm config set registry https://ohpm.openharmony.cn/ohpm/`，引用 `references/05-ohpm.md`。

---

### B-08：设备安装运行

**输入：**

> 构建好 HAP 后，怎么推到设备上安装运行？

**预期激活：** `arkts-build`

**无 skill 预期：** 可能建议 `adb install`。

**有 skill 预期：** 给出三步命令：`hdc file send` → `hdc shell bm install` → `hdc shell aa start`，引用 `references/07-debugging-commands.md` 和 `references/06-building-app.md`。

---

## 四、arkts-ndk-dev 触发与红线测试

### N-01：Node-API 模块注册

**输入：**

> 如何在 HarmonyOS 中注册一个 Node-API 模块，让 ArkTS 调用 C++ 函数？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能给出 Node.js 的 `NAPI_MODULE(init)` 宏。

**有 skill 预期：** 使用 `napi_module` 结构体 + `__attribute__((constructor))` 自动注册，`nm_modname` 必须与 so 名匹配，引用 `references/05-node-api-development.md`。

---

### N-02：napi_env 线程安全

**输入：**

> 我在子线程中用 `napi_call_function(env, ...)` 回调 ArkTS，为什么崩溃？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能建议加锁或用 `uv_queue_work`。

**有 skill 预期：** 明确指出 `napi_env` 与 ArkTS 线程绑定，禁止跨线程使用；必须用 `napi_threadsafe_function`，引用 `references/06-node-api-best-practices.md` 中「线程安全」红线。

---

### N-03：napi_wrap 内存管理

**输入：**

> `napi_wrap` 的 result 参数传 nullptr 和传非 nullptr 有什么区别？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能说不影响，或认为 result 是返回值。

**有 skill 预期：** 传 nullptr 由系统管理生命周期；传非 nullptr 需手动 `napi_remove_wrap`，否则内存泄漏，引用 `references/06-node-api-best-practices.md`。

---

### N-04：ArrayBuffer vs JSArray 性能

**输入：**

> Node-API 中传递大量数值数据给 ArkTS，用 JSArray 还是 ArrayBuffer？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能说两者差不多，或推荐 JSArray 更方便。

**有 skill 预期：** ArrayBuffer 性能比 JSArray 快 400 倍以上，存储值类型数据必须用 ArrayBuffer，引用 `references/06-node-api-best-practices.md`。

---

### N-05：handle scope 使用

**输入：**

> 在循环中频繁创建 JS 对象，运行一段时间后内存持续增长，怎么修？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能建议减少对象创建或手动 GC。

**有 skill 预期：** 循环中必须使用 `napi_open_handle_scope` / `napi_close_handle_scope` 成对管理，引用 `references/06-node-api-best-practices.md`。

---

### N-06：CMake 工具链配置

**输入：**

> HarmonyOS NDK 工程的 CMakeLists.txt 怎么配置交叉编译？需要引入哪个工具链文件？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能建议手动设置 `CMAKE_SYSTEM_NAME` 和编译器路径。

**有 skill 预期：** 使用 `ohos.toolchain.cmake`，通过 `-DOHOS_STL=c++_shared` 等变量配置，引用 `references/03-build-ndk-project.md` 和 `references/09-build-toolchain.md`。

---

### N-07：Rawfile 资源访问

**输入：**

> 在 C++ 侧如何读取 `resources/rawfile/` 下的文件？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能建议用标准 C++ `std::ifstream` 读取相对路径。

**有 skill 预期：** 使用 `Rawfile` API（`OpenRawFile`、`ReadRawFile`），引用 `references/07-rawfile.md`。

---

### N-08：napi_create_external 跨线程

**输入：**

> 用 `napi_create_external` 创建的对象能在子线程中使用吗？

**预期激活：** `arkts-ndk-dev`

**无 skill 预期：** 可能说可以，因为 external 是 C++ 指针。

**有 skill 预期：** `napi_create_external` 创建的对象仅当前线程可用，跨线程需 `napi_coerce_to_native_binding_object`，引用 `references/06-node-api-best-practices.md`。

---

## 五、Skill 边界与交叉引用测试

### X-01：构建报错 → arkts-build + arkts-debug

**输入：**

> 运行 `hvigorw assembleHap` 构建失败，报错 `arkts-no-props-by-index`。

**预期激活：** `arkts-build`（构建命令）+ `arkts-debug`（编译报错修复）

**预期行为：** 先用 `arkts-debug` 定位并修复代码错误，再用 `arkts-build` 重新构建，两个 skill 交叉引用。

---

### X-02：NDK 开发 + 编译报错 → arkts-ndk-dev + arkts-debug

**输入：**

> 我在写 Node-API 模块，但 ArkTS 侧调用时编译报错 `Object literal must correspond to some explicitly declared class or interface`。

**预期激活：** `arkts-ndk-dev`（Node-API 开发）+ `arkts-debug`（ArkTS 编译报错）

**预期行为：** `arkts-debug` 修复 ArkTS 侧的对象字面量问题，`arkts-ndk-dev` 指导 C++ 侧的 Node-API 代码。

---

### X-03：ArkTS 语法 + NDK 互操作 → arkts-helper + arkts-ndk-dev

**输入：**

> ArkTS 中如何声明一个与 C++ 侧结构体对应的 Sendable 类？

**预期激活：** `arkts-helper`（ArkTS 语法/Sendable）+ `arkts-ndk-dev`（跨语言交互）

**预期行为：** `arkts-helper` 指导 Sendable 类的语法，`arkts-ndk-dev` 指导 C++ 侧数据如何通过 Node-API 传递。

---

### X-04：构建命令 + NDK → arkts-build + arkts-ndk-dev

**输入：**

> 如何用命令行构建包含 Native C++ 模块的 HarmonyOS 工程？

**预期激活：** `arkts-build`（构建命令）+ `arkts-ndk-dev`（CMake/NDK 配置）

**预期行为：** `arkts-build` 给出 `hvigorw` 构建命令和 `syncNative` 参数，`arkts-ndk-dev` 指导 CMakeLists.txt 配置。

---

### X-05：纯语法问题不应触发 arkts-debug

**输入：**

> ArkTS 中 `enum` 支持异构枚举吗？

**预期激活：** `arkts-helper`（不应激活 `arkts-debug`）

**预期行为：** 仅 `arkts-helper` 响应，指出 ArkTS 仅支持数字枚举和字符串枚举，不支持异构枚举，引用 `references/01-arkts-language-introduction.md`。

---

### X-06：纯构建问题不应触发 arkts-helper

**输入：**

> `hvigorw assembleHap` 报错 `Error: The product name is not configured`，怎么修？

**预期激活：** `arkts-build`（不应激活 `arkts-helper`）

**预期行为：** 仅 `arkts-build` 响应，指导检查 `build-profile.json5` 中的 product 配置，引用 `references/04-hvigorw.md`。

---

## 六、引用来源验证测试

以下用例专门验证 agent 是否正确引用了离线文档：

### R-01

**输入：** ArkTS 中为什么不能用 `as` 类型断言？

**验证点：** 回答应引用 `arkts-helper/references/04-ts-to-arkts-migration-rules.md`，而非笼统说「官方文档」。

### R-02

**输入：** `arkts-no-props-by-index` 报错怎么修？

**验证点：** 回答应引用 `arkts-debug/references/indexed_access_errors.md`，并提及 `assets/IndexedAccessError.ets` 示例。

### R-03

**输入：** CI 流水线怎么配置 hvigorw 构建？

**验证点：** 回答应引用 `arkts-build/references/06-building-app.md`，并提及 `--no-daemon` 红线。

### R-04

**输入：** `napi_wrap` 的 result 参数怎么传？

**验证点：** 回答应引用 `arkts-ndk-dev/references/06-node-api-best-practices.md`，而非 Node.js 官方文档。

---

## 评分标准

| 维度 | 权重 | 评分方式 |
|------|------|---------|
| Skill 激活准确性 | 30% | 是否激活了正确的 skill，未误触发 |
| 红线拦截率 | 25% | 违反红线的代码/命令是否被拦截并纠正 |
| 文档引用准确性 | 25% | 是否引用了正确的离线文档，而非凭经验猜测 |
| 边界处理 | 20% | 跨 skill 场景是否正确交叉引用，不混淆职责 |

每条用例按 Pass / Partial / Fail 三级评定，最终按权重加权计算总分。
