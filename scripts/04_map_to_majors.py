#!/usr/bin/env python3
"""
Map NSFC disciplines → MOE undergraduate major catalog (2024版本科专业目录)
and produce ranked recommendations for a Shandong Gaokao 2026 graduate.
Score tier is unknown until results release; this script covers all tiers.
"""

import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent
OUT  = BASE / "output" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

# ──────────────────────────────────────────────────────────────────────────────
# 1. NSFC discipline → career signal score (composite of:
#    a) funding share stability  b) application growth  c) strategic importance
#    d) bachelor-level employability  e) industry demand alignment
# Score 1-10, 10 = strongest signal
# ──────────────────────────────────────────────────────────────────────────────

DISCIPLINE_SIGNALS = {
    "信息": {
        "nsfc_dept": "信息科学部",
        "funding_share_2024_pct": 10.87,
        "app_growth_2020_2024_pct": 51.1,
        "career_signal_score": 9.5,
        "notes": "CS/AI highest industry demand; NSFC + MOST both investing; "
                 "bachelor graduates highly employable",
        "risk": "Competitive, requires strong math/coding foundation",
    },
    "工程材料": {
        "nsfc_dept": "工程与材料科学部",
        "funding_share_2024_pct": 17.35,
        "app_growth_2020_2024_pct": 56.3,
        "career_signal_score": 8.5,
        "notes": "Largest NSFC dept by project count. New energy, semiconductors, "
                 "advanced manufacturing are strategic priorities (十四五)",
        "risk": "Broad field; career path varies widely by sub-field",
    },
    "生命": {
        "nsfc_dept": "生命科学部",
        "funding_share_2024_pct": 15.87,
        "app_growth_2020_2024_pct": 66.7,
        "career_signal_score": 7.0,
        "notes": "Biotech, synthetic biology, gene editing are growth areas. "
                 "Bachelor employability weaker; often needs grad school",
        "risk": "PhD usually required for research; biotech industry jobs growing "
                "but competitive. Consider 生物工程 or 生物医学工程 over pure biology",
    },
    "医学": {
        "nsfc_dept": "医学科学部",
        "funding_share_2024_pct": 22.64,
        "app_growth_2020_2024_pct": 53.7,
        "career_signal_score": 8.0,
        "notes": "Largest NSFC recipient but research acceptance rate is lowest (9%). "
                 "Clinical medicine has stable employment. AI+medicine converging.",
        "risk": "8-year MD program required for clinical track. Very competitive entry.",
    },
    "数理": {
        "nsfc_dept": "数学物理科学部",
        "funding_share_2024_pct": 9.32,
        "app_growth_2020_2024_pct": 65.9,
        "career_signal_score": 7.0,
        "notes": "Foundation for all STEM. Stats/applied math has strong industry demand. "
                 "Pure physics/math often requires PhD. Quantum tech is strategic.",
        "risk": "Pure track requires grad school. Applied track (stats, actuarial) "
                "has good bachelor-level jobs.",
    },
    "化学": {
        "nsfc_dept": "化学科学部",
        "funding_share_2024_pct": 9.98,
        "app_growth_2020_2024_pct": 70.4,
        "career_signal_score": 6.5,
        "notes": "New materials, batteries, drug synthesis are application areas. "
                 "Chemical engineering bridges theory to industry better than pure chemistry.",
        "risk": "Most research jobs require PhD. Chemical engineering more employable.",
    },
    "地球": {
        "nsfc_dept": "地球科学部",
        "funding_share_2024_pct": 10.61,
        "app_growth_2020_2024_pct": 72.1,
        "career_signal_score": 6.0,
        "notes": "Carbon neutrality drives demand in environmental science, "
                 "geoscience. China Ocean University (Qingdao) is world-class.",
        "risk": "Narrow career path at bachelor level; fewer industry options.",
    },
    "管理": {
        "nsfc_dept": "管理科学部",
        "funding_share_2024_pct": 3.36,
        "app_growth_2020_2024_pct": 19.4,
        "career_signal_score": 5.0,
        "notes": "Smallest NSFC dept, slowest growth. Management degrees oversupplied. "
                 "Data-driven management (信管、工管) is better than pure management.",
        "risk": "Oversupplied graduates. Not aligned with strategic priorities.",
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# 2. Major recommendations mapped to disciplines
# Format: MOE 专业名称, 专业代码, discipline bucket, career_track, tier
#   tier: A=Top10 schools, B=985/211, C=双一流/省重点, D=一般本科
# ──────────────────────────────────────────────────────────────────────────────

MAJORS = [
    # ── Information Sciences ──────────────────────────────────────────────────
    {
        "rank": 1,
        "major_cn": "计算机科学与技术",
        "major_code": "080901",
        "discipline": "信息",
        "career_track": "Software engineering, AI, systems",
        "shandong_schools": "山东大学, 中国石油大学(华东), 山东科技大学, 青岛大学",
        "signal_strength": "★★★★★",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Most versatile degree. Backend dev, AI, data eng all accessible at "
                 "bachelor level. Strongest funding tailwind from NSFC + MOST.",
    },
    {
        "rank": 2,
        "major_cn": "人工智能",
        "major_code": "080717T",
        "discipline": "信息",
        "career_track": "AI/ML engineering, research",
        "shandong_schools": "山东大学, 中国海洋大学, 山东科技大学",
        "signal_strength": "★★★★★",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "New major (2018+). Strong at top schools, variable quality elsewhere. "
                 "Choose CS if unsure — AI is a sub-field of CS.",
    },
    {
        "rank": 3,
        "major_cn": "数据科学与大数据技术",
        "major_code": "080910T",
        "discipline": "信息",
        "career_track": "Data analytics, ML, business intelligence",
        "shandong_schools": "山东大学, 山东财经大学, 山东师范大学",
        "signal_strength": "★★★★☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Good alternative if CS score is tight. Many programs vary in quality.",
    },
    {
        "rank": 4,
        "major_cn": "电子信息工程",
        "major_code": "080701",
        "discipline": "信息",
        "career_track": "Hardware-software interface, telecom, chips",
        "shandong_schools": "山东大学, 中国石油大学(华东), 青岛科技大学",
        "signal_strength": "★★★★☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Semiconductor wave (芯片) makes EE very strategic. "
                 "Bridges 信息 and 工程材料 fields.",
    },
    # ── Engineering & Materials ───────────────────────────────────────────────
    {
        "rank": 5,
        "major_cn": "新能源科学与工程",
        "major_code": "080503T",
        "discipline": "工程材料",
        "career_track": "Battery, solar, hydrogen energy",
        "shandong_schools": "山东大学, 中国石油大学(华东), 山东科技大学",
        "signal_strength": "★★★★★",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "碳中和 + 双碳目标 direct policy driver. Massive industry investment "
                 "in Shandong (宁德时代 supplier chain, wind/solar). Very strong 10-yr outlook.",
    },
    {
        "rank": 6,
        "major_cn": "材料科学与工程",
        "major_code": "080401",
        "discipline": "工程材料",
        "career_track": "Advanced materials, semiconductors, batteries",
        "shandong_schools": "山东大学, 山东科技大学, 青岛大学",
        "signal_strength": "★★★★☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Broad foundation. Sub-specializations in semiconductor, energy, "
                 "biomaterials all have strong funding.",
    },
    {
        "rank": 7,
        "major_cn": "机器人工程",
        "major_code": "080803T",
        "discipline": "工程材料",
        "career_track": "Robotics, automation, smart manufacturing",
        "shandong_schools": "山东大学, 山东科技大学, 哈尔滨工业大学(威海)",
        "signal_strength": "★★★★☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Manufacturing automation is a national priority (智能制造). "
                 "New major with growing programs.",
    },
    # ── Medical/Life Sciences ─────────────────────────────────────────────────
    {
        "rank": 8,
        "major_cn": "临床医学",
        "major_code": "100201K",
        "discipline": "医学",
        "career_track": "Doctor (5+3 = 8 year track)",
        "shandong_schools": "山东大学, 青岛大学医学院, 山东中医药大学",
        "signal_strength": "★★★★☆",
        "bachelor_employable": False,  # requires 5yr+3yr=8yr
        "grad_school_bonus": True,
        "notes": "Highly stable career. NSFC medical funding is largest. "
                 "Requires 5+3 (本博连读) or 5yr undergrad + 3yr clinical residency. "
                 "Score requirement is HIGH. Choose if he genuinely wants to be a doctor.",
    },
    {
        "rank": 9,
        "major_cn": "生物医学工程",
        "major_code": "080601",
        "discipline": "生命",
        "career_track": "Medical devices, bioinformatics, drug tech",
        "shandong_schools": "山东大学, 山东科技大学",
        "signal_strength": "★★★★☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Bridges life sciences + engineering. Medical devices market growing. "
                 "Better employment than pure biology at bachelor level.",
    },
    {
        "rank": 10,
        "major_cn": "生物工程",
        "major_code": "083001",
        "discipline": "生命",
        "career_track": "Biotech, pharma, synthetic biology",
        "shandong_schools": "山东大学, 中国石油大学(华东), 青岛科技大学",
        "signal_strength": "★★★☆☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Synthetic biology is NSFC + MOST strategic priority. "
                 "Industry track needs pharma/biotech proximity. "
                 "Consider grad school to unlock better positions.",
    },
    # ── Statistics/Math Applied ───────────────────────────────────────────────
    {
        "rank": 11,
        "major_cn": "统计学",
        "major_code": "071201",
        "discipline": "数理",
        "career_track": "Finance, data science, actuarial, quant research",
        "shandong_schools": "山东大学, 山东财经大学, 山东师范大学",
        "signal_strength": "★★★★☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Highly versatile. Applied math backbone for AI/finance/bio. "
                 "Strong quantitative foundation opens many doors. "
                 "Can pivot to almost any field for grad school.",
    },
    # ── Environmental/Earth ───────────────────────────────────────────────────
    {
        "rank": 12,
        "major_cn": "海洋科学",
        "major_code": "070701",
        "discipline": "地球",
        "career_track": "Marine research, oceanic engineering",
        "shandong_schools": "中国海洋大学 (世界一流/A+学科), 山东大学",
        "signal_strength": "★★★★☆",
        "bachelor_employable": True,
        "grad_school_bonus": True,
        "notes": "Shandong-specific advantage: 中国海洋大学 (Qingdao) is world-leading. "
                 "Marine economy is a Shandong provincial strategic priority. "
                 "Good option if score reaches 中海大 threshold (~山东600+).",
    },
    {
        "rank": 13,
        "major_cn": "环境科学与工程",
        "major_code": "082501",
        "discipline": "地球",
        "career_track": "Environmental consulting, carbon auditing, govt",
        "shandong_schools": "山东大学, 青岛大学, 山东科技大学",
        "signal_strength": "★★★☆☆",
        "bachelor_employable": True,
        "grad_school_bonus": False,
        "notes": "Carbon neutrality creates government and consulting demand. "
                 "But lower salary ceiling than engineering disciplines.",
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# 3. Score-tier → recommended majors mapping
# ──────────────────────────────────────────────────────────────────────────────

TIER_GUIDANCE = {
    "Tier-1 (山东~660+, 985 schools)": {
        "accessible_schools": ["山东大学", "中国海洋大学", "哈工大威海", "北师大", "浙大", "复旦"],
        "top_picks": ["计算机科学与技术", "人工智能", "电子信息工程", "统计学", "生物医学工程"],
        "reasoning": "At this tier, prioritize the major over the school brand for "
                     "top-10 schools. CS/EE at 山大 > Management at 复旦 for career outcomes.",
    },
    "Tier-2 (山东~600-660, 双一流/211)": {
        "accessible_schools": ["中国石油大学华东", "山东科技大学", "青岛大学"],
        "top_picks": ["计算机科学与技术", "新能源科学与工程", "数据科学与大数据技术",
                      "材料科学与工程", "机器人工程"],
        "reasoning": "At strong local 211s, engineering programs with industry "
                     "partnerships (特别是新能源、材料) are very strong. "
                     "CS at a 211 > CS at a tier-3 school.",
    },
    "Tier-3 (山东~550-600, 省重点)": {
        "accessible_schools": ["山东建筑大学", "山东农业大学", "青岛科技大学", "山东理工大学"],
        "top_picks": ["计算机科学与技术", "电子信息工程", "新能源科学与工程", "生物工程"],
        "reasoning": "Choose schools with strong industry ties in Shandong's "
                     "industrial clusters (青岛科技/化工, 山东农大/农业科技). "
                     "Employability > brand at this tier.",
    },
}

# ──────────────────────────────────────────────────────────────────────────────
# 4. Output tables
# ──────────────────────────────────────────────────────────────────────────────

majors_df = pd.DataFrame(MAJORS)
majors_df.to_csv(OUT / "major_recommendations.csv", index=False, encoding="utf-8-sig")

signals_df = pd.DataFrame([
    {"discipline": k,
     "nsfc_dept": v["nsfc_dept"],
     "funding_share_2024_pct": v["funding_share_2024_pct"],
     "app_growth_2020_2024_pct": v["app_growth_2020_2024_pct"],
     "career_signal_score_10": v["career_signal_score"],
     "notes": v["notes"],
     "risk": v["risk"]}
    for k, v in DISCIPLINE_SIGNALS.items()
]).sort_values("career_signal_score_10", ascending=False)
signals_df.to_csv(OUT / "discipline_signals.csv", index=False, encoding="utf-8-sig")

print("=== Discipline Career Signal Scores ===")
for _, row in signals_df.iterrows():
    print(f"\n{row['discipline']} [{row['career_signal_score_10']}/10]")
    print(f"  Funding share 2024: {row['funding_share_2024_pct']}%  |  "
          f"Application growth: +{row['app_growth_2020_2024_pct']}%")
    print(f"  Notes: {row['notes']}")
    print(f"  Risk:  {row['risk']}")

print("\n\n=== Top 13 Major Recommendations ===")
for _, m in majors_df.iterrows():
    print(f"\n#{m['rank']} {m['major_cn']} ({m['major_code']}) {m['signal_strength']}")
    print(f"  Discipline: {m['discipline']}  |  Bachelor-level: {'Yes' if m['bachelor_employable'] else 'No (requires grad school)'}")
    print(f"  Shandong schools: {m['shandong_schools']}")
    print(f"  Notes: {m['notes']}")

print("\n\n=== Score-Tier Guidance ===")
for tier, info in TIER_GUIDANCE.items():
    print(f"\n{tier}")
    print(f"  Top picks: {', '.join(info['top_picks'])}")
    print(f"  Reasoning: {info['reasoning']}")

print(f"\nAll tables saved to {OUT}")
