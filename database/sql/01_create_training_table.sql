DROP TABLE IF EXISTS training_in

CREATE TABLE training_invoices (
    record_id SERIAL PRIMARY KEY,

    supplier_id VARCHAR(50),
    department_id VARCHAR(50),

    invoice_date DATE,
    invoice_amount NUMERIC(12,2),
    currency VARCHAR(10),
    payment_terms VARCHAR(50),
    invoice_type VARCHAR(50),
    submission_hour SMALLINT,

    supplier_invoice_count_30d INTEGER,
    supplier_avg_amount_90d NUMERIC(12,2),
    invoice_amount_zscore NUMERIC(8,4),
    duplicate_invoice_flag BOOLEAN,
    split_invoice_flag BOOLEAN,
    late_night_submission_flag BOOLEAN,

    is_fraud BOOLEAN,
    split VARCHAR(20),

    supplier_country VARCHAR(100),
    supplier_age_days INTEGER,
    supplier_risk_score NUMERIC(5,2),
    blacklisted_flag BOOLEAN,
    avg_invoice_amount NUMERIC(12,2),

    region VARCHAR(100),
    annual_budget NUMERIC(15,2),

    invoice_month SMALLINT,
    invoice_weekday SMALLINT,
    invoice_quarter SMALLINT,
    is_weekend BOOLEAN
);