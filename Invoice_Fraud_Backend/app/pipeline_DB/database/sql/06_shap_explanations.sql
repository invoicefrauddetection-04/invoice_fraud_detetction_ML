DROP TABLE IF EXISTS shap_explanations CASCADE;

CREATE TABLE shap_explanations (

    shap_id SERIAL PRIMARY KEY,

    document_id INTEGER NOT NULL UNIQUE,

    prediction VARCHAR(20) NOT NULL,

    fraud_probability NUMERIC(6,5) NOT NULL,

    base_value DOUBLE PRECISION,

    top_features JSONB NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_shap_document
        FOREIGN KEY (document_id)
        REFERENCES uploaded_documents(document_id)
        ON DELETE CASCADE
);