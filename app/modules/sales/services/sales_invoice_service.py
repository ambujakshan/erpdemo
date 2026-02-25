from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.modules.sales.constants import STATUS_DRAFT, STATUS_CANCELLED, STATUS_POSTED, SALES_MODULE_CODE
from app.modules.sales.models.sales_invoice import SalesInvoice, SalesInvoiceItem
from app.modules.sales.repositories import sales_invoice_repo

def _calc_totals(inv: SalesInvoice):
    subtotal = Decimal("0")
    disc_total = Decimal("0")
    tax_total = Decimal("0")
    net_total = Decimal("0")

    for i, it in enumerate(inv.items, start=1):
        it.line_no = i
        line_gross = (it.qty or 0) * (it.unit_price or 0)
        line_disc = (it.discount or 0)
        line_tax = (it.tax or 0)
        line_net = line_gross - line_disc + line_tax

        it.line_total = line_net

        subtotal += line_gross
        disc_total += line_disc
        tax_total += line_tax
        net_total += line_net

    inv.subtotal = subtotal
    inv.discount_total = disc_total
    inv.tax_total = tax_total
    inv.net_total = net_total

def _generate_invoice_no(db: Session) -> str:
    # Simple safe approach: use DB sequence-like by max(id)+1
    # For production ERP, we’ll replace with a proper sequence table per company/branch/year.
    last = db.query(SalesInvoice.id).order_by(SalesInvoice.id.desc()).first()
    next_no = (last[0] if last else 0) + 1
    return f"{SALES_MODULE_CODE}-{next_no:06d}"

def create_invoice(db: Session, dto) -> SalesInvoice:
    inv_no = _generate_invoice_no(db)

    inv = SalesInvoice(
        invoice_no=inv_no,
        invoice_date=dto.invoice_date or datetime.now(),
        customer_id=dto.customer_id,
        status=STATUS_DRAFT,
        items=[]
    )

    for it in dto.items:
        inv.items.append(SalesInvoiceItem(
            product_id=it.product_id,
            description=it.description,
            qty=it.qty,
            unit_price=it.unit_price,
            discount=it.discount,
            tax=it.tax,
        ))

    _calc_totals(inv)
    sales_invoice_repo.save(db, inv)
    db.commit()
    db.refresh(inv)
    return inv

def get_invoice(db: Session, invoice_id: int) -> SalesInvoice:
    inv = sales_invoice_repo.get_by_id(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv

def cancel_invoice(db: Session, invoice_id: int, reason: str) -> SalesInvoice:
    inv = get_invoice(db, invoice_id)

    if inv.status == STATUS_CANCELLED:
        raise HTTPException(status_code=400, detail="Invoice already cancelled")

    if inv.status == STATUS_POSTED:
        # In ERP, posted invoices should reverse with Credit Note instead of cancel.
        raise HTTPException(status_code=400, detail="Posted invoice cannot be cancelled. Create credit note.")

    inv.status = STATUS_CANCELLED
    db.commit()
    db.refresh(inv)
    return inv

def list_invoices(db: Session, limit: int, offset: int) -> list[SalesInvoice]:
    return sales_invoice_repo.list_invoices(db, limit=limit, offset=offset)