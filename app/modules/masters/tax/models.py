from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class TaxMaster(Base):
    __tablename__ = "tax_master"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), nullable=False, unique=True)     # "GST 18%"
    tax_type = Column(String(20), nullable=False)              # INTRA / INTER
    gst_rate_id = Column(Integer, ForeignKey("gst_rate.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    gst_rate = relationship("GstRate")