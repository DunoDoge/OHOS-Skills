---
name: arkts-build
description: Use when building, testing, signing, or deploying HarmonyOS / OpenHarmony apps via command line tools, or when configuring CI pipelines. Triggers include hvigorw, codelinter, hstack, ohpm, assembleHap, assembleApp, assembleHsp, assembleHar, onDeviceTest, buildMode, product, module target, --no-daemon, --mode module, hap-sign-tool, keytool, hdc file send, hdc shell bm install, hdc shell aa start, ohpm install, ohpm publish, ohpm config, code-linter.json5, sourceMap, nameCache, crash stack parsing, CI pipeline, signing, pipeline setup, or any topic under the HarmonyOS Command Line Tools documentation. Loads the offline command-line tools reference set so the agent can give real HarmonyOS commands instead of guessing from npm/gradle knowledge.
---

# arkts-build

The HarmonyOS command-line toolchain (Command Line Tools, including `codelinter`, `hstack`, `hvigorw`, `ohpm`, and SDK tools `hdc`/`aa`/`bm`, etc.) is **not the same** as community npm/gradle/Node tools:

- `hvigorw` task names (`assembleHap`/`assembleApp`/`assembleHsp`/`assembleHar`/`onDeviceTest`) and parameters (`-p product=`, `-p buildMode=`, `-p module=`, `--mode module`, `--no-daemon`) are HarmonyOS-specific — gradle experience does not apply.
- `ohpm` is similar to npm but uses different repository URLs (`https://ohpm.openharmony.cn/ohpm/`), `oh-package.json5`, `strict_ssl`, and other configuration options.
- `codelinter`'s `--exit-on` exit code calculation (binary bit combinations), `code-linter.json5` rule files, and `--incremental` incremental checks are HarmonyOS-specific.
- `hstack` requires sourceMap + nameCache + so archive directories to parse release obfuscated stacks — community sourcemap tools cannot handle HarmonyOS's `entry|har|1.0.0|src/...` path format.
- Signing uses `hap-sign-tool.jar` (ECDSA + .p12/.cer/.p7b), not jarsigner / apksigner.

This skill provides offline reference documents (8 docs + INDEX under `references/`) which are offline copies of Huawei's official "Command Line Tools" documentation series, serving as the **authoritative reference** for build/test/deploy tasks.

## When to Use This Skill

Follow this skill's workflow whenever any of the following conditions are met:

- The user requests **command-line builds** of HarmonyOS projects (`hvigorw`, `assembleHap`, `assembleApp`, `assembleHsp`, `assembleHar`, `clean`, building release/debug packages)
- The user requests **static code analysis** (`codelinter`, CI gates, `--exit-on`, `code-linter.json5`, incremental checks)
- The user requests **release crash stack parsing** (`hstack`, sourceMap, nameCache, so archiving, deobfuscation)
- The user requests **third-party dependency management** (`ohpm install`, `ohpm publish`, `ohpm config`, `oh-package.json5`, repository URL configuration)
- The user requests **CI pipeline setup** (environment configuration, building, signing, installing & running, offline pipelines)
- The user requests **testing** (`onDeviceTest`, `hvigorw test`, coverage, ASan)
- The user requests **signing/deployment** (`hap-sign-tool.jar`, `keytool`, .p12/.cer/.p7b, `hdc file send`, `hdc shell bm install`, `hdc shell aa start`)
- The user requests **emulator** command-line usage (Emulator, `hdc tconn`, gRPC remote service)
- The user mentions `--no-daemon`, `-p product=`, `-p buildMode=`, `-p module=`, `--mode module`, `-p coverage=`, or other hvigorw parameters
- The project root contains `oh-package.json5` / `build-profile.json5` / `hvigorw` / `hvigorfile.ts` or other HarmonyOS project markers, and the task is build/test/deploy rather than code authoring

Do not force this skill onto "pure ArkTS syntax/migration", "ArkTS compilation error fixes", or "NDK/C++ interop" scenarios — use the corresponding skills instead (see boundary below).

## Boundary with Other Skills

This skill covers **"how to invoke command-line tools"**, not **"how to modify code"**. When build tasks involve the following issues, cross-reference the corresponding skill:

