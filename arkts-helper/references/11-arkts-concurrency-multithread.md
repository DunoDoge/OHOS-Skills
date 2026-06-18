# ArkTS 多线程并发与线程间通信

> **上游 URL**:
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/multithread-concurrency
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/interthread-communication
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/concurrency-overview
>
> **抓取时间**: 2026-06-18

---

# 第一部分：并发概述

## 1. 异步并发 vs 多线程并发

| 特性 | 异步并发 | 多线程并发 |
|------|----------|------------|
| 执行模型 | 单线程事件循环 | 多线程并行执行 |
| 线程数 | 1（主线程） | 多个线程 |
| 适用场景 | I/O 密集型、轻量任务 | CPU 密集型、大量计算 |
| 线程安全 | 无需考虑 | 需要考虑 |
| 开销 | 低 | 较高（线程创建、通信） |
| 实现方式 | Promise / async/await | TaskPool / Worker |
| 数据共享 | 天然安全 | 需要通信机制 |

## 2. 多线程并发模型

### 2.1 内存共享模型

传统多线程模型（如 Java、C++）采用内存共享模型：

- 多个线程共享同一块内存地址空间
- 通过锁、信号量等机制保证线程安全
- 容易出现死锁、竞态条件等问题

### 2.2 Actor 模型

HarmonyOS 的 ArkTS 多线程并发采用 **Actor 模型**：

- 每个线程拥有独立的内存空间
- 线程之间通过**消息传递**通信，不共享内存
- 天然避免数据竞争问题
- 每个线程是一个独立的 Actor，通过发送和接收消息交互

```
┌──────────┐    消息     ┌──────────┐
│  主线程   │ ────────→  │  Worker  │
│ (Actor1) │  ←──────── │ (Actor2) │
└──────────┘    结果     └──────────┘
```

> ArkTS 的 Actor 模型实现包括 TaskPool 和 Worker 两种方式。

---

# 第二部分：TaskPool

## 3. TaskPool 概述

TaskPool（任务池）是一个多线程运行框架，提供任务调度、负载均衡和自动扩缩容能力。开发者无需手动管理线程生命周期。

### 3.1 运作机制

```
┌─────────────────────────────────────────────┐
│                  TaskPool                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│  │ Worker1 │  │ Worker2 │  │ Worker3 │ ... │
│  └────┬────┘  └────┬────┘  └────┬────┘     │
│       │            │            │           │
│  ┌────┴────────────┴────────────┴────┐     │
│  │           任务调度器               │     │
│  └────────────────┬──────────────────┘     │
│                   │                         │
└───────────────────┼─────────────────────────┘
                    │
              ┌─────┴─────┐
              │  主线程    │
              │ 提交任务   │
              └───────────┘
```

- TaskPool 内部维护一个 Worker 线程池
- 任务提交后由调度器分配给空闲 Worker
- 支持任务优先级和取消
- 自动管理线程的创建和销毁

### 3.2 @Concurrent 装饰器

在 TaskPool 中执行的任务函数必须使用 `@Concurrent` 装饰器标注：

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function computeTask(input: number): number {
  // CPU 密集型计算
  let result = 0;
  for (let i = 0; i < input; i++) {
    result += Math.sqrt(i);
  }
  return result;
}
```

`@Concurrent` 装饰器的约束：

- 被装饰的函数不能是匿名函数或箭头函数
- 函数必须为顶层函数或模块级函数
- 函数参数和返回值必须是可序列化类型
- 函数内部不能访问主线程的局部变量

### 3.3 使用方法

#### 基本使用

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function heavyCompute(iterations: number): number {
  let result = 0;
  for (let i = 0; i < iterations; i++) {
    result += Math.sqrt(i);
  }
  return result;
}

async function runTask(): Promise<void> {
  // 创建任务
  let task = new taskpool.Task(heavyCompute, 1000000);

  try {
    // 执行任务
    let result = await taskpool.execute(task);
    console.info(`计算结果: ${result}`);
  } catch (error) {
    console.error(`任务执行失败: ${(error as Error).message}`);
  }
}
```

#### 带优先级的任务

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function processData(data: string): string {
  return data.toUpperCase();
}

