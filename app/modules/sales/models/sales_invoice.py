from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class SalesInvoice(Base):
    __tablename__ = "sales_invoice"

    id = Column(Integer, primary_key=True, index=True)

    invoice_no = Column(String(30), unique=True, index=True, nullable=False)
    invoice_date = Column(DateTime, nullable=False, server_default=func.now())

    customer_id = Column(Integer, nullable=True)  # later link customer table
    status = Column(String(20), nullable=False, default="DRAFT")

    subtotal = Column(Numeric(18, 3), nullable=False, default=0)
    tax_total = Column(Numeric(18, 3), nullable=False, default=0)
    discount_total = Column(Numeric(18, 3), nullable=False, default=0)
    net_total = Column(Numeric(18, 3), nullable=False, default=0)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    items = relationship("SalesInvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class SalesInvoiceItem(Base):
    __tablename__ = "sales_invoice_item"

    id = Column(Integer, primary_key=True, index=True)

    invoice_id = Column(Integer, ForeignKey("sales_invoice.id", ondelete="CASCADE"), nullable=False)
    line_no = Column(Integer, nullable=False, default=1)

    product_id = Column(Integer, nullable=True)  # later link product table
    description = Column(String(200), nullable=True)

    qty = Column(Numeric(18, 3), nullable=False, default=1)
    unit_price = Column(Numeric(18, 3), nullable=False, default=0)
    discount = Column(Numeric(18, 3), nullable=False, default=0)
    tax = Column(Numeric(18, 3), nullable=False, default=0)
    line_total = Column(Numeric(18, 3), nullable=False, default=0)

    invoice = relationship("SalesInvoice", back_populates="items")