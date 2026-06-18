# ArkTS 异步并发

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/async-concurrency-overview
> **抓取时间**: 2026-06-18

---

## 1. 概述

ArkTS 的异步并发模型基于**事件循环**机制，通过 `Promise` 和 `async/await` 语法实现非阻塞的异步操作。异步并发适用于 I/O 密集型任务，不需要创建新线程，所有异步代码在主线程（宿主线程）上执行。

异步并发的核心特点：

- **单线程执行**：异步代码在调用线程上执行，不涉及线程切换
- **非阻塞**：通过事件循环机制，I/O 操作不会阻塞主线程
- **协作式调度**：通过 `await` 暂停和恢复函数执行

---

## 2. Promise

### 2.1 三种状态

Promise 对象代表一个异步操作的最终完成（或失败）及其结果值。一个 Promise 必然处于以下三种状态之一：

| 状态 | 说明 | 触发 |
|------|------|------|
| **pending**（待定） | 初始状态，既没有被兑现，也没有被拒绝 | Promise 刚创建时 |
| **fulfilled**（已兑现） | 操作成功完成 | 调用 `resolve()` |
| **rejected**（已拒绝） | 操作失败 | 调用 `reject()` |

状态转换规则：

```
pending → fulfilled（不可逆）
pending → rejected（不可逆）
```

> 一旦状态变更，就不可再改变。fulfilled 和 rejected 统称为 **settled**（已定型）。

### 2.2 创建 Promise

```typescript
// 基本创建
let promise = new Promise<string>((resolve: Function, reject: Function) => {
  // 异步操作
  setTimeout(() => {
    let success = true;
    if (success) {
      resolve('操作成功');
    } else {
      reject(new Error('操作失败'));
    }
  }, 1000);
});
```

#### 封装异步函数

```typescript
// 封装一个返回 Promise 的函数
function fetchData(url: string): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    // 模拟网络请求
    setTimeout(() => {
      if (url.length > 0) {
        resolve(`数据来自 ${url}`);
      } else {
        reject(new Error('URL 不能为空'));
      }
    }, 1000);
  });
}

// 使用
fetchData('https://example.com/api')
  .then((data: string) => {
    console.info(data); // "数据来自 https://example.com/api"
  })
  .catch((error: Error) => {
    console.error(error.message);
  });
```

#### 静态创建方法

```typescript
// Promise.resolve - 创建一个已兑现的 Promise
let resolved = Promise.resolve(42);

// Promise.reject - 创建一个已拒绝的 Promise
let rejected = Promise.reject(new Error('出错了'));
```

### 2.3 then / catch / finally

#### then

`then` 方法注册当 Promise 兑现时的回调函数，返回一个新的 Promise。

```typescript
promise.then(
  (value: string) => {
    // 成功回调
    console.info(value);
    return value.toUpperCase(); // 返回值会被包装为新的 Promise
  },
  (error: Error) => {
    // 可选的失败回调
    console.error(error);
  }
);
```

#### catch

`catch` 方法注册当 Promise 拒绝时的回调函数。

```typescript
promise
  .then((value: string) => {
    console.info(value);
  })
  .catch((error: Error) => {
    console.error(`捕获错误: ${error.message}`);
  });
```

#### finally

`finally` 方法注册无论 Promise 兑现还是拒绝都会执行的回调。

```typescript
promise
  .then((value: string) => {
    console.info(value);
  })
  .catch((error: Error) => {
    console.error(error);
  })
  .finally(() => {
    console.info('操作完成（无论成功或失败）');
    // 适合做清理工作，如关闭加载指示器
  });
```

### 2.4 链式调用

Promise 的 `then` 方法返回一个新的 Promise，因此可以链式调用，实现顺序异步操作。

