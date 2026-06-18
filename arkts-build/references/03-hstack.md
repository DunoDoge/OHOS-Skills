<!-- 上游：https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-command-line-hstack -->
<!-- 抓取时间：2026-06-17 -->

# 堆栈解析工具（hstack）

`hstack` 是为开发人员提供的用于将 release 应用混淆后的 crash 堆栈解析为源码对应堆栈的工具，支持 Windows、Mac、Linux 三个平台。

## 命令行格式

```
hstack [options]
```

## 命令行配置

| 指令 | 说明 |
| --- | --- |
| `-i` / `--input` | 可选，指定工程 crash 文件归档目录。 |
| `-c` / `--crash` | 可选，指定一条 crash 堆栈。 |
| `-o` / `--output` | 可选，指定解析结果输出目录（输入指定为 `-c` 时，`-o` 参数指定一个输出文件）。 |
| `-s` / `--sourcemapDir` | 可选，指定工程 sourceMap 文件归档目录。 |
| `--so` / `--soDir` | 可选，指定工程 shared object 文件归档目录。 |
| `-n` / `--nameObfuscation` | 可选，指定工程 nameCache 文件归档目录。 |
| `-v` / `--version` | 查看 hstack 版本。 |
| `-h` / `--help` | 查询 hstack 命令行帮助。 |

### 参数约束

- crash 文件归档目录（`-i`）与 crash 堆栈（`-c`）**必须且只能提供一项**。
- sourceMap（`-s`）与 shared object 文件归档目录（`--so`）**至少提供一项**。
- 如果需要对方法名进行解析还原，则需要**同时提供 sourceMap 与 nameCache 文件**。
- 路径参数不支持特殊字符：`` ~!@#$^&*=|{};,\s[]<>?~！@#￥……&*（）——|{}【】'；：。，、？ ``

## 环境配置

1. hstack 工具在 Command Line Tools 的 `bin` 目录下，需要[将 bin 目录配置到 PATH 变量中](./01-command-line-tools-overview.md)。
2. 本工具依赖 Node 环境，需要将 Node.js 配置到环境变量中。
3. 如果需要对 C++ 文件产生的异常进行解析，则需要将 SDK 中的 `native/llvm/bin` 目录配置到环境变量中，变量名设置为 `ADDR2LINE_PATH`。

## 使用示例

1. 将应用产生的 crash 文件归档到 crashDir 目录下（或者 `-c` 指定一条 crash 堆栈）。
2. 使用 `-o` 指定输出目录，当不指定时，会输出至 `-i` 指定的 crashDir 目录下（通过 `-c` 输入为 crash 堆栈时，可以使用 `-o` 指定一个输出文件，或不指定，直接将结果输出至控制台）。
3. 使用 `-s` 指定工程对应 sourceMap 文件归档目录（可选，与 shared object 文件归档目录至少提供一项）。
4. 使用 `--so` 指定 shared object 文件归档目录（可选，与 sourceMap 归档目录至少提供一项）。
5. 使用 `-n` 指定 nameCache 文件归档目录（可选，方法名还原需要）。

```bash
# 通过 -i 指定 crash 文件归档目录，并将解析结果输出至 outputDir 目录
hstack -i D:\crashDir -o D:\outputDir -s D:\sourcemapDir --so D:\soDir -n D:\nameCacheDir

# 通过 -c 指定一条堆栈，并将解析结果输出至 out.txt 文件
hstack -c "at anonymous (entry|entry|1.0.0|src/main/ets/pages/Index.ts:401:1)" -o D:\outputDir\out.txt -s D:\sourcemapDir --so D:\soDir -n D:\nameCacheDir
```

如果是指定 crash 文件归档目录，解析完成后，outputDir 目录下会生成对应的解析结果，文件以原始 crash 文件名加 `_` 前缀进行命名。crash 堆栈中的 C++ 日志以及 ArkTS 日志均已解析为源码对应的文件路径以及行列号。

## 构建 Release 时生成包含符号表的 so 文件

在构建 Release 应用时，so 文件默认不包含符号表信息。如果需要生成包含符号表的 so 文件，需要在工程的模块级 `build-profile.json5` 文件的 `buildOption` 属性中配置：

```json5
{
  "buildOption": {
    "externalNativeOptions": {
      "arguments": "-DCMAKE_BUILD_TYPE=RelWithDebInfo"
    }
  }
}
```

## 堆栈解析原理

release 应用 crash 堆栈中包含混淆后的方法名（或属性名）、路径信息以及混淆后的行列号信息：

- **方法名**：在配置相应混淆规则后会进行混淆处理（如 `callHarFunction` 被混淆为 `i`）。方法名混淆前后的映射关系保存在对应模块编译产物的 **nameCache 文件**中。
- **路径信息**：格式为 `引用方 entry-packageName|被引用方 packageName|version|源码相对路径`，其中 packageName 以及 version 保存在对应模块编译产物的 **sourceMap 文件**中。
- **行列号**：混淆前后的映射关系保存在对应模块编译产物的 **sourceMap 文件**中，可利用文件对应的 `mappings` 字段进行解析还原。

### 解析步骤

1. **根据路径信息找到引用方模块 sourceMap**：根据堆栈中的 `entry|har|1.0.0|src/...` 路径信息，在 entry 模块 sourceMap 文件中找到对应字段。
2. **利用 sourceMap 还原路径与行列号**：基于 sourceMap 的 `sources` 及 `mappings` 字段进行解析还原。如果 sourceMap 中包含 `package-info` 字段，可利用 package-info 中对应模块的 sourceMap 对该条堆栈进行二次解析。
3. **利用 nameCache 还原方法名**：在对应模块编译产物中的 nameCache 文件中，通过解析后的文件路径找到 `IdentifierCache` 与 `MemberMethodCache` 字段。格式为 `"源码方法名:该方法起始行号:该方法结束行号":"混淆后方法名"`。找到行号范围包含还原后行号的条目，得到源码对应方法名。
4. **整合结果**：将步骤 2 与步骤 3 所得结果进行整合，得到最终堆栈结果。

### 示例

混淆后的 crash 堆栈：

```
at har (entry|har|1.0.0|src/main/ets/components/mainpage/MainPage.js:58:58)
at i (entry|entry|1.0.0|src/main/ets/pages/Index.ts:71:71)
at anonymous (entry|entry|1.0.0|src/main/ets/pages/Index.ts:55:55)
```

解析还原后的堆栈：

```
at har (har/src/main/ets/components/mainpage/MainPage.ets:20:1)
at callHarFunction (entry/src/main/ets/pages/Index.ets:25:3)
at anonymous (entry/src/main/ets/pages/Index.ets:14:47)
```
