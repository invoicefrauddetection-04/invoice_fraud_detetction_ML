DROP TABLE IF EXISTS prediction_results CASCADE;

CREATE TABLE prediction_results (

    prediction_id SERIAL PRIMARY KEY,

    document_id INT UNIQUE NOT NULL,

    prediction VARCHAR(20) NOT NULL,

    fraud_probability DECIMAL(6,4) NOT NULL,

    model_name VARCHAR(100) NOT NULL,

    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_prediction_document
        FOREIGN KEY (document_id)
        REFERENCES uploaded_documents(document_id)
        ON DELETE CASCADE

);