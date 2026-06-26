---
name: arkts-helper
description: Use when writing, reviewing, or migrating ArkTS code for HarmonyOS / OpenHarmony app development. Triggers include ArkTS syntax, ArkTS type system, ArkTS class/interface/generics, ArkTS coding style, ArkTS language features, TypeScript to ArkTS migration, ArkTS performance optimization, ArkTS standard library, ArkTS concurrency, Promise, async/await, TaskPool, Worker, Sendable, ArkTS container classes, XML/Buffer/JSON, or any topic under the HarmonyOS ArkTS language documentation. Loads the offline ArkTS language reference set so the agent can give accurate ArkTS guidance instead of guessing from TypeScript knowledge.
---

# arkts-helper

ArkTS is the official high-level language for HarmonyOS application development, extending and constraining the TypeScript (TS) ecosystem:

- **Mandatory static typing**: All variables must have declared types; `any`/`unknown` are not supported. The compiler performs stricter type checking at development time.
- **No runtime object layout changes**: Dynamically adding/removing object properties is not allowed; object structure is determined at compile time.
- **Restricted operator semantics**: The unary plus operator `+` can only operate on numbers, not for string-to-number conversion.
- **No Structural typing**: Type compatibility is based on nominal typing, not structural typing.
- **Use `let` instead of `var`**: ArkTS requires `let` for variable declarations; `var` is not supported.

Code written by agents using generic TypeScript experience is **highly likely to fail compilation or underperform on HarmonyOS**. This skill provides offline reference documents (12 docs + INDEX under `references/`) which are offline copies of Huawei's official "ArkTS Language" documentation series, serving as the **authoritative reference** for ArkTS syntax/migration/performance/standard library tasks.

## When to Use This Skill

Follow this skill's workflow whenever any of the following conditions are met:

- The user requests **writing or reviewing ArkTS code** (syntax, type system, classes/interfaces/generics/enums)
- The user requests **migrating TypeScript code to ArkTS** (adaptation rules, adaptation cases)
- The user requests **optimizing ArkTS code performance** (high-performance programming practices)
- The user requests **using the ArkTS standard library** (XML/Buffer/JSON/container libraries)
- The user requests **ArkTS concurrency programming** (Promise/async-await/TaskPool/Worker/Sendable)
- The user asks about **differences between ArkTS and TypeScript**
- The user requests **ArkTS coding standards** (naming, code formatting, comments)
- The user mentions `arkts-no-*` rules but needs syntax guidance rather than error fixes
- The user mentions ArkTS language features (`@Concurrent`, Sendable, container classes, etc.)

Do not force this skill onto "ArkTS compilation error fixes", "NDK/C++ interop", or "command-line build/deploy" scenarios — use the corresponding skills instead (see boundary below).

## Boundary with Other Skills

This skill covers **"ArkTS language syntax and style guidance"**, not **"how to fix compilation errors"**, **"how to write NDK code"**, or **"how to invoke build commands"**. When ArkTS development tasks involve the following issues, cross-reference the corresponding skill:

| Issue Type | Cross-reference Skill | Boundary |
| --- | --- | --- |
| ArkTS compilation errors (`arkts-no-*` rules, etc.) | `arkts-debug` | This skill covers "how to write compliant code"; `arkts-debug` covers "how to fix errors after they occur" |
| NDK / C++ / Node-API interop | `arkts-ndk-dev` | This skill only provides a cross-language interaction overview; detailed Node-API development belongs to `arkts-ndk-dev` |
| Command-line build/deploy/signing/pipeline | `arkts-build` | This skill does not cover build commands |
| APIs / Kits / features not covered by offline docs | `harmony-fetch` | If the 12 offline docs in this skill are insufficient to answer a question (e.g., new Kits, latest API signatures, version changes), use `harmony-fetch` to fetch the latest documentation from the Huawei developer portal |

## Workflow (Follow Strictly)

### 1. Read the Index First, Then Decide Which Doc to Load

Before any ArkTS syntax/migration/performance task, **you must read** `references/INDEX.md` first. It provides the role of each of the 12 documents, reading paths by scenario, and key difference quick references — this prevents loading the entire reference directory into context.

