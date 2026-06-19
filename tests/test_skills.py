"""
OHOS-Skills LLM 功能测试
========================
向 LLM 发送测试提示词，验证 skill 是否被正确激活、
红线是否被拦截、文档是否被引用。

支持 OpenAI 兼容 API（OpenAI / DeepSeek / 本地模型等）。

用法:
    # 设置 API 密钥
    set OPENAI_API_KEY=sk-xxx
    set OPENAI_BASE_URL=https://api.openai.com/v1   # 可选，默认 OpenAI

    # 运行全部测试
    python test_skills.py

    # 只测试某个 skill
    python test_skills.py --skill arkts-debug

    # 指定模型
    python test_skills.py --model gpt-4o

    # 详细输出
    python test_skills.py -v

    # 生成报告
    python test_skills.py --report report.json
"""

import json
import os
import re
import sys
import argparse
import time
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

# 延迟导入，运行时检查
try:
    import httpx
except ImportError:
    print("需要 httpx: pip install httpx")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent  # 项目根目录

# ── 从 .env 文件加载配置（优先级低于环境变量）──────────────────

_env_file = ROOT / ".env"
if _env_file.exists():
    for line in _env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip("\"'")
        if key and key not in os.environ:  # 环境变量优先
            os.environ[key] = value

# ── 配置 ──────────────────────────────────────────────────

API_KEY = os.environ.get("OPENAI_API_KEY")
BASE_URL = os.environ.get("OPENAI_BASE_URL")
DEFAULT_MODEL = os.environ.get("TEST_MODEL")

# ── 测试用例定义 ──────────────────────────────────────────

@dataclass
class TestCase:
    id: str
    skill: str                    # 预期激活的 skill
    prompt: str                   # 用户输入
    expected_keywords: list[str]  # 回答中应包含的关键词
    forbidden_keywords: list[str] # 回答中不应包含的关键词
    expected_ref: str = ""        # 预期引用的文档路径片段
    category: str = ""            # 分类

