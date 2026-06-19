# gaokao-major-intelligence

**数据驱动的高考志愿专业选择分析项目**  
A data-driven analysis framework for Chinese university major selection, targeting the 2026 高考 (Gaokao) cohort.

---

## What This Is

This project maps Chinese government research funding and education policy signals to undergraduate major choices. It answers one question: **given all available quantitative signals from the Chinese government and labor market, which university majors have the strongest long-term outlook for a 2026 high school graduate?**

The analysis combines four independent data dimensions:

| Dimension | Source | What It Measures |
|-----------|--------|-----------------|
| Basic Research Funding | NSFC (国家自然科学基金委) Annual Reports 2020–2024 | Where China funds its academic researchers; competition intensity by field |
| Strategic R&D Programs | MOST (科技部) Key R&D Plans & Major S&T Programs 2021–2026 | Technologies the government has designated as national strategic priorities |
| Higher Education Supply | MOE (教育部) Undergraduate Major Catalog 2026 | Which majors are being created vs. phased out; 10-year talent gap signals |
| Labor Market Pricing | MyCOS 2024 Graduate Survey + BOSS直聘/智联 2024–2025 | Starting salaries and employment rates by major at bachelor's level |

---

## Key Findings

| Major Field | Composite Score (0–10) | Tier |
|-------------|----------------------|------|
| 信息 — CS / AI / EE | **8.2** | ✅ Strong |
| 工程材料 — New Energy / Chips / Manufacturing | **7.6** | ✅ Strong |
| 数理 — Statistics / Applied Math | **4.5** | ⚠️ Depends on sub-field |
| 生命 — Bioengineering / Brain Science | **4.2** | ⚠️ Needs grad school |
| 地球 — Ocean / Environment / Deep Earth | **4.0** | ⚠️ Narrow path |
| 医学 — Clinical / Biomedical Engineering | **2.9** | ⚠️ Special track |
| 化学 — Chemical Engineering | **2.4** | ❌ Weak at bachelor's |
| 管理 — Management | **0.3** | ❌ Avoid |

Full analysis: [`report/2026_gaokao_major_selection_guide.md`](report/2026_gaokao_major_selection_guide.md)

---

## Repository Structure

```
gaokao-major-intelligence/
├── data/
│   ├── processed/              # Cleaned input datasets (CSV)
│   │   ├── nsfc_mianshang_2020_2024.csv      # NSFC grant data, 40 rows × 9 cols
│   │   ├── most_key_programs.csv              # 16 national R&D programs
│   │   ├── moe_major_trends.csv               # 25 MOE major add/remove signals
│   │   └── employment_salary_benchmarks.csv   # 16 major categories, MyCOS 2024
│   └── raw/                    # Source images (NSFC annual report JPEGs)
├── scripts/
│   ├── 02_analyze_nsfc.py      # NSFC pivot tables → output/tables/
│   ├── 03_visualize.py         # Base charts (chart1–chart6)
│   ├── 04_map_to_majors.py     # NSFC discipline → MOE major mapping
│   ├── 05_multi_source_analysis.py  # Four-dimension composite scorer
│   └── 06_extended_charts.py   # Extended charts (chartA–chartK)
├── output/
│   ├── figures/                # 17 PNG charts
│   └── tables/                 # 9 CSV analysis tables
├── report/
│   └── 2026_gaokao_major_selection_guide.md  # Main deliverable (871 lines)
├── EXECUTION_PLAN.md           # Original project plan
└── README.md
```

---

## How to Reproduce

**Requirements:** Python 3.10+, macOS/Linux

```bash
# 1. Clone
git clone https://github.com/yanxht/gaokao-major-intelligence.git
cd gaokao-major-intelligence

# 2. Install dependencies
pip install pandas matplotlib seaborn scikit-learn openpyxl

# 3. Run analysis pipeline in order
python3 scripts/02_analyze_nsfc.py       # generates output/tables/
python3 scripts/03_visualize.py          # generates chart1–chart6
python3 scripts/05_multi_source_analysis.py  # generates multisource_scorecard.csv
python3 scripts/06_extended_charts.py    # generates chartA–chartK
```

All outputs (tables + figures) are already committed. Re-running scripts will overwrite them with identical results.

---

## Data Sources & Freshness

| Dataset | Source | Latest Year | Notes |
|---------|--------|-------------|-------|
| NSFC 面上项目 | [nsfc.gov.cn annual reports](https://www.nsfc.gov.cn/p1/2991/ndbg.html) | **2024** | 2025 data not yet published as of 2026-06-18 |
| MOST Key R&D Programs | [service.most.gov.cn](https://service.most.gov.cn/kjjh_tztg_all/) | **2026** | Includes 2026 newly approved programs |
| MOE Major Catalog | [edu.cn](https://www.edu.cn/rd/gao_xiao_cheng_guo/gao_xiao_zi_xun/202604/t20260428_2731325.shtml) | **2026** | April 28, 2026 release; 38 new majors |
| Employment / Salary | MyCOS 《2024年中国大学生就业报告》 | **2024 cohort** | Most recent available; ~±15% on salary figures |

---

## Limitations

- NSFC data extracted from report images (AI vision reading); individual values ±1% accuracy
- Salary figures are national medians; actual outcomes vary significantly by school tier and city
- Four-dimension composite scores use subjective weights (see Section 1 of report)
- School-level recommendations are intentionally excluded — to be assessed post-score-release

---

## License

MIT — free to use, adapt, and share with attribution.
