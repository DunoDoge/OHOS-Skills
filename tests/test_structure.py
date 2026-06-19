"""
OHOS-Skills 结构验证测试
========================
验证每个 skill 的文件完整性、SKILL.md 格式、引用链接有效性。
无需 API Key，纯本地运行。

用法:
    python test_structure.py
    python test_structure.py -v          # 详细输出
    python test_structure.py --fix       # 仅列出可修复项（不自动修改）
"""

import os
import re
import sys
import io
import argparse
from pathlib import Path
from dataclasses import dataclass, field

# Windows 控制台 UTF-8 输出
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent  # 项目根目录（tests/ 的上级）

# ── 数据模型 ──────────────────────────────────────────────

@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""

@dataclass
class SkillCheck:
    skill_name: str
    skill_dir: Path
    results: list[CheckResult] = field(default_factory=list)

    @property
    def passed_count(self):
        return sum(1 for r in self.results if r.passed)

    @property
    def total_count(self):
        return len(self.results)

# ── SKILL.md frontmatter 解析 ─────────────────────────────

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def parse_frontmatter(text: str) -> dict | None:
    """简单解析 YAML frontmatter（不依赖 pyyaml）"""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    result = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip("\"'")
        if value:
            result[key] = value
    return result if result else None

# ── 检查函数 ──────────────────────────────────────────────

def check_skillmd_exists(sc: SkillCheck):
    """SKILL.md 是否存在"""
    p = sc.skill_dir / "SKILL.md"
    sc.results.append(CheckResult("SKILL.md 存在", p.exists(), str(p)))

def check_frontmatter(sc: SkillCheck):
    """SKILL.md frontmatter 格式"""
    p = sc.skill_dir / "SKILL.md"
    if not p.exists():
        sc.results.append(CheckResult("frontmatter 格式", False, "SKILL.md 不存在"))
        return
    text = p.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        sc.results.append(CheckResult("frontmatter 格式", False, "无法解析 frontmatter"))
        return
    sc.results.append(CheckResult("frontmatter 格式", True))

    # name 字段
    name = fm.get("name")
    sc.results.append(CheckResult(
        "frontmatter.name",
        name == sc.skill_name,
        f"期望 '{sc.skill_name}'，实际 '{name}'"
    ))

    # description 字段
    desc = fm.get("description")
    sc.results.append(CheckResult(
        "frontmatter.description",
        isinstance(desc, str) and len(desc) >= 50,
        f"长度 {len(desc) if desc else 0}，建议 >= 50 字符"
    ))

def check_references_dir(sc: SkillCheck):
    """references/ 目录是否存在"""
    p = sc.skill_dir / "references"
    sc.results.append(CheckResult("references/ 目录", p.is_dir(), str(p)))

def check_index_md(sc: SkillCheck):
    """references/INDEX.md 是否存在（arkts-debug 无 INDEX.md，跳过）"""
    if sc.skill_name == "arkts-debug":
        return
    p = sc.skill_dir / "references" / "INDEX.md"
    sc.results.append(CheckResult("INDEX.md 存在", p.exists(), str(p)))

def check_reference_files(sc: SkillCheck):
    """SKILL.md 中引用的 references/ 文件是否都存在"""
    p = sc.skill_dir / "SKILL.md"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    # 匹配 references/xxx.md 形式的引用（排除跨 skill 引用如 arkts-helper/references/）
    refs = re.findall(r"(?<!\w/)references/([\w\-]+\.md)", text)
    refs = set(refs) - {"INDEX.md"}  # INDEX.md 单独检查
    missing = []
    for ref in sorted(refs):
        if not (sc.skill_dir / "references" / ref).exists():
            # 检查是否为跨 skill 引用（如 arkts-helper/references/xxx.md）
            cross_ref = re.search(r"(\w+)/references/" + re.escape(ref), text)
            if cross_ref and cross_ref.group(1) != sc.skill_name:
                continue  # 跨 skill 引用，跳过
            missing.append(ref)
    sc.results.append(CheckResult(
        "references 文件完整性",
        len(missing) == 0,
        f"缺失: {missing}" if missing else "全部存在"
    ))

