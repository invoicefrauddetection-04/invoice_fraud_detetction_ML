
--drop table if exists training_invoices;
--drop table if exists uploaded_documents;

--select * 
--from training_invoices;

--select count(*)
--from training_invoices;

/*
SELECT is_fraud, COUNT(*)
FROM training_invoices
GROUP BY is_fraud;
*/

--select *
--from uploaded_documents;

--ALTER TABLE uploaded_documents
--ADD CONSTRAINT unique_object_key UNIQUE (object_key);

--SELECT * 
--FROM ocr_results;

--ALTER TABLE ocr_results
--ADD COLUMN invoice_type VARCHAR(50);

--select distinct supplier_id
--from training_invoices;

/*
SELECT
supplier_id,
invoice_amount,
supplier_invoice_count_30d,
supplier_avg_amount_90d,
supplier_risk_score
FROM training_invoices
LIMIT 5;


SELECT column_name
FROM information_schema.columns
WHERE table_name = 'training_invoices';

SELECT
    supplier_id,
    COUNT(*) AS total_invoices
FROM training_invoices
GROUP BY supplier_id
HAVING COUNT(*) > 1
LIMIT 10;


SELECT
    payment_terms,
    invoice_type
FROM training_invoices
LIMIT 10;
*/

--select *
--from prediction_results;

--select *
--from fraud_dashboard_view;

--DELETE FROM prediction_results WHERE document_id = 8;

SELECT
column_name,
data_type
FROM information_schema.columns
WHERE table_name='ocr_results';


