## 1. 修正现有资产合规问题

- [x] 1.1 修正 `assets/PossiblyNullError.ets`：将 `{ id: 1, name: 'Alice' } as User` 改为 `new User(1, 'Alice')`，添加 User 构造函数
- [x] 1.2 修正 `references/possibly_null_errors.md`：同步更新代码示例，移除 `as User` 断言
- [x] 1.3 修正 `assets/IDataSourceError.ets`：移除 LazyForEach 回调的 `: void` 返回类型注解
- [x] 1.4 修正 `references/idata_source_errors.md`：同步更新 LazyForEach 代码示例（已确认无需修改，引用文档已是正确写法）
- [x] 1.5 修正 `assets/ObjectSpreadError.ets`：将 `Partial<Point>` 替换为显式 `PatchPoint` 接口
- [x] 1.6 修正 `references/object_spread_errors.md`：同步更新 mergePoint 示例，移除 `Partial`
- [x] 1.7 修正 `assets/StandaloneFunctionError.ets`：将 `constructor(private context: ...)` 改为显式字段声明 + 构造函数赋值
- [x] 1.8 修正 `references/standalone_function_errors.md`：同步更新类方法示例

## 2. 新增 Indexed Access Errors（arkts-no-props-by-index）

- [x] 2.1 创建 `references/indexed_access_errors.md`：包含 Symptom、Root Cause、Canonical Fix、Notes、See Also
- [x] 2.2 创建 `assets/IndexedAccessError.ets`：BAD 注释展示 `obj['key']` 模式，GOOD 展示点号访问和 Map 替代方案

## 3. 新增 Declaration Merging Errors（arkts-no-decl-merging）

- [x] 3.1 创建 `references/decl_merging_errors.md`：包含 Symptom、Root Cause、Canonical Fix、Notes、See Also
- [x] 3.2 创建 `assets/DeclMergingError.ets`：BAD 注释展示重复声明/命名空间合并，GOOD 展示合并为单一声明

## 4. 新增 Inferred Type Naming Errors

- [x] 4.1 创建 `references/inferred_type_naming_errors.md`：包含 Symptom、Root Cause、Canonical Fix、Notes、See Also
- [x] 4.2 创建 `assets/InferredTypeNamingError.ets`：BAD 注释展示缺少返回类型注解的导出函数，GOOD 展示显式类型注解

## 5. 新增 Array Type Inference Errors

- [x] 5.1 创建 `references/array_type_inference_errors.md`：包含 Symptom、Root Cause、Canonical Fix、Notes、See Also
- [x] 5.2 创建 `assets/ArrayTypeInferenceError.ets`：BAD 注释展示 `[][] = []`，GOOD 展示 `string[][] = []`

## 6. 新增 Module Resolution Errors

- [x] 6.1 创建 `references/module_resolution_errors.md`：包含 Symptom、Root Cause、Canonical Fix、Notes、See Also
- [x] 6.2 创建 `assets/ModuleResolutionError.ets`：BAD 注释展示错误导入路径/大小写不匹配，GOOD 展示正确导入

## 7. 新增 Circular Import Errors

- [x] 7.1 创建 `references/circular_import_errors.md`：包含 Symptom、Root Cause、Canonical Fix、Notes、See Also
- [x] 7.2 创建 `assets/CircularImportError.ets`：BAD 注释展示循环导入，GOOD 展示共享模块提取

## 8. 更新 SKILL.md 主配置

- [x] 8.1 在 Error Categories 表中添加 6 个新类别
- [x] 8.2 在 Quick Reference 表中添加 6 个新条目
- [x] 8.3 在 Detailed Error Solutions 中添加 6 个新条目（含 references/ 和 assets/ 链接）
- [x] 8.4 更新 SKILL.md frontmatter description，添加新的触发关键词（arkts-no-props-by-index、arkts-no-decl-merging、Cannot find module、Maximum call stack）
