from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from app.services.prediction_service import get_prediction
from app.services.context_service import get_invoice_context
from app.services.pipeline_service import execute_pipeline


from app.services.s3_service import (
    upload_to_s3,
    list_invoices,
    get_invoice,
    delete_invoice
)

router = APIRouter()

'''
@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    return upload_to_s3(file) ''' 

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):

    upload_response = upload_to_s3(file)
    print(upload_response)

    if upload_response.get("status") != "success":
        return upload_response

    document_id = upload_response["document_id"]

    already_exists = upload_response["already_exists"]

    pipeline_response = execute_pipeline(
        document_id,
        already_exists
    )

    return {
        "upload": upload_response,
        "pipeline": pipeline_response
    }


@router.get("/invoices")
def get_all_invoices():
    return list_invoices()


@router.get("/invoice/{filename}")
def invoice_details(filename: str):
    return get_invoice(filename)


@router.delete("/invoice/{filename}")
def remove_invoice(filename: str):
    return delete_invoice(filename)

# ==========================================================
# GET Prediction
# ==========================================================

@router.get("/prediction/{image_name}")
def prediction(image_name: str):
    return get_prediction(image_name) 

# =========================================================
# Context API
# =========================================================
@router.get("/context/{document_id}")
def invoice_context(document_id: int):
    return get_invoice_context(document_id)