CASES: list[TestCase] = [
    # ── arkts-helper ──────────────────────────────────────
    TestCase("H-01", "arkts-helper",
        "帮我写一个 ArkTS 函数，接收任意类型的参数并打印它。",
        expected_keywords=["泛型", "generic", "<T>"],
        forbidden_keywords=["any", "unknown"],
        expected_ref="04-ts-to-arkts-migration-rules",
        category="arkts-helper/红线"),
    TestCase("H-02", "arkts-helper",
        "以下 ArkTS 代码有什么问题？`var count = 0;`",
        expected_keywords=["let", "const", "不支持 var"],
        forbidden_keywords=["var 没问题", "var 也可以"],
        expected_ref="04-ts-to-arkts-migration-rules",
        category="arkts-helper/红线"),
    TestCase("H-03", "arkts-helper",
        "在 ArkTS 中，我想返回一个匿名对象 `{ name: 'test', value: 42 }`，怎么写？",
        expected_keywords=["interface", "class", "声明"],
        forbidden_keywords=["直接返回", "匿名对象"],
        expected_ref="04-ts-to-arkts-migration-rules",
        category="arkts-helper/红线"),
    TestCase("H-04", "arkts-helper",
        "我有一段 TypeScript 代码用了 `as` 类型断言和索引签名 `[key: string]: any`，怎么迁移到 ArkTS？",
        expected_keywords=["Map", "显式类型", "不支持索引签名"],
        forbidden_keywords=["as any", "Record<string, any>"],
        expected_ref="04-ts-to-arkts-migration-rules",
        category="arkts-helper/迁移"),
    TestCase("H-05", "arkts-helper",
        "以下 ArkTS 代码有性能问题吗？`let MAX_SIZE = 100;`",
        expected_keywords=["const", "不变"],
        forbidden_keywords=["没有问题", "没问题"],
        expected_ref="06-arkts-high-performance",
        category="arkts-helper/性能"),
    TestCase("H-06", "arkts-helper",
        "ArkTS 中如何执行耗时计算任务而不阻塞主线程？",
        expected_keywords=["TaskPool", "Worker", "@Concurrent"],
        forbidden_keywords=["setTimeout", "Web Worker"],
        expected_ref="11-arkts-concurrency-multithread",
        category="arkts-helper/并发"),

    # ── arkts-debug ───────────────────────────────────────
    TestCase("D-01", "arkts-debug",
        "编译报错：`Property 'length' cannot be accessed on a value that is possibly null.` 代码：`let len = arr!.length`",
        expected_keywords=["null", "检查", "可选链", "?."],
        forbidden_keywords=["as any", "! 非空断言就行"],
        expected_ref="possibly_null_errors",
        category="arkts-debug/空安全"),
    TestCase("D-02", "arkts-debug",
        "报错 `arkts-no-props-by-index`：`obj['key']` 不允许，怎么修改？",
        expected_keywords=["点号", "Map", "obj.key"],
        forbidden_keywords=["as any", "(obj as any)"],
        expected_ref="indexed_access_errors",
        category="arkts-debug/索引访问"),
    TestCase("D-03", "arkts-debug",
        "报错 `arkts-no-decl-merging`：`Declaration merging is not supported`，我有两个同名的 interface 想合并。",
        expected_keywords=["extends", "合并", "单个声明"],
        forbidden_keywords=["declare module", "namespace 合并"],
        expected_ref="decl_merging_errors",
        category="arkts-debug/声明合并"),
    TestCase("D-04", "arkts-debug",
        "`AppStorage.get('count')` 返回类型推断错误，怎么正确使用？",
        expected_keywords=["@StorageLink", "setAndLink", "LocalStorage"],
        forbidden_keywords=["AppStorage.get<number>"],
        expected_ref="appstorage_errors",
        category="arkts-debug/AppStorage"),
    TestCase("D-05", "arkts-debug",
        "`@StorageLink('key') value: string` 报错缺少默认值。",
        expected_keywords=["= undefined", "= ''", "默认值"],
        forbidden_keywords=["!", "非空断言"],
        expected_ref="storage_link_default_errors",
        category="arkts-debug/StorageLink"),
    TestCase("D-06", "arkts-debug",
        "报错 `Object literal must correspond to some explicitly declared class or interface`，代码是 `return { x: 1, y: 2 }`",
        expected_keywords=["interface", "class", "声明"],
        forbidden_keywords=["as Point", "类型断言"],
        expected_ref="object_literal_interface_errors",
        category="arkts-debug/对象字面量"),
    TestCase("D-07", "arkts-debug",
        "使用 `ESObject` 类型时报错，ArkTS 中如何处理动态类型？",
        expected_keywords=["具体类型", "ESModule"],
        forbidden_keywords=["any", "保留 ESObject"],
        expected_ref="esobject_type_errors",
        category="arkts-debug/ESObject"),
    TestCase("D-08", "arkts-debug",
        "`LazyForEach` 报错：数据源必须实现 `IDataSource` 接口。",
        expected_keywords=["IDataSource", "totalCount", "getData"],
        forbidden_keywords=["ForEach", "换成 ForEach"],
        expected_ref="idata_source_errors",
        category="arkts-debug/IDataSource"),

    # ── arkts-build ───────────────────────────────────────
    TestCase("B-01", "arkts-build",
        "如何用命令行构建 HarmonyOS debug HAP？",
        expected_keywords=["hvigorw", "assembleHap", "--no-daemon"],
        forbidden_keywords=["gradle", "npm run build"],
        expected_ref="04-hvigorw",
        category="arkts-build/构建"),
    TestCase("B-02", "arkts-build",
        "运行 `hvigorw assembleHap` 报依赖找不到，怎么办？",
        expected_keywords=["ohpm install"],
        forbidden_keywords=["npm install"],
        expected_ref="05-ohpm",
        category="arkts-build/依赖"),
    TestCase("B-03", "arkts-build",
        "如何在 CI 中配置 codelinter 检查，有错误就失败？",
        expected_keywords=["codelinter", "--exit-on", "code-linter.json5"],
        forbidden_keywords=["eslint"],
        expected_ref="02-codelinter",
        category="arkts-build/检查"),
    TestCase("B-04", "arkts-build",
        "线上 release 包崩溃了，有混淆堆栈，怎么还原？",
        expected_keywords=["hstack", "sourceMap", "nameCache"],
        forbidden_keywords=["source-map", "sourcemap npm"],
        expected_ref="03-hstack",
        category="arkts-build/堆栈"),
    TestCase("B-05", "arkts-build",
        "如何给 HarmonyOS HAP 签名？需要哪些文件？",
        expected_keywords=["hap-sign-tool", ".p12", ".cer", ".p7b"],
        forbidden_keywords=["jarsigner", "apksigner"],
        expected_ref="06-building-app",
        category="arkts-build/签名"),
    TestCase("B-06", "arkts-build",
        "我想只构建 library 模块的 HSP，`hvigorw assembleHsp -p module=library@default` 为什么不生效？",
        expected_keywords=["--mode module"],
        forbidden_keywords=["检查拼写"],
        expected_ref="04-hvigorw",
        category="arkts-build/参数"),
    TestCase("B-07", "arkts-build",
        "`ohpm install` 报网络错误，怎么配置 ohpm 仓库地址？",
        expected_keywords=["ohpm.openharmony.cn", "ohpm config set registry"],
        forbidden_keywords=["npm config set registry"],
        expected_ref="05-ohpm",
        category="arkts-build/ohpm"),
    TestCase("B-08", "arkts-build",
        "构建好 HAP 后，怎么推到设备上安装运行？",
        expected_keywords=["hdc file send", "hdc shell bm install", "hdc shell aa start"],
        forbidden_keywords=["adb install", "adb push"],
        expected_ref="07-debugging-commands",
        category="arkts-build/设备"),

    # ── arkts-ndk-dev ─────────────────────────────────────
    TestCase("N-01", "arkts-ndk-dev",
        "如何在 HarmonyOS 中注册一个 Node-API 模块，让 ArkTS 调用 C++ 函数？",
        expected_keywords=["napi_module", "__attribute__((constructor))", "napi_module_register"],
        forbidden_keywords=["NAPI_MODULE", "napi_register_module_v1"],
        expected_ref="05-node-api-development",
        category="arkts-ndk-dev/注册"),
    TestCase("N-02", "arkts-ndk-dev",
        "我在子线程中用 `napi_call_function(env, ...)` 回调 ArkTS，为什么崩溃？",
        expected_keywords=["napi_threadsafe_function", "ArkTS 线程", "禁止跨线程"],
        forbidden_keywords=["uv_queue_work", "加锁"],
        expected_ref="06-node-api-best-practices",
        category="arkts-ndk-dev/线程安全"),
    TestCase("N-03", "arkts-ndk-dev",
        "`napi_wrap` 的 result 参数传 nullptr 和传非 nullptr 有什么区别？",
        expected_keywords=["napi_remove_wrap", "系统管理", "手动"],
        forbidden_keywords=["没区别", "不影响"],
        expected_ref="06-node-api-best-practices",
        category="arkts-ndk-dev/napi_wrap"),
    TestCase("N-04", "arkts-ndk-dev",
        "Node-API 中传递大量数值数据给 ArkTS，用 JSArray 还是 ArrayBuffer？",
        expected_keywords=["ArrayBuffer", "400"],
        forbidden_keywords=["JSArray", "差不多"],
        expected_ref="06-node-api-best-practices",
        category="arkts-ndk-dev/性能"),
    TestCase("N-05", "arkts-ndk-dev",
        "在循环中频繁创建 JS 对象，运行一段时间后内存持续增长，怎么修？",
        expected_keywords=["napi_open_handle_scope", "napi_close_handle_scope"],
        forbidden_keywords=["手动 GC", "减少创建"],
        expected_ref="06-node-api-best-practices",
        category="arkts-ndk-dev/内存"),
    TestCase("N-06", "arkts-ndk-dev",
        "HarmonyOS NDK 工程的 CMakeLists.txt 怎么配置交叉编译？需要引入哪个工具链文件？",
        expected_keywords=["ohos.toolchain.cmake"],
        forbidden_keywords=["CMAKE_SYSTEM_NAME", "手动设置编译器"],
        expected_ref="03-build-ndk-project",
        category="arkts-ndk-dev/CMake"),
    TestCase("N-07", "arkts-ndk-dev",
        "在 C++ 侧如何读取 `resources/rawfile/` 下的文件？",
        expected_keywords=["Rawfile", "OpenRawFile", "ReadRawFile"],
        forbidden_keywords=["std::ifstream", "fopen"],
        expected_ref="07-rawfile",
        category="arkts-ndk-dev/Rawfile"),
    TestCase("N-08", "arkts-ndk-dev",
        "用 `napi_create_external` 创建的对象能在子线程中使用吗？",
        expected_keywords=["napi_coerce_to_native_binding_object", "仅当前线程"],
        forbidden_keywords=["可以", "没问题"],
        expected_ref="06-node-api-best-practices",
        category="arkts-ndk-dev/跨线程"),
]

