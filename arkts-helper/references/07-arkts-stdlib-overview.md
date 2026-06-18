# ArkTS 基础类库概述

> **上游 URL**: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-utils-overview
> **抓取时间**: 2026-06-18

---

## 1. 简介

ArkTS 基础类库是 HarmonyOS 为 ArkTS 语言提供的一套标准工具库，涵盖 XML 处理、二进制数据操作、容器数据结构、URL 解析、高精度计算和 JSON 扩展等能力。开发者可以通过 `@kit.ArkTS` 统一引入这些工具。

```typescript
import { xml, buffer, collections, url, decimal, json } from '@kit.ArkTS';
```

## 2. 能力范围

| 模块 | 功能说明 | 典型用途 |
|------|----------|----------|
| **XML** | XML 文档的生成、解析与转换 | 配置文件处理、SOAP/WebService 交互 |
| **Buffer / FastBuffer** | 二进制数据的创建、读写、复制与转换 | 网络协议解析、文件 I/O、图像数据处理 |
| **容器类库** | 线性与非线性容器数据结构 | 数据集合管理、算法实现 |
| **URL** | URL 字符串的解析与构造 | 网络请求参数处理、路由解析 |
| **Decimal（高精度浮点）** | 任意精度十进制浮点计算 | 金融计算、科学计算、避免浮点精度丢失 |
| **JSON 扩展** | 增强的 JSON 解析与序列化 | 大整数处理、嵌套引号解析、BigInt 序列化 |

## 3. XML 生成解析转换

### 3.1 XML 概述

ArkTS 提供 `@ohos.xml` 模块，支持：

- **XML 生成**：通过 `XmlSerializer` 将结构化数据序列化为 XML 字符串
- **XML 解析**：通过 `XmlPullParser` 将 XML 字符串解析为事件流
- **XML 转换**：XML 与 JavaScript 对象之间的相互转换

### 3.2 核心类

| 类名 | 用途 |
|------|------|
| `XmlSerializer` | 将数据序列化为 XML 格式 |
| `XmlPullParser` | 基于 SAX 模型解析 XML，以事件驱动方式读取 |

### 3.3 快速示例

```typescript
import { xml } from '@kit.ArkTS';

// XML 生成
let serializer = new xml.XmlSerializer();
serializer.startDocument('1.0', 'utf-8');
serializer.startElement('note');
serializer.setAttributes('priority', 'high');
serializer.addText('Hello World');
serializer.endElement();
serializer.endDocument();
console.info(serializer.getResult()); // 输出完整 XML 字符串

// XML 解析
let xmlStr = '<?xml version="1.0" encoding="utf-8"?><note priority="high">Hello World</note>';
let parser = new xml.XmlPullParser(xmlStr);
parser.parse((name: string, value: string) => {
  console.info(`name: ${name}, value: ${value}`);
  return true; // 返回 true 继续解析
});
```

> 详细的 XML 生成、解析与转换说明请参考 [08-arkts-xml-buffer-json.md](08-arkts-xml-buffer-json.md)。

## 4. 二进制 Buffer 与 FastBuffer

### 4.1 Buffer 概述

`Buffer` 类用于处理二进制数据，类似于 Node.js 的 Buffer，但针对 HarmonyOS 做了优化。`FastBuffer` 是 Buffer 的轻量级变体，在特定场景下具有更好的性能。

### 4.2 核心能力

| 能力 | Buffer | FastBuffer |
|------|--------|------------|
| 创建 | `Buffer.alloc()`, `Buffer.from()` | `FastBuffer.create()` |
| 读写 | 支持 int8/uint8/int16/.../float32/float64 | 支持 int8/uint8/int16/.../float32/float64 |
| 复制 | `copy()`, `slice()` | `copy()`, `slice()` |
| 转换 | `toString()`, `toJSON()` | `toString()`, `toJSON()` |

### 4.3 快速示例

```typescript
import { buffer } from '@kit.ArkTS';

// 创建 Buffer
let buf = buffer.Buffer.alloc(16);
buf.write('Hello', 0, 'utf-8');

// 从数组创建
let buf2 = buffer.Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]);
console.info(buf2.toString('utf-8')); // "Hello"

// 从字符串创建
let buf3 = buffer.Buffer.from('HarmonyOS', 'utf-8');
console.info(`length: ${buf3.length}`); // 8
```

> 详细的 Buffer 与 FastBuffer 说明请参考 [08-arkts-xml-buffer-json.md](08-arkts-xml-buffer-json.md)。

## 5. 多种容器类库

ArkTS 提供了丰富的容器类库，分为**线性容器**和**非线性容器**两大类。

### 5.1 线性容器

| 容器 | 底层结构 | 特点 |
|------|----------|------|
| ArrayList | 数组 | 随机访问快，尾部增删快 |
| List | 数组 | 类似 ArrayList，支持更多操作 |
| LinkedList | 双向链表 | 头尾增删快，随机访问慢 |
| Deque | 数组 | 双端队列，两端增删快 |
| Queue | 数组 | 先进先出队列 |
| Stack | 数组 | 后进先出栈 |
| Vector | 数组 | 类似 ArrayList，支持容量预分配 |

### 5.2 非线性容器

