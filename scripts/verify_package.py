#!/usr/bin/env python3
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "DELIVERY_INDEX.md",
    "QA_REPORT.md",
    "docs/source-brief.md",
    "docs/bilingual-study-note.md",
    "docs/goal-coverage-matrix.md",
    "docs/final-completion-audit.md",
    "docs/authorized-transcript-workflow.md",
    "docs/research-evidence-register.md",
    "docs/learning-guide.md",
    "docs/public-content-pack.md",
    "docs/case-study-workbook.md",
    "docs/brand-teardown-handbook.md",
    "docs/7-day-learning-plan.md",
    "docs/facilitator-guide.md",
    "data/opportunity-scorecard.csv",
    "site/index.html",
    "site/styles.css",
    "site/app.js",
]

FORBIDDEN_PATTERNS = [
    "优优独播放",
    "Hedron",
    "Lavart",
    "Karm",
    "Visa",
    "lovart.ai/en/news",
]

REQUIRED_CASES = [
    "Cal AI",
    "Photoroom",
    "Gamma",
    "PDF.ai",
    "HeyGen",
    "Lovart",
    "Captions",
    "Photo AI",
    "Calm",
    "ElevenLabs",
]

REQUIRED_PUBLIC_PACK_SECTIONS = [
    "对外发布长文",
    "30 分钟公开课讲稿",
    "10 张学习卡片文案",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def check_required_paths() -> None:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).exists()]
    if missing:
        fail(f"missing required paths: {missing}")


def check_csv() -> None:
    csv_path = ROOT / "data/opportunity-scorecard.csv"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) < 10:
        fail(f"scorecard needs at least 10 rows, got {len(rows)}")
    required_columns = {"opportunity", "target_user", "job_to_be_done", "opportunity_score"}
    if not rows or not required_columns.issubset(rows[0]):
        fail("scorecard missing required columns")


def check_forbidden_terms() -> None:
    searchable = [
        path for path in REQUIRED_PATHS if path.endswith((".md", ".html", ".js", ".css"))
    ]
    for path in searchable:
        text = read(path)
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in text:
                fail(f"forbidden pattern {pattern!r} found in {path}")


def check_case_workbook() -> None:
    text = read("docs/case-study-workbook.md")
    for case in REQUIRED_CASES:
        if case not in text:
            fail(f"case workbook missing {case}")
    repeated_sections = {
        "小团队可学": ["小团队可学", "小团队可以学什么"],
        "小团队不要学": ["小团队不要学", "小团队不要学什么"],
        "迁移练习": ["迁移练习"],
    }
    for label, aliases in repeated_sections.items():
        count = sum(text.count(alias) for alias in aliases)
        if count < 8:
            fail(f"case workbook lacks repeated section: {label}")


def check_public_pack() -> None:
    text = read("docs/public-content-pack.md")
    for section in REQUIRED_PUBLIC_PACK_SECTIONS:
        if section not in text:
            fail(f"public content pack missing section: {section}")


def check_bilingual_study_note() -> None:
    text = read("docs/bilingual-study-note.md")
    required = [
        "版权边界",
        "双语分段学习稿",
        "核心术语中英对照",
        "英文表达模板",
        "课堂练习",
    ]
    for section in required:
        if section not in text:
            fail(f"bilingual study note missing section: {section}")


def check_goal_matrix() -> None:
    text = read("docs/goal-coverage-matrix.md")
    required = [
        "原目标拆解",
        "覆盖矩阵",
        "版权受限",
        "深度研究",
        "竞品",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"goal coverage matrix missing phrase: {phrase}")


def check_brand_handbook() -> None:
    text = read("docs/brand-teardown-handbook.md")
    required = [
        "品牌拆解的 8 个问题",
        "10 个品牌样本",
        "品牌命名模式",
        "首页首屏模板",
        "品牌评分表",
        "常见坏味道",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"brand handbook missing phrase: {phrase}")
    for brand in ["Cal AI", "Photoroom", "Gamma", "HeyGen", "Lovart", "Captions", "ElevenLabs"]:
        if brand not in text:
            fail(f"brand handbook missing brand: {brand}")


def check_completion_audit() -> None:
    text = read("docs/final-completion-audit.md")
    required = [
        "审计结论",
        "线上交付证据",
        "原始目标逐项审计",
        "当前验证证据",
        "不能声明完成的部分",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"completion audit missing phrase: {phrase}")


def check_authorized_transcript_workflow() -> None:
    text = read("docs/authorized-transcript-workflow.md")
    required = [
        "用户授权确认模板",
        "目录约定",
        "private/",
        "处理步骤",
        "验收清单",
        "发布判断",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"authorized transcript workflow missing phrase: {phrase}")


def check_research_evidence_register() -> None:
    text = read("docs/research-evidence-register.md")
    required = [
        "证据等级",
        "市场与订阅趋势",
        "平台政策与合规",
        "竞品和品牌来源",
        "维护流程",
        "引用原则",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"research evidence register missing phrase: {phrase}")


def check_site_links() -> None:
    html = read("site/index.html")
    local_links = re.findall(r'(?:href|src)="(\\.\\./[^"#]+)"', html)
    for link in local_links:
        if not (ROOT / "site" / link).resolve().exists():
            fail(f"site local link target missing: {link}")
    for required in ["学习路径", "核心结论", "竞品", "资料"]:
        if required not in html:
            fail(f"site missing required visible text: {required}")


def main() -> None:
    check_required_paths()
    check_csv()
    check_forbidden_terms()
    check_case_workbook()
    check_public_pack()
    check_bilingual_study_note()
    check_goal_matrix()
    check_brand_handbook()
    check_completion_audit()
    check_authorized_transcript_workflow()
    check_research_evidence_register()
    check_site_links()
    print("OK: learning hub package verification passed")


if __name__ == "__main__":
    main()
