# XML 生成解析转换 / Buffer 与 FastBuffer / JSON 扩展库

> **上游 URL**:
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/xml-generation-parsing-conversion
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/buffer
> - https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkts-json
>
> **抓取时间**: 2026-06-18

---

# 第一部分：XML 生成、解析与转换

## 1. XML 概述

ArkTS 提供 `@ohos.xml` 模块，用于 XML 文档的生成、解析与转换。核心类包括：

| 类名 | 说明 |
|------|------|
| `XmlSerializer` | 将结构化数据序列化为 XML 字符串 |
| `XmlPullParser` | 基于 SAX 模型的事件驱动 XML 解析器 |

引入方式：

```typescript
import { xml } from '@kit.ArkTS';
```

## 2. XML 生成

### 2.1 基本流程

1. 创建 `XmlSerializer` 实例
2. 调用 `startDocument()` 开始文档
3. 使用 `startElement()` / `endElement()` 构建元素层级
4. 使用 `setAttributes()` 设置属性
5. 使用 `addText()` 添加文本内容
6. 调用 `endDocument()` 结束文档
7. 调用 `getResult()` 获取生成的 XML 字符串

### 2.2 代码示例

```typescript
import { xml } from '@kit.ArkTS';

// 基本XML生成
let serializer = new xml.XmlSerializer();
serializer.startDocument('1.0', 'utf-8');
serializer.startElement('bookstore');
serializer.setAttributes('category', 'fiction');

serializer.startElement('book');
serializer.setAttributes('id', '1');
serializer.setAttributes('lang', 'zh');

serializer.startElement('title');
serializer.addText('HarmonyOS开发指南');
serializer.endElement(); // title

serializer.startElement('author');
serializer.addText('张三');
serializer.endElement(); // author

serializer.startElement('price');
serializer.addText('99.00');
serializer.endElement(); // price

serializer.endElement(); // book
serializer.endElement(); // bookstore
serializer.endDocument();

let result = serializer.getResult();
console.info(result);
```

输出：

```xml
<?xml version="1.0" encoding="utf-8"?>
<bookstore category="fiction">
  <book id="1" lang="zh">
    <title>HarmonyOS开发指南</title>
    <author>张三</author>
    <price>99.00</price>
  </book>
</bookstore>
```

### 2.3 XmlSerializer 主要方法

| 方法 | 说明 |
|------|------|
| `startDocument(version, encoding)` | 开始 XML 文档 |
| `endDocument()` | 结束 XML 文档 |
| `startElement(name)` | 开始一个元素 |
| `endElement()` | 结束当前元素 |
| `setAttributes(name, value)` | 为当前元素设置属性 |
| `addText(text)` | 添加文本内容 |
| `addComment(comment)` | 添加注释 |
| `setNamespace(prefix, namespace)` | 设置命名空间 |
| `setCDATA(cdata)` | 添加 CDATA 段 |
| `getResult()` | 获取生成的 XML 字符串 |

## 3. XML 解析

### 3.1 解析模型

`XmlPullParser` 采用 **SAX（Simple API for XML）** 事件驱动模型，解析过程中会触发以下事件：

| 事件类型 | 说明 |
|----------|------|
| `START_DOCUMENT` | 文档开始 |
| `END_DOCUMENT` | 文档结束 |
| `START_TAG` | 开始标签 |
| `END_TAG` | 结束标签 |
| `TEXT` | 文本内容 |

### 3.2 代码示例

```typescript
import { xml } from '@kit.ArkTS';

let xmlStr = `<?xml version="1.0" encoding="utf-8"?>
<bookstore category="fiction">
  <book id="1">
    <title>HarmonyOS开发指南</title>
    <price>99.00</price>
  </book>
