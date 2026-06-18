<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-hvigor-commandline -->
<!-- 抓取时间：2026-06-17 -->

# 命令行构建工具（hvigorw）

`hvigorw` 作为 Hvigor 的 wrapper 包装工具，支持自动安装 Hvigor 构建工具和相关插件依赖，以及执行 Hvigor 构建命令。

执行命令前，需要先配置 JDK，配置 Node.js、hvigor 等环境变量，具体请参考[搭建流水线](./06-building-app.md)。

## 命令行格式

```
hvigorw [taskNames...] <options>
```

其中 `taskNames` 是任务，可同时执行多个任务，`options` 是可选参数。

说明：从 hvigorw 5.18.4 版本开始，以下命令支持在任意路径下执行，其他 hvigorw 命令需要在工程根目录下执行：`hvigorw -v`、`hvigorw --version`、`hvigorw version`、`hvigorw -h`、`hvigorw --help`。

## 查询命令

| 参数 | 说明 |
| --- | --- |
| `-h`, `--help` | 打印 hvigorw 的命令帮助信息。 |
| `-v`, `--version`, `version` | 打印 hvigorw 版本信息。 |

## 编译构建任务

| 任务 | 说明 |
| --- | --- |
| `clean` | 清理构建产物 build 目录。 |
| `collectCoverage` | 基于打点数据生成覆盖率统计报表。 |
| `assembleHap` | 构建 Hap 应用。 |
| `assembleApp` | 构建 App 应用。 |
| `assembleHsp` | 构建 Hsp 包。 |
| `assembleHar` | 构建 Har 包。 |

### 编译构建常用扩展参数

| 参数 | 说明 |
| --- | --- |
| `-p buildMode={debug \| release}` | 采用 debug/release 模式进行编译构建。缺省时：构建 Hap/Hsp/Har 时为 debug 模式，构建 App 时为 release 模式。 |
| `-p debuggable=true/false` | 该配置会覆盖构建模式中对应的 buildOption 中的 debuggable 配置。 |
| `-p product={ProductName}` | 指定 product 进行编译，编译 product 下配置的 module target。缺省时：默认为 `default`。 |
| `-p module={ModuleName}@{TargetName}` | 指定模块及 target 进行编译，可指定多个相同类型的模块进行编译，以逗号隔开；TargetName 不指定时默认为 `default`。**限制：此参数需要与 `--mode module` 参数搭配使用。** 缺省时：执行 AssembleHap 任务会编译工程下所有模块，默认指定 target 为 default。 |
| `-p ohos-test-coverage={true \| false}` | 执行测试框架代码覆盖率插桩编译。 |
| `-p coverage={true \| false}` | 是否生成覆盖率报告。 |
| `-p parameterFile=param.json/json5` | 设置 oh-package.json5 文件的参数配置文件。 |
| `-p buildVersion=1` | 设置构建版本号。**从 hvigorw 6.23.3 版本开始支持。** |

### 构建命令示例

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

## 测试命令

| 命令行 | 说明 |
| --- | --- |
| `hvigorw onDeviceTest -p module={moduleName} -p coverage={true \| false} -p scope={suiteName}#{methodName} -p ohos-debug-asan={true\|false}` | 通过命令行方式执行 Instrument Test（设备测试）。`module`：执行测试的模块，缺省默认执行所有模块的用例。`coverage`：是否需要覆盖率报告，缺省默认为 true。`scope`：格式为 `{suiteName}#{methodName}` 或 `{suiteName}`，分别表示测试用例级别或测试套件级别的测试，缺省默认执行当前模块的所有用例。`ohos-debug-asan`：是否启用 ASan 检测，缺省默认为 false。**从 hvigorw 5.19.0 版本开始支持。** 多个 module 和 scope 之间用逗号隔开。 |
| `hvigorw test -p module={moduleName} -p coverage={true \| false} -p scope={suiteName}#{methodName}` | 通过命令行方式执行 Local Test。**暂不支持在 Linux 上执行该命令。** |

### 测试产物路径

- **onDeviceTest 覆盖率测试报告路径**：`<module-path>/.test/default/outputs/ohosTest/reports`
- **onDeviceTest 测试结果文件**：`path_to_project/module_name/.test/default/intermediates/ohosTest/coverage_data/test_result.txt`
- **onDeviceTest ASan 日志路径**：`<module-path>/.test/default/intermediates/ohosTest/coverage_data`
- **Local Test 覆盖率测试结果文件**：`<module-path>/.test/default/outputs/test/reports`
- **Local Test 测试结果文件**：`path_to_project/module_name/.test/default/intermediates/test/coverage_data/test_result.txt`

## 日志参数

