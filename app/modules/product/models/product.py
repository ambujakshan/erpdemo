from sqlalchemy import Column, Integer, String, Boolean, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)

    # A) Identification
    product_code = Column(String(50), unique=True, index=True, nullable=False)
    product_name = Column(String(200), nullable=False)
    short_name = Column(String(100))
    barcode = Column(String(100), unique=True)
    internal_id = Column(String(100), unique=True)

    # B) Classification
    category = Column(String(100))
    subcategory = Column(String(100))
    department = Column(String(100))
    brand = Column(String(100))
    manufacturer = Column(String(100))

    product_class = Column(String(20))   # GOODS / SERVICE / INS
    product_type = Column(String(20))    # STOCK / SERVICE / NON_STOCK / BUNDLE
    asset_type = Column(String(20))      # NORMAL / FIXED_ASSET

    hsn_sac = Column(String(50))

    # C) Pricing
    selling_price = Column(Numeric(18,3), default=0)
    cost_price = Column(Numeric(18,3), default=0)
    max_discount_percent = Column(Numeric(5,2), default=0)

    # D) Tax
    tax_category = Column(String(50))
    output_tax_percent = Column(Numeric(5,2), default=0)
    input_tax_percent = Column(Numeric(5,2), default=0)
    tax_inclusive = Column(Boolean, default=False)

    output_tax_ledger = Column(String(100))
    input_tax_ledger = Column(String(100))

    # E) Units
    base_unit = Column(String(20))
    allow_fraction = Column(Boolean, default=False)
    min_sale_unit = Column(String(20))

    # F) Inventory Control
    track_stock = Column(Boolean, default=True)
    batch_tracking = Column(Boolean, default=False)
    expiry_tracking = Column(Boolean, default=False)

    reorder_level = Column(Numeric(18,3), default=0)
    max_stock_level = Column(Numeric(18,3), default=0)

    preferred_supplier = Column(String(100))
    storage_location = Column(String(100))

    valuation_method = Column(String(30))

    # Relationships
    price_levels = relationship("ProductPrice", back_populates="product")
    units = relationship("ProductUnit", back_populates="product")