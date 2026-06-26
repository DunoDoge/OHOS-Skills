# Documentation Structure Reference

## Available Catalogs

Complete list of catalogs that can be queried with the `getCatalogTree` API.

### HarmonyOS Core

| catalogName | Description | Top-level nodes |
|-------------|-------------|-----------------|
| `harmonyos-guides` | Main development guides (ArkTS, Kits, tools) | 20 |
| `harmonyos-references` | API reference documentation | 9 |
| `harmonyos-releases` | Release notes and changelogs | 1 |
| `harmonyos-faqs` | Frequently asked questions | 10 |
| `harmonyos-roadmap` | Feature roadmap | 1 |

### Design & Architecture

| catalogName | Description |
|-------------|-------------|
| `design-guides` | UI/UX design guidelines (9 sections) |
| `architecture-guides` | System architecture documentation (20 sections) |
| `best-practices` | Best practices and development patterns (29 sections) |

### Platform Services

| catalogName | Description |
|-------------|-------------|
| `app` | Application platform services (8 sections) |
| `service` | Cloud/backend services (4 sections) |

### HarmonyOS Center

| catalogName | Description |
|-------------|-------------|
| `harmonyos-center-guides` | Center-specific guides (10 sections) |

### Atomic Services (元服务)

| catalogName | Description |
|-------------|-------------|
| `atomic-guides` | Atomic service development guides |
| `atomic-references` | Atomic service API reference |
| `atomic-releases` | Atomic service release notes |
| `atomic-faqs` | Atomic service FAQs |
| `atomic-ascf` | ASCF (Atomic Service Component Framework) |

### Games

| catalogName | Description |
|-------------|-------------|
| `games-guides` | Game development guides |
| `games-references` | Game API reference |
| `games-samples` | Game code samples |

## URL Structure

### Page URL Pattern

```
https://developer.huawei.com/consumer/{lang}/doc/{catalogName}[-{version}]/{slug}[-{version}]
```

- `{lang}`: `cn` | `en` | `ru`
- `{catalogName}`: catalog identifier (e.g., `harmonyos-guides`)
- `{version}`: version suffix (e.g., `V5`), optional
- `{slug}`: document slug from catalog tree `relateDocument` field

### API Base URL

```
https://developer.huawei.com/consumer/cn/documentPortal/
```

This is the public-facing endpoint (no auth required). All POST requests go here.

### Language Variants

| Language | Base URL |
|----------|----------|
| Chinese | `https://developer.huawei.com/consumer/cn/documentPortal/` |
| English | `https://developer.huawei.com/consumer/en/documentPortal/` |
| Russian | `https://developer.huawei.com/consumer/ru/documentPortal/` |

## harmonyos-guides Top-Level Sections

The main catalog `harmonyos-guides` contains these top-level sections:

1. **应用开发导读** — Application development introduction
2. **应用开发准备** — Development preparation (quick start)
3. **应用开发** — Application development (Kits overview)
4. **系统** — System capabilities (security, network, basic functions)
5. **媒体** — Media (audio, video, camera)
6. **图形** — Graphics (AR, 2D, 3D)
7. **应用服务** — Application services (accounts, ads, store, payments)
8. **AI** — AI capabilities (Agent Framework, CANN, Speech, Vision)
9. **一多开发适配与部署** — Multi-device adaptation
10. **流转** — Device continuity/hopping
11. **NDK开发** — Native development kit
12. **开发环境搭建** — DevEco Studio setup
13. **应用测试** — Application testing
14. **使用AI智能辅助编码** — AI-assisted coding (CodeGennie)
15. **编写调试应用** — Writing and debugging apps
16. **构建应用** — Building applications (hvigor)
17. **优化应用性能** — Performance optimization
18. **发布应用** — Publishing applications
19. **开发相关工具** — Development tools (command line, codelinter, hstack)
20. **应用质量建议** — Quality recommendations

## Catalog Tree Node Structure

```json
{
  "nodeId": "unique-hash-id",
  "nodeName": "Display Title (Chinese)",
  "catalogIndex": 1,
  "isLeaf": true,
  "parent": "parent-node-id",
  "relateDocument": "document-slug-name",
  "parentFileNameForSearch": "parent-slug-name",
  "children": []
}
```

Key fields:
- `relateDocument`: Use this as the `objectId` parameter for `getDocumentById`
- `isLeaf: true`: This node is a document page (has content)
- `isLeaf: false`: This is a category/section header (may have children but no direct content)
