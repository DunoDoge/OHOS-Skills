---
name: arkts-build
description: Use when building, testing, signing, or deploying HarmonyOS / OpenHarmony apps via command line tools, or when configuring CI pipelines. Triggers include hvigorw, codelinter, hstack, ohpm, assembleHap, assembleApp, assembleHsp, assembleHar, onDeviceTest, buildMode, product, module target, --no-daemon, --mode module, hap-sign-tool, keytool, hdc file send, hdc shell bm install, hdc shell aa start, ohpm install, ohpm publish, ohpm config, code-linter.json5, sourceMap, nameCache, crash stack parsing, CI 流水线, 签名, 流水线搭建, or any topic under the HarmonyOS Command Line Tools documentation. Loads the offline command-line tools reference set so the agent can give real HarmonyOS commands instead of guessing from npm/gradle knowledge.
---

# arkts-build

HarmonyOS 的命令行工具链（Command Line Tools，含 `codelinter`、`hstack`、`hvigorw`、`ohpm` 及 SDK 内 `hdc`/`aa`/`bm` 等）与社区 npm/gradle/Node 工具**不是同一套**：

- `hvigorw` 的任务名（`assembleHap`/`assembleApp`/`assembleHsp`/`assembleHar`/`onDeviceTest`）和参数（`-p product=`、`-p buildMode=`、`-p module=`、`--mode module`、`--no-daemon`）是鸿蒙专属，gradle 经验不适用。
- `ohpm` 虽类似 npm，但仓库地址（`https://ohpm.openharmony.cn/ohpm/`）、`oh-package.json5`、`strict_ssl` 等配置项不同。
- `codelinter` 的 `--exit-on` 退出码计算（二进制位组合）、`code-linter.json5` 规则文件、`--incremental` 增量检查是鸿蒙专属。
- `hstack` 解析 release 混淆堆栈需要 sourceMap + nameCache + so 归档目录，社区 sourcemap 工具无法处理鸿蒙的 `entry|har|1.0.0|src/...` 路径格式。
- 签名走 `hap-sign-tool.jar`（ECDSA + .p12/.cer/.p7b），不是 jarsigner / apksigner。

本 skill 提供的离线参考文档（`references/` 下 8 篇 + INDEX）是华为官方「命令行工具」系列文档的离线副本，是处理构建/测试/部署类任务时的**权威依据**。

## 何时启用本 skill

满足以下任一条件就应当遵循本 skill 的工作流程：

- 用户要求**命令行构建** HarmonyOS 工程（`hvigorw`、`assembleHap`、`assembleApp`、`assembleHsp`、`assembleHar`、`clean`、构建 release/debug 包）
- 用户要求**代码静态检查**（`codelinter`、CI 门禁、`--exit-on`、`code-linter.json5`、增量检查）
- 用户要求**解析 release 崩溃堆栈**（`hstack`、sourceMap、nameCache、so 归档、混淆还原）
- 用户要求**管理三方依赖**（`ohpm install`、`ohpm publish`、`ohpm config`、`oh-package.json5`、仓库地址配置）
- 用户要求**搭建 CI 流水线**（环境配置、构建、签名、安装运行、无网络流水线）
- 用户要求**测试**（`onDeviceTest`、`hvigorw test`、覆盖率、ASan）
- 用户要求**签名/部署**（`hap-sign-tool.jar`、`keytool`、.p12/.cer/.p7b、`hdc file send`、`hdc shell bm install`、`hdc shell aa start`）
- 用户要求使用**模拟器**命令行（Emulator、`hdc tconn`、gRPC 远程服务）
- 用户提到 `--no-daemon`、`-p product=`、`-p buildMode=`、`-p module=`、`--mode module`、`-p coverage=` 等 hvigorw 参数
- 项目根存在 `oh-package.json5` / `build-profile.json5` / `hvigorw` / `hvigorfile.ts` 等鸿蒙工程标志，且任务是构建/测试/部署而非写代码

不要在「纯 ArkTS 语法/迁移」「ArkTS 编译报错修复」「NDK/C++ 互操作」场景下强行套用本 skill；这些场景请使用对应 skill（见下文边界）。

## 与已有 skill 的边界

本 skill 负责**「命令行怎么调」**，不负责**「代码怎么改」**。当构建任务中遇到以下问题时，应交叉引用对应 skill：

