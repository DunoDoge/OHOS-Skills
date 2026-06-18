## 1. 创建 skill 目录结构

- [x] 1.1 创建 `arkts-build/` 目录及 `arkts-build/references/` 子目录
- [x] 1.2 确认目录结构与 `arkts-helper` / `arkts-debug` / `arkts-ndk-dev` 一致（`SKILL.md` 在根，参考文档在 `references/`）

## 2. 编写 references/INDEX.md 索引文件

- [x] 2.1 编写 `references/INDEX.md`，包含：各文档角色一句话说明、按任务类型（构建/检查/堆栈解析/依赖管理/流水线/调试/模拟器）的查阅路径表、关键命令速记（clean/assembleHap/assembleApp/ohpm install/codelinter/hstack/hdc 安装运行/onDeviceTest）
- [x] 2.2 在 INDEX.md 顶部标注「必先阅读」提示与「命令版本差异以官网为准」说明

## 3. 编写 references/ 离线参考文档

- [x] 3.1 编写 `01-command-line-tools-overview.md`：Command Line Tools 获取、Windows/macOS/Linux 环境变量配置、工具总览（codelinter/hstack/hvigorw/ohpm/SDK），来源 `ide-commandline-get`
- [x] 3.2 编写 `02-codelinter.md`：`codelinter` 命令行格式、参数表（--config/--fix/--format/--output/--version/--product/--incremental/--language/--exit-on）、退出码计算方式、工程根目录与非工程根目录用法、输出格式示例，来源 `ide-command-line-codelinter`
- [x] 3.3 编写 `03-hstack.md`：`hstack` 命令行格式、参数表（-i/-c/-o/-s/--so/-n/-v/-h）、环境配置（PATH/Node/ADDR2LINE_PATH）、使用示例、堆栈解析原理（sourceMap + nameCache 还原路径/行号/方法名）、RelWithDebInfo so 配置，来源 `ide-command-line-hstack`
- [x] 3.4 编写 `04-hvigorw.md`：`hvigorw` 命令行格式、查询/编译构建/日志/可视化/daemon/性能内存/公共命令/其他命令参数表、构建任务（clean/assembleHap/assembleApp/assembleHsp/assembleHar/collectCoverage）、扩展参数（-p buildMode/-p product/-p module/-p coverage/-p ohos-test-coverage/-p debuggable/-p buildVersion）、测试命令（onDeviceTest/test）、版本相关命令标注，来源 `ide-hvigor-commandline`
- [x] 3.5 编写 `05-ohpm.md`：`ohpm` 常用命令清单（install/init/publish/uninstall/update/list/info/config/version/cache clean/run/ping/clean/dist-tags/convert/dependency-check）、oh-package.json5、仓库地址配置（`https://ohpm.openharmony.cn/ohpm/`、strict_ssl），来源 `ide-ohpm-cli` 与 `ide-ohpm-common-commands`
- [x] 3.6 编写 `06-building-app.md`：搭建流水线完整流程（系统平台要求、JDK/Node/hdc/hvigor/ohpm 环境配置、npm 镜像、libGL1、ohpm install 工程及模块依赖、hvigorw 构建命令与产物路径、签名三件套 .p12/.cer/.p7b、keytool 生成密钥与 csr、hap-sign-tool.jar 签名、hdc 安装运行、示例脚本、无网络流水线、caseSensitiveCheck），来源 `ide-command-line-building-app`
- [x] 3.7 编写 `07-debugging-commands.md`：SDK 命令行工具索引（hdc/aa/bm/打包拆包/扫描/cem/anm/edm/restool/param/power-shell/atm/network-cfg/hilog/hilogtool/hidumper/hitrace/hiperf/hiprofiler/uinput/命令行工具/netcopilot/二进制签名工具），每个工具一句话用途 + 官方链接，来源 `debugging-commands`
- [x] 3.8 编写 `08-emulator.md`：模拟器工具（Emulator）命令行使用说明，来源 `ide-commandline-emulator`
- [x] 3.9 为每份参考文档顶部标注上游 URL 与抓取时间（2026-06-17）

## 4. 编写 SKILL.md

- [x] 4.1 编写 frontmatter（`name: arkts-build` + `description`，description 含触发关键词：hvigorw/codelinter/hstack/ohpm/assembleHap/流水线/CI/签名/hdc/onDeviceTest 等）
- [x] 4.2 编写「何时启用本 skill」章节，列出触发条件与关键词清单
- [x] 4.3 编写「与已有 skill 的边界」章节，明确与 `arkts-helper`/`arkts-debug`/`arkts-ndk-dev` 的交叉引用关系
- [x] 4.4 编写「工作流程（严格遵守）」章节：先读 INDEX → 按场景加载文档 → 执行命令 → 引用来源
- [x] 4.5 编写「高频命令速查表」：clean/assembleHap/assembleApp/assembleHsp/assembleHar/ohpm install/codelinter/hstack/hdc 安装运行/onDeviceTest/test
- [x] 4.6 编写「高频红线」清单：CI 必加 `--no-daemon`、`-p module=` 必须配 `--mode module`、构建前必须 `ohpm install`、release 堆栈必须 sourceMap+nameCache、签名三件套、产物路径规律、版本相关命令先 `hvigorw -v`、平台差异先确认 OS
- [x] 4.7 编写「目录结构」与「文档来源与维护」章节（上游 URL、更新方式说明）

## 5. 验证与收尾

- [x] 5.1 检查 `references/` 目录文件清单与 SKILL.md 中「目录结构」章节一致
- [x] 5.2 检查 SKILL.md 的 frontmatter 格式与已有 skill（arkts-debug/arkts-helper/arkts-ndk-dev）一致
- [x] 5.3 检查所有参考文档顶部均标注上游 URL 与抓取时间
- [x] 5.4 检查 INDEX.md 的「任务类型 → 必读文件」映射表覆盖所有 8 份文档
- [x] 5.5 运行 `openspec status --change "add-arkts-build-skill"` 确认所有 artifact 完成