| 容器 | 底层结构 | 特点 |
|------|----------|------|
| HashMap | 哈希表 | 键值对，查找 O(1) |
| HashSet | 哈希表 | 不重复元素集合 |
| TreeMap | 红黑树 | 有序键值对，查找 O(log n) |
| TreeSet | 红黑树 | 有序不重复集合 |
| LightWeightMap | 数组+哈希 | 轻量键值对，内存占用更少 |
| LightWeightSet | 数组+哈希 | 轻量不重复集合 |
| PlainArray | 数组 | 稀疏数组，整型键 |

> **注意**：所有容器类库均**非多线程安全**，多线程场景需自行加锁。

> 详细的容器类库说明请参考 [09-arkts-container-library.md](09-arkts-container-library.md)。

## 6. URL 字符串解析

### 6.1 概述

`@ohos.url` 模块提供了 URL 字符串的解析与构造能力，支持 URL 各组成部分的读写操作。

### 6.2 核心类

| 类名 | 用途 |
|------|------|
| `URL` | 解析和构造 URL |
| `URLSearchParams` | 处理 URL 查询字符串 |

### 6.3 快速示例

```typescript
import { url } from '@kit.ArkTS';

// 解析 URL
let u = new url.URL('https://example.com:8080/path?key=value#fragment');
console.info(`protocol: ${u.protocol}`);   // "https:"
console.info(`hostname: ${u.hostname}`);   // "example.com"
console.info(`port: ${u.port}`);           // "8080"
console.info(`pathname: ${u.pathname}`);   // "/path"
console.info(`hash: ${u.hash}`);           // "#fragment"

// 处理查询参数
let params = new url.URLSearchParams('key=value&name=test');
params.append('page', '1');
console.info(params.toString()); // "key=value&name=test&page=1"
console.info(params.get('key')); // "value"
params.delete('name');
```

## 7. 高精度浮点计算

### 7.1 概述

`decimal` 模块提供了任意精度的十进制浮点运算能力，解决了 JavaScript 原生 `number` 类型的精度问题（如 `0.1 + 0.2 !== 0.3`）。

### 7.2 核心类

| 类名 | 用途 |
|------|------|
| `Decimal` | 高精度十进制数 |

### 7.3 快速示例

```typescript
import { decimal } from '@kit.ArkTS';

// 解决浮点精度问题
let a = new decimal.Decimal('0.1');
let b = new decimal.Decimal('0.2');
let c = a.plus(b);
console.info(c.toString()); // "0.3"（精确结果）

// 大数运算
let bigNum = new decimal.Decimal('999999999999999999999999999999');
let result = bigNum.plus('1');
console.info(result.toString()); // "1000000000000000000000000000000"

// 设置精度和舍入模式
decimal.Decimal.set({ precision: 20, rounding: decimal.Decimal.Rounding.ROUND_HALF_UP });
let d = new decimal.Decimal('1').dividedBy('3');
console.info(d.toString()); // 保留20位精度
```

### 7.4 适用场景

- 金融计算（货币金额精确到分）
- 税费计算
- 科学计算
- 任何不允许浮点误差的场景

## 8. JSON 扩展库

### 8.1 概述

ArkTS 的 JSON 扩展库在标准 JSON API 基础上增加了以下能力：

- **大整数处理**：安全解析超出 JavaScript 安全整数范围的整数
- **BigInt 序列化**：支持 BigInt 类型的序列化与反序列化
- **嵌套引号解析**：正确处理 JSON 字符串中包含嵌套引号的情况
- **浮点数序列化**：精确序列化浮点数，避免精度丢失

### 8.2 核心 API

| API | 说明 |
|-----|------|
| `json.parse(text, reviver?)` | 解析 JSON 字符串，支持大整数 |
| `json.stringify(value, replacer?, space?)` | 序列化为 JSON 字符串，支持 BigInt |
| `json.has(key)` | 检查 JSON 对象是否包含指定键 |
| `json.remove(key)` | 移除 JSON 对象中的指定键 |

### 8.3 快速示例

```typescript
import { json } from '@kit.ArkTS';

// 大整数解析
let bigIntJson = '{"id": 9007199254740993}';
let obj = json.parse(bigIntJson);
console.info(obj.id.toString()); // 精确保存大整数

// BigInt 序列化
let data = { value: BigInt(12345678901234567890n) };
let str = json.stringify(data);
console.info(str); // 精确序列化 BigInt
```

> 详细的 JSON 扩展库说明请参考 [08-arkts-xml-buffer-json.md](08-arkts-xml-buffer-json.md)。

## 9. 模块引入方式汇总

```typescript
// 统一引入
import { xml, buffer, collections, url, decimal, json } from '@kit.ArkTS';

// 或按需引入
import { xml } from '@kit.ArkTS';
import { buffer } from '@kit.ArkTS';
import { collections } from '@kit.ArkTS';
import { url } from '@kit.ArkTS';
import { decimal } from '@kit.ArkTS';
import { json } from '@kit.ArkTS';
```

## 10. 相关参考

| 主题 | 文档 |
|------|------|
| XML / Buffer / JSON 详解 | [08-arkts-xml-buffer-json.md](08-arkts-xml-buffer-json.md) |
| 容器类库详解 | [09-arkts-container-library.md](09-arkts-container-library.md) |
| 异步并发 | [10-arkts-concurrency-async.md](10-arkts-concurrency-async.md) |
| 多线程并发 | [11-arkts-concurrency-multithread.md](11-arkts-concurrency-multithread.md) |
