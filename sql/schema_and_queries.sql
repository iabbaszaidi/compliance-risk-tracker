-- ============================================================
-- Compliance & Risk Data Tracker Framework
-- PostgreSQL Schema + Analytical Queries
-- Author: Mohammad Abbas
-- ============================================================

-- ─── CREATE SCHEMA ──────────────────────────────────────────

CREATE SCHEMA IF NOT EXISTS compliance;

-- ─── TABLE 1: customers ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS compliance.customers (
    customer_id       VARCHAR(10)  PRIMARY KEY,
    segment           VARCHAR(20)  NOT NULL,
    branch            VARCHAR(40)  NOT NULL,
    account_type      VARCHAR(30)  NOT NULL,
    onboarding_date   DATE         NOT NULL,
    kyc_status        VARCHAR(20)  NOT NULL,
    risk_profile      VARCHAR(10)  NOT NULL,
    is_active         SMALLINT     DEFAULT 1,
    created_at        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ─── TABLE 2: transactions ───────────────────────────────────
CREATE TABLE IF NOT EXISTS compliance.transactions (
    txn_id            VARCHAR(10)  PRIMARY KEY,
    customer_id       VARCHAR(10)  REFERENCES compliance.customers(customer_id),
    txn_date          DATE         NOT NULL,
    txn_type          VARCHAR(30)  NOT NULL,
    amount_pkr        NUMERIC(15,2) NOT NULL,
    branch            VARCHAR(40),
    channel           VARCHAR(20),
    currency          VARCHAR(5)   DEFAULT 'PKR',
    counterparty      VARCHAR(20),
    is_cross_border   SMALLINT     DEFAULT 0,
    flagged           SMALLINT     DEFAULT 0,
    status            VARCHAR(20),
    created_at        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_txn_customer   ON compliance.transactions(customer_id);
CREATE INDEX idx_txn_date       ON compliance.transactions(txn_date);
CREATE INDEX idx_txn_flagged    ON compliance.transactions(flagged);

-- ─── TABLE 3: anomaly_flags ──────────────────────────────────
CREATE TABLE IF NOT EXISTS compliance.anomaly_flags (
    anomaly_id          VARCHAR(10)  PRIMARY KEY,
    txn_id              VARCHAR(10)  REFERENCES compliance.transactions(txn_id),
    customer_id         VARCHAR(10)  REFERENCES compliance.customers(customer_id),
    detection_date      DATE         NOT NULL,
    risk_category       VARCHAR(40)  NOT NULL,
    severity            VARCHAR(10)  NOT NULL,
    amount_pkr          NUMERIC(15,2),
    anomaly_score       NUMERIC(5,3),
    detection_method    VARCHAR(40),
    assigned_analyst    VARCHAR(30),
    status              VARCHAR(30),
    resolution_date     DATE,
    branch              VARCHAR(40),
    created_at          TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ano_customer   ON compliance.anomaly_flags(customer_id);
CREATE INDEX idx_ano_severity   ON compliance.anomaly_flags(severity);
CREATE INDEX idx_ano_status     ON compliance.anomaly_flags(status);

-- ─── TABLE 4: risk_register ──────────────────────────────────
CREATE TABLE IF NOT EXISTS compliance.risk_register (
    risk_id                   VARCHAR(10)  PRIMARY KEY,
    customer_id               VARCHAR(10)  REFERENCES compliance.customers(customer_id),
    segment                   VARCHAR(20),
    branch                    VARCHAR(40),
    risk_category             VARCHAR(40)  NOT NULL,
    inherent_risk             VARCHAR(10)  NOT NULL,
    control_effectiveness     VARCHAR(20),
    residual_risk             VARCHAR(10),
    last_assessed_date        DATE,
    next_review_date          DATE,
    assigned_analyst          VARCHAR(30),
    escalated_to_compliance   SMALLINT    DEFAULT 0,
    remarks                   TEXT,
    created_at                TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- ─── TABLE 5: remediation_log ────────────────────────────────
CREATE TABLE IF NOT EXISTS compliance.remediation_log (
    remediation_id    VARCHAR(10)  PRIMARY KEY,
    anomaly_id        VARCHAR(10)  REFERENCES compliance.anomaly_flags(anomaly_id),
    customer_id       VARCHAR(10)  REFERENCES compliance.customers(customer_id),
    action_taken      VARCHAR(50)  NOT NULL,
    initiated_by      VARCHAR(30),
    initiation_date   DATE,
    completion_date   DATE,
    days_to_resolve   INT,
    outcome           VARCHAR(30),
    fmu_reported      SMALLINT    DEFAULT 0,
    audit_trail_ref   VARCHAR(20),
    created_at        TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════════
-- ANALYTICAL QUERIES
-- ═══════════════════════════════════════════════════════════════

-- ── Q1: Monthly Anomaly Detection Trend ─────────────────────────
SELECT
    DATE_TRUNC('month', detection_date)::DATE   AS month,
    COUNT(*)                                     AS total_anomalies,
    SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) AS critical,
    SUM(CASE WHEN severity = 'High'     THEN 1 ELSE 0 END) AS high,
    ROUND(AVG(anomaly_score)::NUMERIC, 3)        AS avg_score
FROM compliance.anomaly_flags
GROUP BY 1
ORDER BY 1;

-- ── Q2: Top Risk Categories by Total Flagged Amount ─────────────
SELECT
    risk_category,
    COUNT(*)                              AS anomaly_count,
    ROUND(SUM(amount_pkr)::NUMERIC, 2)   AS total_amount_pkr,
    ROUND(AVG(amount_pkr)::NUMERIC, 2)   AS avg_amount_pkr,
    COUNT(DISTINCT customer_id)          AS unique_customers
FROM compliance.anomaly_flags
GROUP BY risk_category
ORDER BY total_amount_pkr DESC;

-- ── Q3: Customer Risk Profile vs Actual Anomalies ────────────────
SELECT
    c.risk_profile,
    c.segment,
    COUNT(DISTINCT c.customer_id)   AS total_customers,
    COUNT(a.anomaly_id)             AS anomalies_raised,
    ROUND(
        COUNT(a.anomaly_id)::NUMERIC /
        NULLIF(COUNT(DISTINCT c.customer_id), 0), 2
    )                               AS anomalies_per_customer
FROM compliance.customers c
LEFT JOIN compliance.anomaly_flags a ON c.customer_id = a.customer_id
GROUP BY c.risk_profile, c.segment
ORDER BY anomalies_per_customer DESC;

-- ── Q4: Remediation Efficiency by Analyst ────────────────────────
SELECT
    initiated_by                            AS analyst,
    COUNT(*)                                AS cases_handled,
    ROUND(AVG(days_to_resolve)::NUMERIC, 1) AS avg_days_to_resolve,
    MIN(days_to_resolve)                    AS fastest_resolution,
    MAX(days_to_resolve)                    AS slowest_resolution,
    SUM(fmu_reported)                       AS fmu_reported_count,
    SUM(CASE WHEN outcome = 'Resolved' THEN 1 ELSE 0 END) AS resolved_count
FROM compliance.remediation_log
GROUP BY initiated_by
ORDER BY avg_days_to_resolve;

-- ── Q5: Branch-Level Risk Concentration ─────────────────────────
SELECT
    a.branch,
    COUNT(a.anomaly_id)                          AS total_anomalies,
    SUM(CASE WHEN a.severity = 'Critical' THEN 1 ELSE 0 END) AS critical_count,
    ROUND(SUM(a.amount_pkr)::NUMERIC, 2)         AS total_flagged_amount,
    ROUND(AVG(a.anomaly_score)::NUMERIC, 3)      AS avg_risk_score,
    COUNT(DISTINCT a.customer_id)                AS unique_customers
FROM compliance.anomaly_flags a
GROUP BY a.branch
ORDER BY total_flagged_amount DESC;

-- ── Q6: Open Anomalies Pending Remediation (Audit Trail View) ────
SELECT
    a.anomaly_id,
    a.customer_id,
    a.detection_date,
    a.risk_category,
    a.severity,
    a.amount_pkr,
    a.assigned_analyst,
    a.status,
    r.action_taken,
    r.outcome,
    r.audit_trail_ref,
    CURRENT_DATE - a.detection_date          AS days_since_detection
FROM compliance.anomaly_flags a
LEFT JOIN compliance.remediation_log r ON a.anomaly_id = r.anomaly_id
WHERE a.status IN ('Open', 'Under Review', 'Escalated')
ORDER BY a.severity DESC, days_since_detection DESC;

-- ── Q7: KPI Summary View (for Power BI) ─────────────────────────
SELECT
    'Total Transactions'            AS kpi,
    COUNT(*)::TEXT                  AS value
FROM compliance.transactions
UNION ALL
SELECT 'Flagged Transactions',
    COUNT(*)::TEXT
FROM compliance.transactions WHERE flagged = 1
UNION ALL
SELECT 'Flag Rate (%)',
    ROUND(100.0 * SUM(flagged) / COUNT(*), 2)::TEXT
FROM compliance.transactions
UNION ALL
SELECT 'Total Anomalies Detected',
    COUNT(*)::TEXT
FROM compliance.anomaly_flags
UNION ALL
SELECT 'Critical Anomalies',
    COUNT(*)::TEXT
FROM compliance.anomaly_flags WHERE severity = 'Critical'
UNION ALL
SELECT 'Open Anomalies',
    COUNT(*)::TEXT
FROM compliance.anomaly_flags WHERE status IN ('Open','Under Review','Escalated')
UNION ALL
SELECT 'FMU Reports Filed',
    SUM(fmu_reported)::TEXT
FROM compliance.remediation_log
UNION ALL
SELECT 'Avg Days to Resolve',
    ROUND(AVG(days_to_resolve), 1)::TEXT
FROM compliance.remediation_log;

-- ── Q8: Load CSVs into PostgreSQL (run after creating tables) ────
-- COPY compliance.customers         FROM '/path/to/data/customers.csv'         CSV HEADER;
-- COPY compliance.transactions      FROM '/path/to/data/transactions.csv'      CSV HEADER;
-- COPY compliance.anomaly_flags     FROM '/path/to/data/anomaly_flags.csv'     CSV HEADER;
-- COPY compliance.risk_register     FROM '/path/to/data/risk_register.csv'     CSV HEADER;
-- COPY compliance.remediation_log   FROM '/path/to/data/remediation_log.csv'   CSV HEADER;
