# OHOS-Skills

OpenHarmony / HarmonyOS 应用开发的 AI Agent Skill 集合，兼容所有支持 Skill 目录规范的 AI Agent 平台。每个 skill 是一个自包含目录，包含 `SKILL.md`（含 frontmatter 描述触发条件）以及配套的离线参考文档与代码示例，用于让 AI agent 在编写、审阅或修复 ArkTS / `.ets` 代码时基于权威资料工作，而不是凭 TypeScript 经验猜测。

## Skills

| Skill | 用途 |
|-------|------|
| [`arkts-helper`](./arkts-helper) | 写、改、审 ArkTS 代码时的语法 / 规范 / 强约束权威参考。内置 12 篇官方文档的离线副本，覆盖 ArkTS 语言介绍、编程规范、TS→ArkTS 适配背景/规则/案例、高性能编程实践、基础类库（XML/Buffer/JSON/容器类库）、并发编程（Promise/async-await/TaskPool/Worker/Sendable）、跨语言交互概览 |
| [`arkts-debug`](./arkts-debug) | 修复 HarmonyOS 编译报错。汇总 28 类常见错误（`ContentType`、`AppStorage.get`、`@StorageLink`、`getLastWindow`、`AvoidArea`、`TitleButtonRect`、`IDataSource`、`ESObject`、`Possibly null`、`arkts-no-props-by-index`、`arkts-no-decl-merging`、推断类型不可命名、空数组类型推断、模块解析、循环导入等），每类提供根因分析、规范修复方案与最小可复现 `.ets` 示例 |
| [`arkts-build`](./arkts-build) | 使用命令行工具构建、测试、签名、部署 HarmonyOS 应用。内置 8 篇官方「命令行工具」文档的离线副本，覆盖 `hvigorw`（构建任务与扩展参数）、`codelinter`（代码检查与 CI 门禁）、`hstack`（release 崩溃堆栈解析）、`ohpm`（三方依赖管理）、搭建流水线（环境配置→构建→签名→hdc 安装运行）、SDK 调试命令索引、模拟器 |
| [`arkts-ndk-dev`](./arkts-ndk-dev) | HarmonyOS NDK / Node-API / C++ 互操作开发指导。内置 11 篇官方「NDK 开发」文档的离线副本，重点覆盖 Node-API 跨语言交互（模块注册、接口映射、类型转换、生命周期管理、线程安全、异步任务、对象绑定、性能优化），同时覆盖 NDK 工程创建与构建、CMake 工具链配置、Rawfile / NativeBundle 接口、调试性能分析（ASan / LLDB）、硬件兼容性（ABI / CPU 特性 / Neon） |
| [`harmony-fetch`](./harmony-fetch) | 从华为开发者官网在线获取 HarmonyOS 开发文档。当本地离线 skill 文档不足以回答 ArkTS/ArkUI/ArkData/NDK/DevEco Studio 等 API 或特性问题时，通过华为官方公开 API 搜索并拉取最新文档内容，作为离线 skill 的在线补充 |

五个 skill 互补：日常编码用 `arkts-helper`；命中 hvigor / ArkCompiler 报错时用 `arkts-debug`（未匹配的报错回退到 `arkts-helper` 的迁移规则文档）；构建 / 测试 / 签名 / 部署 / CI 流水线时用 `arkts-build`；NDK / Node-API / C++ 互操作开发时用 `arkts-ndk-dev`；离线文档覆盖不到时用 `harmony-fetch` 在线拉取最新文档。

## 安装

将仓库克隆到任意位置，然后把需要的 skill 链接（或复制）到所用 Agent 平台的 skill 目录下即可。

大多数 Agent 平台支持两种 skill 作用域：

| 作用域 | 典型路径 | 说明 |
|-------|---------|------|
| 全局 | `~/.config/<agent-name>/skills/` | 对所有项目生效 |
| 项目级 | `<project-root>/<agent-dir>/skills/` | 仅对当前项目生效 |

其中 `<agent-name>` 和 `<agent-dir>` 因平台而异（如 `.qoder/skills/`、`.codeartsdoer/skills/`、`.trae/skills/` 等），请参阅所用 Agent 平台的文档确认具体路径。

以下示例中用 `<SKILLS_DIR>` 代表目标 skill 目录路径，请根据实际情况替换：

### Linux / macOS（bash）

```bash
git clone git@github.com:DunoDoge/OHOS-Skills.git
cd OHOS-Skills

# 将 <SKILLS_DIR> 替换为实际路径，例如 ~/.config/qoder/skills
ln -s "$PWD/arkts-helper"    <SKILLS_DIR>/arkts-helper
ln -s "$PWD/arkts-debug"     <SKILLS_DIR>/arkts-debug
ln -s "$PWD/arkts-build"     <SKILLS_DIR>/arkts-build
ln -s "$PWD/arkts-ndk-dev"   <SKILLS_DIR>/arkts-ndk-dev
ln -s "$PWD/harmony-fetch"   <SKILLS_DIR>/harmony-fetch
```

### Windows（PowerShell）

```powershell
git clone git@github.com:DunoDoge/OHOS-Skills.git
Set-Location OHOS-Skills

# 将 <SKILLS_DIR> 替换为实际路径，例如 Join-Path $HOME ".config\qoder\skills"
$skillsDir = "<SKILLS_DIR>"
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-helper")  -Target (Resolve-Path "./arkts-helper")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-debug")   -Target (Resolve-Path "./arkts-debug")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-build")   -Target (Resolve-Path "./arkts-build")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "arkts-ndk-dev") -Target (Resolve-Path "./arkts-ndk-dev")
New-Item -ItemType Junction -Force -Path (Join-Path $skillsDir "harmony-fetch") -Target (Resolve-Path "./harmony-fetch")
```

也可以放到项目级 skill 目录下仅对单个工程启用。

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
├── arkts-ndk-dev/
│   ├── SKILL.md
│   └── references/                       # 11 篇官方 NDK 开发文档 + INDEX.md
├── harmony-fetch/
│   ├── SKILL.md
│   ├── scripts/                          # fetch_doc.py 在线文档拉取脚本
│   └── doc-structure.md                  # 华为开发者文档目录结构参考
├── tests/                                # 测试用例与测试报告
└── README.md
```

## License

- 仓库整体（skill 元数据、`arkts-debug/`、`README.md`、`arkts-helper/SKILL.md`、`arkts-ndk-dev/SKILL.md`、`arkts-build/SKILL.md` 等自行编写的内容）以 [MIT 许可](./LICENSE) 发布。
- `arkts-helper` `arkts-build` `arkts-ndk-dev` 的`references/` 目录下的文档转载自华为开发者官网公开文档，遵循华为开发者网站使用条款；二次分发时必须保留上游 URL 署名（参见每份文档顶部的注释）。
