## ADDED Requirements

### Requirement: TS→ArkTS 适配背景参考文档
系统 SHALL 提供离线参考文档 `references/03-ts-to-arkts-migration-background.md`，覆盖 ArkTS 语法适配背景，包括方舟运行时兼容 TS/JS 的约束、ArkTS 设计理念等。

#### Scenario: 开发者了解 ArkTS 适配背景
- **WHEN** 开发者询问为什么 ArkTS 需要适配规则或方舟运行时的兼容性约束
- **THEN** 系统 SHALL 从 `references/03-ts-to-arkts-migration-background.md` 中提取相关内容

### Requirement: TS→ArkTS 适配规则参考文档
系统 SHALL 提供离线参考文档 `references/04-ts-to-arkts-migration-rules.md`，覆盖从 TypeScript 到 ArkTS 的完整适配规则，包括：强制静态类型规则、禁止运行时改变对象布局规则、限制运算符语义规则、不支持 Structural typing 规则，以及每条规则的具体约束和示例。

#### Scenario: 开发者查询具体适配规则
- **WHEN** 开发者询问 "ArkTS 中为什么不能用 as 类型断言" 或 "ArkTS 对象布局限制是什么"
- **THEN** 系统 SHALL 从 `references/04-ts-to-arkts-migration-rules.md` 中提取对应规则并提供说明和示例

#### Scenario: 开发者迁移 TS 代码到 ArkTS
- **WHEN** 开发者需要将现有 TypeScript 代码迁移到 ArkTS
- **THEN** 系统 SHALL 从 `references/04-ts-to-arkts-migration-rules.md` 中逐条检查适配规则，指导代码修改

### Requirement: TS→ArkTS 适配案例参考文档
系统 SHALL 提供离线参考文档 `references/05-ts-to-arkts-migration-cases.md`，覆盖适配指导案例，提供常见 TS 代码到 ArkTS 的转换实例。

#### Scenario: 开发者查看适配案例
- **WHEN** 开发者需要查看 TS 代码到 ArkTS 的具体转换示例
- **THEN** 系统 SHALL 从 `references/05-ts-to-arkts-migration-cases.md` 中提取相关案例

### Requirement: 迁移指导工作流
SKILL.md SHALL 定义迁移指导工作流：1) 先读 INDEX.md 了解文档角色；2) 根据场景加载对应参考文档；3) 按适配规则逐条检查代码；4) 提供修改建议并引用来源。

#### Scenario: 执行 TS→ArkTS 迁移工作流
- **WHEN** 开发者请求将一段 TS 代码迁移为 ArkTS 代码
- **THEN** 系统 SHALL 按 INDEX.md 查阅路径加载适配背景→适配规则→适配案例，逐条检查并提供修改建议