# ── Skill 上下文构建 ──────────────────────────────────────

def load_skill_context(skill_name: str) -> str:
    """加载 skill 的 SKILL.md 内容作为系统提示词的一部分"""
    skill_dir = ROOT / skill_name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ""
    return skill_md.read_text(encoding="utf-8")

def build_system_prompt(with_skill: str | None = None) -> str:
    """构建系统提示词"""
    base = (
        "你是一个 HarmonyOS / OpenHarmony 应用开发助手。"
        "请根据用户的问题给出准确的技术回答。"
    )
    if with_skill:
        context = load_skill_context(with_skill)
        if context:
            base += f"\n\n请严格遵循以下 skill 指导工作：\n\n{context}"
    return base

# ── API 调用 ──────────────────────────────────────────────

def call_llm(prompt: str, system_prompt: str, model: str) -> str:
    """调用 OpenAI 兼容 API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 1024,
    }
    resp = httpx.post(
        f"{BASE_URL.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]

# ── 评估 ──────────────────────────────────────────────────

@dataclass
class TestResult:
    case_id: str
    skill: str
    category: str
    prompt: str
    response: str
    keyword_pass: bool
    forbidden_pass: bool
    ref_pass: bool
    score: float  # 0-1
    detail: str = ""

def evaluate(case: TestCase, response: str) -> TestResult:
    """评估 LLM 回答"""
    resp_lower = response.lower()

    # 关键词命中
    keyword_hits = sum(1 for kw in case.expected_keywords if kw.lower() in resp_lower)
    keyword_pass = keyword_hits >= max(1, len(case.expected_keywords) // 2)

    # 禁止词检查：排除否定语境（如"不能使用 any"、"禁止 NAPI_MODULE"）
    NEGATION_PATTERNS = [
        r"不(?:能|要|支持|允许|推荐|可用|可以)\s*",
        r"禁止\s*",
        r"避免\s*",
        r"不要\s*",
        r"切勿\s*",
        r"❌\s*",
        r"错误[：:]\s*",
        r"不(?:应|该|宜)\s*",
    ]
    negation_re = re.compile("|".join(NEGATION_PATTERNS))

    forbidden_hits = []
    for kw in case.forbidden_keywords:
        kw_lower = kw.lower()
        # 找到所有出现位置
        start = 0
        found_as_recommendation = False
        while True:
            idx = resp_lower.find(kw_lower, start)
            if idx == -1:
                break
            # 检查前面 20 个字符是否有否定词
            context_before = resp_lower[max(0, idx - 20):idx]
            if negation_re.search(context_before):
                found_as_recommendation = True
                break
            start = idx + 1
        if not found_as_recommendation and kw_lower in resp_lower:
            forbidden_hits.append(kw)
    forbidden_pass = len(forbidden_hits) == 0

    # 文档引用
    ref_pass = True
    if case.expected_ref:
        ref_pass = case.expected_ref.lower() in resp_lower

    # 综合评分
    score = 0.0
    if keyword_pass:
        score += 0.4
    if forbidden_pass:
        score += 0.3
    if ref_pass:
        score += 0.3

    detail_parts = []
    if not keyword_pass:
        detail_parts.append(f"关键词命中不足 (命中 {keyword_hits}/{len(case.expected_keywords)})")
    if not forbidden_pass:
        detail_parts.append(f"包含禁止词: {forbidden_hits}")
    if not ref_pass and case.expected_ref:
        detail_parts.append(f"未引用 {case.expected_ref}")

    return TestResult(
        case_id=case.id,
        skill=case.skill,
        category=case.category,
        prompt=case.prompt,
        response=response,
        keyword_pass=keyword_pass,
        forbidden_pass=forbidden_pass,
        ref_pass=ref_pass,
        score=score,
        detail="; ".join(detail_parts) if detail_parts else "全部通过",
    )

# ── 主流程 ────────────────────────────────────────────────

def run_tests(
    model: str,
    skill_filter: str | None = None,
    verbose: bool = False,
    report_path: str | None = None,
    delay: float = 1.0,
):
    if not API_KEY:
        print("错误: 请设置 OPENAI_API_KEY 环境变量")
        print("  set OPENAI_API_KEY=sk-xxx")
        sys.exit(1)

    cases = CASES
    if skill_filter:
        cases = [c for c in cases if c.skill == skill_filter]

    print(f"模型: {model}")
    print(f"API:  {BASE_URL}")
    print(f"用例: {len(cases)} 条\n")

    results: list[TestResult] = []

    for i, case in enumerate(cases):
        print(f"[{i+1}/{len(cases)}] {case.id} ({case.category})")

        # 带 skill 上下文调用
        system_prompt = build_system_prompt(with_skill=case.skill)
        try:
            response = call_llm(case.prompt, system_prompt, model)
        except Exception as e:
            print(f"  API 调用失败: {e}")
            results.append(TestResult(
                case_id=case.id, skill=case.skill, category=case.category,
                prompt=case.prompt, response="",
                keyword_pass=False, forbidden_pass=False, ref_pass=False,
                score=0.0, detail=f"API 错误: {e}",
            ))
            continue

        result = evaluate(case, response)
        results.append(result)

        icon = "PASS" if result.score >= 0.7 else "FAIL"
        print(f"  [{icon}] 得分: {result.score:.1f} — {result.detail}")

        if verbose:
            # 截断显示
            resp_preview = response[:200].replace("\n", " ")
            print(f"  回答预览: {resp_preview}...")

        time.sleep(delay)  # 避免 rate limit

    # ── 汇总 ──────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("  测试报告")
    print(f"{'='*60}")

    # 按 skill 分组
    skills = sorted(set(r.skill for r in results))
    for skill in skills:
        skill_results = [r for r in results if r.skill == skill]
        avg_score = sum(r.score for r in skill_results) / len(skill_results)
        pass_count = sum(1 for r in skill_results if r.score >= 0.7)
        print(f"\n  {skill}: {pass_count}/{len(skill_results)} 通过, 平均分 {avg_score:.2f}")
        for r in skill_results:
            icon = "PASS" if r.score >= 0.7 else "FAIL"
            print(f"    [{icon}] {r.case_id}: {r.score:.1f} — {r.detail}")

    total_pass = sum(1 for r in results if r.score >= 0.7)
    total_avg = sum(r.score for r in results) / len(results) if results else 0
    print(f"\n  总计: {total_pass}/{len(results)} 通过, 平均分 {total_avg:.2f}")

    # 按维度统计
    kw_pass = sum(1 for r in results if r.keyword_pass)
    fb_pass = sum(1 for r in results if r.forbidden_pass)
    ref_pass = sum(1 for r in results if r.ref_pass)
    print(f"\n  维度分析:")
    print(f"    关键词命中: {kw_pass}/{len(results)}")
    print(f"    禁止词规避: {fb_pass}/{len(results)}")
    print(f"    文档引用:   {ref_pass}/{len(results)}")

    # 生成 JSON 报告
    report = {
        "model": model,
        "api": BASE_URL,
        "total": len(results),
        "passed": total_pass,
        "avg_score": round(total_avg, 2),
        "results": [asdict(r) for r in results],
    }
    report_file = Path(report_path)
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  报告已保存: {report_file}")

    return 0 if total_pass == len(results) else 1

def main():
    parser = argparse.ArgumentParser(description="OHOS-Skills LLM 功能测试")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument("--skill", default=None, help="只测试指定 skill")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    parser.add_argument("--report", default=str(Path(__file__).resolve().parent / "report.json"), help="生成 JSON 报告路径 (默认: tests/report.json)")
    parser.add_argument("--delay", type=float, default=1.0, help="请求间隔(秒)")
    args = parser.parse_args()

    sys.exit(run_tests(
        model=args.model,
        skill_filter=args.skill,
        verbose=args.verbose,
        report_path=args.report,
        delay=args.delay,
    ))

if __name__ == "__main__":
    main()