| Issue Type | Cross-reference Skill | Boundary |
| --- | --- | --- |
| ArkTS syntax / migration / coding style | `arkts-helper` | This skill only covers build commands, not ArkTS syntax |
| ArkTS compilation errors (`arkts-no-*` rules, etc.) | `arkts-debug` | If a build failure is caused by code errors, use `arkts-debug` to fix the code first, then return to this skill to rebuild |
| NDK / C++ / Node-API interop | `arkts-ndk-dev` | This skill only covers "how to trigger native builds via hvigorw / syncNative / abiFilters in build-profile.json5" at the command-line level; CMake toolchain variables, .so linking, musl/libc++, and other C++ layer issues belong to `arkts-ndk-dev` |
| Tools / options / workflows not covered by offline docs | `harmony-fetch` | If the 8 offline docs in this skill are insufficient to answer a question (e.g., new CLI parameters, new ohpm behavior changes), use `harmony-fetch` to fetch the latest documentation from the Huawei developer portal |

## Workflow (Follow Strictly)

### 1. Read the Index First, Then Decide Which Doc to Load

Before any build/test/deploy task, **you must read** `references/INDEX.md` first. It provides the role of each of the 8 documents, reading paths by task type, and key command quick references — this prevents loading the entire reference directory into context.

### 2. Load the Corresponding Document by Task Type

| Task Type | Required Reading (under `references/`) |
| -------- | ------------------------------ |
| Tool acquisition / environment variable configuration | `01-command-line-tools-overview.md` |
| Code static analysis / CI gates | `02-codelinter.md` |
| Release crash stack parsing | `03-hstack.md` |
| **hvigorw build commands / build parameters** | `04-hvigorw.md` |
| ohpm install / publish / dependency management | `05-ohpm.md` |
| **CI pipeline setup / post-build signing, install & run** | `06-building-app.md` (+ `04-hvigorw.md`) |
| Device debugging commands (hdc/aa/bm, etc.) | `07-debugging-commands.md` (+ the "Running Applications" section in `06-building-app.md`) |
| Emulator usage | `08-emulator.md` |
| Testing (onDeviceTest / Local Test) | The "Test Commands" section in `04-hvigorw.md` |

When reading documents, prefer using `Grep`/`Read` with offset/limit to locate specific sections — do not read large files in their entirety at once.

### 3. Strictly Enforce Red Lines When Issuing Commands

Before writing or modifying build commands, self-check the following high-frequency red lines (detailed rules are subject to the original documentation):

- **CI builds must add `--no-daemon`**: Command-line mode (especially CI) recommends disabling the daemon process to avoid state residue
- **`-p module=` must be paired with `--mode module`**: The `-p module={ModuleName}@{TargetName}` parameter requires `--mode module` to take effect
- **Run `ohpm install` before building**: You need to run `ohpm install` in both the project root and each module directory to install project-level and module-level third-party dependencies
- **Release stack parsing requires sourceMap + nameCache**: `hstack`'s `-s` (sourceMap) and `--so` (shared object) require at least one; method name deobfuscation requires both sourceMap and nameCache
- **Signing trio: .p12 / .cer / .p7b**: Signing requires a key (.p12), digital certificate (.cer), and Profile (.p7b); HAP pushed to a device must carry signature information
- **Output path patterns**: Hap output is at `${PROJECT_PATH}/{moduleName}/build/{productName}/outputs/{targetName}/xxx.hap`; App output is at `${PROJECT_PATH}/build/outputs/{productName}/xxx.app`
- **Check version first with `hvigorw -v`**: `buildInfo` (5.18.4+), `ohos-debug-asan` (5.19.0+), `--optimization-strategy` (5.19.2+), `--analyze=ultrafine` (6.0.0+), `-p buildVersion=` (6.23.3+) and other commands have version requirements
- **Confirm OS for platform differences**: Environment variable configuration differs across Windows/macOS/Linux (PATH separators, Node path differences: Windows uses `tool/node`, Linux/macOS uses `tool/node/bin`) — confirm the user's OS before providing environment variable commands
- **Do not place project paths inside hidden directories**: Every level of the project path should not start with `.`, otherwise the build may package module code and configuration files as resources into the output

When uncertain, **search the original text in `references/04-hvigorw.md` or the relevant topic-specific document** before writing.

### 4. Cite the Source When Referencing Documents

When answering command/parameter questions, include a citation at the end of the response, e.g.:

