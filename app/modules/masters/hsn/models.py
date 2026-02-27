from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from app.database import Base

class Hsn(Base):
    __tablename__ = "hsn"
    __table_args__ = (UniqueConstraint("code", name="uq_hsn_code"),)

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), nullable=False)     # HSN or SAC
    description = Column(String(255), nullable=True)
    is_service = Column(Boolean, nullable=False, default=False)  # False=Goods(HNS), True=Service(SAC)
    is_active = Column(Boolean, nullable=False, default=True)