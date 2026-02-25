from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProductUnit(Base):
    __tablename__ = "product_unit"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))

    unit_name = Column(String(20))
    conversion_factor = Column(Numeric(18,3))

    product = relationship("Product", back_populates="units")