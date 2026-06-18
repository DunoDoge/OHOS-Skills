<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-command-line-codelinter -->
<!-- 抓取时间：2026-06-17 -->

# 代码检查工具（codelinter）

`codelinter` 同时支持使用命令行执行代码检查与修复，可将 codelinter 工具集成到门禁或持续集成环境中。

## 命令行格式

```
codelinter [options] [dir]
```

- `options`：可选配置，见下表。
- `dir`：待检查的工程根目录；为可选参数，如不指定，默认为当前上下文目录。

## 命令行配置

| 指令 | 说明 |
| --- | --- |
| `--config` / `-c <filepath>` | 指定执行 codelinter 检查的规则配置文件位置。 |
| `--fix` | 设置 codelinter 检查同时执行 QuickFix。 |
| `--format` / `-f` | 设置检查结果的输出格式。目前支持 `default`/`json`/`xml`/`html` 四种格式；不指定时，默认是 `default` 格式（文本格式）。 |
| `--output` / `-o <filepath>` | 指定检查结果保存位置，且命令行窗口不展示检查结果。支持使用相对/绝对路径。不使用 `--output` 指令时，检查结果默认会显示在命令行窗口中。 |
| `--version` / `-v` | 查看 codelinter 版本。 |
| `--product` / `-p <productName>` | 指定当前生效的 product。`<productName>` 为生效的 product 名称。 |
| `--incremental` / `-i` | 对 Git 工程中的增量文件（包含新增/修改/重命名的文件）执行 Code Linter 检查。 |
| `--language` / `-l <language>` | 设置 codelinter 语言为 `cn` 或 `en`。默认为 `en`。 |
| `--help` / `-h` | 查询 codelinter 命令行帮助。 |
| `--exit-on` / `-e <levels>` | 指定哪些告警级别需要返回非零退出码，告警级别包括：`error`、`warn` 和 `suggestion`。若需要指定多个告警级别，级别间需要用英文逗号分开。 |

### --exit-on 退出码计算方式

退出码的计算方式为：用一个 3 位的二进制数从高到低分别表示 `error`、`warn`、`suggestion` 告警级别。若在命令行中配置告警级别，并且代码检查结果中也包含该告警级别，则该二进制值为 1，否则均为 0。将二进制数转换为十进制数，则是退出码。

示例：
- 命令配置为 `--exit-on error`，代码检查结果包括 `error`、`warn`、`suggestion` 三类告警，则退出码的二进制数为 `100`，十进制数为 **4**。
- 命令配置为 `--exit-on error`，代码检查结果包括 `warn`、`suggestion` 两类告警，则退出码的二进制数为 `000`，十进制数为 **0**。

## 使用示例

### 在工程根目录下使用

1. 直接执行 `codelinter` 指令，根据默认 codelinter 检查规则对该工程中的 TS/ArkTS 文件进行代码检查：

```bash
codelinter
```

2. 指定 codelinter 检查所使用的 `code-linter.json5` 规则配置文件：

```bash
codelinter -c filepath
```

3. 根据指定规则配置文件执行 codelinter 检查，并对部分支持修复的告警信息进行自动修复：

```bash
codelinter -c filepath --fix
```

### 在非工程根目录下使用

1. 指定需要进行检查的工程目录或文件路径（支持同时配置多个文件/文件夹路径）：

```bash
codelinter dir [filepath] [dir1]
```

2. 在指定的工程目录下，根据指定的 codelinter 规则配置文件进行代码检查：

```bash
codelinter -c filepath dir
```

3. 对指定工程重新执行 codelinter 检查，并对部分支持修复的告警进行自动修复：

```bash
codelinter -c filepath dir --fix
```

### 指定输出格式与保存位置

1. 指定检查结果输出格式（以 json 格式为例），检查结果将在命令行窗口展示：

```bash
codelinter [dir] -f json
```

2. 指定代码检查输出格式及结果保存位置，此时将不在命令行窗口中打印检查结果：

```bash
codelinter [dir] -f json -o filepath2
```

## CI 场景常用命令

```bash
# 增量检查（仅检查 Git 中新增/修改/重命名的文件）
codelinter -i

# 指定规则配置文件 + json 输出 + 保存到文件 + error 级别返回非零退出码
codelinter -c code-linter.json5 -f json -o report.json --exit-on error
```
