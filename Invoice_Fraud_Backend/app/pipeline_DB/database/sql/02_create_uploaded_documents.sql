CREATE TABLE uploaded_documents (

    document_id SERIAL PRIMARY KEY,
    image_name VARCHAR(255) NOT NULL,
    page_number INT NOT NULL,
    bucket_name VARCHAR(100) NOT NULL,
    object_key VARCHAR(500) NOT NULL,
    upload_timestamp TIMESTAMP,
    processing_status VARCHAR(30)

);