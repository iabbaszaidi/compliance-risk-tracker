#  Compliance & Risk Data Tracker Framework
### Transaction Anomaly Detection Â· Risk Register Â· Remediation Audit Trail

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Domain](https://img.shields.io/badge/Domain-Compliance%20%26%20Risk-C0392B)
![Status](https://img.shields.io/badge/Status-Complete-1E8449)

---

##  Project Overview

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

##  Dashboard Screenshots

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







---

##  Key KPIs Tracked

| KPI | Value (Sample Run) |
|-----|--------------------|
| Total Transactions | 2,000 |
| Flagged Transactions | 311 (15.6%) |
| Critical Anomalies | 56 |
| Open Cases | 194 |
| FMU Reports Filed | 30 |
| Avg Days to Resolve | 14.8 days |

---

##  Analytical Highlights

- **Anomaly Detection**: Rule-based + statistical threshold flags on transaction amount outliers
- **Risk Scoring**: Customer risk profiles (Low / Medium / High) cross-validated against actual anomaly frequency      
- **Branch Risk Heatmap**: Identifies which branches contribute most to flagged amounts
- **Remediation Audit Trail**: Every case linked to an analyst, action taken, outcome, and audit reference
- **FMU Reporting**: Cases escalated to the Financial Monitoring Unit tracked separately

---

## ¸ Tech Stack

| Tool | Use |
|------|-----|
| Python 3.x | Data generation, transformation, analysis |
| Pandas | Data manipulation & aggregation |
| NumPy | Statistical computations |
| Matplotlib | 6 governance-style chart exports |
| PostgreSQL | Relational schema + 8 analytical SQL queries |
| Power BI Desktop | Interactive compliance dashboard (6 pages) |

---

##  Author

**Mohammad Abbas**
BSc Software Engineering â€” University of Karachi (2025)
Data Analytics Intern â€” Meezan Bank Limited
ðŸ“§ mohammadabbas456@outlook.com
ðŸ”— [LinkedIn](https://linkedin.com/in/mohammad-abbas-a23951248) | [GitHub](https://github.com/iabbaszaidi)

---

## „ License

MIT License â€” see [LICENSE](LICENSE)
