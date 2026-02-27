from sqlalchemy import Column, Integer, Numeric, String, Boolean, UniqueConstraint
from app.database import Base

class GstRate(Base):
    __tablename__ = "gst_rate"
    __table_args__ = (UniqueConstraint("rate", "category", name="uq_gst_rate_category"),)

    id = Column(Integer, primary_key=True, index=True)
    rate = Column(Numeric(6, 2), nullable=False)      # 0, 5, 12, 18, 28
    category = Column(String(30), nullable=False, default="TAXABLE")
    # TAXABLE / EXEMPT / NIL / ZERO_RATED
    is_active = Column(Boolean, nullable=False, default=True)