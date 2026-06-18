## Context

仓库 `OHOS-Skills` 已有三个鸿蒙开发 skill：

- `arkts-helper`：ArkTS 语法/迁移/编码规范（离线官方「学习ArkTS语言」9 篇）。
- `arkts-debug`：ArkTS 编译报错修复（22 类常见错误的 reference + assets）。
- `arkts-ndk-dev`：NDK / Node-API / C++ 互操作（42 篇官方 NDK 文档）。

三者都聚焦「写代码」侧，**「构建/测试/部署」侧是空白**。HarmonyOS 的命令行工具链（Command Line Tools，含 `codelinter`、`hstack`、`hvigorw`、`ohpm` 及 SDK 内 `hdc`/`aa`/`bm` 等）与社区 npm/gradle/Node 工具**不是同一套**：

- `hvigorw` 的任务名（`assembleHap`/`assembleApp`/`assembleHsp`/`assembleHar`/`onDeviceTest`）和参数（`-p product=`、`-p buildMode=`、`-p module=`、`--mode module`、`--no-daemon`）是鸿蒙专属，gradle 经验不适用。
- `ohpm` 虽类似 npm，但仓库地址（`https://ohpm.openharmony.cn/ohpm/`）、`oh-package.json5`、`strict_ssl` 等配置项不同。
- `codelinter` 的 `--exit-on` 退出码计算（二进制位组合）、`code-linter.json5` 规则文件、`--incremental` 增量检查是鸿蒙专属。
- `hstack` 解析 release 混淆堆栈需要 sourceMap + nameCache + so 归档目录，社区 sourcemap 工具无法处理鸿蒙的 `entry|har|1.0.0|src/...` 路径格式。
- 签名走 `hap-sign-tool.jar`（ECDSA + .p12/.cer/.p7b），不是 jarsigner / apksigner。

Agent 凭通用经验下笔会给出平台不存在的命令或错误参数。本设计新增 `arkts-build` skill，把官方「命令行工具」系列文档离线化 + 场景化索引，与已有三个 skill 形成「写代码 / 改报错 / 调 native / 构建部署」的完整闭环。

## Goals / Non-Goals

**Goals:**

- 提供 `arkts-build` skill，让 Agent 在构建/测试/部署类任务中按真实鸿蒙命令行规范下笔。
- 离线化官方命令行工具文档（codelinter / hstack / hvigorw / ohpm / 搭建流水线 / 调试命令 / emulator），按场景拆分文件，支持按需加载，避免一次性灌满上下文。
- 明确触发条件与场景化查阅路径（INDEX.md），降低 Agent 选错文档的概率。
- 明确与 `arkts-helper` / `arkts-debug` / `arkts-ndk-dev` 的边界，避免职责重叠。

**Non-Goals:**

- 不覆盖 ArkTS 语法/迁移/编码规范（→ `arkts-helper`）。
- 不覆盖 ArkTS 编译报错的根因与修复（→ `arkts-debug`）。
- 不覆盖 NDK / C++ / Node-API 互操作（→ `arkts-ndk-dev`）；本 skill 只负责「构建 native 模块时 hvigorw/CMake 怎么调」这一命令行层，C++ 代码本身归 ndk skill。
- 不替代 DevEco Studio GUI 操作指南；本 skill 只讲命令行。
- 不内置签名证书/Profile 申请流程的自动化脚本（只给命令与参数说明，证书申请走 AppGallery Connect）。
- 不做文档的自动同步/抓取工具；参考文档为离线快照，更新靠手动重新抓取覆盖。

## Decisions

### 决策 1：参考文档按「工具/场景」拆分为 8 份 + 1 份 INDEX，而非单一大文件

**选择**：`references/` 下按工具拆分（01-overview / 02-codelinter / 03-hstack / 04-hvigorw / 05-ohpm / 06-building-app / 07-debugging-commands / 08-emulator）+ `INDEX.md`。

**理由**：
- 与 `arkts-ndk-dev`（42 篇）、`arkts-helper`（9 篇）的拆分风格一致，便于 `Grep`/`Read` offset/limit 定位。
- 单文件会超过 100KB，Agent 一次性读全会撑爆上下文；按工具拆分后，构建任务只读 04+06，检查任务只读 02，崩溃解析只读 03。
- `INDEX.md` 给出「任务类型 → 必读文件」映射表，Agent 先读 INDEX 再按需加载，与已有 skill 工作流一致。

**备选**：单文件 `references.md`。**否决**：上下文成本太高，且无法按需加载。

### 决策 2：SKILL.md 内置「命令速查表」+「高频红线」，而非只给文档链接

**选择**：`SKILL.md` 中包含：
- 触发关键词清单（hvigorw / codelinter / hstack / ohpm / assembleHap / 流水线 / CI / 签名 / hdc 安装 / onDeviceTest 等）。
- 与已有 skill 的边界说明。
- 工作流（先读 INDEX → 按场景加载文档 → 执行命令 → 引用来源）。
- 高频命令速查表（clean / assembleHap / assembleApp / ohpm install / codelinter / hstack / hdc 安装运行 / onDeviceTest）。
- 高频红线（CI 必加 `--no-daemon`、`-p module=` 必须配 `--mode module`、签名前必须 ohpm install、release 堆栈必须 sourceMap+nameCache、产物路径规律等）。

