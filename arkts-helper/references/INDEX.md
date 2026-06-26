<!-- Must read first -->
<!-- ArkTS language specification: refer to the official documentation: https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/introduction-to-arkts -->

# INDEX - arkts-helper Reference Documentation

> **Must read first**: Before any arkts-helper task, **read this file first**, then load the corresponding document based on the task type mapping table below.
>
> **ArkTS language specification: refer to the official documentation**: ArkTS syntax and migration rules may change with HarmonyOS version updates. This document is an offline snapshot taken on 2026-06-18; if uncertain about syntax, consult the upstream official documentation.

## Document Roles

| File | Role |
| --- | --- |
| `01-arkts-language-introduction.md` | ArkTS language introduction: basics, declarations, types, operators, statements, functions, classes, interfaces, generics, enums, modules, null safety |
| `02-arkts-coding-style.md` | ArkTS coding style: naming conventions, code formatting, comment guidelines, programming practices |
| `03-ts-to-arkts-migration-background.md` | TS→ArkTS migration background: program stability, performance, compatibility, Ark runtime |
| `04-ts-to-arkts-migration-rules.md` | **TS→ArkTS migration rules (core)**: mandatory static typing, no runtime object layout changes, restricted operator semantics, no structural typing, constraint descriptions |
| `05-ts-to-arkts-migration-cases.md` | TS→ArkTS migration cases: concrete adaptation examples for arkts-no-* rules |
| `06-arkts-high-performance.md` | **ArkTS high-performance programming (core)**: declaration optimization, function optimization, array optimization, container optimization, concurrency optimization |
| `07-arkts-stdlib-overview.md` | ArkTS standard library overview: XML / Buffer / containers / URL / Decimal / JSON |
| `08-arkts-xml-buffer-json.md` | XML generation/parsing/conversion + Buffer/FastBuffer + JSON extension library |
| `09-arkts-container-library.md` | ArkTS container library: linear containers (7 types) + non-linear containers (7 types) + selection guide |
| `10-arkts-concurrency-async.md` | Async concurrency: Promise / async-await / combinators / best practices |
| `11-arkts-concurrency-multithread.md` | **Multi-thread concurrency (core)**: TaskPool / Worker / inter-thread communication / Sendable |
| `12-arkts-cross-language-overview.md` | Cross-language interaction overview: Node-API concepts and development entry points (for detailed development, see arkts-ndk-dev skill) |

## Reading Paths by Scenario

| Scenario | Required Reading (under `references/`) |
| --- | --- |
| Learning ArkTS syntax | `01-arkts-language-introduction.md`, `02-arkts-coding-style.md` |
| Migrating TS code to ArkTS | `03-ts-to-arkts-migration-background.md` → `04-ts-to-arkts-migration-rules.md` → `05-ts-to-arkts-migration-cases.md` |
| Optimizing ArkTS code performance | `06-arkts-high-performance.md` |
| Using the standard library | `07-arkts-stdlib-overview.md`, `08-arkts-xml-buffer-json.md`, `09-arkts-container-library.md` |
| Concurrency programming | `10-arkts-concurrency-async.md`, `11-arkts-concurrency-multithread.md` |
| Interacting with C++ | `12-arkts-cross-language-overview.md` (for detailed development, see `arkts-ndk-dev` skill) |
| Fixing compilation errors | See `arkts-debug` skill |

## TS→ArkTS Key Differences Quick Reference

| Difference | TS | ArkTS |
| --- | --- | --- |
| Type System | Optional static | **Mandatory static**, no any/unknown |
| Object Layout | Mutable at runtime | **No runtime changes allowed** |
| Operators | Unary + can convert to number | **Unary + only for numbers** |
| Type Compatibility | Structural typing | **Not supported**, nominal typing |
| Variable Declaration | var/let/const | **No var**, only let/const |
| Type Assertion | as used freely | **Restricted as**, prefer explicit declarations |
| Object Literals | Anonymous types | **Must correspond to class/interface** |
| Index Signatures | Supported | **Not supported**, use Record/Map |
| Function Overloading | Supported | **Not supported**, use union types / optional parameters |

## High-Performance Programming Rules Quick Reference

- **const**: Variables that don't change must use const
- **Numeric**: Avoid mixing integer and floating-point types
- **Loops**: Extract constants, reduce property access
- **Functions**: Avoid optional parameters, avoid reassigning parameters
- **Arrays**: Avoid sparse arrays
- **Containers**: Use ArkTS container classes (ArrayList/HashMap, etc.) instead of Array
- **Concurrency**: Use TaskPool/Worker for long-running tasks to avoid blocking the main thread