```typescript
function step1(): Promise<number> {
  return new Promise<number>((resolve) => {
    setTimeout(() => resolve(1), 1000);
  });
}

function step2(input: number): Promise<number> {
  return new Promise<number>((resolve) => {
    setTimeout(() => resolve(input + 1), 1000);
  });
}

function step3(input: number): Promise<string> {
  return new Promise<string>((resolve) => {
    setTimeout(() => resolve(`结果: ${input}`), 1000);
  });
}

// 链式调用
step1()
  .then((result1: number) => {
    console.info(`步骤1: ${result1}`); // 1
    return step2(result1);
  })
  .then((result2: number) => {
    console.info(`步骤2: ${result2}`); // 2
    return step3(result2);
  })
  .then((result3: string) => {
    console.info(`步骤3: ${result3}`); // "结果: 2"
  })
  .catch((error: Error) => {
    console.error(`链中某步出错: ${error.message}`);
  });
```

### 2.5 Promise 组合方法

#### Promise.all

等待所有 Promise 都兑现后返回结果数组。任一 Promise 拒绝则整体拒绝。

```typescript
let p1 = Promise.resolve(1);
let p2 = new Promise<number>((resolve) => setTimeout(() => resolve(2), 1000));
let p3 = new Promise<number>((resolve) => setTimeout(() => resolve(3), 500));

Promise.all([p1, p2, p3])
  .then((values: Array<number>) => {
    console.info(`全部完成: ${values}`); // [1, 2, 3]
  })
  .catch((error: Error) => {
    console.error(`有一个失败: ${error}`);
  });
```

**适用场景**：多个独立异步操作需要全部完成后才继续。

#### Promise.race

返回最先 settled（兑现或拒绝）的 Promise 结果。

```typescript
let fast = new Promise<string>((resolve) => setTimeout(() => resolve('快'), 100));
let slow = new Promise<string>((resolve) => setTimeout(() => resolve('慢'), 1000));

Promise.race([fast, slow])
  .then((value: string) => {
    console.info(`最先完成: ${value}`); // "快"
  });
```

**适用场景**：请求超时控制、竞速请求。

```typescript
// 超时控制示例
function fetchWithTimeout(url: string, timeout: number): Promise<string> {
  let fetchPromise = new Promise<string>((resolve) => {
    setTimeout(() => resolve(`数据来自 ${url}`), 2000);
  });

  let timeoutPromise = new Promise<string>((_, reject) => {
    setTimeout(() => reject(new Error('请求超时')), timeout);
  });

  return Promise.race([fetchPromise, timeoutPromise]);
}
```

#### Promise.allSettled

等待所有 Promise 都 settled 后返回每个 Promise 的结果状态。

```typescript
let p1 = Promise.resolve('成功1');
let p2 = Promise.reject(new Error('失败2'));
let p3 = Promise.resolve('成功3');

Promise.allSettled([p1, p2, p3])
  .then((results: Array<PromiseSettledResult<string>>) => {
    for (let result of results) {
      if (result.status === 'fulfilled') {
        console.info(`成功: ${result.value}`);
      } else {
        console.error(`失败: ${result.reason}`);
      }
    }
    // 输出:
    // 成功: 成功1
    // 失败: Error: 失败2
    // 成功: 成功3
  });
```

**适用场景**：需要获取所有异步操作的结果，不论成功或失败。

#### Promise.any

返回最先兑现的 Promise 结果。所有 Promise 都拒绝时才拒绝。

```typescript
let p1 = Promise.reject(new Error('失败1'));
let p2 = new Promise<string>((resolve) => setTimeout(() => resolve('成功2'), 100));
let p3 = new Promise<string>((resolve) => setTimeout(() => resolve('成功3'), 200));

Promise.any([p1, p2, p3])
  .then((value: string) => {
    console.info(`最先成功: ${value}`); // "成功2"
  })
  .catch((error: AggregateError) => {
    console.error(`全部失败: ${error.errors}`);
  });
```

**适用场景**：多个备用服务，任一可用即可。

### 2.6 Promise 组合方法对比

| 方法 | 等待条件 | 成功条件 | 失败条件 | 返回值 |
|------|----------|----------|----------|--------|
| `Promise.all` | 全部 settled | 全部兑现 | 任一拒绝 | 值数组 |
| `Promise.race` | 首个 settled | 首个兑现 | 首个拒绝 | 首个值 |
| `Promise.allSettled` | 全部 settled | 永不拒绝 | 永不拒绝 | 结果对象数组 |
| `Promise.any` | 首个兑现或全部拒绝 | 首个兑现 | 全部拒绝 | 首个值 |

