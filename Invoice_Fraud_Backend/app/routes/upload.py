from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

from app.services.s3_service import (
    upload_to_s3,
    list_invoices,
    get_invoice,
    delete_invoice
)

router = APIRouter()


@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    return upload_to_s3(file)


@router.get("/invoices")
def get_all_invoices():
    return list_invoices()


@router.get("/invoice/{filename}")
def invoice_details(filename: str):
    return get_invoice(filename)


@router.delete("/invoice/{filename}")
def remove_invoice(filename: str):
    return delete_invoice(filename)