</bookstore>`;

let parser = new xml.XmlPullParser(xmlStr);

let books: Array<Record<string, string>> = [];
let currentBook: Record<string, string> = {};
let currentTag = '';

parser.parse((name: string, value: string): boolean => {
  switch (name) {
    case 'START_TAG':
      currentTag = value;
      if (value === 'book') {
        currentBook = {};
      }
      break;
    case 'TEXT':
      if (currentTag === 'title') {
        currentBook['title'] = value;
      } else if (currentTag === 'price') {
        currentBook['price'] = value;
      }
      break;
    case 'END_TAG':
      if (value === 'book') {
        books.push(currentBook);
      }
      currentTag = '';
      break;
  }
  return true; // 返回 true 继续解析，返回 false 停止
});

console.info(JSON.stringify(books));
// [{"title":"HarmonyOS开发指南","price":"99.00"}]
```

### 3.3 获取属性

```typescript
let parser = new xml.XmlPullParser(xmlStr);
parser.parse((name: string, value: string): boolean => {
  if (name === 'START_TAG' && value === 'book') {
    // 获取属性
    let attrs = parser.getAttributes();
    for (let attr of attrs) {
      console.info(`attr: ${attr.name} = ${attr.value}`);
    }
  }
  return true;
});
```

## 4. XML 转换

### 4.1 XML 转 JavaScript 对象

```typescript
import { xml } from '@kit.ArkTS';

let xmlStr = '<?xml version="1.0" encoding="utf-8"?><root><name>Test</name><value>42</value></root>';

// 使用 xml.convert 将 XML 转为对象
let options: xml.ConvertOptions = {
  supportDoctype: false,
  ignoreNameSpace: true,
  attributeNamePrefix: '@_',
  textNodeName: '#text',
  arrayNode: ['item'] // 指定哪些节点应解析为数组
};

let result = xml.convert(xmlStr, options);
console.info(JSON.stringify(result));
```

### 4.2 JavaScript 对象转 XML

```typescript
import { xml } from '@kit.ArkTS';

let obj = {
  root: {
    name: 'Test',
    value: '42',
    items: {
      item: ['A', 'B', 'C']
    }
  }
};

let serializer = new xml.XmlSerializer();
serializer.startDocument('1.0', 'utf-8');

// 递归将对象转为 XML
function objectToXml(obj: Record<string, Object>, serializer: xml.XmlSerializer): void {
  for (let key in obj) {
    let val = obj[key];
    if (typeof val === 'object' && val !== null) {
      serializer.startElement(key);
      objectToXml(val as Record<string, Object>, serializer);
      serializer.endElement();
    } else {
      serializer.startElement(key);
      serializer.addText(String(val));
      serializer.endElement();
    }
  }
}

objectToXml(obj, serializer);
serializer.endDocument();
console.info(serializer.getResult());
```

---

# 第二部分：Buffer 与 FastBuffer

## 5. Buffer 场景介绍

Buffer 用于处理二进制数据流，常见场景包括：

- 网络数据收发（TCP/UDP 报文解析）
- 文件读写（二进制文件操作）
- 图像/音视频数据处理
- 加密/解密运算
- 协议编解码

引入方式：

```typescript
import { buffer } from '@kit.ArkTS';
```

## 6. Buffer 创建

### 6.1 创建方式

| 方法 | 说明 |
|------|------|
| `Buffer.alloc(size, fill?, encoding?)` | 分配指定大小的 Buffer，可指定填充值 |
| `Buffer.allocUnsafe(size)` | 分配指定大小的 Buffer，不初始化（性能更优但内容不确定） |
| `Buffer.from(array)` | 从数组创建 |
| `Buffer.from(buffer)` | 从另一个 Buffer 创建 |
| `Buffer.from(string, encoding?)` | 从字符串创建 |
| `Buffer.from(arrayBuffer, byteOffset?, length?)` | 从 ArrayBuffer 创建视图 |

### 6.2 代码示例

```typescript
import { buffer } from '@kit.ArkTS';

// 方式1：分配指定大小
let buf1 = buffer.Buffer.alloc(10); // 10字节，填充0
let buf2 = buffer.Buffer.alloc(10, 'a'); // 10字节，填充 'a'

// 方式2：从数组创建
let buf3 = buffer.Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f]);

// 方式3：从字符串创建
let buf4 = buffer.Buffer.from('Hello HarmonyOS', 'utf-8');

// 方式4：从 ArrayBuffer 创建
let ab = new ArrayBuffer(8);
let buf5 = buffer.Buffer.from(ab, 0, 8);

console.info(`buf3: ${buf3.toString()}`); // "Hello"
console.info(`buf4 length: ${buf4.length}`); // 15
```

