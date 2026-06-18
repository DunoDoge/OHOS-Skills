## ADDED Requirements

### Requirement: ArkTS 高性能编程参考文档
系统 SHALL 提供离线参考文档 `references/06-arkts-high-performance.md`，覆盖 ArkTS 高性能编程实践，包括：声明与表达式优化（const 声明、避免整型浮点混用、避免溢出、循环常量提取）、函数优化（参数传递、避免可选参数、避免函数参数重新赋值）、数组与容器优化（数组初始化、避免稀疏数组、使用 ArkTS 容器类）、并发优化等。

#### Scenario: 开发者查询性能优化建议
- **WHEN** 开发者询问 "ArkTS 如何提升性能" 或 "ArkTS 高性能编程有哪些实践"
- **THEN** 系统 SHALL 从 `references/06-arkts-high-performance.md` 中提取相关优化建议

#### Scenario: 开发者查询特定优化项
- **WHEN** 开发者询问 "ArkTS 中为什么建议用 const" 或 "ArkTS 数组怎么初始化性能最好"
- **THEN** 系统 SHALL 从 `references/06-arkts-high-performance.md` 中提取对应优化项的详细说明

### Requirement: SKILL.md 包含高性能编程红线表
SKILL.md SHALL 包含高性能编程红线速查表，至少覆盖：必须使用 const 声明不变变量、避免整型浮点混用、避免稀疏数组、避免函数参数重新赋值、使用 ArkTS 容器类替代 Array 等关键红线项。

#### Scenario: 开发者快速了解性能红线
- **WHEN** 开发者询问 ArkTS 性能编程有哪些必须遵守的规则
- **THEN** 系统 SHALL 直接从 SKILL.md 的红线表中提供关键规则概览

### Requirement: 性能优化建议必须引用来源
系统在提供性能优化建议时 SHALL 引用来源参考文档编号和章节，确保建议可追溯。

#### Scenario: 性能建议附带来源
- **WHEN** 系统建议开发者使用 const 声明不变变量
- **THEN** 系统 SHALL 引用 "参考 06-arkts-high-performance.md > 声明与表达式 > 使用const声明不变的变量"