async function runWithPriority(): Promise<void> {
  // 创建高优先级任务
  let highTask = new taskpool.Task(processData, 'important');
  let result1 = await taskpool.execute(highTask, taskpool.Priority.HIGH);

  // 创建低优先级任务
  let lowTask = new taskpool.Task(processData, 'background');
  let result2 = await taskpool.execute(lowTask, taskpool.Priority.LOW);
}
```

#### 取消任务

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function longRunningTask(): number {
  let result = 0;
  for (let i = 0; i < 10000000000; i++) {
    result += i;
  }
  return result;
}

async function runAndCancel(): Promise<void> {
  let task = new taskpool.Task(longRunningTask);

  // 执行任务
  let promise = taskpool.execute(task);

  // 延迟后取消
  setTimeout(() => {
    taskpool.cancel(task);
    console.info('任务已取消');
  }, 1000);

  try {
    let result = await promise;
  } catch (error) {
    console.error(`任务被取消或执行失败`);
  }
}
```

#### 批量执行

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function computeChunk(start: number, end: number): number {
  let result = 0;
  for (let i = start; i < end; i++) {
    result += Math.sqrt(i);
  }
  return result;
}

async function batchExecute(): Promise<number> {
  let chunkSize = 250000;
  let tasks: Array<taskpool.Task> = [];

  for (let i = 0; i < 4; i++) {
    let task = new taskpool.Task(computeChunk, i * chunkSize, (i + 1) * chunkSize);
    tasks.push(task);
  }

  // 并行执行所有任务
  let results = await Promise.all(
    tasks.map((task) => taskpool.execute(task) as Promise<number>)
  );

  // 汇总结果
  let total = results.reduce((sum: number, val: number) => sum + val, 0);
  return total;
}
```

### 3.4 扩缩容机制

TaskPool 根据任务负载自动调整线程池大小：

| 参数 | 说明 |
|------|------|
| 最小线程数 | 默认与 CPU 核心数相同，不低于 1 |
| 最大线程数 | 与 CPU 核心数相关 |
| 空闲超时 | 线程空闲超过一定时间后自动回收 |
| 扩容触发 | 任务队列中有待执行任务且当前线程数未达上限 |
| 缩容触发 | 线程空闲时间超过阈值 |

### 3.5 TaskPool 注意事项

1. **@Concurrent 函数限制**：不能是闭包、匿名函数或箭头函数
2. **参数序列化**：函数参数必须是可序列化类型（基本类型、ArrayBuffer、普通对象等）
3. **不能访问主线程变量**：@Concurrent 函数不能捕获主线程的局部变量
4. **任务函数不能是类方法**：必须是独立的顶层函数
5. **返回值限制**：返回值必须是可序列化类型
6. **任务数量**：避免一次性提交过多任务，防止内存溢出

---

# 第三部分：Worker

## 4. Worker 概述

Worker 是 ArkTS 提供的另一种多线程方案，基于 Web Worker 标准模型。开发者需要手动管理 Worker 的生命周期。

### 4.1 运作机制

```
┌──────────────────┐         ┌──────────────────┐
│     主线程        │  消息   │    Worker 线程    │
│                  │ ──────→ │                  │
│  postMessage()   │         │  onmessage       │
│  onmessage       │ ←────── │  postMessage()   │
│                  │  结果   │                  │
└──────────────────┘         └──────────────────┘
```

- Worker 运行在独立线程，拥有独立的执行上下文
- 主线程与 Worker 通过 `postMessage` / `onmessage` 通信
- Worker 不能直接操作 UI

### 4.2 创建注意事项

1. Worker 文件必须放在 `workers/` 目录下（或配置的 Worker 目录）
2. Worker 文件路径有特定规则
3. 每个 Worker 线程有独立的全局对象
4. Worker 线程中不能导入和使用 UI 相关模块

### 4.3 文件路径规则

```
项目结构：
src/main/ets/
├── entryability/
│   └── EntryAbility.ets
├── workers/
│   └── MyWorker.ets      ← Worker 文件
└── pages/
    └── Index.ets
```

创建 Worker 时的路径：

```typescript
// 在主线程中创建 Worker
import { worker } from '@kit.ArkTS';

