## ADDED Requirements

### Requirement: Skill 触发条件

`arkts-build` skill SHALL 在 Agent 面向 HarmonyOS / OpenHarmony 工程执行「构建、依赖管理、静态检查、崩溃堆栈解析、测试、签名、设备部署、CI 流水线」类任务时被激活。`SKILL.md` MUST 列出明确的触发关键词与场景清单，使 Agent 能稳定判断何时启用本 skill。

#### Scenario: 用户要求命令行构建工程
- **WHEN** 用户提出「用命令行构建 HarmonyOS 工程」「hvigorw 怎么打 hap」「assembleHap 参数怎么传」「构建 release 包」等构建类请求
- **THEN** Agent 启用 `arkts-build` skill，按工作流先读 `references/INDEX.md`，再加载 `04-hvigorw.md` 与 `06-building-app.md`，给出符合鸿蒙规范的 `hvigorw` 命令

#### Scenario: 用户要求代码静态检查
- **WHEN** 用户提出「跑 codelinter」「命令行做代码检查」「CI 里加静态检查」「codelinter 退出码怎么配」等检查类请求
- **THEN** Agent 启用本 skill，加载 `02-codelinter.md`，给出正确的 `codelinter` 命令与 `--exit-on` / `--config` / `--incremental` 参数

#### Scenario: 用户要求解析 release 崩溃堆栈
- **WHEN** 用户提出「解析 release 崩溃堆栈」「hstack 怎么用」「sourceMap/nameCache 怎么配」等堆栈解析类请求
- **THEN** Agent 启用本 skill，加载 `03-hstack.md`，给出 `hstack` 命令并说明 sourceMap / so / nameCache 归档目录的提供方式

#### Scenario: 用户要求管理三方依赖
- **WHEN** 用户提出「ohpm 装包」「ohpm 发包」「oh-package.json5 怎么写」「ohpm 仓库地址配置」等依赖管理类请求
- **THEN** Agent 启用本 skill，加载 `05-ohpm.md`，给出正确的 `ohpm install/publish/config` 命令与仓库地址

#### Scenario: 用户要求搭建 CI 流水线
- **WHEN** 用户提出「搭建 HarmonyOS CI 流水线」「无网络环境构建」「构建后怎么签名安装运行」等流水线类请求
- **THEN** Agent 启用本 skill，加载 `06-building-app.md`，按 JDK/Node/hdc/hvigor/ohpm 环境配置 → ohpm install → hvigorw 构建 → 签名 → hdc 安装运行的顺序给出步骤

### Requirement: 离线参考文档集

`arkts-build` skill MUST 提供 `references/` 目录，包含覆盖 HarmonyOS Command Line Tools 的离线参考文档。文档 MUST 按工具/场景拆分为独立文件，并配备 `INDEX.md` 索引文件。文档内容 MUST 来源于华为开发者官网公开文档的离线快照，每份文档 MUST 标注上游 URL 与抓取时间。

#### Scenario: 按需加载文档
- **WHEN** Agent 处理一个具体的构建/检查/解析任务
- **THEN** Agent 先读 `references/INDEX.md` 获取「任务类型 → 必读文件」映射，再按需加载对应的 1-2 份文档，而非一次性读取全部文档

#### Scenario: 文档覆盖范围
- **WHEN** 检查 `references/` 目录内容
- **THEN** 目录 MUST 至少包含以下文件：`INDEX.md`、`01-command-line-tools-overview.md`（工具获取与环境变量）、`02-codelinter.md`（代码检查）、`03-hstack.md`（堆栈解析）、`04-hvigorw.md`（命令行构建）、`05-ohpm.md`（三方依赖管理）、`06-building-app.md`（搭建流水线）、`07-debugging-commands.md`（SDK 调试命令索引）、`08-emulator.md`（模拟器）

### Requirement: INDEX 索引文件

`references/INDEX.md` MUST 作为 Agent 的必先阅读文件，提供「任务类型 → 必读文件」映射表、各文档角色说明、关键命令速记，使 Agent 能在不读全所有文档的前提下定位到正确的参考文档。

#### Scenario: Agent 首次进入 skill
- **WHEN** Agent 启用 `arkts-build` skill 处理任意任务
- **THEN** Agent MUST 先读 `references/INDEX.md`，再根据任务类型按映射表加载具体文档

#### Scenario: 索引内容完整性
- **WHEN** 阅读 `INDEX.md`
- **THEN** 文件 MUST 包含：各文档的角色一句话说明、按任务类型（构建/检查/堆栈解析/依赖管理/流水线/调试/模拟器）的查阅路径表、关键命令速记（clean/assembleHap/assembleApp/ohpm install/codelinter/hstack/hdc 安装运行/onDeviceTest）

