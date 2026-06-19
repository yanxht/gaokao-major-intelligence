"""
06_extended_charts.py
Generates additional charts for the detailed decision brief v2.
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES = os.path.join(BASE, "output", "tables")
FIGS   = os.path.join(BASE, "output", "figures")
DATA   = os.path.join(BASE, "data", "processed")
os.makedirs(FIGS, exist_ok=True)

plt.rcParams["font.family"] = "Arial Unicode MS"   # macOS CJK font
plt.rcParams["axes.spines.top"]   = False
plt.rcParams["axes.spines.right"] = False

# colour palette (8 disciplines)
COLORS = {
    "医学":   "#E15759",
    "工程材料": "#4E79A7",
    "生命":   "#76B7B2",
    "信息":   "#F28E2B",
    "地球":   "#59A14F",
    "化学":   "#B07AA1",
    "数理":   "#FF9DA7",
    "管理":   "#BAB0AC",
}

SHORT_EN = {
    "医学":"Medical","工程材料":"Eng+Mat","生命":"Life Sci",
    "信息":"Info/CS","地球":"Earth","化学":"Chem","数理":"Math+Phys","管理":"Mgmt",
}

# ── load data ──────────────────────────────────────────────────────────────
raw = pd.read_csv(os.path.join(DATA, "nsfc_mianshang_2020_2024.csv"))
dept_map = {
    "数学物理科学部":"数理","化学科学部":"化学","生命科学部":"生命",
    "地球科学部":"地球","工程与材料科学部":"工程材料","信息科学部":"信息",
    "管理科学部":"管理","医学科学部":"医学",
}
raw["dept_short"] = raw["dept_name_cn"].map(dept_map)

apps  = pd.read_csv(os.path.join(TABLES, "applications_by_dept_year.csv"), index_col=0)
funded= pd.read_csv(os.path.join(TABLES, "funded_projects_by_dept_year.csv"), index_col=0)
rates = pd.read_csv(os.path.join(TABLES, "acceptance_rate_by_dept_year.csv"), index_col=0)
fund_wan= pd.read_csv(os.path.join(TABLES, "funding_by_dept_year.csv"), index_col=0)
shares= pd.read_csv(os.path.join(TABLES, "funding_share_by_dept_year.csv"), index_col=0)
score = pd.read_csv(os.path.join(TABLES, "multisource_scorecard.csv"))
score.rename(columns={"学科领域":"dept"}, inplace=True)
emp   = pd.read_csv(os.path.join(DATA, "employment_salary_benchmarks.csv"))
moe   = pd.read_csv(os.path.join(DATA, "moe_major_trends.csv"))
most  = pd.read_csv(os.path.join(DATA, "most_key_programs.csv"))

YEARS = [2020, 2021, 2022, 2023, 2024]
DEPT_ORDER = ["医学","工程材料","生命","信息","地球","化学","数理","管理"]


# ═══════════════════════════════════════════════════════════════════════════
# Chart A — Application count trend (all 8 disciplines, absolute numbers)
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 6))
for dept in DEPT_ORDER:
    row = apps.loc[dept, [str(y) for y in YEARS]]
    ax.plot(YEARS, row.values, marker="o", label=dept,
            color=COLORS[dept], linewidth=2)
    ax.annotate(dept, xy=(2024, row["2024"]),
                xytext=(5, 0), textcoords="offset points",
                va="center", fontsize=9, color=COLORS[dept])

ax.set_title("NSFC 面上项目：各学科申请量趋势（2020–2024）", fontsize=13, fontweight="bold")
ax.set_xlabel("年份"); ax.set_ylabel("申请件数")
ax.set_xticks(YEARS)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.legend(bbox_to_anchor=(1.14, 0.5), loc="center right", fontsize=8, frameon=False)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartA_applications_trend.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartA saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart B — Acceptance rate collapse 2020 vs 2024 (horizontal bar pair)
# ═══════════════════════════════════════════════════════════════════════════
depts_sorted = rates.loc[DEPT_ORDER, "2020"].sort_values(ascending=True).index.tolist()
r2020 = [rates.loc[d, "2020"] for d in depts_sorted]
r2024 = [rates.loc[d, "2024"] for d in depts_sorted]

fig, ax = plt.subplots(figsize=(10, 5.5))
y = np.arange(len(depts_sorted))
h = 0.34
bars2020 = ax.barh(y + h/2, r2020, h, label="2020年", color="#ADC8E6", edgecolor="none")
bars2024 = ax.barh(y - h/2, r2024, h, label="2024年", color="#E15759", edgecolor="none")

for i, (b20, b24) in enumerate(zip(r2020, r2024)):
    ax.text(b20 + 0.3, y[i] + h/2, f"{b20:.1f}%", va="center", fontsize=8.5, color="#555")
    ax.text(b24 + 0.3, y[i] - h/2, f"{b24:.1f}%", va="center", fontsize=8.5, color="#E15759", fontweight="bold")

ax.set_yticks(y)
ax.set_yticklabels([f"{d}  " for d in depts_sorted], fontsize=10)
ax.set_xlabel("资助率 (%)")
ax.set_title("NSFC 面上项目：资助率——2020年 vs 2024年对比\n（全学科资助率断崖式下降）",
             fontsize=12, fontweight="bold")
ax.legend(fontsize=9)
ax.axvline(x=0, color="black", linewidth=0.5)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartB_acceptance_rate_comparison.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartB saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart C — Funding share stability (stacked area 2020–2024)
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(10, 5.5))
year_cols = [str(y) for y in YEARS]
bottoms = np.zeros(len(YEARS))
for dept in DEPT_ORDER:
    vals = shares.loc[dept, year_cols].values.astype(float)
    ax.fill_between(YEARS, bottoms, bottoms + vals,
                    alpha=0.85, label=dept, color=COLORS[dept])
    mid = bottoms + vals / 2
    ax.text(2022, mid[2], f"{dept} {vals[2]:.1f}%",
            ha="center", va="center", fontsize=7.5, color="white", fontweight="bold")
    bottoms += vals

ax.set_xlim(2020, 2024)
ax.set_ylim(0, 100)
ax.set_xlabel("年份"); ax.set_ylabel("经费占比 (%)")
ax.set_title("NSFC 面上项目：各学科经费占比——五年几乎无变化\n（最大波动±0.3%，说明资金分配是制度性锁定配额）",
             fontsize=11, fontweight="bold")
ax.legend(bbox_to_anchor=(1.01, 0.5), loc="center left", fontsize=8, frameon=False)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartC_funding_share_stability.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartC saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart D — "Demand vs Supply" scatter: App growth vs Projects growth
# ═══════════════════════════════════════════════════════════════════════════
apps_growth   = apps["2020→2024%"].astype(float)
funded_growth = funded["2020→2024%"].astype(float)

fig, ax = plt.subplots(figsize=(9, 7))
for dept in DEPT_ORDER:
    x = apps_growth.loc[dept]
    y = funded_growth.loc[dept]
    ax.scatter(x, y, s=200, color=COLORS[dept], zorder=5, edgecolors="white", linewidths=1.5)
    ax.annotate(dept, (x, y), textcoords="offset points", xytext=(8, 4), fontsize=10,
                color=COLORS[dept], fontweight="bold")

# diagonal y=x reference line
lim = max(apps_growth.max(), funded_growth.max()) * 1.1
ax.plot([0, lim], [0, lim], "k--", linewidth=1, alpha=0.4, label="申请增长 = 资助增长（理想线）")
ax.axhline(0, color="gray", linewidth=0.5)
ax.axvline(0, color="gray", linewidth=0.5)

ax.set_xlabel("申请量增长率 2020→2024 (%)", fontsize=11)
ax.set_ylabel("资助数量增长率 2020→2024 (%)", fontsize=11)
ax.set_title("NSFC 申请量 vs 资助量增长对比\n（点在虚线下方 = 竞争更激烈；点越靠右越受申请者追捧）",
             fontsize=11, fontweight="bold")
ax.legend(fontsize=9)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartD_supply_demand_scatter.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartD saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart E — Funded project growth (absolute count per year, grouped bar)
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 6))
n = len(DEPT_ORDER)
x = np.arange(len(YEARS))
width = 0.09
for i, dept in enumerate(DEPT_ORDER):
    vals = funded.loc[dept, [str(y) for y in YEARS]].values.astype(float)
    ax.bar(x + i * width - (n-1)*width/2, vals, width,
           label=dept, color=COLORS[dept], edgecolor="none", alpha=0.9)

ax.set_xticks(x); ax.set_xticklabels(YEARS)
ax.set_xlabel("年份"); ax.set_ylabel("资助项目数")
ax.set_title("NSFC 面上项目：各学科资助数量趋势（2020–2024）", fontsize=12, fontweight="bold")
ax.legend(fontsize=8, ncol=4, loc="upper left")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}"))
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartE_funded_projects_grouped.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartE saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart F — Average grant intensity trend (万元/项)
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 6))
for dept in DEPT_ORDER:
    sub = raw[raw["dept_short"] == dept].sort_values("year")
    ax.plot(sub["year"], sub["avg_intensity_wan"], marker="s", label=dept,
            color=COLORS[dept], linewidth=2)
    ax.annotate(dept, xy=(2024, sub[sub["year"]==2024]["avg_intensity_wan"].values[0]),
                xytext=(5, 0), textcoords="offset points", va="center",
                fontsize=9, color=COLORS[dept])

ax.set_title("NSFC 面上项目：平均资助强度趋势（万元/项，2020–2024）\n（2023年后整体下调，单项经费缩水）",
             fontsize=11, fontweight="bold")
ax.set_xlabel("年份"); ax.set_ylabel("平均资助强度（万元/项）")
ax.set_xticks(YEARS)
ax.legend(bbox_to_anchor=(1.13, 0.5), loc="center right", fontsize=8, frameon=False)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartF_avg_intensity_trend.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartF saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart G — Multi-source composite scorecard (horizontal bar, colour-coded tier)
# ═══════════════════════════════════════════════════════════════════════════
score_sorted = score.sort_values("综合信号分(0-10)", ascending=True)
scores_val   = score_sorted["综合信号分(0-10)"].values

tier_colors = []
for v in scores_val:
    if v >= 7:   tier_colors.append("#2ca02c")   # green — strong
    elif v >= 4: tier_colors.append("#ff7f0e")   # orange — moderate
    else:        tier_colors.append("#d62728")   # red — weak

fig, ax = plt.subplots(figsize=(10, 5.5))
bars = ax.barh(score_sorted["dept"], scores_val, color=tier_colors, edgecolor="none", height=0.6)
for bar, val in zip(bars, scores_val):
    ax.text(val + 0.1, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}", va="center", fontsize=11, fontweight="bold")

ax.set_xlabel("综合信号分（满分10分）", fontsize=11)
ax.set_title("四维综合信号评分：NSFC + MOST + MOE + 就业薪资\n（绿色≥7 强推；橙色4–7 视子方向；红色<4 谨慎）",
             fontsize=11, fontweight="bold")
ax.axvline(x=7, color="green",  linewidth=1.2, linestyle="--", alpha=0.6)
ax.axvline(x=4, color="orange", linewidth=1.2, linestyle="--", alpha=0.6)
ax.set_xlim(0, 11)
legend_patches = [
    mpatches.Patch(color="#2ca02c", label="强推（≥7.0）"),
    mpatches.Patch(color="#ff7f0e", label="视子方向（4–7）"),
    mpatches.Patch(color="#d62728", label="谨慎（<4.0）"),
]
ax.legend(handles=legend_patches, fontsize=9, loc="lower right")
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartG_multisource_scorecard.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartG saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart H — Salary by major category (horizontal bar, sorted)
# ═══════════════════════════════════════════════════════════════════════════
emp_sorted = emp.sort_values("avg_starting_salary_monthly_yuan", ascending=True)
salary_colors = ["#2ca02c" if s >= 9000 else "#ff7f0e" if s >= 7000 else "#d62728"
                 for s in emp_sorted["avg_starting_salary_monthly_yuan"]]

fig, ax = plt.subplots(figsize=(11, 8))
bars = ax.barh(emp_sorted["major_category"], emp_sorted["avg_starting_salary_monthly_yuan"],
               color=salary_colors, edgecolor="none", height=0.6)
for bar, val in zip(bars, emp_sorted["avg_starting_salary_monthly_yuan"]):
    ax.text(val + 80, bar.get_y() + bar.get_height()/2,
            f"¥{val:,}", va="center", fontsize=9)

ax.set_xlabel("应届本科毕业生月薪中位数（元/月）", fontsize=10)
ax.set_title("2024年应届本科毕业生月薪中位数——按专业方向\n（来源：MyCOS 2024 + BOSS直聘/智联校招报告）",
             fontsize=11, fontweight="bold")
ax.axvline(x=9000, color="green",  linewidth=1, linestyle="--", alpha=0.5, label="¥9,000 参考线")
ax.axvline(x=7000, color="orange", linewidth=1, linestyle="--", alpha=0.5, label="¥7,000 参考线")
legend_patches = [
    mpatches.Patch(color="#2ca02c", label="月薪≥¥9,000（高薪区间）"),
    mpatches.Patch(color="#ff7f0e", label="月薪¥7,000–¥9,000（中高）"),
    mpatches.Patch(color="#d62728", label="月薪<¥7,000（偏低）"),
]
ax.legend(handles=legend_patches, fontsize=9)
ax.set_xlim(0, 12500)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"¥{int(v):,}"))
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartH_salary_by_major.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartH saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart I — MOE policy signal strength (new majors only, sorted)
# ═══════════════════════════════════════════════════════════════════════════
new_majors = moe[moe["added_or_removed"].isin(["新增","快速扩张","持续扩张","扩张"])].copy()
# parse star count from signal column
def star_count(s):
    if isinstance(s, str):
        return s.count("★")
    return 0
new_majors["stars"] = new_majors["policy_signal"].apply(star_count)
new_majors = new_majors.sort_values("stars", ascending=True)

star_colors_map = {5:"#2ca02c", 4:"#8fbc8f", 3:"#ff7f0e", 2:"#ffb347", 1:"#d62728"}
bar_colors = [star_colors_map.get(s, "#cccccc") for s in new_majors["stars"]]

fig, ax = plt.subplots(figsize=(11, 9))
bars = ax.barh(new_majors["major_cn"], new_majors["stars"],
               color=bar_colors, edgecolor="none", height=0.65)
for bar, row in zip(bars, new_majors.itertuples()):
    ax.text(row.stars + 0.05, bar.get_y() + bar.get_height()/2,
            row.policy_signal + f"  ({row.added_or_removed})",
            va="center", fontsize=8.5)

ax.set_xlabel("政策信号强度（★数）", fontsize=10)
ax.set_title("教育部专业目录：新增/扩张专业政策信号强度\n（2019–2026年，★★★★★ = 最强）",
             fontsize=11, fontweight="bold")
ax.set_xlim(0, 7)
ax.set_xticks([1, 2, 3, 4, 5])
ax.set_xticklabels(["★", "★★", "★★★", "★★★★", "★★★★★"])
legend_patches = [
    mpatches.Patch(color="#2ca02c", label="★★★★★ 战略级"),
    mpatches.Patch(color="#8fbc8f", label="★★★★ 优先级"),
    mpatches.Patch(color="#ff7f0e", label="★★★ 一般"),
    mpatches.Patch(color="#ffb347", label="★★ 观望"),
]
ax.legend(handles=legend_patches, fontsize=9)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartI_moe_new_majors_signal.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartI saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart J — MOST programs: count by strategic area (horizontal bar)
# ═══════════════════════════════════════════════════════════════════════════
most["field"] = most["undergraduate_relevance"].str.split("/").str[0].str.strip().str.replace('"','')
field_counts = most.groupby("field").size().sort_values(ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
colors_most = ["#E15759" if "医" in f or "生" in f or "RNA" in f
               else "#4E79A7" if "计算机" in f or "AI" in f or "软件" in f
               else "#F28E2B" if "材料" in f or "芯片" in f or "微电子" in f or "集成" in f or "机械" in f
               else "#59A14F" if "能源" in f or "环境" in f or "电气" in f or "地质" in f
               else "#B07AA1" for f in field_counts.index]

bars = ax.barh(field_counts.index, field_counts.values,
               color=colors_most, edgecolor="none", height=0.65)
for bar, val in zip(bars, field_counts.values):
    ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
            f"{val}项", va="center", fontsize=10, fontweight="bold")

ax.set_xlabel("国家级专项数量", fontsize=10)
ax.set_title("MOST 国家重点研发计划 & 国家科技重大专项\n按本科专业相关性分组（2021–2026年活跃专项共16项）",
             fontsize=11, fontweight="bold")
ax.set_xlim(0, 6)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartJ_most_programs_by_field.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartJ saved")


# ═══════════════════════════════════════════════════════════════════════════
# Chart K — Year-by-year funding total (亿元) per department
# ═══════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(11, 6))
for dept in DEPT_ORDER:
    vals_wan = fund_wan.loc[dept, [str(y) for y in YEARS]].values.astype(float)
    vals_yi  = vals_wan / 10000  # 万元 → 亿元
    ax.plot(YEARS, vals_yi, marker="o", label=dept, color=COLORS[dept], linewidth=2)
    ax.annotate(f"{dept} {vals_yi[-1]:.1f}亿",
                xy=(2024, vals_yi[-1]), xytext=(5, 0), textcoords="offset points",
                va="center", fontsize=8.5, color=COLORS[dept])

ax.set_title("NSFC 面上项目：各学科经费总额（亿元，2020–2024）\n（2022年之后整体预算下调，但各学科比例不变）",
             fontsize=11, fontweight="bold")
ax.set_xlabel("年份"); ax.set_ylabel("经费总额（亿元）")
ax.set_xticks(YEARS)
ax.legend(bbox_to_anchor=(1.16, 0.5), loc="center right", fontsize=8, frameon=False)
plt.tight_layout()
fig.savefig(os.path.join(FIGS, "chartK_funding_yi_trend.png"), dpi=150, bbox_inches="tight")
plt.close()
print("chartK saved")


print("\nAll extended charts saved to output/figures/")