// 路径相对于当前文件的路径
let myWorker = new worker.ThreadWorker('entry/ets/workers/MyWorker.ets');
```

### 4.4 生命周期

```
创建 → 运行 → (可接收/发送消息) → 终止
 │                                    ↑
 └── new ThreadWorker()    worker.terminate() / 主线程调用 terminate()
```

| 阶段 | 说明 |
|------|------|
| 创建 | `new worker.ThreadWorker(path)` 创建 Worker 实例 |
| 运行 | Worker 线程开始执行，可以接收和发送消息 |
| 终止 | 调用 `terminate()` 终止 Worker 线程 |

### 4.5 基本用法

#### 主线程代码

```typescript
import { worker } from '@kit.ArkTS';

// 创建 Worker
let myWorker = new worker.ThreadWorker('entry/ets/workers/MyWorker.ets');

// 接收 Worker 消息
myWorker.onmessage = (event: MessageEvents) => {
  console.info(`收到 Worker 结果: ${event.data}`);
};

// 接收 Worker 错误
myWorker.onerror = (event: ErrorEvent) => {
  console.error(`Worker 错误: ${event.message}`);
};

// 向 Worker 发送消息
myWorker.postMessage({ command: 'compute', data: 1000000 });

// 终止 Worker
// myWorker.terminate();
```

#### Worker 线程代码（MyWorker.ets）

```typescript
import { worker } from '@kit.ArkTS';

// 获取 Worker 线程上下文
let workerPort = worker.workerPort;

// 接收主线程消息
workerPort.onmessage = (event: MessageEvents) => {
  let data = event.data;
  console.info(`Worker 收到消息: ${JSON.stringify(data)}`);

  if (data.command === 'compute') {
    let result = heavyCompute(data.data);
    // 向主线程发送结果
    workerPort.postMessage({ result: result });
  }
};

// 错误处理
workerPort.onerror = (event: ErrorEvent) => {
  console.error(`Worker 内部错误: ${event.message}`);
};

function heavyCompute(iterations: number): number {
  let result = 0;
  for (let i = 0; i < iterations; i++) {
    result += Math.sqrt(i);
  }
  return result;
}
```

### 4.6 多级 Worker

Worker 支持嵌套创建，即 Worker 内部可以再创建 Worker：

```typescript
// 主线程 → Worker1 → Worker2

// Worker1 代码
import { worker } from '@kit.ArkTS';

let workerPort = worker.workerPort;

workerPort.onmessage = (event: MessageEvents) => {
  // 在 Worker1 中创建 Worker2
  let worker2 = new worker.ThreadWorker('entry/ets/workers/Worker2.ets');

  worker2.onmessage = (e: MessageEvents) => {
    // 将 Worker2 的结果转发给主线程
    workerPort.postMessage(e.data);
  };

  worker2.postMessage(event.data);
};
```

> **注意**：多级 Worker 会增加线程数量和通信开销，需谨慎使用。

---

# 第四部分：TaskPool vs Worker 对比

## 5. 实现特点对比

| 特性 | TaskPool | Worker |
|------|----------|--------|
| 线程管理 | 自动管理（创建、调度、销毁） | 手动管理 |
| 任务调度 | 自动负载均衡 | 手动分配 |
| 扩缩容 | 自动 | 不支持 |
| 生命周期 | 任务级别 | 开发者控制 |
| 通信方式 | 结构化克隆 / ArrayBuffer 转移 | 结构化克隆 / ArrayBuffer 转移 |
| 任务优先级 | 支持 | 不支持 |
| 任务取消 | 支持 | 需自行实现 |
| 多级嵌套 | 不支持 | 支持多级 Worker |
| 复杂度 | 低（简单 API） | 中（需管理生命周期） |
| 长期运行 | 不适合 | 适合 |

## 6. 适用场景对比

### 6.1 建议使用 TaskPool 的场景

- **独立计算任务**：图像处理、数据加密、JSON 解析等
- **批量并行任务**：将大任务拆分为多个子任务并行执行
- **短期任务**：执行时间较短、不需要持续运行的任务
- **简单场景**：不需要复杂的线程间交互

```typescript
// 示例：图像滤镜处理
import { taskpool } from '@kit.ArkTS';

