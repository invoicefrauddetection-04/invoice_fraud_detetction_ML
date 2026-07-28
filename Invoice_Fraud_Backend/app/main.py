from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routes.upload import router as upload_router

app = FastAPI(
    title="Invoice Fraud Detection API",
    version="1.0"
)

'''app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://192.168.2.214:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)'''

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "Invoice Fraud Detection Backend Running"
    }