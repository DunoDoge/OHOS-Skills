# OHOS-Skills

OpenHarmony / HarmonyOS 应用开发的 [opencode](https://opencode.ai) skill 集合。每个 skill 是一个自包含目录，包含 `SKILL.md`（含 frontmatter 描述触发条件）以及配套的离线参考文档与代码示例，用于让 AI agent 在编写、审阅或修复 ArkTS / `.ets` 代码时基于权威资料工作，而不是凭 TypeScript 经验猜测。

## Skills

| Skill | 用途 |
|-------|------|
| [`arkts-helper`](./arkts-helper) | 写、改、审 ArkTS 代码时的语法 / 规范 / 强约束权威参考。内置 12 篇官方文档的离线副本，覆盖 ArkTS 语言介绍、编程规范、TS→ArkTS 适配背景/规则/案例、高性能编程实践、基础类库（XML/Buffer/JSON/容器类库）、并发编程（Promise/async-await/TaskPool/Worker/Sendable）、跨语言交互概览 |
| [`arkts-debug`](./arkts-debug) | 修复 HarmonyOS 编译报错。汇总 28 类常见错误（`ContentType`、`AppStorage.get`、`@StorageLink`、`getLastWindow`、`AvoidArea`、`TitleButtonRect`、`IDataSource`、`ESObject`、`Possibly null`、`arkts-no-props-by-index`、`arkts-no-decl-merging`、推断类型不可命名、空数组类型推断、模块解析、循环导入等），每类提供根因分析、规范修复方案与最小可复现 `.ets` 示例 |
| [`arkts-build`](./arkts-build) | 使用命令行工具构建、测试、签名、部署 HarmonyOS 应用。内置 8 篇官方「命令行工具」文档的离线副本，覆盖 `hvigorw`（构建任务与扩展参数）、`codelinter`（代码检查与 CI 门禁）、`hstack`（release 崩溃堆栈解析）、`ohpm`（三方依赖管理）、搭建流水线（环境配置→构建→签名→hdc 安装运行）、SDK 调试命令索引、模拟器 |
| [`arkts-ndk-dev`](./arkts-ndk-dev) | HarmonyOS NDK / Node-API / C++ 互操作开发指导。内置 11 篇官方「NDK 开发」文档的离线副本，重点覆盖 Node-API 跨语言交互（模块注册、接口映射、类型转换、生命周期管理、线程安全、异步任务、对象绑定、性能优化），同时覆盖 NDK 工程创建与构建、CMake 工具链配置、Rawfile / NativeBundle 接口、调试性能分析（ASan / LLDB）、硬件兼容性（ABI / CPU 特性 / Neon） |

四个 skill 互补：日常编码用 `arkts-helper`；命中 hvigor / ArkCompiler 报错时用 `arkts-debug`（未匹配的报错回退到 `arkts-helper` 的迁移规则文档）；构建 / 测试 / 签名 / 部署 / CI 流水线时用 `arkts-build`；NDK / Node-API / C++ 互操作开发时用 `arkts-ndk-dev`。

## 安装

将仓库克隆到任意位置，然后把需要的 skill 链接到 opencode 的 skill 目录：

### Linux / macOS（bash）

```bash
git clone git@github.com:DunoDoge/OHOS-Skills.git
cd OHOS-Skills

# 链接到全局 skill 目录（推荐：源仓库的更新会自动同步）
ln -s "$PWD/arkts-helper"  ~/.config/opencode/skills/arkts-helper
ln -s "$PWD/arkts-debug"   ~/.config/opencode/skills/arkts-debug
ln -s "$PWD/arkts-build"   ~/.config/opencode/skills/arkts-build
ln -s "$PWD/arkts-ndk-dev" ~/.config/opencode/skills/arkts-ndk-dev
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
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-build")   -Target (Resolve-Path "./arkts-build")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-ndk-dev") -Target (Resolve-Path "./arkts-ndk-dev")
```

也可以放到项目级 `.opencode/skills/` 下仅对单个工程启用。

链接完成后，在 opencode 内 skill 会按各自 `SKILL.md` 的 frontmatter `description` 自动触发：写 `.ets` / 提到 ArkUI、HarmonyOS NEXT、`arkts-no-*` 规则时加载 `arkts-helper`；粘贴编译错误 / `arkts-no-props-by-index` / `arkts-no-decl-merging` / `Cannot find module` / `Maximum call stack` / 推断类型不可命名时加载 `arkts-debug`；构建 / 测试 / 签名 / 部署 / CI 流水线 / 提到 `hvigorw` / `ohpm` / `codelinter` / `hstack` 时加载 `arkts-build`；NDK 开发 / Node-API / `napi_*` / C++ 互操作 / CMake 工具链 / 提到 `napi_wrap` / `napi_threadsafe_function` / `libace_napi.z.so` 时加载 `arkts-ndk-dev`。

## 目录结构

```
OHOS-Skills/
├── arkts-helper/
│   ├── SKILL.md
│   └── references/                       # 12 篇官方文档 + INDEX.md
├── arkts-debug/
│   ├── SKILL.md
│   ├── references/                        # 28 篇错误根因 / 修复说明
│   └── assets/                           # 28 个 BAD vs GOOD .ets 示例
├── arkts-build/
│   ├── SKILL.md
│   └── references/                       # 8 篇官方命令行工具文档 + INDEX.md
└── arkts-ndk-dev/
    ├── SKILL.md
    └── references/                       # 11 篇官方 NDK 开发文档 + INDEX.md
```

## 文档来源

`arkts-helper/references/` 取自华为开发者官网「学习 ArkTS 语言」和「ArkTS（方舟编程语言）」系列文档（<https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/> 下 `introduction-to-arkts`、`arkts-coding-style-guide`、`arkts-migration-background`、`typescript-to-arkts-migration-guide`、`arkts-more-cases`、`arkts-high-performance-programming`、`arkts-utils-overview`、`xml-generation-parsing-conversion`、`buffer`、`arkts-json`、`containers`、`async-concurrency-overview`、`multithread-concurrency`、`interthread-communication`、`arkts-cross-language-interaction`），为 2026-06-18 抓取的离线快照。

`arkts-build/references/` 取自华为开发者官网「命令行工具」系列文档（<https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/> 下 `ide-commandline-get`、`ide-command-line-codelinter`、`ide-command-line-hstack`、`ide-hvigor-commandline`、`ide-ohpm-cli`、`ide-command-line-building-app`、`debugging-commands`、`ide-commandline-emulator`），为 2026-06-17 抓取的离线快照。

`arkts-ndk-dev/references/` 取自华为开发者官网「NDK 开发」系列文档（<https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/> 下 `ndk-development-overview`、`create-with-ndk`、`build-with-ndk`、`coding`、`rawfile-guidelines`、`native-bundle-guidelines`、`build-toolchain`、`debugging-profiling`、`hardware-compatibility`），为 2026-06-18 抓取的离线快照。

## 贡献

提交信息使用 [Conventional Commits](https://www.conventionalcommits.org/)（如 `feat: ...`、`fix: ...`、`docs: ...`）。新增 skill 时遵循现有结构：单一 `SKILL.md`（含 frontmatter）+ 离线参考目录，不要把内容散落到仓库根。

## License

本仓库使用**双许可**：

- 仓库整体（skill 元数据、`arkts-debug/`、`README.md`、`arkts-helper/SKILL.md`、`arkts-ndk-dev/SKILL.md`、`arkts-build/SKILL.md` 等自行编写的内容）以 [MIT 许可](./LICENSE) 发布。
- `arkts-helper/references/` 下的文档转载自华为开发者官网公开文档，遵循华为开发者网站使用条款；二次分发时必须保留上游 URL 署名（参见每份文档顶部的注释）。
- `arkts-build/references/` 下的文档转载自华为开发者官网公开文档，遵循华为开发者网站使用条款；二次分发时必须保留上游 URL 署名（参见每份文档顶部的注释）。
- `arkts-ndk-dev/references/` 下的文档转载自华为开发者官网公开文档，遵循华为开发者网站使用条款；二次分发时必须保留上游 URL 署名（参见每份文档顶部的注释）。