## 7. Buffer 读写

### 7.1 写入数据

```typescript
import { buffer } from '@kit.ArkTS';

let buf = buffer.Buffer.alloc(16);

// 写入字符串
buf.write('Hello', 0, 'utf-8');

// 写入数值
buf.writeInt8(127, 5);     // 在偏移5写入int8
buf.writeUInt8(255, 6);    // 在偏移6写入uint8
buf.writeInt16LE(1000, 7); // 在偏移7写入int16（小端序）
buf.writeInt32BE(99999, 9); // 在偏移9写入int32（大端序）
buf.writeFloatLE(3.14, 13); // 在偏移13写入float32

console.info(buf.toString('hex'));
```

### 7.2 读取数据

```typescript
import { buffer } from '@kit.ArkTS';

let buf = buffer.Buffer.from([0x48, 0x65, 0x6c, 0x6c, 0x6f, 0x7f, 0xff]);

// 读取字符串
let str = buf.toString('utf-8', 0, 5);
console.info(str); // "Hello"

// 读取数值
let int8Val = buf.readInt8(5);    // 127
let uint8Val = buf.readUInt8(6);  // 255

console.info(`int8: ${int8Val}`);   // 127
console.info(`uint8: ${uint8Val}`); // 255
```

### 7.3 支持的读写方法

| 方法 | 说明 |
|------|------|
| `writeInt8(value, offset)` / `readInt8(offset)` | 8位有符号整数 |
| `writeUInt8(value, offset)` / `readUInt8(offset)` | 8位无符号整数 |
| `writeInt16LE/BE(value, offset)` / `readInt16LE/BE(offset)` | 16位有符号整数 |
| `writeUInt16LE/BE(value, offset)` / `readUInt16LE/BE(offset)` | 16位无符号整数 |
| `writeInt32LE/BE(value, offset)` / `readInt32LE/BE(offset)` | 32位有符号整数 |
| `writeUInt32LE/BE(value, offset)` / `readUInt32LE/BE(offset)` | 32位无符号整数 |
| `writeFloatLE/BE(value, offset)` / `readFloatLE/BE(offset)` | 32位浮点数 |
| `writeDoubleLE/BE(value, offset)` / `readDoubleLE/BE(offset)` | 64位浮点数 |
| `writeBigInt64LE/BE(value, offset)` / `readBigInt64LE/BE(offset)` | 64位大整数 |
| `writeBigUInt64LE/BE(value, offset)` / `readBigUInt64LE/BE(offset)` | 64位无符号大整数 |

## 8. Buffer 复制与转换

### 8.1 复制

```typescript
import { buffer } from '@kit.ArkTS';

let src = buffer.Buffer.from('Hello World');

// slice - 创建视图（与原 Buffer 共享内存）
let sliced = src.slice(0, 5);
console.info(sliced.toString()); // "Hello"

// copy - 复制数据到目标 Buffer
let dst = buffer.Buffer.alloc(5);
src.copy(dst, 0, 0, 5);
console.info(dst.toString()); // "Hello"

// subarray - 创建视图
let sub = src.subarray(6);
console.info(sub.toString()); // "World"
```

### 8.2 转换

```typescript
import { buffer } from '@kit.ArkTS';

let buf = buffer.Buffer.from('Hello');

// 转字符串
console.info(buf.toString('utf-8'));  // "Hello"
console.info(buf.toString('hex'));    // "48656c6c6f"
console.info(buf.toString('base64')); // "SGVsbG8="

// 转 JSON
console.info(JSON.stringify(buf.toJSON()));
// {"type":"Buffer","data":[72,101,108,108,111]}

// 转 ArrayBuffer
let ab: ArrayBuffer = buf.buffer;

// 比较
let buf2 = buffer.Buffer.from('Hello');
console.info(buf.compare(buf2)); // 0（相等）
```

