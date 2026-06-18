<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-command-line-building-app -->
<!-- 抓取时间：2026-06-17 -->

# 搭建流水线

除了使用 DevEco Studio 一键式构建应用/元服务外，还可以使用命令行工具来调用 Hvigor 任务进行构建。通过命令行的方式构建应用或元服务，可用于构建 CI（Continuous Integration）流水线，按照计划时间自动化地构建 HAP/APP、签名、安装运行等操作。

本文以 Linux 系统为例进行讲解，Windows/macOS 系统与 Linux 系统在调用命令行任务上没有区别，仅在搭建构建环境上存在差异。

说明：
- 如果开发者所使用的电脑处于完全无网络的环境中，搭建构建环境请参考文末「无网络流水线搭建」。
- HarmonyOS SDK 已嵌入命令行工具中，无需额外下载配置。
- 请在执行命令行之前，保证当前工程是可信任的，确保安全编译。

## 系统平台要求

- Linux：64 位操作系统
- GLIBC：2.28 或更高版本
- 内存：推荐使用 16GB 及以上，最小 8GB
- 硬盘：100GB 及以上

## 预置条件

### 配置 JDK

1. 下载 JDK，支持 JDK 17 版本。
2. 解压安装包并配置环境变量：

```bash
#jdk
export JAVA_HOME=/opt/jdk-17.0.6_linux-x64_bin
export PATH=$PATH:$JAVA_HOME/bin
```

3. 验证：`java -version`

### 获取命令行工具

1. [命令行工具获取](./01-command-line-tools-overview.md)。
2. 解压命令行工具，将解压后所在的路径定义为 `COMMANDLINE_TOOL_DIR`：

```bash
export COMMANDLINE_TOOL_DIR=/opt
```

### 配置 Node.js 环境变量

命令行工具包含了配套的 Node.js：

```bash
# Linux/macOS（Node.js 在 tool/node/bin 目录下）
export NODE_HOME=${COMMANDLINE_TOOL_DIR}/command-line-tools/tool/node
export PATH=$PATH:$NODE_HOME/bin

# Windows（Node.js 在 tool/node 目录下）
```

验证：`node -v`

说明：建议使用命令行工具中自带的 Node.js，若另外单独下载配置其他版本的 Node.js，推荐使用 v18 版本。

### 配置 hdc 环境变量

hdc 工具存放在命令行工具自带的 sdk 下的 toolchains 目录中：

```bash
export HDC_HOME=${COMMANDLINE_TOOL_DIR}/command-line-tools/sdk/default/openharmony/toolchains
export PATH=$PATH:$HDC_HOME
```

### 配置 hvigor 环境变量

```bash
export PATH=${COMMANDLINE_TOOL_DIR}/command-line-tools/bin:$PATH
```

验证：`hvigorw -v`

### 配置 npm 镜像仓库

若工程在 `hvigor/hvigor-config.json5` 文件中依赖 npm 三方组件，流水线中需要配置 npm 镜像地址：

```bash
npm config set registry https://repo.huaweicloud.com/repository/npm/
npm config set "@ohos:registry" https://repo.harmonyos.com/npm/
```

### 安装 ohpm

```bash
export PATH=${COMMANDLINE_TOOL_DIR}/command-line-tools/bin:$PATH
ohpm -v

# 配置仓库地址
ohpm config set registry https://ohpm.openharmony.cn/ohpm/
ohpm config set strict_ssl false
```

### 安装 libGL1 库（Linux）

在 Linux 系统的构建场景下，使用纹理压缩功能需要安装 libGL1 库：

```bash
# Ubuntu/Debian
apt install -y libgl1-mesa-dev
# CentOS/RHEL
yum install -y mesa-libGL-devel
```

## 构建应用

### 安装工程及模块依赖

使用命令行进行构建前，需要分别进入工程及各个模块下执行 `ohpm install` 命令，安装**工程及各个模块**依赖的三方库。

```bash
# 定义工程路径
PROJECT_PATH=xxx/xxx/project_name

# 切换到指定目录并执行 ohpm install
function ohpm_install() {
    cd $1
    ohpm install --all
}

# 安装工程及各个模块的三方库依赖
ohpm_install "${PROJECT_PATH}"
ohpm_install "${PROJECT_PATH}/entry"
ohpm_install "${PROJECT_PATH}/xxx"
```