| 问题类型 | 交叉引用 skill | 边界说明 |
| --- | --- | --- |
| ArkTS 语法/迁移/编码规范 | `arkts-helper` | 本 skill 只讲构建命令，不讲 ArkTS 语法 |
| ArkTS 编译报错（`arkts-no-*` 规则等） | `arkts-debug` | 构建失败若是代码报错，用 `arkts-debug` 修复代码，再回到本 skill 重新构建 |
| NDK / C++ / Node-API 互操作 | `arkts-ndk-dev` | 本 skill 只覆盖「hvigorw 怎么触发 native 构建 / syncNative / build-profile.json5 的 abiFilters」命令行层；CMake 工具链变量、.so 链接、musl/libc++ 等 C++ 层问题归 `arkts-ndk-dev` |

## 工作流程（严格遵守）

### 1. 先读索引，再决定看哪份文档

任何构建/测试/部署任务开始前，**必须先读** `references/INDEX.md`。它给出 8 份文档的角色、按任务类型的查阅路径以及关键命令速记，能避免你把整个 reference 目录全文读进上下文。

### 2. 按任务类型加载对应文档

| 任务类型 | 必读文件（在 `references/` 下） |
| -------- | ------------------------------ |
| 工具获取 / 环境变量配置 | `01-command-line-tools-overview.md` |
| 代码静态检查 / CI 门禁 | `02-codelinter.md` |
| release 崩溃堆栈解析 | `03-hstack.md` |
| **hvigorw 构建命令 / 构建参数** | `04-hvigorw.md` |
| ohpm 装包 / 发包 / 依赖管理 | `05-ohpm.md` |
| **搭建 CI 流水线 / 构建后签名安装运行** | `06-building-app.md`（+ `04-hvigorw.md`） |
| 设备调试命令（hdc/aa/bm 等） | `07-debugging-commands.md`（+ `06-building-app.md` 的「运行应用」一节） |
| 模拟器使用 | `08-emulator.md` |
| 测试（onDeviceTest / Local Test） | `04-hvigorw.md` 的「测试命令」一节 |

读取文档时优先用 `Grep`/`Read` 的 offset/limit 定位段落，不要把大文件一次性读全。

### 3. 落到命令时严格执行红线

写出 / 修改构建命令前自检以下高频红线（详细规则以文档原文为准）：

- **CI 构建必加 `--no-daemon`**：命令行模式（尤其 CI）推荐关闭守护进程，避免状态残留
- **`-p module=` 必须搭配 `--mode module`**：`-p module={ModuleName}@{TargetName}` 参数需要与 `--mode module` 参数搭配使用，否则无效
- **构建前必须先 `ohpm install`**：需要分别进入工程及各个模块下执行 `ohpm install`，安装工程及各个模块依赖的三方库
- **release 堆栈解析必须提供 sourceMap + nameCache**：`hstack` 的 `-s`（sourceMap）与 `--so`（shared object）至少提供一项；方法名还原需要同时提供 sourceMap 与 nameCache
- **签名三件套：.p12 / .cer / .p7b**：签名需要密钥（.p12）、数字证书（.cer）、Profile（.p7b）三个文件；HAP 推送到设备必须是携带签名信息的
- **产物路径规律**：Hap 产物在 `${PROJECT_PATH}/{moduleName}/build/{productName}/outputs/{targetName}/xxx.hap`；App 产物在 `${PROJECT_PATH}/build/outputs/{productName}/xxx.app`
- **版本相关命令先 `hvigorw -v`**：`buildInfo`（5.18.4+）、`ohos-debug-asan`（5.19.0+）、`--optimization-strategy`（5.19.2+）、`--analyze=ultrafine`（6.0.0+）、`-p buildVersion=`（6.23.3+）等命令有版本要求
- **平台差异先确认 OS**：Windows/macOS/Linux 的环境变量配置方式不同（PATH 分隔符、Node 路径差异：Windows 在 `tool/node`，Linux/macOS 在 `tool/node/bin`），先确认用户 OS 再给环境变量命令
- **工程路径不要放在隐藏目录下**：工程路径的每一级目录中不要以 `.` 开头，否则构建时可能会将模块中的代码和配置文件等作为资源打包进产物中

不确定时，**回 `references/04-hvigorw.md` 或对应专题文档搜索原文**，再下笔。

### 4. 引用文档时给出来源

回答用户的命令/参数类问题时，建议在回复结尾标注引用，例如：

> 依据 `references/04-hvigorw.md` 中「编译构建常用扩展参数」一节，以及 `references/06-building-app.md` 的「执行 Hvigor 命令进行构建」示例。

