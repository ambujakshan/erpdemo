from sqlalchemy import Column, Integer, Boolean, Numeric, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship
from app.database import Base

class ProductUom(Base):
    __tablename__ = "product_uom"
    __table_args__ = (
        UniqueConstraint("product_id", "uom_id", name="uq_product_uom_product_uom"),
    )

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    uom_id = Column(Integer, ForeignKey("uom.id"), nullable=False)

    # factor to base unit: qty_in_base = qty * factor
    factor = Column(Numeric(18, 6), nullable=False, default=1)

    is_base = Column(Boolean, nullable=False, default=False)
    is_sales = Column(Boolean, nullable=False, default=True)
    is_purchase = Column(Boolean, nullable=False, default=True)

    # optional per-UOM barcode / prices (useful in pharmacy / retail)
    barcode = Column(String(80), nullable=True)
    selling_price_excl_tax = Column(Numeric(12, 2), nullable=True)
    purchase_price = Column(Numeric(12, 2), nullable=True)

    product = relationship("Product")
    uom = relationship("Uom")