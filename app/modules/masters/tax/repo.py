from sqlalchemy.orm import Session
from .models import TaxMaster

class TaxRepo:
    def get_by_id(self, db: Session, id: int):
        return db.query(TaxMaster).filter(TaxMaster.id == id).first()

    def get_by_name(self, db: Session, name: str):
        return db.query(TaxMaster).filter(TaxMaster.name.ilike(name.strip())).first()

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        qry = db.query(TaxMaster)
        if q:
            qry = qry.filter(TaxMaster.name.ilike(f"%{q}%"))
        return qry.order_by(TaxMaster.name.asc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj: TaxMaster):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: TaxMaster):
        db.commit()
        db.refresh(obj)
        return obj