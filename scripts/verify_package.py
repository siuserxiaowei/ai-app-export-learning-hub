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
    "docs/learning-guide.md",
    "docs/public-content-pack.md",
    "docs/case-study-workbook.md",
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
    for phrase in ["小团队可以学什么", "小团队不要学什么", "迁移练习"]:
        if text.count(phrase) < 8:
            fail(f"case workbook lacks repeated section: {phrase}")


def check_public_pack() -> None:
    text = read("docs/public-content-pack.md")
    for section in REQUIRED_PUBLIC_PACK_SECTIONS:
        if section not in text:
            fail(f"public content pack missing section: {section}")


def check_site_links() -> None:
    html = read("site/index.html")
    local_links = re.findall(r'href="(\\.\\./[^"#]+)"', html)
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
    check_site_links()
    print("OK: learning hub package verification passed")


if __name__ == "__main__":
    main()