## 9. FastBuffer

### 9.1 概述

`FastBuffer` 是 Buffer 的轻量级变体，在创建和访问方面具有更好的性能，适用于高频二进制数据操作场景。

### 9.2 创建

```typescript
import { buffer } from '@kit.ArkTS';

// 创建 FastBuffer
let fastBuf = buffer.FastBuffer.create(16);

// 从数组创建
let fastBuf2 = buffer.FastBuffer.from([1, 2, 3, 4, 5]);

// 从字符串创建
let fastBuf3 = buffer.FastBuffer.from('Hello', 'utf-8');
```

### 9.3 读写

```typescript
import { buffer } from '@kit.ArkTS';

let fastBuf = buffer.FastBuffer.create(16);

// 写入
fastBuf.writeInt8(100, 0);
fastBuf.writeUInt8(200, 1);
fastBuf.writeInt16LE(1000, 2);
fastBuf.writeInt32BE(99999, 4);

// 读取
let v1 = fastBuf.readInt8(0);     // 100
let v2 = fastBuf.readUInt8(1);    // 200
let v3 = fastBuf.readInt16LE(2);  // 1000
let v4 = fastBuf.readInt32BE(4);  // 99999
```

### 9.4 复制与转换

```typescript
import { buffer } from '@kit.ArkTS';

let fastBuf = buffer.FastBuffer.from('Hello World');

// 复制
let dst = buffer.FastBuffer.create(5);
fastBuf.copy(dst, 0, 0, 5);
console.info(dst.toString()); // "Hello"

// 切片
let sliced = fastBuf.slice(6);
console.info(sliced.toString()); // "World"

// 转换
console.info(fastBuf.toString('hex'));
console.info(JSON.stringify(fastBuf.toJSON()));
```

### 9.5 Buffer 与 FastBuffer 选择指南

| 场景 | 推荐 | 原因 |
|------|------|------|
| 通用二进制数据处理 | Buffer | 功能完整，兼容性好 |
| 高频创建/销毁 | FastBuffer | 创建性能更优 |
| 大量随机读写 | FastBuffer | 读写性能更优 |
| 需要与 ArrayBuffer 互操作 | Buffer | 更好的兼容性 |

---

# 第三部分：JSON 扩展库

## 10. JSON 扩展库概述

ArkTS 的 JSON 扩展库在标准 JSON API 基础上增强了以下能力：

- **大整数安全解析**：安全处理超出 JavaScript 安全整数范围（±2^53-1）的整数
- **BigInt 序列化/反序列化**：原生支持 BigInt 类型
- **嵌套引号解析**：正确处理 JSON 字符串中包含嵌套引号的场景
- **浮点数精确序列化**：避免浮点数序列化时的精度丢失

引入方式：

```typescript
import { json } from '@kit.ArkTS';
```

## 11. 核心 API

### 11.1 json.parse

```typescript
json.parse(text: string, reviver?: (key: string, value: Object) => Object): Object
```

解析 JSON 字符串为 JavaScript 对象。与标准 `JSON.parse` 相比，增强了对大整数的支持。

```typescript
import { json } from '@kit.ArkTS';

// 标准大整数解析
let result = json.parse('{"id": 9007199254740993, "name": "test"}');
console.info(result.id.toString()); // 精确保存大整数值

// 使用 reviver 函数
let data = json.parse('{"date": "2024-01-01"}', (key: string, value: Object) => {
  if (key === 'date') {
    return new Date(value as string);
  }
  return value;
});
```

### 11.2 json.stringify

```typescript
json.stringify(value: Object, replacer?: Object, space?: string | number): string
```

将 JavaScript 对象序列化为 JSON 字符串。增强了对 BigInt 的支持。

```typescript
import { json } from '@kit.ArkTS';

// BigInt 序列化
let obj = {
  id: BigInt(9007199254740993n),
  name: 'test'
};
let str = json.stringify(obj);
console.info(str); // {"id":9007199254740993,"name":"test"}

// 格式化输出
let formatted = json.stringify(obj, null, 2);
console.info(formatted);
// {
//   "id": 9007199254740993,
//   "name": "test"
// }
```

