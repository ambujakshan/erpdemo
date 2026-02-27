from sqlalchemy.orm import Session
from .models import Uom

class UomRepo:
    def get_by_id(self, db: Session, id: int):
        return db.query(Uom).filter(Uom.id == id).first()

    def get_by_name(self, db: Session, name: str):
        return db.query(Uom).filter(Uom.name.ilike(name.strip())).first()

    def list(self, db: Session, q: str | None, skip: int, limit: int):
        query = db.query(Uom)
        if q:
            query = query.filter(Uom.name.ilike(f"%{q}%"))
        return query.order_by(Uom.name.asc()).offset(skip).limit(limit).all()

    def create(self, db: Session, obj: Uom):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, obj: Uom):
        db.commit()
        db.refresh(obj)
        return obj