---

## 3. async / await

### 3.1 async 函数

`async` 关键字用于声明一个异步函数，该函数总是返回一个 Promise。

```typescript
// async 函数自动将返回值包装为 Promise
async function greet(name: string): Promise<string> {
  return `Hello, ${name}!`; // 等价于 return Promise.resolve(`Hello, ${name}!`)
}

// 调用
greet('World').then((msg: string) => {
  console.info(msg); // "Hello, World!"
});
```

### 3.2 await 关键字

`await` 关键字只能在 `async` 函数内使用，用于暂停函数执行直到 Promise settled。

```typescript
async function fetchUserData(userId: string): Promise<string> {
  // await 暂停执行，直到 Promise 兑现
  let data = await fetchData(userId);
  console.info(`获取到数据: ${data}`);
  return data;
}

async function fetchData(id: string): Promise<string> {
  return new Promise<string>((resolve) => {
    setTimeout(() => resolve(`用户${id}的数据`), 1000);
  });
}
```

### 3.3 错误处理 try / catch

使用 `try/catch` 处理 `await` 中的错误，比 `.catch()` 更直观。

```typescript
async function loadUser(userId: string): Promise<string | null> {
  try {
    let data = await fetchUserData(userId);
    let processed = await processData(data);
    return processed;
  } catch (error) {
    // 捕获链中任一 await 抛出的错误
    console.error(`加载用户失败: ${(error as Error).message}`);
    return null;
  } finally {
    console.info('加载操作完成');
  }
}

async function fetchUserData(id: string): Promise<string> {
  return new Promise<string>((resolve, reject) => {
    if (id === '') {
      reject(new Error('用户ID不能为空'));
    } else {
      resolve(`用户${id}的数据`);
    }
  });
}

async function processData(data: string): Promise<string> {
  return data.toUpperCase();
}
```

### 3.4 async/await 与 Promise 的关系

`async/await` 是 Promise 的语法糖，两者可以混用：

```typescript
// async/await 写法
async function fetchAll(): Promise<void> {
  try {
    let user = await fetchUser();
    let posts = await fetchPosts(user.id);
    let comments = await fetchComments(posts[0].id);
    console.info(comments);
  } catch (error) {
    console.error(error);
  }
}

// 等价的 Promise 链式写法
function fetchAllPromise(): Promise<void> {
  return fetchUser()
    .then((user) => fetchPosts(user.id))
    .then((posts) => fetchComments(posts[0].id))
    .then((comments) => console.info(comments))
    .catch((error) => console.error(error));
}
```

#### 并行执行多个异步操作

```typescript
// 错误：串行执行（慢）
async function sequential(): Promise<void> {
  let a = await fetchA(); // 等1秒
  let b = await fetchB(); // 再等1秒
  // 总共2秒
}

// 正确：并行执行（快）
async function parallel(): Promise<void> {
  let [a, b] = await Promise.all([fetchA(), fetchB()]);
  // 总共1秒
}
```

---

## 4. 异步并发适用场景

### 4.1 I/O 非阻塞

异步并发最适合 I/O 密集型操作，避免阻塞主线程：

```typescript
async function readAndProcessFile(path: string): Promise<string> {
  try {
    // 文件读取是 I/O 操作，不会阻塞主线程
    let content = await fs.readText(path);
    let result = processContent(content);
    return result;
  } catch (error) {
    console.error(`文件处理失败: ${(error as Error).message}`);
    return '';
  }
}
```

常见 I/O 场景：
- 网络请求（HTTP/RPC）
- 文件读写
- 数据库操作
- 设备传感器数据读取

### 4.2 轻量任务

不需要大量 CPU 计算的轻量任务：

```typescript
async function loadConfig(): Promise<Record<string, Object>> {
  let response = await fetch('/api/config');
  let config = await response.json();
  return config;
}
```

### 4.3 逻辑依赖清晰

