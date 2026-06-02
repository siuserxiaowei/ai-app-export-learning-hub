#!/usr/bin/env python3
from __future__ import annotations

import csv
from html.parser import HTMLParser
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "DELIVERY_INDEX.md",
    "QA_REPORT.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "ATTRIBUTION.md",
    "CNAME",
    "ads.txt.template",
    "docs/source-brief.md",
    "docs/bilingual-study-note.md",
    "docs/goal-coverage-matrix.md",
    "docs/final-completion-audit.md",
    "docs/authorized-transcript-workflow.md",
    "docs/research-evidence-register.md",
    "docs/knowledge-source-register.md",
    "docs/google-ads-and-adsense-setup.md",
    "docs/google-ads-campaign-plan.md",
    "docs/opc-app-playbook.md",
    "docs/learning-guide.md",
    "docs/public-content-pack.md",
    "docs/case-study-workbook.md",
    "docs/brand-teardown-handbook.md",
    "docs/7-day-learning-plan.md",
    "docs/facilitator-guide.md",
    "data/opportunity-scorecard.csv",
    "site/index.html",
    "site/privacy.html",
    "site/terms.html",
    "site/styles.css",
    "site/app.js",
    "site/google-ads-config.js",
    "site/google-ads-config.example.js",
    "site/tracking.js",
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


def check_knowledge_source_register() -> None:
    text = read("docs/knowledge-source-register.md")
    required = [
        "最后核查日期：2026-06-02",
        "来源等级",
        "当前登记来源",
        "提示词资产化登记",
        "上线修复项",
        "HTTPS 证书",
        "Apple App Review Guidelines",
        "Google Play AI-Generated Content policy",
        "RevenueCat State of Subscription Apps 2026",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"knowledge source register missing phrase: {phrase}")


def check_opc_app_playbook() -> None:
    text = read("docs/opc-app-playbook.md")
    required = [
        "筛选原则",
        "方向 1：Etsy / TikTok Shop Listing Video Kit",
        "方向 2：InterviewLoop",
        "方向 3：ClientBriefAI",
        "推荐优先级",
        "选方向模板",
        "最小落地页文案模板",
    ]
    for phrase in required:
        if phrase not in text:
            fail(f"opc app playbook missing phrase: {phrase}")


def check_site_knowledge_base() -> None:
    html = read("site/index.html")
    js = read("site/app.js")

    required_html = [
        'id="knowledge"',
        'id="knowledgeSearch"',
        'id="tagFilters"',
        'id="topicRail"',
        'id="topicDetail"',
        'id="knowledgeGrid"',
        'id="web-library"',
        'id="webLibraryGrid"',
        'id="webLibraryCount"',
        'id="prompt-system"',
        "App 出海知识库",
        "网页资料馆",
        "把外部网页整理成能用的判断",
        "提示词资产",
        "深度资料库",
        "最后核查：2026-06-02",
    ]
    for phrase in required_html:
        if phrase not in html:
            fail(f"site knowledge base missing html phrase: {phrase}")

    required_topic_ids = [
        'id: "market"',
        'id: "validation"',
        'id: "cases"',
        'id: "compliance"',
        'id: "privacy"',
        'id: "aso"',
        'id: "monetization"',
        'id: "growth"',
    ]
    for topic_id in required_topic_ids:
        if topic_id not in js:
            fail(f"site knowledge base missing topic: {topic_id}")

    required_js = [
        'const lastVerifiedDate = "2026-06-02"',
        "renderKnowledge",
        "renderWebLibrary",
        "makeWebPageCard",
        "makeKnowledgeCard",
        "knowledgeSearch.addEventListener",
        "提示词传承模板",
        "把提示词当业务流程，不当神秘咒语",
        "RevenueCat：Subscription Apps 2026",
    ]
    for phrase in required_js:
        if phrase not in js:
            fail(f"site knowledge base missing js phrase: {phrase}")

    verified_count = js.count("verified: lastVerifiedDate")
    if verified_count != 36:
        fail(f"site knowledge base should have 24 cards and 12 web pages, got {verified_count} verified items")

    web_page_count = js.count("whyRead:")
    if web_page_count != 12:
        fail(f"site web library should have 12 curated pages, got {web_page_count}")


