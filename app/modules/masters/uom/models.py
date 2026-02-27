from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint
from app.database import Base

class Uom(Base):
    __tablename__ = "uom"
    __table_args__ = (UniqueConstraint("name", name="uq_uom_name"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)          # PCS, BOX, KG
    code = Column(String(20), nullable=True)           # optional
    is_active = Column(Boolean, nullable=False, default=True)