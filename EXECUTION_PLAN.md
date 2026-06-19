# China Research Fund Analysis — Execution Plan
> Goal: Help a Shandong Gaokao graduate make an informed college major decision  
> by mapping government research funding patterns to undergraduate opportunities.  
> Last updated: 2026-06-18

---

## 1. Proposal Evaluation

### What the approach gets right
- **Research funding is a leading indicator.** Where the government pours money today shapes which industries hire, which labs expand, and which careers command premium salaries 5–10 years from now — exactly when your nephew will enter the workforce.
- **NSFC data is authoritative and public.** The National Natural Science Foundation of China publishes annual statistical reports with discipline-level breakdowns going back a decade. This is the cleanest structured source available.
- **Government signal is especially strong in China.** Unlike market economies where private R&D often diverges from public funding, in China the Five-Year Plans, NSFC priorities, and industrial policy are tightly coupled. Following the money here is unusually predictive.

### Limitations to call out explicitly
| Limitation | Mitigation in this plan |
|---|---|
| Basic research ≠ jobs (a heavily funded physics field may require a PhD to participate) | Layer in job-market data and salary data alongside funding data |
| Funding today → jobs in 5–10 years; some fields may peak before he graduates | Focus on trend slope (is the field growing?) not just absolute size |
| His score tier will constrain accessible schools and majors | Defer school/major shortlisting to Phase 3 after score release |
| NSFC covers basic science; applied/engineering funded differently | Add MOST National Key R&D Program data as a second source |

### Verdict
Sound approach. Execute it in three phases: **collect → analyze → translate to majors**. Keep the output practical — not a research paper, but a decision brief he can use during 志愿填报.

---

## 2. Data Sources

### Primary: NSFC (国家自然科学基金委员会)
- **URL**: https://www.nsfc.gov.cn/publish/portal0/tab434/
- **What it contains**: Annual statistical reports with project counts, funded amounts, and institutional distribution broken down by the 8 science departments:
  1. 数学与物理科学 (Math & Physics)
  2. 化学科学 (Chemistry)
  3. 生命科学 (Life Sciences)
  4. 地球科学 (Earth Sciences)
  5. 工程与材料科学 (Engineering & Materials)
  6. 信息科学 (Information Sciences)
  7. 管理科学 (Management Sciences)
  8. 医学科学 (Medical Sciences)
- **Years to collect**: 2020–2024 (5-year window covers two plan cycles)
- **Format**: PDF annual reports + some web-scraped tables

### Secondary: MOST National Key R&D Programs (科技部重点研发计划)
- **URL**: https://service.most.gov.cn/kjjh_tztg_all/
- **What it contains**: Applied/translational research program funding by strategic area (AI, new energy, biotech, advanced manufacturing, etc.)
- **Why include it**: Complements NSFC's basic-research view with industry-facing priorities

### Tertiary: Five-Year Plan Priority Areas (国家"十四五"规划)
- Source: Published by NDRC, Xinhua
- Captures declared strategic intent; use as qualitative validation layer

### Job Market Validation (optional Phase 3 enrichment)
- 智联招聘 / 前程无忧 salary index by major — to confirm funding → employability translation
- 麦可思研究院 (MyCOS) annual graduate employment reports — tracks salary, employment rate, and satisfaction by major

---

## 3. Execution Phases

### Phase 1 — Data Collection (Days 1–3)

**Deliverables**: Raw data files in `data/raw/`

**Tasks**:
1. Download NSFC annual reports 2020–2024 (PDF + any web tables)
2. Extract discipline-level funding tables from PDFs (Python: `pdfplumber`)
3. Scrape MOST Key R&D program list by focus area and year
4. Save all raw files with provenance metadata (source URL, download date)

**Script**: `scripts/01_collect_data.py`  
**Output**: `data/raw/nsfc_YYYY.pdf`, `data/raw/nsfc_YYYY_tables.csv`, `data/raw/most_krd_YYYY.csv`

---

### Phase 2 — Analysis & Visualization (Days 3–5)

**Deliverables**: Charts and summary tables in `output/`

