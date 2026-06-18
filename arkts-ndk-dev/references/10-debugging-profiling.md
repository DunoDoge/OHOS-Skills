<!-- 上游 URL: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/debugging-profiling -->
<!-- 抓取时间: 2026-06-18 -->

# 调试与性能分析

## ASan（Address-Sanitizer）

ASan 是 C/C++ 内存错误检测工具，已集成在 DevEco Studio 中。

### 支持的检测类型

- 缓冲区溢出（堆、栈、全局变量）
- 释放后使用（Use-After-Free）
- 双重释放（Double-Free）
- 内存泄漏（Memory Leak）

### 使用方式

1. 在 DevEco Studio 中启用 ASan：Build → Enable Address Sanitizer
2. 运行应用并触发相关代码路径
3. 通过 FaultLog 查看检测到的错误信息

### ASan 错误查看

通过 DevEco Studio 的 FaultLog 面板查看 ASan 报告，包含：
- 错误类型（heap-buffer-overflow、use-after-free 等）
- 调用栈信息
- 内存分配/释放历史

## LLDB 调试器

### 概述

- 基于 LLVM 15.0.4 构建
- DevEco Studio 默认调试器
- 支持 C/C++ 和 ArkTS 混合调试

### 功能特性

| 功能 | 说明 |
|------|------|
| 断点 | 代码断点、条件断点、函数断点 |
| 变量检查 | 查看局部变量、全局变量、表达式值 |
| 内存操作 | 读取/写入内存、查看内存区域 |
| 线程控制 | 暂停、继续、单步执行、步过、步出 |
| 表达式求值 | 在断点处执行表达式 |
| 栈回溯 | 查看调用栈、切换栈帧 |

### 工具路径

| 工具 | 路径 | 说明 |
|------|------|------|
| lldb.exe | `{NDK}/native/llvm/bin/lldb.exe` | Windows 客户端 |
| lldb-server | 设备端 `/data/local/tmp/lldb-server` | 设备端调试服务 |
| 静态 lldb | `{NDK}/native/llvm/lib/clang/15.0.4/bin/{arch}/lldb` | 按架构分目录 |

### 本地调试步骤

通过 hdc 连接设备进行本地调试：

```bash
# 1. 推送 lldb-server 到设备
hdc file send lldb-server /data/local/tmp/
hdc shell chmod +x /data/local/tmp/lldb-server

# 2. 进入设备 shell
hdc shell

# 3. 启动 lldb-server
cd /data/local/tmp
./lldb-server platform --listen "*:1234" --server

# 4. 在主机端启动 lldb 客户端连接
lldb
(lldb) platform select remote-ohos
(lldb) platform connect connect://localhost:1234

# 5. 调试目标程序
(lldb) file /path/to/binary
(lldb) b main
(lldb) run
(lldb) continue
```

### 远程调试

#### Root 镜像调试

1. 关闭 SELinux：`setenforce 0`
2. 推送 lldb-server 到设备
3. 使用 `platform select remote-ohos` 连接

#### 用户镜像调试

推荐使用 DevEco Studio 进行调试，IDE 会自动处理 lldb-server 的部署和连接。

### 常用 LLDB 命令

#### 断点命令

```bash
# 设置断点
(lldb) breakpoint set --file main.cpp --line 42
(lldb) breakpoint set --name myFunction
(lldb) breakpoint set --file main.cpp --line 42 --condition "x > 10"

# 查看断点
(lldb) breakpoint list

# 删除断点
(lldb) breakpoint delete 1

# 禁用/启用断点
(lldb) breakpoint disable 1
(lldb) breakpoint enable 1
```

#### 观察点命令

```bash
# 设置观察点
(lldb) watchpoint set variable globalVar
(lldb) watchpoint set expression -- &myStruct.field

# 查看观察点
(lldb) watchpoint list
```

#### 表达式求值

```bash
# 执行表达式
(lldb) expression myVar
(lldb) expression -- myFunction()
(lldb) expression myObj.method()

# 修改变量值
(lldb) expression myVar = 42
```

#### 栈帧与变量

```bash
# 查看当前栈帧变量
(lldb) frame variable
(lldb) frame variable myVar

# 查看调用栈
(lldb) thread backtrace
(lldb) bt

# 切换栈帧
(lldb) frame select 2
```

#### 线程控制

```bash
# 继续执行
(lldb) continue

# 单步执行（进入函数）
(lldb) step
(lldb) s

# 单步执行（跳过函数）
(lldb) next
(lldb) n

# 步出当前函数
(lldb) finish

# 查看所有线程
(lldb) thread list
```

#### 寄存器与反汇编

```bash
# 查看寄存器
(lldb) register read
(lldb) register read r0 r1

# 反汇编
(lldb) disassemble --frame
(lldb) disassemble --name myFunction
```

### ⚠️ 重要说明

- **lldb-server 具有数字签名验证机制**，只有华为签名的版本才能在设备上正常运行，不可自行替换或重新编译 lldb-server。
- 在子线程中调试时，注意 `napi_env`、`napi_value` 等对象的线程绑定限制。
- 调试 Release 构建时，部分变量可能被优化掉，建议使用 Debug 构建进行调试。
