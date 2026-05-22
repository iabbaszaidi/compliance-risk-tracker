# ðŸ¦ Compliance & Risk Data Tracker Framework
### Transaction Anomaly Detection Â· Risk Register Â· Remediation Audit Trail

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Domain](https://img.shields.io/badge/Domain-Compliance%20%26%20Risk-C0392B)
![Status](https://img.shields.io/badge/Status-Complete-1E8449)

---

## ðŸ“Œ Project Overview

This project simulates a **Compliance & Risk analytics pipeline** for a digital banking environment,
covering transaction anomaly detection, customer risk profiling, remediation tracking, and
governance-style audit trail documentation.

It mirrors real-world workflows used in banking compliance functions â€” including AML monitoring,
risk register maintenance, and FMU (Financial Monitoring Unit) reporting.

| Dataset | Description | Records |
|---------|-------------|---------|
| `customers.csv` | Customer profiles with KYC & risk classification | 200 |
| `transactions.csv` | Banking transactions with anomaly flags | 2,000 |
| `anomaly_flags.csv` | Detected anomalies with severity & analyst assignment | 311 |
| `risk_register.csv` | Customer-level risk assessments | 120 |
| `remediation_log.csv` | Remediation actions with audit trail references | 311 |

**Total: 2,942 records across 5 linked tables**

---

## ðŸ“Š Dashboard Screenshots

### KPI Overview
![KPI Dashboard](screenshots/01_kpi_dashboard.png)

### Transaction Volume & Flagging Trend
![Transaction Trend](screenshots/02_transaction_trend.png)

### Anomaly Severity & Risk Category Analysis
![Anomaly Analysis](screenshots/03_anomaly_analysis.png)

### Branch-Level Risk Concentration
![Branch Risk](screenshots/04_branch_risk.png)

### Remediation Efficiency by Analyst
![Remediation](screenshots/05_remediation_efficiency.png)

### Customer Risk Profile vs Actual Anomalies
![Customer Risk](screenshots/06_customer_risk_profile.png)

---

## ðŸ—‚ï¸ Project Structure

```
compliance-risk-tracker/
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ customers.csv
â”‚   â”œâ”€â”€ transactions.csv
â”‚   â”œâ”€â”€ anomaly_flags.csv
â”‚   â”œâ”€â”€ risk_register.csv
â”‚   â”œâ”€â”€ remediation_log.csv
â”‚   â””â”€â”€ kpi_summary.csv
â”œâ”€â”€ scripts/
â”‚   â”œâ”€â”€ generate_data.py        # Synthetic dataset generation
â”‚   â””â”€â”€ analysis.py             # KPI computation + 6 chart exports
â”œâ”€â”€ sql/
â”‚   â””â”€â”€ schema_and_queries.sql  # PostgreSQL schema + 8 analytical queries
â”œâ”€â”€ dashboard/
â”‚   â””â”€â”€ POWERBI_GUIDE.md        # Power BI setup + DAX measures
â”œâ”€â”€ screenshots/                # Auto-generated chart exports (6 PNGs)
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

---

## ðŸš€ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/iabbaszaidi/compliance-risk-tracker.git
cd compliance-risk-tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic datasets
python scripts/generate_data.py

# 4. Run analysis & generate charts
python scripts/analysis.py
```

For PostgreSQL setup, run `sql/schema_and_queries.sql` in your PostgreSQL client
(pgAdmin or psql), then load CSVs using the COPY commands at the bottom of the file.

For Power BI setup, follow [`dashboard/POWERBI_GUIDE.md`](dashboard/POWERBI_GUIDE.md).

---

## ðŸ“ Key KPIs Tracked

| KPI | Value (Sample Run) |
|-----|--------------------|
| Total Transactions | 2,000 |
| Flagged Transactions | 311 (15.6%) |
| Critical Anomalies | 56 |
| Open Cases | 194 |
| FMU Reports Filed | 30 |
| Avg Days to Resolve | 14.8 days |

---

## ðŸ” Analytical Highlights

- **Anomaly Detection**: Rule-based + statistical threshold flags on transaction amount outliers
- **Risk Scoring**: Customer risk profiles (Low / Medium / High) cross-validated against actual anomaly frequency      
- **Branch Risk Heatmap**: Identifies which branches contribute most to flagged amounts
- **Remediation Audit Trail**: Every case linked to an analyst, action taken, outcome, and audit reference
- **FMU Reporting**: Cases escalated to the Financial Monitoring Unit tracked separately

---

## ðŸ› ï¸ Tech Stack

| Tool | Use |
|------|-----|
| Python 3.x | Data generation, transformation, analysis |
| Pandas | Data manipulation & aggregation |
| NumPy | Statistical computations |
| Matplotlib | 6 governance-style chart exports |
| PostgreSQL | Relational schema + 8 analytical SQL queries |
| Power BI Desktop | Interactive compliance dashboard (6 pages) |

---

## ðŸ‘¤ Author

**Mohammad Abbas**
BSc Software Engineering â€” University of Karachi (2025)
Data Analytics Intern â€” Meezan Bank Limited
ðŸ“§ mohammadabbas456@outlook.com
ðŸ”— [LinkedIn](https://linkedin.com/in/mohammad-abbas-a23951248) | [GitHub](https://github.com/iabbaszaidi)

---

## ðŸ“„ License

MIT License â€” see [LICENSE](LICENSE)