注意：工程目录不要存放在隐藏目录下（即工程路径的每一级目录中不要以 `.` 开头），否则构建时可能会将模块中的代码和配置文件等作为资源打包进产物中，不会进行混淆或加密。

### 执行 Hvigor 命令进行构建

```bash
# clean 工程
hvigorw clean --no-daemon

# 构建 Hap，产物：${PROJECT_PATH}/{moduleName}/build/{productName}/outputs/{targetName}/xxx.hap
hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon

# 构建 Hsp，产物：${PROJECT_PATH}/{moduleName}/build/{productName}/outputs/{targetName}/(xxx.har | xxx.hsp)
hvigorw assembleHsp --mode module -p module=library@default -p product=default --no-daemon

# 构建 Har，产物：${PROJECT_PATH}/{moduleName}/build/{productName}/outputs/{targetName}/outputs/xxx.har
hvigorw assembleHar --mode module -p module=library1@default -p product=default --no-daemon

# 构建 App，产物：${PROJECT_PATH}/build/outputs/{productName}/xxx.app
hvigorw assembleApp --mode project -p product=default -p buildMode=debug --no-daemon
```

更多 hvigorw 命令参数详见 [04-hvigorw.md](./04-hvigorw.md)。

### 大小写敏感检查

Linux 环境会对大小写敏感。通过在项目级的 `build-profile.json5` 文件中配置 `caseSensitiveCheck` 为 `true` 来保持 Windows/macOS 环境编译与 Linux 环境编译结果一致：

```json5
{
  "name": "default",
  "compatibleSdkVersion": "6.1.1(24)",
  "runtimeOS": "HarmonyOS",
  "buildOption": {
    "strictMode": {
      "caseSensitiveCheck": true
    }
  }
}
```

## 运行应用

如果构建时已配置签名文件，会分别生成已签名包（如 `xxx-signed.hap`）和未签名包（如 `xxx-unsigned.hap`）。如果需要对包进行重签名，可使用签名工具对未签名包进行签名。

### 准备申请签名所需文件

准备好申请签名所需 3 个文件：**密钥（.p12 文件）、数字证书（.cer 文件）、Profile（.p7b 文件）**。

#### 生成密钥和证书请求文件

使用 JDK 携带的 Keytool 工具生成密钥和证书请求文件：

```bash
# 生成密钥库文件
keytool -genkeypair -alias "demo_key" -keyalg EC -groupname secp256r1 -sigalg SHA256withECDSA -dname "C=CN,O=HUAWEI,OU=HUAWEI IDE,CN=demo_key" -keystore /path/demo.p12 -storetype pkcs12 -validity 9125 -storepass 123456Abc -keypass 123456Abc
```

参数说明：
- `alias`：密钥的别名信息。
- `dname`：证书基本信息（C=国家/地区代码，O=组织名称，OU=组织单位名称，CN=名字与姓氏）。
- `keystore`：密钥库文件路径。
- `validity`：证书有效期（如 9125 = 25 年）。
- `storepass`：密钥库密码（大写字母、小写字母、数字和特殊符号中的两种以上字符组合，长度至少 8 位）。
- `keypass`：密钥的密码（与 storepass 保持一致）。

```bash
# 生成证书请求文件（执行后需要输入 storepass 密码）
keytool -certreq -alias "demo_key" -sigalg SHA256withECDSA -keystore /path/demo.p12 -storetype pkcs12 -file /path/demo.csr
```

#### 申请调试数字证书和 Profile 文件

生成证书请求文件后，在 AppGallery Connect 中申请、下载调试数字证书（.cer）和 Profile 文件（.p7b）。

### 对未签名的 HAP/APP 进行签名

签名工具 `hap-sign-tool.jar` 位于 `${COMMANDLINE_TOOL_DIR}/command-line-tools/sdk/default/openharmony/toolchains/lib` 下：

```bash
java -jar hap-sign-tool.jar sign-app \
  -keyAlias "demo_key" \
  -signAlg "SHA256withECDSA" \
  -mode "localSign" \
  -appCertFile "/path/demo.cer" \
  -profileFile "/path/demo.p7b" \
  -inFile "/path/hap-unsigned.hap" \
  -keystoreFile "/path/demo.p12" \
  -outFile "/path/hap-signed.hap" \
  -keyPwd "123456Abc" \
  -keystorePwd "123456Abc"
```