### Requirement: SKILL.md 工作流

`SKILL.md` MUST 定义严格的工作流，使 Agent 在启用本 skill 时按固定步骤执行：先读 INDEX → 按场景加载文档 → 执行命令 → 引用来源。`SKILL.md` MUST 包含触发条件、与已有 skill 的边界、工作流步骤、高频命令速查表、高频红线清单、目录结构、文档来源与维护说明。

#### Scenario: 工作流执行
- **WHEN** Agent 启用本 skill 处理任务
- **THEN** Agent MUST 按以下步骤执行：(1) 读 `references/INDEX.md`；(2) 按任务类型加载对应文档；(3) 按文档内容给出命令；(4) 在回复中标注引用的 reference 文件

#### Scenario: 高频红线拦截
- **WHEN** Agent 给出 CI 构建命令
- **THEN** 命令 MUST 包含 `--no-daemon` 参数（CI 场景红线）；若使用 `-p module=` 参数，MUST 同时搭配 `--mode module`；构建前 MUST 先执行 `ohpm install` 安装依赖

### Requirement: 命令准确性

本 skill 给出的所有命令 MUST 是 HarmonyOS Command Line Tools 真实存在的命令与参数，不得用通用 npm/gradle/Node 命令替代。`hvigorw` 任务名、`-p` 扩展参数、`codelinter` 选项、`hstack` 选项、`ohpm` 子命令 MUST 与官方文档一致。对版本相关的命令（如 `buildInfo` 从 hvigorw 5.18.4 起、`onDeviceTest` 的 `ohos-debug-asan` 从 5.19.0 起），MUST 在文档中标注起始版本。

#### Scenario: hvigorw 构建命令
- **WHEN** 用户要求构建 HAP 包
- **THEN** Agent 给出形如 `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon` 的命令，使用鸿蒙真实的 `assembleHap` 任务名与 `-p product=` / `-p buildMode=` / `--mode module` 参数，而非 gradle 的 `assembleDebug`

#### Scenario: 版本相关命令标注
- **WHEN** 文档中出现版本相关的命令或参数
- **THEN** 文档 MUST 标注「从 hvigorw X.X.X 版本开始支持」或类似版本说明，使 Agent 能提示用户先 `hvigorw -v` 确认版本

### Requirement: 与已有 skill 的边界

`SKILL.md` MUST 明确本 skill 与 `arkts-helper`、`arkts-debug`、`arkts-ndk-dev` 的职责边界，使用交叉引用而非互斥策略。本 skill 负责「命令行怎么调」，不负责「代码怎么改」；当构建任务中遇到 ArkTS 编译报错、语法迁移、NDK/C++ 问题时，MUST 提示用户交叉引用对应 skill。

#### Scenario: 构建失败触发代码问题
- **WHEN** 用户在构建过程中遇到 ArkTS 编译报错（如 `arkts-no-*` 规则报错）
- **THEN** Agent 在本 skill 内给出命令行层建议后，MUST 提示用户使用 `arkts-debug` skill 处理代码层报错

#### Scenario: NDK 构建边界
- **WHEN** 用户要求构建包含 native C++ 模块的工程
- **THEN** 本 skill 只覆盖「hvigorw 怎么触发 native 构建 / syncNative / build-profile.json5 的 abiFilters」命令行层；CMake 工具链变量、.so 链接、musl/libc++ 等 C++ 层问题 MUST 交叉引用 `arkts-ndk-dev` skill

### Requirement: 调试命令索引化

`07-debugging-commands.md` MUST 以索引形式列出 SDK 命令行工具清单（hdc、aa、bm、打包拆包、扫描、cem、anm、edm、restool、param、power-shell、atm、network-cfg、hilog、hilogtool、hidumper、hitrace、hiperf、hiprofiler、uinput 等），每个工具给出一句话用途与官方链接，不逐个展开完整文档。构建/部署高频命令（`hdc file send` / `hdc shell bm install` / `hdc shell aa start`）MUST 在 `06-building-app.md` 中给出完整示例。

#### Scenario: 调试命令查询
- **WHEN** 用户询问某个 SDK 调试工具（如 hidumper / hitrace）的用法
- **THEN** Agent 从 `07-debugging-commands.md` 获取工具用途与官方链接，提示用户查阅官网详情，而非在本 skill 内展开该工具的完整文档

#### Scenario: 部署高频命令
- **WHEN** 用户要求将构建好的 HAP 安装到设备并运行
- **THEN** Agent 从 `06-building-app.md` 加载 `hdc file send` + `hdc shell bm install` + `hdc shell aa start` 的完整命令示例