**理由**：
- 与 `arkts-debug`（Quick Reference 表）、`arkts-ndk-dev`（红线清单）风格一致。
- 80% 的构建任务只需速查表 + 红线即可回答，无需打开 reference；复杂场景再查文档。
- 红线能直接拦截「CI 漏 --no-daemon」「module 参数漏 --mode module」「hstack 漏 nameCache」等高频错误。

**备选**：SKILL.md 只放触发条件 + 文档链接。**否决**：Agent 每次都要读 reference 才能下笔，效率低且易漏红线。

### 决策 3：参考文档来源为华为开发者官网公开文档的离线快照

**选择**：`references/` 内容抓取自 `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/` 下「命令行工具」系列（codelinter / hstack / hvigorw / ohpm / 搭建流水线 / 调试命令 / 模拟器 / 获取 Command Line Tools），清洗为 Markdown 后离线存放。每份文档顶部标注上游 URL 与更新时间。

**理由**：
- 与 `arkts-ndk-dev`（来源 gitee openharmony docs）、`arkts-helper`（同源）策略一致。
- 离线化保证 Agent 在无网环境下也能检索；华为官网文档是鸿蒙命令行工具的权威来源。
- 标注上游 URL 便于后续手动更新。

**备选**：实时 WebFetch 官网。**否决**：每次任务都要联网抓取，慢且不可靠；文档结构不稳定，难以按需定位段落。

### 决策 4：调试命令（hdc/aa/bm/hilog 等）只做索引文档，不逐个展开

**选择**：`07-debugging-commands.md` 只列出 SDK 命令行工具清单 + 每个工具的一句话用途 + 官方链接，不把 hdc/aa/bm/hilog/hidumper/hitrace/hiperf 等每个工具的完整文档都搬进来。

**理由**：
- 调试命令工具多达 20+ 个，逐个展开会让 references 体积失控。
- 构建/部署类任务高频只用到 `hdc file send` / `hdc shell bm install` / `hdc shell aa start` 这几个，已在 `06-building-app.md` 的「运行应用」一节给出完整命令；其余调试命令按需 WebFetch 或提示用户查官网即可。
- 与 `arkts-ndk-dev` 中 `37-debug-performance-profiling-overview.md` 只做概览索引的策略一致。

**备选**：把 hdc/aa/bm/hilog 等每个工具都展开成独立 md。**否决**：体积与维护成本过高，且超出「构建/测试/部署」主线。

### 决策 5：与已有 skill 的边界用「交叉引用」而非「互斥」

**选择**：`SKILL.md` 明确「构建任务中遇到 ArkTS 编译报错 → 交叉引用 `arkts-debug`；遇到语法/迁移问题 → 交叉引用 `arkts-helper`；遇到 NDK/C++ → 交叉引用 `arkts-ndk-dev`」。本 skill 负责「命令行怎么调」，不负责「代码怎么改」。

**理由**：
- 构建失败经常是代码问题，强行互斥会让 Agent 来回切换 skill；交叉引用让 Agent 在本 skill 内给出命令行层建议后，提示用户用对应 skill 处理代码层问题。
- 与 `arkts-debug` 中「非报错类任务 prefer arkts-helper」的交叉引用风格一致。

## Risks / Trade-offs

- **[文档时效性]** 官网文档会随 HarmonyOS 版本更新（如 hvigorw 6.x 新增 `--analyze=ultrafine`、`-p buildVersion=`），离线快照可能滞后。
  → **缓解**：每份文档顶部标注上游 URL 与抓取时间；`SKILL.md` 的「文档来源与维护」一节说明更新方式（重新抓取覆盖）；INDEX.md 提示「命令版本差异以官网为准」。
- **[命令版本差异]** hvigorw 不同版本命令支持范围不同（如 `buildInfo` 从 5.18.4 起、`onDeviceTest` 的 `ohos-debug-asan` 从 5.19.0 起），Agent 可能给出用户环境不支持的命令。
  → **缓解**：`04-hvigorw.md` 中对版本相关的命令标注「从 hvigorw X.X.X 版本开始支持」；`SKILL.md` 红线提示「不确定版本时先 `hvigorw -v`」。
- **[平台差异]** Windows/macOS/Linux 的环境变量配置方式不同（PATH 分隔符、Node 路径差异），Agent 可能给错平台命令。
  → **缓解**：`01-command-line-tools-overview.md` 与 `06-building-app.md` 分平台给出配置示例；`SKILL.md` 提示「先确认用户 OS 再给环境变量命令」。
- **[与 arkts-ndk-dev 重叠]** NDK 构建既涉及 hvigorw/CMake 命令行（本 skill），又涉及 C++ 工具链/ABI（ndk skill）。
  → **缓解**：本 skill 只覆盖「hvigorw 怎么触发 native 构建 / syncNative / build-profile.json5 的 abiFilters」命令行层；CMake 工具链变量、.so 链接、musl/libc++ 等归 `arkts-ndk-dev`。SKILL.md 边界说明中明确这一点。
- **[签名流程复杂]** 签名涉及 keytool 生成 .p12/.csr、AppGallery Connect 申请 .cer/.p7b、hap-sign-tool.jar 签名三步，Agent 可能漏步。
  → **缓解**：`06-building-app.md` 完整保留官方签名流程（含 keytool 命令、hap-sign-tool.jar 参数表）；`SKILL.md` 速查表标注「签名三件套：.p12 / .cer / .p7b」。