**Tasks**:
1. **Trend analysis**: Total funding by discipline, 2020–2024 — absolute values and YoY growth rates
2. **Growth ranking**: Which disciplines are growing fastest? Which are declining?
3. **Share shift**: Is the funding pie shifting (e.g., info sciences eating share from traditional sciences)?
4. **Sub-field drill-down**: Within top-3 disciplines, identify the hot sub-fields (NSFC reports list key programs)
5. **MOST cross-check**: Map MOST strategic programs back to NSFC discipline buckets; flag where both signals align (= strong conviction fields)

**Scripts**: `scripts/02_analyze_nsfc.py`, `scripts/03_visualize.py`  
**Key charts**:
- Stacked bar: funding by discipline × year
- Line chart: YoY growth rates by discipline
- Heatmap: discipline × year (normalized share)
- Bubble chart: funding volume vs. growth rate (size = absolute amount)

**Output**: `output/figures/`, `output/tables/summary_by_discipline.csv`

---

### Phase 3 — Major Mapping & Decision Brief (Days 5–7, after score release)

**Deliverables**: `report/decision_brief.md` — a 1–2 page practical guide

**Tasks**:
1. Map top research fields → specific 专业目录 (MOE undergraduate major catalog) entries
2. Filter majors by: (a) offered in Shandong-reachable universities, (b) accessible at his score tier
3. For each shortlisted major, note: funding tailwind strength, typical career paths, PhD-required vs. bachelor-level accessible
4. Flag majors to avoid: oversupplied fields, fields where funding peaked/declining
5. Draft a "top picks" table with rationale + 2–3 backup alternatives

**Script**: `scripts/04_map_to_majors.py` (static mapping table, manually curated)  
**Output**: `report/decision_brief.md`

---

## 4. Project Structure

```
china_research_fund/
├── EXECUTION_PLAN.md          ← this file
├── README.md                  ← one-paragraph summary for quick orientation
├── data/
│   ├── raw/                   ← untouched source files (PDFs, CSVs)
│   └── processed/             ← cleaned/normalized datasets
├── scripts/
│   ├── 01_collect_data.py
│   ├── 02_analyze_nsfc.py
│   ├── 03_visualize.py
│   └── 04_map_to_majors.py
├── output/
│   ├── figures/               ← charts (PNG/HTML)
│   └── tables/                ← summary CSVs
└── report/
    └── decision_brief.md      ← the actual deliverable for your nephew
```

---

## 5. Key Hypotheses to Test

These are the questions the analysis should answer or falsify:

1. **Information Sciences (CS/AI/EE) is growing fastest** — expected, but by how much vs. Life Sciences?
2. **Medical Sciences is large but slowing** — post-COVID normalization?
3. **New materials and green energy are emerging within Engineering & Materials** — aligned with 碳中和 policy
4. **Management Sciences is small and shrinking** — less useful as a funding signal
5. **Is the signal concentrated in a few sub-fields within each discipline**, or broadly distributed?

---

## 6. Caveats for Your Nephew

Include these in the decision brief:

- **Score tier first, then major.** A great major at a tier-3 school is almost always worse than a solid major at a tier-1 school. Don't let funding data override school quality.
- **Not all high-funded fields are bachelor-friendly.** Basic physics and chemistry research careers typically require a PhD. If he wants to work at 22, he needs engineering/applied fields.
- **Emerging fields may have thin enrollment yet.** Some AI-adjacent or biotech majors at provincial schools may be new programs with unproven faculty and employment tracks. Check 就业率 data.
- **Flexibility matters.** Majors like Computer Science, Electrical Engineering, and Statistics have high research funding AND broad employability — they hedge across multiple futures.
- **Graduate school optionality.** If he has any interest in grad school, he can choose a more foundational major and specialize later. If he wants to work directly after graduation, choose an applied engineering track.

---

## 7. Immediate Next Steps

- [ ] Confirm Python environment is set up (`pdfplumber`, `pandas`, `matplotlib`, `requests`)
- [ ] Manually download the NSFC 2023 annual report to verify table structure before scripting
- [ ] Run Phase 1 scripts to collect 2020–2024 data
- [ ] Review Phase 2 output charts together before drafting the decision brief
- [ ] Wait for score release → run Phase 3 with actual score context
