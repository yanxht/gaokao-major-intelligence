#!/usr/bin/env python3
"""
NSFC Funding Visualizations
Generates all charts for the decision brief
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

# ── Setup ─────────────────────────────────────────────────────────────────────
BASE  = Path(__file__).parent.parent
DATA  = BASE / "data" / "processed"
OUT   = BASE / "output" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# Use a clean style with CJK font support
plt.rcParams.update({
    "font.family": ["Arial Unicode MS", "PingFang SC", "sans-serif"],
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 150,
})

df = pd.read_csv(DATA / "nsfc_mianshang_2020_2024.csv")

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
COLORS = {
    "医学":    "#E74C3C",
    "工程材料": "#2980B9",
    "生命":    "#27AE60",
    "信息":    "#9B59B6",
    "地球":    "#F39C12",
    "化学":    "#1ABC9C",
    "数理":    "#34495E",
    "管理":    "#95A5A6",
}
df["dept_short"] = df["dept_name_cn"].map(LABELS)
years = sorted(df["year"].unique())
DEPTS = ["医学", "工程材料", "生命", "信息", "地球", "化学", "数理", "管理"]

# ── CHART 1: Stacked bar — funding by discipline × year ──────────────────────
fig, ax = plt.subplots(figsize=(10, 6))

bottom = np.zeros(len(years))
for dept in DEPTS:
    vals = [df[(df["year"]==y) & (df["dept_short"]==dept)]["funding_wan"].sum() / 10000
            for y in years]
    bars = ax.bar(years, vals, bottom=bottom, color=COLORS[dept], label=dept, width=0.6)
    # Label bars where value > 0.5 亿
    for bar, val, bot in zip(bars, vals, bottom):
        if val > 0.5:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bot + val/2, f"{val:.1f}", ha="center", va="center",
                    fontsize=7, color="white", fontweight="bold")
    bottom = bottom + np.array(vals)

ax.set_title("NSFC 面上项目 — 各学科资助经费 (亿元) 2020-2024\nFunding by Discipline (General Programs)", pad=12)
ax.set_ylabel("资助直接费用 (亿元 RMB)")
ax.set_xticks(years)
ax.legend(loc="upper right", ncol=2, framealpha=0.9)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))
ax.set_ylim(0, 130)
fig.tight_layout()
fig.savefig(OUT / "chart1_stacked_funding.png", bbox_inches="tight")
plt.close()
print("✓ Chart 1: stacked funding bar")

# ── CHART 2: Line — funded projects by discipline, 2020-2024 ─────────────────
fig, ax = plt.subplots(figsize=(10, 6))
for dept in DEPTS:
    sub = df[df["dept_short"]==dept].sort_values("year")
    ax.plot(sub["year"], sub["funded"], marker="o", color=COLORS[dept],
            label=dept, linewidth=2, markersize=6)
    # Annotate 2024 endpoint
    last = sub[sub["year"]==2024]
    ax.annotate(f' {dept}\n {last["funded"].values[0]:,}',
                xy=(2024, last["funded"].values[0]),
                fontsize=8, color=COLORS[dept], va="center")

ax.set_title("NSFC 面上项目 — 各学科资助项目数 2020-2024\nFunded Projects by Discipline", pad=12)
ax.set_ylabel("资助项目数 (项)")
ax.set_xticks(years)
ax.legend(loc="upper left", ncol=2, framealpha=0.9)
ax.set_xlim(2019.8, 2025)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{int(x):,}"))
fig.tight_layout()
fig.savefig(OUT / "chart2_funded_projects_trend.png", bbox_inches="tight")
plt.close()
print("✓ Chart 2: funded projects trend")

# ── CHART 3: Bar — application growth % 2020→2024 ────────────────────────────
app_growth = {}
for dept in DEPTS:
    v2020 = df[(df["year"]==2020) & (df["dept_short"]==dept)]["applications"].values[0]
    v2024 = df[(df["year"]==2024) & (df["dept_short"]==dept)]["applications"].values[0]
    app_growth[dept] = (v2024 - v2020) / v2020 * 100

sorted_depts = sorted(app_growth, key=app_growth.get, reverse=True)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(sorted_depts,
               [app_growth[d] for d in sorted_depts],
               color=[COLORS[d] for d in sorted_depts], height=0.6)
for bar, d in zip(bars, sorted_depts):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f"+{app_growth[d]:.1f}%", va="center", fontsize=10)
ax.set_title("申请数增长率 2020→2024\nApplication Growth Rate by Discipline (Talent Flow Indicator)", pad=12)
ax.set_xlabel("增长率 (%)")
ax.axvline(x=57.6, color="gray", linestyle="--", alpha=0.6, label="全科平均 +57.6%")
ax.legend(fontsize=9)
ax.set_xlim(0, 85)
fig.tight_layout()
fig.savefig(OUT / "chart3_application_growth.png", bbox_inches="tight")
plt.close()
print("✓ Chart 3: application growth")

# ── CHART 4: Acceptance rate change (competition squeeze) ────────────────────
rate_2020 = {dept: df[(df["year"]==2020)&(df["dept_short"]==dept)]["acceptance_rate_pct"].values[0]
             for dept in DEPTS}
rate_2024 = {dept: df[(df["year"]==2024)&(df["dept_short"]==dept)]["acceptance_rate_pct"].values[0]
             for dept in DEPTS}

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(DEPTS))
w = 0.35
bars1 = ax.bar(x - w/2, [rate_2020[d] for d in DEPTS], w, label="2020", alpha=0.85,
               color=[COLORS[d] for d in DEPTS])
bars2 = ax.bar(x + w/2, [rate_2024[d] for d in DEPTS], w, label="2024", alpha=0.5,
               color=[COLORS[d] for d in DEPTS], hatch="//")
# Delta annotations
for i, dept in enumerate(DEPTS):
    delta = rate_2024[dept] - rate_2020[dept]
    ax.text(x[i], max(rate_2020[dept], rate_2024[dept]) + 0.4,
            f"{delta:+.1f}pp", ha="center", fontsize=8.5, color="dimgray")
ax.set_title("资助率对比 2020 vs 2024\nAcceptance Rate 2020 vs 2024 — Competition Pressure", pad=12)
ax.set_ylabel("资助率 (%)")
ax.set_xticks(x)
ax.set_xticklabels(DEPTS, fontsize=10)
ax.legend()
ax.set_ylim(0, 30)
fig.tight_layout()
fig.savefig(OUT / "chart4_acceptance_rate.png", bbox_inches="tight")
plt.close()
print("✓ Chart 4: acceptance rate comparison")

# ── CHART 5: Bubble — funding size vs. growth rate ───────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))

for dept in DEPTS:
    funding_2024 = df[(df["year"]==2024)&(df["dept_short"]==dept)]["funding_wan"].values[0]
    funding_2020 = df[(df["year"]==2020)&(df["dept_short"]==dept)]["funding_wan"].values[0]
    pct_change   = (funding_2024 - funding_2020) / funding_2020 * 100
    apps_growth  = app_growth[dept]
    size         = funding_2024 / 5000   # bubble size proportional to 2024 funding

    ax.scatter(apps_growth, pct_change, s=size * 100, color=COLORS[dept],
               alpha=0.75, edgecolors="white", linewidths=1.2, zorder=3)
    ax.annotate(dept, (apps_growth, pct_change), fontsize=10, fontweight="bold",
                ha="center", va="bottom", color=COLORS[dept],
                xytext=(0, 8), textcoords="offset points")

ax.axhline(0, color="gray", linestyle="--", alpha=0.5)
ax.axvline(57.6, color="gray", linestyle="--", alpha=0.5)
ax.text(58, ax.get_ylim()[1]*0.95, "← 低于平均     高于平均 →",
        fontsize=8, color="gray", ha="center")

ax.set_title("学科象限图: 申请人才增长 vs 资助经费变化\n"
             "Bubble Chart: Talent Inflow vs Funding Change (size = 2024 funding)", pad=12)
ax.set_xlabel("申请数增长率 2020→2024 (%)")
ax.set_ylabel("资助经费变化 2020→2024 (%)")
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(OUT / "chart5_bubble_quadrant.png", bbox_inches="tight")
plt.close()
print("✓ Chart 5: bubble quadrant")

# ── CHART 6: Shandong context — region ranked funding ───────────────────────
# From 2024 annual report: Shandong ranked 8th with 1,010 projects, 49,435.84万元
provinces = [
    ("北京", 3266, 159531.99), ("上海", 2223, 108257.04), ("江苏", 2148, 104671.38),
    ("广东", 2135, 104379.69), ("湖北", 1208, 58510.24),  ("浙江", 1158, 56891.09),
    ("陕西", 1080, 52795.31),  ("山东", 1010, 49435.84),  ("四川", 813, 39830.29),
    ("湖南", 766, 37223.39),   ("安徽", 623, 30528.23),   ("天津", 595, 29035.46),
    ("辽宁", 586, 28564.24),   ("福建", 487, 23664.67),   ("黑龙江", 459, 22429.22),
]
provs, counts, funds = zip(*provinces)
colors = ["#E74C3C" if p == "山东" else "#AED6F1" for p in provs]

fig, axes = plt.subplots(1, 2, figsize=(14, 7))
# Projects
axes[0].barh(provs, counts, color=colors)
axes[0].set_title("2024 面上项目省份排名\n（按资助项目数，前15省）")
axes[0].set_xlabel("资助项目数 (项)")
for i, (v, p) in enumerate(zip(counts, provs)):
    if p == "山东":
        axes[0].text(v + 10, i, f" ★{v:,} (#{i+1})", va="center",
                     fontweight="bold", color="#E74C3C")
    else:
        axes[0].text(v + 10, i, f" {v:,}", va="center", fontsize=8)
# Funding
axes[1].barh(provs, [f/10000 for f in funds], color=colors)
axes[1].set_title("2024 面上项目省份排名\n（按资助经费，前15省）")
axes[1].set_xlabel("资助直接费用 (亿元)")
for i, (v, p) in enumerate(zip(funds, provs)):
    if p == "山东":
        axes[1].text(v/10000 + 0.02, i, f" ★{v/10000:.1f}亿 (#{i+1})",
                     va="center", fontweight="bold", color="#E74C3C")
    else:
        axes[1].text(v/10000 + 0.02, i, f" {v/10000:.1f}亿", va="center", fontsize=8)

fig.suptitle("山东高校在全国科研格局中的位置 (2024 NSFC 面上项目)", fontsize=13, y=1.01)
fig.tight_layout()
fig.savefig(OUT / "chart6_shandong_context.png", bbox_inches="tight")
plt.close()
print("✓ Chart 6: Shandong provincial context")

print(f"\nAll 6 charts saved to {OUT}")
