## Context

arkts-debug 是一个为 HarmonyOS 开发者提供 ArkTS 编译错误诊断与修复的技能，当前包含 22 个错误类别，每个类别有对应的 `references/*.md` 文档和 `assets/*.ets` 代码示例。经审查发现：

1. **合规问题**：4 个现有代码资产文件使用了不符合 ArkTS 严格模式约束的写法
2. **内容遗漏**：华为官方 FAQ（ide-hvigor-faqs）中记录了 6 类常见 ArkTS 编译错误，当前技能未覆盖

## Goals / Non-Goals

**Goals:**
- 修正所有现有资产文件中的 ArkTS 合规问题，确保代码示例能通过 ArkTS 严格模式编译
- 补充 FAQ 文档中记录的 6 类遗漏错误，保持与现有 22 个类别一致的文档结构
- 更新 SKILL.md 主配置文件以反映新增和修正内容

**Non-Goals:**
- 不重构现有技能的工作流或目录结构
- 不覆盖 arkts-helper 技能已处理的通用 ArkTS 语言约束（如 arkts-no-any-unknown、arkts-no-var 等），仅聚焦编译报错诊断场景
- 不修改 arkts-helper 或其他技能的文件

## Decisions

### D1: 合规修正策略 — 最小化改动

对现有资产文件的修正采用最小化改动原则，仅修正违反 ArkTS 约束的代码，不重构整体结构。

| 文件 | 问题 | 修正方式 |
|------|------|----------|
| `PossiblyNullError.ets` | `{ id, name } as User` 类型断言 | 改用 `new User()` 构造函数 |
| `IDataSourceError.ets` | LazyForEach 回调返回 `: void` | 移除 `: void`，让编译器推断组件返回类型 |
| `ObjectSpreadError.ets` | `Partial<Point>` 映射类型 | 定义显式 `PatchPoint` 接口替代 |
| `StandaloneFunctionError.ets` | `constructor(private context: ...)` 参数属性 | 显式声明 `private context` 字段并在构造函数中赋值 |

**替代方案**：删除有问题的示例代码，仅保留正确写法。**否决原因**：保留 before/after 对比对用户理解错误更有帮助。

### D2: 新增错误类别的文档结构 — 遵循现有模式

每个新增错误类别遵循现有模式：
- `references/<topic>_errors.md`：包含 Symptom、Root Cause、Canonical Fix、Notes、See Also 五个部分
- `assets/<Topic>Error.ets`：包含 BAD（注释）和 GOOD（可编译）代码示例
- SKILL.md 中添加对应的 Category、Quick Reference 和 Detailed Solution 条目

### D3: 新增类别选择 — 基于 FAQ 文档优先

优先补充华为官方 FAQ 文档中明确记录的 ArkTS 编译错误，确保与官方文档对齐。arkts-helper 中记录的 30+ 条通用约束（如 arkts-no-var、arkts-no-eval）属于语言迁移范畴，不在 arkts-debug 的编译报错诊断定位内。

## Risks / Trade-offs

- **[风险] Partial<Point> 替代方案可能不够通用** → 缓解：在文档中说明 `Partial` 是映射类型，ArkTS 不支持，需为每个场景定义具体接口
- **[风险] 新增 6 个类别使 SKILL.md 更长** → 缓解：SKILL.md 已有 22 个类别，结构一致，增量可控
- **[风险] IDataSourceError.ets 移除 `: void` 后回调签名可能不精确** → 缓解：ArkUI 的 LazyForEach 第二个参数本就是组件构建函数，不需要 void 返回类型
