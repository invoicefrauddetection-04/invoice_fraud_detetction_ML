DROP TABLE IF EXISTS ocr_results CASCADE;

CREATE TABLE ocr_results (

    ocr_id SERIAL PRIMARY KEY,

    document_id INT NOT NULL UNIQUE,

    supplier_id VARCHAR(100) NOT NULL,

    invoice_id VARCHAR(100) NOT NULL,

    invoice_date DATE,

    payment_terms VARCHAR(50),

    invoice_type VARCHAR(50),

    supplier_country VARCHAR(100),

    total_amount NUMERIC(15,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_document
        FOREIGN KEY(document_id)
        REFERENCES uploaded_documents(document_id)
        ON DELETE CASCADE
);