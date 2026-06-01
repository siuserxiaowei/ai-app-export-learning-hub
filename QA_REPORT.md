# QA Report

状态：初始模板，最终验收时更新。

## 验收范围

- Markdown 资料库
- 机会评分表 CSV
- 静态学习网站
- 交付索引和入口说明

## 版权边界

- 不输出完整视频逐字稿。
- 不输出完整逐句翻译。
- 使用短摘录、分段转述、英文摘要和教学化分析。

## 待运行验证

```bash
find . -maxdepth 3 -type f | sort
python3 - <<'PY'
import csv
rows=list(csv.DictReader(open('data/opportunity-scorecard.csv')))
print(len(rows))
PY
python3 scripts/verify_package.py
```