@Concurrent
function applyFilter(pixelData: ArrayBuffer, width: number, height: number): ArrayBuffer {
  // 图像处理逻辑
  return processedData;
}

async function processImage(data: ArrayBuffer, w: number, h: number): Promise<ArrayBuffer> {
  let task = new taskpool.Task(applyFilter, data, w, h);
  return await taskpool.execute(task) as ArrayBuffer;
}
```

### 6.2 建议使用 Worker 的场景

- **长期运行任务**：后台持续运行的服务（如 WebSocket 长连接）
- **需要持续通信**：主线程与工作线程之间需要频繁双向通信
- **复杂状态管理**：工作线程需要维护复杂的状态
- **多级线程**：需要 Worker 嵌套的场景
- **后台常驻**：需要在后台持续监听或处理

```typescript
// 示例：后台 WebSocket 服务
import { worker } from '@kit.ArkTS';

let wsWorker = new worker.ThreadWorker('entry/ets/workers/WebSocketWorker.ets');

wsWorker.onmessage = (event: MessageEvents) => {
  // 接收来自 Worker 的消息
  let msg = event.data;
  updateUI(msg);
};

// 发送消息到 Worker
function sendMessage(data: string): void {
  wsWorker.postMessage({ type: 'send', payload: data });
}
```

---

# 第五部分：线程间通信

## 7. 通信机制概述

ArkTS 多线程间通信支持以下方式：

| 通信方式 | 机制 | 适用场景 | 性能 |
|----------|------|----------|------|
| Structured Clone | 结构化克隆算法 | 传递普通对象 | 中（需要拷贝） |
| ArrayBuffer 转移 | 所有权转移 | 传递大二进制数据 | 高（零拷贝） |
| SharedArrayBuffer | 共享内存 | 高频数据交换 | 高（直接访问） |
| Sendable 引用传递 | 引用传递 | Sendable 对象共享 | 高（零拷贝） |

## 8. Structured Clone 算法

### 8.1 概述

Structured Clone 是 ArkTS 线程间通信的默认算法，通过深拷贝将数据从一个线程复制到另一个线程。

### 8.2 支持的数据类型

| 类型 | 说明 |
|------|------|
| 基本类型 | number, string, boolean, null, undefined |
| Date | 日期对象 |
| RegExp | 正则表达式 |
| ArrayBuffer | 二进制缓冲区（会被复制） |
| Array | 数组 |
| Object | 普通对象 |
| Map, Set | 集合类型 |
| TypedArray | 类型化数组视图 |

### 8.3 不支持的类型

| 类型 | 原因 |
|------|------|
| Function | 函数无法跨线程 |
| Symbol | 不可克隆 |
| DOM 元素 | 绑定到特定线程 |
| 带循环引用的对象 | 会导致无限递归 |

### 8.4 代码示例

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function processConfig(config: Record<string, Object>): string {
  // config 是通过 Structured Clone 传递的副本
  return JSON.stringify(config);
}

async function run(): Promise<void> {
  let config = {
    host: 'example.com',
    port: 8080,
    features: ['A', 'B', 'C']
  };

  let task = new taskpool.Task(processConfig, config);
  let result = await taskpool.execute(task) as string;
  console.info(result);
}
```

## 9. ArrayBuffer 转移

### 9.1 概述

ArrayBuffer 转移（Transfer）是一种零拷贝的数据传递方式。转移后，原始线程中的 ArrayBuffer 变为不可用（detached），接收线程获得完全所有权。

### 9.2 适用场景

- 传递大型二进制数据（图像、音视频帧等）
- 避免大数据拷贝的性能开销
- 数据只需要在一个线程中使用

### 9.3 代码示例

#### TaskPool 中使用 ArrayBuffer 转移