### 2. Load the Corresponding Document by Task Type

| Task Type | Required Reading (under `references/`) |
| -------- | ------------------------------ |
| ArkTS syntax (declarations/types/operators/statements/functions/classes/interfaces/generics/enums) | `01-arkts-language-introduction.md` |
| ArkTS coding style | `02-arkts-coding-style.md` |
| TS→ArkTS migration background | `03-ts-to-arkts-migration-background.md` |
| **TS→ArkTS migration rules** | `04-ts-to-arkts-migration-rules.md` |
| TS→ArkTS migration cases | `05-ts-to-arkts-migration-cases.md` |
| **ArkTS high-performance programming** | `06-arkts-high-performance.md` |
| ArkTS standard library overview | `07-arkts-stdlib-overview.md` |
| XML/Buffer/JSON extension libraries | `08-arkts-xml-buffer-json.md` |
| ArkTS container library | `09-arkts-container-library.md` |
| Async concurrency (Promise/async-await) | `10-arkts-concurrency-async.md` |
| **Multi-thread concurrency (TaskPool/Worker/Sendable)** | `11-arkts-concurrency-multithread.md` |
| Cross-language interaction overview | `12-arkts-cross-language-overview.md` |

When reading documents, prefer using `Grep`/`Read` with offset/limit to locate specific sections — do not read large files in their entirety at once.

### 3. Strictly Enforce Red Lines When Writing Code

Before writing or modifying ArkTS code, self-check the following high-frequency red lines (detailed rules are subject to the original documentation):

**TS→ArkTS difference red lines**:
- **No `any`/`unknown`**: Must use concrete types
- **No runtime object layout changes**: Cannot dynamically add/remove properties
- **No `as` type assertions**: Use explicit type declarations
- **Unary `+` only for numbers**: Use `Number()` or `parseInt()` for string-to-number conversion
- **Use `let` instead of `var`**: ArkTS does not support `var`
- **Object literals must correspond to declared classes or interfaces**: Cannot use anonymous object types

**High-performance programming red lines**:
- **Use `const` for unchanging variables**: Variables declared with `let` that are never modified should use `const`
- **Avoid mixing integer and floating-point types**: number type variables should not mix integers and floating-point values
- **Avoid sparse arrays**: Arrays should be initialized contiguously
- **Avoid reassigning function parameters**: Parameters should be treated as read-only
- **Use ArkTS container classes instead of Array**: ArrayList/HashMap/TreeMap, etc. offer better performance

When uncertain, **search the original text in `references/04-ts-to-arkts-migration-rules.md` or `06-arkts-high-performance.md` for the relevant red line** before writing.

### 4. Cite the Source When Referencing Documents

When answering ArkTS syntax/migration/performance questions, include a citation at the end of the response, e.g.:

> Per the "Mandatory Static Typing" section in `references/04-ts-to-arkts-migration-rules.md`.

### 5. Do Not Skip or Replace This Skill's Checks

Even if the user's code "looks like valid TypeScript", in the HarmonyOS context you must verify against this skill's red lines before answering — do not assume TypeScript knowledge can be directly applied to ArkTS.

## TS→ArkTS Differences Quick Reference

| Difference | TypeScript | ArkTS | Notes |
| --- | --- | --- | --- |
| Type System | Optional static typing | **Mandatory static typing** | No `any`/`unknown`; all variables must declare types |
| Object Layout | Properties can be added/removed at runtime | **No runtime object layout changes** | Object structure determined at compile time; no dynamic property add/remove |
| Operator Semantics | Unary `+` can convert strings to numbers | **Restricted operator semantics** | Unary `+` only for numbers; use `Number()`/`parseInt()` for string-to-number |
| Type Compatibility | Structural typing | **No Structural typing** | Type compatibility based on nominal typing |
| Variable Declaration | `var`/`let`/`const` | **Use `let`/`const`, no `var`** | Must use `let` or `const` |
| Type Assertion | `as` type assertion | **Restricted `as` type assertion** | Some scenarios prohibit `as`; prefer explicit type declarations |
| Object Literals | Can use anonymous object types | **Must correspond to declared class or interface** | Object literals must correspond to explicitly declared class or interface |
| Index Signatures | Supports `[key: string]: type` | **No index signatures** | Use `Record` or `Map` instead |
| Decorators | Experimental support | **Native support** | `@Entry`/`@Component`/`@State` and other ArkUI decorators |
| Enums | Numeric/string/heterogeneous enums | **Only numeric and string enums** | Heterogeneous enums not supported |
| Functions | Supports function overloading | **No function overloading** | Use union types or optional parameters instead |
| `in` Operator | Supports property checks | **Restricted `in` operator** | Only supported in `for...in` and `keyof` scenarios |

