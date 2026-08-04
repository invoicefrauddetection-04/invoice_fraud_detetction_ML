from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routes.upload import router as upload_router
from app.routes.llm import router as llm_router

app = FastAPI(
    title="Invoice Fraud Detection API",
    version="1.0.0"
)

# -------------------------------------------------------
# CORS Configuration
# -------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Change to specific frontend URL in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# Register Routes
# -------------------------------------------------------
app.include_router(upload_router)
app.include_router(llm_router)

# -------------------------------------------------------
# Root Endpoint
# -------------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "Invoice Fraud Detection Backend Running"
    }