```typescript
import { taskpool } from '@kit.ArkTS';

@Concurrent
function processImageData(data: ArrayBuffer): ArrayBuffer {
  // 处理图像数据
  let view = new Uint8Array(data);
  // ... 图像处理逻辑
  return data.buffer;
}

async function transferArrayBuffer(): Promise<void> {
  let imageData = new ArrayBuffer(1024 * 1024); // 1MB 图像数据

  // 使用 transferList 传递 ArrayBuffer（零拷贝转移）
  let task = new taskpool.Task(processImageData, imageData);
  let result = await taskpool.execute(task, taskpool.Priority.DEFAULT, imageData) as ArrayBuffer;

  // 转移后 imageData 已 detached，不能再使用
  // console.info(imageData.byteLength); // 0 (detached)

  // result 是新的 ArrayBuffer
  console.info(`处理结果大小: ${result.byteLength}`);
}
```

#### Worker 中使用 ArrayBuffer 转移

```typescript
// 主线程
import { worker } from '@kit.ArkTS';

let myWorker = new worker.ThreadWorker('entry/ets/workers/MyWorker.ets');

let largeData = new ArrayBuffer(1024 * 1024);

// 使用 transferList 传递
myWorker.postMessage(largeData, [largeData]);

// 转移后 largeData 已 detached
```

```typescript
// Worker 线程
import { worker } from '@kit.ArkTS';

let workerPort = worker.workerPort;

workerPort.onmessage = (event: MessageEvents) => {
  let data = event.data as ArrayBuffer;
  // 处理数据...

  // 转移回主线程
  workerPort.postMessage(data, [data]);
};
```

## 10. SharedArrayBuffer 共享

### 10.1 概述

SharedArrayBuffer 允许多个线程共享同一块内存，无需拷贝或转移。所有线程可以直接读写同一块内存区域。

### 10.2 适用场景

- 高频数据交换
- 生产者-消费者模式
- 需要多个线程同时访问同一数据

### 10.3 同步机制

由于多线程共享内存，需要使用 `Atomics` 操作保证原子性：

| Atomics 方法 | 说明 |
|--------------|------|
| `Atomics.load(typedArray, index)` | 原子读取 |
| `Atomics.store(typedArray, index, value)` | 原子写入 |
| `Atomics.add(typedArray, index, value)` | 原子加 |
| `Atomics.sub(typedArray, index, value)` | 原子减 |
| `Atomics.compareExchange(typedArray, index, expected, replacement)` | 原子比较交换 |

### 10.4 代码示例

```typescript
import { worker } from '@kit.ArkTS';

// 创建 SharedArrayBuffer
let sharedBuffer = new SharedArrayBuffer(4 * 1024); // 4KB 共享内存
let sharedArray = new Int32Array(sharedBuffer);

// 初始化数据
Atomics.store(sharedArray, 0, 0); // 计数器

let myWorker = new worker.ThreadWorker('entry/ets/workers/CounterWorker.ets');

// 传递 SharedArrayBuffer（不是转移，是共享）
myWorker.postMessage({ buffer: sharedBuffer });

// 主线程也可以读写
setInterval(() => {
  let count = Atomics.load(sharedArray, 0);
  console.info(`当前计数: ${count}`);
}, 1000);
```

```typescript
// Worker 线程 (CounterWorker.ets)
import { worker } from '@kit.ArkTS';

let workerPort = worker.workerPort;

workerPort.onmessage = (event: MessageEvents) => {
  let sharedBuffer = event.data.buffer as SharedArrayBuffer;
  let sharedArray = new Int32Array(sharedBuffer);

  // 原子递增
  setInterval(() => {
    Atomics.add(sharedArray, 0, 1);
  }, 100);
};
```

## 11. Sendable 对象引用传递

### 11.1 概述

Sendable 是 ArkTS 提供的一种跨线程引用传递机制。标记为 Sendable 的对象可以在多个线程间共享引用，无需拷贝。

### 11.2 @Sendable 装饰器

```typescript
import { lang } from '@kit.ArkTS';

@lang.Sendable
class SharedData {
  name: string = '';
  value: number = 0;

  constructor(name: string, value: number) {
    this.name = name;
    this.value = value;
  }
}
```

### 11.3 代码示例

