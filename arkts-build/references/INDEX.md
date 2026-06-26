<!-- Must read first -->
<!-- Command version differences: refer to the official documentation: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-commandline-get -->

# INDEX - arkts-build Reference Documentation

> **Must read first**: Before any arkts-build task, **read this file first**, then load the corresponding document based on the task type mapping table below.
>
> **Command version differences: refer to the official documentation**: Commands and parameters for tools like hvigorw / codelinter / ohpm may change with HarmonyOS version updates. This document is an offline snapshot taken on 2026-06-17; if uncertain about a command, first check the version with `hvigorw -v` / `codelinter -v` / `ohpm -v` and refer to the upstream official documentation.

## Document Roles

| File | Role |
| --- | --- |
| `01-command-line-tools-overview.md` | Command Line Tools acquisition, environment variable configuration (Windows/macOS/Linux), tool overview |
| `02-codelinter.md` | Code linter `codelinter` command-line parameters, rule configuration, incremental checks, QuickFix, exit codes, output formats |
| `03-hstack.md` | Release crash stack parsing tool `hstack` parameters, sourceMap/so/nameCache archiving, parsing principles and examples |
| `04-hvigorw.md` | Command-line build tool `hvigorw` tasks, extension parameters, daemon, logging, visualization, performance switches, test commands |
| `05-ohpm.md` | Third-party dependency management tool `ohpm` common commands, oh-package.json5, repository configuration |
| `06-building-app.md` | Full CI pipeline setup (environment config → ohpm install → hvigorw build → signing → hdc install & run → example scripts) |
| `07-debugging-commands.md` | SDK command-line tool index (hdc/aa/bm/hilog/hidumper/hitrace/hiperf, etc.) |
| `08-emulator.md` | Emulator command-line usage, push-package debugging, Linux version, gRPC remote service |

## Reading Paths by Task Type

| Task Type | Required Reading (under `references/`) |
| --- | --- |
| Tool acquisition / environment variable configuration | `01-command-line-tools-overview.md` |
| Code static analysis / CI gates | `02-codelinter.md` |
| Release crash stack parsing | `03-hstack.md` |
| **hvigorw build commands / build parameters** | `04-hvigorw.md` |
| ohpm install / publish / dependency management | `05-ohpm.md` |
| **CI pipeline setup / post-build signing, install & run** | `06-building-app.md` (+ `04-hvigorw.md`) |
| Device debugging commands (hdc/aa/bm, etc.) | `07-debugging-commands.md` (+ the "Running Applications" section in `06-building-app.md`) |
| Emulator usage | `08-emulator.md` |
| Testing (onDeviceTest / Local Test) | The "Test Commands" section in `04-hvigorw.md` |

## Key Commands Quick Reference

```bash
# === hvigorw Build ===
hvigorw clean --no-daemon                                          # Clean build outputs
hvigorw assembleHap --mode module -p product=default -p buildMode=debug --no-daemon   # Build Hap
hvigorw assembleApp --mode project -p product=default -p buildMode=release --no-daemon # Build App
hvigorw assembleHsp --mode module -p module=library@default -p product=default --no-daemon  # Build Hsp
hvigorw assembleHar --mode module -p module=library1@default -p product=default --no-daemon  # Build Har

# === hvigorw Test ===
hvigorw onDeviceTest -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}  # On-device test
hvigorw test -p module={moduleName} -p coverage=true -p scope={suiteName}#{methodName}          # Local test

# === ohpm Dependency Management ===
ohpm install                          # Install dependencies
ohpm install --all                    # Install all dependencies (including modules)
ohpm publish pkg.har                  # Publish har
ohpm config set registry https://ohpm.openharmony.cn/ohpm/  # Configure repository
ohpm config set strict_ssl false      # Disable strict SSL

# === codelinter Code Analysis ===
codelinter                            # Default check
codelinter -c code-linter.json5 -f json -o report.json --exit-on error  # CI check
codelinter -i                         # Incremental check
codelinter -c filepath --fix          # Check and auto-fix

# === hstack Stack Parsing ===
hstack -i D:\crashDir -o D:\outputDir -s D:\sourcemapDir --so D:\soDir -n D:\nameCacheDir

# === hdc Install & Run ===
hdc file send "xxx.hap" "data/local/tmp/xxx.hap"     # Push HAP
hdc shell bm install -p "data/local/tmp/xxx.hap"     # Install HAP
hdc shell aa start -a EntryAbility -b com.example.myapplication -m entry  # Launch app

# === Signing ===
java -jar hap-sign-tool.jar sign-app -keyAlias "demo_key" -signAlg "SHA256withECDSA" -mode "localSign" \
  -appCertFile "/path/demo.cer" -profileFile "/path/demo.p7b" -inFile "/path/hap-unsigned.hap" \
  -keystoreFile "/path/demo.p12" -outFile "/path/hap-signed.hap" -keyPwd "123456Abc" -keystorePwd "123456Abc"
```

## Version-Specific Commands Quick Reference

The following commands have version requirements. Check with `hvigorw -v` before use:

| Command / Parameter | Minimum Version |
| --- | --- |
| `buildInfo` / `-v` run from any path / `--max-semi-space-size` | hvigorw 5.18.4 |
| `onDeviceTest` with `ohos-debug-asan` | hvigorw 5.19.0 |
| `--optimization-strategy` | hvigorw 5.19.2 |
| `--analyze=ultrafine` | hvigorw 6.0.0 |
| `-p buildVersion=` | hvigorw 6.23.3 |
