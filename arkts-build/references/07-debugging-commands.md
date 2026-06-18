<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/debugging-commands -->
<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/command-line-tools-overview -->
<!-- 抓取时间：2026-06-17 -->

# SDK 命令行工具与调试命令索引

本文档以索引形式列出 HarmonyOS SDK 命令行工具清单。构建/部署高频命令（`hdc file send` / `hdc shell bm install` / `hdc shell aa start`）的完整示例已在 [06-building-app.md](./06-building-app.md) 中给出。

## SDK 命令行工具简介

HarmonyOS SDK 提供了一系列命令行工具，用于应用调试、调优、设备管理、打包拆包等场景。这些工具存放在 SDK 的 `toolchains` 目录下。

详细说明请参考 [SDK 命令行工具简介](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/command-line-tools-overview)。

## 工具清单

| 工具 | 用途 | 官方文档 |
| --- | --- | --- |
| `hdc` | HarmonyOS Device Connector，用于与设备/模拟器交互（文件传输、shell 命令、应用安装等） | [hdc](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hdc) |
| `aa` | Ability Assistant，用于启动/停止 Ability、查询 Ability 信息等 | [aa 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/aa-tool) |
| `bm` | Bundle Manager，用于应用安装/卸载/查询等包管理操作 | [bm 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/bm-tool) |
| 打包拆包工具 | 用于 HAP/HSP 包的打包与拆包 | [打包拆包工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/packing-unpacking) |
| 扫描工具 | 应用安全扫描检查 | [扫描工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/app-check-tool) |
| `cem` | Common Event Manager，公共事件管理 | [cem 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/cem-tool) |
| `anm` | Ability Notification Manager，通知管理 | [anm 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/anm-tool) |
| `edm` | Enterprise Device Manager，企业设备管理 | [edm 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/edm-tool) |
| `restool` | 资源编译工具，用于编译资源文件 | [restool 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/restool) |
| `param` | 系统参数管理工具 | [param 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/param-tool) |
| `power-shell` | 电源管理工具 | [power-shell 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/power-shell) |
| `atm` | AccessToken Manager，访问令牌管理 | [atm 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/atm-tool) |
| `network-cfg` | 网络配置工具 | [network-cfg 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/network-cfg) |
| `hilog` | 日志打印工具，用于在代码中打印日志 | [hilog](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hilog) |
| `hilogtool` | 日志命令行工具，用于命令行获取/过滤日志 | [hilogtool](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hilog-tool) |
| `hidumper` | 系统信息 dump 工具，用于获取系统运行时信息 | [hidumper 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hidumper-tool) |
| `hitrace` | 分布式调用链跟踪工具，用于性能分析 | [hitrace](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hitrace) |
| `hiperf` | 性能 profiling 工具，用于采集 CPU 采样等性能数据 | [hiperf](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hiperf) |
| `hiprofiler` | 性能分析工具，用于内存/CPU/能耗等性能分析 | [hiprofiler](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hiprofiler) |
| `uinput` | 输入事件注入工具，用于模拟用户输入 | [uinput](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/uinput) |
| 命令行工具 | 通用命令行工具集 | [命令行工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/command-line-utilities) |
| `netcopilot` | 网络诊断工具 | [netcopilot 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/network-netcopilot) |
| 二进制签名工具 | 用于二进制文件签名 | [二进制签名工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/binary-sign-tool) |

## 构建/部署高频命令

以下命令在 [06-building-app.md](./06-building-app.md) 中有完整示例：

```bash
# 推送 HAP 到设备
hdc file send "{PROJECT_PATH}/entry/build/default/outputs/default/entry-default-signed.hap" "data/local/tmp/entry-default-signed.hap"

# 安装 HAP
hdc shell bm install -p "data/local/tmp/entry-default-signed.hap"

# 删除临时 HAP
hdc shell rm -rf "data/local/tmp/entry-default-signed.hap"

# 启动应用
hdc shell aa start -a EntryAbility -b com.example.myapplication -m entry
```

## 相关文档

- [Test Kit 简介](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/test-kit-overview)
- [SDK 命令行工具简介](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/command-line-tools-overview)
- [系统调测调优](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/system-debug-optimize)
