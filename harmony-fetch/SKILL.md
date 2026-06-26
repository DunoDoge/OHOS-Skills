---
name: harmony-fetch
description: Search and fetch HarmonyOS/HarmonyOS NEXT developer documentation from Huawei developer portal (developer.huawei.com). Use when local skill docs are insufficient for ArkTS, ArkUI, ArkData, NDK, DevEco Studio, or any HarmonyOS API/feature question. Triggers include HarmonyOS doc lookup, ArkTS API reference, HarmonyOS component usage, DevEco toolchain questions, or when the user explicitly asks to check Huawei official docs.
version: 1.1.0
---

# Harmony-Fetch

Fetch HarmonyOS developer documentation from Huawei's official portal via public APIs.

## When to Use

- ArkTS/ArkUI/ArkData API details not covered by local skills (arkts-helper, arkts-build, etc.)
- HarmonyOS NEXT feature documentation lookup
- DevEco Studio IDE, build tools, or command-line tools reference
- User asks "check Huawei docs" or references developer.huawei.com links
- Need to verify current API signatures, deprecated features, or new capabilities

## 本地文档覆盖范围

在调用线上 API 前，先判断以下本地 skill 是否已覆盖所需内容。**只有当本地文档不足时才使用本 skill 拉取线上文档。**

| 本地 skill | 离线文档 | 覆盖主题 |
| --- | --- | --- |
| `arkts-helper` | 12 篇 | ArkTS 语言语法、类型系统、编码规范、TS→ArkTS 迁移规则与案例、高性能编程、标准库（XML/Buffer/JSON/容器）、并发（Promise/TaskPool/Worker/Sendable） |
| `arkts-debug` | 28 篇 + 28 个 `.ets` 示例 | 28 类常见 ArkTS 编译报错的根因与修复（`arkts-no-*` 规则、`ContentType`、`@StorageLink`、`LazyForEach`、`Possibly null` 等） |
| `arkts-build` | 8 篇 | 命令行构建/测试/签名/部署全流程：`hvigorw`、`codelinter`、`hstack`、`ohpm`、`hdc`、CI 流水线、`hap-sign-tool` |
| `arkts-ndk-dev` | 11 篇 | NDK / Node-API / C++ 互操作：CMake 工具链、`napi_wrap`、`napi_threadsafe_function`、Rawfile、NativeBundle、ASan、LLDB、ABI/Neon |

**判断流程**：用户问题 → 先查上表中对应 skill 的离线文档 → 若文档不足以回答 → 使用本 skill 从华为开发者门户拉取。

## Quick Start

**Two-step workflow**: Search → Fetch.

### Step 1: Find the Document

**Option A — User provides a URL**: Parse the URL to extract the document slug.

URL pattern: `https://developer.huawei.com/consumer/cn/doc/<catalog>-<version>/<slug>-<version>`

Extract `slug` (without version suffix) as the `objectId`.

**Option B — Browse catalog tree**: Run the fetch script with `--catalog` to list sections:

```bash
python3 scripts/fetch_doc.py --catalog harmonyos-guides
```

**Option C — Web search**: Use WebSearch tool with `site:developer.huawei.com/consumer/cn/doc/ <keywords>` to find relevant doc URLs, then extract slugs from results.

### Step 2: Fetch Document Content

```bash
python3 scripts/fetch_doc.py <objectId>
```

Where `objectId` is the document slug (e.g., `arkts-state-management-overview`).

Output is markdown-converted content. For raw HTML, add `--html` flag.

## API Reference

### Catalog Tree API (no auth required)

```
POST https://developer.huawei.com/consumer/cn/documentPortal/getCatalogTree
Content-Type: application/json

{
  "catalogName": "harmonyos-guides",
  "language": "cn",
  "showHide": 0
}
```

Parameters:
- `catalogName`: catalog identifier (see [catalog reference](doc-structure.md))
- `language`: `"cn"` | `"en"` | `"ru"`
- `showHide`: `0` (show all) | `1` (show hidden) | `2` (hide)

