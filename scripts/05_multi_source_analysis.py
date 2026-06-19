#!/usr/bin/env python3
"""
Multi-source analysis: NSFC + MOST + MOE + Employment data
Produces a unified field-level scorecard
"""
import pandas as pd
from pathlib import Path

BASE = Path(__file__).parent.parent
DATA = BASE / "data" / "processed"
OUT  = BASE / "output" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load all sources ──────────────────────────────────────────────────────────
nsfc = pd.read_csv(DATA / "nsfc_mianshang_2020_2024.csv")
most = pd.read_csv(DATA / "most_key_programs.csv")
moe  = pd.read_csv(DATA / "moe_major_trends.csv", on_bad_lines="skip")
emp  = pd.read_csv(DATA / "employment_salary_benchmarks.csv")

# ── NSFC dimension: 5-year trend signal ───────────────────────────────────────
DEPT_LABELS = {
    "数学物理科学部": "数理", "化学科学部": "化学", "生命科学部": "生命",
    "地球科学部": "地球", "工程与材料科学部": "工程材料",
    "信息科学部": "信息", "管理科学部": "管理", "医学科学部": "医学",
}
nsfc["dept_short"] = nsfc["dept_name_cn"].map(DEPT_LABELS)

# Application growth 2020→2024 = researcher talent flow into field
nsfc_signal = {}
for dept in nsfc["dept_short"].unique():
    sub = nsfc[nsfc["dept_short"] == dept]
    apps_2020 = sub[sub["year"] == 2020]["applications"].values[0]
    apps_2024 = sub[sub["year"] == 2024]["applications"].values[0]
    fund_2024 = sub[sub["year"] == 2024]["funding_wan"].values[0]
    fund_share = sub[sub["year"] == 2024]["funding_wan"].values[0] / \
        nsfc[nsfc["year"] == 2024]["funding_wan"].sum() * 100
    nsfc_signal[dept] = {
        "nsfc_talent_inflow_pct": round((apps_2024 - apps_2020) / apps_2020 * 100, 1),
        "nsfc_funding_share_2024_pct": round(fund_share, 2),
    }

# ── MOST dimension: how many active strategic programs per field area ─────────
most["fields"] = most["undergraduate_relevance"].str.split("/")
area_program_counts = {}
area_map = {
    "计算机": "信息", "AI": "信息", "电子信息": "信息", "软件工程": "信息",
    "生命科学": "生命", "生物工程": "生命", "生物医药": "医学",
    "医学": "医学", "药学": "医学",
    "材料": "工程材料", "微电子": "工程材料", "机械工程": "工程材料",
    "新能源": "工程材料", "储能": "工程材料", "精密制造": "工程材料",
    "化学": "化学",
    "物理": "数理", "量子技术": "数理",
    "地质工程": "地球", "资源勘探": "地球", "深地科学": "地球", "环境科学与工程": "地球",
    "脑机科学与技术": "生命",
}
for _, row in most.iterrows():
    for field in str(row.get("undergraduate_relevance", "")).split("/"):
        field = field.strip().rstrip('"')
        dept = area_map.get(field.split("(")[0].strip())
        if dept:
            area_program_counts[dept] = area_program_counts.get(dept, 0) + 1

# ── MOE dimension: new majors pointing to field (higher-ed planning signal) ──
moe_new = moe[moe["added_or_removed"].str.contains("新增|扩张", na=False)]
moe_field_map = {
    "具身智能": "信息", "脑机科学与技术": "生命", "生物制造": "生命",
    "能源科学与工程": "工程材料", "深地科学与工程": "地球", "农业机器人": "工程材料",
    "商业人工智能": "信息", "交通能源融合工程": "工程材料", "未来机器人": "工程材料",
    "人工智能": "信息", "新能源科学与工程": "工程材料",
    "数据科学与大数据技术": "信息", "集成电路设计与集成系统": "工程材料",
    "智能制造工程": "工程材料", "机器人工程": "工程材料",
    "生物医学工程": "生命", "碳储科学与工程": "地球",
}
moe_dept_counts = {}
for _, row in moe_new.iterrows():
    dept = moe_field_map.get(row["major_cn"].strip())
    if dept:
        stars = str(row.get("policy_signal", "")).count("★")
        moe_dept_counts[dept] = moe_dept_counts.get(dept, 0) + stars

