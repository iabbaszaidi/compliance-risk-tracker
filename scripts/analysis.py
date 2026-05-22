"""
analysis.py
Compliance & Risk Data Tracker Framework
Reads CSVs, computes KPIs, runs anomaly analysis, generates charts.

Author : Mohammad Abbas
Dataset: Synthetic banking transaction & risk data (2024–2025)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import os, warnings
warnings.filterwarnings('ignore')

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR   = os.path.join(BASE_DIR, 'data')
SHOTS_DIR  = os.path.join(BASE_DIR, 'screenshots')
os.makedirs(SHOTS_DIR, exist_ok=True)

# ─── Load ────────────────────────────────────────────────────────────────────
customers  = pd.read_csv(os.path.join(DATA_DIR, 'customers.csv'),        parse_dates=['onboarding_date'])
txns       = pd.read_csv(os.path.join(DATA_DIR, 'transactions.csv'),     parse_dates=['txn_date'])
anomalies  = pd.read_csv(os.path.join(DATA_DIR, 'anomaly_flags.csv'),    parse_dates=['detection_date','resolution_date'])
risks      = pd.read_csv(os.path.join(DATA_DIR, 'risk_register.csv'),    parse_dates=['last_assessed_date','next_review_date'])
remediation= pd.read_csv(os.path.join(DATA_DIR, 'remediation_log.csv'),  parse_dates=['initiation_date','completion_date'])

# ─── Palette ─────────────────────────────────────────────────────────────────
NAVY  = '#1A5276'; BLUE  = '#2980B9'; LBLUE = '#AED6F1'
RED   = '#C0392B'; ORANGE= '#E67E22'; GREEN = '#1E8449'; GREY  = '#7F8C8D'
BG    = '#F4F6F8'

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': 'white',
    'axes.spines.top': False, 'axes.spines.right': False,
    'font.family': 'DejaVu Sans', 'axes.titlesize': 13,
    'axes.titleweight': 'bold', 'axes.titlecolor': NAVY,
})

# ─── KPI Computation ─────────────────────────────────────────────────────────
total_txns       = len(txns)
flagged_txns     = txns['flagged'].sum()
flag_rate        = round(flagged_txns / total_txns * 100, 2)
total_anomalies  = len(anomalies)
critical_ano     = len(anomalies[anomalies['severity'] == 'Critical'])
open_anomalies   = len(anomalies[anomalies['status'].isin(['Open','Under Review','Escalated'])])
fmu_reports      = remediation['fmu_reported'].sum()
avg_resolve_days = round(remediation['days_to_resolve'].mean(), 1)

print("═" * 45)
print("  COMPLIANCE & RISK TRACKER — KPI SUMMARY")
print("═" * 45)
print(f"  Total Transactions     : {total_txns:,}")
print(f"  Flagged Transactions   : {flagged_txns:,}  ({flag_rate}%)")
print(f"  Anomalies Detected     : {total_anomalies:,}")
print(f"  Critical Anomalies     : {critical_ano:,}")
print(f"  Open / Pending         : {open_anomalies:,}")
print(f"  FMU Reports Filed      : {fmu_reports:,}")
print(f"  Avg Days to Resolve    : {avg_resolve_days} days")
print("═" * 45)

# ════════════════════════════════════════════════════════════════════════════
# CHART 1 — KPI Dashboard Cards
# ════════════════════════════════════════════════════════════════════════════
kpis = [
    ("Total\nTransactions",     f"{total_txns:,}",      NAVY),
    ("Flagged\nTransactions",   f"{flagged_txns:,}",    ORANGE),
    ("Flag Rate",               f"{flag_rate}%",        RED if flag_rate > 10 else ORANGE),
    ("Anomalies\nDetected",     f"{total_anomalies:,}", ORANGE),
    ("Critical\nAnomalies",     f"{critical_ano:,}",    RED),
    ("FMU Reports\nFiled",      f"{int(fmu_reports)}",  RED),
    ("Open\nCases",             f"{open_anomalies:,}",  ORANGE),
    ("Avg Resolve\nDays",       f"{avg_resolve_days}",  GREEN),
]

fig, axes = plt.subplots(2, 4, figsize=(18, 5))
fig.patch.set_facecolor(BG)
fig.suptitle("Compliance & Risk Tracker — KPI Overview", fontsize=15, fontweight='bold', color=NAVY, y=1.01)
for ax, (label, value, color) in zip(axes.flatten(), kpis):
    ax.set_facecolor('white'); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    rect = mpatches.FancyBboxPatch((0.05,0.08), 0.90, 0.84, boxstyle="round,pad=0.04",
                                    linewidth=2, edgecolor=color, facecolor='white', zorder=2)
    ax.add_patch(rect)
    ax.text(0.50, 0.60, value, ha='center', va='center', fontsize=20, fontweight='bold', color=color, zorder=3)
    ax.text(0.50, 0.26, label, ha='center', va='center', fontsize=9, color=GREY, zorder=3, multialignment='center')
plt.tight_layout()
plt.savefig(os.path.join(SHOTS_DIR, '01_kpi_dashboard.png'), dpi=150, bbox_inches='tight')
plt.close(); print("✓ 01_kpi_dashboard.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 2 — Transaction Volume + Flagged Trend (Monthly)
# ════════════════════════════════════════════════════════════════════════════
txns['month'] = txns['txn_date'].dt.to_period('M')
monthly_all   = txns.groupby('month').size().reset_index(name='total')
monthly_flag  = txns[txns['flagged']==1].groupby('month').size().reset_index(name='flagged')
monthly = monthly_all.merge(monthly_flag, on='month', how='left').fillna(0)
monthly['month_str'] = monthly['month'].astype(str)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
fig.patch.set_facecolor(BG)

ax1.bar(monthly['month_str'], monthly['total'], color=LBLUE, edgecolor=BLUE, linewidth=0.8, label='Total Transactions')
ax1.plot(monthly['month_str'], monthly['total'], color=NAVY, linewidth=2, marker='o', markersize=5)
ax1.set_title("Monthly Transaction Volume", pad=10)
ax1.set_ylabel("Transactions", color=GREY)
ax1.tick_params(colors=GREY)

ax2.bar(monthly['month_str'], monthly['flagged'], color='#FADBD8', edgecolor=RED, linewidth=0.8, label='Flagged')
ax2.plot(monthly['month_str'], monthly['flagged'], color=RED, linewidth=2, marker='o', markersize=5)
ax2.set_title("Monthly Flagged Transactions", pad=10)
ax2.set_ylabel("Flagged Count", color=GREY)
ax2.tick_params(axis='x', rotation=45, labelsize=9); ax2.tick_params(colors=GREY)

plt.tight_layout()
plt.savefig(os.path.join(SHOTS_DIR, '02_transaction_trend.png'), dpi=150, bbox_inches='tight')
plt.close(); print("✓ 02_transaction_trend.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 3 — Anomaly Analysis (Severity + Risk Category)
# ════════════════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor(BG)

# Donut — Severity
sev = anomalies['severity'].value_counts().reindex(['Critical','High','Medium','Low']).fillna(0)
wedges, texts, autotexts = ax1.pie(sev, labels=sev.index, colors=[RED,ORANGE,BLUE,GREEN],
    autopct='%1.0f%%', startangle=140, pctdistance=0.80,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2))
for t in autotexts: t.set_fontsize(10); t.set_color('white'); t.set_fontweight('bold')
for t in texts:     t.set_fontsize(11); t.set_color(NAVY)
ax1.set_title("Anomaly Severity Distribution", pad=12)

# Horizontal bar — Top Risk Categories
cat_counts = anomalies['risk_category'].value_counts().head(8)
bars = ax2.barh(cat_counts.index, cat_counts.values, color=BLUE, edgecolor='white', linewidth=0.8)
ax2.bar_label(bars, padding=4, fontsize=10, fontweight='bold', color=NAVY)
ax2.set_title("Anomalies by Risk Category", pad=12)
ax2.set_xlabel("Count", color=GREY); ax2.tick_params(colors=GREY, labelsize=9)
ax2.invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(SHOTS_DIR, '03_anomaly_analysis.png'), dpi=150, bbox_inches='tight')
plt.close(); print("✓ 03_anomaly_analysis.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 4 — Branch Risk Concentration
# ════════════════════════════════════════════════════════════════════════════
branch_data = anomalies.groupby('branch').agg(
    anomaly_count=('anomaly_id','count'),
    total_amount =('amount_pkr','sum'),
    avg_score    =('anomaly_score','mean')
).reset_index().sort_values('total_amount', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor(BG)

colors_branch = [RED, ORANGE, BLUE, LBLUE, GREEN, GREY][:len(branch_data)]
bars1 = ax1.bar(branch_data['branch'], branch_data['anomaly_count'],
                color=colors_branch, edgecolor='white', linewidth=0.8)
ax1.bar_label(bars1, padding=3, fontsize=10, fontweight='bold', color=NAVY)
ax1.set_title("Anomaly Count by Branch", pad=12)
ax1.set_ylabel("Count", color=GREY)
ax1.tick_params(axis='x', rotation=35, labelsize=8); ax1.tick_params(colors=GREY)

bars2 = ax2.bar(branch_data['branch'],
                (branch_data['total_amount']/1e6).round(1),
                color=colors_branch, edgecolor='white', linewidth=0.8)
ax2.bar_label(bars2, fmt='%.1fM', padding=3, fontsize=9, fontweight='bold', color=NAVY)
ax2.set_title("Total Flagged Amount by Branch (PKR M)", pad=12)
ax2.set_ylabel("PKR (Millions)", color=GREY)
ax2.tick_params(axis='x', rotation=35, labelsize=8); ax2.tick_params(colors=GREY)

plt.tight_layout()
plt.savefig(os.path.join(SHOTS_DIR, '04_branch_risk.png'), dpi=150, bbox_inches='tight')
plt.close(); print("✓ 04_branch_risk.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 5 — Remediation Efficiency
# ════════════════════════════════════════════════════════════════════════════
rem_analyst = remediation.groupby('initiated_by').agg(
    cases=('remediation_id','count'),
    avg_days=('days_to_resolve','mean'),
    resolved=('outcome', lambda x: (x=='Resolved').sum()),
    fmu=('fmu_reported','sum')
).reset_index()
rem_analyst['resolution_rate'] = (rem_analyst['resolved'] / rem_analyst['cases'] * 100).round(1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor(BG)

bars1 = ax1.bar(rem_analyst['initiated_by'], rem_analyst['avg_days'].round(1),
                color=[BLUE,GREEN,ORANGE,NAVY][:len(rem_analyst)], edgecolor='white', width=0.5)
ax1.bar_label(bars1, fmt='%.1f d', padding=3, fontsize=10, fontweight='bold', color=NAVY)
ax1.set_title("Avg Days to Resolve by Analyst", pad=12)
ax1.set_ylabel("Days", color=GREY); ax1.tick_params(colors=GREY, labelsize=9)

bars2 = ax2.bar(rem_analyst['initiated_by'], rem_analyst['resolution_rate'],
                color=[GREEN if v >= 50 else ORANGE for v in rem_analyst['resolution_rate']],
                edgecolor='white', width=0.5)
ax2.bar_label(bars2, fmt='%.1f%%', padding=3, fontsize=10, fontweight='bold', color=NAVY)
ax2.set_title("Resolution Rate by Analyst (%)", pad=12)
ax2.set_ylabel("Resolution Rate %", color=GREY); ax2.set_ylim(0, 100)
ax2.tick_params(colors=GREY, labelsize=9)
ax2.axhline(50, color=RED, linewidth=1.5, linestyle='--', alpha=0.6, label='50% threshold')
ax2.legend(fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(SHOTS_DIR, '05_remediation_efficiency.png'), dpi=150, bbox_inches='tight')
plt.close(); print("✓ 05_remediation_efficiency.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 6 — Customer Risk Profile vs Actual Anomalies
# ════════════════════════════════════════════════════════════════════════════
merged = customers.merge(
    anomalies.groupby('customer_id').size().reset_index(name='anomaly_count'),
    on='customer_id', how='left').fillna(0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor(BG)

# Grouped bar — avg anomalies per risk profile per segment
pivot = merged.groupby(['risk_profile','segment'])['anomaly_count'].mean().unstack(fill_value=0)
pivot.plot(kind='bar', ax=ax1, color=[LBLUE,BLUE,NAVY,ORANGE,GREEN][:len(pivot.columns)],
           edgecolor='white', linewidth=0.8, width=0.7)
ax1.set_title("Avg Anomalies: Risk Profile × Segment", pad=12)
ax1.set_xlabel(""); ax1.set_ylabel("Avg Anomaly Count", color=GREY)
ax1.tick_params(axis='x', rotation=0, labelsize=10); ax1.tick_params(colors=GREY)
ax1.legend(title="Segment", fontsize=9, title_fontsize=9)

# Scatter — anomaly score vs amount
ax2.scatter(anomalies['amount_pkr']/1000, anomalies['anomaly_score'],
            c=anomalies['severity'].map({'Critical':RED,'High':ORANGE,'Medium':BLUE,'Low':GREEN}),
            alpha=0.55, s=40, edgecolors='white', linewidths=0.4)
ax2.set_title("Anomaly Score vs Transaction Amount", pad=12)
ax2.set_xlabel("Amount (PKR '000)", color=GREY)
ax2.set_ylabel("Anomaly Score", color=GREY)
ax2.tick_params(colors=GREY)
legend_elements = [mpatches.Patch(color=RED,label='Critical'), mpatches.Patch(color=ORANGE,label='High'),
                   mpatches.Patch(color=BLUE,label='Medium'),   mpatches.Patch(color=GREEN,label='Low')]
ax2.legend(handles=legend_elements, fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(SHOTS_DIR, '06_customer_risk_profile.png'), dpi=150, bbox_inches='tight')
plt.close(); print("✓ 06_customer_risk_profile.png")

# ─── Export KPI Summary ─────────────────────────────────────────────────────
kpi_summary = pd.DataFrame({
    'KPI': ['Total Transactions','Flagged Transactions','Flag Rate (%)','Total Anomalies',
            'Critical Anomalies','Open Cases','FMU Reports Filed','Avg Days to Resolve'],
    'Value': [total_txns, int(flagged_txns), flag_rate, total_anomalies,
              critical_ano, open_anomalies, int(fmu_reports), avg_resolve_days]
})
kpi_summary.to_csv(os.path.join(DATA_DIR, 'kpi_summary.csv'), index=False)
print("✓ kpi_summary.csv")
print("\n✅ All charts + summary generated!")
