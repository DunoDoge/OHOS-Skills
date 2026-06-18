<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-emulator -->
<!-- 抓取时间：2026-06-17 -->

# 模拟器工具（Emulator）

从 6.1.0 Release 版本开始，Command Line Tools 集成 Emulator 工具，支持 Windows 和 macOS 平台，可独立进行模拟器创建、启动、关闭、镜像下载等操作。

从 26.0.0 Beta1 版本开始，支持在 Linux 平台上使用 Emulator。

说明：在 macOS 上使用命令行工具时，如果弹框提示 Emulator 无法验证开发者，可以在系统的**设置 > 隐私与安全性**中选择**仍要打开 Emulator**，或者使用 DevEco Studio 目录下的 Emulator 工具。

## 环境准备

Emulator 工具在 command-line-tools 安装目录的 `emulator` 目录下，有两种执行命令的方式：

- **方式一**：在命令行终端中进入 `emulator` 目录下，执行命令。
- **方式二**：配置环境变量后，在任意目录下执行命令。
  - Windows：在系统或用户的 PATH 变量中，添加路径 `{command-line-tools 安装目录}/emulator`。
  - macOS/Linux：`export PATH={command-line-tools 安装目录}/emulator:$PATH`

## 模拟器命令

Emulator 命令请参考[通过命令行使用模拟器](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-emulator-command-line)。

## 在模拟器上推包调试

可通过 hdc 工具在模拟器上进行推包调试。

1. 确认模拟器和 hdc 的连接状态。模拟器的 IP 和端口号是 `127.0.0.1:5555`，如果端口号已经被占用，则从 5555 起递增 2（如 5555、5557、5559），端口号范围在 5555-15555 之间：

```bash
hdc list target
```

2. 如果未连接，执行命令连接模拟器：

```bash
hdc tconn 127.0.0.1:5555
```

3. 连接成功后，通过 hdc 在模拟器上安装、卸载应用等，更多使用方式请参考 [07-debugging-commands.md](./07-debugging-commands.md)。

## 使用 Linux 版本 Emulator 工具

从 26.0.0 Beta1 版本开始，支持在 Linux 平台使用模拟器工具。

### 环境准备

当前仅支持 Ubuntu 18.04 及以上的 Linux 系统，使用前需要安装相关的依赖：

```bash
apt install -y libatomic1 libpulse0 libegl1 libgbm1 libgl1 libpng16-16 libfontconfig1 libfreetype6 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-shape0 libxcb-xinerama0 libxcb-xkb1 libsm6 libice6 libxkbcommon-x11-0 libxkbcommon0 libglib2.0-0
```

### 使用约束

- Linux 模拟器依赖系统 kvm 能力，需要手动将 Emulator 程序当前用户加入 `/dev/kvm` 所在的组中。
- Linux 模拟器图形渲染依赖 `/dev/dri` 下的设备渲染节点（如 card0、renderD128 等），需要手动将 Emulator 程序当前用户加入相关节点的用户组中。
- 如需使用第三方远程桌面工具操作 Linux，请确保工具可使用的图形驱动支持 OpenGL 4.1 或以上版本。

### 模拟器命令差异

针对无图形界面的 Linux 环境，启动模拟器命令必须添加 `-noWindow` 参数。除此之外，其他命令和 Windows/macOS 相同。

### 使用远程服务（gRPC）

Linux 模拟器提供了对外的 gRPC 服务，开发者可通过调用模拟器服务接口，远程获取模拟器内的视频流数据、音频流数据，以及远程使用场景化命令和鼠标点击功能。

**启动 gRPC 服务器模式命令**：

```bash
# 无认证模式
Emulator -start {模拟器名称} -instancePath {模拟器实例路径} -imageRoot {模拟器镜像路径} -grpcServer -grpcPort {端口} -noAuth

# 认证模式
Emulator -start {模拟器名称} -instancePath {模拟器实例路径} -imageRoot {模拟器镜像路径} -grpcServer -grpcPort {端口} -pem_root_certs {根证书路径} -pem_private_key {私钥路径} -pem_cert_chain {证书链路径}
```

**参数说明**：

| 参数名 | 说明 |
| --- | --- |
| `-start` | 必选参数，指定模拟器名称。 |
| `-instancePath` | 可选参数，指定模拟器实例路径。如果不指定，默认使用 DevEco Studio 中的模拟器实例路径。 |
| `-imageRoot` | 可选参数，指定模拟器镜像路径。如果不指定，默认使用 DevEco Studio 中的模拟器镜像路径。 |
| `-grpcServer` | 必选参数，指定模拟器启动模式为 gRPC 服务器模式。 |
| `-grpcPort` | 可选参数，指定服务器的端口号。如果不指定，默认范围 6555-6755，端口冲突情况下，默认端口号累加 2。 |
| `-noAuth` | 可选参数，使用无认证模式启动。 |
| `-pem_root_certs` | 可选参数，使用认证模式后必选，指定根证书路径。要求服务端和客户端证书均支持双向认证。 |
| `-pem_private_key` | 可选参数，使用认证模式后必选，指定私钥路径。 |
| `-pem_cert_chain` | 可选参数，使用认证模式后必选，指定证书链路径。 |

如果使用认证模式，启动后在命令执行路径下会生成 token 文件 `server_token.txt`，其中包含认证所需要的 token 字段。

### gRPC 服务

模拟器提供的 gRPC 服务包括：

- **VideoStreamService**：服务端接收客户端视频流请求，返回视频帧流。
- **AudioStreamService**：服务端接收客户端音频流请求，返回音频帧流。
- **ScenarioCommandService**：场景化命令服务，支持远程执行场景化命令。
- **MouseInputService**：鼠标输入服务，支持远程模拟鼠标点击。

详细的服务接口定义和消息结构请参考[官方文档](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-emulator)。

## 相关文档

- [通过命令行使用模拟器](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-emulator-command-line)
- [hdc 工具](https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/hdc)
