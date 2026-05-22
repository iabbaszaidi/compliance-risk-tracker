"""
generate_data.py
Generates synthetic banking transaction datasets with anomalies,
risk flags, and remediation records.
Run once to produce all CSV files under ../data/
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(99)
np.random.seed(99)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

START = datetime(2024, 1, 1)
END   = datetime(2025, 3, 31)

def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# ─── Reference Data ─────────────────────────────────────────────────────────
branches       = ['Karachi-Main', 'Karachi-Clifton', 'Lahore-Gulberg',
                  'Islamabad-Blue Area', 'Faisalabad-Central', 'Quetta-Branch']
txn_types      = ['IBFT', 'Cash Deposit', 'Cash Withdrawal', 'Bill Payment',
                  'POS Purchase', 'ATM Withdrawal', 'Wire Transfer', 'Loan Disbursement']
risk_categories = ['AML Suspicion', 'Structuring', 'Unusual Velocity',
                   'High-Value Cash', 'Sanctioned Entity', 'Dormant Account Activation',
                   'Rapid Fund Movement', 'Cross-Border Alert']
segments       = ['Retail', 'SME', 'Corporate', 'Priority', 'Islamic']
analysts       = ['Analyst_A', 'Analyst_B', 'Analyst_C', 'Compliance_Team']
remediations   = ['Under Review', 'Escalated to Compliance', 'Cleared', 'Reported to FMU',
                  'Account Frozen', 'Closed - No Action']

# ════════════════════════════════════════════════════════════════════════════
# 1. customers.csv  (200 customers)
# ════════════════════════════════════════════════════════════════════════════
customers = []
for i in range(1, 201):
    onboard = rand_date(datetime(2018, 1, 1), datetime(2023, 12, 31))
    customers.append({
        'customer_id'     : f'CUST-{i:04d}',
        'segment'         : random.choice(segments),
        'branch'          : random.choice(branches),
        'account_type'    : random.choice(['Current', 'Savings', 'Term Deposit', 'Islamic Savings']),
        'onboarding_date' : onboard.strftime('%Y-%m-%d'),
        'kyc_status'      : random.choice(['Verified', 'Verified', 'Verified', 'Pending', 'Expired']),
        'risk_profile'    : random.choice(['Low', 'Low', 'Medium', 'Medium', 'High']),
        'is_active'       : random.choice([1, 1, 1, 0]),
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv(os.path.join(OUTPUT_DIR, 'customers.csv'), index=False)
print(f"✓ customers.csv            ({len(df_customers)} rows)")

# ════════════════════════════════════════════════════════════════════════════
# 2. transactions.csv  (2000 transactions)
# ════════════════════════════════════════════════════════════════════════════
transactions = []
for i in range(1, 2001):
    cust = random.choice(customers)
    txn_date = rand_date(START, END)
    amount = round(np.random.lognormal(mean=10.5, sigma=1.8), 2)
    # Inject anomaly signals for ~15% of transactions
    is_anomaly = random.random() < 0.15
    if is_anomaly:
        amount = round(amount * random.uniform(8, 25), 2)  # unusually large

    transactions.append({
        'txn_id'         : f'TXN-{i:05d}',
        'customer_id'    : cust['customer_id'],
        'txn_date'       : txn_date.strftime('%Y-%m-%d'),
        'txn_type'       : random.choice(txn_types),
        'amount_pkr'     : amount,
        'branch'         : cust['branch'],
        'channel'        : random.choice(['Branch', 'Online', 'ATM', 'Mobile App', 'POS']),
        'currency'       : random.choice(['PKR', 'PKR', 'PKR', 'USD', 'AED']),
        'counterparty'   : f'ENTITY-{random.randint(1, 500):03d}',
        'is_cross_border': 1 if random.random() < 0.12 else 0,
        'flagged'        : 1 if is_anomaly else 0,
        'status'         : random.choice(['Completed', 'Completed', 'Completed', 'Pending', 'Reversed']),
    })

df_txn = pd.DataFrame(transactions)
df_txn.to_csv(os.path.join(OUTPUT_DIR, 'transactions.csv'), index=False)
print(f"✓ transactions.csv         ({len(df_txn)} rows)")

# ════════════════════════════════════════════════════════════════════════════
# 3. anomaly_flags.csv  (anomalies from flagged transactions)
# ════════════════════════════════════════════════════════════════════════════
flagged_txns = [t for t in transactions if t['flagged'] == 1]
anomalies = []
for i, txn in enumerate(flagged_txns, 1):
    detected = datetime.strptime(txn['txn_date'], '%Y-%m-%d') + timedelta(days=random.randint(1, 5))
    resolved = detected + timedelta(days=random.randint(3, 45))
    severity = random.choice(['Critical', 'High', 'High', 'Medium', 'Low'])
    anomalies.append({
        'anomaly_id'          : f'ANO-{i:04d}',
        'txn_id'              : txn['txn_id'],
        'customer_id'         : txn['customer_id'],
        'detection_date'      : detected.strftime('%Y-%m-%d'),
        'risk_category'       : random.choice(risk_categories),
        'severity'            : severity,
        'amount_pkr'          : txn['amount_pkr'],
        'anomaly_score'       : round(random.uniform(0.55, 0.99), 3),
        'detection_method'    : random.choice(['Rule-Based', 'Statistical Threshold',
                                               'Peer Group Analysis', 'Velocity Check']),
        'assigned_analyst'    : random.choice(analysts),
        'status'              : random.choice(['Open', 'Open', 'Under Review',
                                               'Cleared', 'Escalated', 'Reported']),
        'resolution_date'     : resolved.strftime('%Y-%m-%d'),
        'branch'              : txn['branch'],
    })

df_anomalies = pd.DataFrame(anomalies)
df_anomalies.to_csv(os.path.join(OUTPUT_DIR, 'anomaly_flags.csv'), index=False)
print(f"✓ anomaly_flags.csv        ({len(df_anomalies)} rows)")

# ════════════════════════════════════════════════════════════════════════════
# 4. risk_register.csv  (customer-level risk assessments)
# ════════════════════════════════════════════════════════════════════════════
risk_records = []
sampled_customers = random.sample(customers, 120)
for i, cust in enumerate(sampled_customers, 1):
    assessed = rand_date(START, END)
    next_rev  = assessed + timedelta(days=random.choice([90, 180, 365]))
    risk_records.append({
        'risk_id'            : f'RSK-{i:04d}',
        'customer_id'        : cust['customer_id'],
        'segment'            : cust['segment'],
        'branch'             : cust['branch'],
        'risk_category'      : random.choice(risk_categories),
        'inherent_risk'      : random.choice(['Low', 'Medium', 'High', 'Critical']),
        'control_effectiveness': random.choice(['Strong', 'Adequate', 'Weak', 'Not Tested']),
        'residual_risk'      : random.choice(['Low', 'Medium', 'High']),
        'last_assessed_date' : assessed.strftime('%Y-%m-%d'),
        'next_review_date'   : next_rev.strftime('%Y-%m-%d'),
        'assigned_analyst'   : random.choice(analysts),
        'escalated_to_compliance': random.choice([0, 0, 0, 1]),
        'remarks'            : random.choice(['Monitoring ongoing', 'Escalated for review',
                                              'Controls adequate', 'Requires enhanced due diligence']),
    })

df_risk = pd.DataFrame(risk_records)
df_risk.to_csv(os.path.join(OUTPUT_DIR, 'risk_register.csv'), index=False)
print(f"✓ risk_register.csv        ({len(df_risk)} rows)")

# ════════════════════════════════════════════════════════════════════════════
# 5. remediation_log.csv  (remediation actions taken on anomalies)
# ════════════════════════════════════════════════════════════════════════════
remediation_log = []
for i, ano in enumerate(anomalies, 1):
    initiated = datetime.strptime(ano['detection_date'], '%Y-%m-%d') + timedelta(days=random.randint(1, 3))
    completed = initiated + timedelta(days=random.randint(2, 30))
    remediation_log.append({
        'remediation_id'     : f'REM-{i:04d}',
        'anomaly_id'         : ano['anomaly_id'],
        'customer_id'        : ano['customer_id'],
        'action_taken'       : random.choice(remediations),
        'initiated_by'       : random.choice(analysts),
        'initiation_date'    : initiated.strftime('%Y-%m-%d'),
        'completion_date'    : completed.strftime('%Y-%m-%d'),
        'days_to_resolve'    : (completed - initiated).days,
        'outcome'            : random.choice(['Resolved', 'Resolved', 'Pending', 'Escalated', 'Reported to FMU']),
        'fmu_reported'       : 1 if random.random() < 0.08 else 0,
        'audit_trail_ref'    : f'AUD-REF-{random.randint(1000,9999)}',
    })

df_rem = pd.DataFrame(remediation_log)
df_rem.to_csv(os.path.join(OUTPUT_DIR, 'remediation_log.csv'), index=False)
print(f"✓ remediation_log.csv      ({len(df_rem)} rows)")

print(f"\n✅ All datasets generated!")
print(f"   Total records: {len(df_customers)+len(df_txn)+len(df_anomalies)+len(df_risk)+len(df_rem)}")
