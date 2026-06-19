#!/usr/bin/env python3
"""
NSFC General Programs (面上项目) Analysis
Source: NSFC Annual Reports 2020-2024
Data type: General Programs (面上项目) - largest NSFC grant category,
           best proxy for discipline-level basic research investment
"""

import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).parent.parent
DATA = BASE / "data" / "processed"
OUT  = BASE / "output" / "tables"
OUT.mkdir(parents=True, exist_ok=True)

# ── Load ─────────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA / "nsfc_mianshang_2020_2024.csv")

# Translate dept names to short labels
LABELS = {
    "数学物理科学部": "数理",
    "化学科学部":     "化学",
    "生命科学部":     "生命",
    "地球科学部":     "地球",
    "工程与材料科学部": "工程材料",
    "信息科学部":     "信息",
    "管理科学部":     "管理",
    "医学科学部":     "医学",
}
df["dept_short"] = df["dept_name_cn"].map(LABELS)

years = sorted(df["year"].unique())
depts = ["医学", "工程材料", "生命", "信息", "地球", "化学", "数理", "管理"]  # ranked by 2020 funding

# ── Table 1: Funding by discipline × year (万元) ─────────────────────────────
pivot_funding = df.pivot_table(index="dept_short", columns="year",
                               values="funding_wan", aggfunc="sum")
pivot_funding = pivot_funding.loc[depts]

# Add 2020→2024 change
pivot_funding["2020→2024%"] = ((pivot_funding[2024] - pivot_funding[2020])
                               / pivot_funding[2020] * 100).round(1)
pivot_funding.to_csv(OUT / "funding_by_dept_year.csv")
print("=== Table 1: Funding (万元) by Department ===")
print(pivot_funding.to_string())
print()

# ── Table 2: Funded projects by discipline × year ────────────────────────────
pivot_projects = df.pivot_table(index="dept_short", columns="year",
                                values="funded", aggfunc="sum")
pivot_projects = pivot_projects.loc[depts]
pivot_projects["2020→2024%"] = ((pivot_projects[2024] - pivot_projects[2020])
                                / pivot_projects[2020] * 100).round(1)
pivot_projects.to_csv(OUT / "funded_projects_by_dept_year.csv")
print("=== Table 2: Funded Projects by Department ===")
print(pivot_projects.to_string())
print()

# ── Table 3: Applications growth (talent flow indicator) ─────────────────────
pivot_apps = df.pivot_table(index="dept_short", columns="year",
                            values="applications", aggfunc="sum")
pivot_apps = pivot_apps.loc[depts]
pivot_apps["2020→2024%"] = ((pivot_apps[2024] - pivot_apps[2020])
                            / pivot_apps[2020] * 100).round(1)
pivot_apps.to_csv(OUT / "applications_by_dept_year.csv")
print("=== Table 3: Applications (Talent Flow) by Department ===")
print(pivot_apps.to_string())
print()

# ── Table 4: Acceptance rate (competition pressure) ──────────────────────────
pivot_rate = df.pivot_table(index="dept_short", columns="year",
                            values="acceptance_rate_pct", aggfunc="mean")
pivot_rate = pivot_rate.loc[depts]
pivot_rate["2020→2024Δ"] = (pivot_rate[2024] - pivot_rate[2020]).round(2)
pivot_rate.to_csv(OUT / "acceptance_rate_by_dept_year.csv")
print("=== Table 4: Acceptance Rate (%) — Competition Pressure ===")
print(pivot_rate.to_string())
print()

# ── Table 5: Funding share (%) — discipline's slice of the pie ───────────────
totals = df.groupby("year")["funding_wan"].sum()
df["funding_share_pct"] = df.apply(
    lambda r: r["funding_wan"] / totals[r["year"]] * 100, axis=1)
pivot_share = df.pivot_table(index="dept_short", columns="year",
                             values="funding_share_pct", aggfunc="sum")
pivot_share = pivot_share.loc[depts].round(2)
pivot_share["2020→2024Δ"] = (pivot_share[2024] - pivot_share[2020]).round(2)
pivot_share.to_csv(OUT / "funding_share_by_dept_year.csv")
print("=== Table 5: Funding Share (%) ===")
print(pivot_share.to_string())
print()

# ── Summary scorecard ─────────────────────────────────────────────────────────
print("=== SUMMARY SCORECARD ===")
summary = pd.DataFrame({
    "Funding_2024_亿RMB": (pivot_funding[2024] / 10000).round(2),
    "Funding_change%":    pivot_funding["2020→2024%"],
    "Projects_2024":      pivot_projects[2024],
    "Projects_growth%":   pivot_projects["2020→2024%"],
    "Apps_growth%":       pivot_apps["2020→2024%"],
    "Accept_rate_2024%":  pivot_rate[2024].round(2),
    "Rate_change_pp":     pivot_rate["2020→2024Δ"],
    "Share_2024%":        pivot_share[2024].round(2),
})
summary = summary.sort_values("Funding_2024_亿RMB", ascending=False)
summary.to_csv(OUT / "summary_scorecard.csv")
print(summary.to_string())
print()
print("All tables saved to output/tables/")