def check_site_links() -> None:
    class Parser(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.links: list[str] = []
            self.ids: set[str] = set()

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            attrs_dict = dict(attrs)
            if attrs_dict.get("id"):
                self.ids.add(attrs_dict["id"] or "")
            for attr in ("href", "src"):
                if attrs_dict.get(attr):
                    self.links.append(attrs_dict[attr] or "")

    for html_path in ["site/index.html", "site/privacy.html", "site/terms.html"]:
        html = read(html_path)
        parser = Parser()
        parser.feed(html)
        site_dir = ROOT / "site"
        for raw in parser.links:
            parsed = urlparse(raw)
            target_without_fragment = raw.split("#", 1)[0].split("?", 1)[0]
            if parsed.fragment and not parsed.scheme and not target_without_fragment:
                if parsed.fragment not in parser.ids:
                    fail(f"{html_path} missing fragment target: {raw}")
            if (
                not target_without_fragment
                or parsed.scheme
                or raw.startswith("//")
                or raw.startswith("mailto:")
                or raw.startswith("tel:")
            ):
                continue
            target = (site_dir / unquote(target_without_fragment)).resolve()
            if not target.exists():
                fail(f"{html_path} local link target missing: {raw}")

    html = read("site/index.html")
    for required in [
        "学习路径",
        "核心结论",
        "竞品",
        "知识库",
        "网页资料馆",
        "提示词资产",
        "深度资料库",
        "Privacy",
        "Terms",
        "GitHub",
        "License",
    ]:
        if required not in html:
            fail(f"site missing required visible text: {required}")


def check_open_source_and_ads_readiness() -> None:
    license_text = read("LICENSE")
    if "CC BY 4.0" not in license_text or "creativecommons.org/licenses/by/4.0" not in license_text:
        fail("LICENSE does not clearly declare CC BY 4.0")

    cname = read("CNAME").strip()
    if cname != "gptimage2.store":
        fail(f"CNAME should be gptimage2.store, got {cname!r}")

    readme = read("README.md")
    for phrase in ["开源协议", "广告和隐私说明", "https://gptimage2.store/"]:
        if phrase not in readme:
            fail(f"README missing open-source/ads phrase: {phrase}")

    live_config = read("site/google-ads-config.js")
    if "enabled: false" not in live_config:
        fail("live Google Ads config must default to enabled: false")
    for forbidden in ["AW-YOUR_CONVERSION_ID", "YOUR_START_LEARNING_LABEL", "YOUR_SCORECARD_LABEL"]:
        if forbidden in live_config:
            fail(f"live Google Ads config contains placeholder: {forbidden}")

    tracking = read("site/tracking.js")
    for required in ["enabled === true", "data-conversion", "gtag/js", "learningHubTrackConversion"]:
        if required not in tracking:
            fail(f"tracking.js missing required phrase: {required}")

    html = read("site/index.html")
    for conversion in ["startLearning", "downloadScorecard", "openGithub", "openOpcPlaybook"]:
        if f'data-conversion="{conversion}"' not in html:
            fail(f"site missing conversion marker: {conversion}")

    ads_template = read("ads.txt.template").strip()
    if ads_template != "google.com, pub-YOUR_PUBLISHER_ID, DIRECT, f08c47fec0942fa0":
        fail("ads.txt.template does not match expected Google AdSense template")


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
    check_knowledge_source_register()
    check_opc_app_playbook()
    check_site_knowledge_base()
    check_site_links()
    check_open_source_and_ads_readiness()
    print("OK: learning hub package verification passed")


if __name__ == "__main__":
    main()
