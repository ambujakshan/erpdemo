from sqlalchemy.orm import Session
from sqlalchemy import select
from app.modules.sales.models.sales_invoice import SalesInvoice

def get_by_id(db: Session, invoice_id: int) -> SalesInvoice | None:
    return db.get(SalesInvoice, invoice_id)

def list_invoices(db: Session, limit: int = 50, offset: int = 0) -> list[SalesInvoice]:
    stmt = select(SalesInvoice).order_by(SalesInvoice.id.desc()).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())

def exists_invoice_no(db: Session, invoice_no: str) -> bool:
    stmt = select(SalesInvoice.id).where(SalesInvoice.invoice_no == invoice_no)
    return db.execute(stmt).first() is not None

def save(db: Session, inv: SalesInvoice) -> SalesInvoice:
    db.add(inv)
    db.flush()   # assigns ID
    return inv