| 参数 | 说明 |
| --- | --- |
| `-e`, `--error` | 设置 hvigor 的日志级别为 error。 |
| `-w`, `--warn` | 设置 Hvigor 的日志级别为 warn。 |
| `-i`, `--info` | 设置 Hvigor 的日志级别为 info。 |
| `-d`, `--debug` | 设置 Hvigor 的日志级别为 debug。 |
| `--stacktrace`, `--no-stacktrace` | Hvigor 默认关闭打印所有异常的堆栈信息，如需开启在命令行后添加 `--stacktrace`。 |

## 可视化参数

| 参数 | 说明 |
| --- | --- |
| `--analyze=normal` | 在 DevEco Studio 中开启 Build Analyzer 构建分析，设置为普通模式。 |
| `--config properties.hvigor.analyzeHtml=true` | 在工程的 `.hvigor/report` 目录下生成构建可视化 html 文件。 |
| `--analyze=false` | 不启用 Build Analyzer 构建分析。 |
| `--analyze=advanced` | 启用 Build Analyzer 构建分析，并设置为进阶模式。 |
| `--analyze=ultrafine` | 启用 Build Analyzer 构建分析，并设置为超精细化模式。**从 hvigorw 6.0.0 版本开始支持。** |

## daemon 参数

| 参数 | 说明 |
| --- | --- |
| `--daemon` | 启用守护进程。 |
| `--no-daemon` | Hvigor 默认启用守护进程，如需关闭，可在命令行后添加该选项。**命令行模式下推荐使用此参数。** |
| `--stop-daemon` | 关闭当前工程的守护进程。 |
| `--stop-daemon-all` | 关闭所有工程的守护进程。 |
| `--status-daemon` | 查询当前环境中所有的 Hvigor 守护进程信息。 |
| `--max-old-space-size=12345` | 设置守护进程最大的老生代内存大小为 12345MB。 |
| `--max-semi-space-size=32` | 设置守护进程新生代最大的半空间大小为 32MB。**从 hvigorw 5.18.4 版本开始支持。** |

## 性能/内存参数

| 参数 | 说明 |
| --- | --- |
| `--parallel`, `--no-parallel` | Hvigor 默认开启并行构建能力，如需关闭在命令行后添加 `--no-parallel`。 |
| `--incremental`, `--no-incremental` | Hvigor 默认开启增量构建能力，如需关闭在命令行后添加 `--no-incremental`。 |
| `--optimization-strategy=performance` | 设置构建模式为性能优先模式，可加快构建速度，但会占用更多内存。**从 hvigorw 5.19.2 版本开始支持。** |
| `--optimization-strategy=memory` | 设置构建模式为内存优先模式，可以减少编译内存占用，默认使用 memory。**从 hvigorw 5.19.2 版本开始支持。** |

## 公共命令

| 任务 | 说明 |
| --- | --- |
| `tasks` | 打印工程各模块包含的任务信息。 |
| `taskTree` | 打印工程各模块的任务依赖关系信息。 |
| `prune` | 清除 30 天内未使用的 Hvigor 缓存文件并从 pnpm 存储中删除未引用的包。 |
| `buildInfo` | 打印工程级或模块级 build-profile.json5 中的配置信息。**从 hvigorw 5.18.4 版本开始支持。** |

### buildInfo 命令扩展参数

| 参数 | 说明 |
| --- | --- |
| `-p module={ModuleName}` | 指定需要打印配置信息的模块名，不指定时会打印工程级的配置信息。 |
| `-p buildOption` | 命令包含此参数时会打印 buildOption 配置。 |
| `-p json` | 将输出结果以 json 格式展示。 |

## 其他命令

| 参数 | 说明 |
| --- | --- |
| `-s`, `--sync` | 处理并持久化 Hvigor 部分工程信息到工程 `./hvigor/outputs/sync/output.json` 中。 |
| `--syncNative` | 在 sync 阶段执行 syncNative，可替换 compileNative 任务执行，完成并行编译。 |
| `-m`, `--mode` | 在对应的目录执行相应的 task，例 `hvigorw clean -m project` 在工程目录下执行 build 目录清理。 |
| `--type-check`, `--no-type-check` | Hvigor 默认关闭工程中 hvigorfile.ts 的类型检查，如需开启，可在命令行后添加 `--type-check`。 |
| `--config`, `-c` | 指定 hvigor-config.json5 配置文件中的参数。`--config properties.key=value` 同 `-c properties.key=value`。 |
| `--watch` | 开启观察模式，主要用于预览和热加载场景。 |
| `--node-home <string>` | 指定 nodejs 路径。 |

## 非 daemon 模式修改 node 内存配置

如果在非 daemon 模式下需要修改 node 内存配置，可在 command-line-tools 的 `hvigor/bin/hvigorw` 文件中取消第 15 行的注释，并配置对应的数值：

```bash
NODE_OPTS="--max-old-space-size=10240"
```
