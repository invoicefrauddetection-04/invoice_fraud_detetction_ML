from fastapi import FastAPI
from app.routes.upload import router as upload_router

app = FastAPI(
    title="Invoice Fraud Detection API",
    version="1.0"
)

app.include_router(upload_router)

@app.get("/")
def home():
    return {
        "message": "Invoice Fraud Detection Backend Running"
    }