> Per the "Common Extension Parameters for Build" section in `references/04-hvigorw.md` and the "Running Hvigor Commands for Build" example in `references/06-building-app.md`.

This allows users to quickly verify against the original text.

### 5. Do Not Skip or Replace This Skill's Checks

Even if the user's build request "looks like something gradle/npm can handle", in the HarmonyOS context you must verify commands against this skill before answering — do not assume gradle/npm knowledge can be directly applied.

## High-Frequency Command Quick Reference

| Scenario | Command |
| --- | --- |
| Clean build outputs | `hvigorw clean --no-daemon` |
| Build Hap (debug) | `hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon` |
| Build Hap (release) | `hvigorw assembleHap --mode module -p product=default -p buildMode=release --no-daemon` |
| Build App | `hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon` |
| Build Hsp | `hvigorw assembleHsp --mode module -p module=library@default -p product=default --no-daemon` |
| Build Har | `hvigorw assembleHar --mode module -p module=library1@default -p product=default --no-daemon` |
| Install dependencies | `ohpm install` / `ohpm install --all` |
| Publish har | `ohpm publish pkg.har` |
| Configure ohpm repository | `ohpm config set registry https://ohpm.openharmony.cn/ohpm/` |
| Code analysis | `codelinter` / `codelinter -c code-linter.json5 -f json -o report.json --exit-on error` |
| Incremental check | `codelinter -i` |
| Check and fix | `codelinter -c filepath --fix` |
| Stack parsing | `hstack -i D:\crashDir -o D:\outputDir -s D:\sourcemapDir --so D:\soDir -n D:\nameCacheDir` |
| On-device test | `hvigorw onDeviceTest -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}` |
| Local test | `hvigorw test -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}` |
| Push HAP | `hdc file send "xxx.hap" "data/local/tmp/xxx.hap"` |
| Install HAP | `hdc shell bm install -p "data/local/tmp/xxx.hap"` |
| Launch app | `hdc shell aa start -a EntryAbility -b com.example.myapplication -m entry` |
| Sign HAP | `java -jar hap-sign-tool.jar sign-app -keyAlias "demo_key" -signAlg "SHA256withECDSA" -mode "localSign" -appCertFile "/path/demo.cer" -profileFile "/path/demo.p7b" -inFile "/path/hap-unsigned.hap" -keystoreFile "/path/demo.p12" -outFile "/path/hap-signed.hap" -keyPwd "123456Abc" -keystorePwd "123456Abc"` |

## Directory Structure

```
arkts-build/
├── SKILL.md                                          # This file
└── references/
    ├── INDEX.md                                      # Must read first
    ├── 01-command-line-tools-overview.md             # Command Line Tools acquisition & env config
    ├── 02-codelinter.md                              # Code linter (codelinter)
    ├── 03-hstack.md                                  # Crash stack parser (hstack)
    ├── 04-hvigorw.md                                 # Command-line build tool (hvigorw)
    ├── 05-ohpm.md                                    # Third-party dependency manager (ohpm)
    ├── 06-building-app.md                            # CI pipeline setup
    ├── 07-debugging-commands.md                      # SDK CLI tools & debugging command index
    └── 08-emulator.md                                # Emulator tool
```

## Documentation Source & Maintenance

- Upstream: Huawei Developer official site "Documentation Center › Application Development › Command Line Tools" series, under `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/`:
  - `ide-commandline-get` (acquiring Command Line Tools)
  - `ide-command-line-codelinter` (codelinter)
  - `ide-command-line-hstack` (hstack)
  - `ide-hvigor-commandline` (hvigorw)
  - `ide-ohpm-cli` / `ide-ohpm-common-commands` (ohpm)
  - `ide-command-line-building-app` (CI pipeline setup)
  - `debugging-commands` (debugging commands)
  - `ide-commandline-emulator` (Emulator)
- Documents are offline snapshots taken on 2026-06-17; each document includes the upstream URL and fetch timestamp at the top.
- To update to the latest version, re-run the fetch (use `curl`/WebFetch from the upstream URLs to overwrite files in `references/`); if expanding the file list, also update `references/INDEX.md`.
- Command version differences are subject to the official documentation: commands and parameters for hvigorw / codelinter / ohpm may change with HarmonyOS version updates; if uncertain, first check the version with `hvigorw -v` / `codelinter -v` / `ohpm -v`.
