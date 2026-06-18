## Why

当前仓库已有 `arkts-helper`（ArkTS 语法/迁移）、`arkts-debug`（ArkTS 编译报错修复）、`arkts-ndk-dev`（NDK/C++ 互操作）三个 skill，但**缺少覆盖「工程构建、依赖管理、代码静态检查、堆栈解析、测试、签名与部署」这一整条命令行工具链的 skill**。

Agent 在被要求「用命令行构建 HarmonyOS 工程」「跑 codelinter」「解析 release 崩溃堆栈」「配置 CI 流水线」「ohpm 装包/发包」「hvigorw 构建参数怎么传」时，只能凭 DevEco Studio GUI 经验或通用 Node/npm 知识猜测，极易给出**平台不存在的命令、错误的参数顺序、或漏掉 `--no-daemon`/`-p product=`/`-p buildMode=` 这类鸿蒙构建必填项**。HarmonyOS 的命令行工具（Command Line Tools，含 `codelinter`、`hstack`、`hvigorw`、`ohpm` 及 SDK 内 `hdc`/`aa`/`bm` 等）与社区 npm/gradle 工具**不是同一套**，参数语义和产物路径都有差异，需要一份离线、权威、按场景索引的参考集。

本 change 新增 `arkts-build` skill，把华为官方「命令行工具」系列文档（codelinter / hstack / hvigorw / ohpm / 搭建流水线 / 调试命令 / 模拟器）整理成离线参考文档 + 场景化工作流，让 Agent 在构建/测试/部署类任务中按真实规范下笔。

## What Changes

- 新增 skill 目录 `arkts-build/`，包含 `SKILL.md`（触发条件、工作流、命令速查、目录结构）。
- 新增 `arkts-build/references/` 离线参考文档集，覆盖以下官方文档（按场景拆分，便于按需加载）：
  - `01-command-line-tools-overview.md`：Command Line Tools 获取、环境变量配置（Windows/macOS/Linux）、工具总览。
  - `02-codelinter.md`：代码检查工具 `codelinter` 命令行参数、规则配置、增量检查、QuickFix、退出码、输出格式。
  - `03-hstack.md`：release 崩溃堆栈解析工具 `hstack` 参数、sourceMap/so/nameCache 归档、解析原理与示例。
  - `04-hvigorw.md`：命令行构建工具 `hvigorw` 任务（clean/assembleHap/assembleApp/assembleHsp/assembleHar/onDeviceTest/test）、扩展参数（`-p buildMode`/`-p product`/`-p module`/`-p coverage`）、daemon、日志、可视化、性能开关。
  - `05-ohpm.md`：三方依赖管理工具 `ohpm` 常用命令（install/init/publish/uninstall/update/list/info/config/version/cache clean 等）、oh-package.json5、仓库配置。
  - `06-building-app.md`：搭建流水线完整流程（JDK/Node/hdc/hvigor/ohpm 环境配置、ohpm install、hvigorw 构建、签名、hdc 安装运行、示例脚本、无网络流水线）。
  - `07-debugging-commands.md`：SDK 命令行工具总览与调试命令索引（hdc、aa、bm、打包拆包、扫描、cem、anm、edm、restool、param、power-shell、atm、network-cfg、hilog、hilogtool、hidumper、hitrace、hiperf、hiprofiler、uinput 等）。
  - `08-emulator.md`：模拟器工具（Emulator）命令行使用。
  - `INDEX.md`：必先阅读的索引，给出每份文档角色、按场景的查阅路径、关键命令速记。
- `SKILL.md` 中明确**触发关键词**（hvigorw、codelinter、hstack、ohpm、assembleHap、流水线、CI、签名、hdc 安装、onDeviceTest 等）与**与已有 skill 的边界**（编译报错归 `arkts-debug`，语法归 `arkts-helper`，NDK 归 `arkts-ndk-dev`）。

## Capabilities

### New Capabilities
- `arkts-build`: 指导 Agent 使用 HarmonyOS Command Line Tools（codelinter / hstack / hvigorw / ohpm / SDK 调试命令 / emulator）完成工程构建、依赖管理、静态检查、崩溃堆栈解析、测试、签名与设备部署的 skill，含离线官方文档参考集与场景化工作流。

### Modified Capabilities
<!-- 无已有 spec 需要修改 -->

## Impact

- **新增代码/文件**：`arkts-build/SKILL.md` + `arkts-build/references/*.md`（约 9 份文档 + INDEX）。
- **无破坏性变更**：纯新增 skill，不影响现有 `arkts-helper` / `arkts-debug` / `arkts-ndk-dev`。
- **依赖**：无运行时依赖；参考文档内容来自华为开发者官网公开文档（https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ 下「命令行工具」系列），离线化后供 Agent 检索。
- **边界**：本 skill 不负责 ArkTS 语法/迁移（→ `arkts-helper`）、ArkTS 编译报错修复（→ `arkts-debug`）、NDK/C++ 互操作（→ `arkts-ndk-dev`）；当构建任务中遇到这三类问题时，应交叉引用对应 skill。
