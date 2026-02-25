from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.modules.sales.schemas.sales_invoice import (
    SalesInvoiceCreate, SalesInvoiceResponse, SalesInvoiceCancelRequest
)
from app.modules.sales.services.sales_invoice_service import (
    create_invoice, get_invoice, cancel_invoice, list_invoices
)

router = APIRouter(prefix="/sales/invoices", tags=["Sales Invoices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SalesInvoiceResponse)
def create(dto: SalesInvoiceCreate, db: Session = Depends(get_db)):
    return create_invoice(db, dto)

@router.get("/", response_model=list[SalesInvoiceResponse])
def list_all(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return list_invoices(db, limit, offset)

@router.get("/{invoice_id}", response_model=SalesInvoiceResponse)
def get_one(invoice_id: int, db: Session = Depends(get_db)):
    return get_invoice(db, invoice_id)

@router.post("/{invoice_id}/cancel", response_model=SalesInvoiceResponse)
def cancel(invoice_id: int, body: SalesInvoiceCancelRequest, db: Session = Depends(get_db)):
    return cancel_invoice(db, invoice_id, body.reason)