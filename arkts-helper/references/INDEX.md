# ArkTS 参考文档索引

本目录文档来源于 OpenHarmony 官方文档仓库 `zh-cn/application-dev/quick-start/` 下的「学习ArkTS语言」一节，与华为开发者文档站「学习ArkTS语言」目录同源（开源版本，内容一致）。

- 上游仓库：<https://gitee.com/openharmony/docs>
- 上游路径：`zh-cn/application-dev/quick-start/`
- 分支：`master`
- 抓取时点：见各文件的 git 历史；本地副本仅作离线参考使用

> 文档中出现的相对链接（如 `../arkts-utils/...`）指向上游仓库的兄弟目录，本地副本未跟随抓取。如需展开请直接到上游仓库查阅。

## 文件清单（按学习顺序）

| 序号 | 文件 | 章节标题 | 用途 |
| ---- | ---- | -------- | ---- |
| 01 | [01-arkts-get-started.md](./01-arkts-get-started.md) | 初识ArkTS语言 | 了解 ArkTS 与 TS 的差异、整体定位 |
| 02 | [02-introduction-to-arkts.md](./02-introduction-to-arkts.md) | ArkTS语言介绍 | 全量语法手册：基本类型、函数、类、接口、泛型、空安全、模块、关键字、注解、ArkUI 支持 |
| 03 | [03-arkts-coding-style-guide.md](./03-arkts-coding-style-guide.md) | ArkTS编程规范 | 命名、格式、编程实践等通用编码风格规范 |
| 04 | [04-arkts-migration-background.md](./04-arkts-migration-background.md) | ArkTS语法适配背景 | 解释为什么 ArkTS 在 TS 基础上做强约束 |
| 05 | [05-typescript-to-arkts-migration-guide.md](./05-typescript-to-arkts-migration-guide.md) | 从TypeScript到ArkTS的适配规则 | **核心强约束清单**，按 `arkts-xxx` 规则 ID 列出全部限制 |
| 06 | [06-arkts-more-cases.md](./06-arkts-more-cases.md) | 适配指导案例 | 上述规则配套的反例/正例代码示范 |
| 07 | [07-arkts-high-performance-programming.md](./07-arkts-high-performance-programming.md) | ArkTS高性能编程实践 | 声明、函数、数组、异常等性能敏感写法 |
| 08 | [08-getting-started-with-arkts-for-java-programmers.md](./08-getting-started-with-arkts-for-java-programmers.md) | 从Java到ArkTS的迁移指导 | 面向 Java 开发者的对照速查 |
| 09 | [09-getting-started-with-arkts-for-swift-programmers.md](./09-getting-started-with-arkts-for-swift-programmers.md) | 从Swift到ArkTS的迁移指导 | 面向 Swift 开发者的对照速查 |

## 按场景检索

| 你想知道… | 优先看 |
| -------- | ----- |
| ArkTS 是什么、和 TS 有何区别 | 01 → 04 |
| 某个语法（类、接口、泛型、空安全 …）怎么写 | 02 |
| 命名、缩进、注释、模块组织风格 | 03 |
| **TS 代码迁移到 ArkTS 时哪些写法被禁止** | 05（按 `arkts-no-xxx` 规则名查） |
| 某条规则该怎么改写 | 06（与 05 中规则 ID 对应） |
| 哪些写法影响性能、应避免 | 07 |
| 从 Java/Swift 学 ArkTS | 08 / 09 |

## 关键强约束速记（出自 03/05/07）

> 下列条目仅为提示，**任何具体编码决策都必须回到对应文档原文中确认**。

- 强制静态类型：禁用 `any` / `unknown`（`arkts-no-any-unknown`）
- 禁止运行时改变对象布局：禁止动态增删属性（`arkts-no-props-by-index` 等）
- 禁止结构化类型（structural typing）：类型必须按声明匹配
- 限制运算符语义：`+` 不能用于非数字类型等
- 不允许无类型对象字面量、不允许把对象字面量当类型用
- 不支持 `with`、`eval`、运行时 `typeof` 取类型字符串作类型判断
- 禁止可调用签名 / 索引签名 / 构造签名等动态特性
- 异常类型必须为 `Error` 子类，禁止 `catch (e: SomeType)` 自定义类型注解
- 模块默认严格，禁止 CommonJS 风格混用

完整清单见 `05-typescript-to-arkts-migration-guide.md`。