当异步操作之间有明确的先后依赖关系时：

```typescript
async function checkout(orderId: string): Promise<string> {
  // 步骤1：验证订单
  let order = await validateOrder(orderId);
  // 步骤2：处理支付（依赖步骤1的结果）
  let payment = await processPayment(order);
  // 步骤3：确认订单（依赖步骤2的结果）
  let confirmation = await confirmOrder(payment);
  return confirmation;
}
```

---

## 5. 最佳实践

### 5.1 优先使用 async/await

`async/await` 比 `.then()` 链更易读、更易调试：

```typescript
// 推荐 ✅
async function loadData(): Promise<void> {
  try {
    let data = await fetchData();
    console.info(data);
  } catch (error) {
    console.error(error);
  }
}

// 不推荐 ❌（可读性差）
function loadData(): Promise<void> {
  return fetchData()
    .then((data) => {
      console.info(data);
    })
    .catch((error) => {
      console.error(error);
    });
}
```

### 5.2 无依赖的异步操作应并行执行

```typescript
// 推荐 ✅
async function loadDashboard(): Promise<void> {
  // 三个请求无依赖关系，应并行执行
  let [user, posts, notifications] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchNotifications()
  ]);
}

// 不推荐 ❌（串行执行，浪费时间）
async function loadDashboard(): Promise<void> {
  let user = await fetchUser();
  let posts = await fetchPosts();
  let notifications = await fetchNotifications();
}
```

### 5.3 始终处理错误

```typescript
// 推荐 ✅
async function safeOperation(): Promise<string | null> {
  try {
    let result = await riskyOperation();
    return result;
  } catch (error) {
    console.error(`操作失败: ${(error as Error).message}`);
    return null; // 优雅降级
  }
}

// 不推荐 ❌（未处理拒绝，可能导致未捕获的 Promise 拒绝）
async function unsafeOperation(): Promise<string> {
  let result = await riskyOperation(); // 可能抛出异常
  return result;
}
```

### 5.4 避免在循环中串行 await

```typescript
// 不推荐 ❌（串行执行，总时间 = 单次时间 × 数量）
async function processAll(items: string[]): Promise<void> {
  for (let item of items) {
    await processItem(item); // 每次等待完成
  }
}

// 推荐 ✅（并行执行）
async function processAll(items: string[]): Promise<void> {
  await Promise.all(items.map((item) => processItem(item)));
}

// 推荐 ✅（限制并发数）
async function processAllWithLimit(items: string[], limit: number): Promise<void> {
  let executing: Array<Promise<void>> = [];
  for (let item of items) {
    let p = processItem(item);
    executing.push(p);
    if (executing.length >= limit) {
      await Promise.race(executing);
      executing = executing.filter((e) => e !== p);
    }
  }
  await Promise.all(executing);
}
```

### 5.5 不要在不需要时创建 Promise

```typescript
// 不推荐 ❌（多余的 Promise 包装）
async function getData(): Promise<string> {
  return new Promise((resolve) => {
    resolve('data'); // 同步值不需要 Promise 包装
  });
}

// 推荐 ✅
async function getData(): Promise<string> {
  return 'data';
}
```

### 5.6 CPU 密集型任务不应使用异步并发

```typescript
// 不推荐 ❌（CPU 密集型任务会阻塞主线程）
async function heavyComputation(): Promise<number> {
  let result = 0;
  for (let i = 0; i < 100000000; i++) {
    result += Math.sqrt(i);
  }
  return result; // 仍然阻塞主线程！
}

// 推荐 ✅（使用 TaskPool 在子线程执行）
import { taskpool } from '@kit.ArkTS';

@Concurrent
function heavyComputation(): number {
  let result = 0;
  for (let i = 0; i < 100000000; i++) {
    result += Math.sqrt(i);
  }
  return result;
}

async function runHeavyTask(): Promise<number> {
  let task = new taskpool.Task(heavyComputation);
  return await taskpool.execute(task);
}
```

> CPU 密集型任务请参考 [11-arkts-concurrency-multithread.md](11-arkts-concurrency-multithread.md) 使用多线程并发。