这样用户可以快速核对原文。

### 5. 不要替换或省略本 skill 的检查

即便用户的构建需求「看起来就是 gradle/npm 能解决的」，在 HarmonyOS 上下文中也要按本 skill 的命令核查后再回答；不能默认 gradle/npm 知识可直接套用。

## 高频命令速查表

| 场景 | 命令 |
| --- | --- |
| 清理构建产物 | `hvigorw clean --no-daemon` |
| 构建 Hap（debug） | `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon` |
| 构建 Hap（release） | `hvigorw assembleHap --mode module -p product=default -p buildMode=release --no-daemon` |
| 构建 App | `hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon` |
| 构建 Hsp | `hvigorw assembleHsp --mode module -p module=library@default -p product=default --no-daemon` |
| 构建 Har | `hvigorw assembleHar --mode module -p module=library1@default -p product=default --no-daemon` |
| 安装依赖 | `ohpm install` / `ohpm install --all` |
| 发布 har | `ohpm publish pkg.har` |
| 配置 ohpm 仓库 | `ohpm config set registry https://ohpm.openharmony.cn/ohpm/` |
| 代码检查 | `codelinter` / `codelinter -c code-linter.json5 -f json -o report.json --exit-on error` |
| 增量检查 | `codelinter -i` |
| 检查并修复 | `codelinter -c filepath --fix` |
| 堆栈解析 | `hstack -i D:\crashDir -o D:\outputDir -s D:\sourcemapDir --so D:\soDir -n D:\nameCacheDir` |
| 设备测试 | `hvigorw onDeviceTest -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}` |
| 本地测试 | `hvigorw test -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}` |
| 推送 HAP | `hdc file send "xxx.hap" "data/local/tmp/xxx.hap"` |
| 安装 HAP | `hdc shell bm install -p "data/local/tmp/xxx.hap"` |
| 启动应用 | `hdc shell aa start -a EntryAbility -b com.example.myapplication -m entry` |
| 签名 HAP | `java -jar hap-sign-tool.jar sign-app -keyAlias "demo_key" -signAlg "SHA256withECDSA" -mode "localSign" -appCertFile "/path/demo.cer" -profileFile "/path/demo.p7b" -inFile "/path/hap-unsigned.hap" -keystoreFile "/path/demo.p12" -outFile "/path/hap-signed.hap" -keyPwd "123456Abc" -keystorePwd "123456Abc"` |

## 目录结构

```
arkts-build/
├── SKILL.md                                          # 本文件
└── references/
    ├── INDEX.md                                      # 必先阅读
    ├── 01-command-line-tools-overview.md             # Command Line Tools 获取与环境变量配置
    ├── 02-codelinter.md                              # 代码检查工具（codelinter）
    ├── 03-hstack.md                                  # 堆栈解析工具（hstack）
    ├── 04-hvigorw.md                                 # 命令行构建工具（hvigorw）
    ├── 05-ohpm.md                                    # 三方依赖管理工具（ohpm）
    ├── 06-building-app.md                            # 搭建流水线
    ├── 07-debugging-commands.md                      # SDK 命令行工具与调试命令索引
    └── 08-emulator.md                                # 模拟器工具（Emulator）
```

## 文档来源与维护

- 上游：华为开发者官网「文档中心 › 应用开发 › 命令行工具」系列，路径 `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/` 下：
  - `ide-commandline-get`（获取 Command Line Tools）
  - `ide-command-line-codelinter`（codelinter）
  - `ide-command-line-hstack`（hstack）
  - `ide-hvigor-commandline`（hvigorw）
  - `ide-ohpm-cli` / `ide-ohpm-common-commands`（ohpm）
  - `ide-command-line-building-app`（搭建流水线）
  - `debugging-commands`（调试命令）
  - `ide-commandline-emulator`（Emulator）
- 文档为 2026-06-17 抓取的离线快照，每份文档顶部标注了上游 URL 与抓取时间。
- 如需更新到最新版本，重新运行抓取（从上游 URL `curl`/WebFetch 各 md 文件覆盖到 `references/` 即可）；若需扩充文件清单，请同步更新 `references/INDEX.md`。
- 命令版本差异以官网为准：hvigorw / codelinter / ohpm 等工具的命令与参数会随 HarmonyOS 版本更新，遇到不确定的命令请先 `hvigorw -v` / `codelinter -v` / `ohpm -v` 确认版本。
