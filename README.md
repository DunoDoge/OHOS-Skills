# OHOS-Skills

OpenHarmony / HarmonyOS 应用开发的 [opencode](https://opencode.ai) skill 集合。每个 skill 是一个自包含目录，包含 `SKILL.md`（含 frontmatter 描述触发条件）以及配套的离线参考文档与代码示例，用于让 AI agent 在编写、审阅或修复 ArkTS / `.ets` 代码时基于权威资料工作，而不是凭 TypeScript 经验猜测。

## Skills

| Skill | 用途 |
|-------|------|
| [`arkts-helper`](./arkts-helper) | 写、改、审 ArkTS 代码时的语法 / 规范 / 强约束权威参考。内置 9 篇官方「学习 ArkTS 语言」文档的离线副本，覆盖语法手册、编码规范、TS→ArkTS 迁移规则（`arkts-no-*`）、高性能编程等 |
| [`arkts-debug`](./arkts-debug) | 修复 HarmonyOS 编译报错。汇总 22 类常见错误（`ContentType`、`AppStorage.get`、`@StorageLink`、`getLastWindow`、`AvoidArea`、`TitleButtonRect`、`IDataSource`、`ESObject`、`Possibly null` 等），每类提供根因分析、规范修复方案与最小可复现 `.ets` 示例 |
| [`arkts-ndk-dev`](./arkts-ndk-dev) | 写、改、审 HarmonyOS NDK（native C/C++）代码时的权威参考。内置 42 篇官方 `application-dev/napi/` 文档的离线副本，覆盖 NDK 工程创建与 CMake 构建、Node-API / JSVM-API 规范与典型场景（异步任务、线程安全、对象包装、Sendable）、ABI / Neon / ASan / fdsan 等 |
| [`arkts-build`](./arkts-build) | 使用命令行工具构建、测试、签名、部署 HarmonyOS 应用。内置 8 篇官方「命令行工具」文档的离线副本，覆盖 `hvigorw`（构建任务与扩展参数）、`codelinter`（代码检查与 CI 门禁）、`hstack`（release 崩溃堆栈解析）、`ohpm`（三方依赖管理）、搭建流水线（环境配置→构建→签名→hdc 安装运行）、SDK 调试命令索引、模拟器 |

四个 skill 互补：日常编码用 `arkts-helper`；命中 hvigor / ArkCompiler 报错时用 `arkts-debug`（未匹配的报错回退到 `arkts-helper` 的迁移规则文档）；写 `napi_*` / native 模块时用 `arkts-ndk-dev`；构建 / 测试 / 签名 / 部署 / CI 流水线时用 `arkts-build`。

## 安装

将仓库克隆到任意位置，然后把需要的 skill 链接到 opencode 的 skill 目录：

### Linux / macOS（bash）

```bash
git clone git@github.com:DunoDoge/OHOS-Skills.git
cd OHOS-Skills

# 链接到全局 skill 目录（推荐：源仓库的更新会自动同步）
ln -s "$PWD/arkts-helper"  ~/.config/opencode/skills/arkts-helper
ln -s "$PWD/arkts-debug"   ~/.config/opencode/skills/arkts-debug
ln -s "$PWD/arkts-ndk-dev" ~/.config/opencode/skills/arkts-ndk-dev
ln -s "$PWD/arkts-build"   ~/.config/opencode/skills/arkts-build
```

### Windows（PowerShell）

```powershell
git clone git@github.com:DunoDoge/OHOS-Skills.git
Set-Location OHOS-Skills

# 创建全局 skill 目录（如已存在则跳过）
$skillsDir = Join-Path $HOME ".config/opencode/skills"
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

# 链接到全局 skill 目录（推荐：源仓库的更新会自动同步）
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-helper")  -Target (Resolve-Path "./arkts-helper")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-debug")   -Target (Resolve-Path "./arkts-debug")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-ndk-dev") -Target (Resolve-Path "./arkts-ndk-dev")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-build")   -Target (Resolve-Path "./arkts-build")
```

也可以放到项目级 `.opencode/skills/` 下仅对单个工程启用。

链接完成后，在 opencode 内 skill 会按各自 `SKILL.md` 的 frontmatter `description` 自动触发：写 `.ets` / 提到 ArkUI、HarmonyOS NEXT、`arkts-no-*` 规则时加载 `arkts-helper`；粘贴编译错误时加载 `arkts-debug`；写 `napi_*` / 配置 CMake / 提到 OpenHarmony NDK 时加载 `arkts-ndk-dev`；构建 / 测试 / 签名 / 部署 / CI 流水线 / 提到 `hvigorw` / `ohpm` / `codelinter` / `hstack` 时加载 `arkts-build`。

## 目录结构

```
OHOS-Skills/
├── arkts-helper/
│   ├── SKILL.md
│   └── references/                       # 9 篇官方文档 + INDEX.md
├── arkts-debug/
│   ├── SKILL.md
│   ├── reference/                        # 22 篇错误根因 / 修复说明
│   └── assets/                           # 22 个 BAD vs GOOD .ets 示例
├── arkts-ndk-dev/
│   ├── SKILL.md
│   └── references/                       # 42 篇官方 NDK 文档 + INDEX.md
└── arkts-build/
    ├── SKILL.md
    └── references/                       # 8 篇官方命令行工具文档 + INDEX.md
```

## 文档来源

`arkts-helper/references/` 取自 OpenHarmony 上游文档仓库 <https://gitee.com/openharmony/docs>，路径 `zh-cn/application-dev/quick-start/`，与华为开发者官网「学习 ArkTS 语言」一节同源。

`arkts-ndk-dev/references/` 同样取自 <https://gitee.com/openharmony/docs>，路径 `zh-cn/application-dev/napi/`，与华为开发者官网「应用开发 › NDK」一节同源。

`arkts-build/references/` 取自华为开发者官网「命令行工具」系列文档（<https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/> 下 `ide-commandline-get`、`ide-command-line-codelinter`、`ide-command-line-hstack`、`ide-hvigor-commandline`、`ide-ohpm-cli`、`ide-command-line-building-app`、`debugging-commands`、`ide-commandline-emulator`），为 2026-06-17 抓取的离线快照。

## 贡献

提交信息使用 [Conventional Commits](https://www.conventionalcommits.org/)（如 `feat: ...`、`fix: ...`、`docs: ...`）。新增 skill 时遵循现有结构：单一 `SKILL.md`（含 frontmatter）+ 离线参考目录，不要把内容散落到仓库根。

## License

本仓库使用**双许可**：

- 仓库整体（skill 元数据、`arkts-debug/`、`README.md`、`arkts-helper/SKILL.md`、`arkts-ndk-dev/SKILL.md`、`arkts-build/SKILL.md` 等自行编写的内容）以 [MIT 许可](./LICENSE) 发布。
- `arkts-helper/references/` 与 `arkts-ndk-dev/references/` 下的文档转载自 OpenHarmony 上游仓库 <https://gitee.com/openharmony/docs>，遵循 [CC-BY-4.0](./arkts-helper/references/LICENSE)；二次分发时必须保留署名（参见各自目录下的 `NOTICE.md`）。
- `arkts-build/references/` 下的文档转载自华为开发者官网公开文档，遵循华为开发者网站使用条款；二次分发时必须保留上游 URL 署名（参见每份文档顶部的注释）。