## High-Performance Programming Rules

| Category | Rule | Violation Consequence |
| --- | --- | --- |
| **Declarations** | Variables that don't change must use `const` | Compiler cannot optimize, performance degrades |
| **Numeric** | Avoid mixing integer and floating-point in number variables | Runtime type check overhead |
| **Numeric** | Avoid numeric overflow in computations | Runtime exceptions |
| **Loops** | Extract constants in loops, reduce property access count | Unnecessary repeated property access |
| **Functions** | Prefer passing external variables as parameters | Closure variable capture causes performance loss |
| **Functions** | Avoid optional parameters | Runtime type check overhead |
| **Functions** | Avoid reassigning function parameters | Compiler cannot optimize |
| **Arrays** | Avoid sparse arrays | Runtime extra checks |
| **Containers** | Use ArkTS container classes (ArrayList/HashMap, etc.) instead of Array | Array operations are less performant than specialized containers |
| **Concurrency** | Use TaskPool/Worker for long-running tasks to avoid blocking main thread | UI stuttering |

## Directory Structure

```
arkts-helper/
├── SKILL.md                                          # This file
└── references/
    ├── INDEX.md                                      # Must read first
    ├── 01-arkts-language-introduction.md             # ArkTS language introduction
    ├── 02-arkts-coding-style.md                      # ArkTS coding style
    ├── 03-ts-to-arkts-migration-background.md        # TS→ArkTS migration background
    ├── 04-ts-to-arkts-migration-rules.md             # TS→ArkTS migration rules
    ├── 05-ts-to-arkts-migration-cases.md             # TS→ArkTS migration cases
    ├── 06-arkts-high-performance.md                  # ArkTS high-performance programming
    ├── 07-arkts-stdlib-overview.md                   # ArkTS standard library overview
    ├── 08-arkts-xml-buffer-json.md                   # XML/Buffer/JSON extension libraries
    ├── 09-arkts-container-library.md                 # ArkTS container library
    ├── 10-arkts-concurrency-async.md                 # Async concurrency (Promise/async-await)
    ├── 11-arkts-concurrency-multithread.md           # Multi-thread concurrency & inter-thread communication
    └── 12-arkts-cross-language-overview.md           # Cross-language interaction overview
```

## Documentation Source & Maintenance

- Upstream: Huawei Developer official site "Documentation Center › Application Development" series, under `https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/`:
  - `introduction-to-arkts` (ArkTS language introduction)
  - `arkts-coding-style-guide` (ArkTS coding style)
  - `arkts-migration-background` (migration background)
  - `typescript-to-arkts-migration-guide` (migration rules)
  - `arkts-more-cases` (migration cases)
  - `arkts-high-performance-programming` (high-performance programming)
  - `arkts-utils-overview` (standard library overview)
  - `xml-generation-parsing-conversion` + `buffer` + `arkts-json` (XML/Buffer/JSON)
  - `containers` + `linear-container` + `nonlinear-container` (container libraries)
  - `async-concurrency-overview` (async concurrency)
  - `multithread-concurrency` + `interthread-communication` (multi-thread concurrency)
  - `arkts-cross-language-interaction` (cross-language interaction)
- Documents are offline snapshots taken on 2026-06-18; each document includes the upstream URL and fetch timestamp at the top.
- To update to the latest version, re-run the fetch (use `curl`/WebFetch from the upstream URLs to overwrite files in `references/`); if expanding the file list, also update `references/INDEX.md`.
- ArkTS language specifications may change with HarmonyOS version updates; if uncertain about syntax, consult the latest official documentation.