Returns a tree where each node has:
- `nodeId`: unique identifier
- `nodeName`: display title (Chinese)
- `relateDocument`: **the slug used as objectId** (leaf nodes only)
- `isLeaf`: whether it's a document page
- `children`: child nodes

### Document Content API (no auth required)

```
POST https://developer.huawei.com/consumer/cn/documentPortal/getDocumentById
Content-Type: application/json

{
  "language": "cn",
  "objectId": "arkts-state-management-overview"
}
```

Returns:
- `value.docId`: internal ID
- `value.title`: document title
- `value.version`: document version (e.g., V85, V219)
- `value.content.content`: **full HTML content**
- `value.anchorList`: heading anchors with hierarchy
- `value.businessName`: product name (HarmonyOS)

**objectId rules**:
- Use the bare slug (no version suffix) for the **latest** version
- Append `-V5` for the HarmonyOS NEXT DP1 version specifically
- Both forms work; prefer bare slug unless user asks for a specific version

### Search (requires auth — use WebSearch instead)

The official search API requires login tokens. **Always use WebSearch with site filter**:

```
site:developer.huawei.com/consumer/cn/doc/ ArkTS Navigation
```

## Catalog Quick Reference

Primary catalogs for HarmonyOS app development:

| Catalog | Content |
|---------|---------|
| `harmonyos-guides` | Main development guides (ArkTS, ArkUI, Kits) |
| `harmonyos-references` | API reference docs |
| `harmonyos-faqs` | FAQ collection |
| `harmonyos-releases` | Release notes |
| `design-guides` | UI/UX design guidelines |
| `best-practices` | Best practices and patterns |
| `architecture-guides` | System architecture docs |

For full catalog list and doc tree structure, see [doc-structure.md](doc-structure.md).

## URL Parsing Examples

| URL | objectId |
|-----|----------|
| `.../doc/harmonyos-guides-V5/arkts-state-management-overview-V5` | `arkts-state-management-overview` |
| `.../doc/harmonyos-references-V5/js-apis-display-V5` | `js-apis-display` |
| `.../doc/best-practices/bpta-smart-reach` | `bpta-smart-reach` |

## Error Handling

- `"document not found"` → objectId slug is wrong; try browsing the catalog tree
- `"主仓不存在"` → the center API catalog doesn't exist; use the standard API
- Empty response → network issue or rate limiting; retry after a short wait
- Garbled Chinese text or `UnicodeEncodeError` → Windows terminal uses GBK encoding by default; the script includes an automatic UTF-8 fix in `main()`. If it still fails, use the import mode described in [Windows 环境注意事项](#windows-环境注意事项).

## Pitfalls

- The documentation site is an Angular SPA — direct WebFetch on page URLs returns empty shells. **Always use the API endpoints**, never try to scrape the HTML page directly.
- Search APIs require authentication cookies. Use WebSearch with `site:` filter as the search alternative.
- Image URLs in document content are CDN-hosted with time-limited signatures; they expire after 24 hours.
- The `-V5` suffix on catalog names and document slugs refers to a specific version; the bare name fetches the latest version.

## Windows 环境注意事项

Windows 终端默认使用 GBK 编码（CP936），直接运行 `fetch_doc.py` 可能导致中文乱码，或在遇到包含特殊 Unicode 字符（如 U+200C 零宽非连接符）的文档时抛出 `UnicodeEncodeError`。脚本已在 `main()` 中内置了 `sys.stdout.reconfigure(encoding='utf-8')` 自动修复，但如果仍有问题（例如在某些终端模拟器或管道环境中），推荐使用 **Python import 模式**：

```python
import sys, os
sys.path.insert(0, r'<skill-dir>/scripts')
from fetch_doc import fetch_document, html_to_markdown

result = fetch_document('some-doc-slug')
value = result.get('value', {})
title = value.get('title', 'Untitled')
html = value.get('content', {}).get('content', '')
md = html_to_markdown(html)

with open('output.md', 'w', encoding='utf-8') as f:
    f.write(f'# {title}\n\n{md}')
```

这种方式绕过终端编码问题，直接将内容写入 UTF-8 文件，是 Windows 上**最可靠的调用方式**。批量获取多个文档时也推荐使用此模式。
