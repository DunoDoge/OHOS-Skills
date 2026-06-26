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

### Atomic Services

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

1. **Application Development Introduction**
2. **Development Preparation** (quick start)
3. **Application Development** (Kits overview)
4. **System** (security, network, basic functions)
5. **Media** (audio, video, camera)
6. **Graphics** (AR, 2D, 3D)
7. **Application Services** (accounts, ads, store, payments)
8. **AI** (Agent Framework, CANN, Speech, Vision)
9. **Multi-Device Adaptation & Deployment**
10. **Device Continuity / Hopping**
11. **NDK Development** (native development kit)
12. **Development Environment Setup** (DevEco Studio)
13. **Application Testing**
14. **AI-Assisted Coding** (CodeGennie)
15. **Writing & Debugging Applications**
16. **Building Applications** (hvigor)
17. **Performance Optimization**
18. **Publishing Applications**
19. **Development Tools** (command line, codelinter, hstack)
20. **Quality Recommendations**

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