# ── Employment dimension: average salary by NSFC dept cluster ────────────────
emp_by_dept = {
    "信息":    {"avg_salary": 10000, "employment_rate": 95.5, "bachelor_ok": True},
    "工程材料": {"avg_salary": 8000,  "employment_rate": 92.5, "bachelor_ok": True},
    "医学":    {"avg_salary": 6500,  "employment_rate": 89.0, "bachelor_ok": False},
    "生命":    {"avg_salary": 5800,  "employment_rate": 86.5, "bachelor_ok": False},
    "数理":    {"avg_salary": 8500,  "employment_rate": 91.0, "bachelor_ok": "mixed"},
    "化学":    {"avg_salary": 6000,  "employment_rate": 87.0, "bachelor_ok": False},
    "地球":    {"avg_salary": 6500,  "employment_rate": 88.5, "bachelor_ok": "mixed"},
    "管理":    {"avg_salary": 6000,  "employment_rate": 87.5, "bachelor_ok": True},
}

# ── Unified scorecard ─────────────────────────────────────────────────────────
depts = ["信息", "工程材料", "医学", "生命", "数理", "化学", "地球", "管理"]
rows = []
for d in depts:
    ns = nsfc_signal.get(d, {})
    em = emp_by_dept.get(d, {})
    rows.append({
        "学科领域": d,
        "NSFC资金占比2024(%)": ns.get("nsfc_funding_share_2024_pct", 0),
        "NSFC申请增长2020→2024(%)": ns.get("nsfc_talent_inflow_pct", 0),
        "MOST活跃专项数": area_program_counts.get(d, 0),
        "MOE新专业信号强度": moe_dept_counts.get(d, 0),
        "应届平均月薪(元)": em.get("avg_salary", 0),
        "就业率(%)": em.get("employment_rate", 0),
        "本科可就业": em.get("bachelor_ok", False),
    })

scorecard = pd.DataFrame(rows)

# Composite score (normalized 0-10 across 5 dimensions):
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 10))
score_cols = ["NSFC申请增长2020→2024(%)", "MOST活跃专项数",
              "MOE新专业信号强度", "应届平均月薪(元)", "就业率(%)"]
try:
    scorecard["综合信号分(0-10)"] = scaler.fit_transform(
        scorecard[score_cols]).mean(axis=1).round(1)
except Exception:
    scorecard["综合信号分(0-10)"] = 0

scorecard = scorecard.sort_values("综合信号分(0-10)", ascending=False)
scorecard.to_csv(OUT / "multisource_scorecard.csv", index=False, encoding="utf-8-sig")

print("=== 多维度学科信号评分表 ===")
print(scorecard.to_string(index=False))

# Print MOST programs grouped by field
print("\n\n=== MOST 活跃战略专项 — 映射到学科 ===")
for _, row in most.iterrows():
    print(f"  [{row['category']}] {row['program_name']}  ({row['start_year']}+)"
          f" → {row['undergraduate_relevance']}")

# Print MOE new majors ranked by signal
print("\n\n=== MOE 2024-2026 新增专业信号 ===")
new_majors = moe[moe["added_or_removed"].str.contains("新增", na=False)].copy()
new_majors = new_majors.sort_values("policy_signal", ascending=False)
for _, row in new_majors.iterrows():
    print(f"  {row['policy_signal']} {row['major_cn']} ({row['year']}年新增) — {row['notes']}")

# Print majors under removal pressure
print("\n\n=== 撤销/停招压力大的专业 ===")
warn = moe[moe["added_or_removed"].str.contains("撤销", na=False)]
for _, row in warn.iterrows():
    print(f"  ⚠️  {row['major_cn']} — {row['notes']}")

print(f"\nSaved to {OUT}/multisource_scorecard.csv")
