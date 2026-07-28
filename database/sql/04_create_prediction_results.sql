DROP TABLE IF EXISTS prediction_results CASCADE;

CREATE TABLE prediction_results (

    prediction_id SERIAL PRIMARY KEY,

    document_id INT NOT NULL,

    supplier_id VARCHAR(100),

    prediction BOOLEAN NOT NULL,

    fraud_probability DECIMAL(6,5),

    model_name VARCHAR(100),

    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_document
        FOREIGN KEY(document_id)
        REFERENCES uploaded_documents(document_id)
        ON DELETE CASCADE
);