def check_assets_dir(sc: SkillCheck):
    """arkts-debug 专属：assets/ 目录和 .ets 文件"""
    if sc.skill_name != "arkts-debug":
        return
    assets_dir = sc.skill_dir / "assets"
    sc.results.append(CheckResult("assets/ 目录", assets_dir.is_dir(), str(assets_dir)))

    # 检查 .ets 文件数量
    ets_files = list(assets_dir.glob("*.ets")) if assets_dir.exists() else []
    sc.results.append(CheckResult(
        "assets .ets 文件数",
        len(ets_files) >= 28,
        f"实际 {len(ets_files)} 个，期望 >= 28"
    ))

    # 检查 references 与 assets 数量对应关系
    # references: snake_case (e.g. possibly_null_errors.md)
    # assets: PascalCase (e.g. PossiblyNullError.ets)
    refs_dir = sc.skill_dir / "references"
    if refs_dir.exists():
        ref_count = len(list(refs_dir.glob("*.md"))) - (1 if (refs_dir / "INDEX.md").exists() else 0)
        asset_count = len(ets_files)
        ok = ref_count == asset_count
        sc.results.append(CheckResult(
            "references <-> assets 数量对应",
            ok,
            f"references {ref_count} 个, assets {asset_count} 个"
        ))

def check_internal_links(sc: SkillCheck):
    """SKILL.md 中的内部链接（相对路径）是否有效"""
    p = sc.skill_dir / "SKILL.md"
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    # 匹配 [text](./path) 或 [text](path) 形式
    links = re.findall(r"\[([^\]]*)\]\(\.?/?([^)]+)\)", text)
    broken = []
    for label, href in links:
        # 跳过外部链接和锚点
        if href.startswith("http") or href.startswith("#") or href.startswith("mailto"):
            continue
        target = sc.skill_dir / href
        if not target.exists():
            broken.append(f"[{label}]({href})")
    sc.results.append(CheckResult(
        "内部链接有效性",
        len(broken) == 0,
        f"失效链接: {broken}" if broken else "全部有效"
    ))

def check_doc_headers(sc: SkillCheck):
    """references/ 下的文档是否包含上游 URL 署名"""
    refs_dir = sc.skill_dir / "references"
    if not refs_dir.exists():
        return
    # arkts-debug 的 references 是自行编写的，跳过上游 URL 检查
    if sc.skill_name == "arkts-debug":
        return
    md_files = list(refs_dir.glob("*.md"))
    md_files = [f for f in md_files if f.name != "INDEX.md"]
    missing_url = []
    for f in sorted(md_files):
        text = f.read_text(encoding="utf-8")
        if "developer.huawei.com" not in text and "developer.openharmony.cn" not in text:
            missing_url.append(f.name)
    sc.results.append(CheckResult(
        "文档上游 URL 署名",
        len(missing_url) == 0,
        f"缺少署名: {missing_url}" if missing_url else "全部包含"
    ))

# ── 运行 ──────────────────────────────────────────────────

ALL_CHECKS = [
    check_skillmd_exists,
    check_frontmatter,
    check_references_dir,
    check_index_md,
    check_reference_files,
    check_assets_dir,
    check_internal_links,
    check_doc_headers,
]

def discover_skills() -> list[SkillCheck]:
    skills = []
    for d in sorted(ROOT.iterdir()):
        if d.is_dir() and (d / "SKILL.md").exists():
            skills.append(SkillCheck(skill_name=d.name, skill_dir=d))
    return skills

def main():
    parser = argparse.ArgumentParser(description="OHOS-Skills 结构验证")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    args = parser.parse_args()

    skills = discover_skills()
    if not skills:
        print("未发现任何 skill 目录（需包含 SKILL.md）")
        sys.exit(1)

    total_pass = 0
    total_all = 0

    for sc in skills:
        for check_fn in ALL_CHECKS:
            check_fn(sc)

        print(f"\n{'='*60}")
        print(f"  {sc.skill_name}")
        print(f"{'='*60}")

        for r in sc.results:
            icon = "PASS" if r.passed else "FAIL"
            line = f"  [{icon}] {r.name}"
            if args.verbose or not r.passed:
                line += f"  — {r.detail}" if r.detail else ""
            print(line)

        total_pass += sc.passed_count
        total_all += sc.total_count
        print(f"\n  小计: {sc.passed_count}/{sc.total_count} 通过")

    print(f"\n{'='*60}")
    print(f"  总计: {total_pass}/{total_all} 通过")
    print(f"{'='*60}")

    sys.exit(0 if total_pass == total_all else 1)

if __name__ == "__main__":
    main()
