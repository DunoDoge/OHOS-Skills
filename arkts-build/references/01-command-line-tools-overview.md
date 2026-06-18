<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get -->
<!-- 抓取时间：2026-06-17 -->

# 获取 Command Line Tools

Command Line Tools 集合了 HarmonyOS 应用开发所用到的系列工具，包括代码检查 `codelinter`、堆栈解析 `hstack`、命令行构建 `hvigorw`、三方依赖管理 `ohpm` 和 SDK 中包含的一系列工具。HarmonyOS SDK 已嵌入命令行工具中，无需额外下载配置。

## 下载 Command Line Tools

请前往[下载中心](https://developer.huawei.com/consumer/cn/download/command-line-tools-for-hmos)获取命令行工具 Command Line Tools，并根据下载中心页面**工具完整性**指导进行完整性校验。

## 配置环境变量

将命令行工具解压，`codelinter`、`ohpm` 等工具存放在 Command Line Tools 的 `bin` 目录下，需要将该目录配置到 PATH 环境变量中。

### Windows

命令行工具解压后，将 `${Command Line Tools 解压路径}\command-line-tools\bin` 目录配置到系统或者用户的 PATH 环境变量中，配置完成后重新打开命令行窗口。

### macOS/Linux

1. 将下载后的命令行工具解压到本地。
2. 打开终端工具，执行 `echo $SHELL` 命令，根据输出结果分别执行不同命令：
   - 如果输出结果为 `/bin/bash`，则执行 `vi ~/.bash_profile` 打开 `.bash_profile` 文件。
   - 如果输出结果为 `/bin/zsh`，则执行 `vi ~/.zshrc` 打开 `.zshrc` 文件。
3. 单击字母 `i`，进入 Insert 模式。
4. 输入以下内容，在 PATH 路径下添加环境变量（请以实际命令行工具存储路径为准）：

```bash
export PATH=${Command Line Tools 解压路径}/command-line-tools/bin:$PATH
```

5. 编辑完成后，单击 `Esc` 键退出编辑模式，然后输入 `:wq`，单击 `Enter` 键保存。
6. 执行以下命令，使配置的环境变量生效：
   - 若打开的是 `.bash_profile`：`source ~/.bash_profile`
   - 若打开的是 `.zshrc`：`source ~/.zshrc`

说明：如需验证是否配置成功，可以使用相关命令验证，例如执行 `codelinter -v` 指令，检查是否可以正确获取 codelinter 工具版本。

## 工具总览

| 工具 | 说明 | 详细文档 |
| --- | --- | --- |
| `codelinter` | 代码检查工具，支持命令行执行代码检查与修复，可集成到门禁或 CI 环境 | [02-codelinter.md](./02-codelinter.md) |
| `hstack` | 堆栈解析工具，将 release 应用混淆后的 crash 堆栈解析为源码对应堆栈 | [03-hstack.md](./03-hstack.md) |
| `hvigorw` | 命令行构建工具，Hvigor 的 wrapper 包装工具，执行构建命令 | [04-hvigorw.md](./04-hvigorw.md) |
| `ohpm` | 三方依赖管理工具，OpenHarmony 三方库的包管理工具 | [05-ohpm.md](./05-ohpm.md) |
| SDK 命令行工具 | 包括 hdc、aa、bm、hilog、hidumper、hitrace、hiperf 等调试调优工具 | [07-debugging-commands.md](./07-debugging-commands.md) |
| `Emulator` | 模拟器工具，支持命令行创建、启动、关闭模拟器 | [08-emulator.md](./08-emulator.md) |

## 相关文档

- [搭建流水线](./06-building-app.md)：完整的 CI 流水线搭建流程（环境配置 → 构建 → 签名 → 安装运行）
- [SDK 命令行工具简介](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/command-line-tools-overview)
