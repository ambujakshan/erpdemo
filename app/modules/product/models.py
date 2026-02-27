from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)

    product_code = Column(String(50), nullable=False, unique=True)
    product_name = Column(String(150), nullable=False)
    product_type = Column(String(20), nullable=False)  # GOODS / SERVICE / FIXED_ASSET

    base_uom_id = Column(Integer, ForeignKey("uom.id"), nullable=False)   # ✅ base unit
    hsn_id = Column(Integer, ForeignKey("hsn.id"), nullable=False)
    tax_master_id = Column(Integer, ForeignKey("tax_master.id"), nullable=False)

    selling_price_excl_tax = Column(Numeric(12, 2), nullable=False, default=0)
    selling_price_incl_tax = Column(Numeric(12, 2), nullable=False, default=0)

    brand = Column(String(80), nullable=True)
    manufacturer = Column(String(120), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    base_uom = relationship("Uom")
    hsn = relationship("Hsn")
    tax_master = relationship("TaxMaster")