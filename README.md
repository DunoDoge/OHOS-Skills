# OHOS-Skills

OpenHarmony / HarmonyOS 应用开发的 [opencode](https://opencode.ai) skill 集合。每个 skill 是一个自包含目录，包含 `SKILL.md`（含 frontmatter 描述触发条件）以及配套的离线参考文档与代码示例，用于让 AI agent 在编写、审阅或修复 ArkTS / `.ets` 代码时基于权威资料工作，而不是凭 TypeScript 经验猜测。

## Skills

| Skill | 用途 |
|-------|------|
| [`arkts-helper`](./arkts-helper) | 写、改、审 ArkTS 代码时的语法 / 规范 / 强约束权威参考。内置 9 篇官方「学习 ArkTS 语言」文档的离线副本，覆盖语法手册、编码规范、TS→ArkTS 迁移规则（`arkts-no-*`）、高性能编程等 |
| [`arkts-debug`](./arkts-debug) | 修复 HarmonyOS 编译报错。汇总 22 类常见错误（`ContentType`、`AppStorage.get`、`@StorageLink`、`getLastWindow`、`AvoidArea`、`TitleButtonRect`、`IDataSource`、`ESObject`、`Possibly null` 等），每类提供根因分析、规范修复方案与最小可复现 `.ets` 示例 |

两个 skill 互补：日常编码用 `arkts-helper`；命中 hvigor / ArkCompiler 报错时用 `arkts-debug`，未匹配的报错会回退到 `arkts-helper` 的迁移规则文档。

## 安装

将仓库克隆到任意位置，然后把需要的 skill 链接到 opencode 的 skill 目录：

```bash
git clone git@github.com:DunoDoge/OHOS-Skills.git
cd OHOS-Skills

# 链接到全局 skill 目录（推荐：源仓库的更新会自动同步）
ln -s "$PWD/arkts-helper"  ~/.config/opencode/skills/arkts-helper
ln -s "$PWD/arkts-debug"   ~/.config/opencode/skills/arkts-debug
```

也可以放到项目级 `.opencode/skills/` 下仅对单个工程启用。

链接完成后，在 opencode 内 skill 会按各自 `SKILL.md` 的 frontmatter `description` 自动触发：写 `.ets` / 提到 ArkUI、HarmonyOS NEXT、`arkts-no-*` 规则时加载 `arkts-helper`；粘贴编译错误时加载 `arkts-debug`。

## 目录结构

```
OHOS-Skills/
├── arkts-helper/
│   ├── SKILL.md
│   └── references/                       # 9 篇官方文档 + INDEX.md
└── arkts-debug/
    ├── SKILL.md
    ├── reference/                        # 22 篇错误根因 / 修复说明
    └── assets/                           # 22 个 BAD vs GOOD .ets 示例
```

## 文档来源

`arkts-helper/references/` 取自 OpenHarmony 上游文档仓库 <https://gitee.com/openharmony/docs>，路径 `zh-cn/application-dev/quick-start/`，与华为开发者官网「学习 ArkTS 语言」一节同源。

## 贡献

提交信息使用 [Conventional Commits](https://www.conventionalcommits.org/)（如 `feat: ...`、`fix: ...`、`docs: ...`）。新增 skill 时遵循现有结构：单一 `SKILL.md`（含 frontmatter）+ 离线参考目录，不要把内容散落到仓库根。

## License

本仓库使用**双许可**：

- 仓库整体（skill 元数据、`arkts-debug/`、`README.md`、`arkts-helper/SKILL.md` 等自行编写的内容）以 [MIT 许可](./LICENSE) 发布。
- `arkts-helper/references/` 下的 9 篇文档转载自 OpenHarmony 上游仓库 <https://gitee.com/openharmony/docs>，遵循 [CC-BY-4.0](./arkts-helper/references/LICENSE)；二次分发时必须保留署名（参见 [NOTICE](./arkts-helper/references/NOTICE.md)）。