```typescript
import { taskpool } from '@kit.ArkTS';
import { lang } from '@kit.ArkTS';

@lang.Sendable
class ImageConfig {
  width: number = 0;
  height: number = 0;
  format: string = '';

  constructor(width: number, height: number, format: string) {
    this.width = width;
    this.height = height;
    this.format = format;
  }
}

@Concurrent
function processWithConfig(config: ImageConfig): string {
  // 直接引用传递，无需拷贝
  return `处理 ${config.width}x${config.height} ${config.format} 图像`;
}

async function runWithSendable(): Promise<void> {
  let config = new ImageConfig(1920, 1080, 'PNG');

  let task = new taskpool.Task(processWithConfig, config);
  let result = await taskpool.execute(task) as string;
  console.info(result);
}
```

### 11.4 Sendable 使用约束

1. `@Sendable` 类的属性必须是基本类型或其他 Sendable 类型
2. `@Sendable` 类不能继承非 Sendable 类
3. Sendable 对象的修改需要注意线程安全
4. 适用于读多写少的共享数据场景

---

# 第六部分：并发注意事项

## 12. 通信方式选择指南

| 场景 | 推荐方式 | 原因 |
|------|----------|------|
| 小对象传递 | Structured Clone | 简单，自动深拷贝 |
| 大二进制数据单向传递 | ArrayBuffer 转移 | 零拷贝，性能高 |
| 多线程高频数据交换 | SharedArrayBuffer | 共享内存，无需拷贝 |
| 复杂对象共享 | Sendable 引用传递 | 零拷贝，类型安全 |

## 13. 并发安全注意事项

### 13.1 避免数据竞争

```typescript
// ❌ 错误：多线程同时修改共享数据
let sharedArray = new Int32Array(new SharedArrayBuffer(4));
// 线程1: sharedArray[0] += 1;  // 非原子操作
// 线程2: sharedArray[0] += 1;  // 可能丢失更新

// ✅ 正确：使用 Atomics 保证原子性
Atomics.add(sharedArray, 0, 1);
```

### 13.2 Worker 生命周期管理

```typescript
// ✅ 正确：在适当时机终止 Worker
let myWorker = new worker.ThreadWorker('entry/ets/workers/MyWorker.ets');

myWorker.onmessage = (event: MessageEvents) => {
  if (event.data.done) {
    myWorker.terminate(); // 任务完成后终止
  }
};

// ❌ 错误：忘记终止 Worker，导致内存泄漏
```

### 13.3 TaskPool 参数限制

```typescript
// ❌ 错误：传递不可序列化的参数
@Concurrent
function badTask(callback: Function): void { // Function 不可序列化
  callback();
}

// ✅ 正确：只传递可序列化的数据
@Concurrent
function goodTask(data: string): string {
  return data.toUpperCase();
}
```

### 13.4 线程数量控制

- TaskPool 有最大线程数限制，避免一次性提交过多任务
- Worker 每个实例占用一个线程，注意控制 Worker 数量
- 建议同时运行的 Worker 数量不超过 CPU 核心数

### 13.5 错误处理

```typescript
// TaskPool 错误处理
async function safeTaskPoolExecute(): Promise<void> {
  try {
    let task = new taskpool.Task(riskyFunction, arg1, arg2);
    let result = await taskpool.execute(task);
  } catch (error) {
    console.error(`TaskPool 任务失败: ${(error as Error).message}`);
  }
}

// Worker 错误处理
let myWorker = new worker.ThreadWorker('entry/ets/workers/MyWorker.ets');

myWorker.onerror = (event: ErrorEvent) => {
  console.error(`Worker 错误: ${event.message}`);
  console.error(`文件: ${event.filename}, 行: ${event.lineno}`);
  myWorker.terminate(); // 出错后终止
};
```

## 14. 通信方式性能对比

| 通信方式 | 数据大小 | 传递时间 | 内存占用 | 适用频率 |
|----------|----------|----------|----------|----------|
| Structured Clone | 小 | 快 | 双倍 | 低频 |
| Structured Clone | 大 | 慢 | 双倍 | 低频 |
| ArrayBuffer 转移 | 任意 | 极快 | 单倍 | 单次 |
| SharedArrayBuffer | 任意 | 极快 | 单倍 | 高频 |
| Sendable 引用 | 中 | 快 | 单倍 | 中频 |