参数说明：
- `keyAlias`：密钥别名。
- `appCertFile`：申请的调试证书文件（.cer）。
- `profileFile`：申请的调试 Profile 文件（.p7b）。
- `inFile`：通过 Hvigor 打包生成的未携带签名信息的 HAP。
- `keystoreFile`：密钥库文件（.p12）。
- `outFile`：经过签名后生成的携带签名信息的 HAP。
- `keyPwd`：密钥密码。
- `keystorePwd`：密钥库密码。

说明：如果要对 APP 进行签名，只需将 `inFile` 和 `outFile` 参数修改为 APP 包即可。

### 通过 hdc 安装运行

通过 hdc 工具将 HAP 推送到真机设备上进行安装，推送的 HAP 必须是携带签名信息的：

```bash
# 将打包好的 hap 包推送至设备中
hdc file send "${PROJECT_PATH}/entry/build/default/outputs/default/entry-default-signed.hap" "data/local/tmp/entry-default-signed.hap"

# 安装 hap 包
hdc shell bm install -p "data/local/tmp/entry-default-signed.hap"

# 删除 hap 包
hdc shell rm -rf "data/local/tmp/entry-default-signed.hap"

# 在设备上运行 HAP
hdc shell aa start -a EntryAbility -b com.example.myapplication -m entry
```

## 示例脚本

以下脚本无法直接运行，仅供参考，业务要根据自己的情况来进行适配：

```bash
#!/bin/bash
set -ex

JAVA_HOME=xxx #指定JDK的安装目录
COMMANDLINE_TOOL_DIR=xxx #命令行工具的安装目录

#配置hvigor、ohpm环境变量
export PATH=${COMMANDLINE_TOOL_DIR}/command-line-tools/bin:$PATH

#配置hdc环境变量
function init_hdc() {
  export HDC_HOME=${COMMANDLINE_TOOL_DIR}/command-line-tools/sdk/default/openharmony/toolchains
  export PATH=$HDC_HOME:$PATH
}

# 安装ohpm
function init_ohpm() {
  ohpm -v
  ohpm config set registry https://ohpm.openharmony.cn/ohpm/
}

# 初始化相关路径
PROJECT_PATH=xxx # 工程目录

# 进入package目录安装依赖
function ohpm_install {
    cd $1
    ohpm install
}

# 环境适配
function buildHAP() {
    ohpm_install "${PROJECT_PATH}"
    ohpm_install "${PROJECT_PATH}/entry"
    ohpm_install "${PROJECT_PATH}/xxx"

    cd ${PROJECT_PATH}
    hvigorw clean --no-daemon
    hvigorw assembleHap --mode module -p product=default -p debuggable=false --no-daemon
}

function install_hap() {
    hdc file send "${PROJECT_PATH}/entry/build/default/outputs/default/entry-default-signed.hap" "data/local/tmp/entry-default-signed.hap"
    hdc shell bm install -p "data/local/tmp/entry-default-signed.hap"
    hdc shell rm -rf "data/local/tmp/entry-default-signed.hap"
    hdc shell aa start -a MainAbility -b com.example.myapplication -m entry
}

# 使用ohpm发布har
function upload_har {
    ohpm publish pkg.har
}

function main {
  local startTime=$(date '+%s')
  init_hdc
  init_ohpm
  buildHAP
  install_hap
  upload_har
  local endTime=$(date '+%s')
  local elapsedTime=$(expr $endTime - $startTime)
  echo "build success in ${elapsedTime}s..."
}

main
```

## 无网络流水线搭建

如果开发者使用的电脑处于完全无网络的环境中，可参考以下步骤搭建流水线环境：

### 安装 pnpm 插件

1. 请在可访问网络的电脑上创建一个空文件夹。
2. 在该文件夹下执行 `pnpm install pnpm` 安装 pnpm。
3. 将该文件夹打包后拷贝到无网络环境。
4. 在无网络环境中解压，配置 pnpm 到 PATH。

### 安装 npm 依赖插件

若工程在 `hvigor/hvigor-config.json5` 中依赖 npm 三方组件，需在可访问网络的电脑上下载依赖后拷贝到无网络环境。

### 安装 ohpm 依赖

在可访问网络的电脑上执行 `ohpm install` 安装依赖，将 `oh_modules` 目录打包后拷贝到无网络环境的工程对应位置。
