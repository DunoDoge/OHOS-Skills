<!-- 必先阅读 -->
<!-- 命令版本差异以官网为准：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get -->

# INDEX - arkts-build 参考文档索引

> **必先阅读**：任何 arkts-build 任务开始前，**必须先读本文件**，再根据任务类型按映射表加载对应文档。
>
> **命令版本差异以官网为准**：hvigorw / codelinter / ohpm 等工具的命令与参数会随 HarmonyOS 版本更新，本文档为 2026-06-17 抓取的离线快照，遇到不确定的命令请先 `hvigorw -v` / `codelinter -v` / `ohpm -v` 确认版本，并以上游官网文档为准。

## 文档角色一览

| 文件 | 角色 |
| --- | --- |
| `01-command-line-tools-overview.md` | Command Line Tools 获取、环境变量配置（Windows/macOS/Linux）、工具总览 |
| `02-codelinter.md` | 代码检查工具 `codelinter` 命令行参数、规则配置、增量检查、QuickFix、退出码、输出格式 |
| `03-hstack.md` | release 崩溃堆栈解析工具 `hstack` 参数、sourceMap/so/nameCache 归档、解析原理与示例 |
| `04-hvigorw.md` | 命令行构建工具 `hvigorw` 任务、扩展参数、daemon、日志、可视化、性能开关、测试命令 |
| `05-ohpm.md` | 三方依赖管理工具 `ohpm` 常用命令、oh-package.json5、仓库配置 |
| `06-building-app.md` | 搭建流水线完整流程（环境配置 → ohpm install → hvigorw 构建 → 签名 → hdc 安装运行 → 示例脚本） |
| `07-debugging-commands.md` | SDK 命令行工具索引（hdc/aa/bm/hilog/hidumper/hitrace/hiperf 等） |
| `08-emulator.md` | 模拟器工具（Emulator）命令行使用、推包调试、Linux 版本、gRPC 远程服务 |

## 按任务类型的查阅路径

| 任务类型 | 必读文件（在 `references/` 下） |
| --- | --- |
| 工具获取 / 环境变量配置 | `01-command-line-tools-overview.md` |
| 代码静态检查 / CI 门禁 | `02-codelinter.md` |
| release 崩溃堆栈解析 | `03-hstack.md` |
| **hvigorw 构建命令 / 构建参数** | `04-hvigorw.md` |
| ohpm 装包 / 发包 / 依赖管理 | `05-ohpm.md` |
| **搭建 CI 流水线 / 构建后签名安装运行** | `06-building-app.md`（+ `04-hvigorw.md`） |
| 设备调试命令（hdc/aa/bm 等） | `07-debugging-commands.md`（+ `06-building-app.md` 的「运行应用」一节） |
| 模拟器使用 | `08-emulator.md` |
| 测试（onDeviceTest / Local Test） | `04-hvigorw.md` 的「测试命令」一节 |

## 关键命令速记

```bash
# === hvigorw 构建 ===
hvigorw clean --no-daemon                                          # 清理构建产物
hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon   # 构建 Hap
hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon # 构建 App
hvigorw assembleHsp --mode module -p module=library@default -p product=default --no-daemon  # 构建 Hsp
hvigorw assembleHar --mode module -p module=library1@default -p product=default --no-daemon  # 构建 Har

# === hvigorw 测试 ===
hvigorw onDeviceTest -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}  # 设备测试
hvigorw test -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}          # 本地测试

# === ohpm 依赖管理 ===
ohpm install                          # 安装依赖
ohpm install --all                    # 安装所有依赖（含模块下）
ohpm publish pkg.har                  # 发布 har
ohpm config set registry https://ohpm.openharmony.cn/ohpm/  # 配置仓库
ohpm config set strict_ssl false      # 关闭严格 SSL

# === codelinter 代码检查 ===
codelinter                            # 默认检查
codelinter -c code-linter.json5 -f json -o report.json --exit-on error  # CI 检查
codelinter -i                         # 增量检查
codelinter -c filepath --fix          # 检查并自动修复

# === hstack 堆栈解析 ===
hstack -i D:\crashDir -o D:\outputDir -s D:\sourcemapDir --so D:\soDir -n D:\nameCacheDir

# === hdc 安装运行 ===
hdc file send "xxx.hap" "data/local/tmp/xxx.hap"     # 推送 HAP
hdc shell bm install -p "data/local/tmp/xxx.hap"     # 安装 HAP
hdc shell aa start -a EntryAbility -b com.example.myapplication -m entry  # 启动应用

# === 签名 ===
java -jar hap-sign-tool.jar sign-app -keyAlias "demo_key" -signAlg "SHA256withECDSA" -mode "localSign" \
  -appCertFile "/path/demo.cer" -profileFile "/path/demo.p7b" -inFile "/path/hap-unsigned.hap" \
  -keystoreFile "/path/demo.p12" -outFile "/path/hap-signed.hap" -keyPwd "123456Abc" -keystorePwd "123456Abc"
```

## 版本相关命令速记

以下命令有版本要求，使用前先 `hvigorw -v` 确认版本：

| 命令/参数 | 起始版本 |
| --- | --- |
| `buildInfo` / `-v` 任意路径执行 / `--max-semi-space-size` | hvigorw 5.18.4 |
| `onDeviceTest` 的 `ohos-debug-asan` | hvigorw 5.19.0 |
| `--optimization-strategy` | hvigorw 5.19.2 |
| `--analyze=ultrafine` | hvigorw 6.0.0 |
| `-p buildVersion=` | hvigorw 6.23.3 |
