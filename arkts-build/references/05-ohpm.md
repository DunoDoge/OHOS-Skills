<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-ohpm-cli -->
<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-ohpm-common-commands -->
<!-- 抓取时间：2026-06-17 -->

# 三方依赖管理工具（ohpm）

`ohpm` 作为 OpenHarmony 三方库的包管理工具，支持 OpenHarmony 共享包的发布、安装和依赖管理。

## 常用命令清单

| 命令 | 说明 |
| --- | --- |
| `ohpm install` | 安装 oh-package.json5 中声明的依赖，或安装指定的三方库 |
| `ohpm init` | 初始化一个 ohpm 包（生成 oh-package.json5） |
| `ohpm publish` | 发布三方库到 ohpm 仓库 |
| `ohpm unpublish` | 撤销已发布的三方库 |
| `ohpm prepublish` | 在 publish 之前执行的预处理命令 |
| `ohpm uninstall` | 卸载指定的三方库 |
| `ohpm update` | 更新指定的三方库到最新版本 |
| `ohpm list` | 列出已安装的三方库 |
| `ohpm info` | 查看指定三方库的详细信息 |
| `ohpm config` | 查看/设置 ohpm 配置 |
| `ohpm version` | 查看 ohpm 版本 |
| `ohpm --version` | 查看 ohpm 版本（简写 `-v`） |
| `ohpm root` | 查看 ohpm 安装根目录 |
| `ohpm cache clean` | 清理 ohpm 缓存 |
| `ohpm clean` | 清理 ohpm 相关数据 |
| `ohpm run` | 运行 oh-package.json5 中定义的脚本 |
| `ohpm ping` | 测试 ohpm 仓库连通性 |
| `ohpm dist-tags` | 查看或修改三方库的 dist-tags |
| `ohpm convert` | 转换工具 |
| `ohpm dependency-check` | 依赖检查 |
| `ohpm help` | 查看 ohpm 帮助 |

## 安装与配置

### 安装 ohpm

ohpm 工具在 Command Line Tools 的 `bin` 目录下，需要将该目录配置到 PATH 环境变量中（参考 [01-command-line-tools-overview.md](./01-command-line-tools-overview.md)）。

```bash
# 验证安装
ohpm -v
```

### 配置仓库地址

```bash
# 配置 ohpm 仓库地址（可指定多个地址，',' 号分割）
ohpm config set registry https://ohpm.openharmony.cn/ohpm/

# 关闭严格 SSL 校验（CI 环境常用）
ohpm config set strict_ssl false
```

## 常用操作示例

### 安装依赖

```bash
# 安装 oh-package.json5 中声明的所有依赖
ohpm install

# 安装所有依赖（含模块下依赖）
ohpm install --all

# 安装指定三方库
ohpm install @ohos/lottie
```

### 发布三方库

```bash
ohpm publish pkg.har
```

### 查看已安装依赖

```bash
ohpm list
```

### 查看配置

```bash
# 查看所有配置
ohpm config

# 查看指定配置项
ohpm config get registry
```

## oh-package.json5

ohpm 使用 `oh-package.json5` 文件管理依赖。该文件位于工程根目录及各模块目录下。

```json5
{
  "name": "my-package",
  "version": "1.0.0",
  "description": "please describe your package",
  "main": "Index.ets",
  "author": "",
  "license": "Apache-2.0",
  "dependencies": {
    "@ohos/lottie": "^2.0.0"
  },
  "devDependencies": {}
}
```

## 相关文档

- [ohpmrc 配置](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-ohpmrc)
- [oh-package.json5 配置](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-oh-package-json5)
- [ohpm 错误码](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-ohpm-errorcode)
- [系统平台要求](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-ohpm-system-platform)
