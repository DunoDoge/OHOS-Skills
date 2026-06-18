## Why

arkts-debug skill 当前的 22 个错误类别未覆盖华为官方 FAQ 文档（ide-hvigor-faqs）中记录的多个常见 ArkTS 编译错误（如 `arkts-no-props-by-index`、`arkts-no-decl-merging`、推断类型不可命名等），且部分现有代码资产（assets/）存在不符合 ArkTS 语言约束的问题（如使用 `as` 类型断言、`Partial<>` 映射类型、构造函数参数属性简写等），需要修正以确保代码示例本身能通过 ArkTS 严格模式编译。

## What Changes

- **修正现有资产中的 ArkTS 合规问题**：
  - `PossiblyNullError.ets`：将 `{ id: 1, name: 'Alice' } as User` 改为使用 `new User()` 构造函数
  - `IDataSourceError.ets`：修正 LazyForEach 回调返回类型 `: void` 为正确的组件返回类型
  - `ObjectSpreadError.ets`：移除 `Partial<Point>` 映射类型，改用显式接口定义
  - `StandaloneFunctionError.ets`：将 `constructor(private context: ...)` 参数属性简写改为显式字段声明
  - 同步修正对应 references/ 文档中的相同问题

- **新增 FAQ 文档中记录的遗漏错误类别**（含 references/ 和 assets/）：
  - `arkts-no-props-by-index`：禁止索引访问属性（`obj['key']`）
  - `arkts-no-decl-merging`：禁止声明合并 / 变量重复声明
  - 推断类型不可命名：需要显式类型注解
  - 空数组类型推断：`[][]` 需显式元素类型
  - 模块解析错误：Cannot find module / no exported member
  - 循环导入：Maximum call stack size exceeded

- **更新 SKILL.md**：在错误类别表、快速参考表和详细解决方案中添加新增条目

## Capabilities

### New Capabilities
- `indexed-access-errors`: 覆盖 arkts-no-props-by-index 索引属性访问错误的诊断与修复
- `decl-merging-errors`: 覆盖 arkts-no-decl-merging 声明合并及变量重复声明错误的诊断与修复
- `inferred-type-naming-errors`: 覆盖推断类型不可命名错误的诊断与修复
- `array-type-inference-errors`: 覆盖空数组类型推断错误的诊断与修复
- `module-resolution-errors`: 覆盖模块解析错误（Cannot find module / no exported member）的诊断与修复
- `circular-import-errors`: 覆盖循环导入错误的诊断与修复

### Modified Capabilities
- `existing-asset-compliance`: 修正现有 4 个资产文件及对应引用文档中的 ArkTS 合规问题

## Impact

- **代码文件**：修改 4 个 assets/*.ets 文件 + 对应 references/*.md 文件；新增 6 组 references/*.md + assets/*.ets 文件
- **SKILL.md**：更新错误类别表、快速参考表、详细解决方案部分
- **向后兼容**：新增错误类别为纯增量，不影响现有功能；修正合规问题可能改变代码示例风格但不影响语义
