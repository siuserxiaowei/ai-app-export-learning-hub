# QA Report

状态：通过追加验收。

验收日期：2026-06-02

## 验收范围

- Markdown 资料库
- 合规双语学习稿
- 原目标覆盖矩阵
- 品牌拆解手册
- 最终完成度审计
- 机会评分表 CSV
- 静态学习网站
- 交付索引和入口说明

## 完成项

- 已将 `main` 合并到 `agent/qa-polish`，合并方式为 fast-forward。
- Required files 共 17 项全部存在：入口说明、交付索引、QA 报告、9 份核心 docs、CSV、静态站三件套和验证脚本。
- 新增 `docs/bilingual-study-note.md`，用中文学习稿、英文学习译稿、术语表和课堂练习替代不可交付的完整逐字稿/逐句译文。
- 新增 `docs/goal-coverage-matrix.md`，逐项说明原始目标、当前交付证据、完成状态和版权限制。
- 新增 `docs/brand-teardown-handbook.md`，独立拆解 AI App 出海品牌的命名、首页、信任层、定价、传播钩子和 10 个品牌样本。
- 新增 `docs/final-completion-audit.md`，逐项审计原始目标、当前证据、线上链接、验证命令和不能声明完成的版权受限部分。
- `data/opportunity-scorecard.csv` 可由 Python `csv.DictReader` 正常解析，含 10 行机会记录和必需字段。
- `site/index.html` 的本地 `href`/`src` 目标均存在，站内锚点均能解析到页面内 `id`。
- Markdown 本地链接可解析到目标文件。
- 内容风险搜索未发现完整逐字稿、完整逐句翻译、明显误听词或不适合对外交付的内部备忘录语气。
- 修复了两类引用链接：Lovart 旧路径返回 404，MyFitnessPal/Cal AI 收购引用改为 GlobeNewswire 原始发布页。
- 修复了 `README.md` 中静态站打开命令的过期 worktree 绝对路径，改为包内相对路径。
- 6 个 agent worktree 已合并回 `main` 并回收；分支记录保留，便于后续追溯。
- 追加更新了 RevenueCat 2026、Lovart、Photoroom、Gamma、HeyGen、ElevenLabs 等参考链接。

## 版权边界

- 不输出完整视频逐字稿。
- 不输出完整逐句翻译。
- 仅使用短摘录、分段转述、英文摘要、教学化分析和公开来源引用。
- 对外发布时不将资料包包装成原作者授权课程、官方译文或源视频复刻稿。

## 验证命令

```bash
git fetch
git merge main
python3 scripts/verify_package.py
python3 - <<'PY'
from pathlib import Path
required = [
    'README.md', 'DELIVERY_INDEX.md', 'QA_REPORT.md',
    'docs/source-brief.md', 'docs/learning-guide.md', 'docs/public-content-pack.md',
    'docs/bilingual-study-note.md', 'docs/goal-coverage-matrix.md',
    'docs/final-completion-audit.md',
    'docs/brand-teardown-handbook.md',
    'docs/case-study-workbook.md', 'docs/7-day-learning-plan.md', 'docs/facilitator-guide.md',
    'data/opportunity-scorecard.csv', 'site/index.html', 'site/styles.css', 'site/app.js',
]
missing = [path for path in required if not Path(path).exists()]
print('required files checked:', len(required))
print('missing:', missing or 'none')
PY
python3 - <<'PY'
import csv
from pathlib import Path
with Path('data/opportunity-scorecard.csv').open(newline='', encoding='utf-8') as handle:
    rows = list(csv.DictReader(handle))
print('rows:', len(rows))
print('columns:', ', '.join(rows[0].keys()))
PY
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
root = Path.cwd()
site = root / 'site'
html = (site / 'index.html').read_text(encoding='utf-8')
class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.links.append((tag, attr, attrs[attr]))
parser = Parser()
parser.feed(html)
missing = []
fragment_missing = []
file_link_count = 0
fragment_count = 0
for tag, attr, raw in parser.links:
    parsed = urlparse(raw)
    url = raw.split('#', 1)[0].split('?', 1)[0]
    if parsed.fragment and not parsed.scheme:
        fragment_count += 1
        if parsed.fragment not in parser.ids:
            fragment_missing.append(raw)
    if not url or parsed.scheme or url.startswith('//') or url.startswith('mailto:') or url.startswith('tel:'):
        continue
    file_link_count += 1
    target = (site / unquote(url)).resolve()
    if not target.exists():
        missing.append(raw)
print('site local href/src checked:', file_link_count)
print('site fragment links checked:', fragment_count)
print('missing local targets:', missing or 'none')
print('missing fragments:', fragment_missing or 'none')
PY
python3 - <<'PY'
from pathlib import Path
from urllib.parse import urlparse, unquote
import re
root = Path.cwd()
missing = []
count = 0
for path in sorted(root.glob('*.md')) + sorted((root / 'docs').glob('*.md')):
    text = path.read_text(encoding='utf-8')
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', text):
        raw = match.group(1).strip()
        url = raw.split('#', 1)[0].split('?', 1)[0]
        parsed = urlparse(url)
        if not url or parsed.scheme or url.startswith('//') or url.startswith('mailto:'):
            continue
        count += 1
        target = (path.parent / unquote(url)).resolve()
        if not target.exists():
            missing.append((path, raw))
print('markdown local links checked:', count)
print('missing markdown links:', missing or 'none')
PY
rg -n "逐字|逐句|全文|完整.*(翻译|译文|转写|字幕|逐字稿)|transcript|translation|原文|字幕|内部|备忘|memo|confidential|not for" README.md DELIVERY_INDEX.md QA_REPORT.md docs site data
rg -n "^[0-9]{1,2}:[0-9]{2}|^[0-9]{2}:[0-9]{2}|\[[0-9]{1,2}:[0-9]{2}\]|Speaker|主持人|采访者|受访者|雷子：|雷子:" docs README.md DELIVERY_INDEX.md QA_REPORT.md site
git worktree list
```

## 验证结果

- `python3 scripts/verify_package.py` 输出：`OK: learning hub package verification passed`。
- Required files 检查输出：17 项，missing 为 `none`。
- CSV 检查输出：10 行，字段包括 `opportunity`、`target_user`、`job_to_be_done`、`opportunity_score` 等。
- 静态站本地链接检查：17 个本地 `href`/`src` 均存在；8 个站内锚点均存在。
- Markdown 本地链接检查：25 个本地链接均存在。
- 核心外部来源轻量检查：RevenueCat 2026、Sensor Tower、GlobeNewswire、Photoroom、Gamma、HeyGen 均返回 200；ElevenLabs 返回 308 跳转；Lovart 页面经浏览器/web 打开可读，但普通脚本请求返回 404，记录为站点请求方式差异。
- 内容风险搜索只命中版权边界说明、正常时间轴摘要、字幕/翻译作为产品功能描述，以及“内部”作为交接/团队场景描述；验证脚本内维护的已知误听词列表未命中交付内容。
- `git worktree list` 仅保留主仓库工作区，临时 agent worktree 已清理。

## 遗留限制

- 外部网页链接已做轻量存活检查并修复发现的问题，但第三方站点未来仍可能改版、跳转、限流或失效。
- 本次 QA 未重新下载、重转写或逐字复核原始视频；验收基于仓库内已交付内容和公开引用链接。
- 市场数据、收入数字和政策条款只做引用链接可访问性与资料边界检查，未展开二次事实审计。
