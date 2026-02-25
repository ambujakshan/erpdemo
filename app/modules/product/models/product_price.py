from sqlalchemy import Column, Integer, Numeric, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class ProductPrice(Base):
    __tablename__ = "product_price"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))

    price_level = Column(String(50))  # Wholesale, Retail, VIP, Branch
    price = Column(Numeric(18,3))

    product = relationship("Product", back_populates="price_levels")