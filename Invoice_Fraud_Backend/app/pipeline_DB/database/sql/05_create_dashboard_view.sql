CREATE OR REPLACE VIEW fraud_dashboard_view AS

SELECT

    u.document_id,

    u.image_name "file_name",

    u.object_key,

    u.upload_timestamp,

    o.invoice_id,

    o.supplier_id,

    o.invoice_date,

    o.payment_terms,

    o.invoice_type,

    o.supplier_country,

    o.total_amount,

    p.prediction,

    p.fraud_probability,

    p.model_name,

    p.prediction_timestamp

FROM uploaded_documents u

INNER JOIN ocr_results o

ON u.document_id = o.document_id

LEFT JOIN prediction_results p

ON u.document_id = p.document_id;