### 11.3 json.has

```typescript
json.has(key: string): boolean
```

检查 JSON 对象中是否包含指定的键。

```typescript
import { json } from '@kit.ArkTS';

let obj = json.parse('{"name": "test", "value": 42}');
console.info(json.has.call(obj, 'name'));  // true
console.info(json.has.call(obj, 'other')); // false
```

### 11.4 json.remove

```typescript
json.remove(key: string): boolean
```

移除 JSON 对象中的指定键，返回是否成功移除。

```typescript
import { json } from '@kit.ArkTS';

let obj = json.parse('{"name": "test", "value": 42}');
json.remove.call(obj, 'value');
console.info(JSON.stringify(obj)); // {"name":"test"}
```

## 12. 开发场景

### 12.1 场景一：解析嵌套引号

当 JSON 字符串中包含嵌套引号时，标准 `JSON.parse` 可能失败，ArkTS JSON 扩展库可以正确处理。

```typescript
import { json } from '@kit.ArkTS';

// 包含嵌套引号的 JSON
let jsonStr = '{"text": "He said \\"Hello World\\""}';
let result = json.parse(jsonStr);
console.info(result.text); // He said "Hello World"

// 多层嵌套引号
let complexStr = '{"msg": "Path: \\"C:\\\\Users\\\\test\\"" }';
let result2 = json.parse(complexStr);
console.info(result2.msg); // Path: "C:\Users\test"
```

### 12.2 场景二：大整数处理

```typescript
import { json } from '@kit.ArkTS';

// 超出安全整数范围的 ID
let jsonStr = '{"userId": 9007199254740993, "orderId": 123456789012345678901234}';
let result = json.parse(jsonStr);

// 精确保存大整数值
console.info(result.userId.toString());    // "9007199254740993"
console.info(result.orderId.toString());   // "123456789012345678901234"

// 序列化回 JSON 不会丢失精度
let output = json.stringify(result);
console.info(output); // 精确输出原始大整数
```

### 12.3 场景三：序列化 BigInt

```typescript
import { json } from '@kit.ArkTS';

// 在应用中使用 BigInt 进行精确计算
let account = {
  balance: BigInt('99999999999999999999'),
  userId: BigInt('9007199254740993'),
  name: 'user1'
};

// 序列化包含 BigInt 的对象
let jsonStr = json.stringify(account);
console.info(jsonStr);
// {"balance":99999999999999999999,"userId":9007199254740993,"name":"user1"}

// 反序列化还原 BigInt
let parsed = json.parse(jsonStr);
console.info(parsed.balance.toString()); // "99999999999999999999"
```

### 12.4 场景四：序列化浮点数

```typescript
import { json } from '@kit.ArkTS';

// 标准JSON序列化浮点数可能丢失精度
let data = {
  price: 0.1 + 0.2,       // 0.30000000000000004
  amount: 1 / 3,           // 0.3333333333333333
  precise: 99.99
};

let str = json.stringify(data);
console.info(str);
// 使用扩展库可保持精确的浮点表示

// 配合 decimal 模块实现精确计算后序列化
import { decimal } from '@kit.ArkTS';
let precisePrice = new decimal.Decimal('0.1').plus('0.2');
let preciseData = {
  price: precisePrice.toString(), // "0.3"
  amount: '0.3333333333333333',
  precise: 99.99
};
console.info(json.stringify(preciseData));
```

## 13. 标准 JSON 与 ArkTS JSON 扩展对比

| 特性 | 标准 JSON | ArkTS JSON 扩展 |
|------|-----------|-----------------|
| 基本解析/序列化 | ✅ | ✅ |
| 大整数安全解析 | ❌（精度丢失） | ✅ |
| BigInt 序列化 | ❌（TypeError） | ✅ |
| 嵌套引号处理 | 有限 | ✅ 增强 |
| has/remove 操作 | ❌ | ✅ |
| reviver/replacer | ✅ | ✅ |
| 格式化输出 | ✅ | ✅ |
