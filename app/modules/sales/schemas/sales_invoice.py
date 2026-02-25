from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

class SalesInvoiceItemCreate(BaseModel):
    product_id: int | None = None
    description: str | None = None
    qty: Decimal = Field(gt=0)
    unit_price: Decimal = Field(ge=0)
    discount: Decimal = Field(ge=0, default=0)
    tax: Decimal = Field(ge=0, default=0)

class SalesInvoiceCreate(BaseModel):
    customer_id: int | None = None
    invoice_date: datetime | None = None
    items: list[SalesInvoiceItemCreate]

class SalesInvoiceItemResponse(BaseModel):
    id: int
    line_no: int
    product_id: int | None
    description: str | None
    qty: Decimal
    unit_price: Decimal
    discount: Decimal
    tax: Decimal
    line_total: Decimal

    class Config:
        from_attributes = True

class SalesInvoiceResponse(BaseModel):
    id: int
    invoice_no: str
    invoice_date: datetime
    customer_id: int | None
    status: str
    subtotal: Decimal
    tax_total: Decimal
    discount_total: Decimal
    net_total: Decimal
    items: list[SalesInvoiceItemResponse]

    class Config:
        from_attributes = True

class SalesInvoiceCancelRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=250)